# 配置 Wilson 的 LLM API

browser-use 支持多种 LLM provider。选择一个配置：

## 选项 1：OpenAI（或兼容服务）

```bash
# .env 文件
OPENAI_API_KEY=sk-xxxxx
OPENAI_BASE_URL=https://api.openai.com/v1  # 可选，默认 OpenAI
```

**兼容服务示例：**
- DeepSeek: `https://api.deepseek.com/v1`
- Together: `https://api.together.xyz/v1`
- 本地 Ollama: `http://localhost:11434/v1`

## 选项 2：本地模型（Ollama）

```bash
# 安装 Ollama
sudo pacman -S ollama
ollama serve &

# 拉取模型
ollama pull qwen2.5:7b  # 或其他模型

# .env 配置
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=not-needed
```

## 选项 3：ChatBrowserUse（推荐）

专为浏览器任务优化，速度快 3-5 倍

```bash
# 注册获取 API key
# https://cloud.browser-use.com/new-api-key
# 新用户有 $10 免费额度

# .env 配置
BROWSER_USE_API_KEY=bup-xxxxx
```

然后修改 wilson_agent.py 使用 ChatBrowserUse：
```python
from browser_use import ChatBrowserUse
llm = ChatBrowserUse()
```

## 快速测试

```bash
# 方式 1：命令行任务
cd /home/vimalinx/.openclaw/workspace/browser-use-test
uv run wilson_agent.py "访问 example.com 并告诉我标题"

# 方式 2：运行内置示例
uv run wilson_agent.py
```

## Wilson 建议

如果你有 OpenAI API key，用那个最简单。
如果想省钱，用本地 Ollama。
如果追求最佳性能，用 ChatBrowserUse。
