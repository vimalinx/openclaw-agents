#!/usr/bin/env python3
"""
生成 AI 前沿信息报告 HTML
"""

import json
import os
from datetime import datetime
from jinja2 import Template

# 配置
OUTPUT_DIR = "/home/vimalinx/.openclaw/workspace/ai_insights"
DATA_DIR = f"{OUTPUT_DIR}/data"

# HTML 模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>AI前沿信息周报 - {{ report_date }}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            font-size: 11px;
            line-height: 1.4;
            color: #2C3E50;
            background: white;
        }

        .container {
            width: 794px;
            margin: 0 auto;
            background: white;
        }

        /* 封面 - 完整A4 */
        .cover {
            width: 794px;
            height: 1123px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: url('https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1600&h=900&fit=crop') center/cover;
            position: relative;
            color: white;
            page-break-after: always;
        }

        .cover::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        }

        .cover > * {
            position: relative;
            z-index: 1;
        }

        .cover h1 {
            font-family: 'Noto Serif SC', serif;
            font-size: 52px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: 4px;
        }

        .cover .subtitle {
            font-size: 22px;
            font-weight: 300;
            margin-bottom: 30px;
            letter-spacing: 2px;
            opacity: 0.95;
        }

        .cover .info {
            font-size: 14px;
            opacity: 0.9;
            text-align: center;
        }

        .cover .divider {
            width: 80px;
            height: 2px;
            background: rgba(255,255,255,0.6);
            margin: 25px auto;
        }

        /* 内容页通用 */
        .page {
            width: 794px;
            min-height: 1123px;
            padding: 30px 40px;
            position: relative;
            background: white;
            page-break-after: always;
        }

        .page-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px 20px;
            margin: -30px -40px 20px -40px;
            position: relative;
            overflow: hidden;
        }

        .page-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&h=400&fit=crop') center/cover;
            opacity: 0.12;
        }

        .page-header h2 {
            font-family: 'Noto Serif SC', serif;
            font-size: 28px;
            color: white;
            position: relative;
            z-index: 1;
            margin-bottom: 5px;
        }

        .page-header .meta {
            font-size: 12px;
            color: rgba(255,255,255,0.85);
            position: relative;
            z-index: 1;
        }

        /* 论文列表 */
        .paper-item {
            background: #f8f9fa;
            border-left: 3px solid #667eea;
            padding: 12px 15px;
            margin-bottom: 12px;
            page-break-inside: avoid;
        }

        .paper-title {
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 5px;
            line-height: 1.3;
        }

        .paper-meta {
            font-size: 10px;
            color: #7f8c8d;
            margin-bottom: 6px;
        }

        .paper-summary {
            color: #5a6c7d;
            line-height: 1.4;
        }

        .category-tag {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 9px;
            margin-right: 5px;
        }

        /* HN讨论 */
        .hn-item {
            border-bottom: 1px solid #eee;
            padding: 10px 0;
            page-break-inside: avoid;
        }

        .hn-title {
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 4px;
        }

        .hn-meta {
            font-size: 10px;
            color: #7f8c8d;
        }

        .hn-score {
            color: #ff6600;
            font-weight: 600;
        }

        /* GitHub项目 */
        .github-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }

        .github-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 12px;
            page-break-inside: avoid;
        }

        .repo-name {
            font-weight: 600;
            color: #667eea;
            margin-bottom: 4px;
        }

        .repo-desc {
            color: #5a6c7d;
            line-height: 1.4;
            margin-bottom: 6px;
            font-size: 10px;
        }

        .repo-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 10px;
            color: #7f8c8d;
        }

        .repo-tags span {
            display: inline-block;
            background: #e9ecef;
            padding: 1px 6px;
            border-radius: 4px;
            margin-right: 3px;
            font-size: 9px;
        }

        /* 统计卡片 */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 20px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-number {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 11px;
            opacity: 0.9;
        }

        /* 装饰图片 */
        .decor-image {
            position: absolute;
            bottom: 20px;
            left: 20px;
            width: 200px;
            height: 150px;
            opacity: 0.3;
            background: url('https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=400&h=300&fit=crop') center/cover;
            border-radius: 8px;
            z-index: 0;
        }

        /* 打印优化 */
        @media print {
            body {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
            .page {
                page-break-after: always;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 封面 -->
        <div class="cover">
            <h1>AI前沿信息</h1>
            <div class="divider"></div>
            <div class="subtitle">第 {{ week_number }} 周周报</div>
            <div class="info">
                <p>{{ report_date }}</p>
                <p style="margin-top: 10px;">涵盖论文 · 技术 · 社区 · 项目</p>
            </div>
        </div>

        <!-- 统计概览 -->
        <div class="page">
            <div class="decor-image"></div>
            <div class="page-header">
                <h2>本周概览</h2>
                <div class="meta">Overview | Week {{ week_number }}</div>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{{ papers|length }}</div>
                    <div class="stat-label">arXiv 论文</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ hn_discussions|length }}</div>
                    <div class="stat-label">HN 热门讨论</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{{ github_trending|length }}</div>
                    <div class="stat-label">热门项目</div>
                </div>
            </div>

            <h3 style="margin: 20px 0 10px 0; color: #667eea;">📚 本周热点领域</h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 6px;">
                <p style="color: #5a6c7d; line-height: 1.6;">
                    本周 AI 领域持续火热，大语言模型应用、多智能体系统、视觉生成技术仍是核心关注点。
                    社区讨论集中在模型推理效率优化、实际应用场景落地、以及开源工具的生态建设。
                </p>
            </div>
        </div>

        <!-- 论文部分 -->
        <div class="page">
            <div class="page-header">
                <h2>arXiv 热门论文</h2>
                <div class="meta">Latest Research from arXiv</div>
            </div>

            {% for paper in papers[:8] %}
            <div class="paper-item">
                <div class="paper-title">{{ paper.title }}</div>
                <div class="paper-meta">
                    <span class="category-tag">{{ paper.category }}</span>
                    <span>{{ paper.authors|join(', ') }}</span>
                </div>
                <div class="paper-summary">{{ paper.summary }}</div>
            </div>
            {% endfor %}
        </div>

        {% if papers|length > 8 %}
        <!-- 论文续页 -->
        <div class="page">
            <div class="page-header">
                <h2>arXiv 热门论文 (续)</h2>
                <div class="meta">More Papers</div>
            </div>

            {% for paper in papers[8:] %}
            <div class="paper-item">
                <div class="paper-title">{{ paper.title }}</div>
                <div class="paper-meta">
                    <span class="category-tag">{{ paper.category }}</span>
                    <span>{{ paper.authors|join(', ') }}</span>
                </div>
                <div class="paper-summary">{{ paper.summary }}</div>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <!-- HN讨论 -->
        <div class="page">
            <div class="page-header">
                <h2>Hacker News 热门讨论</h2>
                <div class="meta">Community Insights</div>
            </div>

            {% for hn in hn_discussions %}
            <div class="hn-item">
                <div class="hn-title">{{ hn.title }}</div>
                <div class="hn-meta">
                    <span class="hn-score">▲ {{ hn.score }}</span>
                    <span style="margin: 0 10px;">💬 {{ hn.comments }}</span>
                    <span>{{ hn.time }}</span>
                </div>
            </div>
            {% endfor %}
        </div>

        <!-- GitHub项目 -->
        <div class="page">
            <div class="page-header">
                <h2>GitHub 热门AI项目</h2>
                <div class="meta">Trending Projects</div>
            </div>

            <div class="github-grid">
                {% for repo in github_trending %}
                <div class="github-card">
                    <div class="repo-name">{{ repo.name }}</div>
                    <div class="repo-desc">{{ repo.description }}</div>
                    <div class="repo-meta">
                        <div class="repo-tags">
                            {% for tag in repo.tags %}
                            <span>{{ tag }}</span>
                            {% endfor %}
                        </div>
                        <div>⭐ {{ repo.stars|int }}</div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
"""


def load_latest_data() -> dict:
    """加载最新的数据文件"""
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"数据目录不存在: {DATA_DIR}")

    # 找到最新的JSON文件
    json_files = [f for f in os.listdir(DATA_DIR) if f.startswith('ai_insights_') and f.endswith('.json')]

    if not json_files:
        raise FileNotFoundError("没有找到数据文件，请先运行 fetch_ai_insights.py")

    # 按修改时间排序，取最新的
    latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(DATA_DIR, f)))

    with open(os.path.join(DATA_DIR, latest_file), 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📂 加载数据: {latest_file}")
    return data


def generate_html(data: dict) -> str:
    """生成HTML"""
    print("\n🎨 正在生成HTML...")

    template = Template(HTML_TEMPLATE)
    html_content = template.render(**data)

    # 保存HTML
    output_file = os.path.join(OUTPUT_DIR, f"ai_insights_{datetime.now().strftime('%Y%m%d')}.html")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML已生成: {output_file}")
    return output_file


if __name__ == "__main__":
    # 加载数据
    data = load_latest_data()

    # 生成HTML
    html_file = generate_html(data)

    print(f"\n🌐 在浏览器中打开: file://{html_file}")
    print("   或打印为PDF: Ctrl+P → 保存为PDF")
