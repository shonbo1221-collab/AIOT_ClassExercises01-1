---
description: Start a new work session - pull code, review context, suggest next steps
---

# Startup Workflow

This workflow initializes your work session by syncing code, reviewing context, and planning next steps.

## Steps

### 1. Pull Latest Code from GitHub

```bash
git pull origin main
```

Check for any merge conflicts and resolve if necessary.

### 2. Review Current Code State

- Read the current active change in `openspec/changes/` (if any)
- Review `openspec/project.md` for project conventions
- Check recent commits to understand what changed since last session

### 3. Read Handover Documents

Look for handover documentation in:
- `openspec/changes/[active-change]/proposal.md` - Understand the current change
- `openspec/changes/[active-change]/tasks.md` - See what's pending
- `openspec/changes/[active-change]/design.md` - Review technical decisions (if exists)
- Any `.md` files in the project root or docs folder

### 4. Suggest Next Steps

Based on the review:
- Identify incomplete tasks from `tasks.md`
- Check validation status: `openspec validate --strict`
- Suggest the next logical task to work on
- Highlight any blockers or issues found

## Expected Output

A summary including:
- ✅ Code sync status
- 📋 Current active change (if any)
- 📝 Pending tasks
- 🎯 Recommended next action
