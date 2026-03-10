#!/usr/bin/env python3
"""
Health Guardian - 个人健康管家
全方位健康管理 · 科学减肥 · 智能提醒 · 个性化建议
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import requests
from typing import Dict, Optional

# ============================================================================
# 配置管理
# ============================================================================

CONFIG_FILE = Path.home() / ".health_guardian_config.json"
DATA_FILE = Path.home() / ".health_guardian_data.json"

DEFAULT_CONFIG = {
    "user": {
        "height_cm": 178,
        "weight_kg": 103,
        "age": 30,
        "gender": "male",
        "goal": "lose_weight",
        "target_weight_kg": 75,
        "activity_level": "low"
    },
    "health": {
        "conditions": ["sleep_apnea"],
        "devices": ["cpap"],
        "allergies": [],
        "medications": []
    },
    "notifications": {
        "wechat_webhook": "",
        "enabled": True,
        "quiet_hours": ["22:00", "07:00"]
    },
    "reminders": {
        "water": {
            "enabled": True,
            "times": ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"],
            "amount_ml": 250
        },
        "meals": {
            "enabled": True,
            "times": ["07:30", "12:00", "18:00"]
        },
        "exercise": {
            "enabled": True,
            "times": ["17:00"],
            "duration_min": 30
        },
        "sleep": {
            "enabled": True,
            "bedtime": "22:30",
            "reminder_time": "21:30"
        }
    },
    "location": {
        "city": "北京",
        "weather_service": "wttr.in"
    }
}

# ============================================================================
# 健康计算
# ============================================================================

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """计算 BMI"""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def get_bmi_category(bmi: float) -> str:
    """BMI 分类"""
    if bmi < 18.5:
        return "偏瘦"
    elif bmi < 24:
        return "正常"
    elif bmi < 28:
        return "偏胖"
    else:
        return "肥胖"

def calculate_daily_water_intake(weight_kg: float, exercise_min: int = 0, temperature_c: int = 25) -> int:
    """
    计算每日建议饮水量
    
    公式：
    - 基础量 = 体重 (kg) × 35
    - 运动追加 = 运动时长 (分钟) × 12
    - 高温追加 = 温度>30°C ? 500 : 0
    """
    base = weight_kg * 35
    exercise_bonus = exercise_min * 12
    heat_bonus = 500 if temperature_c > 30 else 0
    return int(base + exercise_bonus + heat_bonus)

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    计算基础代谢率 (BMR)
    
    Mifflin-St Jeor 公式
    """
    if gender.lower() == "male":
        bmr = 88.36 + (13.4 * weight_kg) + (4.8 * height_cm) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight_kg) + (3.1 * height_cm) - (4.3 * age)
    return bmr

def calculate_tdee(bmr: float, activity_level: str) -> float:
    """
    计算每日总能量消耗 (TDEE)
    """
    activity_multipliers = {
        "sedentary": 1.2,    # 几乎不运动
        "low": 1.375,        # 轻度运动
        "moderate": 1.55,    # 中度运动
        "high": 1.725,       # 高度运动
        "very_high": 1.9     # 极高强度
    }
    return bmr * activity_multipliers.get(activity_level, 1.375)

def calculate_weight_loss_plan(current_kg: float, target_kg: float, weeks: int = 12) -> Dict:
    """
    计算减肥计划
    
    安全减重速度：每周 0.5-1kg
    """
    total_loss = current_kg - target_kg
    weekly_loss = total_loss / weeks
    
    if weekly_loss > 1:
        weeks_adjusted = int(total_loss / 0.75)
        return {
            "status": "adjusted",
            "message": f"建议调整周期为 {weeks_adjusted} 周（每周减重 0.75kg 更健康）",
            "weekly_loss_kg": 0.75,
            "daily_calorie_deficit": 500
        }
    
    return {
        "status": "ok",
        "weekly_loss_kg": weekly_loss,
        "daily_calorie_deficit": int(weekly_loss * 7700 / 7),  # 1kg 脂肪 ≈ 7700 大卡
        "weeks": weeks
    }

# ============================================================================
# 天气集成
# ============================================================================

def get_weather(city: str) -> Optional[Dict]:
    """
    获取天气数据（使用 wttr.in）
    """
    try:
        response = requests.get(f"https://wttr.in/{city}?format=j1", timeout=5)
        data = response.json()
        
        current = data["current_condition"][0]
        return {
            "temperature_c": int(current["temp_C"]),
            "feels_like_c": int(current["FeelsLikeC"]),
            "humidity": int(current["humidity"]),
            "condition": current["weatherDesc"][0]["value"],
            "wind_speed_kmh": int(current["windspeedKmph"]),
            "air_quality": "unknown"  # wttr.in 不提供空气质量
        }
    except Exception as e:
        print(f"⚠️  获取天气失败：{e}")
        return None

# ============================================================================
# 通知系统
# ============================================================================

def send_wechat_notification(webhook_url: str, message: str) -> bool:
    """
    发送企业微信通知
    """
    if not webhook_url:
        print("⚠️  未配置企业微信 webhook")
        return False
    
    try:
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            }
        }
        response = requests.post(webhook_url, json=data, timeout=10)
        result = response.json()
        
        if result.get("errcode") == 0:
            print("✅ 微信通知已发送")
            return True
        else:
            print(f"❌ 微信通知失败：{result}")
            return False
    except Exception as e:
        print(f"❌ 发送通知失败：{e}")
        return False

def send_notification(config: Dict, message: str):
    """
    根据配置发送通知
    """
    if not config["notifications"]["enabled"]:
        return
    
    # 检查安静时间
    quiet_start = config["notifications"]["quiet_hours"][0]
    quiet_end = config["notifications"]["quiet_hours"][1]
    current_hour = datetime.now().hour
    
    # 简单判断（实际应该更精确）
    if quiet_start <= f"{current_hour:02d}:00" <= quiet_end:
        print("⏰ 当前是安静时间，跳过通知")
        return
    
    # 发送微信通知
    webhook = config["notifications"].get("wechat_webhook", "")
    if webhook:
        send_wechat_notification(webhook, message)
    
    # 打印到控制台
    print("\n" + "="*60)
    print(message)
    print("="*60 + "\n")

# ============================================================================
# 提醒生成
# ============================================================================

def generate_water_reminder(config: Dict, weather: Optional[Dict] = None) -> str:
    """生成喝水提醒"""
    user = config["user"]
    daily_water = calculate_daily_water_intake(
        user["weight_kg"],
        temperature_c=weather["temperature_c"] if weather else 25
    )
    
    # 读取已喝水量
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    today_water = data.get("water_log", {}).get(today, 0)
    
    progress = (today_water / daily_water) * 100
    
    message = f"""💧 喝水提醒

⏰ 时间：{datetime.now().strftime("%H:%M")}
📊 今日建议：{daily_water}ml
📈 当前进度：{today_water}ml / {daily_water}ml ({progress:.0f}%)
🎯 本次建议：250ml

{weather_advice(weather) if weather else ""}
"""
    return message

def generate_exercise_reminder(config: Dict, weather: Optional[Dict] = None) -> str:
    """生成运动提醒"""
    user = config["user"]
    
    # 根据天气和体重推荐运动
    if weather:
        if weather["temperature_c"] > 30:
            exercise = "室内游泳或健身房"
            duration = 30
        elif weather["temperature_c"] < 10:
            exercise = "室内瑜伽或力量训练"
            duration = 40
        elif weather["condition"] == "Rain":
            exercise = "室内有氧操"
            duration = 30
        else:
            exercise = "户外快走或慢跑"
            duration = 40
    else:
        exercise = "户外快走"
        duration = 40
    
    # 根据体重调整
    if user["weight_kg"] > 100:
        exercise = "低冲击运动：" + exercise
        note = "⚠️ 体重较大，建议保护膝盖"
    else:
        note = ""
    
    message = f"""🏃 运动时间

⏰ 时间：{datetime.now().strftime("%H:%M")}
📍 推荐：{exercise}
⏱️ 时长：{duration} 分钟
🔥 预计消耗：{duration * 5} 大卡

{note}
{weather_advice(weather) if weather else ""}
"""
    return message

def generate_sleep_reminder(config: Dict) -> str:
    """生成睡前提醒"""
    bedtime = config["reminders"]["sleep"]["bedtime"]
    
    message = f"""😴 睡前准备

⏰ 当前时间：{datetime.now().strftime("%H:%M")}
🛏️ 目标睡眠：{bedtime}
⏳ 剩余准备：30 分钟

✅ 待办事项：
1. 关闭电子设备
2. 准备呼吸机设备
3. 调暗灯光
4. 温水泡脚
5. 冥想放松

💡 健康提示：
- 睡眠呼吸暂停患者请确保呼吸机正常工作
- 保持卧室温度 18-22°C
- 避免睡前 2 小时进食
"""
    return message

def generate_meal_reminder(config: Dict, meal_type: str = "午餐") -> str:
    """生成用餐提醒"""
    user = config["user"]
    
    # 计算每日卡路里需求
    bmr = calculate_bmr(user["weight_kg"], user["height_cm"], user["age"], user["gender"])
    tdee = calculate_tdee(bmr, user["activity_level"])
    
    # 减肥目标
    if user["goal"] == "lose_weight":
        daily_calories = tdee - 500
    else:
        daily_calories = tdee
    
    # 分配每餐
    if meal_type == "早餐":
        calories = int(daily_calories * 0.3)
    elif meal_type == "午餐":
        calories = int(daily_calories * 0.4)
    else:
        calories = int(daily_calories * 0.3)
    
    message = f"""🍽️ {meal_type}提醒

⏰ 时间：{datetime.now().strftime("%H:%M")}
🔥 建议摄入：{calories} 大卡

💡 健康建议：
- 细嚼慢咽，每口咀嚼 20-30 次
- 先吃蔬菜，再吃蛋白质，最后吃主食
- 吃到 7 分饱即可
- 饭后站立或散步 15 分钟

⚠️ 注意事项：
- 避免高糖高油食物
- 控制主食摄入量
- 多喝水，少喝含糖饮料
"""
    return message

def weather_advice(weather: Optional[Dict]) -> str:
    """根据天气给出建议"""
    if not weather:
        return ""
    
    advice = []
    
    if weather["temperature_c"] > 30:
        advice.append("🌡️ 天气炎热，注意防暑降温，增加饮水量")
    elif weather["temperature_c"] < 10:
        advice.append("🥶 天气寒冷，注意保暖，运动前充分热身")
    
    if weather["humidity"] > 80:
        advice.append("💦 湿度较大，体感闷热，注意通风")
    
    if weather["condition"] == "Rain":
        advice.append("🌧️ 下雨天，建议室内活动")
    
    return "\n".join(advice) if advice else ""

# ============================================================================
# 数据管理
# ============================================================================

def load_config() -> Dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict):
    """保存配置"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"✅ 配置已保存：{CONFIG_FILE}")

def load_data() -> Dict:
    """加载数据"""
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"water_log": {}, "weight_log": [], "exercise_log": []}

def save_data(data: Dict):
    """保存数据"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================================
# 命令实现
# ============================================================================

def cmd_init():
    """初始化用户配置"""
    print("🏥 Health Guardian 初始化向导\n")
    
    config = DEFAULT_CONFIG.copy()
    
    # 收集用户信息
    print("请输入您的基本信息：")
    config["user"]["height_cm"] = int(input("身高 (cm): ") or 178)
    config["user"]["weight_kg"] = float(input("体重 (kg): ") or 103)
    config["user"]["age"] = int(input("年龄：") or 30)
    config["user"]["gender"] = input("性别 (male/female): ") or "male"
    config["user"]["goal"] = input("目标 (lose_weight/gain_muscle/maintain): ") or "lose_weight"
    config["user"]["target_weight_kg"] = float(input("目标体重 (kg): ") or 75)
    config["user"]["activity_level"] = input("活动量 (sedentary/low/moderate/high): ") or "low"
    
    # 健康状况
    print("\n健康状况（用逗号分隔，直接回车跳过）：")
    conditions = input("疾病/状况：")
    config["health"]["conditions"] = [c.strip() for c in conditions.split(",")] if conditions else []
    
    devices = input("使用设备（如 cpap）：")
    config["health"]["devices"] = [d.strip() for d in devices.split(",")] if devices else []
    
    # 通知设置
    print("\n通知设置：")
    config["notifications"]["wechat_webhook"] = input("企业微信 webhook URL（直接回车跳过）：") or ""
    config["notifications"]["enabled"] = bool(config["notifications"]["wechat_webhook"])
    
    # 位置
    config["location"]["city"] = input("\n所在城市：") or "北京"
    
    # 保存配置
    save_config(config)
    
    # 显示健康摘要
    print("\n" + "="*60)
    print("📊 健康摘要")
    print("="*60)
    
    bmi = calculate_bmi(config["user"]["weight_kg"], config["user"]["height_cm"])
    print(f"BMI: {bmi:.1f} ({get_bmi_category(bmi)})")
    
    daily_water = calculate_daily_water_intake(config["user"]["weight_kg"])
    print(f"每日建议饮水：{daily_water}ml")
    
    bmr = calculate_bmr(config["user"]["weight_kg"], config["user"]["height_cm"], config["user"]["age"], config["user"]["gender"])
    tdee = calculate_tdee(bmr, config["user"]["activity_level"])
    print(f"基础代谢：{bmr:.0f} 大卡/天")
    print(f"每日消耗：{tdee:.0f} 大卡/天")
    
    if config["user"]["goal"] == "lose_weight":
        plan = calculate_weight_loss_plan(config["user"]["weight_kg"], config["user"]["target_weight_kg"])
        print(f"\n减肥计划：")
        print(f"每周减重：{plan['weekly_loss_kg']:.2f}kg")
        print(f"每日热量缺口：{plan['daily_calorie_deficit']} 大卡")
    
    print("="*60)
    print("\n✅ 初始化完成！")
    print("\n使用示例:")
    print("  python health_guardian.py today          # 查看今日计划")
    print("  python health_guardian.py log-water 250  # 记录喝水")
    print("  python health_guardian.py status         # 查看状态")

def cmd_today():
    """显示今日计划"""
    config = load_config()
    weather = get_weather(config["location"]["city"])
    
    print("="*60)
    print(f"📅 今日健康计划 - {datetime.now().strftime('%Y-%m-%d %A')}")
    print("="*60)
    
    # 天气
    if weather:
        print(f"\n🌤️  {config['location']['city']} 天气")
        print(f"   温度：{weather['temperature_c']}°C (体感 {weather['feels_like_c']}°C)")
        print(f"   状况：{weather['condition']}")
        print(f"   湿度：{weather['humidity']}%")
    
    # 今日目标
    user = config["user"]
    daily_water = calculate_daily_water_intake(
        user["weight_kg"],
        temperature_c=weather["temperature_c"] if weather else 25
    )
    
    print(f"\n🎯 今日目标")
    print(f"   💧 饮水：{daily_water}ml")
    print(f"   🏃 运动：{config['reminders']['exercise']['duration_min']} 分钟")
    print(f"   😴 睡眠：{config['reminders']['sleep']['bedtime']}")
    
    # 提醒时间表
    print(f"\n⏰ 提醒时间")
    if config["reminders"]["water"]["enabled"]:
        print(f"   喝水：{', '.join(config['reminders']['water']['times'])}")
    if config["reminders"]["meals"]["enabled"]:
        print(f"   用餐：{', '.join(config['reminders']['meals']['times'])}")
    if config["reminders"]["exercise"]["enabled"]:
        print(f"   运动：{', '.join(config['reminders']['exercise']['times'])}")
    if config["reminders"]["sleep"]["enabled"]:
        print(f"   睡前：{config['reminders']['sleep']['reminder_time']}")
    
    print("="*60)

def cmd_status():
    """显示健康状态"""
    config = load_config()
    data = load_data()
    user = config["user"]
    
    print("="*60)
    print("📊 健康状态")
    print("="*60)
    
    # BMI
    bmi = calculate_bmi(user["weight_kg"], user["height_cm"])
    category = get_bmi_category(bmi)
    print(f"\n⚖️  体重指数")
    print(f"   BMI: {bmi:.1f} ({category})")
    print(f"   当前：{user['weight_kg']}kg")
    print(f"   目标：{user['target_weight_kg']}kg")
    print(f"   还需：{user['weight_kg'] - user['target_weight_kg']:.1f}kg")
    
    # 今日进度
    today = datetime.now().strftime("%Y-%m-%d")
    daily_water = calculate_daily_water_intake(user["weight_kg"])
    today_water = data.get("water_log", {}).get(today, 0)
    
    print(f"\n💧 今日饮水")
    print(f"   {today_water}ml / {daily_water}ml ({today_water/daily_water*100:.0f}%)")
    
    # 体重记录
    weight_log = data.get("weight_log", [])
    if weight_log:
        recent = weight_log[-5:]
        print(f"\n📈 体重趋势")
        for entry in recent:
            print(f"   {entry['date']}: {entry['weight']}kg")
    
    print("="*60)

def cmd_log_water(amount_ml: int):
    """记录喝水"""
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if "water_log" not in data:
        data["water_log"] = {}
    
    data["water_log"][today] = data["water_log"].get(today, 0) + amount_ml
    save_data(data)
    
    config = load_config()
    daily_water = calculate_daily_water_intake(config["user"]["weight_kg"])
    today_water = data["water_log"][today]
    progress = today_water / daily_water * 100
    
    print(f"✅ 已记录喝水 {amount_ml}ml")
    print(f"📊 今日总计：{today_water}ml / {daily_water}ml ({progress:.0f}%)")

def cmd_log_weight(weight_kg: float):
    """记录体重"""
    data = load_data()
    
    if "weight_log" not in data:
        data["weight_log"] = []
    
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "weight": weight_kg
    }
    data["weight_log"].append(entry)
    
    # 更新配置中的当前体重
    config = load_config()
    config["user"]["weight_kg"] = weight_kg
    save_config(config)
    
    save_data(data)
    
    print(f"✅ 已记录体重 {weight_kg}kg")
    
    # 计算变化
    if len(data["weight_log"]) > 1:
        prev = data["weight_log"][-2]["weight"]
        change = weight_kg - prev
        print(f"📈 较上次：{change:+.2f}kg")

def cmd_remind(reminder_type: str):
    """手动触发提醒"""
    config = load_config()
    weather = get_weather(config["location"]["city"])
    
    if reminder_type == "water":
        message = generate_water_reminder(config, weather)
    elif reminder_type == "exercise":
        message = generate_exercise_reminder(config, weather)
    elif reminder_type == "sleep":
        message = generate_sleep_reminder(config)
    elif reminder_type == "meal":
        message = generate_meal_reminder(config, "午餐")
    else:
        print(f"❌ 未知提醒类型：{reminder_type}")
        return
    
    send_notification(config, message)

def cmd_weekly_report():
    """生成周报"""
    data = load_data()
    config = load_config()
    
    print("="*60)
    print("📊 健康周报")
    print("="*60)
    
    # 本周日期范围
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    print(f"\n📅 周期：{week_start.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')}")
    
    # 体重变化
    weight_log = data.get("weight_log", [])
    if weight_log:
        week_weights = [w for w in weight_log if datetime.strptime(w["date"], "%Y-%m-%d") >= week_start]
        if len(week_weights) >= 2:
            start_weight = week_weights[0]["weight"]
            end_weight = week_weights[-1]["weight"]
            change = end_weight - start_weight
            print(f"\n⚖️  体重变化")
            print(f"   本周：{start_weight:.1f}kg → {end_weight:.1f}kg ({change:+.2f}kg)")
            print(f"   目标：{config['user']['target_weight_kg']}kg (还需 {end_weight - config['user']['target_weight_kg']:.1f}kg)")
    
    # 喝水统计
    water_log = data.get("water_log", {})
    daily_water = calculate_daily_water_intake(config["user"]["weight_kg"])
    week_days = [(week_start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((today - week_start).days + 1)]
    week_water = [water_log.get(day, 0) for day in week_days]
    
    if week_water:
        avg_water = sum(week_water) / len(week_water)
        print(f"\n💧 喝水达标率")
        print(f"   平均每日：{avg_water:.0f}ml / {daily_water}ml ({avg_water/daily_water*100:.0f}%)")
    
    print("="*60)

# ============================================================================
# 主程序
# ============================================================================

def print_help():
    """打印帮助信息"""
    print("""
🏥 Health Guardian - 个人健康管家

用法:
  python health_guardian.py <command> [args]

命令:
  init                  初始化用户配置
  today                 查看今日计划
  status                查看健康状态
  log-water <ml>        记录喝水 (ml)
  log-weight <kg>       记录体重 (kg)
  remind <type>         手动触发提醒 (water/exercise/sleep/meal)
  weekly-report         生成周报
  help                  显示帮助

示例:
  python health_guardian.py init
  python health_guardian.py today
  python health_guardian.py log-water 250
  python health_guardian.py remind water
""")

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1]
    
    if command == "init":
        cmd_init()
    elif command == "today":
        cmd_today()
    elif command == "status":
        cmd_status()
    elif command == "log-water":
        if len(sys.argv) < 3:
            print("❌ 请指定喝水量 (ml)")
            return
        cmd_log_water(int(sys.argv[2]))
    elif command == "log-weight":
        if len(sys.argv) < 3:
            print("❌ 请指定体重 (kg)")
            return
        cmd_log_weight(float(sys.argv[2]))
    elif command == "remind":
        if len(sys.argv) < 3:
            print("❌ 请指定提醒类型 (water/exercise/sleep/meal)")
            return
        cmd_remind(sys.argv[2])
    elif command == "weekly-report":
        cmd_weekly_report()
    elif command == "help":
        print_help()
    else:
        print(f"❌ 未知命令：{command}")
        print_help()

if __name__ == "__main__":
    main()
