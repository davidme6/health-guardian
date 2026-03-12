# Health Guardian - Feishu Scheduled Task Setup
$notifyScript = "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\scripts\feishu_standalone.py"
$taskName = "HealthGuardian-Feishu-Notify"

# Remove old task if exists
Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

# Create new task (check every 10 minutes)
$action = New-ScheduledTaskAction -Execute "python" -Argument "`"$notifyScript`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 10)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Health Guardian Feishu Notification - Check every 10 minutes" -Force

Write-Host "OK - Feishu notification task created"
Write-Host "Task Name: $taskName"
Write-Host "Check Interval: Every 10 minutes"
