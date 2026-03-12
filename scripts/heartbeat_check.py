#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Guardian - OpenClaw Heartbeat Check
Checks for pending health reminders and outputs them for OpenClaw to send
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
STATE_FILE = SCRIPT_DIR / "reminder_state.json"
OUTPUT_FILE = Path.home() / ".health_reminder_message.txt"

# Reminder schedule
REMINDERS = {
    "07:30": {
        "type": "morning",
        "title": "☀️ 早上好！",
        "content": "新的一天开始了！\n\n📅 日期：{date}\n💧 今日饮水目标：3605ml\n🏃 运动目标：30 分钟\n😴 睡觉时间：22:30\n\n加油，向着 90kg 的目标前进！💪"
    },
    "08:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "content": "建议饮用 250ml 温水\n\n保持水分充足有助于新陈代谢和减肥！🥛"
    },
    "10:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "content": "建议饮用 250ml 温水\n\n保持水分充足！🥛"
    },
    "12:00": {
        "type": "meal",
        "title": "🍽️ 午餐时间到了！",
        "content": "健康饮食建议：\n• 多吃蔬菜和高蛋白\n• 控制碳水摄入\n• 七分饱就好\n\n每一餐都是减肥的机会！🥗"
    },
    "14:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "content": "建议饮用 250ml 温水\n\n下午保持水分充足！🥛"
    },
    "16:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "content": "建议饮用 250ml 温水\n\n继续加油！🥛"
    },
    "17:00": {
        "type": "exercise",
        "title": "🏃 运动时间到了！",
        "content": "建议运动 30 分钟：\n• 快走或慢跑\n• 跳绳\n• 俯卧撑/深蹲\n\n运动后记得补充水分！💪"
    },
    "18:00": {
        "type": "meal",
        "title": "🍽️ 晚餐时间到了！",
        "content": "晚餐建议：\n• 清淡为主\n• 少吃碳水\n• 多吃蔬菜\n\n晚餐七分饱！🥗"
    },
    "20:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "content": "建议饮用 250ml 温水\n\n今天是最后一次喝水提醒！🥛"
    },
    "21:30": {
        "type": "sleep",
        "title": "😴 睡前准备时间！",
        "content": "1 小时后该睡觉了 (22:30)\n\n睡前准备：\n• 关闭电子设备\n• 准备呼吸机\n• 调暗灯光\n\n好的睡眠有助于减肥！😴"
    }
}

def load_state():
    """Load reminder state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"lastReminder": None, "lastCheck": None}

def save_state(state):
    """Save reminder state"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def check_reminders():
    """Check if there's a reminder to send"""
    now = datetime.now()
    current_time = f"{now.hour:02d}:{now.minute:02d}"
    today = now.strftime("%Y-%m-%d")
    
    state = load_state()
    
    if current_time in REMINDERS:
        reminder = REMINDERS[current_time]
        reminder_key = f"{today} {current_time}"
        
        # Check if already sent today
        if state.get("lastReminder") != reminder_key:
            # Prepare message
            message = f"{reminder['title']}\n{reminder['content'].format(date=today)}"
            
            # Write to output file for OpenClaw
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                f.write(message)
            
            # Update state
            state["lastReminder"] = reminder_key
            state["lastCheck"] = now.strftime("%Y-%m-%d %H:%M:%S")
            save_state(state)
            
            print(f"[OK] Reminder ready: {reminder['title']}")
            print(f"  Message written to: {OUTPUT_FILE}")
            return True
        else:
            print(f"[OK] Reminder already sent for {current_time}")
            return False
    else:
        print(f"[OK] No reminder scheduled for {current_time}")
        return False

if __name__ == "__main__":
    check_reminders()
