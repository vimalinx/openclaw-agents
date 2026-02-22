#!/bin/bash
# 小红书自动化系统独立打包脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  小红书自动化系统打包脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 配置
BACKUP_DIR="/home/vimalinx/.openclaw/xhs-backup-$(date +%Y%m%d_%H%M%S)"
PACKAGE_DIR="/home/vimalinx/.openclaw/xhs-package-$(date +%Y%m%d_%H%M%S)"

echo -e "${GREEN}备份目录：${BACKUP_DIR}${NC}"
echo -e "${GREEN}打包目录：${PACKAGE_DIR}${NC}"
echo ""

# 创建目录
mkdir -p "$BACKUP_DIR"
mkdir -p "$PACKAGE_DIR"

# ============================================
# 1. 备份小红书自动化主目录
# ============================================
echo -e "${BLUE}[1/9] 备份小红书自动化主目录...${NC}"

# 复制整个 xhs-auto-publisher 目录
cp -r /home/vimalinx/.openclaw/skills/xhs-auto-publisher "$PACKAGE_DIR/xhs-auto-publisher/"

# 备份独立的知识库目录（如果存在）
if [ -d /home/vimalinx/.openclaw/xhs-knowledge-base ]; then
    cp -r /home/vimalinx/.openclaw/xhs-knowledge-base "$PACKAGE_DIR/xhs-knowledge-base/"
    echo -e "  ${GREEN}✓ 外部知识库${NC}"
fi

echo -e "  ${GREEN}✓ 小红书自动化目录${NC}"
echo ""

# ============================================
# 2. 创建 README
# ============================================
echo -e "${BLUE}[2/9] 创建 README...${NC}"

cd "$PACKAGE_DIR"

cat > README.md << 'EOF'
# 小红书自动化系统完整打包

**打包时间**: $(date '+%Y-%m-%d %H:%M:%S')
**版本**: v2.0
**系统**: 小红书自动化系统（XHS AutoPilot）

---

## 📦 包含内容

### 核心目录
\`\`\`xhs-auto-publisher/\`\`\` - 小红书自动化主目录（完整的 Skill）
- 发布器（Playwright）
- 上传脚本
- 内容生成器
- 封面生成器

\`\`\`xhs-knowledge-base/\`\`\` - 外部知识库（可选，如果存在）
- AI 知识库相关文件
- 示例和测试脚本

---

## 🚀 系统功能

### 1. 自动发布
- 基于 Playwright 的浏览器自动化
- 支持图片、标题、标签
- 登录态持久化
- 防风控设计

### 2. AI 内容生成
- AI 知识库集成
- 结构化内容生成
- 多种内容模板

### 3. 数据收集
- 爆款笔记分析
- 互动数据统计
- 趋势识别

### 4. 热点追踪
- 关键词监控
- 爆款笔记分析
- 潜在话题发现

---

## 📋 安装和配置

### 环境要求
- Python 3.9+
- Playwright
- Chrome/Chromium
- 网络连接

### 安装步骤
\`\`\`bash
# 1. 复制到 OpenClaw Skills 目录
cp -r xhs-auto-publisher ~/.openclaw/skills/

# 2. 重新加载 Skill
openclaw skills reload

# 3. 验证安装
openclaw skills list xhs-auto-publisher
\`\`\`

### 配置说明
查看 \`\`\`SKILL.md\`\`\` 了解详细配置
- 配置登录态和浏览器路径

---

## 📊 文件统计

### 核心脚本
- 发布器脚本：\`\`\`publisher_fixed.py\`\`\`
- 封面生成器：\`\`\`cover_generator.py\`\`\`
- 内容生成器：\`\`\`content_generator_v2.py\`\`\`
- 工作流：\`\`\`xhs_auto_workflow.py\`\`\`

### 测试脚本
- 多个 \`\`\`test_*.py\`\`\` 文件

### 配置文件
- \`\`\`package.json\`\`\` - Skill 配置
- \`\`\`ISSUES.md\`\`\` - 已知问题和解决方案
- \`\`\`requirements.txt\`\`\` - Python 依赖
- \`\`\`SETUP.md\`\`\` - 快速开始指南
- \`\`\`README.md\`\`\` - 系统说明

### 知识库文件
- AI 知识库脚本
- 示例和测试文件
- 数据模板

---

## 🚀 在新机器上部署

### 步骤 1：传输打包文件
\`\`\`bash
# 使用 SCP 传输
scp -r xhs-package-*.tar.gz user@new-machine:/tmp/

# 或使用 rsync
rsync -avz xhs-package-*/ user@new-machine:~/backup/xhs-auto-pilot/
\`\`\`

### 步骤 2：解压并恢复
\`\`\`bash
# 解压
tar xzf xhs-package-*.tar.gz

# 进入目录
cd xhs-package-*/

# 复制到 OpenClaw Skills
cp -r xhs-auto-publisher/ ~/.openclaw/skills/

# 验证
openclaw skills list xhs-auto-publisher
\`\`\`

### 步骤 3：安装依赖
\`\`\`bash
# 进入虚拟环境
cd xhs-auto-publisher/venv

# 激活
source bin/activate

# 安装依赖
pip install -r requirements.txt
\`\`\`

### 步骤 4：配置
\`\`\`bash
# 编辑配置
nano package.json

# 或使用 CLI 配置
openclaw skills config xhs-auto-publisher
\`\`\`

### 步骤 5：测试
\`\`\`bash
# 测试账号检查
python check_account.py

# 测试浏览器连接
python test_connect.py

# 测试发布流程
python publisher_fixed.py --test
\`\`\`

---

## 📝 使用指南

### 快速开始
1. \`\`\`快速开始.md\`\`\` - 了解基础功能
2. \`\`\`ISSUES.md\`\`\` - 已知问题和解决方案
3. \`\`\`product_package.md\`\`\` - AI 知识库产品说明

### 高级功能
1. AI 知识库集成 - 了解如何使用 AI 生成内容
2. 热点追踪 - 监控关键词和趋势
3. 数据分析 - 分析笔记和互动数据

---

## ⚠️ 注意事项

### 依赖关系
- 此系统独立运行，不需要 OpenClaw Gateway
- 但可以与 OpenClaw Skills 集成
- 如需集成，请参考 \`\`\`SETUP.md\`\`\`

### 浏览器配置
- Playwright 会自动下载 Chromium
- 或可使用系统 Chrome
- 配置路径在 Skill 中指定

### 账号管理
- 登录态会持久化
- 建议定期检查和更新

---

## 🎉 完成

系统已完整打包，可以传输到新机器进行部署！

需要帮助？查看 \`\`\`README.md\`\`\` 或 \`\`\`SETUP.md\`\`\`
EOF

echo -e "  ${GREEN}✓ README.md 创建完成${NC}"
echo ""

# ============================================
# 3. 创建文件清单
# ============================================
echo -e "${BLUE}[3/9] 创建文件清单...${NC}"

# 统计文件数量
TOTAL_FILES=$(find "$PACKAGE_DIR" -type f | wc -l)

echo -e "  ${GREEN}✓ 总文件数: ${TOTAL_FILES}${NC}"

echo ""

# ============================================
# 4. 创建压缩包
# ============================================
echo -e "${BLUE}[4/9] 创建压缩包...${NC}"

cd "/home/vimalinx/.openclaw"

# 创建 tar.gz 压缩包
tar czf "xhs-auto-system-$(date +%Y%m%d_%H%M%S).tar.gz" -C "$PACKAGE_DIR" .

# 获取包大小
PACKAGE_SIZE=$(du -sh "xhs-auto-system-$(date +%Y%m%d_%H%M%S).tar.gz" | cut -f1)
PACKAGE_SIZE_MB=$(echo "scale=2; $PACKAGE_SIZE / 1048576" | bc)

echo -e "  ${GREEN}✓ 压缩包创建完成${NC}"
echo -e "  ${YELLOW}包大小: ${PACKAGE_SIZE_MB} MB${NC}"
echo ""

# ============================================
# 完成
# ============================================
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}      小红书自动化系统打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📦 打包目录：${NC}"
echo -e "  ${YELLOW}$PACKAGE_DIR${NC}"
echo ""
echo -e "${BLUE}📦 压缩包：${NC}"
echo -e "  ${YELLOW}xhs-auto-system-$(date +%Y%m%d_%H%M%S).tar.gz${NC}"
echo -e "  ${YELLOW}大小: ${PACKAGE_SIZE_MB} MB${NC}"
echo ""
echo -e "${BLUE}📋 文件统计：${NC}"
echo -e "  ${YELLOW}总文件数: ${TOTAL_FILES}${NC}"
echo ""
echo -e "${BLUE}🚀 在新机器上部署的步骤：${NC}"
echo ""
echo -e "${YELLOW}1. 传输打包文件${NC}"
echo "     scp -r xhs-auto-system-*.tar.gz user@new-machine:/tmp/"
echo ""
echo -e "${YELLOW}2. 在新机器上解压${NC}"
echo "     tar xzf xhs-auto-system-*.tar.gz"
echo ""
echo -e "${YELLOW}3. 恢复到 OpenClaw Skills${NC}"
echo "     cp -r xhs-auto-publisher/ ~/.openclaw/skills/"
echo ""
echo -e "${YELLOW}4. 安装依赖${NC}"
echo "     cd xhs-auto-publisher/venv"
echo "     pip install -r requirements.txt"
echo ""
echo -e "${YELLOW}5. 重新加载 Skill${NC}"
echo "     openclaw skills reload"
echo ""
echo -e "${YELLOW}6. 配置和测试${NC}"
echo "     openclaw skills config xhs-auto-publisher"
echo "     openclaw skills exec xhs-auto-publisher check_account"
echo ""
echo -e "${BLUE}========================================${NC}"
