# Common Agent Workflow Guidelines

## GitHub Issue Workflow

All changes made to a project MUST be based on an associated GitHub issue or direct Code Scanning / Dependabot alert IDs. If a task or instruction is given without an associated issue, create a GitHub issue containing the details of the work to be done (`gh issue create`) before starting.

Once a GitHub issue is identified or created, follow this workflow:

1. **Preparation**:
   - Start in `main` branch and pull latest changes: `git pull origin main`.
   - Verify GitHub authentication: `gh auth status` (Note: `gh` CLI commands require network access; bypass sandbox isolation if running in a restricted sandbox).
   - Read issue details: `gh issue view <id> --json title,body`.
2. **Branching**:
   - Create and check out a dedicated development branch following the pattern: `gh-issue/<id>` (e.g., `gh-issue/39`), branched off `main`.
   - For security or dependency alerts, use `sec-<ids>-...` or `dep-<ids>-...`.
3. **Submodule Updates on Development Branch**:
   - **Check for Latest Guidelines**: Immediately after checking out the development branch, pull the latest `main` branch for all submodules under `.agents/`. Do not rely on plain `git submodule update` (which only checks out the old pinned commit) or `git submodule update --remote` (which creates a detached HEAD):
     ```bash
     # Sjekk ut og pull nyeste main for felles- og språkspesifikke instruksjoner:
     git -C .agents/common-agent-instructions checkout main && git -C .agents/common-agent-instructions pull origin main
     ```
     (Gjenta tilsvarende for eventuelle andre submoduler under `.agents/`, f.eks. `python-agent-instructions` eller `node-agent-instructions`).
   - **Commit Updated Submodule Pointers**: Check `git status`. If any submodule pointer has changed (`modified: .agents/...`), immediately stage and commit the updated submodule pointer(s) in a separate commit on the current feature branch:
     ```bash
     git add .agents/
     git commit -m "Update .agents submodules pointer"
     ```
   - **Rationale**: This ensures every new development task always executes with the latest agent guidelines, keeps `main` clean, avoids detached HEAD states, and rolls submodule pointer updates naturally into `main` via the regular feature PR.
4. **Implementation Plan**:
   - When resolving issues, an implementation plan MUST be presented before making code changes, unless the task is very small and does not require planning.
5. **Implementation**:
   - Resolve the issue adhering to project coding standards and architecture.
   - Routinely run project formatters whenever files are created or modified.
   - Create or update automated tests and ensure all linters and test suites pass.
   - Update project documentation (`README.md`, `DEV_README.md`, `docs/`) for any new features, endpoints, schemas, or models implemented.
6. **Submission & Commit Messages**:
   - **Formatting Hygiene**: ALWAYS run repository formatting tools immediately before staging files (`git add`) and committing.
   - **Commit Message Format**:
     - Within the same repository: Issue commits MUST start with `(#<id>)`, e.g., `(#1) Fixed xxx...`.
     - Within a submodule or cross-repository referencing another repo's issue: Commits MUST start with `(<owner>/<repo>#<id>)`, e.g., `(jonasfh/snippen-sms-service#39) Fixed xxx...`.
     - Make separate commits for different issue numbers.
   - **Commit Suggestion**: ALWAYS suggest a commit message as plain text in a copy-pasteable code block. Focus on the problem solved in the header, with rationale in the body.
   - Push branch: `git push -u origin HEAD`.
   - Create Pull Request: `gh pr create --body "Closes #<id>" --title "(#<id>) <Issue Title>"`.
7. **Issue Status & Feedback**:
   - Add implementation notes and summary to the GitHub issue (`gh issue comment <id> --body "..."`).
8. **Pull Request Completion & Hand-off**:
   - **Stop and Return Prompt**: Once implementation is complete, changes committed and pushed, and the PR is created, the AI agent MUST STOP immediately and return the prompt to the user.
   - **Do NOT Wait for Workflows**: Do NOT wait for PR validation workflows, CI checks, or background pipelines to complete.
   - **Do NOT Merge Automatically**: The agent must NEVER merge the PR automatically.
9. **Merging Pull Requests**:
   - Only proceed with merging after receiving explicit user instruction to do so.
   - Merge method: ALWAYS use **Rebase and merge** (`gh pr merge <id> --rebase --delete-branch`) as the default strategy. If rebasing issues or conflicts arise, use a standard **merge commit** (`gh pr merge <id> --merge --delete-branch`). Do NOT use squash and merge (`--squash`) unless explicitly instructed or required for a specific reason.

## Development Environment & Devcontainers

- **Prefer Devcontainer Environments**: Developing inside a devcontainer (`.devcontainer/`) is preferred to ensure reproducible, isolated toolchains and runtime dependencies across agents and human developers.
- **Task-Driven Environment Customization**: Always allow and proactively customize the development environment (e.g. updating `.devcontainer/devcontainer.json`, `Dockerfile`, installing system packages, CLI tools, runtime versions, or language toolchains) whenever necessary to fit the requirements of the task.

## Versioning & Changelog

- **Version Bump**: Bump the semantic version in package configuration/manifests on functional changes.
- **CHANGELOG.md**: Every version bump must have an entry in `CHANGELOG.md` under `## [X.Y.Z] - YYYY-MM-DD`.

## Formatting & Whitespace Hygiene

All project files (code, Markdown, JSON, YAML, TOML, etc.) must adhere to strict formatting hygiene:
- Trailing whitespaces stripped across all lines.
- Exactly one trailing newline (`\n`) at the end of the file.
- Duplicate or excess trailing newlines removed from the end of the file.

## Self-Improvement & Environment Adaptation

- **Continuous Agent Guideline Updates**: Whenever an agent experiences friction, environment errors (e.g., sandbox network access for `gh` CLI commands, missing tools, unusual log locations, container paths, or git ref locks), the agent MUST update project guidelines immediately with the discovered workaround or instructions so subsequent agent sessions execute cleanly without repeating trial-and-error.
- **Git Credential Helper in Devcontainers**: If `git fetch`/`push` hangs due to a host credential helper mount, override it for the repository: run `git config --unset-all credential.helper && git config --add credential.helper "" && git config --add credential.helper '!gh auth git-credential'`.

## Dependabot & Security Alerts Workflow

- Refer to alerts using full GitHub URLs, e.g., `https://github.com/<owner>/<repo>/security/dependabot/<alert_id>`.
- Use branches like `dep-<ids>-fix-dependabot-issues` or `sec-<ids>-fix-code-scanning-issues`.
- Format commit headers as `(dep-<ids>) Description` or `(sec-<ids>) Description`.
