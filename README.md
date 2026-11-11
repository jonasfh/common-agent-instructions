# Common Agent Instructions

## Purpose
This repository serves as a centralized, technology-agnostic knowledge base of development workflows, multi-agent roles, documentation rules, quality standards, and architectural conventions for AI agents (and human developers) working across multiple software projects.

## Modular Sub-guidelines

- 🔄 **[Workflow Guidelines](file:///./WORKFLOW.md)**: GitHub issue-driven development, Single-Agent Fast Path vs. Multi-Agent Path, Conventional Commits v1.0.0, submodule updates at startup, `/plan` approval gate, stop-on-completion PR rules, branching, and PR merge strategies.
- 🤝 **[Multi-Agent Roles & Contracts](file:///./ROLES.md)**: Automatic complexity triage (Level 1/2/3), role definitions (Coordinator, Researcher, Implementer, Verifier, Reviewer), hand-off contracts, workspace isolation, and tool portability (Antigravity & GitHub Copilot).
- 📖 **[Developer Playbook](file:///./PLAYBOOK.md)**: Practical manual for developers on prompting, `/plan`, `/teamwork`, `/grill-me`, and working across Antigravity and GitHub Copilot.
- 📝 **[Documentation Standards](file:///./DOCUMENTATION.md)**: User-facing vs. developer documentation, continuous documentation synchronization, and Mermaid diagram constraints.
- 🧪 **[Testing & Quality Assurance](file:///./TESTING.md)**: Automated testing requirements, zero-lint policy, and formatting hygiene.
- 📐 **[Architecture Standards](file:///./ARCHITECTURE.md)**: Modularity, separation of concerns, and universal database timestamp rules.

## Progressive Skills (`skills/`)
Task-specific checklists live in `skills/<name>/SKILL.md` (registered in `skills.json`) so specialist agents only load what they need:
- **`conventional-commits`** ([`skills/conventional-commits/SKILL.md`](file:///./skills/conventional-commits/SKILL.md)): Conventional Commits v1.0.0 checklist, SemVer mapping, and zero-dependency commit/PR validator (`scripts/validate_commit.py`).
- **`issue-breakdown`** ([`skills/issue-breakdown/SKILL.md`](file:///./skills/issue-breakdown/SKILL.md)): Decomposing a GitHub issue into independent, non-overlapping worker slices.
- **`independent-verification`** ([`skills/independent-verification/SKILL.md`](file:///./skills/independent-verification/SKILL.md)): Running and reporting tests/linters independently of the author.
- **`pr-review`** ([`skills/pr-review/SKILL.md`](file:///./skills/pr-review/SKILL.md)): Reviewing the final diff against architecture, testing, documentation, Conventional Commits, and changelog rules.

## Using this Submodule in Consuming Projects

Add this repository as a git submodule in your project under `.agents/common-agent-instructions/`:

```bash
git submodule add https://github.com/jonasfh/common-agent-instructions.git .agents/common-agent-instructions
```

To expose shared skills automatically in Antigravity, add `.agents/skills.json` in the consuming project:

```json
{
  "entries": [
    {
      "path": "common-agent-instructions/skills"
    }
  ]
}
```

In the consuming project's `AGENTS.md`, link to the modular sub-guidelines in `.agents/common-agent-instructions/`.
