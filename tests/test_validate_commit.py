"""Unit tests for the conventional-commits validator script."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "conventional-commits"
    / "scripts"
    / "validate_commit.py"
)

spec = importlib.util.spec_from_file_location("validate_commit", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
validate_commit = importlib.util.module_from_spec(spec)
sys.modules["validate_commit"] = validate_commit
spec.loader.exec_module(validate_commit)


class TestValidateCommit(unittest.TestCase):
    """Test Conventional Commits validation rules."""

    def test_valid_messages(self) -> None:
        valid = [
            "feat(ble): support temporary PIN schedules (#87)",
            "fix: prevent duplicate slot allocation (#81)",
            "feat(api)!: require explicit lock_id (#92)",
            "docs(workflow): adopt conventional commits (jonasfh/snippen-doorman-service#87)",
            "fix(deps): bump cryptography to 50.0.2 (dep-42)",
            "fix(security): sanitize shell args (sec-7)",
            "chore(agents): update .agents submodule pointers (#87)\n\nCloses #87",
        ]
        for msg in valid:
            with self.subTest(msg=msg):
                self.assertEqual(validate_commit.validate_message(msg, require_issue=True), [])

    def test_valid_without_issue_when_optional(self) -> None:
        self.assertEqual(validate_commit.validate_message("chore: tidy readme"), [])

    def test_invalid_messages(self) -> None:
        cases = [
            "",
            "(#87) Old format without type",
            "feat: Uppercase description (#87)",
            "unknown(ble): unsupported type (#87)",
            "feat(ble): trailing period not allowed. (#87)",
            "feat(ble): ends with period.",
            "feat(BadScope): uppercase scope (#87)",
            "feat: " + "a" * 100 + " (#87)",
        ]
        for msg in cases:
            with self.subTest(msg=msg):
                self.assertTrue(validate_commit.validate_message(msg))

    def test_require_issue_enforced(self) -> None:
        errs = validate_commit.validate_message("feat(ble): add rtc sync", require_issue=True)
        self.assertTrue(any("issue/alert reference" in e for e in errs))

        # Footer Closes #12 satisfies require_issue
        self.assertEqual(
            validate_commit.validate_message("feat(ble): add rtc sync\n\nCloses #12", require_issue=True),
            [],
        )


if __name__ == "__main__":
    unittest.main()
