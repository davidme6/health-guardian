#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康管理系统 - 多用户个性化飞书通知
支持多个用户，根据每个人的健康数据发送专属通知
"""

import json
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

# 配置文件
USERS_FILE = Path.home() / ".health_users.json"
STATE_FILE = Path.home() / ".health_multi_user_state.json"

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
    return {"lastNotify": {}}

def save_state(state):
    """保存状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def send_feishu_card(title, content, webhook_url):
    """发送飞书卡片消息"""
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
                                "content": "✅ 已收到",
                                "tag": "plain_text"
                            },
                            "type": "primary"
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

def get_personalized_reminder(user_id, user_data, reminder_type):
    """获取个性化提醒内容"""
    name = user_data.get("name", "朋友")
    profile = user_data.get("profile", {})
    health = user_data.get("health_conditions", {})
    goals = user_data.get("goals", {})
    stats = user_data.get("stats", {})
    templates = load_users().get("notification_templates", {})
    
    # 计算数据
    current_weight = profile.get("weight_kg", 0)
    target_weight = goals.get("daily_water_ml", 90)
    daily_water = goals.get("daily_water_ml", 3605)
    today_water = stats.get("today_water_ml", 0)
    water_percentage = int((today_water / daily_water) * 100) if daily_water > 0 else 0
    
    # 获取模板
    template = templates.get(reminder_type, {})
    title = template.get("title", "健康提醒")
    content = template.get("content", "")
    
    # 替换个性化变量
    content = content.replace("{name}", name)
    content = content.replace("{date}", datetime.now().strftime("%Y-%m-%d %A"))
    content = content.replace("{daily_water}", str(daily_water))
    content = content.replace("{today_water}", str(today_water))
    content = content.replace("{percentage}", str(water_percentage))
    content = content.replace("{current_weight}", str(current_weight))
    content = content.replace("{target_weight}", str(target_weight))
    
    # 特殊提醒（根据健康状况）
    if reminder_type == "sleep" and health.get("sleep_apnea"):
        content += "\n\n⚠️ **重要：** 记得使用呼吸机！"
    
    return title, content

def check_and_notify_all():
    """检查并为所有用户发送通知"""
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
    
    # 为每个用户发送通知
    for user_id, user_data in users_data.get("users", {}).items():
        webhook = user_data.get("feishu_webhook", "")
        if not webhook:
            continue
        
        reminder_key = f"{today}_{user_id}_{current_time}"
        if state.get("lastNotify", {}).get(reminder_key):
            print(f"✅ {user_data.get('name', '用户')} 已发送过")
            continue
        
        # 获取个性化内容
        title, content = get_personalized_reminder(user_id, user_data, reminder["type"])
        
        # 发送
        if send_feishu_card(title, content, webhook):
            print(f"✅ {user_data.get('name', '用户')} - {title}")
            state.setdefault("lastNotify", {})[reminder_key] = True
            sent_count += 1
        else:
            print(f"❌ {user_data.get('name', '用户')} 发送失败")
    
    save_state(state)
    print(f"\n总计发送：{sent_count}/{len(users_data.get('users', {}))} 人")
    return sent_count > 0

def add_user(name, feishu_webhook, profile=None):
    """添加新用户"""
    users_data = load_users()
    
    # 生成用户 ID（实际应该用飞书用户 ID）
    import uuid
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    
    user_data = {
        "user_id": user_id,
        "name": name,
        "feishu_webhook": feishu_webhook,
        "profile": profile or {},
        "health_conditions": {},
        "goals": {},
        "preferences": {},
        "stats": {}
    }
    
    users_data.setdefault("users", {})[user_id] = user_data
    save_users(users_data)
    
    print(f"✅ 已添加用户：{name} (ID: {user_id})")
    return user_id

def update_user_profile(user_id, profile_data):
    """更新用户健康档案"""
    users_data = load_users()
    
    if user_id in users_data.get("users", {}):
        users_data["users"][user_id].setdefault("profile", {}).update(profile_data)
        save_users(users_data)
        print(f"✅ 已更新用户 {user_id} 的健康档案")
        return True
    else:
        print(f"❌ 用户 {user_id} 不存在")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "now":
            # 立即检查并发送
            print(f"🏥 健康管理系统 - 多用户通知")
            print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            check_and_notify_all()
        elif sys.argv[1] == "add" and len(sys.argv) > 3:
            # 添加新用户
            name = sys.argv[2]
            webhook = sys.argv[3]
            add_user(name, webhook)
        elif sys.argv[1] == "test":
            # 测试所有用户
            print("🧪 发送测试消息给所有用户...")
            users_data = load_users()
            for user_id, user_data in users_data.get("users", {}).items():
                webhook = user_data.get("feishu_webhook", "")
                if webhook:
                    send_feishu_card(
                        "✅ 健康管理系统测试",
                        f"**【测试消息】**\n\n{user_data.get('name', '朋友')}，如果你收到这条消息，说明个性化通知配置成功！",
                        webhook
                    )
            print("✅ 测试完成")
    else:
        # 默认模式
        check_and_notify_all()
