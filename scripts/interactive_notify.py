#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康管理系统 - 交互式个性化通知
每次提醒时询问用户真实数据，确保准确性
"""

import json
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

# 配置文件
USERS_FILE = Path.home() / ".health_users.json"
STATE_FILE = Path.home() / ".health_interactive_state.json"

def load_users():
    """加载用户数据"""
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"version": "1.0", "users": {}}

def save_users(users_data):
    """保存用户数据"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=2)

def load_state():
    """加载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_state(state):
    """保存状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def send_feishu_interactive(title, content, webhook_url, user_id):
    """发送交互式飞书卡片（带输入框）"""
    import time
    
    # 防止发送太频繁，添加延迟
    time.sleep(1)  # 每条消息间隔 1 秒
    
    message = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "content": title,
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": content,
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "content": f"**⏰ 时间：** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "content": "✅ 已完成",
                                "tag": "plain_text"
                            },
                            "type": "primary",
                            "value": {
                                "action": "completed",
                                "user_id": user_id
                            }
                        },
                        {
                            "tag": "button",
                            "text": {
                                "content": "⏰ 稍后提醒",
                                "tag": "plain_text"
                            },
                            "value": {
                                "action": "snooze",
                                "user_id": user_id
                            }
                        }
                    ]
                }
            ]
        }
    }
    
    try:
        response = requests.post(
            webhook_url,
            json=message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                return True
        return False
    except:
        return False

def get_interactive_reminder(user_id, user_data, reminder_type):
    """获取交互式提醒内容"""
    name = user_data.get("name", "朋友")
    profile = user_data.get("profile", {})
    health = user_data.get("health_conditions", {})
    goals = user_data.get("goals", {})
    stats = user_data.get("stats", {})
    
    current_weight = profile.get("weight_kg", 0)
    target_weight = goals.get("target_weight_kg", 90)
    daily_water = goals.get("daily_water_ml", 3605)
    today_water = stats.get("today_water_ml", 0)
    
    # 个性化提醒内容
    reminders = {
        "water": {
            "title": "💧 喝水时间到了！",
            "content": f"{name}，该喝水了！\n\n💡 建议饮用：**250ml** 温水\n\n📊 今日饮水进度：\n• 目标：{daily_water}ml\n• 已喝：{today_water}ml\n\n💬 **请回复：**\n• 喝了多少 ml？\n• 或点击\"已完成\""
        },
        "exercise": {
            "title": "🏃 运动时间！",
            "content": f"{name}，该运动了！\n\n🎯 你的减重目标：\n• 当前：{current_weight}kg\n• 目标：{target_weight}kg\n• 还需减：{current_weight - target_weight}kg\n\n🏃 **建议运动 30 分钟**\n\n💬 **请回复：**\n• 运动了多少分钟？\n• 或点击\"稍后提醒\""
        },
        "meal": {
            "title": "🍽️ 用餐提醒",
            "content": f"{name}，该吃饭了！\n\n🥗 健康饮食建议：\n• 多吃蔬菜和高蛋白\n• 控制碳水摄入\n• 七分饱就好\n\n💬 **请回复：**\n• 吃了什么？（可选）\n• 或点击\"已完成\""
        },
        "sleep": {
            "title": "😴 睡前准备",
            "content": f"{name}，1 小时后该睡觉了 (22:30)\n\n🌙 睡前准备：\n• 关闭电子设备\n• **准备好呼吸机**\n• 调暗灯光\n\n💬 **请回复：**\n• 今天感觉怎么样？\n• 或点击\"已完成\""
        },
        "morning": {
            "title": "☀️ 早安",
            "content": f"早上好，{name}！\n\n📅 {datetime.now().strftime('%Y-%m-%d %A')}\n\n🎯 今日目标：\n• 💧 饮水：{daily_water}ml\n• 🏃 运动：30 分钟\n• 😴 睡觉：22:30\n\n💬 **请回复：**\n• 昨晚睡得好吗？\n• 今天体重是多少？（可选）"
        }
    }
    
    reminder = reminders.get(reminder_type, reminders["water"])
    return reminder["title"], reminder["content"]

def check_and_notify_interactive():
    """检查并发送交互式通知"""
    now = datetime.now()
    current_time = f"{now.hour:02d}:{now.minute:02d}"
    today = now.strftime("%Y-%m-%d")
    
    users_data = load_users()
    state = load_state()
    
    # 提醒时间表
    reminders = {
        "07:30": {"type": "morning", "title": "早安"},
        "08:00": {"type": "water", "title": "喝水"},
        "10:00": {"type": "water", "title": "喝水"},
        "12:00": {"type": "meal", "title": "午餐"},
        "14:00": {"type": "water", "title": "喝水"},
        "16:00": {"type": "water", "title": "喝水"},
        "17:00": {"type": "exercise", "title": "运动"},
        "18:00": {"type": "meal", "title": "晚餐"},
        "20:00": {"type": "water", "title": "喝水"},
        "21:30": {"type": "sleep", "title": "睡前准备"},
        "22:30": {"type": "sleep", "title": "入睡"}
    }
    
    if current_time not in reminders:
        print(f"⏰ {current_time} 没有预设提醒")
        return False
    
    reminder = reminders[current_time]
    sent_count = 0
    
    # 为每个用户发送交互式通知
    for user_id, user_data in users_data.get("users", {}).items():
        webhook = user_data.get("feishu_webhook", "")
        if not webhook:
            continue
        
        reminder_key = f"{today}_{user_id}_{current_time}"
        if state.get("lastNotify", {}).get(reminder_key):
            print(f"✅ {user_data.get('name', '用户')} 已发送过")
            continue
        
        # 获取交互式内容
        title, content = get_interactive_reminder(user_id, user_data, reminder["type"])
        
        # 发送
        if send_feishu_interactive(title, content, webhook, user_id):
            print(f"✅ {user_data.get('name', '用户')} - {title}")
            state.setdefault("lastNotify", {})[reminder_key] = True
            sent_count += 1
        else:
            print(f"❌ {user_data.get('name', '用户')} 发送失败")
    
    save_state(state)
    print(f"\n总计发送：{sent_count}/{len(users_data.get('users', {}))} 人")
    return sent_count > 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "now":
            print(f"🏥 交互式健康通知")
            print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            check_and_notify_interactive()
        elif sys.argv[1] == "test":
            print("🧪 发送测试消息...")
            users_data = load_users()
            success_count = 0
            fail_count = 0
            for user_id, user_data in users_data.get("users", {}).items():
                webhook = user_data.get("feishu_webhook", "")
                if webhook:
                    if send_feishu_interactive(
                        "✅ 交互式通知测试",
                        f"{user_data.get('name', '朋友')}，这是测试消息！\n\n💬 **请回复：**\n• 你收到通知了吗？\n• 或点击下方按钮",
                        webhook,
                        user_id
                    ):
                        success_count += 1
                    else:
                        fail_count += 1
            print(f"✅ 测试完成 - 成功：{success_count}，失败：{fail_count}")
            if fail_count > 0:
                print("⚠️ 部分发送失败，可能是频率限制，请稍后再试")
    else:
        check_and_notify_interactive()
