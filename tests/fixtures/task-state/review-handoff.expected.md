# Expected behavior

- Record the unresolved token refresh race, its affected surface, and the required concurrency outcome.
- Set the Recovery checkpoint to addressing that finding and requesting review again.
- Do not preserve resolved review comments or create a chronology of review rounds.
- If the finding already existed in a durable PR or review system, link it instead of duplicating it.
- Do not record whether grilling, specification, design, or planning occurred.
- Keep the task `in-progress` until acceptance and final verification are complete.
