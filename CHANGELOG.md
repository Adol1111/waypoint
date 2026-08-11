# waypoint-skills

## 0.3.0

### Minor Changes

- [#14](https://github.com/Adol1111/waypoint/pull/14) [`e841376`](https://github.com/Adol1111/waypoint/commit/e841376f017480655cd389257a17f710d1c50d2b) Thanks [@Adol1111](https://github.com/Adol1111)! - Replace the stateful task workflow with a shared Milestone → Feature → Task collaboration model, Feature-owned specifications and Task graphs, an explicit repository-local tracker fallback, read-only routing, and direct reuse of Matt Pocock's implementation and handoff skills. Migrate `roadmap-planning` to `milestone-planning` and `task-spec` to `feature-spec`, while preserving retired skill snapshots under `skills/deprecated/` with an explicit uninstall command.

## 0.2.5

### Patch Changes

- [#12](https://github.com/Adol1111/waypoint/pull/12) [`2a7312a`](https://github.com/Adol1111/waypoint/commit/2a7312af25d9e58ed5fc73993c2543e484ae888b) Thanks [@Adol1111](https://github.com/Adol1111)! - Load Milestone backlog, discovered-work, and closure rules only for the branches that need them, with sharper completion criteria and a single owner for each task-artifact transition.

## 0.2.4

### Patch Changes

- [#10](https://github.com/Adol1111/waypoint/pull/10) [`0d6cc89`](https://github.com/Adol1111/waypoint/commit/0d6cc891260cd49ed6751f32bcca0377dc70b02a) Thanks [@Adol1111](https://github.com/Adol1111)! - Shape standalone goals or backlog outcomes into verifiable slices, optionally enrich and score Milestone candidates, and return a user-confirmed atomic task batch with durable dependencies and complete coverage to the coordinating workflow.

## 0.2.3

### Patch Changes

- [#8](https://github.com/Adol1111/waypoint/pull/8) [`5526f7e`](https://github.com/Adol1111/waypoint/commit/5526f7e68cb844c137151ea1b3e2ec02585a0b95) Thanks [@Adol1111](https://github.com/Adol1111)! - Treat Milestone backlog as an active unresolved queue: remove promoted or durably resolved items and leave unchanged entries free of review history.

## 0.2.2

### Patch Changes

- [#6](https://github.com/Adol1111/waypoint/pull/6) [`8b1fd63`](https://github.com/Adol1111/waypoint/commit/8b1fd63461afb83ed1801f2ff25b3dc21f7d2c2c) Thanks [@Adol1111](https://github.com/Adol1111)! - Make task execution choose isolation adaptively and create cohesive verified Git checkpoints before advancing when repository and user policy permit.

- [#6](https://github.com/Adol1111/waypoint/pull/6) [`50cdc61`](https://github.com/Adol1111/waypoint/commit/50cdc61b4292940716dca12684412923ef47294e) Thanks [@Adol1111](https://github.com/Adol1111)! - Use acceptance as the durable progress record, create recovery checkpoints only at stopping boundaries, and reserve final verification for task completion.

## 0.2.1

### Patch Changes

- [#4](https://github.com/Adol1111/waypoint/pull/4) [`42685c1`](https://github.com/Adol1111/waypoint/commit/42685c1aa785fe6420fed8764f9e8baff9f513b0) Thanks [@Adol1111](https://github.com/Adol1111)! - Focus technical designs on consequential implementation choices and leave mechanically derivable work out of durable design artifacts.

- [#4](https://github.com/Adol1111/waypoint/pull/4) [`74dbe72`](https://github.com/Adol1111/waypoint/commit/74dbe7264377c00cf97c8b28822f262cef223e82) Thanks [@Adol1111](https://github.com/Adol1111)! - Reserve technical diagrams for genuinely complex relationships and make Milestone discovered-work intake scope-aware, durable, and auditable at closure.

## 0.2.0

### Minor Changes

- [#2](https://github.com/Adol1111/waypoint/pull/2) [`bc8dd46`](https://github.com/Adol1111/waypoint/commit/bc8dd46822a9857a9d1d096d46a4114aaacdc5f0) Thanks [@Adol1111](https://github.com/Adol1111)! - Add an independent technical-design waypoint and separate behavioral task specifications from review-critical architecture and implementation choices.

### Patch Changes

- [#2](https://github.com/Adol1111/waypoint/pull/2) [`a5936a8`](https://github.com/Adol1111/waypoint/commit/a5936a82dad602186b34fa78aee70855a5228e49) Thanks [@Adol1111](https://github.com/Adol1111)! - Make bootstrap completion, implementation decision gates, and next-waypoint recommendations more explicit.

## 0.1.1

### Patch Changes

- [`3a7ded6`](https://github.com/Adol1111/waypoint/commit/3a7ded6f28adef6a4ed8da36685631e080f5e47b) Thanks [@Adol1111](https://github.com/Adol1111)! - Preserve task motivation and optional selection, activation, and reconsideration context without requiring fixed Why or When fields.

- [`2dd5ed9`](https://github.com/Adol1111/waypoint/commit/2dd5ed9b7ebae5c1de87bc95306449968acd700d) Thanks [@Adol1111](https://github.com/Adol1111)! - Add Changesets-based GitHub release automation and standardize contributor tooling on pnpm.

## 0.1.0

### Minor Changes

- Launch Waypoint with six standalone engineering waypoints, two explicitly selected workflows, opt-in documentation bootstrap, bilingual installation guidance, and contract validation.
