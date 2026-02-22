#!/bin/bash
# AI前沿信息周报生成器 - 一键运行

cd "$(dirname "$0")"

echo "🚀 AI前沿信息周报生成器"
echo "======================"

# 1. 采集数据
echo ""
echo "📊 Step 1: 采集数据..."
.venv/bin/python3 fetch_ai_insights.py

# 2. 生成HTML
echo ""
echo "🎨 Step 2: 生成HTML..."
.venv/bin/python3 generate_html.py

echo ""
echo "✅ 完成！"
echo ""
echo "📄 HTML文件: ai_insights_$(date +%Y%m%d).html"
echo "💡 提示: 在浏览器中打开HTML，按 Ctrl+P 保存为PDF"
