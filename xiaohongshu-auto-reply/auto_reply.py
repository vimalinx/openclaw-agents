"""
小红书自动回复系统主程序
整合监控、策略、客户跟踪等功能
"""
import json
import time
import sys
from pathlib import Path
from datetime import datetime

from monitor import XHSMonitor
from reply_strategy import ReplyStrategy
from customer_tracker import CustomerTracker


class AutoReplySystem:
    def __init__(self, config_file="./config.json"):
        self.config = self._load_config(config_file)
        self.monitor = XHSMonitor(config_file)
        self.strategy = ReplyStrategy()
        self.tracker = CustomerTracker(
            db_file=self.config.get("storage", {}).get("customer_db", "./data/customers.json")
        )

        # 创建必要的目录
        Path("./data").mkdir(parents=True, exist_ok=True)
        Path("./logs").mkdir(parents=True, exist_ok=True)

        # 回复统计
        self.reply_stats = {
            "total_replies": 0,
            "today_replies": 0,
            "last_reset": datetime.now().strftime("%Y-%m-%d")
        }

    def _load_config(self, config_file):
        """加载配置文件"""
        config_path = Path(config_file)
        if not config_path.exists():
            print(f"配置文件不存在: {config_file}")
            return {}
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _log_reply(self, note_id, comment, reply_text):
        """记录回复日志"""
        log_file = Path("./logs/reply.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = f"[{timestamp}] 笔记:{note_id} | 用户:{comment['user_name']} | 评论:{comment['content'][:30]}... | 回复:{reply_text[:30]}...\n"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def _check_daily_reset(self):
        """检查是否需要重置每日统计"""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.reply_stats["last_reset"] != today:
            self.reply_stats["today_replies"] = 0
            self.reply_stats["last_reset"] = today
            print(f"📅 新的一天开始，每日统计已重置")

    def _should_reply(self, comment):
        """判断是否应该回复"""
        # 检查是否为子评论（可选）
        if comment.get("is_sub_comment"):
            # 子评论是否也回复，根据配置决定
            return False

        # 检查今日回复数量限制
        max_replies = self.config.get("reply", {}).get("max_reply_per_note", 20)
        if self.reply_stats["today_replies"] >= max_replies:
            print(f"⚠️ 今日回复已达上限 ({max_replies})")
            return False

        return True

    def _process_comment(self, note_id, comment):
        """
        处理单条评论
        :param note_id: 笔记ID
        :param comment: 评论数据
        """
        if not self._should_reply(comment):
            return

        # 获取用户历史
        user_id = comment.get("user_id")
        user_history = self.tracker.get_user_history(user_id)

        # 选择回复策略
        reply_text = self.strategy.get_reply_with_conversion(
            comment.get("content", ""),
            user_history
        )

        # 添加延迟，模拟真人
        reply_delay = self.config.get("reply", {}).get("reply_delay", 5)
        time.sleep(reply_delay)

        # 发布回复
        success = self.monitor.post_reply(
            note_id,
            comment.get("comment_id"),
            reply_text
        )

        if success:
            # 记录互动
            self.tracker.record_interaction(
                user_id,
                comment.get("user_name"),
                note_id,
                comment.get("content"),
                reply_text
            )

            # 记录日志
            self._log_reply(note_id, comment, reply_text)

            # 更新统计
            self._check_daily_reset()
            self.reply_stats["total_replies"] += 1
            self.reply_stats["today_replies"] += 1

            print(f"📊 总回复: {self.reply_stats['total_replies']} | 今日: {self.reply_stats['today_replies']}")

    def run(self):
        """运行自动回复系统"""
        print("=" * 50)
        print("小红书自动回复系统")
        print("=" * 50)

        # 检查配置
        if not self.config.get("xiaohongshu", {}).get("note_ids"):
            print("❌ 错误: 请在 config.json 中配置要监控的笔记ID")
            return

        if not self.config.get("reply", {}).get("auto_reply", True):
            print("⚠️ 自动回复已关闭，仅监控模式")
            mode = "monitor"
        else:
            print("✅ 自动回复已启用")
            mode = "auto"

        print(f"\n监控的笔记数量: {len(self.config['xiaohongshu']['note_ids'])}")
        print(f"每日回复上限: {self.config['reply'].get('max_reply_per_note', 20)}")
        print(f"回复延迟: {self.config['reply'].get('reply_delay', 5)} 秒")
        print("\n系统运行中... (按 Ctrl+C 停止)")
        print("=" * 50 + "\n")

        # 开始监控
        self.monitor.start_monitoring(callback=self._process_comment)

    def show_stats(self):
        """显示统计信息"""
        summary = self.tracker.export_summary()

        print("\n" + "=" * 50)
        print("📊 客户统计")
        print("=" * 50)
        print(f"总客户数: {summary['total_customers']}")
        print(f"VIP客户: {summary['vip_customers']}")
        print(f"活跃客户: {summary['active_customers']}")
        print(f"新客户: {summary['new_customers']}")
        print(f"已接触: {summary['contacted_customers']}")

        print("\n" + "=" * 50)
        print("📝 回复统计")
        print("=" * 50)
        print(f"总回复数: {self.reply_stats['total_replies']}")
        print(f"今日回复: {self.reply_stats['today_replies']}")

    def show_customers(self, status=None):
        """显示客户列表"""
        if status == "vip":
            customers = self.tracker.get_vip_customers()
            title = "VIP客户"
        elif status == "active":
            customers = self.tracker.get_active_customers()
            title = "活跃客户"
        elif status == "new":
            customers = self.tracker.get_new_customers()
            title = "新客户"
        else:
            customers = self.tracker.get_all_customers()
            title = "所有客户"

        print(f"\n{'=' * 50}")
        print(f"👥 {title} ({len(customers)})")
        print(f"{'=' * 50}")

        for user_id, customer in customers.items():
            print(f"\n📌 {customer.get('user_name', 'Unknown')}")
            print(f"   状态: {customer.get('status', 'unknown')}")
            print(f"   互动次数: {customer.get('interaction_count', 0)}")
            print(f"   首次接触: {customer.get('first_contact', '-')}")

        return customers


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="小红书自动回复系统")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    parser.add_argument("--customers", nargs="?", const="all", help="显示客户列表 [all|vip|active|new]")

    args = parser.parse_args()

    system = AutoReplySystem()

    if args.stats:
        system.show_stats()
    elif args.customers:
        system.show_customers(status=args.customers)
    else:
        system.run()


if __name__ == "__main__":
    main()
