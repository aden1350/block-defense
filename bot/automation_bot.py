#!/usr/bin/env python3
"""
Automation Bot - Test Version
Runs scheduled tasks and reports
"""

import json
import os
from datetime import datetime
from ddgs import DDGS

# Tasks storage
TASKS_FILE = "/root/.openclaw/workspace/bot/tasks.json"

def load_tasks():
    """Load tasks from file"""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to file"""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(name, schedule, action):
    """Add a new automated task"""
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "name": name,
        "schedule": schedule,
        "action": action,
        "last_run": None,
        "enabled": True
    }
    tasks.append(task)
    save_tasks(tasks)
    return f"Task added: {name}"

def run_task(task):
    """Run a specific task"""
    action = task.get('action', {})
    action_type = action.get('type', 'search')
    
    if action_type == 'search':
        query = action.get('query', '')
        ddgs = DDGS()
        results = ddgs.text(query, max_results=5)
        return [r['title'] for r in results]
    
    return ["Unknown action type"]

def list_tasks():
    """List all tasks"""
    tasks = load_tasks()
    if not tasks:
        return "No tasks configured."
    
    result = "=== Automated Tasks ===\n"
    for t in tasks:
        status = "✅" if t.get('enabled') else "❌"
        result += f"{status} {t['name']} - {t['schedule']}\n"
    return result

# Test
if __name__ == "__main__":
    # Add test tasks
    print(add_task("Daily AI News", "daily", {"type": "search", "query": "AI news today"}))
    print(add_task("Crypto Prices", "hourly", {"type": "search", "query": "Bitcoin price today"}))
    print()
    print(list_tasks())
    
    # Run a task
    tasks = load_tasks()
    if tasks:
        print("\n=== Running task: Daily AI News ===")
        results = run_task(tasks[0])
        for r in results:
            print(f"- {r}")
