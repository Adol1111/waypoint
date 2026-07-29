# Expected behavior

- Make the new Milestone or one of its tasks explicitly own token rotation before removing that backlog entry, then update its source discovered-work destination.
- Verify retry telemetry's durable completion evidence, update its source discovered-work resolution, and remove that backlog entry.
- Leave the regional failover entry untouched because its outcome and reconsideration signal have not changed.
- Add no review date, retained disposition, or review-history entry for regional failover.
- Preserve history in the source Milestones and completed task rather than in backlog.
- Never delete a backlog entry before its replacement ownership or resolution evidence is durable.
