#!/usr/bin/env python3
"""Zero-dependency Conventional Commits v1.0.0 validator for commits and PR titles."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ALLOWED_TYPES = (
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
)

HEADER_PATTERN = re.compile(
    rf"^({'|'.join(ALLOWED_TYPES)})(\([a-z0-9._/-]+\))?!?:\s(?![A-Z]).+$"
)

ISSUE_REF_PATTERN = re.compile(
    r"(\((?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#\d+\)"
    r"|\((?:dep|sec)-[A-Za-z0-9_.-]+\)"
    r"|(?:Closes|Fixes|Resolves|Refs):?\s+(?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#\d+)"
)


def validate_message(
    message: str,
    *,
    max_length: int = 100,
    require_issue: bool = False,
) -> list[str]:
    """Validate a commit message or PR title against project Conventional Commits rules.

    Returns a list of error strings (empty if valid).
    """
    errors: list[str] = []
    stripped = message.strip()
    if not stripped:
        return ["Commit message or PR title must not be empty."]

    lines = stripped.splitlines()
    header = lines[0].strip()

    if len(header) > max_length:
        errors.append(f"Header exceeds {max_length} characters ({len(header)}): {header!r}")

    if not HEADER_PATTERN.match(header):
        errors.append(
            "Header must match '<type>[optional (scope)][!]: <lowercase description>' "
            f"(allowed types: {', '.join(ALLOWED_TYPES)}). Got: {header!r}"
        )

    desc_part = header.split(": ", 1)[1] if ": " in header else header
    desc_without_ref = re.sub(
        r"\s*(?:\((?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#\d+\)|\((?:dep|sec)-[A-Za-z0-9_.-]+\))\s*$",
        "",
        desc_part,
    )
    if header.endswith(".") or desc_without_ref.endswith("."):
        errors.append(f"Header must not end with a trailing period: {header!r}")

    if require_issue and not ISSUE_REF_PATTERN.search(stripped):
        errors.append(
            "Missing issue/alert reference (expected '(#<id>)', '(<owner>/<repo>#<id>)', "
            "'(dep-<id>)', '(sec-<id>)', or 'Closes/Refs #<id>' footer)."
        )

    return errors


def validate_git_range(
    rev_range: str,
    *,
    repo_root: Path | None = None,
    max_length: int = 100,
    require_issue: bool = False,
    skip_merges: bool = True,
) -> list[tuple[str, list[str]]]:
    """Validate all commits in a git revision range (e.g. 'origin/main..HEAD')."""
    cmd = ["git", "log", "--format=%H%x1f%B%x1e"]
    if skip_merges:
        cmd.append("--no-merges")
    cmd.append(rev_range)

    result = subprocess.run(
        cmd,
        cwd=repo_root or Path.cwd(),
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git log failed for range {rev_range!r}: {result.stderr.strip() or result.stdout.strip()}"
        )

    failures: list[tuple[str, list[str]]] = []
    for raw_record in result.stdout.split("\x1e"):
        record = raw_record.strip()
        if not record or "\x1f" not in record:
            continue
        sha, body = record.split("\x1f", 1)
        errs = validate_message(body, max_length=max_length, require_issue=require_issue)
        if errs:
            failures.append((sha.strip()[:8], errs))
    return failures


def main() -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Validate Conventional Commits messages and PR titles.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--message", "-m", type=str, help="Commit message or PR title to validate.")
    group.add_argument("--file", "-f", type=Path, help="Path to file containing commit message.")
    group.add_argument(
        "--range",
        "-r",
        type=str,
        help="Git revision range to validate (e.g. origin/main..HEAD).",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=100,
        help="Maximum header length in characters (default: 100).",
    )
    parser.add_argument(
        "--require-issue",
        action="store_true",
        help="Require an issue or alert reference in header or footer.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Git repository root for --range (default: cwd).",
    )
    args = parser.parse_args()

    if args.message is not None:
        errors = validate_message(
            args.message, max_length=args.max_length, require_issue=args.require_issue
        )
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        print("OK: valid Conventional Commit message.")
        return 0

    if args.file is not None:
        text = args.file.read_text(encoding="utf-8")
        errors = validate_message(
            text, max_length=args.max_length, require_issue=args.require_issue
        )
        if errors:
            for err in errors:
                print(f"ERROR: {err}", file=sys.stderr)
            return 1
        print("OK: valid Conventional Commit message.")
        return 0

    try:
        failures = validate_git_range(
            args.range,
            repo_root=args.repo_root,
            max_length=args.max_length,
            require_issue=args.require_issue,
        )
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if failures:
        for sha, errs in failures:
            for err in errs:
                print(f"ERROR [{sha}]: {err}", file=sys.stderr)
        return 1

    print(f"OK: all commits in {args.range} follow Conventional Commits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
