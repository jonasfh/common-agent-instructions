# Common Agent Instructions

## Purpose
This repository serves as a centralized, technology-agnostic knowledge base of development workflows, documentation rules, quality standards, and architectural conventions for AI agents (and human developers) working across multiple software projects.

## Modular Sub-guidelines

- 🔄 **[Workflow Guidelines](file:///./WORKFLOW.md)**: GitHub issue-driven development, submodule updates at startup, implementation planning, stop-on-completion PR rules (no workflow waiting), devcontainer preferences, branching, commit conventions, PR merge strategies, SemVer, and self-improvement feedback loops.
- 📝 **[Documentation Standards](file:///./DOCUMENTATION.md)**: User-facing vs. developer documentation, continuous documentation synchronization, and Mermaid diagram constraints.
- 🧪 **[Testing & Quality Assurance](file:///./TESTING.md)**: Automated testing requirements, zero-lint policy, and formatting hygiene.
- 📐 **[Architecture Standards](file:///./ARCHITECTURE.md)**: Modularity, separation of concerns, and universal database timestamp rules.

## Shared Skills

Reusable agent skills live under `skills/` (registered in `skills.json`), including:

- **`conventional-commits`** ([`skills/conventional-commits/SKILL.md`](file:///./skills/conventional-commits/SKILL.md)): Conventional Commits v1.0.0 checklist, SemVer mapping, and zero-dependency commit/PR validator (`scripts/validate_commit.py`).

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

In the consuming project's `AGENTS.md`, link to the modular sub-guidelines in `.agents/common-agent-instructions/` and define any project-specific / technology-specific instructions alongside them.
