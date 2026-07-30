# Expected behavior

- Closure is allowed.
- The workflow rechecks every discovered item individually.
- Backlog and later-Milestone items retain only durable destination links; discarded items retain reasons.
- Findings resolved by current tasks are removed because their task artifacts already own the history.
- Follow-up work placed in backlog or a later Milestone does not block closure.
- The workflow moves the Milestone to completed state and preserves Completion Evidence only for ownerless cross-task proof.
- It does not require a commit, branch action, or fixed review pause.
