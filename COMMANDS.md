# Health Guardian - Quick Commands

## 发送健康提醒到飞书

```bash
# 检查并发送待发送的提醒
python github\davidme6\health-guardian\scripts\heartbeat_check.py

# 如果有提醒，查看消息内容
type $env:USERPROFILE\.health_reminder_message.txt
```

## 手动触发提醒

```bash
# 喝水提醒
powershell -ExecutionPolicy Bypass -File "github\davidme6\health-guardian\scripts\send_reminder.ps1" -ReminderType water

# 用餐提醒
powershell -ExecutionPolicy Bypass -File "github\davidme6\health-guardian\scripts\send_reminder.ps1" -ReminderType meal

# 运动提醒
powershell -ExecutionPolicy Bypass -File "github\davidme6\health-guardian\scripts\send_reminder.ps1" -ReminderType exercise

# 睡前提醒
powershell -ExecutionPolicy Bypass -File "github\davidme6\health-guardian\scripts\send_reminder.ps1" -ReminderType sleep
```

## 查看健康状态

```bash
$env:PYTHONUTF8=1; python github\davidme6\health-guardian\scripts\health_guardian.py today
$env:PYTHONUTF8=1; python github\davidme6\health-guardian\scripts\health_guardian.py status
```

## 记录数据

```bash
# 记录喝水 250ml
$env:PYTHONUTF8=1; python github\davidme6\health-guardian\scripts\health_guardian.py log-water 250

# 记录体重
$env:PYTHONUTF8=1; python github\davidme6\health-guardian\scripts\health_guardian.py log-weight 102.5
```

## 定时提醒

Windows 任务计划程序已设置，会在以下时间自动触发提醒：
- 07:30, 08:00, 10:00, 12:00, 14:00, 16:00, 17:00, 18:00, 20:00, 21:30

提醒消息会写入：`%TEMP%\health_reminder_queue.txt`
