#!/usr/bin/env python3
"""
Memory template helpers for the agent
"""

from datetime import datetime

def create_objective_template(objective):
    """Create initial objective memory"""
    return f"""# Project Objective

## Main Goal
{objective}

## Success Criteria
- Objective is fully implemented
- All tests pass
- Code is documented
- Solution is deployed or deployable

## Created
{datetime.now().isoformat()}
"""

def create_progress_template():
    """Create initial progress tracking"""
    return """# Progress Tracker

## Overall Progress: 0%

## Completed Tasks
- [ ] Understand objective
- [ ] Plan approach
- [ ] Implement solution
- [ ] Test solution
- [ ] Document solution

## Current Status
Starting analysis...
"""

def create_architecture_template():
    """Create architecture decisions template"""
    return """# Architecture Decisions

## Technology Stack
(To be determined based on requirements)

## Key Components
(To be identified during implementation)

## Design Patterns
(To be discovered and documented)
"""

def create_patterns_template():
    """Create patterns documentation template"""
    return """# Discovered Patterns

## Code Patterns
(Patterns found in the codebase will be documented here)

## Workflow Patterns
(Effective workflows will be noted here)

## Anti-Patterns to Avoid
(Problematic approaches will be listed here)
"""

def create_decisions_template():
    """Create decisions log template"""
    return """# Decision Log

## Format: [Date] Decision: Rationale

(Decisions will be logged here as they are made)
"""