# Handoff Memory

This directory facilitates communication between agents:

- Files named `to-{agent}.md` contain tasks for specific agents
- Files named `from-{agent}.md` contain results from agents
- `shared-context.md` contains context all agents should know

Example:
1. Parent writes task to `to-frontend.md`
2. Frontend agent reads task, does work
3. Frontend agent writes results to `from-frontend.md`
4. Parent reads results and continues