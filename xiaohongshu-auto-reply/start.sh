#!/bin/bash
# 小红书自动回复系统 - 快速启动脚本

echo "============================================================"
echo "小红书自动评论回复系统"
echo "============================================================"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import requests" 2>/dev/null || {
    echo "⚠️  缺少依赖，正在安装..."
    pip install -r requirements.txt
}

# 检查配置
echo "📝 检查配置..."
if [ ! -f "config.json" ]; then
    echo "❌ 错误: 未找到配置文件 config.json"
    exit 1
fi

# 提取配置信息
NOTE_COUNT=$(python3 -c "import json; f=open('config.json'); d=json.load(f); print(len(d.get('xiaohongshu', {}).get('note_ids', [])))" 2>/dev/null || echo "0")

if [ "$NOTE_COUNT" -eq 0 ]; then
    echo "⚠️  警告: 配置文件中没有设置要监控的笔记ID"
    echo ""
    echo "请按以下步骤配置："
    echo "1. 编辑 config.json 文件"
    echo "2. 在 'xiaohongshu.cookies' 填入你的小红书Cookies"
    echo "3. 在 'xiaohongshu.note_ids' 添加要监控的笔记ID列表"
    echo ""
    read -p "按回车键继续（或按Ctrl+C退出）..."
fi

echo ""
echo "============================================================"
echo "选择操作："
echo "============================================================"
echo "1. 运行自动回复系统"
echo "2. 查看统计信息"
echo "3. 查看客户列表"
echo "4. 运行测试"
echo "5. 退出"
echo ""
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo ""
        echo "🚀 启动自动回复系统..."
        echo ""
        python3 auto_reply.py
        ;;
    2)
        echo ""
        python3 auto_reply.py --stats
        ;;
    3)
        echo ""
        echo "选择客户类型:"
        echo "  1 - 所有客户"
        echo "  2 - VIP客户"
        echo "  3 - 活跃客户"
        echo "  4 - 新客户"
        read -p "请输入选项 (1-4): " customer_type

        case $customer_type in
            1) python3 auto_reply.py --customers all ;;
            2) python3 auto_reply.py --customers vip ;;
            3) python3 auto_reply.py --customers active ;;
            4) python3 auto_reply.py --customers new ;;
            *) echo "无效选项" ;;
        esac
        ;;
    4)
        echo ""
        echo "🧪 运行测试套件..."
        echo ""
        python3 test.py
        ;;
    5)
        echo "👋 再见！"
        exit 0
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
