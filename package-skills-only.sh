#!/bin/bash
# OpenClaw Skills 简化打包脚本（只打包核心 Skills）

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE} OpenClaw Skills 简化打包${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 配置
BACKUP_DIR="/home/vimalinx/.openclaw/skills-backup-$(date +%Y%m%d)"
PACKAGE_DIR="/home/vimalinx/.openclaw/skills-package-$(date +%Y%m%d)"

echo -e "${GREEN}备份目录：${BACKUP_DIR}${NC}"
echo -e "${GREEN}打包目录：${PACKAGE_DIR}${NC}"
echo ""

# 创建目录
mkdir -p "$BACKUP_DIR"
mkdir -p "$PACKAGE_DIR"

# ============================================
# 1. 只备份 Skills 目录
# ============================================
echo -e "${BLUE}[1/3] 备份 Skills...${NC}"

# 备份所有 skills
find /home/vimalinx/.openclaw/skills -maxdepth 1 -type d -exec cp -r {} "$BACKUP_DIR/" \;

echo -e "  ${GREEN}✓ Skills 目录备份完成${NC}"
echo ""

# ============================================
# 2. 打包核心 Skills
# ============================================
echo -e "${BLUE}[2/3] 打包核心 Skills...${NC}"

# 直接复制 skills 目录
cp -r /home/vimalinx/.openclaw/skills "$PACKAGE_DIR/"

echo -e "  ${GREEN}✓ Skills 打包完成${NC}"
echo ""

# ============================================
# 3. 生成 README
# ============================================
echo -e "${BLUE}[3/3] 生成 README...${NC}"

cd "$PACKAGE_DIR"

# 统计每个 skill 的文件
cat > README.md << 'EOF'
# OpenClaw Skills 打包

**打包时间**: $(date '+%Y-%m-%d %H:%M:%S')
**版本**: v3.0 (简化版)

---

## 📦 包含的 Skills

### 已打包的目录
\`\`\`bash
cd /home/vimalinx/.openclaw/skills
ls -la
\`\`\`

EOF

# 添加每个 skill 的统计
echo "" >> README.md
echo "## 📊 Skills 文件统计" >> README.md
echo "" >> README.md

# 遍历每个 skill 目录
for skill_dir in */; do
    if [ -d "$skill_dir" ]; then
        echo "### \`\`\`$skill_dir\`\`\`" >> README.md
        echo "" >> README.md

        # 统计文件
        file_count=$(find "$skill_dir" -type f | wc -l)
        total_size=$(du -sh "$skill_dir" | cut -f1)

        echo "- **文件数**: \`\`\`$file_count\`\`\`" >> README.md
        echo "- **大小**: \`\`\`$total_size\`\`\`" >> README.md

        # 列出核心文件（排除缓存和临时文件）
        echo "- **核心文件**:" >> README.md
        find "$skill_dir" -maxdepth 1 -type f \
            ! -path "*/__pycache__/*" \
            ! -name "*.pyc" \
            ! -name ".DS_Store" \
            -exec basename {} \; | sort | head -10 | sed 's/^/    / /' | sed 's/^/- /' >> README.md

        echo "" >> README.md
    fi
done

# 添加总统计
echo "" >> README.md
echo "---" >> README.md
echo "**总 Skills 数**: \`\`\`$(ls -d /home/vimalinx/.openclaw/skills | wc -l)\`\`\`" >> README.md
echo "" >> README.md

echo "## 🚀 如何在 OpenClaw 中使用" >> README.md
echo "" >> README.md
echo "### 安装 Skills" >> README.md
echo "\`\`\`bash" >> README.md
echo "# 备份当前 Skills" >> README.md
echo "openclaw skills backup" >> README.md
echo "" >> README.md
echo "# 恢复 Skills" >> README.md
echo "openclaw skills restore skills-backup-$(date +%Y%m%d)" >> README.md
echo "" >> README.md
echo "# 验证安装" >> README.md
echo "openclaw skills list" >> README.md
echo "" >> README.md
echo "### 使用 Skills" >> README.md
echo "\`\`\`bash" >> README.md
echo "# 小红书自动发布" >> README.md
echo "openclaw skills exec xhs-auto-publisher publish --help" >> README.md
echo "" >> README.md
echo "# 媒体市场情报" >> README.md
echo "openclaw skills exec media-crawler collect --help" >> README.md
echo "" >> README.md
echo "# AI 周报生成" >> README.md
echo "openclaw skills exec ai-weekly-generator --help" >> README.md
echo "" >> README.md
echo "# 播客生成" >> README.md
echo "openclaw skills exec tts --text \"你的播客内容\"" >> README.md
echo "" >> README.md

echo "## 📝 配置文件说明" >> README.md
echo "" >> README.md
echo "### 主配置" >> README.md
echo "位置: \`\`\`~/.openclaw/openclaw.json\`\`\`" >> README.md
echo "" >> README.md
echo "### 技能配置" >> README.md
echo "每个 Skill 可能有独立的配置文件，在 Skill 目录中查看" >> README.md
echo "" >> README.md
echo "## ⚠️ 注意事项" >> README.md
echo "" >> README.md
echo "1. **备份目录**: \`\`\`$BACKUP_DIR\`\`\` - 包含 Skills 的完整备份" >> README.md
echo "2. **打包目录**: \`\`\`$PACKAGE_DIR\`\`\` - 可以直接传输的完整 Skills 包" >> README.md
echo "3. **环境不打包**: venv、.env、外部知识库不包含在此打包中" >> README.md
echo "4. **恢复方式**: 使用 OpenClaw 的备份和恢复命令" >> README.md
echo "" >> README.md
echo "## 📚 文档链接" >> README.md
echo "" >> README.md
echo "- OpenClaw 文档: https://docs.openclaw.ai" >> README.md
echo "- ClawHub: https://clawhub.ai" >> README.md
echo "- GitHub: https://github.com/openclaw" >> README.md
echo "" >> README.md

echo "**打包完成！** 🎉" >> README.md

echo -e "  ${GREEN}✓ README.md 生成完成${NC}"
echo ""

# ============================================
# 4. 生成文件列表
# ============================================
echo -e "${BLUE}[4/3] 生成文件列表...${NC}"

cd "$PACKAGE_DIR"

find . -type f -exec ls -lh {} \; > file_list.txt
find . -type d | sort > directory_structure.txt

echo -e "  ${GREEN}✓ 文件列表生成${NC}"
echo ""

# ============================================
# 完成
# ============================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}      Skills 打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📦 备份目录：${NC}"
echo -e "  ${YELLOW}$BACKUP_DIR${NC}"
echo ""
echo -e "${BLUE}📦 打包目录：${NC}"
echo -e "  ${YELLOW}$PACKAGE_DIR${NC}"
echo ""
echo -e "${BLUE}📊 文件统计：${NC}"
echo -e "  ${YELLOW}$(find . -type f | wc -l) 个文件${NC}"
echo ""
echo -e "${BLUE}📄 文档：${NC}"
echo -e "  ${YELLOW}README.md${NC}"
echo -e "  ${YELLOW}file_list.txt${NC}"
echo -e "  ${YELLOW}directory_structure.txt${NC}"
echo ""
echo -e "${BLUE}🚀 在新机器上的恢复步骤：${NC}"
echo ""
echo -e "${BLUE}1. 传输打包目录${NC}"
echo -e "     scp -r $PACKAGE_DIR user@new-machine:/tmp/"
echo ""
echo -e "${BLUE}2. 在新机器上备份 Skills${NC}"
echo -e "     openclaw skills backup"
echo ""
echo -e "${BLUE}3. 传输打包目录到新机器${NC}"
echo -e "     scp -r $PACKAGE_DIR user@new-machine:/tmp/"
echo ""
echo -e "${BLUE}4. 在新机器上恢复 Skills${NC}"
echo -e "     openclaw skills restore skills-backup-$(date +%Y%m%d)"
echo ""
echo -e "${BLUE}========================================${NC}"
