# Ending Script - Wrap up work session
# This script updates tasks, validates, archives if done, creates handover, and pushes code

Write-Host "🏁 Ending work session..." -ForegroundColor Green
Write-Host ""

# Step 1: Update tasks.md and validate
Write-Host "📝 Step 1: Checking task completion..." -ForegroundColor Cyan
Write-Host ""

# Find active changes
$activeChanges = @()
if (Test-Path "openspec/changes") {
    $activeChanges = Get-ChildItem "openspec/changes" -Directory | Where-Object { $_.Name -ne "archive" } | Select-Object -ExpandProperty Name
}

if ($activeChanges.Count -eq 0) {
    Write-Host "  No active changes to process."
} else {
    foreach ($change in $activeChanges) {
        Write-Host "Processing change: $change" -ForegroundColor Yellow
        
        # Check if all tasks are complete
        $tasksFile = "openspec/changes/$change/tasks.md"
        if (Test-Path $tasksFile) {
            $incomplete = (Get-Content $tasksFile | Select-String "^\s*- \[ \]").Count
            if ($incomplete -eq 0) {
                Write-Host "  ✅ All tasks complete for $change" -ForegroundColor Green
                $response = Read-Host "  Archive this change? (y/n)"
                if ($response -eq 'y' -or $response -eq 'Y') {
                    Write-Host "  📦 Archiving $change..." -ForegroundColor Cyan
                    openspec archive $change --yes
                }
            } else {
                Write-Host "  ⏳ $incomplete tasks still pending" -ForegroundColor Yellow
            }
        }
    }
}
Write-Host ""

# Step 2: Validate
Write-Host "🔍 Step 2: Validating changes..." -ForegroundColor Cyan
openspec validate --strict
Write-Host ""

# Step 3: Create/update handover documentation
Write-Host "📄 Step 3: Creating handover documentation..." -ForegroundColor Cyan

$handoverContent = @"
# Handover Document

**Date:** $(Get-Date -Format "yyyy-MM-dd")
**Session End**

## Current Status

[Describe what was accomplished this session]

## Active Changes

"@

# List active changes
if ($activeChanges.Count -eq 0) {
    $handoverContent += "`nNone`n"
} else {
    foreach ($change in $activeChanges) {
        $handoverContent += "`n- $change"
    }
}

$handoverContent += @"

## Next Steps

[What should be done next session]

## Blockers

[Any issues or decisions needed]

## Notes

[Important context for next session]
"@

Set-Content -Path "HANDOVER.md" -Value $handoverContent

Write-Host "  ✅ HANDOVER.md created/updated" -ForegroundColor Green
Write-Host "  ⚠️  Please edit HANDOVER.md to add session details" -ForegroundColor Yellow
Write-Host ""

# Step 4: Push to GitHub
Write-Host "🚀 Step 4: Pushing to GitHub..." -ForegroundColor Cyan
$commitMsg = Read-Host "Enter commit message (or press Enter for default)"

if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Session end: $(Get-Date -Format 'yyyy-MM-dd')"
}

git add .
git commit -m $commitMsg
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Code pushed successfully" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Push failed. Please check and push manually." -ForegroundColor Yellow
}
Write-Host ""

Write-Host "✅ Session ended successfully!" -ForegroundColor Green
Write-Host "📋 Don't forget to update HANDOVER.md with session details" -ForegroundColor Cyan
