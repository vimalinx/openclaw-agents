#!/usr/bin/env python3
"""
AI前沿信息爬虫
采集 arXiv、Hacker News、GitHub 等平台的AI相关信息
"""

import requests
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict
import json
import os

# 数据输出路径
OUTPUT_DIR = "/home/vimalinx/.openclaw/workspace/ai_insights/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_arxiv_papers(days_back=7, limit=15) -> List[Dict]:
    """
    从 arXiv 获取最新AI/ML论文

    使用 arXiv API: http://export.arxiv.org/api/query
    """
    print("📚 正在从 arXiv 获取最新论文...")

    # 搜索最近N天的论文
    categories = [
        "cs.AI",        # Artificial Intelligence
        "cs.LG",        # Machine Learning
        "cs.CL",        # Computation and Language
        "cs.CV",        # Computer Vision
        "cs.NE",        # Neural and Evolutionary Computing
    ]

    papers = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    for category in categories:
        query = f"cat:{category}"
        url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={limit//len(categories)}&sortBy=submittedDate&sortOrder=descending"

        try:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                # 解析作者
                authors = [author.name for author in entry.authors]

                # 解析摘要（去掉多余空格）
                summary = ' '.join(entry.summary.split())

                papers.append({
                    "title": entry.title,
                    "authors": authors[:4] + ["等"] if len(authors) > 4 else authors,
                    "summary": summary[:500] + "..." if len(summary) > 500 else summary,
                    "link": entry.id.replace("http://arxiv.org/abs/", "https://arxiv.org/abs/"),
                    "category": category,
                    "published": entry.published,
                })
        except Exception as e:
            print(f"  ⚠️  {category} 抓取失败: {e}")

    return papers[:limit]


def fetch_hacker_news_ai(limit=10) -> List[Dict]:
    """
    从 Hacker News 获取AI相关热门讨论

    使用 HN API: https://github.com/HackerNews/API
    """
    print("💬 正在从 Hacker News 获取AI讨论...")

    base_url = "https://hacker-news.firebaseio.com/v0"
    ai_keywords = ["AI", "ML", "machine learning", "deep learning", "GPT", "LLM", "neural"]

    # 获取最新故事ID列表
    try:
        new_stories = requests.get(f"{base_url}/newstories.json").json()
        top_stories = requests.get(f"{base_url}/topstories.json").json()
        story_ids = list(dict.fromkeys(new_stories[:200] + top_stories[:200]))  # 去重合并
    except Exception as e:
        print(f"  ⚠️  获取故事列表失败: {e}")
        return []

    discussions = []
    checked_ids = set()

    for story_id in story_ids:
        if len(discussions) >= limit:
            break

        if story_id in checked_ids:
            continue
        checked_ids.add(story_id)

        try:
            story = requests.get(f"{base_url}/item/{story_id}.json").json()

            # 检查是否与AI相关
            title = story.get("title", "")
            text = story.get("text", "")

            is_ai_related = any(
                keyword.lower() in title.lower() or keyword.lower() in text.lower()
                for keyword in ai_keywords
            )

            if not is_ai_related:
                continue

            discussions.append({
                "title": title,
                "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                "score": story.get("score", 0),
                "comments": story.get("descendants", 0),
                "time": datetime.fromtimestamp(story.get("time", 0)).strftime("%Y-%m-%d"),
            })

        except Exception as e:
            continue

    return discussions


def fetch_github_trending_ai(limit=10) -> List[Dict]:
    """
    获取 GitHub 热门 AI 项目

    通过搜索 API 或使用第三方服务
    """
    print("🐙 正在从 GitHub 获取热门AI项目...")

    # 使用 GitHub API 搜索（需要token）或使用第三方服务
    # 这里简化为模拟数据，实际可以集成 GitHub API

    trending_projects = [
        {
            "name": "autogen",
            "author": "microsoft",
            "description": "Enable next-gen LLM applications. Converse, collaborate, and code with agents.",
            "stars": 28000,
            "url": "https://github.com/microsoft/autogen",
            "tags": ["多智能体", "LLM", "框架"],
        },
        {
            "name": "langchain",
            "author": "langchain-ai",
            "description": "Building applications with LLMs through composability",
            "stars": 76000,
            "url": "https://github.com/langchain-ai/langchain",
            "tags": ["LLM", "RAG", "框架"],
        },
        {
            "name": "vllm",
            "author": "vllm-project",
            "description": "A high-throughput and memory-efficient inference and serving engine for LLMs",
            "stars": 21000,
            "url": "https://github.com/vllm-project/vllm",
            "tags": ["推理加速", "LLM", "部署"],
        },
        {
            "name": "open-interpreter",
            "author": "OpenInterpreter",
            "description": "Open Interpreter lets LLMs run code (Python, JS, Shell, etc.) on your computer",
            "stars": 46000,
            "url": "https://github.com/OpenInterpreter/open-interpreter",
            "tags": ["代码执行", "AI助手", "工具"],
        },
        {
            "name": "ComfyUI",
            "author": "comfyanonymous",
            "description": "A powerful and modular stable diffusion GUI",
            "stars": 39000,
            "url": "https://github.com/comfyanonymous/ComfyUI",
            "tags": ["图像生成", "GUI", "扩散模型"],
        },
    ]

    return trending_projects[:limit]


def generate_weekly_report() -> Dict:
    """
    生成周报数据
    """
    print("\n🚀 开始采集AI前沿信息...\n")

    data = {
        "report_date": datetime.now().strftime("%Y年%m月%d日"),
        "week_number": datetime.now().isocalendar()[1],
        "papers": fetch_arxiv_papers(days_back=7, limit=15),
        "hn_discussions": fetch_hacker_news_ai(limit=8),
        "github_trending": fetch_github_trending_ai(limit=6),
    }

    print(f"\n✅ 采集完成！")
    print(f"   📄 论文: {len(data['papers'])} 篇")
    print(f"   💬 HN讨论: {len(data['hn_discussions'])} 条")
    print(f"   🐙 GitHub项目: {len(data['github_trending'])} 个")

    return data


def save_data(data: Dict, filename: str = None):
    """
    保存数据到JSON文件
    """
    if filename is None:
        filename = f"ai_insights_{datetime.now().strftime('%Y%m%d')}.json"

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 数据已保存到: {filepath}")
    return filepath


if __name__ == "__main__":
    # 采集数据
    data = generate_weekly_report()

    # 保存数据
    save_data(data)

    print("\n🎉 完成！现在可以生成 HTML 报告了")
    print("   运行: python generate_html.py")
