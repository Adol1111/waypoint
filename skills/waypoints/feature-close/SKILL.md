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

Treat Acceptance as the durable completion checklist and each existing mark as a claim to verify. Proactively determine whether every applicable item deserves `[x]`, including items currently marked `[ ]`, without waiting for a separate request to check the implementation.

For each item:

1. Read its acceptance requirement and relevant Feature spec or Task contract, then identify the observable condition that would satisfy it.
2. Inspect the relevant implementation and verification/review/integration evidence against that condition. Confirm that evidence applies to the current implementation and covers the whole item, including required failure cases and boundaries. A successful build, a commit, or an implementation agent's done message alone does not prove acceptance.
3. Reuse sufficient current evidence; where it is missing, stale, or incomplete, actively run the relevant available checks or inspect the behavior. If verification requires unavailable access, an environment, or human judgment, record the exact unverified condition and what is needed to resolve it. Missing evidence starts verification rather than ending the audit.
4. Record an item-level verdict with concrete evidence references, such as implementation paths, commands and results, or review/integration records. Mark a proven item `[x]` in its owning artifact. Leave an unmet or unverified item `[ ]`; if it was `[x]`, clear the stale mark and record the failure or evidence gap. Preserve the acceptance requirement itself.

Apply this audit at each relevant level:

The following are final closeout requirements. If an item can only be satisfied by the exact integration now being considered, keep it unchecked and record it as pending that integration, with its post-integration check. Such an item does not block presenting or confirming integration when all pre-integration requirements pass; it still blocks final Feature completion. Apply this distinction to completion entries at every level. Failing checks, missing implementation, and unresolved review findings remain pre-integration blockers.

- **Task:** for every child Task, require every Task Acceptance item to be `[x]`, task-local verification to pass, review corrections to be resolved, and any required Task integration to be complete. An unsplit Feature has no Task-level gate.
- **Feature:** require every Feature Acceptance item to be `[x]`, the Feature-level verification and integration proof to be recorded, and no unresolved blocker to remain.
- **Milestone:** when the Feature belongs to a Milestone, require the Feature's Milestone entry and every exit criterion it owns to be `[x]` or explicitly covered by the accepted Feature evidence. Do not close a Milestone merely because this Feature is complete; sibling Features and remaining exit criteria still belong to the coordinator.

Finish all independently verifiable items even when another item is blocked. Stop before offering integration if any pre-integration requirement remains unmet or unverified, or discovered work has no accepted destination, and report the exact blockers. Verification and evidence-backed checkbox corrections are part of this audit; implementation fixes remain outside this skill's scope.

## Gate integration and cleanup

Do not merge until every applicable Task, Feature, and Feature-owned Milestone Acceptance item required before integration is `[x]` and the corresponding verification/review evidence is present. An unchecked item that belongs to another sibling Feature does not block this Feature, but it does block Milestone closure.

After the pre-merge audit passes:

1. Resolve the source branch or detached HEAD, destination branch, exact Feature/Task PR or MR and its merge readiness, worktree path, and uncommitted files, including audit edits. Use the existing request, records, and repository configuration to resolve the destination; ask if it remains ambiguous.
2. Actively ask the user how to finish, with concrete options appropriate to that state. Do not end with only a passing audit or a suggestion that the user invoke another command. Offer:
   - Merge the exact ready PR/MR into its named destination, or merge the named source into the named destination locally when repository policy allows it.
   - Push the named branch and create a PR/MR against the named destination when none exists. For an existing PR/MR awaiting review or CI, offer to leave it open and report what remains. For detached HEAD, resolve a branch name before proposing publication.
   - Keep the branch/worktree as-is for later.
   Omit inapplicable options. If integration is already complete, proceed to completion recording and ask about applicable cleanup instead of offering another merge. Discard is only a response to an explicit user request.
3. Wait for the integration choice unless the user has already explicitly authorized the exact action and targets. For an MR merge without that authorization, ask for fresh confirmation naming that MR and destination; for a local merge, name both branches. Selecting an option that explicitly names the merge and its targets is sufficient confirmation for that merge; do not ask twice. Do not treat `ok`, `continue`, implementation approval, or automatic tool approval as merge authorization. Execute the selected action within its scope. Creating a PR/MR or choosing to keep the work leaves the Feature awaiting integration and preserves its branch/worktree.
4. After integration, verify the resulting state and all deferred Acceptance items before marking them complete. If checks fail, report the failure and preserve the branch/worktree. Once all final closeout requirements pass, record Task and Feature completion evidence in their existing authority. If local tracking is configured, close the exact Feature through `local-work-tracker` and render its views; otherwise update the repository-native Feature/Milestone artifacts without creating a second tracker. The Feature owner confirms Feature completion; the Milestone coordinator confirms Milestone closure.
5. After verified integration, actively ask whether to remove the exact eligible branch/worktree or keep it. Deleting each exact branch or worktree requires separate target-specific confirmation; merge approval does not authorize cleanup. Preserve externally managed workspaces unless explicitly authorized for cleanup. Never delete or discard unrelated uncommitted files; preserve them and report them.

Keep the Feature directory as its detailed history. Remove it from an active Feature view and add it to the repository's completed-Feature history only through the existing Milestone/tracker convention. A completed Feature may live without a Milestone.

## Stop conditions

Return a compact closeout report containing:

- Task, Feature, and Milestone Acceptance results, with each item's verdict, evidence reference, and any checkbox correction;
- verification, review, integration, and discovered-work blockers;
- exact merge decision and required confirmation, if any;
- exact cleanup candidates and required confirmation, if any;
- state changes already made and remaining next action.

When a ready integration or cleanup decision is still pending, include the concrete question and applicable options in the report so the user can answer directly.

Do not invoke implementation, specification, Task planning, or Milestone replanning. Do not merge, delete, or discard without the required exact confirmation.
