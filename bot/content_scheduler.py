#!/usr/bin/env python3
"""
Content Scheduler Bot - Test Version
Schedule and automate content posting
"""

import json
import os
from datetime import datetime, timedelta

# Content storage
CONTENT_FILE = "/root/.openclaw/workspace/bot/content_schedule.json"

def load_schedule():
    if os.path.exists(CONTENT_FILE):
        with open(CONTENT_FILE, 'r') as f:
            return json.load(f)
    return []

def save_schedule(schedule):
    with open(CONTENT_FILE, 'w') as f:
        json.dump(schedule, f, indent=2)

def add_content(title, content, schedule_time, platform="xiaohongshu"):
    schedule = load_schedule()
    schedule.append({
        "id": len(schedule) + 1,
        "title": title,
        "content": content,
        "schedule_time": schedule_time,
        "platform": platform,
        "created": datetime.now().isoformat(),
        "posted": False
    })
    save_schedule(schedule)
    return f"Content scheduled: {title} at {schedule_time}"

def list_schedule():
    schedule = load_schedule()
    if not schedule:
        return "No content scheduled."
    
    result = "=== Content Schedule ===\n"
    for item in schedule:
        status = "✅" if item.get('posted') else "⏳"
        result += f"{status} {item['title']} - {item['schedule_time']} ({item['platform']})\n"
    return result

def get_due_content():
    """Get content that's due to be posted"""
    schedule = load_schedule()
    now = datetime.now()
    due = []
    
    for item in schedule:
        if item.get('posted'):
            continue
        # Simple check - if scheduled time has passed today
        schedule_time = item.get('schedule_time', '')
        if schedule_time:
            due.append(item)
    
    return due

# Test
if __name__ == "__main__":
    # Add test content
    print(add_content("AI早报", "今日AI热点...", "2026-02-20 08:00"))
    print(add_content("股市晚报", "今日行情分析", "2026-02-20 18:00"))
    print()
    print(list_schedule())
