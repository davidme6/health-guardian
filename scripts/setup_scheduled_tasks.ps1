# Setup Health Guardian Scheduled Tasks
# Uses Windows Task Scheduler

$reminderScript = "C:\Windows\system32\UsersAdministrator.openclawworkspace\github\davidme6\health-guardian\scripts\send_reminder.ps1"
$taskNamePrefix = "HealthGuardian"

# Remove old tasks if exist
Get-ScheduledTask -TaskName "$taskNamePrefix_*" -ErrorAction SilentlyContinue | Unregister-ScheduledTask -Confirm:$false

# Create scheduled tasks
$tasks = @(
    @{Name = "$taskNamePrefix_Morning"; Time = "07:30"; Args = "-ReminderType morning"},
    @{Name = "$taskNamePrefix_Water1"; Time = "08:00"; Args = "-ReminderType water"},
    @{Name = "$taskNamePrefix_Meal1"; Time = "07:30"; Args = "-ReminderType meal"},
    @{Name = "$taskNamePrefix_Water2"; Time = "10:00"; Args = "-ReminderType water"},
    @{Name = "$taskNamePrefix_Meal2"; Time = "12:00"; Args = "-ReminderType meal"},
    @{Name = "$taskNamePrefix_Water3"; Time = "12:00"; Args = "-ReminderType water"},
    @{Name = "$taskNamePrefix_Water4"; Time = "14:00"; Args = "-ReminderType water"},
    @{Name = "$taskNamePrefix_Water5"; Time = "16:00"; Args = "-ReminderType water"},
    @{Name = "$taskNamePrefix_Exercise"; Time = "17:00"; Args = "-ReminderType exercise"},
    @{Name = "$taskNamePrefix_Meal3"; Time = "18:00"; Args = "-ReminderType meal"},
    @{Name = "$taskNamePrefix_Water6"; Time = "18:00"; Args = "-ReminderType water"},
    @{Name = "$taskNamePrefix_Water7"; Time = "20:00"; Args = "-ReminderType water"},
    @{Name = "$taskNamePrefix_Sleep"; Time = "21:30"; Args = "-ReminderType sleep"}
)

foreach ($task in $tasks) {
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
        -Argument "-ExecutionPolicy Bypass -File `"$reminderScript`" $($task.Args)"
    
    $trigger = New-ScheduledTaskTrigger -Daily -At $task.Time
    
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    
    Register-ScheduledTask -TaskName $task.Name `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Health Guardian Reminder" `
        -Force
    
    Write-Host "Created task: $($task.Name) at $($task.Time)"
}

Write-Host "`nHealth Guardian scheduled tasks setup complete!"
Write-Host "Total tasks created: $($tasks.Count)"
