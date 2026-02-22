#!/usr/bin/env python3
"""
日程集成系统
支持添加日程、查询日程、提前提醒
"""
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path

CALENDAR_FILE = Path("/home/vimalinx/.openclaw/workspace/calendar.json")
REMINDERS_FILE = Path("/home/vimalinx/.openclaw/workspace/reminders.json")

def load_calendar():
    """加载日程"""
    if CALENDAR_FILE.exists():
        with open(CALENDAR_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_calendar(events):
    """保存日程"""
    with open(CALENDAR_FILE, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

def add_event(title, date, time=None, duration=60, reminder_hours=2):
    """添加日程"""
    events = load_calendar()

    event = {
        "id": len(events) + 1,
        "title": title,
        "date": date,  # YYYY-MM-DD
        "time": time,  # HH:MM
        "duration": duration,  # 分钟
        "reminder_hours": reminder_hours,  # 提前提醒小时数
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "status": "upcoming"
    }

    events.append(event)
    save_calendar(events)

    return event

def list_events(filter_date=None):
    """列出日程"""
    events = load_calendar()

    if filter_date:
        events = [e for e in events if e["date"] == filter_date]

    # 按时间排序
    events.sort(key=lambda e: (e["date"], e["time"] or "00:00"))

    return events

def get_upcoming_events(hours=24):
    """获取未来 N 小时内的日程"""
    events = load_calendar()
    now = datetime.now()
    upcoming = []

    for event in events:
        event_datetime = datetime.strptime(f"{event['date']} {event.get('time', '00:00')}", '%Y-%m-%d %H:%M')

        if now <= event_datetime <= now + timedelta(hours=hours):
            upcoming.append(event)

    return upcoming

def format_event(event):
    """格式化日程显示"""
    status_icon = {
        "upcoming": "📅",
        "done": "✅",
        "cancelled": "❌"
    }

    time_str = event.get('time', '全天')
    return f"{status_icon.get(event['status'], '?')} {event['date']} {time_str} - {event['title']} ({event['duration']}分钟)"

async def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("🐺 Wilson 日程管理系统\n")
        print("用法:")
        print("  calendar.py add <title> <date> [time]  # 添加日程")
        print("  calendar.py list                          # 列出所有日程")
        print("  calendar.py list <date>                   # 列出指定日期")
        print("  calendar.py upcoming                      # 列出未来24小时日程")
        print("\n示例:")
        print("  calendar.py add '客户会议' 2026-02-21 14:00")
        print("  calendar.py upcoming")
        print("  calendar.py list 2026-02-21")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 4:
            print("❌ 请提供标题和日期")
            print("用法: calendar.py add <title> <date> [time]")
            return

        title = sys.argv[2]
        date = sys.argv[3]
        time = sys.argv[4] if len(sys.argv) > 4 else None

        try:
            event = add_event(title, date, time)
            print(f"✅ 日程已添加: {format_event(event)}")
        except Exception as e:
            print(f"❌ 添加失败: {e}")

    elif command == "list":
        date_filter = sys.argv[2] if len(sys.argv) > 2 else None
        events = list_events(filter_date=date_filter)

        if not events:
            print("🎉 没有相关日程")
            return

        print("\n📅 日程列表\n")
        for event in events:
            print(f"  {format_event(event)}")

    elif command == "upcoming":
        events = get_upcoming_events(hours=24)

        if not events:
            print("🎉 未来24小时内没有日程")
            return

        print("\n📅 未来24小时日程\n")
        for event in events:
            print(f"  {format_event(event)}")
            print(f"      ⏰ 提前{event.get('reminder_hours', 2)}小时提醒")

    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    asyncio.run(main())
