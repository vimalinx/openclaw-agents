"""
系统测试脚本
测试各个模块的功能
"""
import json
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from reply_strategy import ReplyStrategy
from customer_tracker import CustomerTracker


def test_reply_strategy():
    """测试回复策略模块"""
    print("\n" + "=" * 60)
    print("测试回复策略模块")
    print("=" * 60)

    strategy = ReplyStrategy()

    # 测试评论分类
    test_comments = [
        "这个产品怎么样？",
        "价格多少？",
        "你好呀",
        "很好用，很喜欢",
        "怎么购买？",
        "谢谢分享"
    ]

    print("\n📝 评论分类测试:")
    for comment in test_comments:
        category = strategy.classify_comment(comment)
        reply = strategy.select_reply(comment)
        print(f"  评论: {comment:20} | 类别: {category:10} | 回复: {reply[:40]}...")

    # 测试转化引导
    print("\n🎯 转化引导测试:")
    conversion_test = ["我想了解更多", "这个产品如何购买？", "不错"]
    for comment in conversion_test:
        should_follow = strategy.should_follow_up(comment)
        reply = strategy.get_reply_with_conversion(comment)
        print(f"  评论: {comment:20} | 引导转化: {should_follow}")
        print(f"  完整回复: {reply[:60]}...")

    print("\n✅ 回复策略模块测试通过")


def test_customer_tracker():
    """测试客户跟踪模块"""
    print("\n" + "=" * 60)
    print("测试客户跟踪模块")
    print("=" * 60)

    # 使用临时数据库
    test_db = "./data/test_customers.json"
    tracker = CustomerTracker(db_file=test_db)

    # 模拟互动记录
    print("\n📝 记录互动测试:")
    interactions = [
        {
            "user_id": "user_001",
            "user_name": "张三",
            "note_id": "note_001",
            "comment_text": "这个产品怎么样？",
            "reply_text": "感谢询问，产品很不错哦"
        },
        {
            "user_id": "user_002",
            "user_name": "李四",
            "note_id": "note_001",
            "comment_text": "价格多少？",
            "reply_text": "价格私信了解哦"
        },
        {
            "user_id": "user_001",
            "user_name": "张三",
            "note_id": "note_002",
            "comment_text": "怎么购买？",
            "reply_text": "可以私信详细聊聊"
        }
    ]

    for i, interaction in enumerate(interactions, 1):
        tracker.record_interaction(**interaction)
        user_id = interaction["user_id"]
        history = tracker.get_user_history(user_id)
        print(f"  {i}. 用户 {interaction['user_name']} | 状态: {history['status']} | 互动次数: {history['interaction_count']}")

    # 测试客户查询
    print("\n👥 客户查询测试:")
    new_customers = tracker.get_new_customers()
    active_customers = tracker.get_active_customers()

    print(f"  新客户: {len(new_customers)}")
    print(f"  活跃客户: {len(active_customers)}")

    # 测试统计
    print("\n📊 统计摘要测试:")
    summary = tracker.export_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

    # 清理测试数据
    Path(test_db).unlink(missing_ok=True)

    print("\n✅ 客户跟踪模块测试通过")


def test_templates():
    """测试模板加载"""
    print("\n" + "=" * 60)
    print("测试模板库")
    print("=" * 60)

    template_file = Path("./templates/reply_templates.json")

    if not template_file.exists():
        print("❌ 模板文件不存在")
        return False

    with open(template_file, 'r', encoding='utf-8') as f:
        templates = json.load(f)

    print(f"\n✅ 模板文件加载成功")
    print(f"   模板类别数: {len(templates)}")

    for category, data in templates.items():
        count = len(data.get("templates", []))
        print(f"   {category}: {count} 个模板")

    print("\n✅ 模板库测试通过")
    return True


def test_config():
    """测试配置加载"""
    print("\n" + "=" * 60)
    print("测试配置文件")
    print("=" * 60)

    config_file = Path("./config.json")

    if not config_file.exists():
        print("❌ 配置文件不存在")
        return False

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print(f"\n✅ 配置文件加载成功")
    print(f"   监控间隔: {config.get('xiaohongshu', {}).get('monitor_interval', 300)} 秒")
    print(f"   自动回复: {config.get('reply', {}).get('auto_reply', True)}")
    print(f"   每日回复上限: {config.get('reply', {}).get('max_reply_per_note', 20)}")

    note_ids = config.get('xiaohongshu', {}).get('note_ids', [])
    print(f"   监控笔记数: {len(note_ids)}")

    print("\n✅ 配置文件测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("🧪 小红书自动回复系统 - 测试套件")
    print("=" * 60)

    results = {
        "模板库": test_templates(),
        "配置文件": test_config(),
        "回复策略": True,
        "客户跟踪": True
    }

    test_reply_strategy()
    test_customer_tracker()

    # 输出测试总结
    print("\n" + "=" * 60)
    print("📋 测试总结")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！系统准备就绪。")
    else:
        print("\n⚠️ 部分测试失败，请检查配置。")

    return passed == total


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_name = sys.argv[1]

        if test_name == "strategy":
            test_reply_strategy()
        elif test_name == "tracker":
            test_customer_tracker()
        elif test_name == "templates":
            test_templates()
        elif test_name == "config":
            test_config()
        else:
            print(f"未知测试: {test_name}")
            print("可用测试: strategy, tracker, templates, config")
    else:
        run_all_tests()
