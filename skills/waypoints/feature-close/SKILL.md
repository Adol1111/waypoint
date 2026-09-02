---
name: feature-close
description: Verify and close one completed Feature across its Task, Feature, and optional Milestone Acceptance records, then coordinate safe integration and cleanup without forcing a workflow.
---

# Feature Close

Finish one explicitly targeted Feature after any implementation skill, agent team, or human execution path reports that it is done. This is a closeout gate, not an implementation workflow.

## Resolve the target

1. Read repository instructions, the exact Feature record, its Task plan and child Task records, the optional Milestone, configured tracker, and current Git branch/worktree state.
2. Prefer a Feature ID, link, path, or name from the request. Otherwise resolve the current actor from the request, `.waypoint/local.yaml`, or the external tracker and filter active Features by owner.
3. Continue only when exactly one Feature remains. Ask when none or several remain. Never choose another owner's Feature, the first ready item, recent work, Git history, or branch naming.
4. Reuse the Feature owner from its record or tracker. Only that owner may confirm Feature completion.

## Audit completion before integration

Treat Acceptance as the durable completion checklist. Inspect every applicable checkbox and its evidence; do not infer completion from a successful build, a commit, or an implementation agent's done message.

- **Task:** for every child Task, require every Task Acceptance item to be `[x]`, task-local verification to pass, review corrections to be resolved, and any required Task integration to be complete. An unsplit Feature has no Task-level gate.
- **Feature:** require every Feature Acceptance item to be `[x]`, the Feature-level verification and integration proof to be recorded, and no unresolved blocker to remain.
- **Milestone:** when the Feature belongs to a Milestone, require the Feature's Milestone entry and every exit criterion it owns to be `[x]` or explicitly covered by the accepted Feature evidence. Do not close a Milestone merely because this Feature is complete; sibling Features and remaining exit criteria still belong to the coordinator.

If evidence is present but a corresponding authoritative checkbox is stale, update that checkbox in its owning artifact. If evidence is missing, the checkbox is not complete, or discovered work has no accepted destination, stop and report the exact blocker. Never check an item merely to make the tree look complete.

## Gate integration and cleanup

Do not merge until every applicable Task, Feature, and Feature-owned Milestone Acceptance item is `[x]` and the corresponding verification/review evidence is present. An unchecked item that belongs to another sibling Feature does not block this Feature, but it does block Milestone closure.

After the pre-merge audit passes:

1. Report whether the exact Feature/Task MR is already merged, ready to merge, or absent, including source and destination branches and uncommitted files.
2. If a specific MR must be merged, ask for fresh confirmation naming that MR and destination. Do not treat `ok`, `continue`, implementation approval, or automatic tool approval as merge authorization.
3. After confirmed integration, record Task and Feature completion evidence in their existing authority. If local tracking is configured, close the exact Feature through `local-work-tracker` and render its views; otherwise update the repository-native Feature/Milestone artifacts without creating a second tracker. The Feature owner confirms Feature completion; the Milestone coordinator confirms Milestone closure.
4. Offer branch/worktree cleanup only after merge state is known. Deleting each exact branch or worktree requires separate target-specific confirmation. Never delete or discard unrelated uncommitted files; preserve them and report them.

Keep the Feature directory as its detailed history. Remove it from an active Feature view and add it to the repository's completed-Feature history only through the existing Milestone/tracker convention. A completed Feature may live without a Milestone.

## Stop conditions

Return a compact closeout report containing:

- Task, Feature, and Milestone Acceptance results;
- verification, review, integration, and discovered-work blockers;
- exact merge decision and required confirmation, if any;
- exact cleanup candidates and required confirmation, if any;
- state changes already made and remaining next action.

Do not invoke implementation, specification, Task planning, or Milestone replanning. Do not merge, delete, or discard without the required exact confirmation.
