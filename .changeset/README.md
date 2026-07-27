# Changesets

Each user-visible skill or workflow change should include one Markdown fragment in this directory.

Run `pnpm changeset`, select `waypoint-skills`, choose `patch`, `minor`, or `major`, and write a concise release-note summary. The release workflow collects pending fragments into a Version PR, updates `CHANGELOG.md`, and removes consumed fragments.

Do not edit generated version entries by hand when a pending changeset can express the change.
