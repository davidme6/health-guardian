# Health Guardian Heartbeat Check
# Run this periodically to send health reminders

$healthDir = "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian"
$stateFile = "$healthDir\reminder_state.json"
$outputFile = "$env:TEMP\health_openclaw_message.txt"

# Load state
$state = @{
    lastCheck = $null
    lastReminder = $null
}
if (Test-Path $stateFile) {
    $state = Get-Content $stateFile -Raw | ConvertFrom-Json
}

# Get current time
$now = Get-Date
$currentHour = $now.Hour
$currentMinute = $now.Minute
$timeStr = "$("{0:D2}" -f $currentHour):$("{0:D2}" -f $currentMinute)"

# Define reminder schedule
$reminders = @{
    "07:30" = @{Type = "morning"; Title = "☀️ 早上好！"; Content = "新的一天开始了！`n`n📅 日期：$($now.ToString('yyyy-MM-dd'))`n💧 今日饮水目标：3605ml`n🏃 运动目标：30 分钟`n😴 睡觉时间：22:30`n`n加油，向着 90kg 的目标前进！💪"}
    "08:00" = @{Type = "water"; Title = "💧 喝水时间到了！"; Content = "建议饮用 250ml 温水`n`n保持水分充足有助于新陈代谢和减肥！🥛"}
    "10:00" = @{Type = "water"; Title = "💧 喝水时间到了！"; Content = "建议饮用 250ml 温水`n`n保持水分充足！🥛"}
    "12:00" = @{Type = "meal"; Title = "🍽️ 午餐时间到了！"; Content = "健康饮食建议：`n• 多吃蔬菜和高蛋白`n• 控制碳水摄入`n• 七分饱就好`n`n每一餐都是减肥的机会！🥗"}
    "14:00" = @{Type = "water"; Title = "💧 喝水时间到了！"; Content = "建议饮用 250ml 温水`n`n下午保持水分充足！🥛"}
    "16:00" = @{Type = "water"; Title = "💧 喝水时间到了！"; Content = "建议饮用 250ml 温水`n`n继续加油！🥛"}
    "17:00" = @{Type = "exercise"; Title = "🏃 运动时间到了！"; Content = "建议运动 30 分钟：`n• 快走或慢跑`n• 跳绳`n• 俯卧撑/深蹲`n`n运动后记得补充水分！💪"}
    "18:00" = @{Type = "meal"; Title = "🍽️ 晚餐时间到了！"; Content = "晚餐建议：`n• 清淡为主`n• 少吃碳水`n• 多吃蔬菜`n`n晚餐七分饱！🥗"}
    "20:00" = @{Type = "water"; Title = "💧 喝水时间到了！"; Content = "建议饮用 250ml 温水`n`n今天是最后一天喝水提醒！🥛"}
    "21:30" = @{Type = "sleep"; Title = "😴 睡前准备时间！"; Content = "1 小时后该睡觉了 (22:30)`n`n睡前准备：`n• 关闭电子设备`n• 准备呼吸机`n• 调暗灯光`n`n好的睡眠有助于减肥！😴"}
}

# Check if it's reminder time
if ($reminders.ContainsKey($timeStr)) {
    $reminder = $reminders[$timeStr]
    
    # Check if we already sent this reminder today
    $today = $now.ToString('yyyy-MM-dd')
    if ($state.lastReminder -ne "$today $timeStr") {
        # Write message to output file for OpenClaw
        $message = "$($reminder.Title)`n$($reminder.Content)"
        $message | Out-File -FilePath $outputFile -Encoding UTF8
        
        # Update state
        $state.lastReminder = "$today $timeStr"
        $state.lastCheck = $now.ToString('yyyy-MM-dd HH:mm:ss')
        $state | ConvertTo-Json | Out-File $stateFile
        
        Write-Host "Reminder ready: $($reminder.Title)"
    } else {
        Write-Host "Reminder already sent for $timeStr"
    }
} else {
    Write-Host "No reminder scheduled for $timeStr"
}
