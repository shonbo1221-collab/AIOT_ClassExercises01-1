---
description: End work session - wrap up tasks, validate, archive if done, create handover, push code
---

# Ending Workflow

This workflow wraps up your work session by updating documentation, validating changes, archiving if complete, and syncing to GitHub.

## Steps

### 1. Wrap Up and Update Documentation

#### 1.1 Update tasks.md
- Mark completed tasks as `[x]`
- Mark in-progress tasks as `[/]`
- Leave pending tasks as `[ ]`

#### 1.2 Validate Changes
```bash
openspec validate --strict
```

Fix any validation errors before proceeding.

#### 1.3 Check if Change is Complete
- Review `tasks.md` - are all tasks marked `[x]`?
- If YES: Proceed to archive (step 2)
- If NO: Skip to handover documentation (step 3)

### 2. Archive Change (Only if Complete)

**Only run this if ALL tasks are done and validated.**

```bash
openspec archive <change-id> --yes
```

This will:
- Move change to `changes/archive/YYYY-MM-DD-<change-id>/`
- Update `specs/` with implemented changes
- Validate the archived state

### 3. Write Handover Documentation

Create or update a handover document for the next session:

**File:** `HANDOVER.md` (in project root)

Include:
- **Current Status:** What was accomplished this session
- **Active Change:** Which change is in progress (if any)
- **Next Steps:** What should be done next
- **Blockers:** Any issues or decisions needed
- **Notes:** Important context for next session

### 4. Push Code to GitHub

```bash
git add .
git commit -m "Session end: [brief description of work done]"
git push origin main
```

Use descriptive commit messages that reference the change ID if applicable.

## Expected Output

A clean session end with:
- ✅ Updated task.md
- ✅ Validation passed
- ✅ Change archived (if complete)
- ✅ Handover document created/updated
- ✅ Code pushed to GitHub
