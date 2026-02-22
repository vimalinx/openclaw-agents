# 使用 GLM-4 配置 browser-use

## 发现的配置

从 OpenClaw 配置中找到：

- **Provider:** ZAI (智谱 AI)
- **Base URL:** `https://open.bigmodel.cn/api/coding/paas/v4`
- **Model:** `glm-4.7` (或 glm-4-plus, glm-4-flash 等)
- **API Key (部分):** `9ac45d...I2f54T`

## 需要完整的 API Key

要使用 GLM-4，需要完整的 API key。有几种方式获取：

### 方法 1：从 OpenClaw 运行时获取

运行以下命令查看完整 key：

```bash
# 查看 session 状态（显示部分 key）
openclaw status

# 或者直接读取配置
cat ~/.openclaw/openclaw.json | jq -r '.auth.profiles["zai:default"].apiKey'
```

### 方法 2：从智谱 AI 控制台获取

访问：https://open.bigmodel.cn/usercenter/apikeys

### 方法 3：使用环境变量

```bash
# 导出 API key（替换为完整 key）
export OPENAI_API_KEY=你的完整GLM_API_KEY
export OPENAI_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
```

## 配置 .env 文件

编辑 `.env` 文件：

```bash
cd /home/vimalinx/.openclaw/workspace/browser-use-test
nano .env  # 或使用其他编辑器
```

添加：

```env
OPENAI_API_KEY=你的完整GLM_API_KEY
OPENAI_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
```

## 测试运行

```bash
# 1. 确保 API key 已配置
cat .env | grep OPENAI

# 2. 运行测试
uv run test_glm.py

# 3. 或直接运行 agent
uv run wilson_agent.py "访问 example.com 并告诉我标题"
```

## GLM-4 模型选择

智谱 AI 提供多个版本：

- `glm-4.7` - 默认，平衡性能和成本
- `glm-4-plus` - 更强大
- `glm-4-flash` - 更快，适合简单任务
- `glm-4-air` - 轻量级

可以在脚本中修改 `model="glm-4.7"` 来切换。

## 备选方案

如果获取 API key 有困难，可以：

1. **使用 ChatBrowserUse** - 新用户有 $10 免费额度
2. **使用本地 Ollama** - 完全免费，但需要拉取模型
3. **使用 OpenAI** - 如果有 OpenAI API key

---

🐺 Wilson - 等待完整 API key 来测试
