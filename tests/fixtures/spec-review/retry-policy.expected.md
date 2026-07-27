# Per-request Retry Budget Specification

## Intent

Bound HTTP retry time per request so transient failures cannot consume unbounded client time.

## Scope

- Apply one 800 ms retry budget to retries and backoff after the first attempt.
- Keep timeouts and connection resets retryable within the remaining budget.
- Keep HTTP 4xx responses non-retryable.

## Non-goals

- Per-endpoint retry configuration.
- Server-side behavior changes.

## Implementation surface

`client/retry.go` remains the owner of retry classification and budget enforcement.

## Decision and rationale

Exclude the first attempt from the 800 ms budget so the new limit bounds recovery work without redefining the normal request timeout. Keep classification in the existing retry owner to avoid a second policy source.

## Error behavior

When the budget is exhausted, return the last transport error wrapped with `ErrRetryBudgetExceeded`. A 4xx response returns without retrying or producing the budget error.

## Completion proof

- Focused unit tests demonstrate budget exhaustion and non-retryable 4xx behavior.
- The existing client integration suite passes, demonstrating preserved surrounding behavior.
