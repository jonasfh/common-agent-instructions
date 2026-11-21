---
name: independent-verification
description: Independently verify integrated code by running linters, tests, and builds without authoring bias, reporting only directly observed command outputs.
---

# Independent Verification Skill (Verifier)

Use this skill when acting as an independent `Verifier` after `Implementer` changes are integrated.

## Rules

1. **Never Assume or Extrapolate**:
   - Only report test suites, linters, or builds as passing if you ran them **after** the final edit/integration and observed all reported cases pass.
   - Never silently relax assertions or skip failing checks.
2. **Run Targeted & Full Checks**:
   - Run the project's mandatory lint check (e.g., `composer lint`, `npm run lint`).
   - Run the full test suite (e.g., `composer test`, `npm run test:js`).
   - Run UI/visual tests (e.g., `npm run test:ui:fast`) **only** when UI, CSS, templates, or frontend logic changed.
3. **Verify Against Acceptance Criteria**:
   - Cross-check each requirement in `gh issue view <id>` against the actual implementation and test coverage.
4. **Report Format**:
   - List exact commands executed, exit codes, pass/fail counts, and any remaining gaps or warnings.
