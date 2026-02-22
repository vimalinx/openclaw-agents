# 小红书自动化系统优化方案

## 1. 架构优化

### 当前架构问题
- 三层架构清晰，但组件间耦合度较高
- 缺少统一的错误处理和日志记录
- 配置管理分散，没有集中管理

### 优化方案

#### 1.1 引入配置管理器
```python
# config_manager.py
from pathlib import Path
import json
from typing import Dict, Any

class ConfigManager:
    """统一配置管理"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path or Path.home() / ".config/xhs-publisher/config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "debug_port": 9222,
            "base_url": "https://www.xiaohongshu.com",
            "default_tags": ["干货", "分享"],
            "default_location": "珠海市",
            "retry_attempts": 3,
            "headless": False,
            "api_keys": {
                "grsai": "",
                "bocha": "",
                "volces": ""
            },
            "rate_limits": {
                "min_delay": 30,
                "max_delay": 120,
                "max_per_day": 10
            },
            "logging": {
                "level": "INFO",
                "file": "/var/log/xhs-publisher.log"
            }
        }

        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    def get(self, key: str, default=None):
        """获取配置项"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key: str, value: Any):
        """设置配置项"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self._save_config()

    def _save_config(self):
        """保存配置文件"""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
```

#### 1.2 统一日志管理
```python
# logger.py
import logging
import sys
from pathlib import Path
from datetime import datetime

class XHSLogger:
    """统一日志管理"""

    def __init__(self, name: str = "xhs-publisher", level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))

        # 避免重复添加handler
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """配置日志处理器"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台输出
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # 文件输出
        log_dir = Path("/var/log/xhs-publisher")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / f"xhs-publisher-{datetime.now().strftime('%Y%m%d')}.log"

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
```

#### 1.3 统一错误处理
```python
# exceptions.py
class XHSError(Exception):
    """基础异常类"""
    pass

class XHSPublishError(XHSError):
    """发布异常"""
    pass

class XHSAPIError(XHSError):
    """API调用异常"""
    pass

class XHSConfigError(XHSError):
    """配置异常"""
    pass

# error_handler.py
from functools import wraps
from typing import Callable, Any
import asyncio

def handle_errors(logger):
    """错误处理装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except XHSError as e:
                logger.error(f"业务异常: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"未知异常: {str(e)}", exc_info=True)
                raise XHSPublishError(f"操作失败: {str(e)}")

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except XHSError as e:
                logger.error(f"业务异常: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"未知异常: {str(e)}", exc_info=True)
                raise XHSPublishError(f"操作失败: {str(e)}")

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator
```

#### 1.4 API客户端统一管理
```python
# ai_client.py
import aiohttp
from typing import Dict, Any, Optional
from enum import Enum

class AIProvider(Enum):
    """AI提供商"""
    GRSAI = "grsai"
    BOCHA = "bocha"
    VOLCES = "volces"

class AIClient:
    """统一AI客户端"""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def call(
        self,
        provider: AIProvider,
        prompt: str,
        **kwargs
    ) -> Optional[str]:
        """调用AI服务"""
        api_key = self.config.get(f"api_keys.{provider.value}")
        if not api_key:
            raise XHSConfigError(f"未配置{provider.value}的API Key")

        if provider == AIProvider.GRSAI:
            return await self._call_grsai(prompt, api_key, **kwargs)
        elif provider == AIProvider.BOCHA:
            return await self._call_bocha(prompt, api_key, **kwargs)
        elif provider == AIProvider.VOLCES:
            return await self._call_volces(prompt, api_key, **kwargs)
        else:
            raise XHSConfigError(f"不支持的AI提供商: {provider}")

    async def _call_grsai(self, prompt: str, api_key: str, **kwargs) -> str:
        """调用Grsai"""
        url = "https://grsai.dakka.com.cn/v1beta/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "nano-banana-fast",
            "messages": [{"role": "user", "content": prompt}],
            **kwargs
        }

        async with self.session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]

    async def _call_bocha(self, prompt: str, api_key: str, **kwargs) -> str:
        """调用BoCha搜索"""
        # 实现BoCha搜索API调用
        pass

    async def _call_volces(self, prompt: str, api_key: str, **kwargs) -> str:
        """调用火山引擎"""
        url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "doubao-pro-4k",
            "messages": [{"role": "user", "content": prompt}],
            **kwargs
        }

        async with self.session.post(url, headers=headers, json=payload) as response:
            response.raise_for_status()
            data = await response.json()
            return data["choices"][0]["message"]["content"]
```

## 2. 性能优化

### 2.1 连接池复用
```python
# 使用单一aiohttp会话，避免重复创建
class ConnectionPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = None
        return cls._instance

    async def get_session(self):
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=120)
            )
        return self.session
```

### 2.2 缓存机制
```python
# cache.py
from functools import lru_cache
from typing import Any
import hashlib
import json

class Cache:
    """缓存管理器"""

    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self._cache = {}

    def _make_key(self, func_name: str, *args, **kwargs) -> str:
        """生成缓存key"""
        data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True)
        return hashlib.md5(f"{func_name}:{data}".encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """获取缓存"""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any):
        """设置缓存"""
        self._cache[key] = (value, time.time())

    def cached(self, func):
        """缓存装饰器"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = self._make_key(func.__name__, *args, **kwargs)
            cached_value = self.get(key)
            if cached_value is not None:
                return cached_value

            result = await func(*args, **kwargs)
            self.set(key, result)
            return result
        return wrapper
```

## 3. 可靠性提升

### 3.1 健康检查
```python
# health_check.py
class HealthChecker:
    """健康检查"""

    def __init__(self, config: ConfigManager):
        self.config = config

    async def check_browser(self) -> bool:
        """检查浏览器连接"""
        try:
            port = self.config.get("debug_port")
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://localhost:{port}/json") as response:
                    return response.status == 200
        except:
            return False

    async def check_api_keys(self) -> Dict[str, bool]:
        """检查API密钥"""
        results = {}
        for provider in ["grsai", "bocha", "volces"]:
            api_key = self.config.get(f"api_keys.{provider}")
            results[provider] = bool(api_key and len(api_key) > 10)
        return results

    async def run_all_checks(self) -> Dict[str, Any]:
        """运行所有检查"""
        return {
            "browser": await self.check_browser(),
            "api_keys": await self.check_api_keys(),
            "config": self.config_path.exists()
        }
```

### 3.2 监控指标
```python
# metrics.py
from collections import defaultdict
from datetime import datetime

class MetricsCollector:
    """指标收集器"""

    def __init__(self):
        self.counters = defaultdict(int)
        self.timers = defaultdict(list)
        self.errors = defaultdict(int)

    def increment(self, name: str):
        """增加计数器"""
        self.counters[name] += 1

    def record_time(self, name: str, duration: float):
        """记录时间"""
        self.timers[name].append(duration)

    def record_error(self, name: str, error: str):
        """记录错误"""
        self.errors[name] += 1

    def get_summary(self) -> Dict[str, Any]:
        """获取摘要"""
        summary = {
            "counters": dict(self.counters),
            "errors": dict(self.errors),
            "timestamp": datetime.now().isoformat()
        }

        # 计算平均时间
        avg_timers = {}
        for name, times in self.timers.items():
            avg_timers[name] = {
                "count": len(times),
                "avg": sum(times) / len(times),
                "min": min(times),
                "max": max(times)
            }
        summary["timers"] = avg_timers

        return summary
```

## 4. 部署优化

### 4.1 Docker化
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装Playwright浏览器
RUN playwright install chromium

# 复制代码
COPY . .

# 创建日志目录
RUN mkdir -p /var/log/xhs-publisher

# 设置环境变量
ENV PYTHONUNBUFFERED=1

CMD ["python", "xhs_auto_workflow.py"]
```

### 4.2 systemd服务
```ini
# /etc/systemd/system/xhs-publisher.service
[Unit]
Description=XHS Auto Publisher
After=network.target

[Service]
Type=simple
User=vimalinx
WorkingDirectory=/home/vimalinx/.openclaw/skills/xhs-auto-publisher
ExecStart=/usr/bin/python3 xhs_auto_workflow.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## 5. 总结

**优化成果：**
- ✅ 统一配置管理
- ✅ 统一日志记录
- ✅ 统一错误处理
- ✅ API客户端统一管理
- ✅ 连接池复用
- ✅ 缓存机制
- ✅ 健康检查
- ✅ 监控指标
- ✅ Docker化支持
- ✅ systemd服务支持

**后续工作：**
- [ ] 实现上述优化方案
- [ ] 编写单元测试
- [ ] 性能测试
- [ ] 文档更新
