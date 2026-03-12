#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Guardian - Anti-Aging Edition (v2.0)
个人健康管理系统（新增抗衰老）
整合抖音视频抗衰老智慧 + 柳叶刀科学研究
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Paths
CONFIG_FILE = Path.home() / ".health_guardian_config.json"
STATE_FILE = Path.home() / ".health_guardian_state.json"

# Reminder schedule with messages (updated with Douyin video wisdom)
REMINDERS = {
    "07:00": {
        "type": "morning_care",
        "title": "🌅 晨间护理时间！",
        "message": "日出而作，顺应自然 🌞\n\n晨间流程：\n1. 温和洁面\n2. 爽肤水→精华→眼霜→面霜\n3. 防晒霜（必须！）\n4. 一杯温水\n\n🍵 清淡饮食，从今天开始！"
    },
    "07:30": {
        "type": "morning",
        "title": "☀️ 早上好！",
        "message": "新的一天开始了！\n\n📅 日期：{date}\n💧 今日饮水目标：{water}ml\n🏃 运动目标：30 分钟\n😴 睡觉时间：22:30\n\n🌟 抗衰老今日重点：\n• 遵循昼夜节律\n• 清茶淡饭\n• 不劳心力\n• 顺应自然\n\n加油，向着 {target}kg 的目标前进！💪"
    },
    "08:00": {
        "type": "water",
        "title": "💧 喝水 + 营养时间！",
        "message": "建议饮用 250ml 温水\n\n🥜 早餐建议（柳叶刀研究）：\n• 全谷物（燕麦、全麦面包）\n• 豆类（豆浆、豆腐）\n• 坚果（核桃、杏仁）\n• 新鲜水果\n\n🍊 补充维生素 C 抗氧化！"
    },
    "10:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "message": "建议饮用 250ml 温水\n\n🍵 可以喝杯绿茶：\n• 茶多酚抗氧化\n• 降低炎症\n• 提神醒脑\n\n清茶淡饭，养生之道！"
    },
    "12:00": {
        "type": "meal",
        "title": "🍽️ 午餐时间！",
        "message": "健康午餐建议（柳叶刀研究）：\n\n✅ 多吃：\n• 豆类制品（豆腐、豆浆）\n• 全谷物（糙米、全麦）\n• 深色蔬菜\n• 坚果\n\n❌ 少吃：\n• 红肉（猪牛羊）\n• 加工肉类（香肠、培根）\n\n清淡饮食，抗炎抗衰老！🥗"
    },
    "14:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "message": "建议饮用 250ml 温水\n\n💡 抗衰老小贴士：\n下午容易疲劳，喝杯绿茶提神，\n同时抗氧化、降低炎症！"
    },
    "16:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "message": "建议饮用 250ml 温水\n\n🥒 健康加餐：\n• 一小把坚果（核桃、杏仁）\n• 新鲜水果\n• 酸奶\n\n补充健康脂肪和蛋白质！"
    },
    "17:00": {
        "type": "exercise",
        "title": "🏃 运动时间到了！",
        "message": "柳叶刀研究：好好运动 🏃\n\n建议运动 30 分钟：\n• 快走或慢跑\n• 跳绳\n• 俯卧撑 + 深蹲\n• 瑜伽或拉伸\n\n💡 关键：动对比多动更重要！\n选择适合自己的强度，持之以恒！"
    },
    "18:00": {
        "type": "meal",
        "title": "🍽️ 晚餐时间！",
        "message": "健康晚餐建议：\n\n✅ 推荐：\n• 豆制品（豆腐、豆浆）\n• 深海鱼（三文鱼、鳕鱼）\n• 大量蔬菜\n• 少量全谷物\n\n❌ 避免：\n• 红肉和加工肉类\n• 油腻食物\n• 过饱（七分就好）\n\n清淡饮食，助眠又抗衰！🥗"
    },
    "20:00": {
        "type": "stretching",
        "title": "🧘 拉伸放松时间！",
        "message": "日入而息，准备休息 🌙\n\n睡前拉伸 10 分钟：\n• 颈部拉伸\n• 肩部放松\n• 背部伸展\n• 腿部拉伸\n\n好处：\n• 缓解肌肉紧张\n• 促进血液循环\n• 帮助入睡\n• 减少压力（不劳心力）"
    },
    "21:00": {
        "type": "night_care",
        "title": "🌙 晚间护理时间！",
        "message": "准备入睡流程 🌙\n\n晚间护肤：\n1. 温和洁面\n2. 爽肤水\n3. 修复精华（视黄醇/肽类）\n4. 眼霜\n5. 晚霜\n\n🌟 夜间是皮肤修复黄金时间！\n\n随后准备睡觉，顺应自然作息！"
    },
    "21:30": {
        "type": "sleep",
        "title": "😴 睡前准备时间！",
        "message": "日入而息，该休息了 🌙\n\n柳叶刀研究：好好睡觉是抗衰老黄金标准！\n\n睡前准备：\n• 关闭电子设备（蓝光影响睡眠）\n• 准备好呼吸机（如有需要）\n• 调暗灯光\n• 冥想或深呼吸\n• 不劳心力，放松心情\n\n😴 22:30 准时入睡，保证 7-8 小时！"
    }
}

def load_config():
    """Load user configuration"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_state():
    """Load reminder state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"lastReminder": None}

def save_state(state):
    """Save reminder state"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def get_current_time():
    """Get current time in HH:MM format"""
    now = datetime.now()
    return f"{now.hour:02d}:{now.minute:02d}"

def check_and_send():
    """Check if there's a reminder to send"""
    current_time = get_current_time()
    today = datetime.now().strftime("%Y-%m-%d %A")
    
    config = load_config()
    state = load_state()
    
    # Get user info for personalization
    user = config.get("user", {})
    target_weight = user.get("target_weight_kg", 90)
    water_goal = user.get("weight_kg", 100) * 35
    
    if current_time in REMINDERS:
        reminder = REMINDERS[current_time]
        reminder_key = f"{today.split(' ')[0]} {current_time}"
        
        # Check if already sent today
        if state.get("lastReminder") != reminder_key:
            # Prepare message
            message = reminder["message"].format(
                date=today,
                water=water_goal,
                target=target_weight
            )
            
            # Output for OpenClaw to capture and send
            output = {
                "type": "health_reminder",
                "time": current_time,
                "title": reminder["title"],
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            
            print(json.dumps(output, ensure_ascii=False, indent=2))
            
            # Update state
            state["lastReminder"] = reminder_key
            state["lastCheck"] = datetime.now().isoformat()
            save_state(state)
            
            return output
        else:
            print(json.dumps({"status": "already_sent", "time": current_time}, ensure_ascii=False))
            return None
    else:
        print(json.dumps({"status": "no_reminder", "time": current_time}, ensure_ascii=False))
        return None

if __name__ == "__main__":
    result = check_and_send()
    sys.exit(0 if result else 1)
