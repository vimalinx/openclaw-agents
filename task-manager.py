#!/usr/bin/env python3
"""
Wilson 任务管理系统
支持创建、查看、更新、删除任务
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path

TASKS_FILE = Path("/home/vimalinx/.openclaw/workspace/tasks.json")
ARCHIVE_FILE = Path("/home/vimalinx/.openclaw/workspace/tasks-archive.json")

def load_tasks():
    """加载任务"""
    if TASKS_FILE.exists():
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """保存任务"""
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(title, priority="normal", category="general", deadline=None):
    """添加任务"""
    tasks = load_tasks()

    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "priority": priority,  # high, normal, low
        "category": category,  # general, project, idea
        "status": "todo",  # todo, in_progress, done
        "createdAt": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "deadline": deadline,
        "subtasks": []
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return new_task

def list_tasks(filter_status=None, filter_priority=None):
    """列出任务"""
    tasks = load_tasks()

    # 过滤
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]
    if filter_priority:
        tasks = [t for t in tasks if t["priority"] == filter_priority]

    # 排序（优先级 + 创建时间）
    priority_order = {"high": 0, "normal": 1, "low": 2}
    tasks.sort(key=lambda t: (priority_order.get(t["priority"], 1), t["id"]))

    return tasks

def update_task(task_id, status=None, title=None):
    """更新任务"""
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            if status:
                task["status"] = status
                task["completedAt"] = datetime.now().strftime('%Y-%m-%d %H:%M')
            if title:
                task["title"] = title
            break

    save_tasks(tasks)

def delete_task(task_id):
    """删除任务（移动到归档）"""
    tasks = load_tasks()
    archived_tasks = []

    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            archived = tasks.pop(i)
            archived["archivedAt"] = datetime.now().strftime('%Y-%m-%d %H:%M')
            archived_tasks.append(archived)
            break

    save_tasks(tasks)

    # 保存到归档
    if archived_tasks:
        archive = []
        if ARCHIVE_FILE.exists():
            with open(ARCHIVE_FILE, 'r', encoding='utf-8') as f:
                archive = json.load(f)
        archive.extend(archived_tasks)
        with open(ARCHIVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(archive, f, ensure_ascii=False, indent=2)

def format_task(task):
    """格式化任务显示"""
    status_icon = {
        "todo": "⬜",
        "in_progress": "🔄",
        "done": "✅"
    }

    priority_icon = {
        "high": "🔴",
        "normal": "🟡",
        "low": "🟢"
    }

    return f"{status_icon.get(task['status'], '?')} {priority_icon.get(task['priority'], '⚪')} [{task['id']}] {task['title']}"

def print_tasks(tasks):
    """打印任务列表"""
    if not tasks:
        print("🎉 没有待办任务！")
        return

    print("\n📋 任务列表\n")

    for task in tasks:
        print(f"  {format_task(task)}")
        if task.get("deadline"):
            print(f"      ⏰ 截止: {task['deadline']}")
        if task.get("subtasks"):
            for sub in task["subtasks"]:
                print(f"        - {sub}")

async def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("🐺 Wilson 任务管理系统\n")
        print("用法:")
        print("  task.py add <title>              # 添加任务")
        print("  task.py add <title> --high     # 高优先级")
        print("  task.py list                   # 列出所有任务")
        print("  task.py list --todo            # 列出待办")
        print("  task.py list --high            # 列出高优先级")
        print("  task.py done <id>              # 完成任务")
        print("  task.py delete <id>            # 删除任务")
        print("\n示例:")
        print("  task.py add '实现小红书自动化' --high")
        print("  task.py list --todo")
        print("  task.py done 1")
        return

    command = sys.argv[1]
    title = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None

    if command == "add":
        if not title:
            print("❌ 请提供任务标题")
            return
        priority = "--high" in sys.argv and "high" or "normal"
        task = add_task(title, priority)
        print(f"✅ 任务已添加: {format_task(task)}")

    elif command == "list":
        status = "--todo" in sys.argv and "todo" or None
        priority = "--high" in sys.argv and "high" or None
        tasks = list_tasks(filter_status=status, filter_priority=priority)
        print_tasks(tasks)

    elif command == "done":
        if not title or not title.isdigit():
            print("❌ 请提供任务ID")
            return
        update_task(int(title), status="done")
        print(f"✅ 任务已标记完成: #{title}")

    elif command == "delete":
        if not title or not title.isdigit():
            print("❌ 请提供任务ID")
            return
        delete_task(int(title))
        print(f"🗑️ 任务已删除: #{title}")

    else:
        print(f"❌ 未知命令: {command}")

if __name__ == "__main__":
    asyncio.run(main())
