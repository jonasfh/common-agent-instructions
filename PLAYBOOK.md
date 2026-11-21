# Developer Playbook: Working with Single & Multi-Agent Teams

## Overview
This playbook explains how **you** (the developer) interact with the agent setup day-to-day. You do **not** need to manually classify every task—the AI agent assesses complexity automatically and scales up only when needed.

---

## Who Decides Complexity?
**The AI agent decides automatically** using the three levels in [ROLES.md](file:///./ROLES.md):
- **Small tasks (Level 1):** The agent executes directly (Fast Path). No subagent overhead.
- **Medium tasks (Level 2):** The agent acts as Coordinator, delegates codebase research or independent test verification to subagents, and handles the rest.
- **Large tasks (Level 3):** The agent proposes a `/plan` splitting the work into parallel tracks (e.g., backend + frontend + tests) and asks for your approval before spawning parallel workers.

> **Tip:** You can still *override* this at any time—for example, by starting a prompt with `/teamwork` when you already know you want a parallel team, or saying *"just fix this directly"* for a quick tweak.

---

## Practical Prompting Patterns

### 1. Small Task (Level 1 — Normal Prompt)
Just describe the task or reference the GitHub issue:
> *"Fix the typo in the booking confirmation message (issue #45)."*

The agent creates `gh-issue/45`, fixes it, runs fast tests/lint, commits, and opens the PR.

### 2. Medium Task (Level 2 — Automatic or Guided Delegation)
Describe the goal normally, or ask for `/plan` first if the design has trade-offs:
> *"/plan Implement issue #52: add cancellation deadline validation to BookingApi and unit tests."*

The Coordinator maps the codebase (using `research` if broad), presents the plan, waits for your approval, implements, and uses an independent **Verifier** check before opening the PR.

### 3. Large Task (Level 3 — `/teamwork` in Antigravity)
When an issue spans multiple independent modules (e.g., PHP backend/DB + JS/CSS frontend + Playwright UI tests + docs):
> *"/teamwork Solve issue #60: split into backend, frontend, and independent verification."*

What happens:
1. **Coordinator** reads the issue, creates `gh-issue/60`, updates `.agents/` submodules, and produces `/plan` with clear file ownership.
2. **Approval Gate:** Coordinator stops **once** after `/plan` so you can confirm the split and interfaces.
3. **Parallel Execution:** Workers run in isolated workspaces (`share` / `git worktree`) so they never overwrite each other's files.
4. **Integration & Verification:** Coordinator integrates worker changes (no extra approval pause here), and an independent **Verifier** runs `composer lint`, `composer test`, and UI tests if frontend files changed.
5. **PR & Stop:** Coordinator updates docs/version/`CHANGELOG.md`, commits, pushes, creates the PR, and stops—waiting for you to review and approve merging to `main`.

---

## Using `/grill-me` Before `/plan`
If requirements in an issue are ambiguous or have multiple architectural options, start with:
> *"/grill-me on issue #60 before we plan"*

The agent will interview you with targeted questions to lock down edge cases before any code or subagent is launched.

---

## Using the Same Setup in GitHub Copilot
Because the core instructions live in `AGENTS.md`, `ROLES.md`, `WORKFLOW.md`, and standard `SKILL.md` files:
- **Copilot Chat / Agent Mode** automatically reads `AGENTS.md` (and `.github/copilot-instructions.md` if present).
- For parallel work outside Antigravity, use separate `git worktree` checkouts per task and assign each session its bounded slice from `ROLES.md`.
