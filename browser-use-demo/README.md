# Browser-Use 小红书自动发布

## 安装依赖

```bash
# 安装浏览器（需要 sudo 权限）
uvx browser-use install

# 或者使用系统已有的 Chromium
```

## 配置

1. 复制 `.env.example` 为 `.env`
2. 如果使用 Browser-Use Cloud，添加 API Key
3. 如果使用其他 LLM，添加对应的 API Key

## 运行

### 方式一：直接运行脚本

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行脚本
python xhs_poster.py
```

### 方式二：使用 uvx

```bash
uv run python xhs_poster.py
```

### 方式三：交互式命令行

```bash
# 打开小红书
browser-use open https://www.xiaohongshu.com

# 查看页面状态
browser-use state

# 点击元素
browser-use click <index>

# 输入文字
browser-use type "Hello"

# 截图
browser-use screenshot page.png
```

## 注意事项

1. **首次使用需要手动登录**：小红书可能需要扫码或验证码登录
2. **保存登录状态**：可以指定 Chrome profile 路径来保持登录
3. **发布内容检查**：发布前请检查内容是否符合平台规则
4. **频率限制**：避免频繁发布，防止被限流

## 高级用法

### 使用真实 Chrome 配置文件

```python
browser = Browser(
    headless=False,
    # 指定你的 Chrome profile 路径
    # ~/.config/chromium 或 ~/.config/google-chrome
)
```

### 自定义 LLM

```python
from openai import OpenAI

client = OpenAI(api_key="your-api-key")

browser = Browser()
agent = Agent(
    task="你的任务",
    llm=client,
    browser=browser,
)
```

## 参考链接

- [Browser-Use 文档](https://docs.browser-use.com)
- [Browser-Use Cloud](https://cloud.browser-use.com)
- [GitHub 仓库](https://github.com/browser-use/browser-use)
