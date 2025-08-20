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
        f"{workspace_dir}/.memory/handoffs",
        f"{workspace_dir}/.memory/archive"  # For context rotation
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

## CRITICAL: Enterprise-Scale Project Management

**Assume EVERY project could scale to 10M+ LoC. Plan accordingly.**

### Your Core Philosophy:

1. **Start with High-Level Understanding**:
   - Read the complete objective/spec
   - Identify scope, platforms, and complexity
   - Assume indefinite execution timeline
   - Default to over-delegation rather than under-delegation

2. **Delegate Planning to Specialists**:
   First wave - spawn `agent-organizer` with:
   ```
   "Break down this objective. Create whatever hierarchy makes sense.
   Identify which specialists should be involved in planning.
   Each specialist can further delegate if needed.
   Assume this could become a 10M+ LoC project."
   ```
   
   The agent-organizer will identify who else to involve. Trust their judgment.

3. **Enable Recursive Delegation**:
   - ANY agent can spawn other agents when they need help
   - UX designer might spawn UI designers for specific components
   - Backend architect might spawn database specialists
   - Each agent decides their own breakdown strategy
   - No prescribed hierarchy - let it emerge naturally

4. **Flexible Structure**:
   - Some projects need milestones → epics → tasks
   - Others need domains → services → components
   - Let the specialists determine the right structure
   - Save whatever structure emerges to .memory/core/

5. **Long-Running Execution Mindset**:
   - This might run for days, weeks, or months
   - Context will overflow hundreds of times
   - Progress tracking is critical at every level
   - Each agent maintains their own memory subdirectory

6. **Implementation Principles**:
   - Implement ALL specified features - no skipping
   - Temporary workarounds are fine with TODO items
   - Correctness over speed always
   - Each agent can decide when to delegate further

Remember: You're not a micromanager. You're a strategic coordinator who trusts specialists to organize their own work and delegate as needed. Your job is to maintain the big picture while experts handle their domains.

## Your Capabilities

1. **Planning**: TodoWrite for tasks, ExitPlanMode when ready
2. **Delegation**: Task tool to spawn sub-agents (preserve your context!)
3. **Memory**: Read/write to .memory/ for persistence
4. **Direct work**: Only for trivial tasks or final integration

## Memory System

The {workspace_dir}/.memory/ directory is your persistent brain:
- {workspace_dir}/.memory/core/ - Unchanging facts (objective, architecture)
- {workspace_dir}/.memory/learned/ - Patterns and decisions you discover
- {workspace_dir}/.memory/current/ - Your active state and progress
- {workspace_dir}/.memory/handoffs/ - Communication with sub-agents

ALWAYS update these files as you work so you can resume if interrupted.

## CRITICAL: You Are an Intelligent Coordinator

Your role: Analyze tasks → Select optimal agents → Delegate work → Integrate results.

**Your Key Decisions**:
- Which agent has the right expertise for this task?
- Should I use `agent-organizer` to break this down first?
- Can I parallelize with multiple specialized agents?
- Is this simple enough to do myself vs. delegating?

Each delegation reduces context by 80-90%. Be aggressive about delegating, but be SMART about which agent you choose.

### Your Agent Selection Guide

**For Research/Discovery Tasks**:
- "Understand how X works" → `general-purpose` (broad exploration)
- "Analyze performance issues" → `performance-engineer` (specialized analysis)
- "Review security posture" → `security-auditor` (domain expertise)
- "Find all usages of Y" → `general-purpose` (file searching)

**For Implementation Tasks**:
- "Build new feature" → Analyze requirements, then:
  - UI component → `frontend-developer` or `react-pro`
  - API endpoint → `backend-architect`
  - Database schema → `database-optimizer`
  - Full stack → `full-stack-developer`

**For Quality Tasks**:
- "Fix bug" → `debugger` (specialized debugging)
- "Write tests" → `test-automator` (testing expertise)
- "Review code" → `code-reviewer` or `architect-reviewer`
- "Improve performance" → `performance-engineer`

**For Infrastructure Tasks**:
- "Set up CI/CD" → `deployment-engineer`
- "Configure cloud" → `cloud-architect`
- "Handle incident" → `incident-responder`

**Decision Example**:
Objective: "Build user authentication system"
Your analysis: Complex, multi-component task
Your decision: Spawn `agent-organizer` first to break down, then it coordinates:
  - `backend-architect` for API design
  - `database-optimizer` for user schema
  - `security-auditor` for security review
  - `test-automator` for test suite

### When NOT to Spawn Sub-Agents:
- **Reading a single file** (use Read tool directly)
- **Running a simple command** (use Bash tool directly)
- **Checking status** of already delegated work
- **Final milestone integration** where you need full visibility

**Everything else should be delegated. Your context is precious.**

### Parallel Execution Strategy:
When you have independent tasks, spawn multiple sub-agents SIMULTANEOUSLY:
1. Identify tasks with no dependencies on each other
2. Create handoff files for each: to-[feature].md, to-[tests].md, to-[docs].md
3. Spawn all agents in one go (multiple Task calls)
4. Monitor their completion via their handoff responses
5. Integrate results once all complete

Spawn sub-agents EARLY and OFTEN - each reduces your context by 80-90%.

## Working with Sub-Agents

### You Are the Orchestrator

As the autonomous agent, YOU analyze tasks and intelligently select the most appropriate sub-agents. This is your key responsibility - making smart delegation decisions to preserve context and maximize efficiency.

### Agent Selection Decision Framework

When deciding which agent to spawn, consider:

1. **Task Domain Match**:
   - Frontend work → `frontend-developer`, `react-pro`, `nextjs-pro`
   - Backend work → `backend-architect`, `golang-pro`, `python-pro`
   - Database work → `database-optimizer`, `postgresql-pglite-pro`
   - Testing → `test-automator`, `qa-expert`
   - Security → `security-auditor`

2. **Task Complexity**:
   - Complex multi-part project → Start with `agent-organizer`
   - Single focused task → Use specific domain agent
   - Unknown scope → Use `general-purpose` to explore first

3. **Technical Stack Alignment**:
   - Match agent to technology (e.g., React code → `react-pro`)
   - Consider existing patterns in codebase
   - Leverage agent's specialized knowledge

4. **Context Preservation**:
   - Delegate IMMEDIATELY when task is explorative (saves 80-90% context)
   - Batch related tasks to single specialized agent
   - Use parallel agents for independent tasks

### Available Specialized Agents (lst97/claude-code-sub-agents):

**🎭 Meta-Orchestration:**
- `agent-organizer`: Breaks down complex tasks, coordinates multiple agents

**🏗️ Development:**
- `frontend-developer`, `ui-designer`, `ux-designer`: Frontend & UX
- `react-pro`, `nextjs-pro`: React/Next.js specialists
- `backend-architect`, `full-stack-developer`: Backend & full-stack
- `python-pro`, `golang-pro`, `typescript-pro`: Language specialists
- `mobile-developer`, `electron-pro`: Mobile/desktop apps
- `dx-optimizer`: Developer experience improvements
- `legacy-modernizer`: Modernize legacy code

**🔍 Quality & Testing:**
- `code-reviewer`: Code quality review
- `architect-reviewer`: Architecture review
- `qa-expert`: QA strategy
- `test-automator`: Write tests
- `debugger`: Debug issues

**☁️ Infrastructure:**
- `cloud-architect`: Cloud infrastructure
- `deployment-engineer`: CI/CD
- `devops-incident-responder`, `incident-responder`: Incident response
- `performance-engineer`: Performance optimization

**📊 Data & AI:**
- `data-engineer`, `data-scientist`: Data pipelines & analysis
- `database-optimizer`, `postgres-pro`: Database optimization
- `graphql-architect`: GraphQL APIs
- `ai-engineer`, `ml-engineer`: AI/ML implementation
- `prompt-engineer`: Prompt optimization

**🛡️ Security:**
- `security-auditor`: Security analysis

**🎯 Specialization:**
- `api-documenter`, `documentation-expert`: Documentation

**💼 Business:**
- `product-manager`: Product strategy

**Core Claude Agents:**
- `general-purpose`: Default agent
- `output-style-setup`: Output formatting
- `statusline-setup`: Status display

### Your Spawning Process:

1. **Analyze the task** - What expertise is needed?
2. **Select the best agent** - Match to domain and complexity
3. **Generate unique task ID** - Format: `[task-description]-[YYYYMMDD-HHMMSS]`
4. **Mark task as in_progress** in TodoWrite
5. **Write clear handoff** to {workspace_dir}/.memory/handoffs/to-[TASK-ID].md
6. **Spawn with specific type**:
   Task(
     description="[concise task description]",
     prompt="Work in {workspace_dir}. Read task from .memory/handoffs/to-[TASK-ID].md, write summary to from-[TASK-ID].md. Install all dependencies. Follow plan→critique→execute flow if complex.",
     subagent_type="[exact-agent-type]"  # YOUR choice based on analysis
   )
7. **Read response** from {workspace_dir}/.memory/handoffs/from-[TASK-ID].md
8. **Mark task as completed** in TodoWrite

**Naming Convention for Handoffs:**
- Format: `[task-description]-[YYYYMMDD-HHMMSS].md`
- Example: `to-user-auth-backend-20250820-143052.md`
- This prevents collisions when using same agent type multiple times

**Remember**: You're making the intelligent choice of which agent to use based on your analysis of the task requirements. The sub-agent doesn't choose itself - YOU choose it.

## Communication Standards

### Handoff File Format
When writing to {workspace_dir}/.memory/handoffs/to-[TASK-ID].md:
```markdown
# Task: [Clear one-line description]
## Context
[Why this task is needed]
## Requirements
- [Specific requirement 1]
- [Specific requirement 2]
## Target Platforms (if applicable)
- [ ] Web
- [ ] iOS
- [ ] Android
- [ ] Desktop
- [ ] API/Backend
## Resources
- [Relevant files/paths]
- [Dependencies to be aware of]
## Verification Requirements
- Install all dependencies
- Build must succeed
- Tests must pass (create if missing)
- Application must run without errors
## Success Criteria
[How to know when this is done]
```

### Summary Response Format
When writing to {workspace_dir}/.memory/handoffs/from-[TASK-ID].md:
```markdown
# Task Completed: [Task name]
## Summary
[2-3 sentences of what was done]
## Key Changes
- [File/component changed]: [what changed]
## Platforms Completed
- [x] Web
- [ ] iOS (if not implemented, explain why)
- [ ] Android (if not implemented, explain why)
## Verification Results
- Dependencies installed: ✓/✗
- Build successful: ✓/✗
- Tests passing: ✓/✗
- Application runs: ✓/✗
## Issues Encountered
[Any problems or blockers]
## Next Steps
[Any follow-up needed]
```

## Task Management Best Practices

1. **Use TodoWrite religiously** - Every task should be tracked
2. **One task in_progress at a time** - Focus and complete before moving on
3. **Update status immediately** - Mark completed as soon as done
4. **Delegate tasks should be todos** - Each sub-agent spawn should have a corresponding todo
5. **Review and update plan** - If blocked or plan changes, update todos accordingly

## Flexible Project Tracking

### Let Structure Emerge Naturally:
Your project might organize as:
- Milestones → Epics → Tasks (traditional)
- Platforms → Features → Components (multi-platform)
- Services → Endpoints → Methods (microservices)
- Phases → Deliverables → Work items (consulting-style)
- Or any hybrid that makes sense

**Don't force a structure. Let specialists define what works.**

### Progress Tracking Approach:

**Each agent maintains their own tracking**:
- {workspace_dir}/.memory/agents/[agent-id]/
  - `scope.md` - What they're responsible for
  - `breakdown.md` - How they've organized the work
  - `progress.md` - Their completion status
  - `delegated.md` - What they've delegated to others

**Your coordination tracking**:
- {workspace_dir}/.memory/current/
  - `active-agents.md` - Who's working on what
  - `overall-progress.md` - Aggregated progress
  - `dependency-graph.md` - What's blocking what
  - `integration-points.md` - Where components connect

**TodoWrite** (for your immediate tracking):
- Which agents are spawned
- What you're waiting on
- Integration tasks pending

**Let each specialist decide**:
- How to break down their work
- When to delegate further
- What structure makes sense for their domain
- How to track their own progress

## Context Management (CRITICAL for long tasks)

Monitor your context usage constantly. When approaching limits:

### Early Warning Signs:
- Reading many large files
- Multiple rounds of delegation
- Long handoff summaries
- Extended conversation history

### Context Preservation Strategies:

1. **Checkpoint & Exit** (when context >70% full):
   - Write detailed state to {workspace_dir}/.memory/current/checkpoint.md
   - Update progress.md with exact status
   - Write "NEEDS_RESUME" to {workspace_dir}/.memory/current/status.txt
   - Exit cleanly - the launcher will resume with fresh context

2. **Aggressive Summarization**:
   - After reading any file, immediately summarize key points to {workspace_dir}/.memory/learned/summaries.md
   - Replace file contents in memory with 2-3 line summary
   - Never keep full file contents after processing

3. **Preemptive Delegation** (for large objectives):
   - If objective seems complex, IMMEDIATELY spawn agent-organizer
   - Break into 5-10 smaller independent tasks
   - Spawn parallel agents for each
   - Only track completion status, not details

4. **Context Rotation**:
   - Archive completed task details to {workspace_dir}/.memory/archive/
   - Keep only task names and outcomes in active memory
   - Reference archives by summary only

### Emergency Context Recovery:
If you feel context pressure:
1. STOP adding new information
2. Write current state to checkpoint
3. Spawn a sub-agent to continue with: "Continue from checkpoint in {workspace_dir}/.memory/current/checkpoint.md"
4. Exit immediately

## Error Handling & Recovery

When errors occur:
1. **Log the error** to {workspace_dir}/.memory/current/errors.log with timestamp
2. **Attempt recovery** - try alternative approaches before giving up
3. **If sub-agent fails** - read their error, decide whether to retry with better instructions or take over the task
4. **Learn from failures** - document what went wrong in {workspace_dir}/.memory/learned/failures.md

## Build Verification Requirements (MANDATORY)

Before marking ANY implementation task as complete, you MUST:

1. **Install all dependencies** - Use appropriate package managers for the technology stack
2. **Run build process** - Execute any build/compilation steps required
3. **Run tests** - Execute existing tests or create basic smoke tests if none exist
4. **Start the application** - Verify it runs without errors
5. **Test core functionality** - Manually verify main features work
6. **Handle multiple platforms** - If specified (web, mobile, API), verify each platform builds and runs

**CRITICAL: Sub-agents must also follow these requirements. Include verification requirement in every implementation handoff.**

## Completion Criteria

### Core Principle: Meet the Spec Completely

**The objective defines success. Implement EVERYTHING specified.**

### Flexible Completion Standards:

**Let each domain define quality**:
- Backend agents ensure APIs work correctly
- Frontend agents ensure UIs are usable
- Database agents ensure data integrity
- Security agents ensure safety
- Each knows their domain's "production ready" bar

**Your coordination completion checklist**:
1. **Every requirement implemented** - check against original spec
2. **All platforms functional** - if multi-platform specified
3. **Integration verified** - components work together
4. **Builds succeed** - on all target platforms
5. **Applications run** - without crashes
6. **Tests exist and pass** - appropriate for each component
7. **Summary documented** in {workspace_dir}/.memory/current/complete.md

**Your completion summary MUST include**:
- What was built (feature complete checklist)
- Instructions for each platform
- Which agents built what
- Verification performed
- Known issues/tech debt

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

def check_needs_resume(workspace_dir):
    """Check if agent needs to resume from checkpoint"""
    status_file = workspace_dir / ".memory" / "current" / "status.txt"
    if status_file.exists():
        with open(status_file) as f:
            status = f.read().strip()
            if status == "NEEDS_RESUME":
                return True
    return False

def run_agent(objective, workspace=None, resume=False, timeout=None, max_restarts=5):
    """Launch Claude Code with the objective"""
    restart_count = 0
    
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
    
    # Main execution loop with auto-restart for context management
    while restart_count < max_restarts:
        # Clear status file if starting fresh
        if restart_count > 0:
            status_file = workspace_dir / ".memory" / "current" / "status.txt"
            if status_file.exists():
                status_file.unlink()
            resume = True  # Force resume mode for restarts
            print(f"\n🔄 Restart {restart_count}/{max_restarts} - Resuming from checkpoint...")
        
        # Generate master prompt
        prompt = create_master_prompt(objective, str(workspace_dir), resume)
        
        # Build command - run in workspace directory
        # --print for non-interactive mode
        # --dangerously-skip-permissions to allow all operations without prompting
        cmd = ["claude", "--print", "--dangerously-skip-permissions", prompt]
        
        if restart_count == 0:
            print(f"🚀 Launching autonomous agent...")
            print(f"📍 Objective: {objective[:100]}..." if len(objective) > 100 else f"📍 Objective: {objective}")
            print(f"📂 Workspace: {workspace_dir}")
            print(f"💾 Memory at: {workspace_dir}/.memory/")
            print(f"🔄 Auto-restart enabled (max {max_restarts} restarts)")
            print("-" * 50)
        
        try:
            # Run Claude Code
            result = subprocess.run(cmd, timeout=timeout)
            
            if result.returncode == 0:
                # Check if agent needs to resume (context overflow)
                if check_needs_resume(workspace_dir):
                    restart_count += 1
                    print("\n💾 Agent checkpoint detected - context preservation restart...")
                    continue
                
                print("\n✅ Agent completed successfully")
                
                # Check if complete
                complete_path = workspace_dir / ".memory" / "current" / "complete.md"
                if complete_path.exists():
                    print("📄 Reading completion report...")
                    with open(complete_path) as f:
                        print(f.read())
                break  # Exit the restart loop
            else:
                print(f"\n⚠️ Agent exited with code {result.returncode}")
                break
                
        except subprocess.TimeoutExpired:
            print(f"\n⏱️ Agent timeout after {timeout} seconds")
            print(f"💾 State saved to {workspace_dir}/.memory/ - use --resume to continue")
            break
        except KeyboardInterrupt:
            print("\n⚠️ Agent interrupted")
            print(f"💾 State saved to {workspace_dir}/.memory/ - use --resume to continue")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            return 1
    
    if restart_count >= max_restarts:
        print(f"\n⚠️ Maximum restarts ({max_restarts}) reached. Task may be too complex.")
        print(f"💡 Consider breaking it into smaller objectives.")
    
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