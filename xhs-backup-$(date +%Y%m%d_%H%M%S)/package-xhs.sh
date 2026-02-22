#!/bin/bash
# 小红书自动化系统独立打包脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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
# 1. 备份主目录
# ============================================
echo -e "${BLUE}[1/9] 备份小红书自动化主目录...${NC}"

# 复制整个 xhs-auto-publisher 目录
cp -r /home/vimalinx/.openclaw/skills/xhs-auto-publisher "$PACKAGE_DIR/xhs-auto-publisher/"

# 复制独立的知识库目录（如果存在）
if [ -d /home/vimalinx/.openclaw/xhs-knowledge-base ]; then
    cp -r /home/vimalinx/.openclaw/xhs-knowledge-base "$PACKAGE_DIR/xhs-knowledge-base/"
    echo -e "  ${GREEN}✓ 外部知识库${NC}"
fi

echo -e "  ${GREEN}✓ 小红书自动化目录${NC}"
echo ""

# ============================================
# 2. 备份环境配置
# ============================================
echo -e "${BLUE}[2/9] 备份环境配置...${NC}"

# 备份 venv（如果存在）
if [ -d /home/vimalinx/.openclaw/skills/xhs-auto-publisher/venv ]; then
    cp -r /home/vimalinx/.openclaw/skills/xhs-auto-publisher/venv "$PACKAGE_DIR/xhs-venv/"
    echo -e "  ${GREEN}✓ Python 虚拟环境（venv）${NC}"
fi

# 备份 .env 文件（如果存在）
if [ -f /home/vimalinx/.openclaw/skills/xhs-auto-publisher/venv ]; then
    cp /f /home/vimalinx/.openclaw/skills/xhs-auto-publisher/venv/.env "$PACKAGE_DIR/xhs-venv/.env"
    echo -e "  ${GREEN}✓ 环境变量文件${NC}"
fi

echo ""

# ============================================
# 3. 备份产品文档
# ============================================
echo -e "${BLUE}[3/9] 备份产品文档...${NC}"

# 复制产品包说明
if [ -f /home/vimalinx/.openclaw/skills/xhs-auto-publisher/PRODUCT_PACKAGE.md ]; then
    cp /home/vimalinx/.openclaw/skills/xhs-auto-publisher/PRODUCT_PACKAGE.md "$PACKAGE_DIR/PRODUCT_PACKAGE.md"
    echo -e "  ${GREEN}✓ 产品包说明${NC}"
fi

# 复制安装指南
if [ -f /home/vimalinx/.openclaw/skills/xhs-auto-publisher/SETUP.md ]; then
    cp /home/vimalinx/.openclaw/skills/xhs-auto-publisher/SETUP.md "$PACKAGE_DIR/SETUP.md"
    echo -e "  ${GREEN}✓ 安装指南${NC}"
fi

# 复制 Skill 文档
if [ -f /home/vimalinx/.openclaw/skills/xhs-auto-publisher/SKILL.md ]; then
    cp /home/vimalinx/.openclaw/skills/xhs-auto-publisher/SKILL.md "$PACKAGE_DIR/SKILL.md"
    echo -e "  ${GREEN}✓ Skill 文档${NC}"
fi

# 复制更新日志
if [ -f /home/vimalinx/.openclaw/skills/xhs-auto-publisher/CHANGELOG.md ]; then
    cp /home/vimalinx/.openclaw/skills/xhs-auto-publisher/CHANGELOG.md "$PACKAGE_DIR/CHANGELOG.md"
    echo -e "  ${GREEN}✓ 更新日志${NC}"
fi

# 复制问题列表
if [ -f /home/vimalinx/.openclaw/skills/xhs-auto-publisher/ISSUES.md ]; then
    cp /home/vimalinx/.openclaw/skills/xhs-auto-publisher/ISSUES.md "$PACKAGE_DIR/ISSUES.md"
    echo -e "  ${GREEN}✓ 问题列表${NC}"
fi

echo ""

# ============================================
# 4. 创建 README
# ============================================
echo -e "${BLUE}[4/9] 创建打包说明文档...${NC}"

cd "$PACKAGE_DIR"

cat > README.md << 'EOF'
# 小红书自动化系统完整打包

**打包时间**: $(date '+%Y-%m-%d %H:%M:%S')
**版本**: v2.0
**系统**: 小红书自动化系统（XHS AutoPilot）

---

## 📦 包含内容

### 核心目录
\`\`\`xhs-auto-publisher/\`\`\` - 小红书自动化系统主目录（完整的 Skill）
  - Python 脚本集合
  - 配置文件
  - 测试文件
  - 依赖管理

\`\`\`xhs-knowledge-base/\`\`\` - 外部知识库（如果存在）
  - AI 知识库相关文件

### 文档和指南
\`\`\`PRODUCT_PACKAGE.md\`\`\` - AI 知识库产品包说明
\`\`\`SETUP.md\`\`\` - 系统安装和配置指南
\`\`\`SKILL.md\`\`\` - Skill 文档
\`\`\`ISSUES.md\`\`\` - 已知问题和解决方案
\`\`\`CHANGELOG.md\`\`\` - 更新日志
\`\`\`README.md\`\`\` - 系统说明

### 环境配置
\`\`\`xhs-venv/\`\`\` - Python 虚拟环境（已安装依赖）
\`\`\`xhs-venv/.env\`\`\` - 环境变量配置（如果存在）

### 测试和示例
\`\`\`example.py\`\`\` - 使用示例
\`\`\`demo_post.py\`\`\` - 示例发布脚本
\`\`\`test_*.py\`\`\` - 各种测试脚本

### 工作流脚本
\`\`\`xhs_auto_workflow.py\`\`\` - 完整自动化工作流

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

### 3. 热点追踪
- 关键词监控
- 爆款笔记分析
- 趋势识别

### 4. 数据收集
- 笔记数据收集
- 互动数据分析
- 市场情报报告

---

## 📋 安装和配置

### 环境要求
- Python 3.9+
- Playwright
- Chrome/Chromium
- 网络连接

### 安装步骤
\`\`\`bash
# 1. 复制整个 xhs-auto-publisher 目录到 OpenClaw Skills 目录
cp -r xhs-auto-publisher/ ~/.openclaw/skills/xhs-auto-publisher/

# 2. 激活 Skill
openclaw skills reload

# 3. 验证安装
openclaw skills list xhs-auto-publisher
\`\`\`

### 配置
- 查看配置文件：\`\`\`~/.openclaw/openclaw.json\`\`\`
- 编辑配置或使用 CLI 工具

---

## ⚙️ 已知问题和解决方案

### ✅ 已解决
- 标题超过 20 字限制 → 已修复（截取前 20 字）
- 图片中文乱码 → 已修复（改用支持中文的字体）
- 发布错误内容 → 已修复（草稿预览确认）
- 需要查看账号已有内容 → 已修复

### 🔄 优化中
- 进入创作页面超时（30 秒限制）→ 待优化

---

## 🔧 高级配置

### 依赖管理
\`\`\`bash
cd ~/.openclaw/skills/xhs-auto-publisher/venv

# 安装依赖
pip install -r requirements.txt

# 列出已安装依赖
pip list
\`\`\`

### 环境变量
\`\`\`bash
# 编辑 xhs-venv/.env（如果需要）
nano xhs-auto-publisher/venv/.env
\`\`\`

---

## 📊 使用统计

### 核心脚本数量
- 发布脚本: \`\`\`publisher_fixed.py\`\`\`
- 上传脚本: \`\`\`publish_note.py\`\`\`
- 检查脚本: \`\`\`check_account.py\`\`\`
- 测试脚本: 多个

### 知识库文件
- 核心脚本: \`\`\`ai_knowledge_base.py\`\`\`, \`\`\`ai_knowledge_base_v2.py\`\`\`
- 示例和测试: 多个

### 文档文件
- 产品说明
- 安装指南
- Skill 文档
- 更新日志
- 问题列表

---

## 🎯 下一步

1. 在新机器上安装 OpenClaw
2. 复制 \`\`\`xhs-auto-publisher\`\`\` 目录到 Skills 目录
3. 激活并测试系统
4. 根据实际需求配置环境变量

---

## ⚠️ 注意事项

### 依赖关系
- 此系统可以独立运行，不需要 OpenClaw Gateway
- 如果需要集成到 OpenClaw 代理生态，需要额外配置

### 数据安全
- 所有配置文件和脚本都包含在此包中
- \`\`\`venv/.env\`\`\` 文件可能包含敏感信息，请注意保护
- 建议在迁移前检查并移除敏感数据

### 网络要求
- 需要能访问小红书网站（可能需要代理）
- Playwright 需要下载浏览器

---

**打包完成！** 🎉

需要帮助？查看 \`\`\`README.md\`\`\` 或 \`\`\`SETUP.md\`\`\` 获取详细说明。

EOF

echo -e "  ${GREEN}✓ README.md 创建完成${NC}"
echo ""

# ============================================
# 5. 创建文件清单
# ============================================
echo -e "${BLUE}[5/9] 创建文件清单...${NC}"

# 统计文件数量
TOTAL_FILES=$(find "$PACKAGE_DIR" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$PACKAGE_DIR" | cut -f1)

echo -e "${GREEN}✓ 总文件数: ${TOTAL_FILES}${NC}"
echo -e "${GREEN}✓ 总大小: ${TOTAL_SIZE}${NC}"

# 生成文件列表
find "$PACKAGE_DIR" -type f -exec ls -lh {} \; > file_list.txt

# 生成目录结构
find "$PACKAGE_DIR" -type d | sort > directory_structure.txt

echo ""

# ============================================
# 6. 创建压缩包
# ============================================
echo -e "${BLUE}[6/9] 创建压缩包...${NC}"

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
echo -e "${BLUE}📋 文件统计${NC}"
echo -e "  ${YELLOW}总文件数: ${TOTAL_FILES}${NC}"
echo -e "  ${YELLOW}总大小: ${TOTAL_SIZE}${NC}"
echo ""
echo -e "${BLUE}📂 主要目录${NC}"
echo -e "  ${YELLOW}- xhs-auto-publisher/ (主系统)${NC}"
if [ -d "$PACKAGE_DIR/xhs-knowledge-base" ]; then
    echo -e "  ${YELLOW}- xhs-knowledge-base/ (外部知识库)${NC}"
fi
echo -e "  ${YELLOW}- xhs-venv/ (Python 环境)${NC}"
echo ""
echo -e "${BLUE}📚 文档清单${NC}"
echo -e "  ${YELLOW}- PRODUCT_PACKAGE.md (产品说明)${NC}"
echo -e "  ${YELLOW}- SETUP.md (安装指南)${NC}"
echo -e "  ${YELLOW}- SKILL.md (Skill 文档)${NC}"
echo -e "  ${YELLOW}- ISSUES.md (问题列表)${NC}"
echo -e "  ${YELLOW}- CHANGELOG.md (更新日志)${NC}"
echo -e "  ${YELLOW}- README.md (本指南)${NC}"
echo ""
echo -e "${BLUE}🚀 新机器上的安装步骤${NC}"
echo ""
echo -e "${YELLOW}1. 解压压缩包${NC}"
echo -e "     tar xzf xhs-auto-system-*.tar.gz${NC}"
echo -e "     cd xhs-auto-system-*/${NC}"
echo ""
echo -e "${YELLOW}2. 复制到 OpenClaw Skills 目录${NC}"
echo -e "     cp -r xhs-auto-publisher/ ~/.openclaw/skills/${NC}"
echo ""
echo -e "${YELLOW}3. 重新加载 Skill${NC}"
echo -e "     openclaw skills reload${NC}"
echo ""
echo -e "${YELLOW}4. 验证安装${NC}"
echo -e "     openclaw skills list xhs-auto-publisher${NC}"
echo ""
echo -e "${BLUE}⚠️  重要注意事项${NC}"
echo ""
echo -e "${YELLOW}- Python 依赖${NC}"
echo -e "     系统使用 Python venv，依赖已安装${NC}"
echo -e "     如需重新安装: \`\`\`cd xhs-auto-publisher/venv && pip install -r requirements.txt\`\`\`${NC}"
echo ""
echo -e "${YELLOW}- 环境变量${NC}"
echo -e "     venv/.env 文件可能包含敏感配置${NC}"
echo -e "     迁移前请检查并移除敏感信息${NC}"
echo ""
echo -e "${YELLOW}- Playwright 浏览器${NC}"
echo -e "     需要下载 Chromium 浏览器用于 Playwright${NC}"
echo -e "     系统会自动使用已安装的浏览器${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
