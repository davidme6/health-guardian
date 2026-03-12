# Health Guardian - OpenClaw Skill
# 通过 OpenClaw 飞书通道发送健康提醒

## 命令

### 查看今日健康计划
```
/health today
```

### 记录喝水
```
/health water 250
```

### 记录体重
```
/health weight 102.5
```

### 查看健康状态
```
/health status
```

### 手动触发提醒
```
/health remind water
/health remind meal
/health remind exercise
/health remind sleep
```

## 定时提醒

定时提醒通过 Windows 任务计划程序自动触发，会在以下时间发送消息到你的飞书：

| 时间 | 提醒 |
|------|------|
| 07:30 | ☀️ 早安 + 早餐 |
| 08:00 | 💧 喝水 #1 |
| 10:00 | 💧 喝水 #2 |
| 12:00 | 🍽️ 午餐 + 💧 喝水 #3 |
| 14:00 | 💧 喝水 #4 |
| 16:00 | 💧 喝水 #5 |
| 17:00 | 🏃 运动 |
| 18:00 | 💧 喝水 #6 |
| 20:00 | 💧 喝水 #7 |
| 21:30 | 😴 睡前准备 |

## 配置

配置文件位置：`C:\Users\Administrator\.health_guardian_config.json`

## 脚本位置

- 主脚本：`github\davidme6\health-guardian\scripts\health_guardian.py`
- 提醒脚本：`github\davidme6\health-guardian\scripts\send_reminder.ps1`
- 检查提醒：`github\davidme6\health-guardian\scripts\check_reminders.ps1`
