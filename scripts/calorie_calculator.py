#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热量计算器 - 科学计算每日热量需求
基于 Mifflin-St Jeor 公式和 WHO 标准
"""

import json
from datetime import datetime
from pathlib import Path

# 配置文件
USERS_FILE = Path.home() / ".health_users.json"

def calculate_bmr(weight_kg, height_cm, age, gender):
    """
    计算基础代谢率 (BMR)
    使用 Mifflin-St Jeor 公式（最准确）
    """
    if gender == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:  # female
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
    
    return int(bmr)

def calculate_tdee(bmr, activity_level):
    """
    计算每日总能量消耗 (TDEE)
    基于活动水平
    """
    activity_multipliers = {
        "sedentary": 1.2,      # 久坐，几乎不运动
        "low": 1.375,          # 轻度活动（每周 1-3 天运动）
        "moderate": 1.55,      # 中度活动（每周 3-5 天运动）
        "high": 1.725,         # 高度活动（每周 6-7 天运动）
        "very_high": 1.9       # 极高活动（体力劳动或专业训练）
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.375)
    return int(bmr * multiplier)

def calculate_calorie_goal(tdee, goal, current_weight, target_weight):
    """
    计算每日热量目标
    基于减肥/增肌目标
    """
    if goal == "lose_weight":
        # 减肥：每日热量缺口 500-750 大卡
        # 安全减重速度：每周 0.5-1kg
        deficit = 500 if (current_weight - target_weight) > 20 else 750
        return max(tdee - deficit, 1200)  # 不低于 1200 大卡（安全底线）
    
    elif goal == "gain_muscle":
        # 增肌：每日热量盈余 250-500 大卡
        surplus = 250
        return tdee + surplus
    
    else:  # maintain
        return tdee

def calculate_macros(calorie_goal, goal):
    """
    计算三大营养素比例
    碳水化合物、蛋白质、脂肪
    """
    if goal == "lose_weight":
        # 减肥：高蛋白、中低碳水、低脂
        protein_ratio = 0.35    # 35%
        carb_ratio = 0.35       # 35%
        fat_ratio = 0.30        # 30%
    elif goal == "gain_muscle":
        # 增肌：高蛋白、高碳水、中脂
        protein_ratio = 0.30
        carb_ratio = 0.45
        fat_ratio = 0.25
    else:
        # 维持：均衡
        protein_ratio = 0.25
        carb_ratio = 0.50
        fat_ratio = 0.25
    
    # 1g 蛋白质 = 4 大卡
    # 1g 碳水 = 4 大卡
    # 1g 脂肪 = 9 大卡
    
    protein_g = int((calorie_goal * protein_ratio) / 4)
    carb_g = int((calorie_goal * carb_ratio) / 4)
    fat_g = int((calorie_goal * fat_ratio) / 9)
    
    return {
        "protein_g": protein_g,
        "carb_g": carb_g,
        "fat_g": fat_g,
        "protein_cal": protein_g * 4,
        "carb_cal": carb_g * 4,
        "fat_cal": fat_g * 9
    }

def calculate_bmi(weight_kg, height_cm):
    """计算 BMI"""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    if bmi < 18.5:
        category = "偏瘦"
    elif bmi < 24:
        category = "正常"
    elif bmi < 28:
        category = "偏胖"
    else:
        category = "肥胖"
    
    return round(bmi, 1), category

def generate_meal_plan(calorie_goal, macros, goal):
    """
    生成一日三餐建议
    """
    if goal == "lose_weight":
        breakfast_cal = int(calorie_goal * 0.30)   # 30%
        lunch_cal = int(calorie_goal * 0.40)       # 40%
        dinner_cal = int(calorie_goal * 0.30)      # 30%
        
        breakfast = "高蛋白早餐（鸡蛋、牛奶、全麦面包）"
        lunch = "均衡午餐（瘦肉 + 蔬菜 + 少量主食）"
        dinner = "清淡晚餐（鱼/豆腐 + 大量蔬菜）"
    else:
        breakfast_cal = int(calorie_goal * 0.25)
        lunch_cal = int(calorie_goal * 0.35)
        dinner_cal = int(calorie_goal * 0.40)
        
        breakfast = "营养早餐"
        lunch = "丰盛午餐"
        dinner = "高蛋白晚餐"
    
    return {
        "breakfast": {
            "calories": breakfast_cal,
            "suggestion": breakfast
        },
        "lunch": {
            "calories": lunch_cal,
            "suggestion": lunch
        },
        "dinner": {
            "calories": dinner_cal,
            "suggestion": dinner
        }
    }

def analyze_food(food_name):
    """
    分析常见食物热量
    """
    food_database = {
        # 快餐
        "汉堡": {"calories": 250, "unit": "个", "protein": 12, "carb": 30, "fat": 10},
        "薯条": {"calories": 312, "unit": "小份", "protein": 3, "carb": 41, "fat": 15},
        "无糖可乐": {"calories": 0, "unit": "罐", "protein": 0, "carb": 0, "fat": 0},
        
        # 水果
        "耙耙柑": {"calories": 45, "unit": "个", "protein": 1, "carb": 11, "fat": 0},
        "苹果": {"calories": 52, "unit": "个", "protein": 0, "carb": 14, "fat": 0},
        "香蕉": {"calories": 89, "unit": "根", "protein": 1, "carb": 23, "fat": 0},
        
        # 主食
        "米饭": {"calories": 130, "unit": "碗", "protein": 3, "carb": 28, "fat": 0},
        "面条": {"calories": 110, "unit": "碗", "protein": 4, "carb": 25, "fat": 1},
        
        # 蛋白质
        "鸡蛋": {"calories": 78, "unit": "个", "protein": 6, "carb": 1, "fat": 5},
        "鸡胸肉": {"calories": 165, "unit": "100g", "protein": 31, "carb": 0, "fat": 4},
        "鱼": {"calories": 206, "unit": "100g", "protein": 22, "carb": 0, "fat": 12},
        
        # 蔬菜
        "蔬菜": {"calories": 25, "unit": "份", "protein": 1, "carb": 5, "fat": 0},
        "沙拉": {"calories": 150, "unit": "份", "protein": 3, "carb": 10, "fat": 10}
    }
    
    # 模糊匹配
    for food_key, data in food_database.items():
        if food_key in food_name:
            return data
    
    return None

def calculate_user_calorie_plan(user_data):
    """
    为用户计算完整的热量计划
    """
    profile = user_data.get("profile", {})
    goals = user_data.get("goals", {})
    
    weight = profile.get("weight_kg", 70)
    height = profile.get("height_cm", 170)
    age = profile.get("age", 30)
    gender = profile.get("gender", "male")
    activity_level = profile.get("activity_level", "low")
    
    target_weight = goals.get("target_weight_kg", 70)
    goal = goals.get("primary", "lose_weight")
    
    # 计算
    bmr = calculate_bmr(weight, height, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    calorie_goal = calculate_calorie_goal(tdee, goal, weight, target_weight)
    macros = calculate_macros(calorie_goal, goal)
    bmi, bmi_category = calculate_bmi(weight, height)
    meal_plan = generate_meal_plan(calorie_goal, macros, goal)
    
    return {
        "bmr": bmr,
        "tdee": tdee,
        "calorie_goal": calorie_goal,
        "macros": macros,
        "bmi": bmi,
        "bmi_category": bmi_category,
        "meal_plan": meal_plan,
        "weight_loss_speed": f"{(calorie_goal - tdee) / 7700 * 7:.1f}kg/周",
        "time_to_goal": f"{(weight - target_weight) / 0.5:.0f}周"
    }

if __name__ == "__main__":
    # 加载用户数据
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
        
        # 为每个用户计算热量计划
        for user_id, user_data in users_data.get("users", {}).items():
            print(f"\n{'='*50}")
            print(f"用户：{user_data.get('name', '未知')}")
            print(f"{'='*50}")
            
            plan = calculate_user_calorie_plan(user_data)
            
            print(f"\n📊 身体数据：")
            print(f"• BMI: {plan['bmi']} ({plan['bmi_category']})")
            print(f"• BMR: {plan['bmr']} 大卡/天（基础代谢）")
            print(f"• TDEE: {plan['tdee']} 大卡/天（总消耗）")
            
            print(f"\n🎯 热量目标：")
            print(f"• 每日摄入：{plan['calorie_goal']} 大卡")
            print(f"• 减重速度：{plan['weight_loss_speed']}")
            print(f"• 到达目标：{plan['time_to_goal']}")
            
            print(f"\n🍽️ 三大营养素：")
            print(f"• 蛋白质：{plan['macros']['protein_g']}g ({plan['macros']['protein_cal']} 大卡)")
            print(f"• 碳水：{plan['macros']['carb_g']}g ({plan['macros']['carb_cal']} 大卡)")
            print(f"• 脂肪：{plan['macros']['fat_g']}g ({plan['macros']['fat_cal']} 大卡)")
            
            print(f"\n📅 一日三餐建议：")
            print(f"• 早餐：{plan['meal_plan']['breakfast']['calories']} 大卡 - {plan['meal_plan']['breakfast']['suggestion']}")
            print(f"• 午餐：{plan['meal_plan']['lunch']['calories']} 大卡 - {plan['meal_plan']['lunch']['suggestion']}")
            print(f"• 晚餐：{plan['meal_plan']['dinner']['calories']} 大卡 - {plan['meal_plan']['dinner']['suggestion']}")
    else:
        print("❌ 未找到用户数据文件")
