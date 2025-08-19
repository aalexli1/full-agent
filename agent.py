#!/usr/bin/env python3
"""
Full Agent - Minimal autonomous agent launcher using Claude Code
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import argparse
import re

def ensure_memory_structure(workspace_dir):
    """Ensure memory directory structure exists in workspace"""
    memory_dirs = [
        f"{workspace_dir}/.memory/core",
        f"{workspace_dir}/.memory/learned", 
        f"{workspace_dir}/.memory/current",
        f"{workspace_dir}/.memory/handoffs"
    ]
    for dir_path in memory_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def load_objective(objective_path):
    """Load objective from file or string"""
    # First check if it's a file relative to current directory
    if os.path.isfile(objective_path):
        with open(objective_path) as f:
            return f.read().strip()
    
    # Check if it's a file relative to agent root
    agent_root = get_agent_root()
    agent_relative_path = agent_root / objective_path
    if agent_relative_path.is_file():
        with open(agent_relative_path) as f:
            return f.read().strip()
    
    # Otherwise treat as literal objective string
    return objective_path

def create_master_prompt(objective, workspace_dir, resume=False):
    """Generate the master prompt for Claude"""
    if resume:
        resume_context = f"""
You are resuming work on an objective. Your workspace is: {workspace_dir}

First, read the memory files to understand:
- {workspace_dir}/.memory/core/objective.md - The main goal
- {workspace_dir}/.memory/current/progress.md - What's been done
- {workspace_dir}/.memory/current/working-on.md - What was in progress
- {workspace_dir}/.memory/current/blocked.md - Any blockers

Then continue working toward completion.
"""
    else:
        resume_context = f"""
You are starting fresh on this objective:
{objective}

Your workspace directory is: {workspace_dir}
All your work should be done within this directory.

First, write this objective to {workspace_dir}/.memory/core/objective.md for future reference.
"""
    
    return f"""You are an autonomous agent with a specific objective to complete.

{resume_context}

## CRITICAL: Always Start in Plan Mode

YOU MUST BEGIN BY:
1. **Enter plan mode** to think through the objective thoroughly
2. **Create a comprehensive plan** breaking down the objective into clear steps
3. **Use TodoWrite** to create a task list from your plan
4. **Critique your plan by asking**:
   - Is there a simpler approach I'm overlooking?
   - What could go wrong with this approach?
   - Are there dependencies I haven't considered?
   - Which tasks can be delegated to sub-agents?
   - Is the order optimal or are there parallelization opportunities?
   - Have I broken down tasks small enough to track progress?
5. **Revise plan and todos** based on your critique
6. **Only then use ExitPlanMode** to begin implementation

This ensures you think before acting and maintain clear task tracking throughout.

## Your Capabilities

1. **Planning & Tracking**: Use TodoWrite to manage tasks, ExitPlanMode when ready to implement
2. **Direct work**: You can implement solutions directly
3. **Spawn specialists**: Use the Task tool to spawn sub-agents for specific expertise
4. **Memory management**: Read/write to .memory/ for persistent context
5. **User communication**: Create GitHub issues when truly blocked

## Memory System

The {workspace_dir}/.memory/ directory is your persistent brain:
- {workspace_dir}/.memory/core/ - Unchanging facts (objective, architecture)
- {workspace_dir}/.memory/learned/ - Patterns and decisions you discover
- {workspace_dir}/.memory/current/ - Your active state and progress
- {workspace_dir}/.memory/handoffs/ - Communication with sub-agents

ALWAYS update these files as you work so you can resume if interrupted.

## CRITICAL: Context Management Strategy

To maximize efficiency and minimize context usage, you MUST proactively delegate tasks to sub-agents.
Your role is to be a coordinator/architect who:
1. Plans the high-level approach
2. Delegates implementation details to specialists
3. Integrates results without needing to see the implementation

### When to Spawn Sub-Agents (ALWAYS do this for):
- **Research tasks**: "Research existing patterns for X" → Let sub-agent explore and summarize
- **Implementation tasks**: "Implement feature Y" → Let sub-agent handle the details
- **Debugging/fixes**: "Fix the bug in Z" → Let sub-agent investigate and fix
- **File operations**: "Update all files matching pattern" → Let sub-agent do the work
- **Testing**: "Write and run tests" → Let sub-agent handle test creation/execution
- **Documentation**: "Document the API" → Let sub-agent write docs

You should spawn sub-agents EARLY and OFTEN. Don't wait until you're blocked.
Each sub-agent reduces your context by 80-90% since you only see their summary.

## Working with Sub-Agents

For EVERY substantial task:
1. **Mark task as in_progress** in your TodoWrite list
2. Write detailed instructions to {workspace_dir}/.memory/handoffs/to-[specialist].md
3. Spawn with: Task(
     description="[Short task name]",
     prompt="You are a specialist sub-agent. ALWAYS START IN PLAN MODE: 1) Think through the task, 2) Create a plan with TodoWrite, 3) Critique your plan, 4) Use ExitPlanMode to begin. Work in {workspace_dir}. Read {workspace_dir}/.memory/handoffs/to-[specialist].md for your task. Write summary to {workspace_dir}/.memory/handoffs/from-[specialist].md when complete. IMPORTANT: You should also delegate to sub-agents when appropriate - if you don't need implementation details for a subtask, spawn another agent to handle it and just read their summary.",
     subagent_type="general-purpose"
   )
4. Sub-agent writes results to {workspace_dir}/.memory/handoffs/from-[specialist].md
5. **Mark task as completed** in your TodoWrite list after reading results
6. You read ONLY the summary, not the implementation details

Sub-agents can spawn their own sub-agents! This creates efficient delegation chains where each agent only holds the context it needs. For example:
- Main agent → Feature agent (coordinates feature) → Implementation agents (handle specific files)
- Main agent → Research agent (explores codebase) → Pattern analysis agent (analyzes findings)

## Task Management Best Practices

1. **Use TodoWrite religiously** - Every task should be tracked
2. **One task in_progress at a time** - Focus and complete before moving on
3. **Update status immediately** - Mark completed as soon as done
4. **Delegate tasks should be todos** - Each sub-agent spawn should have a corresponding todo
5. **Review and update plan** - If blocked or plan changes, update todos accordingly

## Progress Tracking

Regularly update BOTH:

**TodoWrite** (for immediate task tracking):
- Current task statuses
- What's blocked
- What's delegated

**Memory files** (for persistence):
- {workspace_dir}/.memory/current/progress.md - Overall progress percentage and summary
- {workspace_dir}/.memory/current/working-on.md - Current focus
- {workspace_dir}/.memory/learned/patterns.md - Discovered patterns
- {workspace_dir}/.memory/learned/decisions.md - Key decisions and rationale

## Completion

Continue working until the objective is fully complete.
When done, write a final summary to {workspace_dir}/.memory/current/complete.md

If truly blocked:
1. Document the blocker in {workspace_dir}/.memory/current/blocked.md
2. Create a GitHub issue if it requires user intervention
3. Work on other aspects if possible

Remember: You are autonomous. Make decisions, implement solutions, and complete the objective."""

def sanitize_name(name):
    """Convert objective to safe directory name"""
    # Take first 50 chars, remove special characters
    safe_name = re.sub(r'[^a-zA-Z0-9-_]', '_', name[:50])
    return safe_name.lower().strip('_')

def get_default_workspace_base():
    """Get the default workspace base directory"""
    # Check for environment variable first
    if "FULL_AGENT_WORKSPACE" in os.environ:
        return Path(os.environ["FULL_AGENT_WORKSPACE"]).absolute()
    
    # Use ~/full-agent-workspace as default to avoid polluting the repo
    return Path.home() / "full-agent-workspace"

def get_agent_root():
    """Get the root directory where agent.py lives"""
    return Path(__file__).parent.absolute()

def run_agent(objective, workspace=None, resume=False, timeout=None):
    """Launch Claude Code with the objective"""
    # Determine workspace directory
    if workspace:
        # If absolute path given, use it; otherwise relative to current directory
        workspace_path = Path(workspace)
        if workspace_path.is_absolute():
            workspace_dir = workspace_path
        else:
            workspace_dir = Path.cwd() / workspace
    elif resume:
        # Find existing workspace with saved state
        workspace_base = get_default_workspace_base()
        if workspace_base.exists():
            for dir in workspace_base.iterdir():
                if (dir / ".memory" / "core" / "objective.md").exists():
                    workspace_dir = dir.absolute()
                    break
            else:
                print("❌ No saved state found. Specify workspace with --workspace")
                return 1
        else:
            print("❌ No workspace directory found")
            return 1
    else:
        # Create new workspace based on objective
        workspace_base = get_default_workspace_base()
        workspace_base.mkdir(exist_ok=True)
        
        # Generate workspace name from objective
        workspace_name = sanitize_name(objective)
        workspace_dir = workspace_base / workspace_name
        
        # Add timestamp if directory exists
        if workspace_dir.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            workspace_dir = workspace_base / f"{workspace_name}_{timestamp}"
        
        workspace_dir.mkdir(parents=True, exist_ok=True)
    
    # Ensure memory structure exists
    ensure_memory_structure(workspace_dir)
    
    # Generate master prompt
    prompt = create_master_prompt(objective, str(workspace_dir), resume)
    
    # Build command - run in workspace directory
    # --print for non-interactive mode
    # --dangerously-skip-permissions to allow all operations without prompting
    cmd = ["claude", "--print", "--dangerously-skip-permissions", prompt]
    
    print(f"🚀 Launching autonomous agent...")
    print(f"📍 Objective: {objective[:100]}..." if len(objective) > 100 else f"📍 Objective: {objective}")
    print(f"📂 Workspace: {workspace_dir}")
    print(f"💾 Memory at: {workspace_dir}/.memory/")
    print("-" * 50)
    
    try:
        # Run Claude Code
        result = subprocess.run(cmd, timeout=timeout)
        
        if result.returncode == 0:
            print("\n✅ Agent completed successfully")
            
            # Check if complete
            complete_path = workspace_dir / ".memory" / "current" / "complete.md"
            if complete_path.exists():
                print("📄 Reading completion report...")
                with open(complete_path) as f:
                    print(f.read())
        else:
            print(f"\n⚠️ Agent exited with code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"\n⏱️ Agent timeout after {timeout} seconds")
        print(f"💾 State saved to {workspace_dir}/.memory/ - use --resume to continue")
    except KeyboardInterrupt:
        print("\n⚠️ Agent interrupted")
        print(f"💾 State saved to {workspace_dir}/.memory/ - use --resume to continue")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

def main():
    parser = argparse.ArgumentParser(description="Launch an autonomous Claude agent")
    parser.add_argument("objective", nargs="?", help="Objective to complete (string or file path)")
    parser.add_argument("--workspace", "-w", help="Workspace directory for this task")
    parser.add_argument("--resume", action="store_true", help="Resume from saved state")
    parser.add_argument("--timeout", type=int, help="Timeout in seconds")
    parser.add_argument("--list", action="store_true", help="List existing workspaces")
    
    args = parser.parse_args()
    
    # List workspaces if requested
    if args.list:
        workspace_base = get_default_workspace_base()
        if workspace_base.exists():
            print("📂 Existing workspaces:")
            for dir in sorted(workspace_base.iterdir()):
                if dir.is_dir():
                    obj_file = dir / ".memory" / "core" / "objective.md"
                    if obj_file.exists():
                        with open(obj_file) as f:
                            obj = f.readline().strip()[:50]
                        print(f"  • {dir.name}: {obj}...")
                    else:
                        print(f"  • {dir.name}: (no objective)")
        else:
            print("No workspaces found")
        return 0
    
    if args.resume:
        objective = "Resuming from saved state"
    elif args.objective:
        objective = load_objective(args.objective)
    else:
        print("❌ Provide an objective or use --resume")
        parser.print_help()
        return 1
    
    return run_agent(objective, args.workspace, args.resume, args.timeout)

if __name__ == "__main__":
    sys.exit(main())