# Setup Health Guardian Scheduled Tasks
$reminderScript = "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\scripts\send_reminder.ps1"

# Remove old tasks
Get-ScheduledTask -TaskName "HealthGuardian_*" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

# Create tasks one by one
$action1 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType morning"
$trigger1 = New-ScheduledTaskTrigger -Daily -At 7:30
Register-ScheduledTask -TaskName "HealthGuardian_Morning" -Action $action1 -Trigger $trigger1 -Force

$action2 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType water"
$trigger2 = New-ScheduledTaskTrigger -Daily -At 8:00
Register-ScheduledTask -TaskName "HealthGuardian_Water1" -Action $action2 -Trigger $trigger2 -Force

$action3 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType water"
$trigger3 = New-ScheduledTaskTrigger -Daily -At 10:00
Register-ScheduledTask -TaskName "HealthGuardian_Water2" -Action $action3 -Trigger $trigger3 -Force

$action4 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType meal"
$trigger4 = New-ScheduledTaskTrigger -Daily -At 12:00
Register-ScheduledTask -TaskName "HealthGuardian_Meal" -Action $action4 -Trigger $trigger4 -Force

$action5 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType water"
$trigger5 = New-ScheduledTaskTrigger -Daily -At 12:00
Register-ScheduledTask -TaskName "HealthGuardian_Water3" -Action $action5 -Trigger $trigger5 -Force

$action6 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType water"
$trigger6 = New-ScheduledTaskTrigger -Daily -At 14:00
Register-ScheduledTask -TaskName "HealthGuardian_Water4" -Action $action6 -Trigger $trigger6 -Force

$action7 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType water"
$trigger7 = New-ScheduledTaskTrigger -Daily -At 16:00
Register-ScheduledTask -TaskName "HealthGuardian_Water5" -Action $action7 -Trigger $trigger7 -Force

$action8 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType exercise"
$trigger8 = New-ScheduledTaskTrigger -Daily -At 17:00
Register-ScheduledTask -TaskName "HealthGuardian_Exercise" -Action $action8 -Trigger $trigger8 -Force

$action9 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType water"
$trigger9 = New-ScheduledTaskTrigger -Daily -At 18:00
Register-ScheduledTask -TaskName "HealthGuardian_Water6" -Action $action9 -Trigger $trigger9 -Force

$action10 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType water"
$trigger10 = New-ScheduledTaskTrigger -Daily -At 20:00
Register-ScheduledTask -TaskName "HealthGuardian_Water7" -Action $action10 -Trigger $trigger10 -Force

$action11 = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" -ReminderType sleep"
$trigger11 = New-ScheduledTaskTrigger -Daily -At 21:30
Register-ScheduledTask -TaskName "HealthGuardian_Sleep" -Action $action11 -Trigger $trigger11 -Force

Write-Host "Health Guardian tasks created successfully!"
Get-ScheduledTask -TaskName "HealthGuardian_*" | Select-Object TaskName, State
