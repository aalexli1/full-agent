# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Full Agent is a minimal system for running autonomous AI agents using Claude Code. It launches Claude with a single objective and lets it run autonomously using a filesystem-based memory system.

## Philosophy

### Core Principles

- **Memory over context** – Update `.memory/` before losing context or switching tasks
- **Progress over perfection** – Document partial work to enable resumption
- **Explicit over implicit** – Record decisions and patterns in memory for future sessions
- **Fail loudly, recover gracefully** – Document blockers immediately, then try alternatives
- **Small steps, clear traces** – Break work into memory-tracked stages that build on each other

### Simplicity Means

- One clear objective per workspace
- Memory files as the single source of truth
- Filesystem state over complex abstractions
- Clear handoffs when delegating to sub-agents

## Process

### 1. Starting Work

When beginning any task:
1. Read `core/objective.md` to understand the goal
2. Check `current/progress.md` for existing work
3. Review `learned/` for relevant patterns and decisions
4. Break objective into 3-5 stages in `working-on.md`

### 2. Memory Update Protocol

**Update memory at these triggers:**
- **Starting work**: Write current focus to `working-on.md`
- **Every ~10 minutes**: Update `progress.md` with accomplishments
- **Making decisions**: Document in `learned/decisions.md` with rationale
- **Finding patterns**: Record in `learned/patterns.md` for reuse
- **Getting stuck**: Write full context to `blocked.md`
- **Completing objective**: Summary in `complete.md`

### 3. When Stuck (Max 3 Attempts)

1. **Document** – Write error details to `blocked.md`:
   - What you tried
   - Error messages/logs
   - Why it failed
   
2. **Check patterns** – Review `learned/patterns.md` for similar issues

3. **Try alternative** – Different approach, document attempt

4. **Delegate if needed** – Create handoff in `.memory/handoffs/` for sub-agent

## Implementation Flow

### Breaking Down Objectives

Every objective should be decomposed into stages:

```markdown
## Stage 1: [Setup/Foundation]
**Goal**: [Specific deliverable]
**Success**: [Clear criteria]
**Memory Updates**: [Which files to update]

## Stage 2: [Core Implementation]
**Goal**: [Building on Stage 1]
**Success**: [Measurable outcome]
**Memory Updates**: [Progress tracking]
```

### Decision Framework

When multiple solutions exist, prioritize:

1. **Resumability** – Can another session continue from here?
2. **Clarity** – Will the memory files explain what happened?
3. **Simplicity** – Is this the least complex working solution?
4. **Patterns** – Does this match existing patterns in `learned/`?
5. **Reversibility** – Can we easily try something else if this fails?

## Sub-Agent Delegation

### When to Use Task Tool

**Delegate when:**
- Switching domains (e.g., backend → frontend)
- Need specialized expertise
- Current approach failed 3 times
- Task requires different workspace
- Exploring multiple solutions in parallel

**Do it yourself when:**
- Clear path forward exists
- Following established patterns
- Simple file operations
- Within current domain/context

### Handoff Protocol

When delegating:
1. Create clear handoff in `.memory/handoffs/[task-name].md`
2. Include: objective, context, constraints, expected output
3. Check for response in same location
4. Integrate results into main workspace

## Quality Checkpoints

### Before Marking Complete

Verify:
- ✓ Objective achieved (compare to `core/objective.md`)
- ✓ Progress documented (check `current/progress.md`)
- ✓ Decisions recorded (check `learned/decisions.md`)
- ✓ Resumable state (sufficient context in memory)
- ✓ Tests pass (if applicable to project)
- ✓ No blocking errors in `blocked.md`

### Completion Report

Write to `complete.md`:
- What was accomplished
- Key decisions made
- Patterns discovered
- Any remaining limitations
- How to extend/improve

## Key Commands

### Running the Agent
```bash
# Launch with objective (creates workspace in ~/full-agent-workspace/)
python agent.py "Build a calculator web app"

# Launch with objective file
python agent.py examples/calculator.md

# Resume from saved state
python agent.py --resume
python agent.py --resume --workspace workspace/calculator

# List existing workspaces
python agent.py --list

# Run with timeout (seconds)
python agent.py "Build feature X" --timeout 3600
```

### Python Environment
- Python 3.7+ required
- Minimal dependencies: only `python-dotenv` for environment variables
- No test framework configured - agent should determine testing approach per project

## Architecture

### Core Components
- **agent.py**: Main launcher script that creates workspaces and invokes Claude Code with autonomous instructions
- **.memory/**: Persistent filesystem-based memory for each workspace
- **workspace management**: By default creates workspaces in `~/full-agent-workspace/` to keep the repo clean

### Memory System Structure
```
workspace/
└── .memory/
    ├── core/                 # Unchanging facts
    │   ├── objective.md      # Original goal
    │   └── architecture.md   # System design decisions
    ├── learned/              # Accumulated knowledge
    │   ├── patterns.md       # Reusable solutions
    │   ├── decisions.md      # Architectural choices
    │   └── dependencies.md   # External requirements
    ├── current/              # Active state
    │   ├── working-on.md     # Current focus
    │   ├── progress.md       # Completed stages
    │   ├── blocked.md        # Current blockers
    │   └── complete.md       # Final report
    └── handoffs/             # Sub-agent communication
        └── [task-name].md    # Delegation requests/responses
```

### Workspace Organization
```
~/full-agent-workspace/        # Default location (configurable via FULL_AGENT_WORKSPACE env var)
├── calculator/                 # Task-specific workspace
│   ├── .memory/               # Persistent memory for this task
│   └── [implementation files]
└── [other workspaces]
```

### How the Agent Works

1. **Launch**: `agent.py` creates workspace and generates master prompt with autonomous instructions
2. **Execution**: Claude Code runs with `--print --dangerously-skip-permissions` flags for non-interactive mode
3. **Memory**: Agent reads/writes to `.memory/` for persistence across sessions
4. **Sub-agents**: Main agent spawns specialists via Task tool, communicating through `.memory/handoffs/`
5. **Completion**: Agent writes final report to `.memory/current/complete.md` when objective is achieved

### Key Implementation Details
- Workspace names are sanitized from objectives (first 50 chars, alphanumeric)
- Timestamps added if workspace name already exists
- Memory structure is created automatically via `ensure_memory_structure()`
- Agent runs in the workspace directory, not the repo directory
- Resume functionality checks for existing `.memory/core/objective.md` files

## Development Notes

### When Working on the Agent System
- The agent launcher is intentionally minimal (~260 lines)
- No complex state management - all state is in filesystem
- Claude CLI does all the heavy lifting for code operations

### When Running as an Agent
- Always work within the assigned workspace directory
- Update memory files regularly for persistence
- Document decisions with rationale
- Test changes when possible
- Leave resumable state

### Error Recovery
- Always document failures before trying alternatives
- Check memory for similar past issues
- After 3 attempts, consider different approach
- Use sub-agents for specialized domains

### Working with Existing Code
- Study patterns in codebase before implementing
- Follow existing conventions and style
- Use same libraries and frameworks
- Document any new patterns in `learned/patterns.md`

### Important Reminders

**ALWAYS:**
- Work within assigned workspace directory
- Update memory before context expires
- Document decisions with rationale
- Test changes when possible
- Leave resumable state

**NEVER:**
- Skip memory updates when stuck
- Implement without checking existing patterns
- Leave workspace in broken state
- Ignore repeated failures
- Delete memory files