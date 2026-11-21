---
name: pr-review
description: Review the final git diff before PR creation against architecture, testing, documentation, versioning, and formatting hygiene rules.
---

# PR Review Skill (Reviewer / Coordinator)

Use this skill before committing/pushing the final integrated branch and opening a Pull Request.

## Checklist

1. **Diff Inspection (`git diff main...HEAD`)**:
   - Verify no unintended files, debug leftovers, or out-of-scope edits were introduced.
   - Check modularity, no duplicated logic, and adherence to project `ARCHITECTURE.md`.
2. **Documentation & Changelog**:
   - Confirm `README.md`, `DEV_README.md`, or `docs/` are updated if features, endpoints, schemas, or models changed.
   - Confirm semantic version bump and `CHANGELOG.md` entry (`## [X.Y.Z] - YYYY-MM-DD`) for functional changes.
3. **Formatting & Whitespace Hygiene**:
   - Confirm formatters (`phpcbf` / `composer lint:fix`, etc.) were run.
   - Confirm no trailing whitespace and a single trailing newline (`\n`) on modified files.
4. **PR Readiness**:
   - Commits follow `(#<id>) Description` format.
   - PR uses `Closes #<id>` and stops immediately after `gh pr create` without auto-merging.
