# Browser-Use 小红书发布问题 - Debug 报告

## 执行时间
2026-02-16 21:30+

## 测试结果

### ✅ 测试 1: Qwen API 响应时间

| 测试类型 | 响应时间 | 状态 |
|---------|---------|------|
| 简单请求 (Hello) | 0.70秒 | ✅ 正常 |
| 复杂请求 (HTML分析) | 2.55秒 | ✅ 正常 |
| 超长请求 (页面分析) | 1.54秒 | ✅ 正常 |

**结论**: Qwen API 响应时间完全正常，不是超时原因。

### ✅ 测试 2: Agent 配置参数

```python
# 默认配置
llm_timeout: None      # LLM 调用超时（无限制，使用 OpenAI 默认）
step_timeout: 180       # 每步超时 3 分钟
```

**问题**: 实际运行时显示 75 秒超时，说明有其他地方设置了更短的超时。

### ❌ 测试 3: 实际页面导航

**发现的问题**:

1. **未登录拦截**
   ```
   INFO 页面仍为空，SPA可能未加载完成或需先登录。
   INFO 当前有两个标签页，均重定向至登录页（Tab 41AD 和 Tab 554A），
        说明发布页面因未登录被拦截。
   ```

2. **登录流程复杂**
   ```
   INFO 需先完成登录流程。当前登录页已加载，可见短信登录入口、
        手机号输入框、验证码输入框和登录按钮。
   INFO 但尚未提供账号密码，且无用户输入凭证。
   ```

3. **AI 陷入分析循环**
   - AI 不断分析登录页面的各种可能性
   - 尝试找到扫码登录、快捷登录等方式
   - 但没有凭据，无法完成登录

## 根本原因分析

### 1️⃣ 主要问题：未登录

**现象**:
- 小红书创作者平台 (`creator.xiaohongshu.com`) 需要登录才能访问
- 未登录时，所有发布相关页面都会重定向到登录页
- Browser-Use 无法自动完成登录（需要手机号+验证码）

**影响**:
- AI 浪费时间分析登录页面
- 每次尝试导航到发布页面都会被重定向
- 形成死循环：导航 → 重定向 → 分析 → 尝试登录 → 失败

### 2️⃣ 次要问题：超时设置不一致

**现象**:
- 配置显示 `llm_timeout=None`, `step_timeout=180`（3分钟）
- 但实际运行显示 `LLM call timed out after 75 seconds`

**可能原因**:
1. OpenAI 客户端内部有默认 75 秒超时
2. Browser-Use 在某个环节覆盖了配置
3. CDP 协议层有超时限制

### 3️⃣ 页面复杂度

**小红书创作者平台特点**:
- 单页应用 (SPA)
- 需要身份认证
- 动态加载内容
- 大量 JavaScript 执行

**对 Browser-Use 的影响**:
- 需要等待页面加载完成
- 需要处理重定向
- 需要识别登录状态

## 解决方案

### 🎯 方案 1: 手动登录后自动化（推荐）

**步骤**:
1. 手动打开浏览器并登录小红书
2. 保存浏览器配置文件 (Chrome profile)
3. 使用保存的配置文件运行 Browser-Use

**代码**:
```python
browser = Browser(
    headless=False,
    # 使用已登录的 Chrome profile
    profile_path="/home/vimalinx/.config/chromium",  # 修改为实际路径
)
```

**优点**:
- 无需修改登录逻辑
- 可以长期使用（保存登录状态）
- 简单直接

**缺点**:
- 首次需要手动登录

### 🎯 方案 2: 使用 ChatBrowserUse（官方推荐）

**步骤**:
1. 注册 https://cloud.browser-use.com
2. 获取 API Key（新用户有 $10 免费额度）
3. 修改代码使用 ChatBrowserUse

**代码**:
```python
from browser_use import ChatBrowserUse

llm = ChatBrowserUse()  # 专门优化的模型
browser = Browser(headless=False)

agent = Agent(
    task="...",
    llm=llm,
    browser=browser,
)
```

**优点**:
- 专为浏览器自动化优化
- 响应快 3-5 倍
- 准确率更高
- 更好的登录/认证处理

**缺点**:
- 需要付费 API（虽然有免费额度）

### 🎯 方案 3: 增加超时时间（临时方案）

**代码**:
```python
llm = ChatOpenAI(
    model="qwen-plus",
    api_key="...",
    base_url="...",
    timeout=600,  # 增加到 10 分钟
)

agent = Agent(
    task="...",
    llm=llm,
    browser=browser,
    llm_timeout=600,  # LLM 超时 10 分钟
    step_timeout=600,  # 每步超时 10 分钟
)
```

**优点**:
- 无需额外成本
- 配置简单

**缺点**:
- 不能解决登录问题
- 只是延长等待时间，不是根本解决方案

### 🎯 方案 4: 简化任务 - 跳过导航步骤

**思路**:
- 假设用户已经手动打开并登录了发布页面
- Browser-Use 只负责填写表单和点击发布

**代码**:
```python
agent = Agent(
    task="""
    任务：填写并发布小红书笔记

    步骤：
    1. 点击标题输入框
    2. 输入标题："🤖 认识一下你的AI助手 Wilson"
    3. 点击内容输入框
    4. 输入内容："..."
    5. 点击发布按钮

    注意：假设已经在发布页面，不需要导航或登录。
    """,
    llm=llm,
    browser=browser,
)
```

**优点**:
- 跳过复杂的导航和登录
- 只做简单的表单填写
- 100% 可控

**缺点**:
- 需要手动打开页面
- 不完全自动化

## 推荐执行方案

### 对于本次任务（立即发布 Wilson 介绍笔记）

**使用方案 4 + 手动辅助**:
1. 手动打开浏览器，访问 https://creator.xiaohongshu.com/publish/publish
2. 手动登录
3. 运行简化的 Browser-Use 脚本，只负责填写表单

### 对于长期自动化（未来频繁发布）

**使用方案 1（保存 Chrome Profile）**:
1. 手动登录一次，保存配置文件
2. 使用方案 1 的代码长期自动化

**或者使用方案 2（ChatBrowserUse）**:
- 如果预算允许，这是最佳方案
- 专门优化的模型，性能最好

## 下一步行动

请选择一个方案：

1. **快速发布** - 我给你手动操作指南
2. **保存 Profile** - 我帮你配置 Chrome profile
3. **获取 ChatBrowserUse** - 我指导你注册和配置

---

## 总结

**问题核心**: 未登录导致无法访问创作者平台，AI 陷入登录分析的死循环。

**Qwen API 性能**: 完全正常，不是问题。

**最佳解决方案**:
- 短期：方案 4（手动打开页面，AI 只负责填写）
- 长期：方案 1（保存 Chrome Profile）或 方案 2（ChatBrowserUse）
