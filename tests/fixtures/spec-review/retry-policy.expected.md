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

## Behavioral contract

- The first request attempt does not consume the retry budget.
- Retried attempts and their backoff share one 800 ms budget.
- Timeout and connection-reset failures remain retryable while budget remains.
- HTTP 4xx responses remain non-retryable.

## Behavioral decisions

Exclude the first attempt from the 800 ms budget so the new limit bounds recovery work without redefining the normal request timeout.

## Error and compatibility requirements

When the budget is exhausted, expose the last transport failure together with a distinguishable retry-budget-exhausted condition. A 4xx response returns without retrying or producing the budget-exhausted condition.

---

# Task artifact update

## References

- [Specification](./spec.md)

## Acceptance

- [ ] Focused tests demonstrate budget exhaustion and non-retryable 4xx behavior.
- [ ] The existing client integration suite passes with surrounding behavior preserved.
