# Algora 赏金任务自动化配置指南

## 📊 当前状态

### 发现的赏金任务
通过 GitHub API 搜索找到了 42 个带有明确赏金的任务。

### 高价值任务（匹配技能栈）

#### 🥇 最高赏金：$3,000
- **标题**: "Bounty - Add Decibel Perpetual Connector"
- **仓库**: hummingbot/hummingbot
- **链接**: https://github.com/hummingbot/hummingbot/issues/8028
- **技术栈**: TypeScript, Playwright, AI/ML, Go
- **匹配度**: ✅ 完全匹配

#### 🥈 第二高：$1,000
- **标题**: "[Enhancement]: Use pgBackRest for Postgres backups"
- **仓库**: coollabsio/coolify
- **链接**: https://github.com/coollabsio/coolify/issues/7423
- **技术栈**: TypeScript, AI/ML, Go
- **匹配度**: ✅ 匹配

#### 🥉 第三高：$402
- **标题**: "[BOUNTY] Claim: Mobile SERP Tracker..."
- **仓库**: bolivian-peru/marketplace-service-template
- **链接**: https://github.com/bolivian-peru/marketplace-service-template/issues/91
- **技术栈**: Python, TypeScript, JavaScript, AI/ML, Go
- **匹配度**: ✅ 匹配

## ⚠️ 重要说明

### Algora API 配置需求

要获取 Algora 官方赏金列表和完整功能，需要以下配置：

#### 1. Algora API Token
获取方式：
1. 访问 https://algora.io 并登录/注册
2. 进入账户设置或 API 设置页面
3. 生成 API Token
4. 配置到环境变量：
   ```bash
   export ALGORA_API_TOKEN="your-token-here"
   ```

#### 2. Algora SDK 安装
```bash
npm install @algora/sdk
```

#### 3. 使用 SDK 查询赏金
```typescript
import { algora } from "@algora/sdk";

// 查询活跃的赏金任务
const { items, next_cursor } = await algora.bounty.list.query({
  status: 'active',
  limit: 100
});
```

## 🔧 当前限制

1. **无法访问 Algora 动态网站** - web_fetch 只能获取静态 HTML
2. **浏览器未启动** - 需要启动 OpenClaw gateway 才能使用浏览器
3. **可能缺少 API token** - 需要用户配置才能访问完整 API

## 🎯 建议的执行方案

### 选项 A：使用当前发现的任务
从 GitHub 搜索的任务中选择一个执行（推荐 $3,000 任务）

### 选项 B：配置 Algora API
获取 API token 后，使用官方 SDK 查找更准确的赏金任务

### 选项 C：启动浏览器
启动 OpenClaw gateway 后，使用浏览器直接访问 Algora 网站

## 📝 执行流程（完整）

对于选定的任务，执行以下步骤：

1. **接取任务**
   - 在 GitHub issue 上评论表示接取
   - 检查是否需要 fork 仓库
   - 查看任务要求和验收标准

2. **克隆代码仓库**
   ```bash
   git clone <repo-url>
   cd <repo-name>
   git checkout -b feature/<task-name>
   ```

3. **完成开发工作**
   - 分析代码结构
   - 实现功能
   - 编写测试
   - 更新文档

4. **提交 PR/MR**
   ```bash
   git add .
   git commit -m "feat: implement <feature>"
   git push origin feature/<task-name>
   # 然后在 GitHub 上创建 PR
   ```

5. **更新任务状态**
   - 在 issue 中更新进度
   - 提交 PR 后通知维护者

6. **领取赏金**
   - 等待 PR 被合并
   - 按照项目赏金流程领取

## 🤖 自动化脚本

项目已创建以下自动化脚本：
- `algora-bounty-finder.js` - 查找 Algora 赏金任务
- `github-bounty-searcher.js` - 搜索 GitHub 赏金任务

## 📋 下一步

请选择：
1. 使用当前发现的 $3,000 任务开始执行
2. 提供 Algora API token 进行更准确的搜索
3. 启动 OpenClaw gateway 使用浏览器访问

## 🔗 相关链接

- Algora 主页: https://algora.io
- Algora SDK: https://github.com/algora-io/sdk
- Algora 文档: https://algora.io/docs
