# Feature Spec Template

Use the smallest subset that lets a reviewer and every child Task work without chat history.

```md
# <Feature> Specification

Feature: <stable Feature ID and link>

## Intent

<Problem or motivation, desired outcome, actors, and why it matters.>

## Scope

- <Required behavior>

## Non-goals

- <Tempting adjacent behavior that is excluded>

## Behavioral contract

- <Observable input, output, rule, or state transition>

## Representative scenarios

- <Compact success, failure, or edge case that clarifies a material decision>

## Error and compatibility requirements

<Only externally observable failure or compatibility behavior.>

## Constraints

<Externally imposed constraint only when it limits an acceptable solution.>
```

When `feature.md` exists, keep canonical Acceptance there. Otherwise add a compact `Acceptance` section here. Omit unused sections and do not add implementation decisions, internal interfaces, schema, algorithms, Task decomposition, file paths, or an exhaustive user-story inventory.
