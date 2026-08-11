# Implementation Plan Template

Use only for real execution risk. Omit irrelevant headings and never prescribe commits.

```md
# <Feature or Task> Implementation Plan

Execution unit: <link to the assigned Feature or Task and authoritative Acceptance>

## Strategy

<Execution approach and why sequence matters.>

## Change map

- `<surface>`: <responsibility of the change>

## Ordered slices

### 1. <Stable outcome>

- Changes: <bounded work>
- Constraints: <compatibility or coordination boundary>
- Stable state: <safe, reviewable state that remains after this slice>
- Verification: <proof before the next slice>

## Risk, containment, and rollback

- Risk: <failure mode>
- Containment: <how exposure is limited>
- Rollback/recovery: <safe reversal or forward-repair path>

## Final verification

- <end-to-end or release-level evidence>
```
