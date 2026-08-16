# Expected target resolution

- Read `.waypoint/local.yaml` and resolve the current actor as `alice`.
- Filter active Feature records by owner and select `F-alice` only because it is the single match.
- Never select `F-bob` because it appears first, is ready, or was edited recently.
- If Alice owns zero or multiple active Features, stop and ask for an exact Feature ID, link, or path.
- Do not infer the target from Git history or the current branch.
