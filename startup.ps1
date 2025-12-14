# Startup Script - Initialize work session
# This script pulls code, reviews context, and suggests next steps

Write-Host "🚀 Starting work session..." -ForegroundColor Green
Write-Host ""

# Step 1: Pull latest code from GitHub
Write-Host "📥 Step 1: Pulling latest code from GitHub..." -ForegroundColor Cyan
try {
    git pull origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Warning: Git pull failed or had conflicts. Please resolve manually." -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Error pulling from git: $_" -ForegroundColor Yellow
}
Write-Host ""

# Step 2: Review current code state
Write-Host "📋 Step 2: Reviewing current state..." -ForegroundColor Cyan
Write-Host ""

# Check for active changes
if (Test-Path "openspec/changes") {
    Write-Host "Active changes:"
    Get-ChildItem "openspec/changes" -Directory | Where-Object { $_.Name -ne "archive" } | ForEach-Object {
        $changeName = $_.Name
        Write-Host "  - $changeName" -ForegroundColor Yellow
        
        $tasksFile = Join-Path $_.FullName "tasks.md"
        if (Test-Path $tasksFile) {
            Write-Host "    Tasks pending:"
            Get-Content $tasksFile | Select-String "^\s*- \[ \]" | Select-Object -First 3 | ForEach-Object {
                Write-Host "      $_"
            }
        }
    }
} else {
    Write-Host "  No active changes found."
}
Write-Host ""

# Step 3: Read handover documents
Write-Host "📝 Step 3: Checking for handover documentation..." -ForegroundColor Cyan
if (Test-Path "HANDOVER.md") {
    Write-Host "Found HANDOVER.md:"
    Write-Host "---" -ForegroundColor Gray
    Get-Content "HANDOVER.md" | Select-Object -First 20
    Write-Host "---" -ForegroundColor Gray
} else {
    Write-Host "  No HANDOVER.md found."
}
Write-Host ""

# Step 4: Suggest next steps
Write-Host "🎯 Step 4: Suggested next steps..." -ForegroundColor Cyan
Write-Host ""

# Check project conventions
if (Test-Path "openspec/project.md") {
    Write-Host "✅ Project conventions documented in openspec/project.md" -ForegroundColor Green
}

# Suggest running validation
Write-Host "💡 Recommended actions:" -ForegroundColor Magenta
Write-Host "  1. Review active changes above"
Write-Host "  2. Run: openspec validate --strict"
Write-Host "  3. Continue working on pending tasks"
Write-Host ""

Write-Host "✅ Startup complete! Ready to work." -ForegroundColor Green
