# Health Guardian - Multi-User Feishu Scheduled Task
$notifyScript = "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\scripts\multi_user_notify.py"
$taskName = "HealthGuardian-MultiUser-Notify"

# Remove old task if exists
Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

# Create new task (check every 10 minutes)
$action = New-ScheduledTaskAction -Execute "python" -Argument "`"$notifyScript`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 10)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Health Guardian Multi-User Feishu Notification - Check every 10 minutes" -Force

Write-Host "OK - Multi-user notification task created"
Write-Host "Task Name: $taskName"
Write-Host "Check Interval: Every 10 minutes"
