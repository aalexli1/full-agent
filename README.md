# Full Agent - Autonomous Claude Code System

A minimal, powerful system for running fully autonomous AI agents using Claude Code.

## Overview

Full Agent launches Claude Code with a single objective and lets it run autonomously until completion. It uses a filesystem-based memory system for persistence and can spawn specialized sub-agents as needed.

## Quick Start

```bash
# Run with an objective
python agent.py "Build a calculator web app"

# Run with an objective file
python agent.py examples/calculator.md

# Resume from saved state
python agent.py --resume

# Run with timeout
python agent.py "Build feature X" --timeout 3600
```

## How It Works

1. **Launch**: You provide an objective
2. **Autonomous Execution**: Claude Code works independently
3. **Memory Persistence**: Progress saved to `.memory/` directory
4. **Specialist Delegation**: Spawns sub-agents when needed
5. **Completion**: Continues until objective is complete

## Memory System

The `.memory/` directory serves as the agent's persistent brain:

```
.memory/
├── core/           # Unchanging facts
│   ├── objective.md
│   └── architecture.md
├── learned/        # Discovered knowledge
│   ├── patterns.md
│   ├── decisions.md
│   └── dependencies.md
├── current/        # Active state
│   ├── working-on.md
│   ├── blocked.md
│   └── progress.md
└── handoffs/       # Inter-agent communication
```

## Features

- **True Autonomy**: Runs until objective is complete
- **Resumable**: Can stop and resume from saved state
- **Self-Organizing**: Spawns specialists as needed
- **Self-Documenting**: Updates memory as it works
- **User Communication**: Creates GitHub issues when blocked

## Architecture

The system is intentionally minimal:
- `agent.py` - Launcher script (~150 lines)
- `.memory/` - Filesystem-based memory
- Claude Code - Does all the actual work

## Sub-Agent Communication

The main agent can spawn specialists using Claude Code's Task tool:

```python
# Main agent writes context
Write(".memory/handoffs/to-frontend.md", task_details)

# Spawns specialist
Task(prompt="Read .memory/handoffs/to-frontend.md and execute")

# Specialist writes results
Write(".memory/handoffs/from-frontend.md", results)

# Main agent continues with results
```

## Example Objectives

See the `examples/` directory for sample objectives:
- `calculator.md` - Build a calculator web app
- `twitter-clone.md` - Build a Twitter clone

## Requirements

- Python 3.7+
- Claude Code CLI (`claude-code` command)
- Git (for memory versioning)

## Advanced Usage

### Custom Memory Location
```bash
MEMORY_DIR=/path/to/memory python agent.py "objective"
```

### Watch Progress
```bash
# In another terminal
watch cat .memory/current/progress.md
```

### Monitor Blockers
```bash
tail -f .memory/current/blocked.md
```

## How It's Different

Unlike traditional AI coding assistants:
- **No conversation needed** - Just state the objective
- **Truly autonomous** - Continues working without prompts
- **Handles complexity** - Breaks down and delegates work
- **Learns and adapts** - Builds memory of patterns
- **Survives interruption** - Can resume from saved state

## Limitations

- Requires Claude Code CLI installed
- Memory grows over time (periodic cleanup may be needed)
- Complex objectives may hit token limits
- User intervention needed for credentials/API keys

## Contributing

This is an experimental system. Contributions and feedback welcome!

## License

MIT