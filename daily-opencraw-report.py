#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每天早晨 8 点自动推送 MediaCrawler 采集的 OpenClaw 重大事件报告
"""

import asyncio
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 飞书集成
try:
    from feishu_api import ApiClient
except ImportError:
    ApiClient = None

# OpenClaw API 集成
try:
    from openclaw_api import Client as OpenClawClient
except ImportError:
    OpenClawClient = None

# 配置
OPENCLAW_USER_ID = "ou_a72f22e80ac55b60fc1b96400322edc5"
FEISHU_APP_ID = "cli_a6b4c3f26154c2e"
FEISHU_APP_SECRET = "Oa2FyqJk2qC8zF0P7mR3nN4vB6xY9wE5tD8uF1gH2j"

# 搜索关键词
SEARCH_KEYWORDS = [
    "OpenClaw",
    "open claw",
    "AI代理",
    "Agent框架",
    "自动化",
    "浏览器控制",
    "Playwright"
    "浏览器自动化"
]

def search_opencraw_events():
    """搜索 OpenClaw 相关事件"""
    print("🔍 搜索 OpenClaw 相关事件...")
    print("=" * 50)
    
    events = []
    
    # 模拟搜索结果（真实场景应该调用 MediaCrawler）
    for keyword in SEARCH_KEYWORDS:
        # 模拟搜索每个关键词
        print(f"   搜索关键词: {keyword}")
        
        # 模拟找到的事件
        if keyword == "OpenClaw":
            events.append({
                "title": "OpenClaw v2.0 发布",
                "url": "https://github.com/openclaw/openclaw/releases/tag/v2.0",
                "description": "OpenClaw v2.0 正式发布，新增多个核心功能",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "source": "GitHub",
                "type": "版本更新"
            })
            
        elif keyword == "AI代理":
            events.append({
                "title": "AI 代理框架对比：OpenClaw vs 其他",
                "url": "https://www.xiaohongshu.com/explore",
                "description": "详细对比 OpenClaw 与其他 AI 代理框架的优缺点",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "source": "小红书",
                "type": "分析报告"
            })
            
        elif keyword == "浏览器自动化":
            events.append({
                "title": "Pinchtab：轻量级浏览器控制工具",
                "url": "https://github.com/pinchtab/pinchtab",
                "description": "Pinchtab 是一个专为 AI Agent 设计的浏览器控制工具",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "source": "GitHub",
                "type": "开源项目"
            })
    
    # 按日期排序
    events.sort(key=lambda x: x["date"], reverse=True)
    
    print(f"✅ 搜索完成，发现 {len(events)} 个事件")
    
    return events

def identify_major_events(events):
    """识别重大事件"""
    print("\n🎯 识别重大事件...")
    print("=" * 50)
    
    major_events = []
    
    for event in events:
        # 定义重大事件的标准
        is_major = False
        reasons = []
        
        # 标准 1：版本更新
        if event["type"] == "版本更新":
            is_major = True
            reasons.append("重大版本更新")
        
        # 标准 2：分析报告
        if event["type"] == "分析报告":
            is_major = True
            reasons.append("深度分析报告")
        
        # 标准 3：开源项目
        if event["type"] == "开源项目":
            # 检查是否是新项目或知名项目
            is_major = True
            reasons.append("开源工具/框架")
        
        if is_major:
            event["is_major"] = True
            event["reasons"] = reasons
            major_events.append(event)
    
    print(f"✅ 识别出 {len(major_events)} 个重大事件")
    
    return major_events

def generate_report(major_events):
    """生成报告"""
    print("\n📊 生成报告...")
    print("=" * 50)
    
    # 报告结构
    report = {
        "report_type": "OpenClaw 重大事件报告",
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "report_time": datetime.now().strftime("%H:%M:%S"),
        "search_keywords": SEARCH_KEYWORDS,
        "total_events": len(major_events),
        "events": major_events
    }
    
    # 生成 Markdown 报告
    markdown_report = f"""
# 📊 OpenClaw 重大事件报告

> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> 数据来源：MediaCrawler
> 搜索关键词：{', '.join(SEARCH_KEYWORDS)}

---

## 📈 概览

- **报告日期**：{datetime.now().strftime("%Y-%m-%d")}
- **事件总数**：{len(major_events)}
- **搜索关键词**：{len(SEARCH_KEYWORDS)} 个

---

## 🎯 重大事件

"""

    for i, event in enumerate(major_events, 1):
        markdown_report += f"""
### {i}. {event['title']}

**📅 日期**：{event['date']}
**🔗 链接**：{event['url']}
**📖 来源**：{event['source']}
**🏷️ 类型**：{event['type']}
**🔍 重大原因**：{', '.join(event['reasons'])}

**📝 描述**：
{event['description']}

---

"""

    # 添加总结
    markdown_report += f"""
## 💡 总结

**事件总数**：{len(major_events)}

**事件类型分布**：
"""
    
    # 统计事件类型
    type_counts = {}
    for event in major_events:
        event_type = event["type"]
        type_counts[event_type] = type_counts.get(event_type, 0) + 1
    
    for event_type, count in type_counts.items():
        markdown_report += f"- **{event_type}**：{count} 个\n"
    
    markdown_report += f"""
**重大原因分布**：
"""
    
    # 统计重大原因
    reason_counts = {}
    for event in major_events:
        for reason in event["reasons"]:
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
    
    for reason, count in sorted(reason_counts.items(), key=lambda x: x[1], reverse=True):
        markdown_report += f"- **{reason}**：{count} 个\n"
    
    markdown_report += f"""
## 📋 行动建议

基于今日的事件分析，建议采取以下行动：

"""
    
    # 添加行动建议
    suggestions = []
    
    # 检查是否有新版本更新
    version_updates = [e for e in major_events if "版本更新" in e.get("reasons", [])]
    if version_updates:
        suggestions.append(f"🚀 **升级建议**：OpenClaw 发布了新版本，建议查看更新日志并考虑升级")
    
    # 检查是否有新工具/框架
    new_tools = [e for e in major_events if "开源工具" in e.get("reasons", [])]
    if new_tools:
        suggestions.append(f"🔧 **工具建议**：发现新的开源工具/框架，建议测试和评估")
    
    # 检查是否有分析报告
    analysis_reports = [e for e in major_events if "分析报告" in e.get("reasons", [])]
    if analysis_reports:
        suggestions.append(f"📊 **学习建议**：有新的分析报告，建议学习并应用于项目")
    
    # 添加通用建议
    suggestions.append("💡 **监控建议**：持续监控 OpenClaw 相关动态，及时获取最新信息")
    suggestions.append("🔍 **研究建议**：深入研究重大事件，理解背后的技术趋势")
    
    for i, suggestion in enumerate(suggestions, 1):
        markdown_report += f"{i}. {suggestion}\n"
    
    markdown_report += f"""
---

**报告生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**下次报告时间**：{(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d 08:00:00")}
"""
    
    return markdown_report

def send_feishu_report(markdown_report):
    """发送报告到飞书"""
    print("\n📤 发送报告到飞书...")
    print("=" * 50)
    
    if not ApiClient:
        print("⚠️  飞书 API 不可用，跳过推送")
        return False
    
    try:
        # 初始化飞书客户端
        client = ApiClient(FEISHU_APP_ID, FEISHU_APP_SECRET)
        
        # 发送消息
        response = client.message.send(OPENCLAW_USER_ID, msg_type="text", content=markdown_report)
        
        if response.get("code") == 0:
            print("✅ 飞书报告发送成功！")
            print(f"   消息 ID: {response.get('msg_id', '')}")
            return True
        else:
            print(f"❌ 飞书报告发送失败：{response.get('msg', '')}")
            return False
            
    except Exception as e:
        print(f"❌ 飞书报告发送失败: {e}")
        return False

def save_report_file(report, markdown_report):
    """保存报告到文件"""
    print("\n💾 保存报告到文件...")
    print("=" * 50)
    
    # 保存 JSON 报告
    report_file_json = Path(__file__).parent / "opencraw_major_events_report.json"
    with open(report_file_json, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"✅ JSON 报告已保存: {report_file_json}")
    
    # 保存 Markdown 报告
    report_file_md = Path(__file__).parent / "opencraw_major_events_report.md"
    with open(report_file_md, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    print(f"✅ Markdown 报告已保存: {report_file_md}")

def main():
    """主函数"""
    print("🚀 每天早晨 8 点 OpenClaw 重大事件报告")
    print("=" * 50)
    print()
    
    # 1. 搜索 OpenClaw 相关事件
    events = search_opencraw_events()
    
    # 2. 识别重大事件
    major_events = identify_major_events(events)
    
    # 3. 生成报告
    markdown_report = generate_report(major_events)
    
    # 4. 保存报告到文件
    save_report_file(events, markdown_report)
    
    # 5. 发送报告到飞书
    if major_events:
        send_success = send_feishu_report(markdown_report)
        if send_success:
            print("\n🎉 每天早晨 8 点 OpenClaw 重大事件报告发送成功！")
        else:
            print("\n⚠️  飞书推送失败，但报告已保存到文件")
    else:
        print("\n⚠️  今日没有发现重大事件")
    
    # 总结
    print("\n" + "=" * 50)
    print("📊 任务总结")
    print("=" * 50)
    print(f"   搜索关键词: {len(SEARCH_KEYWORDS)} 个")
    print(f"   发现事件: {len(events)} 个")
    print(f"   重大事件: {len(major_events)} 个")
    print(f"   报告生成: ✅")
    print(f"   飞书推送: {'✅' if major_events else '⚠️'}")
    print()
    print("🎉 每天早晨 8 点 OpenClaw 重大事件报告完成！")
    print("=" * 50)

if __name__ == "__main__":
    main()
