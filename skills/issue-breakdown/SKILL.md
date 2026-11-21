---
name: issue-breakdown
description: Decompose a GitHub issue into non-overlapping, parallelizable worker slices with explicit interfaces and acceptance criteria for Coordinator agents.
---

# Issue Breakdown Skill (Coordinator)

Use this skill during `/plan` on Level 2 or Level 3 tasks before delegating to `Implementer` workers.

## Checklist

1. **Read the Issue & Map the Codebase**:
   - Inspect `gh issue view <id> --json title,body`.
   - For unfamiliar or broad areas, delegate a read-only `Researcher` subagent to map affected files, symbols, and existing tests.
2. **Define Clean File & Module Boundaries**:
   - Split work by domain/layer (e.g., PHP backend/DB vs. JS/CSS frontend vs. tests/docs) so no two concurrent `Implementer` workers edit the same file.
   - Lock shared interfaces (API endpoints, payload schemas, CSS classes, method signatures) in the plan before workers start.
3. **Assign Workspaces**:
   - **Readers / Verifiers:** `inherit` (shared workspace).
   - **Concurrent Implementers:** Isolated `git worktree` / `workspace: "share"` (or `"branch"`).
4. **Define Done Per Worker**:
   - Specify exact deliverables, required unit/integration tests, and local checks (e.g., `composer test:changed`, `composer lint:fix`).
5. **Approval Gate**:
   - Present the plan to the user and **wait for approval** before spawning parallel implementation workers.
