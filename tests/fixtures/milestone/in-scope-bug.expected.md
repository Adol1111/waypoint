# Expected behavior

- Keep the failure in the current task because fixing it is required by that task's existing acceptance.
- During continuous work, fix it directly without adding a process-log entry.
- Fix and verify it before completing the task, or mark that task blocked.
- If work stops first, preserve only unrecoverable remaining work or the blocker in the task.
- Do not duplicate it in Milestone Discovered Work.
- Do not defer it to backlog or another task merely because it was discovered during implementation.
