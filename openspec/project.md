# Project Context

## Purpose
AIoT (AI + IoT) course project for Master's degree program.

## Tech Stack
- [To be filled based on project requirements]
- [e.g., Python, MQTT, Raspberry Pi, etc.]

## Project Conventions

### Change Numbering Convention
**CRITICAL**: All change IDs MUST follow this numbering format:
- Format: `{number}-{description}`
- Number format: Two digits with leading zero (01, 02, 03, etc.)
- Auto-increment: Each new change increments from the last used number
- Description: Kebab-case, verb-led (add-, update-, remove-, refactor-)

**Examples:**
- ✅ `01-add-sensor-integration`
- ✅ `02-update-mqtt-protocol`
- ✅ `03-remove-legacy-api`
- ❌ `add-sensor-integration` (missing number)
- ❌ `1-add-sensor` (single digit, needs 01)

**How to find the next number:**
1. Run `openspec list` to see active changes
2. Check `openspec/changes/archive/` for completed changes
3. Use the highest number + 1

### Code Style
[To be defined based on chosen tech stack]

### Architecture Patterns
[To be documented as project develops]

### Testing Strategy
[To be defined based on project requirements]

### Git Workflow
[To be defined based on team/course requirements]

## Domain Context
AIoT project focusing on integrating AI capabilities with IoT devices and systems.

## Important Constraints
- Academic project with course-specific requirements
- Must follow the auto-incrementing change numbering convention above

## External Dependencies
[To be documented as external services/APIs are integrated]
