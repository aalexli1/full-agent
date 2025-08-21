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
- **Match the codebase** – Study existing patterns, use current libraries, follow established style and best practices
- **Protect the workspace** – Never delete memory files, always leave resumable state, test changes when possible

### Simplicity Means

- One clear objective per workspace
- Memory files as the single source of truth
- Filesystem state over complex abstractions
- Clear handoffs when delegating to sub-agents

## Process

### 1. Starting Work

When beginning any task:
1. Read `core/objective.md` to understand the goal
2. Check `current/progress.md` for what's been done (detailed history)
3. Check `current/working-on.md` for planned tasks and next steps
4. Review `learned/` for relevant patterns and `core/architecture.md` for design decisions

### 2. Memory Update Protocol

**Update memory to maintain resumable state:**
- **Planning tasks**: Write future work and next steps to `working-on.md` (your todo list)
- **Making progress**: Update `progress.md` with detailed record of what you did (your work log)
- **Making architectural decisions**: Document in `core/architecture.md` with rationale
- **Discovering patterns**: Always record in `learned/patterns.md` (e.g., solved errors, code conventions, new solutions)
- **Getting stuck**: Write full context to `blocked.md`
- **Completing objective**: Summary in `complete.md`

### 3. When Stuck

1. **Document** – Write error details to `blocked.md`:
   - What you tried
   - Error messages/logs
   - Why it failed
   
2. **Check patterns** – Review `learned/patterns.md` for similar issues

3. **Try alternatives** – Different approaches, document attempts

4. **Delegate if needed** – Create handoff in `.memory/handoffs/` for sub-agent when stuck or need different expertise

## Implementation Flow

### Breaking Down Objectives

Break complex objectives into clear stages that build on each other. Document your plan in `working-on.md` so you can track progress and resume if interrupted.

### Decision Framework

Choose solutions that are simple, resumable, and well-documented in memory.

## Sub-Agent Delegation

### When to Use Task Tool

Delegate to specialized agents when you need different expertise, are switching domains, or want to explore multiple approaches in parallel. Handle tasks yourself when you have a clear path forward.

### Handoff Protocol

When delegating:
1. Create detailed handoff in `.memory/handoffs/[task-name].md` with enough context for autonomous execution
2. Include: specific objective, full context, constraints, expected output format
3. Check for response in same location
4. Integrate results into main workspace

## Quality Checkpoints

### Before Marking Complete

Ensure the objective is achieved and the work is documented in memory for future sessions.

### Completion Report

Write a summary to `complete.md` explaining what was accomplished and any important context for future work.

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
    │   └── architecture.md   # System design and major architectural decisions
    ├── learned/              # Accumulated knowledge
    │   ├── patterns.md       # Reusable solutions and code conventions
    │   └── dependencies.md   # External requirements
    ├── current/              # Active state
    │   ├── working-on.md     # Todo list and planned tasks
    │   ├── progress.md       # Detailed work log and state
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


