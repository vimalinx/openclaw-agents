#!/bin/bash
# 老板助理子代理完整打包脚本

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE} 老板助理子代理打包脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 配置
BACKUP_DIR="/home/vimalinx/.openclaw/subagent-backup-$(date +%Y%m%d)"
PACKAGE_DIR="/home/vimalinx/.openclaw/subagent-package-$(date +%Y%m%d)"

echo -e "${GREEN}备份目录：${BACKUP_DIR}${NC}"
echo -e "${GREEN}打包目录：${PACKAGE_DIR}${NC}"
echo ""

# 创建目录
mkdir -p "$BACKUP_DIR"
mkdir -p "$PACKAGE_DIR"

# ============================================
# 1. 备份子代理配置
# ============================================
echo -e "${BLUE}[1/5] 备份子代理配置...${NC}"

# 备份 main 子代理（默认）
if [ -d "/home/vimalinx/.openclaw/agents/main" ]; then
    cp -r "/home/vimalinx/.openclaw/agents/main" "$PACKAGE_DIR/subagent-main/"
    echo -e "  ${GREEN}✓ main 子代理${NC}"
fi

# 备份 feishu-bot 子代理
if [ -d "/home/vimalinx/.openclaw/agents/feishu-bot" ]; then
    cp -r "/home/vimalinx/.openclaw/agents/feishu-bot" "$PACKAGE_DIR/subagent-feishu-bot/"
    echo -e "  ${GREEN}✓ feishu-bot 子代理${NC}"
fi

# 备份 subagents 配置
if [ -f "/home/vimalinx/.openclaw/subagents.json" ]; then
    cp "/home/vimalinx/.openclaw/subagents.json" "$PACKAGE_DIR/subagents.json"
    echo -e "  ${GREEN}✓ subagents.json${NC}"
fi

echo -e "  ${GREEN}✓ 子代理配置备份完成${NC}"
echo ""

# ============================================
# 2. 提取配置信息
# ============================================
echo -e "${BLUE}[2/5] 提取配置信息...${NC}"

# 提取所有已配置的子代理
cat > "$PACKAGE_DIR/agent-list.txt" << 'EOF'
# 已配置的子代理列表
EOF

cd "/home/vimalinx/.openclaw/agents"

# 遍历所有子代理目录
for agent_dir in */; do
    if [ -d "$agent_dir" ]; then
        agent_name=$(basename "$agent_dir")
        echo "- $agent_name" >> "$PACKAGE_DIR/agent-list.txt"
        
        # 检查是否有配置文件
        if [ -f "$agent_dir/config.json" ]; then
            echo "  - 配置文件: config.json" >> "$PACKAGE_DIR/agent-list.txt"
        fi
        
        # 列出所有 skill 目录
        if [ -d "$agent_dir/skills" ]; then
            skill_count=$(find "$agent_dir/skills" -maxdepth 1 -type d | wc -l)
            echo "  - Skills 数量: $skill_count" >> "$PACKAGE_DIR/agent-list.txt"
        fi
    fi
done

cd "$PACKAGE_DIR"

echo -e "  ${GREEN}✓ 子代理列表生成${NC}"
echo ""

# ============================================
# 3. 创建 README
# ============================================
echo -e "${BLUE}[3/5] 创建 README...${NC}"

cat > README.md << 'EOF'
# 老板助理子代理打包

**打包时间**: $(date '+%Y-%m-%d %H:%M:%S')
**版本**: v1.0

---

## 📦 包含内容

### 子代理配置
\`\`\`subagents.json\`\`\` - 所有已配置的子代理列表
\`\`\`subagent-main/\`\`\` - main 子代理（默认）
\`\`\`subagent-feishu-bot/\`\`\` - feishu-bot 子代理
\`\`\`agent-list.txt\`\`\` - 子代理详细信息

### 配置说明

#### subagents.json 结构
\`\`\`json
{
  "maxConcurrent": 8,
  "list": [
    {
      "id": "main",
      "name": "主代理",
      "default": true
    },
    {
      "id": "feishu-bot",
      "name": "飞书机器人"
    }
  ]
}
\`\`\`

#### bindings 配置
\`\`\`json
{
  "agentId": "main",
  "match": {
    "channel": "feishu",
    "accountId": "*"
  }
}
\`\`\`

---

## 🚀 在新机器上部署

### 步骤 1：传输打包文件
\`\`\`bash
# 使用 SCP 传输
scp -r subagent-package-$(date +%Y%m%d).tar.gz user@new-machine:/tmp/

# 或使用 rsync（推荐）
rsync -avz subagent-package-*/ user@new-machine:~/backup/subagents/
\`\`\`

### 步骤 2：在新机器上解压
\`\`\`bash
# 解压
tar xzf subagent-package-$(date +%Y%m%d).tar.gz
cd subagent-package-*/

# 查看子代理列表
cat agent-list.txt
\`\`\`

### 步骤 3：复制到 OpenClaw
\`\`\`bash
# 复制所有子代理
cp -r subagent-main/ ~/.openclaw/agents/main/
cp -r subagent-feishu-bot/ ~/.openclaw/agents/feishu-bot/

# 或者复制特定子代理
cp -r <子代理名称>/ ~/.openclaw/agents/<子代理名称>/

# 重新加载子代理
openclaw subagents reload
\`\`\`

### 步骤 4：验证部署
\`\`\`bash
# 列出所有子代理
openclaw subagents list

# 查看主代理状态
openclaw subagents status main

# 查看特定子代理状态
openclaw subagents status <子代理ID>
\`\`\`

---

## 🔧 配置和使用

### 切换主代理
\`\`\`bash
# 设置 main 为主代理
openclaw subagents set-default main
\`\`\`

### 查看子代理状态
\`\`\`bash
# 查看所有状态
openclaw subagents list

# 查看主代理
openclaw subagents status main
\`\`\`

### 测试子代理
\`\`\`bash
# 在 Telegram 中测试 feishu-bot
# 在飞书中测试
\`\`\`

---

## 📊 子代理说明

### main（主代理）
- **ID**: main
- **名称**: 主代理
- **默认**: 是
- **功能**: 默认处理所有请求
- **Skills**: 使用 \`\`\`~/.openclaw/skills/\`\`\`

### feishu-bot（飞书机器人）
- **ID**: feishu-bot
- **名称**: 飞书机器人
- **默认**: 否
- **功能**: 专门处理飞书相关请求
- **Skills**: 使用 \`\`\`~/.openclaw/skills/feishu-*/\`\`\`
- **绑定**: 绑定到 \`\`\`channels.feishu\`\`\`

---

## 🎯 老板助理功能

### 飞书机器人功能
- 自动回复消息
- 自动点赞和表情回复
- 自动@提及处理
- 群组自动管理

### 主代理功能
- AI 对话和推理
- Skills 调用
- 工作流自动化
- 会话记忆管理

---

## 📝 配置文件

### 子代理配置
- 位置：\`\`\`~/.openclaw/subagents.json\`\`\`
- 用途：管理所有已配置的子代理
- 结构：列表、默认、最大并发

### Bindings 配置
- 位置：\`\`\`~/.openclaw/openclaw.json > channels > bindings\`\`\`
- 用途：定义子代理与通道的映射关系
- 功能：路由、过滤、默认代理

---

## ⚠️ 注意事项

### 1. 备份建议
在修改任何配置之前，务必备份现有配置：
\`\`\`bash
# 备份 subagents.json
cp ~/.openclaw/subagents.json ~/.openclaw/subagents.json.backup
\`\`\`

### 2. 配置验证
修改配置后，使用 \`\`\`openclaw subagents list\`\`\` 验证配置是否正确

### 3. 测试顺序
建议按以下顺序测试：
1. 部署 main 子代理
2. 测试基本对话功能
3. 部署 feishu-bot 子代理
4. 测试飞书集成
5. 调整 bindings 配置

### 4. 日志查看
如果遇到问题，查看日志：
\`\`\`bash
openclaw logs --follow | grep subagent
\`\`\`

---

## 🚀 常用命令

### 子代理管理
\`\`\`bash
# 列出所有子代理
openclaw subagents list

# 查看主代理状态
openclaw subagents status main

# 重新加载所有子代理
openclaw subagents reload

# 设置默认子代理
openclaw subagents set-default <subagent-id>
\`\`\`

### Bindings 管理
\`\`\`bash
# 列出所有 bindings
openclaw bindings list

# 添加 binding
openclaw bindings add

# 删除 binding
openclaw bindings remove <binding-id>
\`\`\`

### Gateway 管理
\`\`\`bash
# 重启 Gateway
openclaw gateway restart

# 查看状态
openclaw gateway status

# 查看日志
openclaw logs --follow
\`\`\`

---

## 🎯 测试建议

### 基础功能测试
1. 发送测试消息到飞书
2. 验证自动回复是否工作
3. 检查日志确认消息路由
4. 测试多轮对话

### 高级功能测试
1. 测试多个子代理切换
2. 验证 bindings 路由规则
3. 测试并发处理
4. 测试错误处理和恢复

### 性能测试
1. 监控响应时间
2. 测试并发消息处理
3. 查看资源使用情况
4. 优化配置提升性能

---

## 📞 支持和文档

### 官方文档
- OpenClaw 文档: https://docs.openclaw.ai
- 子代理文档: https://docs.openclaw.ai/subagents
- Bindings 文档: https://docs.openclaw.ai/bindings

### 问题排查
1. 查看 Gateway 日志
2. 查看子代理日志
3. 检查配置文件
4. 验证网络连接

---

**打包完成！** 🎉

现在你有了完整的老板助理子代理打包，可以在新机器上部署和测试了！

需要详细说明吗？
EOF

echo -e "  ${GREEN}✓ README.md 创建${NC}"
echo ""

# ============================================
# 4. 创建文件清单
# ============================================
echo -e "${BLUE}[4/5] 创建文件清单...${NC}"

cd "$PACKAGE_DIR"

find . -type f -exec ls -lh {} \; > file_list.txt
find . -type d | sort > directory_structure.txt

echo -e "  ${GREEN}✓ 文件清单生成${NC}"
echo ""

# ============================================
# 5. 创建压缩包
# ============================================
echo -e "${BLUE}[5/5] 创建压缩包...${NC}"

cd "/home/vimalinx/.openclaw"

# 创建 tar.gz 压缩包
tar czf "subagent-boss-assistant-package-$(date +%Y%m%d_%H%M%S).tar.gz" -C "$PACKAGE_DIR" .

# 获取包大小
PACKAGE_SIZE=$(du -sh "subagent-boss-assistant-package-$(date +%Y%m%d_%H%M%S).tar.gz" | cut -f1)
PACKAGE_SIZE_MB=$(echo "scale=2; $PACKAGE_SIZE / 1048576" | bc)

echo -e "  ${GREEN}✓ 压缩包创建${NC}"
echo -e "  ${YELLOW}包大小: ${PACKAGE_SIZE_MB} MB${NC}"
echo ""

# ============================================
# 完成
# ============================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}      老板助理子代理打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📦 备份目录：${NC}"
echo -e "  ${YELLOW}$BACKUP_DIR${NC}"
echo ""
echo -e "${BLUE}📦 打包目录：${NC}"
echo -e "  ${YELLOW}$PACKAGE_DIR${NC}"
echo ""
echo -e "${BLUE}📦 压缩包：${NC}"
echo -e "  ${YELLOW}subagent-boss-assistant-package-$(date +%Y%m%d_%H%M%S).tar.gz${NC}"
echo -e "  ${YELLOW}大小: ${PACKAGE_SIZE_MB} MB${NC}"
echo ""
echo -e "${BLUE}📄 文档：${NC}"
echo -e "  ${YELLOW}README.md${NC}"
echo -e "  ${YELLOW}agent-list.txt${NC}"
echo -e "  ${YELLOW}file_list.txt${NC}"
echo -e "  ${YELLOW}directory_structure.txt${NC}"
echo ""
echo -e "${BLUE}🚀 在新机器上部署的步骤：${NC}"
echo ""
echo -e "${YELLOW}1. 传输打包文件${NC}"
echo -e "     scp -r subagent-boss-assistant-package-*.tar.gz user@new-machine:/tmp/${NC}"
echo ""
echo -e "${YELLOW}2. 在新机器上解压${NC}"
echo -e "     tar xzf subagent-boss-assistant-package-*.tar.gz${NC}"
echo -e "     cd subagent-boss-assistant-package-*/${NC}"
echo ""
echo -e "${YELLOW}3. 复制到 OpenClaw${NC}"
echo -e "     cp -r subagent-main/ ~/.openclaw/agents/main/${NC}"
echo -e "     cp -r subagent-feishu-bot/ ~/.openclaw/agents/feishu-bot/${NC}"
echo -e "     openclaw subagents reload${NC}"
echo ""
echo -e "${YELLOW}4. 验证部署${NC}"
echo -e "     openclaw subagents list${NC}"
echo -e "     openclaw subagents status main${NC}"
echo ""
echo -e "${YELLOW}5. 测试功能${NC}"
echo -e "     在飞书中测试自动回复${NC}"
echo -e "     在 Telegram 中测试${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
