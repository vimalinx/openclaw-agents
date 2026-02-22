#!/usr/bin/env python3
"""
Wilson 心跳检查脚本
每天早8点/晚8点自动执行
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path

# 配置
HEARTBEAT_STATE = Path("/home/vimalinx/.openclaw/workspace/heartbeat-state.json")
MEMORY_MD = Path("/home/vimalinx/.openclaw/workspace/MEMORY.md")
DAILY_MEMORY_DIR = Path("/home/vimalinx/.openclaw/workspace/memory")

def load_state():
    """加载心跳状态"""
    if HEARTBEAT_STATE.exists():
        with open(HEARTBEAT_STATE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"lastChecks": {}, "keywords": {}, "monitoredAccounts": []}

def save_state(state):
    """保存心跳状态"""
    with open(HEARTBEAT_STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def check_calendar():
    """检查日程提醒"""
    import subprocess

    try:
        # 获取未来2小时的日程
        result = subprocess.run(
            ["python3", "calendar-manager.py", "upcoming"],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            output = result.stdout.strip()
            if "未来24小时内没有日程" not in output:
                return f"⚠️ 有即将到来的日程:\n{output}"
            else:
                return "✅ 未来24小时内无日程"
        else:
            return "❌ 日程检查失败"
    except Exception as e:
        return f"⚠️ 日历检查异常: {e}"

def check_email():
    """检查邮件（暂时返回待实现）"""
    return "⏳ 邮箱集成待实现"

def check_project_progress():
    """检查项目进度"""
    return {
        "VimaOS": "原型位置不存在",
        "小红书自动化": "核心功能已完成",
        "OpenClaw skills": "正常"
    }

def check_memory_update():
    """检查上次 MEMORY.md 更新时间"""
    if MEMORY_MD.exists():
        import os
        mtime = MEMORY_MD.stat().st_mtime
        last_update = datetime.fromtimestamp(mtime)
        days_ago = (datetime.now() - last_update).days

        if days_ago >= 3:
            return f"⚠️ 已 {days_ago} 天未更新，建议整理"
        else:
            return f"✅ {days_ago} 天前更新"
    return "❌ 文件不存在"

def generate_report():
    """生成心跳报告"""
    state = load_state()
    now = datetime.now()

    report = []
    report.append(f"🐺 Wilson 心跳报告 | {now.strftime('%Y-%m-%d %H:%M')}\n")

    # 邮箱检查
    email_status = check_email()
    report.append(f"\n📧 邮箱状态\n{email_status}")

    # 日程检查
    calendar_status = check_calendar()
    report.append(f"\n📅 日程检查\n{calendar_status}")

    # 项目进度
    progress = check_project_progress()
    report.append(f"\n📝 项目进度")
    for project, status in progress.items():
        report.append(f"  - {project}: {status}")

    # MEMORY.md 更新
    memory_status = check_memory_update()
    report.append(f"\n🧠 记忆文件\n{memory_status}")

    # 热点追踪建议
    report.append(f"\n🔥 热点追踪建议")
    report.append("  需要实现 MediaCrawler 集成")

    # 机会推荐
    report.append(f"\n💡 今日建议")
    report.append("  1. 实现小红书自动化闭环")
    report.append("  2. 配置日程集成")

    # 更新状态
    state["lastChecks"]["email"] = now.strftime('%Y-%m-%d %H:%M')
    state["lastChecks"]["calendar"] = now.strftime('%Y-%m-%d %H:%M')
    save_state(state)

    return "\n".join(report)

async def main():
    """主函数"""
    report = generate_report()

    # 保存报告
    report_file = Path("/home/vimalinx/.openclaw/workspace/heartbeat-report.txt")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print("=" * 50)
    print(report)
    print("=" * 50)
    print(f"\n✅ 报告已保存到: {report_file}")

if __name__ == "__main__":
    asyncio.run(main())
