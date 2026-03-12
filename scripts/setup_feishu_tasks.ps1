# Health Guardian - 飞书通知定时任务设置
# 使用 Windows 任务计划程序

$notifyScript = "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\scripts\feishu_notify.py"
$taskNamePrefix = "HealthGuardian-Feishu"

# 删除旧任务
Get-ScheduledTask -TaskName "$taskNamePrefix_*" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

# 创建定时任务（每 10 分钟检查一次）
$action = New-ScheduledTaskAction -Execute "python" -Argument "`"$notifyScript`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 10)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "$taskNamePrefix-Check" -Action $action -Trigger $trigger -Settings $settings -Description "健康管理系统 - 飞书通知检查（每 10 分钟）" -Force

Write-Host "✅ 飞书通知定时任务已创建"
Write-Host "任务名称：$taskNamePrefix-Check"
Write-Host "检查频率：每 10 分钟"
Write-Host ""
Write-Host "使用 Get-ScheduledTask -TaskName '$taskNamePrefix-*' 查看任务状态"
Write-Host "使用 Get-ScheduledTaskLog -TaskName '$taskNamePrefix-Check' 查看执行日志"
