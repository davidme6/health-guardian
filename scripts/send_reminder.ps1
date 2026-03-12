# Health Guardian Reminder Script
# Sends health reminders via OpenClaw Feishu channel

param(
    [string]$ReminderType = "all"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$configFile = "$env:USERPROFILE\.health_guardian_config.json"
$reminderQueueFile = "$env:TEMP\health_reminder_queue.txt"

# Load config
$config = @{}
if (Test-Path $configFile) {
    $config = Get-Content $configFile -Raw | ConvertFrom-Json
}

function Write-ReminderToQueue {
    param([string]$Title, [string]$Content)
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $message = "[$timestamp] $Title`n$Content"
    
    # Write to queue file for OpenClaw to pick up
    Add-Content -Path $reminderQueueFile -Value $message
    
    # Also output to console
    Write-Host $message
}

$currentHour = (Get-Date).Hour
$currentMinute = (Get-Date).Minute
$dateStr = Get-Date -Format "yyyy-MM-dd"

switch ($ReminderType) {
    "morning" {
        Write-ReminderToQueue "☀️ 早上好！" "新的一天开始了！`n`n📅 日期：$dateStr`n💧 今日饮水目标：3605ml`n🏃 运动目标：30 分钟`n😴 睡觉时间：22:30`n`n加油，向着 90kg 的目标前进！💪"
    }
    "water" {
        Write-ReminderToQueue "💧 喝水时间到了！" "建议饮用 250ml 温水`n`n保持水分充足有助于：`n• 新陈代谢`n• 脂肪燃烧`n• 皮肤健康`n`n现在就去喝一杯吧！🥛"
    }
    "meal" {
        Write-ReminderToQueue "🍽️ 用餐时间到了！" "健康饮食建议：`n`n• 多吃蔬菜和高蛋白食物`n• 控制碳水化合物摄入`n• 细嚼慢咽，七分饱`n• 避免油腻和甜食`n`n每一餐都是减肥的机会！🥗"
    }
    "exercise" {
        Write-ReminderToQueue "🏃 运动时间到了！" "建议运动 30 分钟：`n`n• 快走或慢跑`n• 跳绳`n• 俯卧撑/深蹲`n• 瑜伽或拉伸`n`n运动后记得补充水分！💪"
    }
    "sleep" {
        Write-ReminderToQueue "😴 睡前准备时间！" "1 小时后该睡觉了 (22:30)`n`n睡前准备：`n• 关闭电子设备`n• 准备呼吸机`n• 调暗灯光`n• 放松身心`n`n好的睡眠有助于减肥！😴"
    }
    default {
        Write-Host "Unknown reminder type: $ReminderType"
    }
}
