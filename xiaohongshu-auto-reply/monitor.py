"""
小红书评论监控脚本
定时检查笔记的新评论
"""
import json
import time
import requests
from pathlib import Path
from datetime import datetime


class XHSMonitor:
    def __init__(self, config_file="./config.json"):
        self.config = self._load_config(config_file)
        self.cookies = self.config.get("xiaohongshu", {}).get("cookies", "")
        self.user_agent = self.config.get("xiaohongshu", {}).get("user_agent", "")
        self.check_interval = self.config.get("xiaohongshu", {}).get("monitor_interval", 300)

        # 存储已处理的评论ID
        self.processed_comments = set()
        self.comments_cache = {}

    def _load_config(self, config_file):
        """加载配置文件"""
        config_path = Path(config_file)
        if not config_path.exists():
            return {}
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_headers(self):
        """获取请求头"""
        return {
            "User-Agent": self.user_agent,
            "Cookie": self.cookies,
            "Content-Type": "application/json"
        }

    def get_note_comments(self, note_id, page=1, page_size=20):
        """
        获取笔记的评论列表
        :param note_id: 笔记ID
        :param page: 页码
        :param page_size: 每页数量
        :return: 评论列表
        """
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/comment/page"

        params = {
            "note_id": note_id,
            "cursor": str((page - 1) * page_size),
            "top_comment_id": "",
            "image_scenes": ""
        }

        try:
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                comments = data.get("data", {}).get("comments", [])
                return comments
            else:
                print(f"获取评论失败: {note_id}, 状态码: {response.status_code}")
                return []

        except Exception as e:
            print(f"请求异常: {e}")
            return []

    def check_new_comments(self, note_id):
        """
        检查新评论
        :param note_id: 笔记ID
        :return: 新评论列表
        """
        if note_id not in self.comments_cache:
            self.comments_cache[note_id] = {}

        comments = self.get_note_comments(note_id, page=1, page_size=50)
        new_comments = []

        for comment in comments:
            comment_id = comment.get("id")

            # 跳过已处理的评论
            if comment_id in self.processed_comments:
                continue

            # 记录新评论
            self.processed_comments.add(comment_id)
            new_comments.append({
                "comment_id": comment_id,
                "user_id": comment.get("user", {}).get("user_id"),
                "user_name": comment.get("user", {}).get("nickname"),
                "content": comment.get("content", ""),
                "create_time": comment.get("create_time"),
                "like_count": comment.get("like_count", 0)
            })

        # 检查子评论
        for comment in comments:
            sub_comments = comment.get("sub_comments", [])
            for sub_comment in sub_comments:
                sub_comment_id = sub_comment.get("id")

                if sub_comment_id in self.processed_comments:
                    continue

                self.processed_comments.add(sub_comment_id)
                new_comments.append({
                    "comment_id": sub_comment_id,
                    "user_id": sub_comment.get("user", {}).get("user_id"),
                    "user_name": sub_comment.get("user", {}).get("nickname"),
                    "content": sub_comment.get("content", ""),
                    "create_time": sub_comment.get("create_time"),
                    "like_count": sub_comment.get("like_count", 0),
                    "is_sub_comment": True,
                    "parent_comment_id": comment.get("id")
                })

        return new_comments

    def start_monitoring(self, callback=None):
        """
        开始监控笔记评论
        :param callback: 新评论回调函数
        """
        note_ids = self.config.get("xiaohongshu", {}).get("note_ids", [])

        if not note_ids:
            print("没有配置要监控的笔记ID")
            return

        print(f"开始监控 {len(note_ids)} 个笔记的评论...")
        print(f"检查间隔: {self.check_interval} 秒")

        while True:
            try:
                for note_id in note_ids:
                    new_comments = self.check_new_comments(note_id)

                    if new_comments:
                        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                              f"笔记 {note_id} 发现 {len(new_comments)} 条新评论")

                        # 调用回调函数
                        if callback:
                            for comment in new_comments:
                                callback(note_id, comment)

            except KeyboardInterrupt:
                print("\n监控已停止")
                break
            except Exception as e:
                print(f"监控异常: {e}")

            # 等待下一次检查
            time.sleep(self.check_interval)

    def post_reply(self, note_id, comment_id, content):
        """
        发布回复
        :param note_id: 笔记ID
        :param comment_id: 评论ID
        :param content: 回复内容
        :return: 是否成功
        """
        url = "https://edith.xiaohongshu.com/api/sns/web/v1/comment/post"

        data = {
            "note_id": note_id,
            "content": content,
            "comment_id": comment_id,
            "at_users": {}
        }

        try:
            response = requests.post(url, headers=self._get_headers(), json=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get("success", False):
                    print(f"✅ 回复成功: {content[:30]}...")
                    return True
                else:
                    print(f"❌ 回复失败: {result.get('msg', '未知错误')}")
                    return False
            else:
                print(f"❌ 请求失败: 状态码 {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ 回复异常: {e}")
            return False
