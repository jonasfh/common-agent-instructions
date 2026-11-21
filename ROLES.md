# Multi-Agent Roles & Contracts

## Purpose
This document defines portable, role-based contracts for scaling from a single AI agent to delegated subagents and parallel multi-agent teams. The core roles are tool-agnostic and apply across Antigravity, GitHub Copilot, and other agentic coding environments.

---

## Automatic Complexity Triage (AI Responsibility)
The primary agent (or Coordinator) is responsible for assessing task complexity **automatically** at the start of every task—the developer should not have to micromanage team size:

| Level | Criteria | Execution Mode |
| --- | --- | --- |
| **Level 1: Single Agent** | Small, well-scoped task (1–2 files, clear fix, single domain) | Execute directly on the feature branch (Fast Path). |
| **Level 2: Coordinator + Subagents** | Medium task (multiple files, needs codebase exploration or independent test verification) | Primary agent acts as Coordinator; delegates read-only exploration (`Researcher`) and/or final checks (`Verifier`). |
| **Level 3: Multi-Agent Team** | Large task (parallel domains such as backend + frontend, multi-module refactor, or broad test + doc updates) | Coordinator produces `/plan`, **waits for user approval**, then spawns parallel `Implementer` workers in isolated workspaces (`git worktree` / `share`) followed by an independent `Verifier`. |

> **Antigravity Note:** If the user has not invoked `/teamwork` on a Level 3 task, the Coordinator should recommend `/teamwork` during `/plan` (or use `invoke_subagent` with `Workspace: "share"` / `"branch"` when appropriate).

---

## Standard Roles

### 1. Coordinator (Orchestrator)
- **Owns:** Reading the GitHub issue, creating `gh-issue/<id>`, updating `.agents/` submodules, running `/plan` (and stopping for user approval on Level 2/3 plans), decomposing work into non-overlapping tasks, integrating worker changes, updating docs/version/`CHANGELOG.md`, committing, pushing, and opening the PR.
- **Does NOT own:** Writing large blocks of production code on Level 3 tasks when parallel `Implementer` workers are assigned.
- **Hand-off Output:** Approved task breakdown with explicit file/module boundaries and acceptance criteria per worker.

### 2. Researcher (Read-Only Explorer)
- **Owns:** Mapping existing architecture, call sites, dependencies, and conventions before implementation begins.
- **Workspace:** Shared read-only (`inherit`). Never modifies files.
- **Hand-off Output:** Concise summary of relevant file paths, symbol names, constraints, and existing patterns.

### 3. Implementer (Coder)
- **Owns:** Implementing a bounded slice (e.g., one PHP service/API, one JS/UI component, or one test suite) within assigned files/modules, plus running fast local checks (e.g., `composer test:changed`, `composer lint:fix`).
- **Workspace:** Isolated (`git worktree`, or `workspace: "share"` / `"branch"` in Antigravity) whenever multiple Implementers run concurrently.
- **Anti-patterns:** Never opens a PR, merges to `main`, or edits files outside its assigned slice when working in a team.
- **Hand-off Output:** List of modified/created files, summary of changes, and exact local commands run with results.

### 4. Verifier (Independent Tester)
- **Owns:** Running linters, unit/integration tests, and UI/build checks against the **integrated** code without having authored the implementation.
- **Skill:** Load `independent-verification` (`skills/independent-verification/SKILL.md`).
- **Anti-patterns:** Never guesses or extrapolates test status; never silently skips failing checks.
- **Hand-off Output:** Verification report listing exact commands executed, pass/fail counts, and any uncovered gaps.

### 5. Reviewer / Docs
- **Owns:** Reviewing the final diff against `ARCHITECTURE.md`, `TESTING.md`, `DOCUMENTATION.md`, formatting hygiene, version bump, and `CHANGELOG.md`.
- **Skill:** Load `pr-review` (`skills/pr-review/SKILL.md`).
- **Hand-off Output:** Confirmation that docs, changelog, and architectural rules are satisfied (or concrete list of fixes).

---

## Tool Portability Mapping

| Concept | Antigravity | GitHub Copilot / Other Tools |
| --- | --- | --- |
| **Always-on rules** | `AGENTS.md` | `AGENTS.md` / `.github/copilot-instructions.md` |
| **On-demand procedures** | `SKILL.md` (via `.agents/skills.json`) | `SKILL.md` (standard YAML frontmatter) |
| **Planning gate** | `/plan` (or `/grill-me` for unclear specs) | Plan mode / issue breakdown before coding |
| **Subagents (Level 2)** | `invoke_subagent` (`research`, custom roles) | Subagent / background agent delegation |
| **Parallel team (Level 3)** | `/teamwork` (swarm) + `workspace: "share"` | Parallel coding agents in separate `git worktree`s |
