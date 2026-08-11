# Discovered Work and Closure

Read this reference when a finding may outlive its current task, when handing off unresolved findings, or before closing a Milestone.

## Place a finding

Compare the finding with durable task ownership:

1. Keep a correction required for the current task's Acceptance or correctness in that task. Fix it during continuous work; if work stops, preserve only the unresolved Recovery or Blocker.
2. Put a finding explicitly owned by another current Milestone task directly into that task's scope or Acceptance.
3. Put one concise entry in Milestone Discovered Work only when the Milestone cannot handle the finding now or its owner is uncertain.

Discovered Work contains durable out-of-scope or unowned concerns that affect correctness, exit criteria, compatibility, migration, operations, or future capability. Each entry needs only enough detail to understand the concern and decide its owner.

Placement is complete when the finding has exactly one durable owner. Ask before changing product intent, exit criteria, or a consequential delivery boundary.

## Audit for closure

Check every Discovered Work entry:

- route concrete unresolved work to backlog, Future Directions, or another Milestone, retaining only the disposition and destination link;
- remove an entry resolved inside a current task because that task owns its history;
- retain a concrete reason for a discarded entry.

The audit is complete when every entry has been removed or has a durable destination or discard reason. An unowned entry, missing destination, or unexplained discard blocks closure; follow-up work with a durable destination does not.

After the audit, apply the completion and compaction rules in [milestone-artifact.md](milestone-artifact.md).
