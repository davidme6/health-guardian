# Health Guardian - Robust Scheduled Task
$notifyScript = "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\scripts\interactive_notify.py"
$taskName = "HealthGuardian-Active-Notify"
$logFile = "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\logs\notify.log"

# Remove old task
Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

# Create log directory
if (-not (Test-Path (Split-Path $logFile))) {
    New-Item -ItemType Directory -Path (Split-Path $logFile) -Force
}

# Create new task (check every 10 minutes)
$action = New-ScheduledTaskAction -Execute "python" `
    -Argument "`"$notifyScript`"" `
    -WorkingDirectory "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\scripts"

$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
    -RepetitionInterval (New-TimeSpan -Minutes 10) `
    -RepetitionDuration (New-TimeSpan -Days 365)

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

Register-ScheduledTask -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Description "Health Guardian Active Notification - Check every 10 minutes" `
    -Force

# Start task immediately
Start-ScheduledTask -TaskName $taskName

Write-Host "OK - Task created and started"
Write-Host "Task Name: $taskName"
Write-Host "Check Interval: Every 10 minutes"
Write-Host "Log File: $logFile"
