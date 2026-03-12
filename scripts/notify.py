#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Health Guardian - Anti-Aging Edition
个人健康管理系统（新增抗衰老）
全方位健康管理 · 科学减肥 · 智能提醒 · 抗衰老优化
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Paths
CONFIG_FILE = Path.home() / ".health_guardian_config.json"
STATE_FILE = Path.home() / ".health_guardian_state.json"

# Reminder schedule with messages (including anti-aging)
REMINDERS = {
    "07:00": {
        "type": "skin_care",
        "title": "🧴 晨间护肤时间！",
        "message": "晨间护肤步骤：\n\n1. 温和洁面\n2. 爽肤水\n3. 精华液（维 C 抗氧化）\n4. 眼霜\n5. 保湿霜\n6. 防晒霜（重要！）\n\n防晒是抗衰老的第一步！☀️"
    },
    "07:30": {
        "type": "morning",
        "title": "☀️ 早上好！",
        "message": "新的一天开始了！\n\n📅 日期：{date}\n💧 今日饮水目标：{water}ml\n🏃 运动目标：30 分钟\n😴 睡觉时间：22:30\n\n🌟 抗衰老今日重点：\n• 补充维 C 抗氧化\n• 防晒保护皮肤\n• 充足饮水保持弹性\n\n加油，向着 {target}kg 的目标前进！💪"
    },
    "08:00": {
        "type": "water",
        "title": "💧 喝水 + 维 C 时间！",
        "message": "建议饮用 250ml 温水\n\n🍊 建议补充维生素 C：\n• 抗氧化、抗衰老\n• 促进胶原蛋白合成\n• 增强免疫力\n\n可以通过橙子、猕猴桃或补充剂获取！"
    },
    "10:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "message": "建议饮用 250ml 温水\n\n💡 抗衰老小贴士：\n保持水分充足可以让皮肤更有弹性，减少细纹产生！"
    },
    "12:00": {
        "type": "meal",
        "title": "🍽️ 午餐时间 + 维 E！",
        "message": "健康午餐建议：\n\n• 多吃深色蔬菜（抗氧化）\n• 适量优质蛋白（鱼肉、鸡肉）\n• 补充维生素 E（坚果、橄榄油）\n• 控制碳水摄入\n\n🥗 抗衰老食物推荐：\n• 蓝莓、番茄（抗氧化）\n• 深海鱼（Omega-3）\n• 坚果（维生素 E）"
    },
    "14:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "message": "建议饮用 250ml 温水\n\n🍵 下午可以喝绿茶：\n• 富含茶多酚\n• 抗氧化、抗衰老\n• 提神醒脑"
    },
    "16:00": {
        "type": "water",
        "title": "💧 喝水时间到了！",
        "message": "建议饮用 250ml 温水\n\n🥒 抗衰老加餐建议：\n• 一小把坚果\n• 新鲜水果\n• 酸奶"
    },
    "17:00": {
        "type": "exercise",
        "title": "🏃 运动时间到了！",
        "message": "建议运动 30 分钟：\n\n🏃 有氧运动（燃脂）：\n• 快走或慢跑\n• 跳绳\n\n💪 力量训练（增肌抗衰老）：\n• 俯卧撑\n• 深蹲\n• 平板支撑\n\n运动可以促进新陈代谢，延缓衰老！"
    },
    "18:00": {
        "type": "meal",
        "title": "🍽️ 晚餐 + Omega-3 时间！",
        "message": "健康晚餐建议：\n\n• 清淡为主\n• 深海鱼（三文鱼、鳕鱼）补充 Omega-3\n• 多吃蔬菜\n• 少吃主食\n\n🐟 Omega-3 好处：\n• 抗炎、抗衰老\n• 保护心血管\n• 改善皮肤健康"
    },
    "20:00": {
        "type": "stretching",
        "title": "🧘 拉伸放松时间！",
        "message": "睡前拉伸 10 分钟：\n\n• 颈部拉伸\n• 肩部放松\n• 背部伸展\n• 腿部拉伸\n\n🌙 好处：\n• 缓解肌肉紧张\n• 促进血液循环\n• 帮助入睡\n• 减少皱纹产生"
    },
    "20:00_water": {
        "type": "water",
        "title": "💧 最后一次喝水！",
        "message": "建议饮用 200ml 温水\n\n⚠️ 睡前少喝水，避免夜尿影响睡眠质量！"
    },
    "21:00": {
        "type": "night_skin_care",
        "title": "🌙 晚间护肤时间！",
        "message": "晚间护肤步骤：\n\n1. 卸妆（如有）\n2. 温和洁面\n3. 爽肤水\n4. 精华液（视黄醇/肽类）\n5. 眼霜\n6. 晚霜/面霜\n\n🌟 夜间是皮肤修复黄金时间！"
    },
    "21:30": {
        "type": "sleep",
        "title": "😴 睡前准备时间！",
        "message": "1 小时后该睡觉了 (22:30)\n\n🌙 睡前准备清单：\n• 关闭电子设备（蓝光影响睡眠）\n• 准备好呼吸机\n• 调暗房间灯光\n• 可以泡个热水脚\n• 冥想或深呼吸放松\n\n💤 好的睡眠是最好的抗衰老！"
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
