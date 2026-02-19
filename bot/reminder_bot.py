#!/usr/bin/env python3
"""
Reminder Bot - Test Version
Automated reminders and scheduling
"""

import json
import os
from datetime import datetime, timedelta

# Reminders storage
REMINDERS_FILE = "/root/.openclaw/workspace/bot/reminders.json"

def load_reminders():
    """Load reminders from file"""
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_reminders(reminders):
    """Save reminders to file"""
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)

def add_reminder(message, time_str, repeat="once"):
    """Add a new reminder"""
    reminders = load_reminders()
    reminder = {
        "id": len(reminders) + 1,
        "message": message,
        "time": time_str,
        "repeat": repeat,
        "created": datetime.now().isoformat()
    }
    reminders.append(reminder)
    save_reminders(reminders)
    return f"Reminder added: {message} at {time_str}"

def list_reminders():
    """List all reminders"""
    reminders = load_reminders()
    if not reminders:
        return "No reminders set."
    
    result = "=== Reminders ===\n"
    for r in reminders:
        result += f"{r['id']}. {r['message']} at {r['time']} ({r['repeat']})\n"
    return result

def delete_reminder(reminder_id):
    """Delete a reminder"""
    reminders = load_reminders()
    reminders = [r for r in reminders if r['id'] != reminder_id]
    save_reminders(reminders)
    return f"Reminder {reminder_id} deleted."

# Test
if __name__ == "__main__":
    # Add test reminder
    print(add_reminder("检查AI研究", "09:00", "daily"))
    print(add_reminder("运动", "18:00", "weekly"))
    print()
    print(list_reminders())
