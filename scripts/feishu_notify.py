#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康管理系统 - 飞书独立通知服务
直接通过飞书 webhook 发送通知，不依赖 OpenClaw
"""

import json
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

# 配置文件
CONFIG_FILE = Path.home() / ".health_guardian_config.json"
STATE_FILE = Path.home() / ".health_guardian_notify_state.json"

# 飞书 webhook URL（请替换为你的）
FEISHU_WEBHOOK = ""  # 从配置文件读取

def load_config():
    """加载配置文件"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def load_state():
    """加载状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"lastNotify": None}

def save_state(state):
    """保存状态"""
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def send_feishu_notification(title, content, webhook_url=None):
    """
    发送飞书通知
    
    Args:
        title: 消息标题
        content: 消息内容
        webhook_url: 飞书 webhook URL（可选，默认从配置读取）
    """
    if not webhook_url:
        config = load_config()
        webhook_url = config.get("notifications", {}).get("feishu_webhook", "")
    
    if not webhook_url:
        print("❌ 飞书 webhook URL 未配置")
        return False
    
    # 飞书消息格式
    message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": content
                            }
                        ]
                    ]
                }
            }
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
                print(f"✅ 飞书通知发送成功：{title}")
                return True
            else:
                print(f"❌ 飞书通知发送失败：{result}")
                return False
        else:
            print(f"❌ HTTP 错误：{response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 发送失败：{str(e)}")
        return False

def send_text_message(text, webhook_url=None):
    """发送纯文本消息"""
    if not webhook_url:
        config = load_config()
        webhook_url = config.get("notifications", {}).get("feishu_webhook", "")
    
    if not webhook_url:
        return False
    
    message = {
        "msg_type": "text",
        "content": {
            "text": text
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
            print("✅ 消息发送成功")
            return True
        else:
            print(f"❌ HTTP 错误：{response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 发送失败：{str(e)}")
        return False

def get_current_reminder():
    """获取当前时间的提醒"""
    now = datetime.now()
    current_time = f"{now.hour:02d}:{now.minute:02d}"
    today = now.strftime("%Y-%m-%d %A")
    
    # 提醒时间表
    reminders = {
        "07:00": {
            "title": "🧴 晨间护肤时间",
            "content": f"【{today}】\n\n晨间护肤步骤：\n1. 温和洁面\n2. 爽肤水→精华→眼霜→面霜\n3. 防晒霜（必须！）\n\n☀️ 新的一天开始了！"
        },
        "07:30": {
            "title": "☀️ 早安提醒",
            "content": f"【{today}】\n\n早上好！今日健康目标：\n• 💧 饮水：3605ml\n• 🏃 运动：30 分钟\n• 😴 睡觉：22:30\n\n加油！"
        },
        "08:00": {
            "title": "💧 喝水 + 维 C 时间",
            "content": f"【{today}】\n\n建议饮用 250ml 温水\n\n🍊 建议补充维生素 C（抗氧化）\n可以通过橙子、猕猴桃或补充剂获取！"
        },
        "10:00": {
            "title": "💧 喝水时间",
            "content": f"【{today}】\n\n建议饮用 250ml 温水\n\n💡 保持水分充足可以让皮肤更有弹性！"
        },
        "12:00": {
            "title": "🍽️ 午餐 + 维 E 时间",
            "content": f"【{today}】\n\n健康午餐建议：\n• 多吃深色蔬菜（抗氧化）\n• 适量优质蛋白（鱼肉、鸡肉）\n• 补充维生素 E（坚果、橄榄油）\n• 控制碳水摄入\n\n🥗 每一餐都是减肥的机会！"
        },
        "14:00": {
            "title": "💧 喝水 + 绿茶时间",
            "content": f"【{today}】\n\n建议饮用 250ml 温水\n\n🍵 下午可以喝绿茶：\n• 富含茶多酚\n• 抗氧化、抗衰老\n• 提神醒脑"
        },
        "16:00": {
            "title": "💧 喝水 + 加餐时间",
            "content": f"【{today}】\n\n建议饮用 250ml 温水\n\n🥒 健康加餐建议：\n• 一小把坚果\n• 新鲜水果\n• 酸奶"
        },
        "17:00": {
            "title": "🏃 运动时间",
            "content": f"【{today}】\n\n建议运动 30 分钟：\n\n🏃 有氧运动：\n• 快走或慢跑\n• 跳绳\n\n💪 力量训练：\n• 俯卧撑\n• 深蹲\n• 平板支撑\n\n运动可以促进新陈代谢，延缓衰老！"
        },
        "18:00": {
            "title": "🍽️ 晚餐 + Omega-3 时间",
            "content": f"【{today}】\n\n健康晚餐建议：\n• 清淡为主\n• 深海鱼（三文鱼、鳕鱼）补充 Omega-3\n• 多吃蔬菜\n• 少吃主食\n\n🐟 Omega-3 好处：抗炎、抗衰老、保护心血管"
        },
        "20:00": {
            "title": "🧘 拉伸放松时间",
            "content": f"【{today}】\n\n睡前拉伸 10 分钟：\n• 颈部拉伸\n• 肩部放松\n• 背部伸展\n• 腿部拉伸\n\n🌙 好处：缓解肌肉紧张、促进血液循环、帮助入睡"
        },
        "21:00": {
            "title": "🌙 晚间护肤时间",
            "content": f"【{today}】\n\n晚间护肤步骤：\n1. 卸妆（如有）\n2. 温和洁面\n3. 爽肤水\n4. 精华液（视黄醇/肽类）\n5. 眼霜\n6. 晚霜/面霜\n\n🌟 夜间是皮肤修复黄金时间！"
        },
        "21:30": {
            "title": "😴 睡前准备时间",
            "content": f"【{today}】\n\n1 小时后该睡觉了 (22:30)\n\n睡前准备清单：\n• 关闭电子设备（蓝光影响睡眠）\n• 准备好呼吸机\n• 调暗房间灯光\n• 可以泡个热水脚\n• 冥想或深呼吸放松\n\n💤 好的睡眠是最好的抗衰老！"
        },
        "22:30": {
            "title": "💤 入睡时间",
            "content": f"【{today}】\n\n该睡觉了！\n\n保证 7-8 小时睡眠\n\n🌙 晚安，好梦！"
        }
    }
    
    if current_time in reminders:
        return reminders[current_time]
    return None

def check_and_send():
    """检查并发送通知"""
    reminder = get_current_reminder()
    
    if not reminder:
        print(f"⏰ {datetime.now().strftime('%H:%M')} 没有预设提醒")
        return False
    
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    reminder_key = f"{today} {datetime.now().strftime('%H:%M')}"
    
    # 检查是否已发送
    if state.get("lastNotify") == reminder_key:
        print(f"✅ 提醒已发送过：{reminder['title']}")
        return False
    
    # 发送飞书通知
    config = load_config()
    webhook_url = config.get("notifications", {}).get("feishu_webhook", "")
    
    if not webhook_url:
        print("⚠️ 飞书 webhook 未配置，输出消息到控制台：")
        print(f"\n{reminder['title']}\n{reminder['content']}\n")
        return False
    
    success = send_feishu_notification(reminder['title'], reminder['content'], webhook_url)
    
    if success:
        # 保存状态
        state["lastNotify"] = reminder_key
        state["lastNotifyTime"] = datetime.now().isoformat()
        save_state(state)
    
    return success

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            # 测试模式
            print("🧪 发送测试消息...")
            success = send_text_message("【健康管理系统测试】\n\n如果你收到这条消息，说明飞书通知配置成功！✅", None)
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "now":
            # 立即发送当前提醒
            print("⏰ 检查当前提醒...")
            success = check_and_send()
            sys.exit(0 if success else 1)
    else:
        # 默认模式：检查并发送
        print(f"🏥 健康管理系统 - 飞书通知")
        print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        success = check_and_send()
        sys.exit(0 if success else 1)
