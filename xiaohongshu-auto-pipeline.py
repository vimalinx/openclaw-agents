#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书自动化闭环 - 主脚本
功能：热点监控 → 策略制定 → 内容生成 → 配图生成 → 自动发布 → 数据反馈
"""

import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Playwright
from playwright.sync_api import sync_playwright

# 配置文件路径
CONFIG_FILE = Path(__file__).parent / "xhs-auto-pipeline-config.json"
STATE_FILE = Path(__file__).parent / "xhs-auto-state.json"
RECORDS_FILE = Path(__file__).parent / "xhs-auto-records.json"

# 内容模板
CONTENT_TEMPLATES = {
    "tutorial": {
        "title_prefix": "【教程】",
        "content_template": """大家好！{emoji}

今天给大家分享一个{topic}的{feature}，绝对干货！

📖 主要内容：
{main_content}

💡 使用技巧：
{tips}

🎯 适用人群：
{target_audience}

📸 {call_to_action}

{hashtags}

喜欢的小伙伴记得点赞+收藏哦~
#小红书运营 #自媒体运营 #干货分享""",
        "emojis": ["🔥", "📖", "💡", "🎯", "📸", "👍"]
    },
    "sharing": {
        "title_prefix": "【分享】",
        "content_template": """姐妹们！发现一个{topic}，一定要试！

{main_content}

{call_to_action}

{hashtags}

#好物分享 #生活方式 #{topic}"""
    },
    "recommendation": {
        "title_prefix": "【推荐】",
        "content_template": """{topic} 真的太棒了！

{main_content}

{reason}

{call_to_action}

{hashtags}

#种草推荐 #{topic}"""
    }
}

# 标题模板
TITLE_TEMPLATES = {
    "curiosity": ["你一定要试的{topic}", "绝了！{topic}", "{topic}真的太强了", "谁懂{topic}？"],
    "benefit": ["{topic}让我...", "用{topic}提升...", "{topic}解决了我", "{topic}救了我的命"],
    "urgency": ["{topic}紧急", "今天必须看{topic}", "{topic}不能错过", "{topic}太重要了"]
}

class XiaoHongShuAutomator:
    """小红书自动化系统核心类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.state = self.load_state()
        self.records = self.load_records()
        self.browser = None
        self.page = None
        
        # 添加统计
        self.stats = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "total_posts": 0,
            "successful_posts": 0,
            "total_views": 0,
            "total_likes": 0,
            "total_collects": 0
            "total_comments": 0
        }
    
    def load_state(self) -> Dict:
        """加载状态"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"last_run": None, "last_post_time": None}
    
    def save_state(self):
        """保存状态"""
        self.state["last_run"] = datetime.now().isoformat()
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def load_records(self) -> List[Dict]:
        """加载发布记录"""
        if RECORDS_FILE.exists():
            with open(RECORDS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_record(self, record: Dict):
        """保存发布记录"""
        self.records.append(record)
        self.stats["total_posts"] += 1
        if record.get("success"):
            self.stats["successful_posts"] += 1
            self.stats["total_views"] += record.get("views", 0)
            self.stats["total_likes"] += record.get("likes", 0)
            self.stats["total_collects"] += record.get("collects", 0)
            self.stats["total_comments"] += record.get("comments", 0)
        
        with open(RECORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
        
        # 更新状态
        self.state["last_post_time"] = datetime.now().isoformat()
        self.save_state()
    
    def generate_title(self, topic: str, template_type: str = "curiosity") -> str:
        """生成标题"""
        if template_type == "curiosity":
            titles = TITLE_TEMPLATES["curiosity"]
        elif template_type == "benefit":
            titles = TITLE_TEMPLATES["benefit"]
        elif template_type == "urgency":
            titles = TITLE_TEMPLATES["urgency"]
        else:
            titles = TITLE_TEMPLATES["curiosity"]
        
        title = random.choice(titles)
        return title.format(topic=topic)
    
    def generate_content(self, topic: str, content_type: str = "tutorial", **kwargs) -> Dict:
        """生成内容"""
        template = CONTENT_TEMPLATES.get(content_type, CONTENT_TEMPLATES["tutorial"])
        
        # 选择emoji
        emojis = template["emojis"]
        selected_emojis = random.sample(emojis, min(5, len(emojis)))
        emoji_str = " ".join(selected_emojis)
        
        # 主要内容
        main_content = kwargs.get("main_content", "")
        
        # 使用技巧
        tips = kwargs.get("tips", "")
        
        # 目标受众
        target_audience = kwargs.get("target_audience", "所有对{topic}感兴趣的朋友")
        
        # 行动号召
        call_to_action = kwargs.get("call_to_action", "快来试试吧！")
        
        # Hashtags
        hashtags = kwargs.get("hashtags", "")
        
        # 格式化内容
        content = template["content_template"].format(
            emoji=emoji_str,
            topic=topic,
            feature=kwargs.get("feature", "神器"),
            main_content=main_content,
            tips=tips,
            target_audience=target_audience,
            call_to_action=call_to_action,
            hashtags=hashtags
        )
        
        return {
            "content_type": content_type,
            "content": content,
            "emojis": selected_emojis,
            "main_content": main_content,
            "hashtags": hashtags
        }
    
    def generate_hashtags(self, topic: str, count: int = 10) -> List[str]:
        """生成标签"""
        # 基础标签
        base_tags = [f"#{topic}", f"#{topic}神器", f"#{topic}技巧", f"#{topic}教程"]
        
        # 相关标签
        related_tags = []
        for word in ["效率", "工具", "干货", "分享", "推荐", "生活", "工作", "学习"]:
            related_tags.append(f"#{word}")
        
        # 组合标签
        all_tags = base_tags + related_tags
        selected_tags = random.sample(all_tags, min(count, len(all_tags)))
        
        return selected_tags
    
    def launch_browser(self):
        """启动浏览器"""
        print("🌐 正在启动 Playwright 浏览器...")
        
        try:
            self.browser = sync_playwright().chromium.launch(
                headless=self.config.get("chrome", {}).get("headless", False),
                slow_mo=1000
            )
            
            self.page = self.browser.new_page()
            print("✅ 浏览器启动成功！")
            
            # 设置视口
            self.page.set_viewport_size(1280, 800)
            
            return True
            
        except Exception as e:
            print(f"❌ 浏览器启动失败: {e}")
            return False
    
    def navigate_to_xiaohongshu(self):
        """导航到小红书"""
        print("📱 正在导航到小红书...")
        
        try:
            self.page.goto("https://www.xiaohongshu.com")
            self.page.wait_for_load_state("networkidle", timeout=30000)
            print("✅ 小红书页面加载完成！")
            return True
            
        except Exception as e:
            print(f"❌ 导航失败: {e}")
            return False
    
    def check_login_status(self) -> Dict:
        """检查登录状态"""
        current_url = self.page.url
        
        is_logged_in = False
        status = "unknown"
        
        if "xiaohongshu.com/explore" in current_url:
            is_logged_in = True
            status = "logged_in_home"
            print("✅ 已登录到小红书首页！")
        elif "xiaohongshu.com/user" in current_url:
            is_logged_in = True
            status = "logged_in_profile"
            print("✅ 已登录到小红书个人主页！")
        elif "login" in current_url.lower() or "signin" in current_url.lower():
            status = "login_page"
            print("⏰ 当前在登录页面，请完成登录")
        else:
            print(f"⚠️ 当前在其他页面: {current_url}")
        
        return {
            "is_logged_in": is_logged_in,
            "status": status,
            "current_url": current_url
        }
    
    def hotspot_monitoring(self) -> List[Dict]:
        """热点监控（模拟）"""
        print("🔥 正在监控小红书热点...")
        
        # 模拟热点数据（真实场景需要集成 MediaCrawler）
        hot_topics = [
            {"topic": "AI工具", "heat": 85, "trend": "rising", "engagement_rate": 12.5},
            {"topic": "效率神器", "heat": 78, "trend": "stable", "engagement_rate": 10.8},
            {"topic": "副业搞钱", "heat": 92, "trend": "rising", "engagement_rate": 15.2},
            {"topic": "小红书运营", "heat": 88, "trend": "stable", "engagement_rate": 13.5},
            {"topic": "自媒体变现", "heat": 75, "trend": "stable", "engagement_rate": 9.8}
        ]
        
        # 按热度排序
        hot_topics.sort(key=lambda x: x["heat"], reverse=True)
        
        # 选择前 3 个
        top_topics = hot_topics[:3]
        
        print(f"✅ 发现 {len(hot_topics)} 个热点话题")
        for i, topic in enumerate(top_topics):
            print(f"   {i+1}. {topic['topic']} (热度: {topic['heat']})")
        
        return top_topics
    
    def strategy_formulation(self, hot_topics: List[Dict]) -> Dict:
        """策略制定"""
        print("📊 正在制定内容策略...")
        
        # 选择最热的话题
        selected_topic = hot_topics[0]["topic"]
        trend = hot_topics[0]["trend"]
        
        # 确定内容类型
        if trend == "rising":
            content_type = "tutorial"  # 教程类
            template_type = "urgency"    # 紧迫感
        elif trend == "stable" and hot_topics[0]["heat"] > 85:
            content_type = "sharing"    # 分享类
            template_type = "curiosity" # 好奇感
        else:
            content_type = "recommendation"  # 推荐类
            template_type = "benefit"    # 利益点
        
        # 生成内容
        content = self.generate_content(
            topic=selected_topic,
            content_type=content_type,
            main_content=f"这个{selected_topic}真的太好用了，完全改变了我的{random.choice(['工作', '生活', '学习'])}方式！",
            tips=f"1. {random.choice(['一定要试', '绝对不后悔', '谁用谁知道'])} 2. {random.choice(['超好用', '效果惊人', '真心推荐'])} 3. {random.choice(['提升效率', '节省时间', '事半功倍'])}",
            target_audience=f"所有对{selected_topic}感兴趣的朋友",
            call_to_action=f"快来试试吧！",
            hashtags=f" #{selected_topic} {random.choice(['#效率工具', '#神器', '#干货'])}"
        )
        
        # 生成标题
        title = self.generate_title(selected_topic, template_type)
        
        # 确保标题不超过 20 字
        if len(title) > 20:
            title = title[:20]
        
        # 生成图片描述
        image_prompt = f"""
        小红书风格封面图，{selected_topic}相关
        主标题：{title}
        副标题：{random.choice(['太好用了', '绝对神器', '真心推荐', '谁用谁知道'])}
        风格：简洁现代，使用{random.choice(['蓝色', '紫色', '橙色'])}为主色调
        元素：包含{selected_topic}相关图标或图形
        文字：大标题突出，副标题补充说明
        整体：干净整洁，吸引点击
        """
        
        # 发布延迟（5-10 分钟）
        publish_delay = random.randint(300, 600)
        
        return {
            "topic": selected_topic,
            "title": title,
            "content": content,
            "image_prompt": image_prompt,
            "content_type": content_type,
            "template_type": template_type,
            "publish_delay": publish_delay,
            "estimated_engagement": hot_topics[0]["engagement_rate"]
        }
    
    def content_generation(self, strategy: Dict) -> Dict:
        """内容生成（已集成在策略制定中）"""
        print("✅ 内容生成完成！")
        return strategy
    
    def image_generation(self, strategy: Dict) -> str:
        """配图生成（模拟）"""
        print("🎨 正在生成配图...")
        
        # 模拟图片文件路径
        image_filename = f"xhs_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        image_path = Path(__file__).parent / "images" / image_filename
        
        # 创建 images 目录（如果不存在）
        image_path.parent.mkdir(exist_ok=True)
        
        # 模拟生成过程
        print(f"   正在生成: {image_filename}")
        print(f"   风格: {strategy['topic']}相关")
        print(f"   主标题: {strategy['title']}")
        
        # 模拟文件创建（真实场景需要调用 Grsai API）
        time.sleep(2)  # 模拟生成时间
        
        # 创建占位文件
        image_path.touch()
        
        print(f"✅ 配图生成完成: {image_filename}")
        print(f"   保存路径: {image_path}")
        
        return str(image_path)
    
    def auto_publish(self, strategy: Dict, image_path: str) -> Dict:
        """自动发布（模拟）"""
        print("📤 正在准备发布...")
        
        try:
            # 导航到发布页面
            self.page.goto("https://creator.xiaohongshu.com/publish/publish")
            self.page.wait_for_load_state("networkidle", timeout=30000)
            
            print("✅ 已进入发布页面")
            
            # 模拟发布流程（真实场景需要 xhs-auto-publisher）
            print(f"   标题: {strategy['title']}")
            print(f"   配图: {image_path}")
            print(f"   内容: {strategy['content'][:50]}...")
            
            # 模拟等待时间（发布延迟）
            publish_delay = strategy.get("publish_delay", 300)
            print(f"   等待 {publish_delay} 秒后发布...")
            time.sleep(min(publish_delay, 10))  # 最多等待 10 秒
            
            # 模拟发布
            success = True
            message = "发布成功"
            
            # 模拟数据反馈
            views = random.randint(100, 1000)
            likes = random.randint(10, 100)
            collects = random.randint(5, 50)
            comments = random.randint(1, 20)
            
            print(f"✅ 模拟发布完成！")
            print(f"   预期浏览量: {views}")
            print(f"   预期点赞: {likes}")
            print(f"   预期收藏: {collects}")
            print(f"   预期评论: {comments}")
            
            # 更新统计
            self.stats["total_posts"] += 1
            self.stats["successful_posts"] += 1
            self.stats["total_views"] += views
            self.stats["total_likes"] += likes
            self.stats["total_collects"] += collects
            self.stats["total_comments"] += comments
            
            # 保存发布记录
            record = {
                "timestamp": datetime.now().isoformat(),
                "topic": strategy["topic"],
                "title": strategy["title"],
                "content_type": strategy["content_type"],
                "image_path": image_path,
                "success": success,
                "message": message,
                "views": views,
                "likes": likes,
                "collects": collects,
                "comments": comments,
                "estimated_engagement": strategy.get("estimated_engagement", 0),
                "publish_delay": strategy.get("publish_delay", 300)
            }
            
            self.save_record(record)
            
            return {
                "success": success,
                "message": message,
                "topic": strategy["topic"],
                "title": strategy["title"],
                "views": views,
                "likes": likes,
                "collects": collects,
                "comments": comments,
                "record": record
            }
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            self.stats["failed_runs"] += 1
            
            return {
                "success": False,
                "message": f"发布失败: {str(e)}",
                "topic": strategy["topic"],
                "title": strategy["title"]
            }
    
    def data_feedback(self, record: Dict) -> Dict:
        """数据反馈"""
        print("📊 正在收集发布数据...")
        
        # 模拟数据分析
        views = record.get("views", 0)
        likes = record.get("likes", 0)
        collects = record.get("collects", 0)
        comments = record.get("comments", 0)
        estimated_engagement = record.get("estimated_engagement", 0)
        
        # 计算实际互动率
        actual_engagement = (likes * 2 + collects * 3 + comments * 5) / 100
        
        # 评估效果
        if actual_engagement >= estimated_engagement * 0.8:
            effect = "优秀"
            improvement = "继续保持"
        elif actual_engagement >= estimated_engagement * 0.6:
            effect = "良好"
            improvement = "可以优化"
        elif actual_engagement >= estimated_engagement * 0.4:
            effect = "一般"
            improvement = "需要改进"
        else:
            effect = "较差"
            improvement = "需要大幅优化"
        
        # 生成建议
        suggestions = []
        if actual_engagement < estimated_engagement * 0.6:
            suggestions.append("考虑调整发布时间（选择流量高峰时段）")
            suggestions.append("优化标题和封面（增加吸引力）")
            suggestions.append("增加与评论区互动")
        
        # 生成分析报告
        analysis = {
            "views": views,
            "likes": likes,
            "collects": collects,
            "comments": comments,
            "estimated_engagement": estimated_engagement,
            "actual_engagement": actual_engagement,
            "engagement_rate": actual_engagement * 100,
            "effect_evaluation": effect,
            "improvement_suggestions": suggestions,
            "next_steps": ["继续监控", "分析竞品表现", "优化内容策略"]
        }
        
        print(f"✅ 数据反馈分析完成！")
        print(f"   浏览量: {views}")
        print(f"   点赞: {likes}")
        print(f"   收藏: {collects}")
        print(f"   评论: {comments}")
        print(f"   效果评估: {effect}")
        print(f"   改进建议: {'; '.join(suggestions)}")
        
        return analysis
    
    def run_full_pipeline(self, topic: str = None) -> Dict:
        """运行完整流程"""
        print("🚀 开始运行小红书自动化闭环...")
        print("=" * 50)
        
        # 步骤 1: 热点监控
        print("\n📥 步骤 1: 热点监控")
        hot_topics = self.hotspot_monitoring()
        
        # 步骤 2: 策略制定
        print("\n📊 步骤 2: 策略制定")
        if not topic:
            strategy = self.strategy_formulation(hot_topics)
        else:
            # 使用指定话题
            content = self.generate_content(
                topic=topic,
                content_type="tutorial",
                main_content=f"这个{topic}真的太好用了，完全改变了我的工作方式！",
                tips=f"1. 一定要试 2. 绝对不后悔 3. 事半功倍",
                target_audience=f"所有对{topic}感兴趣的朋友",
                call_to_action=f"快来试试吧！",
                hashtags=f" #{topic} #效率工具"
            )
            
            title = self.generate_title(topic, "curiosity")
            if len(title) > 20:
                title = title[:20]
            
            strategy = {
                "topic": topic,
                "title": title,
                "content": content,
                "image_prompt": f"{topic}相关封面，{title}",
                "content_type": "tutorial",
                "template_type": "curiosity",
                "publish_delay": random.randint(300, 600),
                "estimated_engagement": 12.0
            }
        
        # 步骤 3: 内容生成
        print("\n✍️  步骤 3: 内容生成")
        strategy = self.content_generation(strategy)
        
        # 步骤 4: 配图生成
        print("\n🎨 步骤 4: 配图生成")
        image_path = self.image_generation(strategy)
        
        # 步骤 5: 自动发布
        print("\n📤 步骤 5: 自动发布")
        publish_result = self.auto_publish(strategy, image_path)
        
        # 步骤 6: 数据反馈
        print("\n📊 步骤 6: 数据反馈")
        if publish_result["success"]:
            feedback = self.data_feedback(publish_result["record"])
        else:
            feedback = {"error": "发布失败，无法收集数据反馈"}
        
        # 更新统计
        self.stats["total_runs"] += 1
        
        print("\n" + "=" * 50)
        print("✅ 小红书自动化闭环完成！")
        print("=" * 50)
        
        # 总结报告
        self.print_summary(feedback if publish_result["success"] else None, publish_result)
        
        return {
            "success": publish_result["success"],
            "topic": strategy["topic"],
            "title": strategy["title"],
            "publish_result": publish_result,
            "feedback": feedback if publish_result["success"] else None,
            "stats": self.stats
        }
    
    def print_summary(self, feedback: Optional[Dict], publish_result: Dict):
        """打印总结报告"""
        print("\n📋 小红书自动化闭环 - 总结报告")
        print("=" * 40)
        
        print(f"📊 运行统计")
        print(f"   总运行次数: {self.stats['total_runs']}")
        print(f"   成功次数: {self.stats['successful_runs']}")
        print(f"   失败次数: {self.stats['failed_runs']}")
        print()
        
        print(f"📤 发布统计")
        print(f"   总发布: {self.stats['total_posts']}")
        print(f"   成功发布: {self.stats['successful_posts']}")
        print(f"   总浏览量: {self.stats['total_views']}")
        print(f"   总点赞: {self.stats['total_likes']}")
        print(f"   总收藏: {self.stats['total_collects']}")
        print(f"   总评论: {self.stats['total_comments']}")
        print()
        
        if feedback:
            print(f"📈 发布效果")
            print(f"   效果评估: {feedback['effect_evaluation']}")
            print(f"   互动率: {feedback['engagement_rate']:.2f}%")
            print()
            
            print(f"💡 改进建议")
            for suggestion in feedback['improvement_suggestions']:
                print(f"   • {suggestion}")
            print()
            
            print(f"🚀 下一步行动")
            for next_step in feedback['next_steps']:
                print(f"   • {next_step}")
        
        print("=" * 40)
    
    def cleanup(self):
        """清理资源"""
        if self.browser:
            self.browser.close()
            print("🧹 浏览器已关闭")
        
        self.page = None
        self.browser = None


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书自动化闭环系统")
    parser.add_argument("action", choices=["run", "test", "stats"], help="要执行的操作")
    parser.add_argument("--topic", type=str, help="指定发布话题")
    parser.add_argument("--mode", choices=["headless", "headed"], default="headed", help="浏览器模式")
    
    args = parser.parse_args()
    
    # 加载配置
    if not CONFIG_FILE.exists():
        print(f"❌ 配置文件不存在: {CONFIG_FILE}")
        print("请先运行一次 'test' 操作生成默认配置")
        return
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 创建自动化系统
    automator = XiaoHongShuAutomator(config)
    
    # 启动浏览器
    if not automator.launch_browser():
        print("❌ 浏览器启动失败，退出")
        return
    
    # 导航到小红书
    if not automator.navigate_to_xiaohongshu():
        print("❌ 导航失败，退出")
        automator.cleanup()
        return
    
    # 检查登录状态
    login_status = automator.check_login_status()
    
    if args.action == "run":
        # 完整流程
        if not login_status["is_logged_in"]:
            print("⚠️ 未登录，请先完成登录")
            automator.cleanup()
            return
        
        # 运行完整流程
        result = automator.run_full_pipeline(args.topic)
        
    elif args.action == "test":
        # 测试模式（模拟数据）
        print("🧪 测试模式（模拟数据）")
        result = automator.run_full_pipeline(args.topic or "AI工具")
        
    elif args.action == "stats":
        # 统计模式
        print("📊 统计模式")
        print("=" * 40)
        print(f"📤 发布统计")
        print(f"   总发布: {automator.stats['total_posts']}")
        print(f"   成功发布: {automator.stats['successful_posts']}")
        print(f"   总浏览量: {automator.stats['total_views']}")
        print(f"   总点赞: {automator.stats['total_likes']}")
        print(f"   总收藏: {automator.stats['total_collects']}")
        print(f"   总评论: {automator.stats['total_comments']}")
        print()
        
        print(f"📈 运行统计")
        print(f"   总运行次数: {automator.stats['total_runs']}")
        print(f"   成功次数: {automator.stats['successful_runs']}")
        print(f"   失败次数: {automator.stats['failed_runs']}")
        print("=" * 40)
    
    # 清理资源
    automator.cleanup()
    
    print("\n✅ 小红书自动化闭环系统执行完成！")


if __name__ == "__main__":
    main()
