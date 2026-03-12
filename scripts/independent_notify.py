#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康管理系统 - 独立通知服务
通过独立的 Web 端口发送通知，不和主窗口混合
"""

import json
import os
import sys
import threading
import time
import webbrowser
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver

# 配置文件
CONFIG_FILE = Path.home() / ".health_guardian_config.json"
NOTIFY_PORT = 8899  # 独立通知端口

# 提醒时间表
REMINDERS = {
    "07:00": {"title": "🧴 晨间护肤", "content": "洁面→保湿→防晒"},
    "07:30": {"title": "☀️ 早安", "content": "今日计划：饮水 3605ml，运动 30 分钟"},
    "08:00": {"title": "💧 喝水 + 维 C", "content": "250ml 温水 + 维生素 C"},
    "10:00": {"title": "💧 喝水", "content": "250ml 温水"},
    "12:00": {"title": "🍽️ 午餐 + 维 E", "content": "豆制品 + 全谷物 + 坚果"},
    "14:00": {"title": "💧 喝水 + 绿茶", "content": "250ml 温水或绿茶"},
    "16:00": {"title": "💧 喝水 + 加餐", "content": "250ml 水 + 坚果/水果"},
    "17:00": {"title": "🏃 运动", "content": "30 分钟有氧/力量训练"},
    "18:00": {"title": "🍽️ 晚餐 + Omega-3", "content": "清淡 + 深海鱼"},
    "20:00": {"title": "🧘 拉伸", "content": "10 分钟睡前拉伸"},
    "21:00": {"title": "🌙 晚间护肤", "content": "清洁→修复→滋养"},
    "21:30": {"title": "😴 睡前准备", "content": "关闭电子设备，准备呼吸机"},
    "22:30": {"title": "💤 入睡", "content": "保证 7-8 小时睡眠"}
}

# 通知历史
notification_history = []

class NotificationHandler(SimpleHTTPRequestHandler):
    """处理通知请求"""
    
    def do_GET(self):
        if self.path == '/':
            self.send_notification_page()
        elif self.path == '/api/notifications':
            self.send_notifications()
        elif self.path == '/api/check':
            self.check_and_notify()
        else:
            self.send_error(404)
    
    def send_notification_page(self):
        """发送通知页面"""
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>健康管理系统 - 独立通知</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #667eea;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        .header p {{
            color: #666;
            font-size: 16px;
        }}
        .notification {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            animation: slideIn 0.5s ease;
        }}
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .notification.active {{
            border-left: 5px solid #667eea;
        }}
        .notification-title {{
            font-size: 24px;
            color: #333;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .notification-content {{
            font-size: 18px;
            color: #666;
            line-height: 1.6;
        }}
        .notification-time {{
            font-size: 14px;
            color: #999;
            margin-top: 15px;
        }}
        .status {{
            background: #f0f0f0;
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
        }}
        .status-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }}
        .status-item:last-child {{
            border-bottom: none;
        }}
        .status-label {{
            color: #666;
        }}
        .status-value {{
            color: #333;
            font-weight: bold;
        }}
        .btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s;
        }}
        .btn:hover {{
            background: #764ba2;
            transform: translateY(-2px);
        }}
        .history {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin-top: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        .history h2 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        .history-item {{
            padding: 15px;
            border-left: 3px solid #e0e0e0;
            margin-bottom: 10px;
            background: #f9f9f9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏥 健康管理系统</h1>
            <p>独立通知窗口 - 端口：{NOTIFY_PORT}</p>
            <button class="btn" onclick="checkNow()">立即检查</button>
        </div>
        
        <div id="current-notification">
            <!-- 当前通知将显示在这里 -->
        </div>
        
        <div class="status">
            <div class="status-item">
                <span class="status-label">当前时间</span>
                <span class="status-value" id="current-time">--</span>
            </div>
            <div class="status-item">
                <span class="status-label">下次提醒</span>
                <span class="status-value" id="next-reminder">--</span>
            </div>
            <div class="status-item">
                <span class="status-label">今日已提醒</span>
                <span class="status-value" id="today-count">0</span>
            </div>
        </div>
        
        <div class="history">
            <h2>📋 通知历史</h2>
            <div id="history-list">
                <!-- 历史记录 -->
            </div>
        </div>
    </div>
    
    <script>
        let notifications = {history: []};
        
        function updateTime() {{
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleString('zh-CN');
        }}
        
        async function loadNotifications() {{
            try {{
                const response = await fetch('/api/notifications');
                notifications = await response.json();
                renderNotifications();
                updateStatus();
            }} catch (error) {{
                console.error('加载通知失败:', error);
            }}
        }}
        
        function renderNotifications() {{
            const container = document.getElementById('current-notification');
            const historyContainer = document.getElementById('history-list');
            
            if (notifications.current) {{
                container.innerHTML = `
                    <div class="notification active">
                        <div class="notification-title">${{notifications.current.title}}</div>
                        <div class="notification-content">${{notifications.current.content}}</div>
                        <div class="notification-time">${{notifications.current.time}}</div>
                    </div>
                `;
            }} else {{
                container.innerHTML = '<div class="notification"><p>暂无新通知</p></div>';
            }}
            
            historyContainer.innerHTML = notifications.history.slice(-10).reverse().map(item => `
                <div class="history-item">
                    <strong>${{item.title}}</strong> - <small>${{item.time}}</small>
                </div>
            `).join('');
        }}
        
        function updateStatus() {{
            const now = new Date();
            const currentTime = `${{String(now.getHours()).padStart(2, '0')}}:${{String(now.getMinutes()).padStart(2, '0')}}`;
            
            // 计算下次提醒
            let nextReminder = '--';
            for (const time of Object.keys($REMINDERS).sort()) {{
                if (time > currentTime) {{
                    nextReminder = time;
                    break;
                }}
            }}
            
            document.getElementById('next-reminder').textContent = nextReminder;
            document.getElementById('today-count').textContent = notifications.history.filter(h => h.time.includes('${{now.strftime("%Y-%m-%d")}}')).length;
        }}
        
        async function checkNow() {{
            try {{
                const response = await fetch('/api/check', {{ method: 'POST' }});
                const result = await response.json();
                if (result.sent) {{
                    alert('✅ 提醒已发送！');
                    loadNotifications();
                }} else {{
                    alert('ℹ️ ' + (result.message || '暂无新提醒'));
                }}
            }} catch (error) {{
                alert('检查失败：' + error);
            }}
        }}
        
        // 初始加载
        updateTime();
        loadNotifications();
        
        // 每分钟更新
        setInterval(() => {{
            updateTime();
            loadNotifications();
        }}, 60000);
    </script>
</body>
</html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def send_notifications(self):
        """发送通知数据"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        
        data = {
            'current': notification_history[-1] if notification_history else None,
            'history': notification_history[-20:]  # 最近 20 条
        }
        
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        if self.path == '/api/check':
            self.check_and_notify()
        else:
            self.send_error(404)
    
    def check_and_notify(self):
        """检查并发送通知"""
        now = datetime.now()
        current_time = f"{now.hour:02d}:{now.minute:02d}"
        today = now.strftime("%Y-%m-%d")
        
        if current_time in REMINDERS:
            reminder = REMINDERS[current_time]
            
            # 检查是否已发送
            already_sent = any(
                n['title'] == reminder['title'] and n['time'].startswith(today)
                for n in notification_history
            )
            
            if not already_sent:
                # 添加通知
                notification = {
                    'title': reminder['title'],
                    'content': reminder['content'],
                    'time': now.strftime("%Y-%m-%d %H:%M:%S")
                }
                notification_history.append(notification)
                
                # 自动打开浏览器窗口
                threading.Thread(target=open_browser, daemon=True).start()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                
                data = {
                    'sent': True,
                    'notification': notification,
                    'message': f"已发送：{reminder['title']}"
                }
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
                return
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        
        data = {
            'sent': False,
            'message': f"当前时间 {current_time} 没有预设提醒"
        }
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def open_browser():
    """延迟打开浏览器"""
    time.sleep(1)
    webbrowser.open(f'http://localhost:{NOTIFY_PORT}')

def check_periodically():
    """定期检查"""
    while True:
        now = datetime.now()
        current_time = f"{now.hour:02d}:{now.minute:02d}"
        
        if current_time in REMINDERS:
            # 检查是否已发送
            today = now.strftime("%Y-%m-%d")
            already_sent = any(
                n['title'] == REMINDERS[current_time]['title'] and n['time'].startswith(today)
                for n in notification_history
            )
            
            if not already_sent:
                notification = {
                    'title': REMINDERS[current_time]['title'],
                    'content': REMINDERS[current_time]['content'],
                    'time': now.strftime("%Y-%m-%d %H:%M:%S")
                }
                notification_history.append(notification)
                print(f"✅ {notification['time']} - {notification['title']}")
                
                # 打开浏览器通知
                threading.Thread(target=open_browser, daemon=True).start()
        
        # 每分钟检查一次
        time.sleep(60)

def main():
    """主函数"""
    print(f"🏥 健康管理系统 - 独立通知服务")
    print(f"通知端口：http://localhost:{NOTIFY_PORT}")
    print(f"检查频率：每分钟")
    print(f"\n提醒时间表：")
    for time, reminder in REMINDERS.items():
        print(f"  {time} - {reminder['title']}")
    print(f"\n服务启动中...")
    
    # 启动定期检查线程
    check_thread = threading.Thread(target=check_periodically, daemon=True)
    check_thread.start()
    
    # 启动 HTTP 服务器
    with socketserver.TCPServer(("", NOTIFY_PORT), NotificationHandler) as httpd:
        print(f"✅ 服务已启动")
        print(f"\n访问地址：http://localhost:{NOTIFY_PORT}")
        print(f"按 Ctrl+C 停止服务")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n服务已停止")

if __name__ == "__main__":
    main()
