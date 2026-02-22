#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler 小红书搜索功能测试脚本
测试目标：搜索小红书热门内容并分析结果
"""

import json
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import shutil

# 搜索关键词配置
SEARCH_KEYWORDS = ["AI工具", "效率神器", "副业搞钱", "小红书运营"]

# 输出配置
OUTPUT_DIR = Path("mediacrawler_search_results")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_FILE = OUTPUT_DIR / f"xhs_search_results_{TIMESTAMP}.json"

def setup_environment():
    """配置环境"""
    print("=" * 60)
    print("MediaCrawler 小红书搜索功能测试")
    print("=" * 60)

    # 创建输出目录
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"✓ 输出目录已创建: {OUTPUT_DIR}")

    # 备份原始配置
    config_file = "mediacrawler/config/base_config.py"
    backup_file = f"mediacrawler/config/base_config.py.backup_{TIMESTAMP}"

    if not os.path.exists(backup_file):
        shutil.copy(config_file, backup_file)
        print(f"✓ 原始配置已备份: {backup_file}")

    return config_file

def modify_config(config_file):
    """修改配置文件"""
    print("\n" + "=" * 60)
    print("修改配置文件...")
    print("=" * 60)

    with open(config_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 修改关键词
    new_keywords = ",".join(SEARCH_KEYWORDS)
    content = content.replace(
        'KEYWORDS = "AI工具,ChatGPT,编程学习,Python教程,副业编程,AI绘画,机器学习,前端开发"',
        f'KEYWORDS = "{new_keywords}"'
    )
    print(f"✓ 搜索关键词设置为: {new_keywords}")

    # 修改爬取数量为每个关键词 20 个笔记
    content = content.replace(
        'CRAWLER_MAX_NOTES_COUNT = 50',
        'CRAWLER_MAX_NOTES_COUNT = 20'
    )
    print("✓ 每个关键词爬取数量设置为: 20")

    # 确保保存为 JSON 格式
    content = content.replace(
        'SAVE_DATA_OPTION = "json"',
        'SAVE_DATA_OPTION = "json"'
    )

    # 设置数据保存路径
    content = content.replace(
        'SAVE_DATA_PATH = ""',
        f'SAVE_DATA_PATH = "{OUTPUT_DIR}"'
    )
    print(f"✓ 数据保存路径设置为: {OUTPUT_DIR}")

    # 关闭词云生成（加快速度）
    content = content.replace(
        'ENABLE_GET_WORDCLOUD = False',
        'ENABLE_GET_WORDCLOUD = False'
    )

    # 保存配置
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ 配置文件已更新")

def run_crawler():
    """运行 MediaCrawler"""
    print("\n" + "=" * 60)
    print("运行 MediaCrawler 爬虫...")
    print("=" * 60)

    os.chdir("mediacrawler")

    # 使用虚拟环境运行
    cmd = [
        ".venv/bin/python",
        "main.py",
        "--platform", "xhs",
        "--lt", "qrcode",
        "--type", "search"
    ]

    print(f"执行命令: {' '.join(cmd)}")
    print("\n注意：这将打开浏览器，请使用小红书APP扫码登录...")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        print("\n" + "=" * 60)
        print("爬虫执行完成")
        print("=" * 60)

        if result.stdout:
            print("标准输出:")
            print(result.stdout[-2000:])  # 只显示最后2000字符

        if result.stderr:
            print("错误输出:")
            print(result.stderr[-2000:])

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("错误：爬虫执行超时（10分钟）")
        return False
    except Exception as e:
        print(f"错误：爬虫执行失败 - {e}")
        return False
    finally:
        os.chdir("..")

def collect_results():
    """收集搜索结果"""
    print("\n" + "=" * 60)
    print("收集搜索结果...")
    print("=" * 60)

    results = []

    # 扫描输出目录中的 JSON 文件
    json_files = list(OUTPUT_DIR.glob("*.json"))

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                results.extend(data)
            print(f"✓ 已加载: {json_file.name} ({len(data)} 条记录)")
        except Exception as e:
            print(f"✗ 加载失败: {json_file.name} - {e}")

    print(f"\n总共收集到 {len(results)} 条笔记")

    return results

def analyze_results(results):
    """分析搜索结果"""
    print("\n" + "=" * 60)
    print("分析搜索结果...")
    print("=" * 60)

    if not results:
        print("错误：没有搜索结果")
        return None

    analysis = {
        "total_notes": len(results),
        "keywords": SEARCH_KEYWORDS,
        "notes": [],
        "trends": {},
        "content_suggestions": [],
        "best_practices": []
    }

    # 统计数据
    total_views = 0
    total_likes = 0
    total_collects = 0
    title_lengths = []
    image_counts = []

    for note in results:
        note_data = {
            "title": note.get("title", ""),
            "url": note.get("note_id", ""),
            "views": note.get("view_count", 0),
            "likes": note.get("liked_count", 0),
            "collects": note.get("collected_count", 0),
            "comments": note.get("comment_count", 0),
            "title_length": len(note.get("title", "")),
            "image_count": len(note.get("images", [])),
            "content": note.get("desc", "")[:200]  # 前200字符
        }

        analysis["notes"].append(note_data)

        # 累计统计
        total_views += note_data["views"]
        total_likes += note_data["likes"]
        total_collects += note_data["collects"]
        title_lengths.append(note_data["title_length"])
        image_counts.append(note_data["image_count"])

    # 计算平均值
    if results:
        analysis["trends"]["avg_views"] = total_views // len(results)
        analysis["trends"]["avg_likes"] = total_likes // len(results)
        analysis["trends"]["avg_collects"] = total_collects // len(results)
        analysis["trends"]["avg_title_length"] = sum(title_lengths) // len(title_lengths)
        analysis["trends"]["avg_image_count"] = sum(image_counts) // len(image_counts)

        # 找出最受欢迎的笔记
        sorted_notes = sorted(analysis["notes"], key=lambda x: x["likes"], reverse=True)
        analysis["trends"]["top_notes"] = sorted_notes[:10]

        # 找出标题最长的笔记
        sorted_by_title = sorted(analysis["notes"], key=lambda x: x["title_length"], reverse=True)
        analysis["trends"]["longest_titles"] = sorted_by_title[:5]

        # 找出配图最多的笔记
        sorted_by_images = sorted(analysis["notes"], key=lambda x: x["image_count"], reverse=True)
        analysis["trends"]["most_images"] = sorted_by_images[:5]

    print(f"✓ 笔记总数: {analysis['total_notes']}")
    print(f"✓ 平均浏览量: {analysis['trends'].get('avg_views', 0)}")
    print(f"✓ 平均点赞数: {analysis['trends'].get('avg_likes', 0)}")
    print(f"✓ 平均收藏数: {analysis['trends'].get('avg_collects', 0)}")
    print(f"✓ 平均标题长度: {analysis['trends'].get('avg_title_length', 0)} 字")
    print(f"✓ 平均配图数: {analysis['trends'].get('avg_image_count', 0)} 张")

    # 生成内容建议
    analysis["content_suggestions"] = generate_content_suggestions(analysis)
    analysis["best_practices"] = generate_best_practices(analysis)

    return analysis

def generate_content_suggestions(analysis):
    """生成内容建议"""
    suggestions = []

    trends = analysis.get("trends", {})
    top_notes = trends.get("top_notes", [])

    if top_notes:
        suggestions.append("📌 热门笔记标题特征分析：")

        for note in top_notes[:5]:
            title = note.get("title", "")
            likes = note.get("likes", 0)
            suggestions.append(f"   - {title[:50]}... (点赞: {likes})")

    suggestions.append("\n🎯 内容优化建议：")
    avg_title_len = trends.get("avg_title_length", 0)
    avg_images = trends.get("avg_image_count", 0)

    if avg_title_len > 0:
        suggestions.append(f"   - 建议标题长度在 {avg_title_len-5}-{avg_title_len+5} 字之间")

    if avg_images > 0:
        suggestions.append(f"   - 建议配图数量在 {avg_images-1}-{avg_images+2} 张左右")

    suggestions.append("   - 标题中包含数字、疑问句、感叹句更容易吸引点击")
    suggestions.append("   - 封面图应清晰、美观，突出主题")
    suggestions.append("   - 内容要有实用性，解决用户痛点")
    suggestions.append("   - 合理使用标签和话题，提高曝光")

    return suggestions

def generate_best_practices(analysis):
    """生成最佳实践建议"""
    practices = []

    practices.append("📚 小红书热门笔记最佳实践：")

    practices.append("\n1️⃣ 标题优化：")
    practices.append("   - 使用疑问句：'如何...''为什么...'")
    practices.append("   - 使用数字：'5个技巧''3种方法'")
    practices.append("   - 突出痛点：'解决...问题''告别...烦恼'")
    practices.append("   - 添加表情符号，增加视觉吸引力")

    practices.append("\n2️⃣ 内容结构：")
    practices.append("   - 开头点明主题，快速抓住用户注意")
    practices.append("   - 中间详细展开，提供实用价值")
    practices.append("   - 结尾引导互动：点赞、收藏、评论")
    practices.append("   - 适当分段，使用小标题提高可读性")

    practices.append("\n3️⃣ 配图策略：")
    practices.append("   - 封面图：高清、美观、信息明确")
    practices.append("   - 内容图：图文结合，信息丰富")
    practices.append("   - 图片尺寸：建议 1080x1440 或 3:4 比例")
    practices.append("   - 使用统一风格，建立个人品牌")

    practices.append("\n4️⃣ 发布时间：")
    practices.append("   - 工作日：12:00-13:00, 18:00-22:00")
    practices.append("   - 周末：09:00-11:00, 15:00-22:00")
    practices.append("   - 根据目标用户活跃时间调整")

    practices.append("\n5️⃣ 互动策略：")
    practices.append("   - 及时回复评论，增加用户粘性")
    practices.append("   - 在结尾引导用户：'觉得有用请收藏'")
    practices.append("   - 参与热门话题，增加曝光机会")
    practices.append("   - 与其他博主互动，扩大影响力")

    return practices

def generate_report(analysis):
    """生成测试报告"""
    print("\n" + "=" * 60)
    print("生成测试报告...")
    print("=" * 60)

    report_lines = []

    report_lines.append("# MediaCrawler 小红书搜索功能测试报告")
    report_lines.append(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"\n## 搜索关键词")
    report_lines.append(", ".join(SEARCH_KEYWORDS))

    report_lines.append(f"\n## 搜索结果统计")
    report_lines.append(f"- 笔记总数: {analysis['total_notes']}")
    report_lines.append(f"- 平均浏览量: {analysis['trends'].get('avg_views', 0)}")
    report_lines.append(f"- 平均点赞数: {analysis['trends'].get('avg_likes', 0)}")
    report_lines.append(f"- 平均收藏数: {analysis['trends'].get('avg_collects', 0)}")
    report_lines.append(f"- 平均标题长度: {analysis['trends'].get('avg_title_length', 0)} 字")
    report_lines.append(f"- 平均配图数: {analysis['trends'].get('avg_image_count', 0)} 张")

    report_lines.append("\n## 热门笔记 TOP 10")
    top_notes = analysis['trends'].get('top_notes', [])
    for i, note in enumerate(top_notes[:10], 1):
        report_lines.append(f"\n### {i}. {note.get('title', '')}")
        report_lines.append(f"- URL: {note.get('url', '')}")
        report_lines.append(f"- 浏览量: {note.get('views', 0)}")
        report_lines.append(f"- 点赞: {note.get('likes', 0)}")
        report_lines.append(f"- 收藏: {note.get('collects', 0)}")
        report_lines.append(f"- 评论: {note.get('comments', 0)}")
        report_lines.append(f"- 标题长度: {note.get('title_length', 0)} 字")
        report_lines.append(f"- 配图数: {note.get('image_count', 0)} 张")
        report_lines.append(f"- 内容预览: {note.get('content', '')[:100]}...")

    report_lines.append("\n## 内容趋势分析")
    report_lines.append("\n### 标题特征")
    longest_titles = analysis['trends'].get('longest_titles', [])
    report_lines.append("标题较长的笔记示例：")
    for note in longest_titles[:3]:
        report_lines.append(f"- {note.get('title', '')} ({note.get('title_length', 0)} 字)")

    report_lines.append("\n### 配图策略")
    most_images = analysis['trends'].get('most_images', [])
    report_lines.append("配图较多的笔记示例：")
    for note in most_images[:3]:
        report_lines.append(f"- {note.get('title', '')} ({note.get('image_count', 0)} 张图)")

    report_lines.append("\n## 内容建议")
    for suggestion in analysis['content_suggestions']:
        report_lines.append(f"{suggestion}")

    report_lines.append("\n## 最佳实践建议")
    for practice in analysis['best_practices']:
        report_lines.append(f"{practice}")

    # 保存报告
    report_file = OUTPUT_DIR / f"xhs_search_report_{TIMESTAMP}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"✓ 测试报告已保存: {report_file}")

    # 同时保存 JSON 格式的分析结果
    analysis_file = OUTPUT_DIR / f"xhs_search_analysis_{TIMESTAMP}.json"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"✓ 分析数据已保存: {analysis_file}")

    return report_file

def main():
    """主函数"""
    try:
        # 1. 设置环境
        config_file = setup_environment()

        # 2. 修改配置
        modify_config(config_file)

        # 3. 运行爬虫
        success = run_crawler()

        if not success:
            print("\n错误：爬虫执行失败，请检查错误信息")
            return 1

        # 4. 收集结果
        results = collect_results()

        if not results:
            print("\n警告：没有收集到搜索结果")
            return 1

        # 5. 分析结果
        analysis = analyze_results(results)

        if not analysis:
            print("\n错误：结果分析失败")
            return 1

        # 6. 生成报告
        report_file = generate_report(analysis)

        print("\n" + "=" * 60)
        print("✓ 测试完成！")
        print("=" * 60)
        print(f"\n查看完整报告: {report_file}")

        return 0

    except Exception as e:
        print(f"\n错误：{e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
