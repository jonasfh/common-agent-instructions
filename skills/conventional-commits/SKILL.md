---
name: conventional-commits
description: >-
  Guide and validator for Conventional Commits v1.0.0 commit messages, PR titles,
  issue references, and SemVer version bumps across common-agent-instructions projects.
  Use before running git commit, creating a PR (gh pr create), or bumping versions in CHANGELOG.md.
---

# Conventional Commits Workflow

Use this skill when composing commit messages, PR titles, or SemVer/changelog updates.

## Format

```text
<type>[optional scope][!]: <description> (#<id>)

[optional body]

[optional footer(s)]
```

- **Allowed types**: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
- **Description**: lowercase first character, imperative mood, no trailing period, max 100 chars total header.
- **Issue reference**:
  - Same repository: append `(#<id>)` to header and include `Closes #<id>` or `Refs #<id>` in footer/PR body.
  - Submodule or cross-repository: append `(<owner>/<repo>#<id>)` to header and `Refs: <owner>/<repo>#<id>` in footer.
  - Dependabot / security alerts: `fix(deps): <description> (dep-<ids>)` or `fix(security): <description> (sec-<ids>)`.

## SemVer Mapping

- `fix:` -> **PATCH** (`0.0.X`)
- `feat:` -> **MINOR** (`0.X.0`)
- `feat!:` / `fix!:` / `BREAKING CHANGE:` footer -> **MAJOR** (`X.0.0`)
- `docs:`, `chore:`, `ci:`, `test:`, `refactor:`, `style:`, `build:`, `perf:` -> no bump unless functional/packaging behavior changes (or PATCH if repo CI requires `__version__ > latest_tag`).

## Steps Before Commit / PR

1. Check detailed examples and edge cases in [spec-cheatsheet.md](./references/spec-cheatsheet.md) if needed.
2. Validate commit message or PR title with [validate_commit.py](./scripts/validate_commit.py):
   ```bash
   python3 .agents/common-agent-instructions/skills/conventional-commits/scripts/validate_commit.py --require-issue --message "feat(ble): add rtc sync (#87)"
   python3 .agents/common-agent-instructions/skills/conventional-commits/scripts/validate_commit.py --require-issue --range origin/main..HEAD
   ```
3. Verify `CHANGELOG.md` and package version match the commit types (`fix` / `feat` / `!`).
