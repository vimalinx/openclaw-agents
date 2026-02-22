# Wilson 的 browser-use 测试环境

## 安装状态
✅ browser-use v0.11.9 已安装
✅ langchain-openai 已安装
⚠️  Playwright 浏览器依赖需要手动安装（需要 sudo）

## 使用方法

### 1. 安装 Playwright 依赖（需要 sudo）

```bash
# Arch Linux 系统依赖
sudo pacman -S --noconfirm \
  alsa-lib at-spi2-atk at-spi2-core gtk3 libdrm \
  libxkbcommon mesa nss cups libsecret \
  xorg-xrandr xorg-xprop xorg-xvfb
```

或者尝试不使用系统依赖，直接运行（可能有限制）

### 2. 配置 LLM

需要配置一个 LLM provider。选项：

**A. 使用 ChatBrowserUse（推荐，专为浏览器优化）**
```bash
# 获取 API key: https://cloud.browser-use.com/new-api-key
export BROWSER_USE_API_KEY=your-key-here
```

**B. 使用 OpenAI**
```bash
export OPENAI_API_KEY=your-key-here
```

**C. 使用本地 LLM（Ollama 等）**
修改脚本使用本地 endpoint

### 3. 运行测试

```bash
cd /home/vimalinx/.openclaw/workspace/browser-use-test
uv run wilson_test.py
```

## 可用脚本

- `test_browser.py` - 基础测试脚本
- `wilson_test.py` - Wilson 的测试脚本（支持自定义 LLM）
- `default/default_template.py` - 官方默认模板

## CLI 快速使用

```bash
# 打开浏览器
uvx browser-use open https://www.example.com

# 查看页面状态
uvx browser-use state

# 点击元素
uvx browser-use click <index>

# 输入文本
uvx browser-use type "text here"

# 截图
uvx browser-use screenshot page.png

# 关闭浏览器
uvx browser-use close
```

## 集成到 OpenClaw

可以将 browser-use 添加为 Wilson 的技能，让自动化浏览器操作更容易。

## 注意事项

- Playwright 在 Arch 上不是官方支持，可能需要额外配置
- 可以考虑使用 Docker 或 cloud 版本获得更好的兼容性
- ChatBrowserUse 模型针对浏览器任务优化，速度更快

## 下一步

1. 装好系统依赖后测试运行
2. 配置好 LLM API key
3. 尝试更复杂的任务（填表、购物、信息收集等）

---

🐺 Wilson - 你的 AI 助手
