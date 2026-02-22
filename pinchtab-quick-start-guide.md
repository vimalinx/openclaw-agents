# Pinchtab 使用指南 - 快速开始

> 生成时间: 2026-02-20 23:20
> 状态: 已安装 ✅

---

## 📋 当前状态

**Pinchtab 版本**: v0.5.1
**安装位置**: `/home/vimalinx/pinchtab`
**服务端口**: 9867
**服务状态**: ✅ 正常运行

---

## 🚀 快速开始

### 第 1 步：验证服务运行

**检查 Pinchtab 是否在运行**：

```bash
# 方法 1: 检查端口
netstat -tuln | grep 9867

# 方法 2: 测试健康接口
curl http://localhost:9867/health
```

**预期输出**：
```json
{
  "status": "ok",
  "version": "0.5.1",
  "chromeConnected": false,
  "sessions": 0
}
```

---

## 📖 使用示例

### 示例 1：导航到网页

**目标**: 导航到 Google

```bash
curl -X POST http://localhost:9867/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

**预期输出**：
```json
{
  "result": "success",
  "url": "https://www.google.com"
}
```

---

### 示例 2：获取页面快照

**目标**: 获取当前页面的无障碍树

```bash
curl http://localhost:9867/snapshot
```

**预期输出**：
```json
{
  "url": "https://www.google.com",
  "title": "Google",
  "tree": {
    "role": "document",
    "name": "",
    "children": [...]
  }
}
```

---

### 示例 3：提取页面文本

**目标**: 提取可读文本（比快照省 92% tokens）

```bash
curl http://localhost:9867/text
```

**预期输出**：
```json
{
  "text": "Google 搜索...",
  "url": "https://www.google.com",
  "format": "text"
}
```

---

### 示例 4：执行 JavaScript 代码

**目标**: 在页面中执行 JavaScript

```bash
curl -X POST http://localhost:9867/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "document.title"
  }'
```

**预期输出**：
```json
{
  "result": "Google",
  "type": "string"
}
```

---

### 示例 5：截图（可选）

**目标**: 截取当前页面

```bash
curl http://localhost:9867/screenshot -o screenshot.jpg
```

**预期输出**：
- 文件 `screenshot.jpg` 会保存到当前目录

---

### 示例 6：查看标签页

**目标**: 查看所有打开的标签页

```bash
curl http://localhost:9867/tabs
```

**预期输出**：
```json
{
  "tabs": [
    {
      "id": "tab-1",
      "url": "https://www.google.com",
      "title": "Google"
    }
  ]
}
```

---

## 🔧 高级用法

### 隐身模式（绕过 Bot 检测）

Pinchtab 内置了隐身模式，可以自动：
- 修改 `navigator.webdriver`
- 欺骗 User-Agent
- 隐藏自动化标志

**用法**：默认已启用，无需额外配置

---

### 会话持久化

Pinchtab 可以自动保存：
- Cookies
- 登录状态
- 标签页状态

**好处**：跨重启保持登录状态

---

### 智能过滤（节省 75% tokens）

**用法**：添加 `?filter=interactive` 参数

```bash
# 只返回按钮、链接、输入框
curl "http://localhost:9867/snapshot?filter=interactive"
```

**优势**：
- 减少输出大小
- 节省 tokens 成本
- 只保留交互元素

---

## 💻 实战案例

### 案例 1：监控网页变化

**目标**: 每 10 秒检查一次网页快照，检测变化

```bash
# 第一次快照
curl http://localhost:9867/snapshot > snapshot1.json

# 等待 10 秒
sleep 10

# 第二次快照
curl http://localhost:9867/snapshot > snapshot2.json

# 对比差异（手动或使用 diff 工具）
diff snapshot1.json snapshot2.json
```

---

### 案例 2：批量搜索

**目标**: 搜索多个关键词

```bash
# 搜索关键词列表
keywords=("AI工具" "效率神器" "副业搞钱")

# 循环搜索
for keyword in "${keywords[@]}"; do
  echo "搜索: $keyword"
  curl -X POST http://localhost:9867/navigate \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"https://www.google.com/search?q=$keyword\"}"
  sleep 2
  curl http://localhost:9867/text > "${keyword}_results.txt"
done
```

---

### 案例 3：自动化登录

**目标**: 自动填写登录表单

```bash
# 1. 导航到登录页面
curl -X POST http://localhost:9867/navigate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/login"}'

# 2. 填写表单（需要先分析页面）
curl -X POST http://localhost:9867/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "expression": "document.querySelector(\"input[name=\"username\"]\").value = \"your_username\""
  }'

# 3. 点击登录按钮
curl -X POST http://localhost:9867/actions \
  -H "Content-Type: application/json" \
  -d '{
    "type": "click",
    "selector": "button[type=\"submit\"]"
  }'
```

---

## 📊 性能优势

### 对比：Pinchtab vs 传统浏览器自动化

| 特性 | Pinchtab | Playwright | Selenium |
|------|----------|-----------|----------|
| 安装难度 | ⭐ 极简 | ⭐⭐⭐ 复杂 | ⭐⭐ 中等 |
| Token/页 | ~800 | 10,000+ | 10,000+ |
| 启动速度 | 30 秒 | 2-5 分钟 | 1-3 分钟 |
| 隐身模式 | ✅ 内置 | ⚠️ 插件 | ⚠️ 插件 |
| 跨语言 | ✅ 任何语言 | Python only | Python/Java |

---

## 🎯 推荐使用场景

1. **AI Agent 浏览器自动化**
   - 使用 `/text` 接口（节省 92% tokens）
   - 使用 `?filter=interactive`（节省 75% tokens）

2. **快速原型开发**
   - 30 秒安装，零配置启动
   - 即插即用

3. **Token 成本敏感项目**
   - 大幅降低 API 调用成本
   - 比截图工具便宜 10 倍以上

4. **需要隐身能力**
   - 内置反 Bot 检测
   - 无需额外配置

---

## 🔍 故障排除

### 问题 1：服务未响应

**症状**: `curl: (7) Failed to connect`

**解决方案**：
```bash
# 1. 检查 Pinchtab 是否在运行
ps aux | grep pinchtab

# 2. 重新启动 Pinchtab
./pinchtab &

# 3. 检查端口是否正确
netstat -tuln | grep 9867
```

---

### 问题 2：Chrome 实例未连接

**症状**: API 返回 `"chromeConnected": false`

**解决方案**：
```bash
# Pinchtab 会自动启动 Chrome
# 如果 Chrome 未启动，请检查：
# 1. Chrome 是否已安装
which google-chrome

# 2. Pinchtab 配置
# 查看 ~/.pinchtab/ 目录
ls -la ~/.pinchtab/
```

---

### 问题 3：API 返回错误

**症状**: `{"error": "..."}`

**解决方案**：
```bash
# 1. 检查 URL 格式
# 2. 检查 JSON 格式
# 3. 查看详细错误日志
cat ~/.pinchtab/pinchtab.log
```

---

## 📝 常用命令速查

```bash
# 健康检查
curl http://localhost:9867/health

# 获取快照
curl http://localhost:9867/snapshot

# 获取文本
curl http://localhost:9867/text

# 获取标签页
curl http://localhost:9867/tabs

# 导航
curl -X POST http://localhost:9867/navigate -d '{"url": "https://example.com"}'

# 执行 JS
curl -X POST http://localhost:9867/evaluate -d '{"expression": "document.title"}'

# 截图
curl http://localhost:9867/screenshot -o screenshot.jpg
```

---

## ✅ 准备好了

**Pinchtab 已安装并运行** ✅
**所有 API 接口正常** ✅
**详细的使用指南已准备** ✅

**现在可以开始使用了！**

---

**💡 建议**：

1. **从简单开始** - 先测试导航和快照
2. **逐步进阶** - 尝试执行 JavaScript 和自动化表单
3. **关注 Token 成本** - 使用 `/text` 而非 `/snapshot`
4. **使用智能过滤** - 需要交互元素时用 `?filter=interactive`

---

**准备好了吗？** 🐺

可以开始使用 Pinchtab 了！有任何问题随时告诉我！
