# Common Agent Instructions

## Purpose
This repository serves as a centralized, technology-agnostic knowledge base of development workflows, documentation rules, quality standards, and architectural conventions for AI agents (and human developers) working across multiple software projects.

## Modular Sub-guidelines

- 🔄 **[Workflow Guidelines](file:///./WORKFLOW.md)**: GitHub issue-driven development, branching patterns, commit conventions, PR merge strategies, SemVer versioning, CHANGELOG maintenance, and self-improvement feedback loops.
- 📝 **[Documentation Standards](file:///./DOCUMENTATION.md)**: User-facing vs. developer documentation, continuous documentation synchronization, and Mermaid diagram constraints.
- 🧪 **[Testing & Quality Assurance](file:///./TESTING.md)**: Automated testing requirements, zero-lint policy, and formatting hygiene.
- 📐 **[Architecture Standards](file:///./ARCHITECTURE.md)**: Modularity, separation of concerns, and universal database timestamp rules.

## Using this Submodule in Consuming Projects

Add this repository as a git submodule in your project under `.agents/common-agent-instructions/`:

```bash
git submodule add https://github.com/jonasfh/common-agent-instructions.git .agents/common-agent-instructions
```

In the consuming project's `AGENTS.md`, link to the modular sub-guidelines in `.agents/common-agent-instructions/` and define any project-specific / technology-specific instructions alongside them.
