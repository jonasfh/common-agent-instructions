# Testing & Quality Assurance Guidelines

## Universal Quality Principles

1. **Automated Testing**:
   - Write automated unit and/or integration tests for all newly added functionality.
   - Update existing test suites whenever modifying existing functionality to prevent regressions.
   - Ensure the entire test suite passes before submitting changes.

2. **Linting and Static Analysis**:
   - Run project linters and static analysis tools before completing any task.
   - Resolving all linting errors and warnings is mandatory.

3. **Formatting & Hygiene**:
   - Run project-wide formatters before staging changes.
   - Enforce trailing whitespace removal and proper newline endings on all text files.
