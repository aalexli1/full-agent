# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Full Agent is a minimal system for running autonomous AI agents using Claude Code. It launches Claude with a single objective and lets it run autonomously using a filesystem-based memory system.

## Key Commands

### Running the Agent
```bash
# Launch with an objective (creates workspace in ~/full-agent-workspace/)
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
Each workspace contains a `.memory/` directory:
- **core/**: Unchanging facts (objective.md, architecture.md)
- **learned/**: Discovered patterns and decisions (patterns.md, decisions.md, dependencies.md)
- **current/**: Active state (working-on.md, blocked.md, progress.md, complete.md)
- **handoffs/**: Inter-agent communication for sub-agent delegation

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
4. **Sub-agents**: Main agent can spawn specialists via Task tool, communicating through `.memory/handoffs/`
5. **Completion**: Agent writes to `.memory/current/complete.md` when objective is achieved

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
- Memory templates in `memory_templates.py` are currently unused but available

### When Running as an Agent
- Always work within the assigned workspace directory
- Update memory files regularly for persistence
- Use `.memory/handoffs/` for sub-agent communication
- Write completion report to `.memory/current/complete.md` when done
- Document blockers in `.memory/current/blocked.md` if stuck