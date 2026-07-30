# Expected contract

- The Milestone index remains a compact global map of outcome, selection, exit criteria, linked tasks and status, dependency shape, and global gaps.
- Every confirmed task receives a non-empty task-local `task.md` with planned status, Milestone link, outcome, planning boundary, stage proof, and only real dependencies or already-known open decisions.
- The initial `task.md` is a planning handoff rather than a completed behavioral specification. When development starts, `task-spec` creates a separate spec, writes canonical Acceptance and an existing-target Reference to `task.md`, and removes superseded planning fields.
- Exit criteria link their task owners inline. No separate coverage table is created.
- Task-local details are not repeated in the Milestone index.
- Task status is the Milestone recovery signal; there is no Milestone Current Focus. Remaining work, next action, blocker, and non-obvious recovery state stay in the relevant `task.md` only when needed for a pause.
- The Milestone uses an ordered ``- `status` [Task](...)`` list. Top-to-bottom order suggests execution sequence without becoming a hard dependency. When cross-task dependencies exist, Mermaid carries them and labels completion or verification gates distinctly; no dependency section appears when every task is independent.
- Empty Discovered Work, Completion Evidence, and other unused sections are omitted.
