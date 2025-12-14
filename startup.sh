#!/bin/bash

# Startup Script - Initialize work session
# This script pulls code, reviews context, and suggests next steps

echo "🚀 Starting work session..."
echo ""

# Step 1: Pull latest code from GitHub
echo "📥 Step 1: Pulling latest code from GitHub..."
git pull origin main
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: Git pull failed or had conflicts. Please resolve manually."
fi
echo ""

# Step 2: Review current code state
echo "📋 Step 2: Reviewing current state..."
echo ""

# Check for active changes
if [ -d "openspec/changes" ]; then
    echo "Active changes:"
    for dir in openspec/changes/*/; do
        if [ -d "$dir" ] && [ "$(basename "$dir")" != "archive" ]; then
            change_name=$(basename "$dir")
            echo "  - $change_name"
            if [ -f "$dir/tasks.md" ]; then
                echo "    Tasks pending:"
                grep -E "^\s*- \[ \]" "$dir/tasks.md" | head -3
            fi
        fi
    done
else
    echo "  No active changes found."
fi
echo ""

# Step 3: Read handover documents
echo "📝 Step 3: Checking for handover documentation..."
if [ -f "HANDOVER.md" ]; then
    echo "Found HANDOVER.md:"
    echo "---"
    head -20 HANDOVER.md
    echo "---"
else
    echo "  No HANDOVER.md found."
fi
echo ""

# Step 4: Suggest next steps
echo "🎯 Step 4: Suggested next steps..."
echo ""

# Check project conventions
if [ -f "openspec/project.md" ]; then
    echo "✅ Project conventions documented in openspec/project.md"
fi

# Suggest running validation
echo "💡 Recommended actions:"
echo "  1. Review active changes above"
echo "  2. Run: openspec validate --strict"
echo "  3. Continue working on pending tasks"
echo ""

echo "✅ Startup complete! Ready to work."
