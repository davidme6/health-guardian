# Health Guardian - OpenClaw Integration
# This script checks for pending reminders and sends them via OpenClaw

$reminderQueueFile = "$env:TEMP\health_reminder_queue.txt"
$lastSentFile = "$env:TEMP\health_last_sent.txt"

# Check if there are pending reminders
if (Test-Path $reminderQueueFile) {
    $lastSentTime = ""
    if (Test-Path $lastSentFile) {
        $lastSentTime = Get-Content $lastSentFile
    }
    
    $content = Get-Content $reminderQueueFile
    $newContent = @()
    $hasNewReminder = $false
    
    foreach ($line in $content) {
        if ($line -and $line -notlike "*$lastSentTime*") {
            # This is a new reminder, output it for OpenClaw to send
            Write-Host $line
            $hasNewReminder = $true
        }
        $newContent += $line
    }
    
    if ($hasNewReminder) {
        # Update last sent time
        Get-Date -Format "yyyy-MM-dd HH:mm:ss" | Out-File $lastSentFile
    }
}
