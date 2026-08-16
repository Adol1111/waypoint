from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "skills"
    / "setup"
    / "local-work-tracker"
    / "scripts"
    / "waypoint_tracker.py"
)


class LocalWorkTrackerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        (self.repo / ".git").mkdir()
        feature_dir = self.repo / "docs" / "work" / "features" / "agent-foundation"
        (feature_dir / "tasks" / "contract").mkdir(parents=True)
        (feature_dir / "tasks" / "runtime").mkdir(parents=True)
        (feature_dir / "feature.md").write_text(
            "# Agent Foundation\n\nHuman-owned context.\n", encoding="utf-8"
        )
        (feature_dir / "tasks" / "contract" / "task.md").write_text(
            "# Contract\n", encoding="utf-8"
        )
        (feature_dir / "tasks" / "runtime" / "task.md").write_text(
            "# Runtime\n", encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_tracker(self, *arguments: str, succeeds: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.repo), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )
        if succeeds and result.returncode != 0:
            self.fail(f"tracker failed: {result.stderr}\n{result.stdout}")
        if not succeeds and result.returncode == 0:
            self.fail(f"tracker unexpectedly succeeded: {result.stdout}")
        return result

    def initialize_and_register(self) -> None:
        self.run_tracker(
            "init",
            "--actor",
            "gaoxiaoyi",
            "--display-name",
            "Gao Xiaoyi",
            "--executor-harness",
            "codex",
            "--executor-label",
            "window-1",
        )
        self.run_tracker(
            "register-feature",
            "--id",
            "agent-foundation",
            "--title",
            "Agent Foundation",
            "--summary",
            "Enable shared agent delivery",
            "--owner",
            "gaoxiaoyi",
            "--milestone",
            "m1",
            "--path",
            "docs/work/features/agent-foundation/feature.md",
        )
        self.run_tracker(
            "register-task",
            "--feature",
            "agent-foundation",
            "--id",
            "contract",
            "--title",
            "Freeze contract",
            "--path",
            "docs/work/features/agent-foundation/tasks/contract/task.md",
        )
        self.run_tracker(
            "register-task",
            "--feature",
            "agent-foundation",
            "--id",
            "runtime",
            "--title",
            "Runtime loop",
            "--path",
            "docs/work/features/agent-foundation/tasks/runtime/task.md",
            "--blocked-by",
            "contract",
        )

    def test_identity_is_local_and_exactly_ignored(self) -> None:
        self.run_tracker("init", "--actor", "gaoxiaoyi")
        gitignore = (self.repo / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/.waypoint/local.yaml", gitignore.splitlines())
        self.assertTrue((self.repo / ".waypoint" / "config.yaml").exists())
        whoami = self.run_tracker("whoami").stdout
        self.assertIn('"actor_id": "gaoxiaoyi"', whoami)

    def test_revision_assignment_dependency_and_rendering(self) -> None:
        self.initialize_and_register()

        blocked = self.run_tracker(
            "assign",
            "--feature",
            "agent-foundation",
            "--task",
            "runtime",
            "--assignee",
            "gaoxiaoyi",
            "--expect-revision",
            "0",
            succeeds=False,
        )
        self.assertIn("incomplete structural dependencies", blocked.stderr)

        self.run_tracker(
            "assign",
            "--feature",
            "agent-foundation",
            "--task",
            "contract",
            "--assignee",
            "gaoxiaoyi",
            "--expect-revision",
            "0",
        )
        mismatch = self.run_tracker(
            "transition",
            "--feature",
            "agent-foundation",
            "--task",
            "contract",
            "--to",
            "in-progress",
            "--expect-revision",
            "0",
            succeeds=False,
        )
        self.assertIn("revision mismatch", mismatch.stderr)

        for revision, target in ((1, "in-progress"), (2, "in-review")):
            self.run_tracker(
                "transition",
                "--feature",
                "agent-foundation",
                "--task",
                "contract",
                "--to",
                target,
                "--expect-revision",
                str(revision),
            )
        self.run_tracker(
            "transition",
            "--feature",
            "agent-foundation",
            "--task",
            "contract",
            "--to",
            "completed",
            "--expect-revision",
            "3",
            "--evidence",
            "MR 12 merged and acceptance verified",
            "--mr",
            "!12",
        )
        self.run_tracker(
            "assign",
            "--feature",
            "agent-foundation",
            "--task",
            "runtime",
            "--assignee",
            "bob",
            "--executor",
            "opencode/deepseek",
            "--branch",
            "feature/agent-foundation/runtime",
            "--expect-revision",
            "0",
        )
        for revision, target in ((1, "in-progress"), (2, "in-review")):
            self.run_tracker(
                "transition",
                "--feature",
                "agent-foundation",
                "--task",
                "runtime",
                "--to",
                target,
                "--expect-revision",
                str(revision),
            )
        self.run_tracker(
            "transition",
            "--feature",
            "agent-foundation",
            "--task",
            "runtime",
            "--to",
            "completed",
            "--expect-revision",
            "3",
            "--evidence",
            "MR 13 merged and acceptance verified",
        )
        denied = self.run_tracker(
            "close-feature",
            "--feature",
            "agent-foundation",
            "--expect-revision",
            "0",
            "--confirmed-by",
            "bob",
            "--evidence",
            "Feature acceptance passed",
            succeeds=False,
        )
        self.assertIn("must be confirmed by owner gaoxiaoyi", denied.stderr)
        self.run_tracker(
            "close-feature",
            "--feature",
            "agent-foundation",
            "--expect-revision",
            "0",
            "--confirmed-by",
            "gaoxiaoyi",
            "--evidence",
            "Feature acceptance and integration passed",
            "--completed-at",
            "2026-08-16",
        )
        self.run_tracker("render")
        self.run_tracker("check")

        feature = (
            self.repo / "docs" / "work" / "features" / "agent-foundation" / "feature.md"
        ).read_text(encoding="utf-8")
        dashboard = (self.repo / "docs" / "work" / "index.md").read_text(
            encoding="utf-8"
        )
        completed = (self.repo / "docs" / "work" / "completed.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Human-owned context.", feature)
        self.assertIn("- [x] [Freeze contract]", feature)
        self.assertIn("- [x] [Runtime loop]", feature)
        self.assertIn("assignee: bob", feature)
        self.assertIn("branch: feature/agent-foundation/runtime", feature)
        self.assertNotIn("Agent Foundation", dashboard)
        self.assertIn(
            "2026-08-16 — [Agent Foundation](features/agent-foundation/feature.md) — Enable shared agent delivery",
            completed,
        )

    def test_unsplit_feature_has_explicit_lifecycle(self) -> None:
        self.run_tracker("init", "--actor", "gaoxiaoyi")
        self.run_tracker(
            "register-feature",
            "--id",
            "agent-foundation",
            "--title",
            "Agent Foundation",
            "--owner",
            "gaoxiaoyi",
            "--milestone",
            "m1",
            "--path",
            "docs/work/features/agent-foundation/feature.md",
        )
        self.run_tracker(
            "transition-feature",
            "--feature",
            "agent-foundation",
            "--to",
            "in-progress",
            "--expect-revision",
            "0",
        )
        self.run_tracker("render")
        dashboard = (self.repo / "docs" / "work" / "index.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("in-progress", dashboard)

    def test_completed_index_is_newest_first(self) -> None:
        self.run_tracker("init", "--actor", "gaoxiaoyi")
        self.run_tracker(
            "register-feature",
            "--id",
            "agent-foundation",
            "--title",
            "Agent Foundation",
            "--owner",
            "gaoxiaoyi",
            "--milestone",
            "m1",
            "--path",
            "docs/work/features/agent-foundation/feature.md",
        )
        self.run_tracker(
            "close-feature",
            "--feature",
            "agent-foundation",
            "--expect-revision",
            "0",
            "--confirmed-by",
            "gaoxiaoyi",
            "--evidence",
            "Acceptance passed",
            "--completed-at",
            "2026-08-15",
        )

        newer = self.repo / "docs" / "work" / "features" / "newer" / "feature.md"
        newer.parent.mkdir(parents=True)
        newer.write_text("# Newer Feature\n", encoding="utf-8")
        self.run_tracker(
            "register-feature",
            "--id",
            "newer",
            "--title",
            "Newer Feature",
            "--owner",
            "gaoxiaoyi",
            "--milestone",
            "m1",
            "--path",
            "docs/work/features/newer/feature.md",
        )
        self.run_tracker(
            "close-feature",
            "--feature",
            "newer",
            "--expect-revision",
            "0",
            "--confirmed-by",
            "gaoxiaoyi",
            "--evidence",
            "Acceptance passed",
            "--completed-at",
            "2026-08-16",
        )
        self.run_tracker("render")

        completed = (self.repo / "docs" / "work" / "completed.md").read_text(
            encoding="utf-8"
        )
        self.assertLess(
            completed.index("Newer Feature"), completed.index("Agent Foundation")
        )


if __name__ == "__main__":
    unittest.main()
