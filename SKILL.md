---
name: health-guardian
description: Personal Health Guardian - Comprehensive health management with weight loss, hydration tracking, exercise reminders, sleep optimization, and personalized recommendations. Integrates weather data for context-aware suggestions. Supports WeChat/Enterprise WeChat notifications.
version: 1.0.0
author: davidme6
homepage: https://github.com/davidme6/openclaw/tree/main/skills/health-guardian
---

# 🏥 Health Guardian - 个人健康管家

**全方位健康管理 · 科学减肥 · 智能提醒 · 个性化建议**

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| **💧 喝水提醒** | 定时提醒，根据体重计算饮水量 |
| **🏃 运动计划** | 个性化运动建议，结合天气 |
| **😴 睡眠优化** | 睡眠呼吸暂停支持，呼吸机提醒 |
| **🍽️ 饮食指导** | 卡路里计算，营养建议 |
| **⚖️ 体重管理** | BMI 计算，减肥计划追踪 |
| **🌤️ 天气集成** | 根据当地天气调整建议 |
| **📱 多渠道通知** | OpenClaw Web + 微信/企业微信 |

## 📋 用户配置

### 基本信息

```json
{
  "height": 178,           // 身高 (cm)
  "weight": 103,           // 体重 (kg)
  "age": 30,               // 年龄
  "gender": "male",        // 性别
  "goal": "lose_weight",   // 目标：lose_weight/gain_muscle/maintain
  "activity_level": "low"  // 活动量：sedentary/low/moderate/high
}
```

### 健康状况

```json
{
  "conditions": [
    "sleep_apnea",         // 睡眠呼吸暂停
    "high_blood_pressure", // 高血压
    "diabetes"             // 糖尿病
  ],
  "devices": [
    "cpap"                 // 呼吸机
  ],
  "medications": []
}
```

### 通知设置

```json
{
  "wechat_enabled": true,
  "enterprise_wechat_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
  "notification_times": {
    "water": ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"],
    "meal": ["07:30", "12:00", "18:00"],
    "exercise": ["17:00"],
    "sleep": ["21:30"]
  }
}
```

## 🚀 使用方式

### CLI 命令

```bash
# 初始化用户资料
python scripts/health_guardian.py init

# 查看今日计划
python scripts/health_guardian.py today

# 记录喝水
python scripts/health_guardian.py log-water 250

# 记录体重
python scripts/health_guardian.py log-weight 102.5

# 查看 BMI 和健康评分
python scripts/health_guardian.py status

# 获取运动建议（结合天气）
python scripts/health_guardian.py exercise-suggestion

# 手动触发提醒
python scripts/health_guardian.py remind water
```

### OpenClaw 集成

```
用户：我今天该喝多少水？

Health Guardian: 根据您的体重 (103kg)，今日建议饮水量为 3500ml。
已为您设置 7 次喝水提醒，下次提醒：14:00
当前进度：1500ml / 3500ml 💧
```

## 📊 科学计算

### 每日饮水量
```
基础量 (ml) = 体重 (kg) × 35
运动追加 = 运动时长 (分钟) × 12
天气追加 = 温度>30°C ? 500 : 0
```

### BMI 计算
```
BMI = 体重 (kg) / 身高 (m)²

分类:
< 18.5  偏瘦
18.5-24 正常
24-28   偏胖
> 28    肥胖
```

### 每日卡路里需求
```
BMR (男) = 88.36 + (13.4 × 体重 kg) + (4.8 × 身高 cm) - (5.7 × 年龄)
BMR (女) = 447.6 + (9.2 × 体重 kg) + (3.1 × 身高 cm) - (4.3 × 年龄)

TDEE = BMR × 活动系数
减肥目标 = TDEE - 500 (每日 deficit)
```

## 🌤️ 天气集成

```bash
# 获取当地天气
wttr.in/北京

# 根据天气调整建议
温度 > 30°C → 增加饮水量 500ml
温度 < 10°C → 建议室内运动
雨天 → 室内运动替代方案
空气质量差 → 避免户外运动
```

## 📱 多渠道通知集成

### 支持的通知渠道

| 渠道 | 配置难度 | 实时性 | 推荐度 |
|------|---------|--------|--------|
| **企业微信** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **iMessage** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **钉钉** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **飞书** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Slack** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Telegram** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **邮件** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### 企业微信配置

```python
import requests

def send_wechat_notification(message):
    webhook_url = "YOUR_WEBHOOK_URL"
    data = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    requests.post(webhook_url, json=data)
```

### 通知模板

```
💧 喝水提醒
时间：14:00
建议：250ml
今日进度：1500/3500ml (43%)

🏃 运动时间
时间：17:00
天气：晴 25°C
建议：户外慢跑 30 分钟

😴 睡前准备
时间：21:30
提醒：关闭电子设备，准备呼吸机
目标睡眠：22:30
```

## ⚠️ 医疗免责声明

**重要：** 本技能提供的建议仅供参考，不能替代专业医疗建议。

- 如有健康问题，请咨询医生
- 减肥计划应在专业人士指导下进行
- 呼吸机使用请遵医嘱
- 本技能不诊断、治疗任何疾病

## 📁 文件结构

```
health-guardian/
├── SKILL.md                  # 技能定义
├── README.md                 # 使用文档
├── LICENSE                   # 许可证
├── _meta.json                # ClawHub 元数据
├── scripts/
│   ├── health_guardian.py    # 主脚本
│   ├── notifications.py      # 通知模块
│   ├── weather.py            # 天气集成
│   └── calculations.py       # 健康计算
└── references/
    ├── health-guidelines.md  # 健康指南
    └── notification-templates.md  # 通知模板
```

## 🔧 配置示例

### 完整配置文件 (.health_guardian_config.json)

```json
{
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
    "wechat_webhook": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "enabled": true,
    "quiet_hours": ["22:00", "07:00"]
  },
  "reminders": {
    "water": {
      "enabled": true,
      "times": ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"],
      "amount_ml": 250
    },
    "meals": {
      "enabled": true,
      "times": ["07:30", "12:00", "18:00"]
    },
    "exercise": {
      "enabled": true,
      "times": ["17:00"],
      "duration_min": 30
    },
    "sleep": {
      "enabled": true,
      "bedtime": "22:30",
      "reminder_time": "21:30"
    }
  },
  "location": {
    "city": "北京",
    "weather_service": "wttr.in"
  }
}
```

## 📊 进度追踪

### 周报生成

```bash
python scripts/health_guardian.py weekly-report
```

输出示例：
```
📊 健康周报 (2026-03-03 ~ 2026-03-10)

⚖️ 体重变化
本周：103.0kg → 102.2kg (-0.8kg)
目标：75.0kg (还需 -27.2kg)

💧 喝水达标率
平均每日：2800ml / 3500ml (80%)

🏃 运动完成
本周运动：4 次 / 目标 5 次

😴 睡眠质量
平均睡眠：6.5 小时
呼吸机使用率：100% ✅
```

## 🆘 故障排除

**Q: 微信通知不工作？**
A: 检查 webhook URL 是否正确，确保企业微信机器人已启用

**Q: 天气数据获取失败？**
A: 检查网络连接，wttr.in 可能暂时不可用

**Q: 提醒时间不准确？**
A: 检查系统时区设置，确认配置文件中的时间格式

---

**版本:** 1.0.0
**作者:** davidme6
**许可:** MIT
**发布日期:** 2026-03-10
