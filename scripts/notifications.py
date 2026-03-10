#!/usr/bin/env python3
"""
Health Guardian - 通知模块
支持多种通知渠道：企业微信、iMessage、钉钉、飞书等
"""

import json
import os
import requests
from typing import Dict, Optional, List
from pathlib import Path

# ============================================================================
# 通知渠道接口定义
# ============================================================================

class NotificationChannel:
    """通知渠道基类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.enabled = config.get("enabled", False)
    
    def send(self, message: str) -> bool:
        """发送通知"""
        raise NotImplementedError
    
    def test(self) -> bool:
        """测试连接"""
        try:
            return self.send("【Health Guardian 测试通知】如果您收到这条消息，说明通知配置成功！")
        except Exception as e:
            print(f"❌ 测试失败：{e}")
            return False


# ============================================================================
# 企业微信通知
# ============================================================================

class WeChatWorkChannel(NotificationChannel):
    """企业微信机器人通知"""
    
    def send(self, message: str) -> bool:
        webhook_url = self.config.get("webhook_url", "")
        if not webhook_url:
            return False
        
        try:
            data = {
                "msgtype": "text",
                "text": {
                    "content": message,
                    "mentioned_list": ["@all"]
                }
            }
            response = requests.post(webhook_url, json=data, timeout=10)
            result = response.json()
            
            if result.get("errcode") == 0:
                print("✅ 企业微信通知已发送")
                return True
            else:
                print(f"❌ 企业微信通知失败：{result}")
                return False
        except Exception as e:
            print(f"❌ 发送企业微信通知失败：{e}")
            return False


# ============================================================================
# iMessage 通知（通过 BlueBubbles 或 iMessage 网关）
# ============================================================================

class iMessageChannel(NotificationChannel):
    """iMessage 通知"""
    
    def send(self, message: str) -> bool:
        # 方式 1: BlueBubbles API
        bluebubbles_url = self.config.get("bluebubbles_url", "")
        bluebubbles_token = self.config.get("bluebubbles_token", "")
        
        if bluebubbles_url and bluebubbles_token:
            return self._send_via_bluebubbles(message, bluebubbles_url, bluebubbles_token)
        
        # 方式 2: 本地 iMessage 脚本（macOS）
        if self.config.get("use_local_imessage", False):
            return self._send_via_local_imessage(message)
        
        print("⚠️  iMessage 未配置")
        return False
    
    def _send_via_bluebubbles(self, message: str, url: str, token: str) -> bool:
        """通过 BlueBubbles API 发送"""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            data = {
                "address": self.config.get("recipient", ""),
                "message": message,
                "method": "iMessage"
            }
            
            response = requests.post(f"{url}/api/v1/message/send", 
                                   json=data, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ iMessage 通知已发送")
                return True
            else:
                print(f"❌ iMessage 发送失败：{response.text}")
                return False
        except Exception as e:
            print(f"❌ 发送 iMessage 失败：{e}")
            return False
    
    def _send_via_local_imessage(self, message: str) -> bool:
        """通过 macOS 本地 AppleScript 发送"""
        import subprocess
        
        recipient = self.config.get("recipient", "")
        if not recipient:
            print("❌ 未指定收件人")
            return False
        
        try:
            script = f'''
            tell application "Messages"
                send "{message}" to buddy "{recipient}" of (service 1 whose service type is iMessage)
            end tell
            '''
            
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ iMessage 通知已发送")
                return True
            else:
                print(f"❌ iMessage 发送失败：{result.stderr}")
                return False
        except Exception as e:
            print(f"❌ 发送 iMessage 失败：{e}")
            return False


# ============================================================================
# 钉钉通知
# ============================================================================

class DingTalkChannel(NotificationChannel):
    """钉钉机器人通知"""
    
    def send(self, message: str) -> bool:
        webhook_url = self.config.get("webhook_url", "")
        secret = self.config.get("secret", "")
        
        if not webhook_url:
            return False
        
        try:
            import time
            import hmac
            import hashlib
            import base64
            import urllib.parse
            
            # 添加签名
            if secret:
                timestamp = str(round(time.time() * 1000))
                secret_enc = secret.encode('utf-8')
                string_to_sign = f'{timestamp}\n{secret}'
                string_to_sign_enc = string_to_sign.encode('utf-8')
                hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
                sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
                webhook_url = f"{webhook_url}&timestamp={timestamp}&sign={sign}"
            
            data = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            result = response.json()
            
            if result.get("errcode") == 0:
                print("✅ 钉钉通知已发送")
                return True
            else:
                print(f"❌ 钉钉通知失败：{result}")
                return False
        except Exception as e:
            print(f"❌ 发送钉钉通知失败：{e}")
            return False


# ============================================================================
# 飞书通知
# ============================================================================

class FeishuChannel(NotificationChannel):
    """飞书机器人通知"""
    
    def send(self, message: str) -> bool:
        webhook_url = self.config.get("webhook_url", "")
        if not webhook_url:
            return False
        
        try:
            data = {
                "msg_type": "text",
                "content": {
                    "text": message
                }
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            result = response.json()
            
            if result.get("StatusCode") == 0 or result.get("code") == 0:
                print("✅ 飞书通知已发送")
                return True
            else:
                print(f"❌ 飞书通知失败：{result}")
                return False
        except Exception as e:
            print(f"❌ 发送飞书通知失败：{e}")
            return False


# ============================================================================
# Slack 通知
# ============================================================================

class SlackChannel(NotificationChannel):
    """Slack 通知"""
    
    def send(self, message: str) -> bool:
        webhook_url = self.config.get("webhook_url", "")
        if not webhook_url:
            return False
        
        try:
            data = {
                "text": message
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            
            if response.status_code == 200:
                print("✅ Slack 通知已发送")
                return True
            else:
                print(f"❌ Slack 通知失败：{response.text}")
                return False
        except Exception as e:
            print(f"❌ 发送 Slack 通知失败：{e}")
            return False


# ============================================================================
# 邮件通知
# ============================================================================

class EmailChannel(NotificationChannel):
    """邮件通知"""
    
    def send(self, message: str) -> bool:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        smtp_server = self.config.get("smtp_server", "")
        smtp_port = self.config.get("smtp_port", 587)
        username = self.config.get("username", "")
        password = self.config.get("password", "")
        to_email = self.config.get("to_email", "")
        
        if not all([smtp_server, username, password, to_email]):
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = to_email
            msg['Subject'] = "🏥 Health Guardian 健康提醒"
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            print("✅ 邮件通知已发送")
            return True
        except Exception as e:
            print(f"❌ 发送邮件失败：{e}")
            return False


# ============================================================================
# Telegram 通知
# ============================================================================

class TelegramChannel(NotificationChannel):
    """Telegram 通知"""
    
    def send(self, message: str) -> bool:
        bot_token = self.config.get("bot_token", "")
        chat_id = self.config.get("chat_id", "")
        
        if not all([bot_token, chat_id]):
            return False
        
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown"
            }
            
            response = requests.post(url, json=data, timeout=10)
            result = response.json()
            
            if result.get("ok"):
                print("✅ Telegram 通知已发送")
                return True
            else:
                print(f"❌ Telegram 通知失败：{result}")
                return False
        except Exception as e:
            print(f"❌ 发送 Telegram 通知失败：{e}")
            return False


# ============================================================================
# 通知管理器
# ============================================================================

class NotificationManager:
    """通知管理器 - 统一管理所有通知渠道"""
    
    CHANNEL_TYPES = {
        "wechat_work": WeChatWorkChannel,
        "imessage": iMessageChannel,
        "dingtalk": DingTalkChannel,
        "feishu": FeishuChannel,
        "slack": SlackChannel,
        "email": EmailChannel,
        "telegram": TelegramChannel
    }
    
    def __init__(self, config: Dict):
        self.config = config
        self.channels: List[NotificationChannel] = []
        self._init_channels()
    
    def _init_channels(self):
        """初始化所有启用的通知渠道"""
        channels_config = self.config.get("channels", {})
        
        for channel_type, channel_config in channels_config.items():
            if channel_config.get("enabled", False):
                channel_class = self.CHANNEL_TYPES.get(channel_type)
                if channel_class:
                    channel = channel_class(channel_config)
                    self.channels.append(channel)
                    print(f"✅ 已初始化通知渠道：{channel_type}")
    
    def send(self, message: str) -> Dict[str, bool]:
        """
        向所有启用的渠道发送通知
        
        返回：{渠道名：是否成功}
        """
        results = {}
        
        for channel in self.channels:
            channel_name = channel.__class__.__name__.replace("Channel", "")
            try:
                success = channel.send(message)
                results[channel_name] = success
            except Exception as e:
                print(f"❌ {channel_name} 发送失败：{e}")
                results[channel_name] = False
        
        return results
    
    def test_all(self) -> Dict[str, bool]:
        """测试所有通知渠道"""
        print("\n🔔 开始测试所有通知渠道...\n")
        
        results = {}
        for channel in self.channels:
            channel_name = channel.__class__.__name__.replace("Channel", "")
            print(f"\n测试 {channel_name}...")
            success = channel.test()
            results[channel_name] = success
        
        print("\n" + "="*60)
        print("📊 测试结果")
        print("="*60)
        for name, success in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {name}")
        print("="*60)
        
        return results
    
    def add_channel(self, channel_type: str, config: Dict) -> bool:
        """添加新的通知渠道"""
        channel_class = self.CHANNEL_TYPES.get(channel_type)
        if not channel_class:
            print(f"❌ 不支持的通知渠道：{channel_type}")
            return False
        
        channel = channel_class(config)
        self.channels.append(channel)
        print(f"✅ 已添加通知渠道：{channel_type}")
        return True
    
    def remove_channel(self, channel_type: str) -> bool:
        """移除通知渠道"""
        for i, channel in enumerate(self.channels):
            if channel.__class__.__name__.replace("Channel", "").lower() == channel_type.lower():
                self.channels.pop(i)
                print(f"✅ 已移除通知渠道：{channel_type}")
                return True
        return False


# ============================================================================
# 辅助函数
# ============================================================================

def create_notification_manager(config_file: Optional[Path] = None) -> NotificationManager:
    """创建通知管理器实例"""
    if config_file is None:
        config_file = Path.home() / ".health_guardian_config.json"
    
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}
    
    return NotificationManager(config)


def send_health_notification(message: str, channels: Optional[List[str]] = None):
    """
    发送健康通知
    
    Args:
        message: 通知内容
        channels: 指定渠道列表，None 表示所有启用的渠道
    """
    manager = create_notification_manager()
    
    if channels:
        # 只发送到指定渠道
        results = {}
        for channel_type in channels:
            channel_class = manager.CHANNEL_TYPES.get(channel_type)
            if channel_class:
                # 从配置中获取该渠道的配置
                config_file = Path.home() / ".health_guardian_config.json"
                with open(config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                channel_config = config.get("notifications", {}).get("channels", {}).get(channel_type, {})
                channel = channel_class(channel_config)
                results[channel_type] = channel.send(message)
        return results
    else:
        # 发送到所有启用的渠道
        return manager.send(message)


# ============================================================================
# 命令行测试
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python notifications.py <command> [args]")
        print("\n命令:")
        print("  test              测试所有通知渠道")
        print("  send <message>    发送通知")
        print("  add <type>        添加通知渠道")
        sys.exit(1)
    
    command = sys.argv[1]
    manager = create_notification_manager()
    
    if command == "test":
        manager.test_all()
    elif command == "send":
        if len(sys.argv) < 3:
            print("❌ 请指定消息内容")
            sys.exit(1)
        message = " ".join(sys.argv[2:])
        results = manager.send(message)
        print("\n发送结果:")
        for channel, success in results.items():
            status = "✅" if success else "❌"
            print(f"{status} {channel}")
    elif command == "add":
        if len(sys.argv) < 3:
            print("❌ 请指定渠道类型")
            print("支持的渠道：wechat_work, imessage, dingtalk, feishu, slack, email, telegram")
            sys.exit(1)
        channel_type = sys.argv[2]
        print(f"添加渠道：{channel_type}")
        print("请手动编辑配置文件添加渠道配置")
    else:
        print(f"❌ 未知命令：{command}")
        sys.exit(1)
