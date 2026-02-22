#!/bin/bash
# OpenClaw 完整打包和迁移脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  OpenCl 完整打包脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 配置
BACKUP_DIR="/home/vimalinx/.openclaw/openclaw-backup-$(date +%Y%m%d_%H%M%S)"
PACKAGE_DIR="/home/vimalinx/openclaw/openclaw-package-$(date +%Y%m%d_%H%M%S)"

echo -e "${GREEN}备份目录：${BACKUP_DIR}${NC}"
echo -e "${GREEN}打包目录：${PACKAGE_DIR}${NC}"
echo ""

# 创建备份目录
mkdir -p "$BACKUP_DIR"
mkdir -p "$PACKAGE_DIR"

# ============================================
# 1. 备份主配置文件
# ============================================
echo -e "${BLUE}[1/8] 备份主配置文件...${NC}"

# 主配置
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/openclaw.json"

# 配置备份（所有 .bak 文件）
find ~/.openclaw -maxdepth 1 -name "openclaw.json.bak.*" -exec cp {} "$BACKUP_DIR/" \;

echo -e "  ${GREEN}✓ 主配置${NC}"
echo -e "  ${GREEN}✓ 备份配置 ($(find ~/.openclaw -maxdepth 1 -name "openclaw.json.bak.*" | wc -l) 个)${NC}"
echo ""

# ============================================
# 2. 打包 Skills
# ============================================
echo -e "${BLUE}[2/8] 打包 Skills...${NC}"

# 复制整个 skills 目录
cp -r ~/.openclaw/skills "$PACKAGE_DIR/skills/"

echo -e "  ${GREEN}✓ Skills 目录复制完成${NC}"
echo ""

# ============================================
# 3. 打包 Workspace
# ============================================
echo -e "${BLUE}[3/8] 打包 Workspace...${NC}"

# 复制 workspace
cp -r ~/.openclaw/workspace "$PACKAGE_DIR/workspace/"

echo -e "  ${GREEN}✓ Workspace 目录复制完成${NC}"
echo ""

# ============================================
# 4. 打包 Agents
# ============================================
echo -e "${BLUE}[4/8] 打包 Agents...${NC}"

# 复制 agents
cp -r ~/.openclaw/agents "$PACKAGE_DIR/agents/"

echo -e "  ${GREEN}✓ Agents 目录复制完成${NC}"
echo ""

# ============================================
# 5. 打包个性化文件
# ============================================
echo -e "${BLUE}[5/8] 打包个性化文件...${NC}"

# 打包工作区中的报告和配置
find ~/.openclaw/workspace -maxdepth 1 -type f \( -name "*.md" -o -name "*.html" -o -name "*.pdf" -o -name "*.json" \) \
    -exec cp {} "$PACKAGE_DIR/workspace/" \;

echo -e "  ${GREEN}✓ 个性化文件打包 ($(find ~/.openclaw/workspace -maxdepth 1 -type f \( -name "*.md" -o -name "*.html" -o -name "*.pdf" -o -name "*.json" \) | wc -l) 个)${NC}"
echo ""

# ============================================
# 6. 打包环境变量
# ============================================
echo -e "${BLUE}[6/8] 打包环境变量...${NC}"

# 导出 .env 文件（如果存在）
if [ -f ~/.openclaw/.env ]; then
    cp ~/.openclaw/.env "$PACKAGE_DIR/.env"
    echo -e "  ${GREEN}✓ .env 文件${NC}"
fi

# 导出 auth-profiles（如果存在）
if [ -d ~/.openclaw/agents/main/agent ]; then
    cp -r ~/.openclaw/agents/main/agent "$PACKAGE_DIR/auth-profiles/"
    echo -e "  ${GREEN}✓ auth-profiles${NC}"
fi

echo ""

# ============================================
# 7. 创建索引文件
# ============================================
echo -e "${BLUE}[7/8] 创建打包索引...${NC}"

cd "$PACKAGE_DIR"

# 创建文件列表
find . -type f -exec ls -lh {} \; > package_contents.txt

# 创建目录结构树
find . -type d | sort > package_structure.txt

# 创建 README
cat > README.md << 'EOF'
# OpenCl 完整打包

**打包时间**: $(date '+%Y-%m-%d %H:%M:%S')
**机器**: VimalinxG16 (Arch Linux)
**用户**: vimalinx

---

## 📦 目录结构

\`\`\`
find . -type d | sed 's|;   |/|;     /;g' | head -20
\`\`\`

---

## 📋 文件清单

主要配置：
- \`openclaw.json\` - 主配置文件
- \`openclaw.json.bak.*\` - 配置备份

Skills: \`skills/\`
Workspace: \`workspace/\`
Agents: \`agents/\`
环境变量: \`.env\` (如果存在)
认证文件: \`auth-profiles/\`

---

## 🚀 迁移步骤

### 1. 将打包文件夹传输到新机器

\`\`\`bash
# 方式1：通过 SSH 传输
scp -r /home/vimalinx/openclaw/openclaw-package-*.tar.gz user@new-machine:/tmp/

# 方式2：使用 rsync 同步
rsync -avz /home/vimalinx/.openclaw/ user@new-machine:~/backup/

# 方式3：创建 tar.gz 压缩包
cd /home/vimalinx/.openclaw
tar czf openclaw-full-backup-$(date +%Y%m%d).tar.gz openclaw-package-*/
\`\`\`

### 2. 在新机器上解压和恢复

\`\`\`bash
# 解压包
tar xzf openclaw-full-backup-*.tar.gz

# 恢复配置
mkdir -p ~/.openclaw
cp -r openclaw-package-*/.env ~/.openclaw/
cp -r openclaw-package-*/openclaw.json ~/.openclaw/

# 恢复 skills
cp -r openclaw-package-*/skills ~/.openclaw/skills/

# 恢复 workspace
cp -r openclaw-package-*/workspace ~/.openclaw/workspace/

# 恢复 agents
cp -r openclaw-package-*/agents ~/.openclaw/agents/

# 启动 OpenClaw Gateway
openclaw gateway restart
\`\`\`

### 3. 重新安装 OpenClaw

\`\`\`bash
# 使用 npm 全局安装
npm install -g openclaw@latest

# 运行安装向导
openclaw onboard --install-daemon

# 添加通道
openclaw channels login
openclaw gateway --port 18789
\`\`\`

---

## ⚙️ 注意事项

1. **API Keys**: \`~/.openclaw/agents/main/agent/auth-profiles.json\` 中的 API keys 需要一起迁移
2. **敏感数据**: \`.env\` 文件可能包含敏感信息，注意保密
3. **服务配置**: 如果使用自定义端口或配置，需要重新配置
4. **数据库缓存**: 可选 \`~/.openclaw/sessions/\` 和 \`~/.openclaw/logs/\` 可以单独迁移
5. **浏览器数据**: Chrome 配置在 \`~/.config/google-chrome\`，需要重新设置

---

## 📊 文件统计

打包完成后，运行以下命令查看统计：

\`\`\`bash
# 查看打包目录大小
du -sh $PACKAGE_DIR

# 查看各目录大小
du -sh $PACKAGE_DIR/*

\`\`\`

---

**打包完成！** 🎉
EOF

echo -e "  ${GREEN}✓ 打包索引文件${NC}"
echo ""

cd ~/

# ============================================
# 8. 创建压缩包
# ============================================
echo -e "${BLUE}[8/8] 创建压缩包...${NC}"

cd "$PACKAGE_DIR"

# 创建 tar.gz 压缩包
tar czf "openclaw-backup-$(date +%Y%m%d_%H%M%S).tar.gz" ./*

# 获取包大小
PACKAGE_SIZE=$(du -sh "openclaw-backup-$(date +%Y%m%d_%H%M%S).tar.gz" | cut -f1)
PACKAGE_SIZE_MB=$(echo "scale=2; $PACKAGE_SIZE / 1048576" | bc)

echo -e "  ${GREEN}✓ 压缩包创建完成${NC}"
echo -e "  ${YELLOW}包大小: ${PACKAGE_SIZE_MB} MB${NC}"
echo ""

# ============================================
# 完成
# ============================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}      OpenCl 打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📦 打包目录：${NC}"
echo -e "  ${YELLOW}$PACKAGE_DIR${NC}"
echo ""
echo -e "${BLUE}📋 压缩包：${NC}"
echo -e "  ${YELLOW}openclaw-backup-$(date +%Y%m%d_%H%M%S).tar.gz${NC}"
echo -e "  ${YELLOW}大小: ${PACKAGE_SIZE_MB} MB${NC}"
echo ""
echo -e "${BLUE}🚀 迁移步骤：${NC}"
echo ""
echo -e "${BLUE}1. 传输打包目录到新机器${NC}"
echo -e "${BLUE}2. 在新机器上解压并恢复文件${NC}"
echo -e "${BLUE}3. 重新安装 OpenClaw (npm install -g openclaw@latest)${NC}"
echo -e "${BLUE}4. 运行 openclaw onboard --install-daemon${NC}"
echo ""
echo -e "${BLUE}⚠️  注意事项：${NC}"
echo -e "${YELLOW}- API keys 在 ~/.openclaw/agents/main/agent/auth-profiles.json${NC}"
echo -e "${YELLOW}- 敏感信息在 ~/.openclaw/.env${NC}"
echo -e "${YELLOW}- 浏览器数据在 ~/.config/google-chrome${NC}"
echo -e "${YELLOW}- 自定义技能在 ~/.openclaw/skills/${NC}"
echo -e "${YELLOW}- 工作区报告在 ~/.openclaw/workspace/${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
