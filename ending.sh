#!/bin/bash

# Ending Script - Wrap up work session
# This script updates tasks, validates, archives if done, creates handover, and pushes code

echo "🏁 Ending work session..."
echo ""

# Step 1: Update tasks.md and validate
echo "📝 Step 1: Checking task completion..."
echo ""

# Find active changes
active_changes=()
if [ -d "openspec/changes" ]; then
    for dir in openspec/changes/*/; do
        if [ -d "$dir" ] && [ "$(basename "$dir")" != "archive" ]; then
            active_changes+=("$(basename "$dir")")
        fi
    done
fi

if [ ${#active_changes[@]} -eq 0 ]; then
    echo "  No active changes to process."
else
    for change in "${active_changes[@]}"; do
        echo "Processing change: $change"
        
        # Check if all tasks are complete
        if [ -f "openspec/changes/$change/tasks.md" ]; then
            incomplete=$(grep -c "^\s*- \[ \]" "openspec/changes/$change/tasks.md" || true)
            if [ "$incomplete" -eq 0 ]; then
                echo "  ✅ All tasks complete for $change"
                read -p "  Archive this change? (y/n): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    echo "  📦 Archiving $change..."
                    openspec archive "$change" --yes
                fi
            else
                echo "  ⏳ $incomplete tasks still pending"
            fi
        fi
    done
fi
echo ""

# Step 2: Validate
echo "🔍 Step 2: Validating changes..."
openspec validate --strict
echo ""

# Step 3: Create/update handover documentation
echo "📄 Step 3: Creating handover documentation..."
cat > HANDOVER.md << 'EOF'
# Handover Document

**Date:** $(date +%Y-%m-%d)
**Session End**

## Current Status

[Describe what was accomplished this session]

## Active Changes

EOF

# List active changes
if [ ${#active_changes[@]} -eq 0 ]; then
    echo "None" >> HANDOVER.md
else
    for change in "${active_changes[@]}"; do
        echo "- $change" >> HANDOVER.md
    done
fi

cat >> HANDOVER.md << 'EOF'

## Next Steps

[What should be done next session]

## Blockers

[Any issues or decisions needed]

## Notes

[Important context for next session]
EOF

echo "  ✅ HANDOVER.md created/updated"
echo "  ⚠️  Please edit HANDOVER.md to add session details"
echo ""

# Step 4: Push to GitHub
echo "🚀 Step 4: Pushing to GitHub..."
read -p "Enter commit message (or press Enter for default): " commit_msg

if [ -z "$commit_msg" ]; then
    commit_msg="Session end: $(date +%Y-%m-%d)"
fi

git add .
git commit -m "$commit_msg"
git push origin main

if [ $? -eq 0 ]; then
    echo "  ✅ Code pushed successfully"
else
    echo "  ⚠️  Push failed. Please check and push manually."
fi
echo ""

echo "✅ Session ended successfully!"
echo "📋 Don't forget to update HANDOVER.md with session details"
