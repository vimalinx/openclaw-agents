#!/bin/bash
# 小红书自动化闭环 - 常用命令集合

# ========================================
# 测试命令
# ========================================

# 运行技能可用性测试
python3 /home/vimalinx/.openclaw/workspace/test-xhs-skills-v2.py

# 运行主脚本测试模式
python3 /home/vimalinx/.openclaw/workspace/xhs-auto-pipeline.py test

# ========================================
# 配置命令
# ========================================

# 启动 Chrome 远程调试（临时）
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug

# 启动 Chrome 远程调试（后台）
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug > /dev/null 2>&1 &

# 配置图像生成 API 密钥（临时）
export VOLCENGINE_API_KEY="your_api_key_here"

# 配置图像生成 API 密钥（永久）
echo 'export VOLCENGINE_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc

# ========================================
# 验证命令
# ========================================

# 检查 Chrome CDP 状态
curl http://localhost:9222/json/version

# 检查 Chrome 进程
ps aux | grep chrome

# 检查端口占用
netstat -tlnp | grep 9222

# 检查环境变量
echo $VOLCENGINE_API_KEY

# 检查 Python 依赖
pip list | grep playwright

# ========================================
# 依赖安装
# ========================================

# 安装 MediaCrawler 依赖
cd /home/vimalinx/.openclaw/skills/media-crawler
pip install -r requirements.txt

# 安装 XHS Auto Publisher 依赖
cd /home/vimalinx/.openclaw/skills/xhs-auto-publisher
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# ========================================
# 文档查看
# ========================================

# 查看完整测试报告
cat /home/vimalinx/.openclaw/workspace/XHS_AUTOMATION_TEST_REPORT.md

# 查看快速配置指南
cat /home/vimalinx/.openclaw/workspace/XHS_QUICK_START_GUIDE.md

# 查看执行摘要
cat /home/vimalinx/.openclaw/workspace/XHS_TEST_SUMMARY.md

# 查看 MediaCrawler 文档
cat /home/vimalinx/.openclaw/skills/media-crawler/SKILL.md

# 查看 XHS Auto Publisher 文档
cat /home/vimalinx/.openclaw/skills/xhs-auto-publisher/SKILL.md

# ========================================
# 数据管理
# ========================================

# 查看运行记录
cat /home/vimalinx/.openclaw/workspace/xhs-auto-records.json

# 查看测试报告
cat /home/vimalinx/.openclaw/workspace/xhs-automation-test-report.json

# ========================================
# 清理命令
# ========================================

# 停止 Chrome 进程
pkill -f "chrome.*remote-debugging"

# 清理 Chrome 用户数据
rm -rf /tmp/chrome-debug

# ========================================
# 调试命令
# ========================================

# 测试 MediaCrawler 导入
python3 -c "import sys; sys.path.insert(0, '/home/vimalinx/.openclaw/skills/media-crawler'); import skill; print('MediaCrawler OK')"

# 测试 ContentGenerator 导入
python3 -c "import sys; sys.path.insert(0, '/home/vimalinx/.openclaw/skills/xhs-auto-publisher'); import content_generator_v2; print('ContentGenerator OK')"

# 测试 CoverGenerator 导入
python3 -c "import sys; sys.path.insert(0, '/home/vimalinx/.openclaw/skills/xhs-auto-publisher'); import cover_generator; print('CoverGenerator OK')"

# 测试 Publisher 导入
python3 -c "import sys; sys.path.insert(0, '/home/vimalinx/.openclaw/skills/xhs-auto-publisher'); import publisher; print('Publisher OK')"

# 检查 API 密钥配置
python3 -c "import os; print('API 密钥已配置' if os.environ.get('VOLCENGINE_API_KEY') else 'API 密钥未配置')"

# ========================================
# 帮助
# ========================================

echo "使用方法:"
echo "  1. 复制需要的命令"
echo "  2. 粘贴到终端执行"
echo "  3. 查看文档了解更多"

echo ""
echo "快速开始:"
echo "  1. 启动 Chrome CDP: google-chrome --remote-debugging-port=9222"
echo "  2. 登录小红书: 访问 https://www.xiaohongshu.com"
echo "  3. 运行测试: python3 xhs-auto-pipeline.py test"

echo ""
echo "更多帮助:"
echo "  - 查看完整测试报告: cat XHS_AUTOMATION_TEST_REPORT.md"
echo "  - 查看快速配置指南: cat XHS_QUICK_START_GUIDE.md"
