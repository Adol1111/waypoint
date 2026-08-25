from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "setup" / "local-work-tracker" / "scripts" / "waypoint_tracker.py"


class LocalWorkTrackerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        (self.repo / ".git").mkdir()

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

    def initialize(self, actor: str = "gaoxiaoyi") -> None:
        self.run_tracker("init", "--actor", actor, "--display-name", actor.title())

    def create_feature(self, feature_id: str, owner: str, milestone: str | None = None) -> Path:
        path = self.repo / "docs" / "work" / "features" / feature_id / "feature.md"
        path.parent.mkdir(parents=True)
        path.write_text(f"# {feature_id}\n\nHuman-owned context.\n", encoding="utf-8")
        arguments = [
            "register-feature",
            "--id",
            feature_id,
            "--title",
            feature_id.title(),
            "--summary",
            f"Outcome for {feature_id}",
            "--owner",
            owner,
            "--path",
            str(path.relative_to(self.repo)),
        ]
        if milestone:
            arguments.extend(["--milestone", milestone])
        self.run_tracker(*arguments)
        return path

    def test_identity_is_local_and_exactly_ignored(self) -> None:
        self.initialize()
        gitignore = (self.repo / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("/.waypoint/local.yaml", gitignore.splitlines())
        self.assertTrue((self.repo / ".waypoint" / "config.yaml").exists())
        whoami = json.loads(self.run_tracker("whoami").stdout)
        self.assertEqual(whoami["actor_id"], "gaoxiaoyi")
        self.assertNotIn("executor_harness", whoami)

    def test_owner_filter_returns_only_the_current_actors_features(self) -> None:
        self.initialize("alice")
        self.create_feature("alice-feature", "alice")
        self.create_feature("bob-feature", "bob")

        mine = json.loads(self.run_tracker("list-features", "--mine", "--active-only").stdout)
        self.assertEqual([feature["feature_id"] for feature in mine], ["alice-feature"])

        bob = json.loads(
            self.run_tracker("list-features", "--owner", "bob", "--active-only").stdout
        )
        self.assertEqual([feature["feature_id"] for feature in bob], ["bob-feature"])

    def test_feature_can_close_without_registered_tasks(self) -> None:
        self.initialize()
        feature_path = self.create_feature("agent-foundation", "gaoxiaoyi", "m1")
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

        dashboard = (self.repo / "docs" / "work" / "index.md").read_text(encoding="utf-8")
        completed = (self.repo / "docs" / "work" / "completed.md").read_text(encoding="utf-8")
        self.assertNotIn("Agent Foundation", dashboard)
        self.assertIn(
            "2026-08-16 — [Agent-Foundation](features/agent-foundation/feature.md) — Outcome for agent-foundation",
            completed,
        )
        self.assertTrue(feature_path.exists())
        self.assertFalse((self.repo / ".waypoint" / "tracker" / "tasks").exists())

    def test_replan_changes_only_feature_path_and_grouping(self) -> None:
        self.initialize()
        old_path = self.create_feature("agent-foundation", "gaoxiaoyi", "m1")
        new_path = self.repo / "docs" / "work" / "milestones" / "m2" / "features" / "agent-foundation" / "feature.md"
        new_path.parent.parent.mkdir(parents=True)
        old_path.parent.rename(new_path.parent)

        self.run_tracker(
            "replan-feature",
            "--feature",
            "agent-foundation",
            "--to-milestone",
            "m2",
            "--path",
            str(new_path.relative_to(self.repo)),
            "--expect-revision",
            "0",
            "--reason",
            "Move before execution",
        )
        self.run_tracker("check")

        record = (
            self.repo / ".waypoint" / "tracker" / "features" / "agent-foundation.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'path: "docs/work/milestones/m2/features/agent-foundation/feature.md"',
            record,
        )
        self.assertIn("revision: 1", record)
        self.assertFalse((self.repo / ".waypoint" / "tracker" / "tasks").exists())

    def test_task_tracking_commands_are_not_part_of_local_tracker(self) -> None:
        self.initialize()
        result = self.run_tracker("register-task", succeeds=False)
        self.assertIn("invalid choice", result.stderr)

    def test_dashboard_keeps_human_context_and_has_feature_owner_columns(self) -> None:
        self.initialize()
        feature_path = self.create_feature("standalone", "gaoxiaoyi")
        self.run_tracker("render")
        dashboard = (self.repo / "docs" / "work" / "index.md").read_text(encoding="utf-8")
        self.assertIn("| Feature | Owner | Status |", dashboard)
        self.assertIn("| [Standalone](features/standalone/feature.md) | gaoxiaoyi | planned |", dashboard)
        self.assertTrue(feature_path.read_text(encoding="utf-8").startswith("# standalone"))


if __name__ == "__main__":
    unittest.main()
