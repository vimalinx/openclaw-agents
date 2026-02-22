# 小红书自动化闭环 - 快速配置指南

本文档提供快速配置步骤，帮助你快速启动小红书自动化闭环系统。

---

## 🚀 快速开始（5 分钟）

### 1. 启动 Chrome 远程调试

```bash
# 方式 1: 临时启动（关闭浏览器后失效）
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug

# 方式 2: 后台启动（持续运行）
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug > /dev/null 2>&1 &
```

### 2. 登录小红书

在已启动的 Chrome 浏览器中：
1. 访问 `https://www.xiaohongshu.com`
2. 扫码或密码登录
3. 确保登录成功

### 3. 验证 CDP 连接

```bash
curl http://localhost:9222/json/version
```

**预期输出**: JSON 格式的 Chrome 版本信息

### 4. 运行测试

```bash
cd /home/vimalinx/.openclaw/workspace
python3 xhs-auto-pipeline.py test
```

---

## 🔑 配置图像生成 API（10 分钟）

### 1. 获取火山引擎豆包绘图 API 密钥

1. 访问 [火山引擎控制台](https://console.volcengine.com/ark)
2. 注册/登录账号
3. 开通豆包绘图服务
4. 创建 API 密钥
5. 复制 API 密钥

### 2. 配置环境变量

```bash
# 临时配置（当前会话）
export VOLCENGINE_API_KEY="your_api_key_here"

# 永久配置（推荐）
echo 'export VOLCENGINE_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. 验证配置

```python
import os
print("API 密钥已配置" if os.environ.get("VOLCENGINE_API_KEY") else "API 密钥未配置")
```

---

## 📦 安装依赖（5 分钟）

```bash
# MediaCrawler 依赖
cd /home/vimalinx/.openclaw/skills/media-crawler
pip install -r requirements.txt

# XHS Auto Publisher 依赖
cd /home/vimalinx/.openclaw/skills/xhs-auto-publisher
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

---

## 🧪 完整测试（2 分钟）

```bash
# 运行技能可用性测试
cd /home/vimalinx/.openclaw/workspace
python3 test-xhs-skills-v2.py

# 运行主脚本测试
python3 xhs-auto-pipeline.py test
```

---

## 📚 常用命令

```bash
# 测试技能可用性
python3 test-xhs-skills-v2.py

# 测试主脚本
python3 xhs-auto-pipeline.py test

# 查看 CDP 状态
curl http://localhost:9222/json/version

# 检查环境变量
echo $VOLCENGINE_API_KEY

# 查看 Chrome 进程
ps aux | grep chrome
```

---

## ⚠️ 常见问题

### Q1: Chrome CDP 无法连接

**症状**: `curl: Connection refused`

**解决方案**:
```bash
# 检查 Chrome 是否运行
ps aux | grep chrome

# 检查端口是否被占用
netstat -tlnp | grep 9222

# 重新启动 Chrome CDP
pkill -f "chrome.*remote-debugging"
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
```

### Q2: Playwright 浏览器未安装

**症状**: `Executable doesn't exist at /path/to/chromium`

**解决方案**:
```bash
playwright install chromium
```

### Q3: API 密钥未配置

**症状**: `API 密钥: ❌ 未配置`

**解决方案**:
```bash
# 配置环境变量
export VOLCENGINE_API_KEY="your_api_key_here"

# 验证
python3 -c "import os; print(os.environ.get('VOLCENGINE_API_KEY'))"
```

### Q4: 小红书登录失效

**症状**: 无法访问笔记数据

**解决方案**:
1. 在 Chrome 中访问 `https://www.xiaohongshu.com`
2. 重新登录
3. 确保登录状态持久化（使用 `--user-data-dir`）

---

## 📖 下一步

完成快速配置后，建议：

1. ✅ 阅读 [完整测试报告](./XHS_AUTOMATION_TEST_REPORT.md)
2. ✅ 查看各技能的 SKILL.md 文档
3. ✅ 尝试集成实际技能到主脚本
4. ✅ 实现数据反馈功能
5. ✅ 添加定时任务

---

## 📞 支持

如有问题，请查看：
- [MediaCrawler SKILL.md](../skills/media-crawler/SKILL.md)
- [XHS Auto Publisher SKILL.md](../skills/xhs-auto-publisher/SKILL.md)
- [完整测试报告](./XHS_AUTOMATION_TEST_REPORT.md)

---

**最后更新**: 2026-02-20
