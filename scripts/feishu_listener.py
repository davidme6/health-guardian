#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书事件监听服务 - 接收并回复群消息
实现双向互动功能
"""

import json
import base64
import hashlib
import hmac
import time
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from pathlib import Path
import threading

# 配置文件
CONFIG_FILE = Path(__file__).parent.parent / "feishu_config.json"
USERS_FILE = Path.home() / ".health_users.json"

class FeishuEventHandler(BaseHTTPRequestHandler):
    """处理飞书事件"""
    
    def do_POST(self):
        """接收 POST 请求"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            event_data = json.loads(post_data.decode('utf-8'))
            
            # 验证挑战（飞书验证用）
            if event_data.get('type') == 'url_verification':
                challenge = event_data.get('challenge', '')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'challenge': challenge}).encode())
                return
            
            # 处理消息事件
            if event_data.get('type') == 'im.message.receive_v1':
                self.handle_message(event_data)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode())
            
        except Exception as e:
            print(f"❌ 处理事件失败：{e}")
            self.send_response(500)
            self.end_headers()
    
    def handle_message(self, event_data):
        """处理接收到的消息"""
        try:
            # 解析消息内容
            header = event_data.get('header', {})
            event = event_data.get('event', {})
            message = event.get('message', {})
            
            # 获取消息内容
            content_json = json.loads(message.get('content', '{}'))
            text = content_json.get('text', '')
            
            # 获取用户信息
            sender_id = event.get('sender', {}).get('sender_id', {}).get('open_id', '')
            chat_id = event.get('chat_id', '')
            
            print(f"📨 收到消息：{text}")
            print(f"发送者：{sender_id}")
            print(f"群聊：{chat_id}")
            
            # 处理消息并回复
            response = self.process_user_message(text, sender_id, chat_id)
            
            if response:
                self.send_feishu_message(chat_id, response)
                
        except Exception as e:
            print(f"❌ 处理消息失败：{e}")
    
    def process_user_message(self, text, user_id, chat_id):
        """处理用户消息，返回回复内容"""
        text = text.strip().lower()
        
        # 饮水记录
        if any(keyword in text for keyword in ['喝水', '饮水', '喝了', 'ml']):
            return self.handle_water_record(text, user_id)
        
        # 运动记录
        elif any(keyword in text for keyword in ['运动', '跑步', '走路', '步', '分钟']):
            return self.handle_exercise_record(text, user_id)
        
        # 饮食记录
        elif any(keyword in text for keyword in ['吃', '喝', '早餐', '午餐', '晚餐', '饭']):
            return self.handle_food_record(text, user_id)
        
        # 查询状态
        elif any(keyword in text for keyword in ['状态', '进度', '多少', '查看']):
            return self.handle_status_query(user_id)
        
        # 体重记录
        elif any(keyword in text for keyword in ['体重', 'kg', '公斤']):
            return self.handle_weight_record(text, user_id)
        
        # 睡眠记录
        elif any(keyword in text for keyword in ['睡觉', '睡眠', '昨晚']):
            return self.handle_sleep_record(text, user_id)
        
        # 帮助
        elif any(keyword in text for keyword in ['帮助', 'help', '怎么用']):
            return self.get_help_message()
        
        return None
    
    def handle_water_record(self, text, user_id):
        """处理饮水记录"""
        # 提取数字（ml）
        import re
        numbers = re.findall(r'\d+', text)
        amount = int(numbers[0]) if numbers else 250
        
        # 更新用户数据
        self.update_user_stats(user_id, 'today_water_ml', amount)
        
        # 获取当前进度
        user_data = self.get_user_data(user_id)
        today_water = user_data.get('stats', {}).get('today_water_ml', 0)
        daily_goal = user_data.get('goals', {}).get('daily_water_ml', 3605)
        percentage = int((today_water / daily_goal) * 100)
        
        return f"""✅ 已记录饮水 {amount}ml！

💧 **当前进度**
• 已喝：{today_water}ml / {daily_goal}ml
• 进度：{percentage}%
• 还需喝：{daily_goal - today_water}ml

💡 **建议**
• 每小时喝 250ml
• 小口慢饮，不要一次喝太多

继续加油！💪"""
    
    def handle_exercise_record(self, text, user_id):
        """处理运动记录"""
        import re
        numbers = re.findall(r'\d+', text)
        
        # 判断是分钟还是步数
        if '步' in text:
            steps = int(numbers[0]) if numbers else 0
            self.update_user_stats(user_id, 'today_steps', steps)
            
            # 估算卡路里（每步约 0.04 大卡）
            calories = int(steps * 0.04)
            
            return f"""✅ 已记录步数 {steps}步！

🏃 **运动数据**
• 步数：{steps}步
• 估算消耗：{calories}大卡

💡 **建议**
• 每日目标：6000-10000 步
• 保持这个节奏！

继续加油！💪"""
        else:
            minutes = int(numbers[0]) if numbers else 30
            self.update_user_stats(user_id, 'today_exercise_min', minutes)
            
            # 估算卡路里（每分钟约 5 大卡）
            calories = int(minutes * 5)
            
            return f"""✅ 已记录运动 {minutes}分钟！

🏃 **运动数据**
• 时间：{minutes}分钟
• 估算消耗：{calories}大卡

💡 **建议**
• 每日目标：30 分钟
• 运动后记得补充水分

太棒了！继续保持！💪"""
    
    def handle_food_record(self, text, user_id):
        """处理饮食记录"""
        # 简单分析
        food_text = text.replace('吃了', '').replace('吃', '').replace('喝了', '').replace('喝', '')
        
        # 记录饮食
        self.append_user_log(user_id, 'food', food_text)
        
        # 估算热量（简单匹配）
        calories = self.estimate_food_calories(text)
        
        return f"""✅ 已记录饮食！

🍽️ **食物分析**
• 内容：{food_text}
• 估算热量：{calories}大卡

💡 **建议**
• 选择高蛋白、低碳水食物
• 多吃蔬菜
• 避免油炸食品

今日总热量会持续更新！📊"""
    
    def handle_weight_record(self, text, user_id):
        """处理体重记录"""
        import re
        numbers = re.findall(r'\d+\.?\d*', text)
        weight = float(numbers[0]) if numbers else 0
        
        # 更新体重
        self.update_user_profile(user_id, 'weight_kg', weight)
        
        # 获取目标体重
        user_data = self.get_user_data(user_id)
        target = user_data.get('goals', {}).get('target_weight_kg', 90)
        diff = weight - target
        
        return f"""✅ 已记录体重 {weight}kg！

⚖️ **体重数据**
• 当前：{weight}kg
• 目标：{target}kg
• 还需减：{diff:.1f}kg

💡 **建议**
• 每周减重 0.5-1kg 最安全
• 坚持就是胜利！

加油！你一定能做到！💪"""
    
    def handle_sleep_record(self, text, user_id):
        """处理睡眠记录"""
        # 记录睡眠质量
        self.append_user_log(user_id, 'sleep', text)
        
        return f"""✅ 已记录睡眠情况！

😴 **睡眠数据**
• 记录：{text}

💡 **建议**
• 保证 7-8 小时睡眠
• 22:30 前入睡
• 睡前 1 小时不用手机

好的睡眠有助于减肥！🌙"""
    
    def handle_status_query(self, user_id):
        """处理状态查询"""
        user_data = self.get_user_data(user_id)
        stats = user_data.get('stats', {})
        goals = user_data.get('goals', {})
        
        today_water = stats.get('today_water_ml', 0)
        daily_water = goals.get('daily_water_ml', 3605)
        exercise = stats.get('today_exercise_min', 0)
        
        water_pct = int((today_water / daily_water) * 100)
        
        return f"""📊 **你的健康状态**

💧 **饮水**
• 已喝：{today_water}ml / {daily_water}ml
• 进度：{water_pct}%

🏃 **运动**
• 已运动：{exercise}分钟
• 目标：30 分钟

🍽️ **饮食**
• 记录的食物会显示在这里

😴 **睡眠**
• 目标：22:30 入睡

💡 **下一步**
• 多喝水
• 坚持运动
• 清淡饮食

继续加油！💪"""
    
    def get_help_message(self):
        """返回帮助信息"""
        return """💬 **我可以帮你记录**：

1️⃣ **饮水**
"喝了 250ml"
"喝水 300ml"

2️⃣ **运动**
"运动了 30 分钟"
"走了 5000 步"

3️⃣ **饮食**
"吃了汉堡和薯条"
"早餐吃了鸡蛋牛奶"

4️⃣ **体重**
"体重 102.5kg"

5️⃣ **睡眠**
"昨晚睡得不错"

6️⃣ **查询**
"查看健康状态"
"今天喝了多少水"

**直接发消息给我就行！** 🤖"""
    
    def send_feishu_message(self, chat_id, text):
        """发送消息到飞书"""
        config = self.load_config()
        app_access_token = config.get('app_access_token', '')
        
        if not app_access_token:
            print("❌ 缺少 app_access_token")
            return
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        
        headers = {
            'Authorization': f'Bearer {app_access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }
        
        params = {"receive_id_type": "chat_id"}
        
        try:
            response = requests.post(url, headers=headers, json=payload, params=params)
            if response.status_code == 200:
                print("✅ 消息发送成功")
            else:
                print(f"❌ 发送失败：{response.text}")
        except Exception as e:
            print(f"❌ 发送消息异常：{e}")
    
    def load_config(self):
        """加载配置"""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_user_data(self, user_id):
        """获取用户数据"""
        if USERS_FILE.exists():
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
                users = users_data.get('users', {})
                return users.get(user_id, {})
        return {}
    
    def update_user_stats(self, user_id, key, value):
        """更新用户统计数据"""
        if USERS_FILE.exists():
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            users = users_data.get('users', {})
            if user_id in users:
                users[user_id].setdefault('stats', {})
                current = users[user_id]['stats'].get(key, 0)
                users[user_id]['stats'][key] = current + value
                users[user_id]['stats']['last_update'] = datetime.now().isoformat()
            
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    def update_user_profile(self, user_id, key, value):
        """更新用户档案"""
        if USERS_FILE.exists():
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            users = users_data.get('users', {})
            if user_id in users:
                users[user_id].setdefault('profile', {})
                users[user_id]['profile'][key] = value
            
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    def append_user_log(self, user_id, log_type, content):
        """添加用户日志"""
        if USERS_FILE.exists():
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
            
            users = users_data.get('users', {})
            if user_id in users:
                users[user_id].setdefault('logs', [])
                users[user_id]['logs'].append({
                    'type': log_type,
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                })
            
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users_data, f, ensure_ascii=False, indent=2)
    
    def estimate_food_calories(self, text):
        """估算食物热量"""
        # 简单估算
        calories = 0
        
        if '汉堡' in text:
            calories += 250 * text.count('汉堡')
        if '薯条' in text:
            calories += 312
        if '可乐' in text:
            if '无糖' in text:
                calories += 0
            else:
                calories += 140
        if '耙耙柑' in text:
            calories += 45 * text.count('耙耙柑')
        if '鸡蛋' in text:
            calories += 78 * text.count('鸡蛋')
        if '米饭' in text:
            calories += 130 * text.count('米饭')
        
        return calories

def get_app_access_token(app_id, app_secret):
    """获取应用的 access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    
    payload = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            return result.get('app_access_token')
    
    return None

def run_server(port=8080):
    """启动 HTTP 服务器"""
    server = HTTPServer(('0.0.0.0', port), FeishuEventHandler)
    print(f"🚀 飞书事件监听服务已启动")
    print(f"📍 监听端口：{port}")
    print(f"⏰ 等待飞书事件...")
    server.serve_forever()

if __name__ == "__main__":
    port = 8080
    print(f"🏥 飞书双向互动服务")
    print(f"启动端口：{port}")
    run_server(port)
