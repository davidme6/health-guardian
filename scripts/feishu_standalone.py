#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康管理系统 - 飞书独立窗口通知
通过飞书机器人发送通知到独立会话
"""

import json
import os
import sys
import requests
from datetime import datetime
from pathlib import Path

# 配置文件
CONFIG_FILE = Path.home() / ".health_guardian_config.json"
STATE_FILE = Path.home() / ".health_guardian_feishu_state.json"

# 飞书 webhook（从配置文件读取）
FEISHU_WEBHOOK = ""

def load_config():
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    """保存配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

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

def send_feishu_card(title, content, webhook_url=None):
    """
    发送飞书卡片消息（独立窗口效果）
    
    飞书会在会话中显示一个独立的卡片，非常醒目！
    """
    if not webhook_url:
        config = load_config()
        webhook_url = config.get("notifications", {}).get("feishu_webhook", "")
    
    if not webhook_url:
        print("❌ 飞书 webhook 未配置")
        print("\n请配置飞书 webhook：")
        print("1. 打开飞书")
        print("2. 创建群聊（可以只拉自己）")
        print("3. 群设置 → 群机器人 → 添加机器人")
        print("4. 复制 webhook URL")
        print("5. 告诉我 webhook URL，我帮你配置")
        return False
    
    # 飞书卡片消息格式（更美观、更醒目）
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
                            "url": "",
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
                print(f"✅ 飞书卡片通知发送成功")
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
    """发送普通文本消息"""
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
    
    # 完整提醒时间表
    reminders = {
        "07:00": {
            "title": "🧴 晨间护肤时间",
            "icon": "blue",
            "content": f"**【{today}】**\n\n晨间护肤步骤：\n• 温和洁面\n• 爽肤水→精华→眼霜→面霜\n• **防晒霜（必须！）**\n\n☀️ 新的一天开始了！"
        },
        "07:30": {
            "title": "☀️ 早安提醒",
            "icon": "green",
            "content": f"**【{today}】**\n\n早上好！今日健康目标：\n• 💧 饮水：3605ml\n• 🏃 运动：30 分钟\n• 😴 睡觉：22:30\n\n加油！💪"
        },
        "08:00": {
            "title": "💧 喝水 + 维 C 时间",
            "icon": "blue",
            "content": f"**【{today}】**\n\n建议饮用 **250ml** 温水\n\n🍊 建议补充维生素 C（抗氧化）\n可以通过橙子、猕猴桃或补充剂获取！"
        },
        "10:00": {
            "title": "💧 喝水时间",
            "icon": "blue",
            "content": f"**【{today}】**\n\n建议饮用 **250ml** 温水\n\n💡 保持水分充足可以让皮肤更有弹性！"
        },
        "12:00": {
            "title": "🍽️ 午餐 + 维 E 时间",
            "icon": "orange",
            "content": f"**【{today}】**\n\n健康午餐建议：\n• 多吃深色蔬菜（抗氧化）\n• 适量优质蛋白（鱼肉、鸡肉）\n• 补充维生素 E（坚果、橄榄油）\n• 控制碳水摄入\n\n🥗 每一餐都是减肥的机会！"
        },
        "14:00": {
            "title": "💧 喝水 + 绿茶时间",
            "icon": "blue",
            "content": f"**【{today}】**\n\n建议饮用 **250ml** 温水\n\n🍵 下午可以喝绿茶：\n• 富含茶多酚\n• 抗氧化、抗衰老\n• 提神醒脑"
        },
        "16:00": {
            "title": "💧 喝水 + 加餐时间",
            "icon": "blue",
            "content": f"**【{today}】**\n\n建议饮用 **250ml** 温水\n\n🥒 健康加餐建议：\n• 一小把坚果\n• 新鲜水果\n• 酸奶"
        },
        "17:00": {
            "title": "🏃 运动时间",
            "icon": "red",
            "content": f"**【{today}】**\n\n建议运动 **30 分钟**：\n\n🏃 有氧运动：\n• 快走或慢跑\n• 跳绳\n\n💪 力量训练：\n• 俯卧撑\n• 深蹲\n• 平板支撑\n\n运动可以促进新陈代谢，延缓衰老！"
        },
        "18:00": {
            "title": "🍽️ 晚餐 + Omega-3 时间",
            "icon": "orange",
            "content": f"**【{today}】**\n\n健康晚餐建议：\n• 清淡为主\n• 深海鱼（三文鱼、鳕鱼）补充 Omega-3\n• 多吃蔬菜\n• 少吃主食\n\n🐟 Omega-3 好处：抗炎、抗衰老、保护心血管"
        },
        "20:00": {
            "title": "🧘 拉伸放松时间",
            "icon": "purple",
            "content": f"**【{today}】**\n\n睡前拉伸 **10 分钟**：\n• 颈部拉伸\n• 肩部放松\n• 背部伸展\n• 腿部拉伸\n\n🌙 好处：缓解肌肉紧张、促进血液循环、帮助入睡"
        },
        "21:00": {
            "title": "🌙 晚间护肤时间",
            "icon": "blue",
            "content": f"**【{today}】**\n\n晚间护肤步骤：\n1. 卸妆（如有）\n2. 温和洁面\n3. 爽肤水\n4. 精华液（视黄醇/肽类）\n5. 眼霜\n6. 晚霜/面霜\n\n🌟 夜间是皮肤修复黄金时间！"
        },
        "21:30": {
            "title": "😴 睡前准备时间",
            "icon": "grey",
            "content": f"**【{today}】**\n\n**1 小时后该睡觉了 (22:30)**\n\n睡前准备清单：\n• 关闭电子设备（蓝光影响睡眠）\n• 准备好呼吸机\n• 调暗房间灯光\n• 可以泡个热水脚\n• 冥想或深呼吸放松\n\n💤 好的睡眠是最好的抗衰老！"
        },
        "22:30": {
            "title": "💤 入睡时间",
            "icon": "grey",
            "content": f"**【{today}】**\n\n该睡觉了！\n\n保证 **7-8 小时** 睡眠\n\n🌙 晚安，好梦！"
        }
    }
    
    if current_time in reminders:
        return reminders[current_time]
    return None

def check_and_send():
    """检查并发送飞书通知"""
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
    
    # 发送飞书卡片通知
    config = load_config()
    webhook_url = config.get("notifications", {}).get("feishu_webhook", "")
    
    if not webhook_url:
        print("⚠️ 飞书 webhook 未配置")
        print("\n📱 配置步骤：")
        print("1. 打开飞书")
        print("2. 创建一个群（可以只拉自己一个人）")
        print("3. 群名称：健康管理通知")
        print("4. 群设置 → 群机器人 → 添加机器人")
        print("5. 选择「自定义机器人」")
        print("6. 名称：健康管家")
        print("7. 复制 webhook URL")
        print("8. 告诉我 webhook URL，我帮你配置")
        return False
    
    # 设置卡片颜色
    header_template = reminder.get("icon", "blue")
    
    success = send_feishu_card(
        f"{reminder['icon'].split(' ')[0]} {reminder['title']}",
        reminder['content'],
        webhook_url
    )
    
    if success:
        # 保存状态
        state["lastNotify"] = reminder_key
        state["lastNotifyTime"] = datetime.now().isoformat()
        save_state(state)
        print(f"✅ 飞书通知已发送：{reminder['title']}")
    
    return success

def test_send(webhook_url):
    """测试发送"""
    print("🧪 发送测试消息...")
    success = send_feishu_card(
        "✅ 健康管理系统测试",
        "**【测试消息】**\n\n如果你收到这条消息，说明飞书通知配置成功！\n\n从现在开始，我会在指定时间通过飞书发送健康提醒到你这个独立的会话窗口。",
        webhook_url
    )
    return success

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test" and len(sys.argv) > 2:
            # 测试模式
            webhook = sys.argv[2]
            success = test_send(webhook)
            
            # 保存到配置
            if success:
                config = load_config()
                if "notifications" not in config:
                    config["notifications"] = {}
                config["notifications"]["feishu_webhook"] = webhook
                save_config(config)
                print(f"✅ Webhook 已保存到配置")
            
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "now":
            # 立即发送
            print("⏰ 检查当前提醒...")
            success = check_and_send()
            sys.exit(0 if success else 1)
    else:
        # 默认模式
        print(f"🏥 健康管理系统 - 飞书独立通知")
        print(f"检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        success = check_and_send()
        sys.exit(0 if success else 1)
