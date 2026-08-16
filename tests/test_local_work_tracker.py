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
        feature_dir = (
            self.repo
            / "docs"
            / "work"
            / "milestones"
            / "m1"
            / "features"
            / "agent-foundation"
        )
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
            "docs/work/milestones/m1/features/agent-foundation/feature.md",
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
            "docs/work/milestones/m1/features/agent-foundation/tasks/contract/task.md",
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
            "docs/work/milestones/m1/features/agent-foundation/tasks/runtime/task.md",
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

    def test_standalone_feature_does_not_require_milestone(self) -> None:
        self.run_tracker("init", "--actor", "gaoxiaoyi")
        feature = self.repo / "docs" / "work" / "features" / "standalone" / "feature.md"
        feature.parent.mkdir(parents=True)
        feature.write_text("# Standalone\n", encoding="utf-8")
        self.run_tracker(
            "register-feature",
            "--id",
            "standalone",
            "--title",
            "Standalone",
            "--owner",
            "gaoxiaoyi",
            "--path",
            "docs/work/features/standalone/feature.md",
        )
        self.run_tracker("render")
        self.run_tracker("check")
        dashboard = (self.repo / "docs" / "work" / "index.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("### Unscheduled", dashboard)
        self.assertIn("| Feature | Owner | Status | Tasks |", dashboard)
        self.assertIn("features/standalone/feature.md", dashboard)

    def test_planned_feature_move_rebases_task_paths(self) -> None:
        self.initialize_and_register()
        old_directory = (
            self.repo
            / "docs"
            / "work"
            / "milestones"
            / "m1"
            / "features"
            / "agent-foundation"
        )
        new_directory = (
            self.repo
            / "docs"
            / "work"
            / "milestones"
            / "m2"
            / "features"
            / "agent-foundation"
        )
        new_directory.parent.mkdir(parents=True)
        old_directory.rename(new_directory)
        self.run_tracker(
            "replan-feature",
            "--feature",
            "agent-foundation",
            "--to-milestone",
            "m2",
            "--path",
            "docs/work/milestones/m2/features/agent-foundation/feature.md",
            "--expect-revision",
            "0",
            "--reason",
            "Move the planned Feature",
        )
        self.run_tracker("render")
        self.run_tracker("check")

        task_record = (
            self.repo
            / ".waypoint"
            / "tracker"
            / "tasks"
            / "agent-foundation"
            / "contract.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'path: "docs/work/milestones/m2/features/agent-foundation/tasks/contract/task.md"',
            task_record,
        )
        self.assertIn("revision: 1", task_record)
        feature = (new_directory / "feature.md").read_text(encoding="utf-8")
        self.assertIn("[Freeze contract](tasks/contract/task.md)", feature)

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
            self.repo
            / "docs"
            / "work"
            / "milestones"
            / "m1"
            / "features"
            / "agent-foundation"
            / "feature.md"
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
            "2026-08-16 — [Agent Foundation](milestones/m1/features/agent-foundation/feature.md) — Enable shared agent delivery",
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
            "docs/work/milestones/m1/features/agent-foundation/feature.md",
        )
        old_directory = (
            self.repo
            / "docs"
            / "work"
            / "milestones"
            / "m1"
            / "features"
            / "agent-foundation"
        )
        new_directory = (
            self.repo
            / "docs"
            / "work"
            / "milestones"
            / "m2"
            / "features"
            / "agent-foundation"
        )
        new_directory.parent.mkdir(parents=True)
        old_directory.rename(new_directory)
        self.run_tracker(
            "replan-feature",
            "--feature",
            "agent-foundation",
            "--to-milestone",
            "m2",
            "--path",
            "docs/work/milestones/m2/features/agent-foundation/feature.md",
            "--expect-revision",
            "0",
            "--reason",
            "Move before execution",
        )
        self.run_tracker(
            "transition-feature",
            "--feature",
            "agent-foundation",
            "--to",
            "in-progress",
            "--expect-revision",
            "1",
        )
        self.run_tracker(
            "replan-feature",
            "--feature",
            "agent-foundation",
            "--to-milestone",
            "m3",
            "--expect-revision",
            "2",
            "--reason",
            "Carry active work without moving it",
        )
        self.run_tracker(
            "replan-feature",
            "--feature",
            "agent-foundation",
            "--standalone",
            "--expect-revision",
            "3",
            "--reason",
            "Remove it from Milestone scope without moving active work",
        )
        self.run_tracker("render")
        dashboard = (self.repo / "docs" / "work" / "index.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("### m3", dashboard)
        self.assertNotIn("### Unscheduled", dashboard)
        self.assertIn("in-progress", dashboard)
        feature_record = (
            self.repo
            / ".waypoint"
            / "tracker"
            / "features"
            / "agent-foundation.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'path: "docs/work/milestones/m2/features/agent-foundation/feature.md"',
            feature_record,
        )

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
            "docs/work/milestones/m1/features/agent-foundation/feature.md",
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

        newer = (
            self.repo
            / "docs"
            / "work"
            / "milestones"
            / "m1"
            / "features"
            / "newer"
            / "feature.md"
        )
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
            "docs/work/milestones/m1/features/newer/feature.md",
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
