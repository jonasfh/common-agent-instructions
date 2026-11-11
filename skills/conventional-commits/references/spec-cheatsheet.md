# Conventional Commits v1.0.0 Cheatsheet

## Types and SemVer Impact

| Type | Purpose | SemVer |
|---|---|---|
| `feat` | New user-facing or API feature | MINOR (`0.X.0`) |
| `fix` | Bug fix | PATCH (`0.0.X`) |
| `feat!` / `fix!` / `BREAKING CHANGE:` | Incompatible API/behavior change | MAJOR (`X.0.0`) |
| `perf` | Performance improvement without API break | None / PATCH |
| `refactor` | Code restructuring without behavior change | None |
| `docs` | Documentation only | None |
| `test` | Adding or updating tests | None |
| `build` | Packaging, dependencies, Dockerfile | None / PATCH |
| `ci` | CI workflows and validation scripts | None |
| `chore` | Maintenance, submodule pointer updates | None |
| `style` | Formatting, whitespace, lint-only fixes | None |
| `revert` | Reverts a previous commit | Mirrors reverted commit |

## Examples

Same-repo feature commit:

```text
feat(ble): support temporary keypad PIN schedules (#87)

Closes #87
```

Submodule / cross-repo commit:

```text
docs(workflow): adopt conventional commits (jonasfh/snippen-doorman-service#87)

Refs: jonasfh/snippen-doorman-service#87
```

Breaking change:

```text
feat(api)!: require explicit lock_id for multi-door sync (#92)

BREAKING CHANGE: Removed implicit fallback to default lock when multiple locks are configured.
Closes #92
```

Dependabot / security alert fix:

```text
fix(deps): bump cryptography to 50.0.2 (dep-42)

Refs: https://github.com/owner/repo/security/dependabot/42
```
