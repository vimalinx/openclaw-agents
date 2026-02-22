"""
智能回复策略模块
根据评论内容和上下文选择合适的回复模板
"""
import json
import random
import jieba
from pathlib import Path


class ReplyStrategy:
    def __init__(self, template_file="./templates/reply_templates.json"):
        self.template_file = Path(template_file)
        self.templates = self._load_templates()
        self._init_keywords()

    def _load_templates(self):
        """加载回复模板"""
        if not self.template_file.exists():
            return {}
        with open(self.template_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _init_keywords(self):
        """初始化关键词映射"""
        self.keywords = {
            "question": ["怎么", "如何", "什么", "吗", "疑问", "想问", "请问"],
            "price": ["价格", "多少钱", "贵", "便宜", "费用", "成本"],
            "product": ["产品", "怎么样", "好用", "效果", "体验", "推荐"],
            "praise": ["棒", "好", "赞", "喜欢", "爱", "不错", "优秀"],
            "greeting": ["你好", "哈喽", "Hi", "hello", "早上好", "晚上好"]
        }

    def classify_comment(self, comment):
        """
        分类评论
        :param comment: 评论内容
        :return: 评论类别
        """
        comment_lower = comment.lower()
        words = list(jieba.cut(comment))

        # 检查关键词
        for category, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword.lower() in comment_lower:
                    return category

        # 如果包含多个问号，归类为问题
        if comment.count('?') + comment.count('？') >= 2:
            return "question"

        # 默认返回default
        return "default"

    def select_reply(self, comment, user_history=None):
        """
        根据评论选择合适的回复
        :param comment: 评论内容
        :param user_history: 用户历史记录（用于个性化回复）
        :return: 选中的回复文本
        """
        category = self.classify_comment(comment)

        # 获取该类别的模板
        templates = self.templates.get(category, self.templates.get("default", {}))

        if not templates:
            return "感谢评论！欢迎私信交流~"

        # 随机选择一个模板
        replies = templates.get("templates", [])
        if not replies:
            return "感谢评论！欢迎私信交流~"

        # 简单个性化：根据用户历史记录添加前缀
        prefix = ""
        if user_history:
            if user_history.get("interaction_count", 0) > 3:
                prefix = f"老朋友，"

        reply = random.choice(replies)
        return prefix + reply

    def should_follow_up(self, comment, user_history=None):
        """
        判断是否需要引导转化（私信/关注）
        :param comment: 评论内容
        :param user_history: 用户历史记录
        :return: 是否需要引导转化
        """
        # 检查是否包含转化关键词
        conversion_keywords = ["想了解更多", "感兴趣", "咨询", "了解"]
        for keyword in conversion_keywords:
            if keyword in comment:
                return True

        # 如果是首次互动且有疑问，引导私信
        if user_history and user_history.get("interaction_count", 0) == 0:
            category = self.classify_comment(comment)
            if category in ["question", "price", "product"]:
                return True

        return False

    def get_conversion_message(self):
        """
        获取转化引导消息
        :return: 转化引导文本
        """
        messages = [
            "👉 私信我，有惊喜等着你~",
            "💬 想了解更多？点击右上角私信我吧",
            "🎁 关注我不迷路，后续有更多福利哦",
            "📩 有问题随时私信，我看到都会回复的",
            "✨ 关注+私信，领取专属福利！"
        ]
        return random.choice(messages)

    def get_reply_with_conversion(self, comment, user_history=None):
        """
        获取包含转化引导的完整回复
        :param comment: 评论内容
        :param user_history: 用户历史记录
        :return: 完整回复文本
        """
        base_reply = self.select_reply(comment, user_history)

        if self.should_follow_up(comment, user_history):
            conversion_msg = self.get_conversion_message()
            return f"{base_reply}\n{conversion_msg}"

        return base_reply
