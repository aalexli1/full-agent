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

def ensure_memory_structure():
    """Ensure memory directory structure exists"""
    memory_dirs = [
        ".memory/core",
        ".memory/learned", 
        ".memory/current",
        ".memory/handoffs"
    ]
    for dir_path in memory_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)

def load_objective(objective_path):
    """Load objective from file or string"""
    if os.path.isfile(objective_path):
        with open(objective_path) as f:
            return f.read().strip()
    return objective_path

def create_master_prompt(objective, resume=False):
    """Generate the master prompt for Claude"""
    if resume:
        resume_context = """
You are resuming work on an objective. First, read the memory files to understand:
- .memory/core/objective.md - The main goal
- .memory/current/progress.md - What's been done
- .memory/current/working-on.md - What was in progress
- .memory/current/blocked.md - Any blockers

Then continue working toward completion.
"""
    else:
        resume_context = f"""
You are starting fresh on this objective:
{objective}

First, write this objective to .memory/core/objective.md for future reference.
"""
    
    return f"""You are an autonomous agent with a specific objective to complete.

{resume_context}

## Your Capabilities

1. **Direct work**: You can implement solutions directly
2. **Spawn specialists**: Use the Task tool to spawn sub-agents for specific expertise
3. **Memory management**: Read/write to .memory/ for persistent context
4. **User communication**: Create GitHub issues when truly blocked

## Memory System

The .memory/ directory is your persistent brain:
- .memory/core/ - Unchanging facts (objective, architecture)
- .memory/learned/ - Patterns and decisions you discover
- .memory/current/ - Your active state and progress
- .memory/handoffs/ - Communication with sub-agents

ALWAYS update these files as you work so you can resume if interrupted.

## Working with Sub-Agents

When you need specialist help:
1. Write context to .memory/handoffs/to-[specialist].md
2. Spawn with: Task(prompt="Read .memory/handoffs/to-[specialist].md and execute")
3. Sub-agent will write results to .memory/handoffs/from-[specialist].md
4. Read results and continue

## Progress Tracking

Regularly update:
- .memory/current/progress.md - Overall progress percentage and summary
- .memory/current/working-on.md - Current focus
- .memory/learned/patterns.md - Discovered patterns
- .memory/learned/decisions.md - Key decisions and rationale

## Completion

Continue working until the objective is fully complete.
When done, write a final summary to .memory/current/complete.md

If truly blocked:
1. Document the blocker in .memory/current/blocked.md
2. Create a GitHub issue if it requires user intervention
3. Work on other aspects if possible

Remember: You are autonomous. Make decisions, implement solutions, and complete the objective."""

def run_agent(objective, resume=False, timeout=None):
    """Launch Claude Code with the objective"""
    ensure_memory_structure()
    
    # Generate master prompt
    prompt = create_master_prompt(objective, resume)
    
    # Build command
    cmd = ["claude-code", "--no-interactive", prompt]
    
    print(f"🚀 Launching autonomous agent...")
    print(f"📍 Objective: {objective[:100]}..." if len(objective) > 100 else f"📍 Objective: {objective}")
    print(f"💾 Memory at: .memory/")
    print("-" * 50)
    
    try:
        # Run Claude Code
        result = subprocess.run(cmd, timeout=timeout)
        
        if result.returncode == 0:
            print("\n✅ Agent completed successfully")
            
            # Check if complete
            if Path(".memory/current/complete.md").exists():
                print("📄 Reading completion report...")
                with open(".memory/current/complete.md") as f:
                    print(f.read())
        else:
            print(f"\n⚠️ Agent exited with code {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print(f"\n⏱️ Agent timeout after {timeout} seconds")
        print("💾 State saved to .memory/ - use --resume to continue")
    except KeyboardInterrupt:
        print("\n⚠️ Agent interrupted")
        print("💾 State saved to .memory/ - use --resume to continue")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

def main():
    parser = argparse.ArgumentParser(description="Launch an autonomous Claude agent")
    parser.add_argument("objective", nargs="?", help="Objective to complete (string or file path)")
    parser.add_argument("--resume", action="store_true", help="Resume from saved state")
    parser.add_argument("--timeout", type=int, help="Timeout in seconds")
    
    args = parser.parse_args()
    
    if args.resume:
        if not Path(".memory/core/objective.md").exists():
            print("❌ No saved state found. Start fresh with an objective.")
            return 1
        objective = "Resuming from saved state"
    elif args.objective:
        objective = load_objective(args.objective)
    else:
        print("❌ Provide an objective or use --resume")
        parser.print_help()
        return 1
    
    return run_agent(objective, args.resume, args.timeout)

if __name__ == "__main__":
    sys.exit(main())