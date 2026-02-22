"""
客户跟进记录模块
记录用户互动历史，支持客户分级管理
"""
import json
import time
from datetime import datetime
from pathlib import Path


class CustomerTracker:
    def __init__(self, db_file="./data/customers.json"):
        self.db_file = Path(db_file)
        self.db_file.parent.mkdir(parents=True, exist_ok=True)
        self.customers = self._load_database()

    def _load_database(self):
        """加载客户数据库"""
        if not self.db_file.exists():
            return {}
        with open(self.db_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_database(self):
        """保存客户数据库"""
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.customers, f, ensure_ascii=False, indent=2)

    def record_interaction(self, user_id, user_name, note_id, comment_text, reply_text):
        """
        记录用户互动
        :param user_id: 用户ID
        :param user_name: 用户名
        :param note_id: 笔记ID
        :param comment_text: 评论内容
        :param reply_text: 回复内容
        """
        timestamp = int(time.time())
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if user_id not in self.customers:
            self.customers[user_id] = {
                "user_name": user_name,
                "first_contact": date_str,
                "last_contact": date_str,
                "interaction_count": 0,
                "notes": [],
                "status": "new"
            }

        # 更新用户信息
        customer = self.customers[user_id]
        customer["last_contact"] = date_str
        customer["interaction_count"] += 1
        customer["status"] = self._update_status(customer["interaction_count"])

        # 记录互动详情
        interaction = {
            "timestamp": timestamp,
            "date": date_str,
            "note_id": note_id,
            "comment": comment_text,
            "reply": reply_text
        }
        customer["notes"].append(interaction)

        # 只保留最近50条记录
        if len(customer["notes"]) > 50:
            customer["notes"] = customer["notes"][-50:]

        self._save_database()
        return customer

    def get_user_history(self, user_id):
        """
        获取用户互动历史
        :param user_id: 用户ID
        :return: 用户历史记录
        """
        return self.customers.get(user_id, None)

    def _update_status(self, interaction_count):
        """
        根据互动次数更新客户状态
        :param interaction_count: 互动次数
        :return: 客户状态
        """
        if interaction_count >= 5:
            return "vip"
        elif interaction_count >= 3:
            return "active"
        elif interaction_count >= 1:
            return "contacted"
        else:
            return "new"

    def get_customers_by_status(self, status):
        """
        按状态获取客户列表
        :param status: 客户状态
        :return: 客户列表
        """
        result = {}
        for user_id, customer in self.customers.items():
            if customer.get("status") == status:
                result[user_id] = customer
        return result

    def get_vip_customers(self):
        """获取VIP客户"""
        return self.get_customers_by_status("vip")

    def get_active_customers(self):
        """获取活跃客户"""
        return self.get_customers_by_status("active")

    def get_new_customers(self):
        """获取新客户"""
        return self.get_customers_by_status("new")

    def get_all_customers(self):
        """获取所有客户"""
        return self.customers

    def add_note(self, user_id, note):
        """
        为客户添加备注
        :param user_id: 用户ID
        :param note: 备注内容
        """
        if user_id in self.customers:
            if "notes_manual" not in self.customers[user_id]:
                self.customers[user_id]["notes_manual"] = []

            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.customers[user_id]["notes_manual"].append({
                "date": date_str,
                "note": note
            })
            self._save_database()

    def export_summary(self):
        """
        导出客户统计摘要
        :return: 统计摘要
        """
        total = len(self.customers)
        vip = len(self.get_vip_customers())
        active = len(self.get_active_customers())
        new = len(self.get_new_customers())

        return {
            "total_customers": total,
            "vip_customers": vip,
            "active_customers": active,
            "new_customers": new,
            "contacted_customers": total - vip - active - new
        }
