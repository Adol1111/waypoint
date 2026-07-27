# Source task

Add a per-request retry budget to the HTTP client.

Current facts:

- `client/retry.go` owns retry decisions.
- Timeouts and connection resets are retryable.
- HTTP 4xx responses are not retryable.

Decisions:

- The total retry budget is 800 ms, including backoff but excluding the first attempt.
- Exhaustion returns the last transport error wrapped with `ErrRetryBudgetExceeded`.
- This task does not add per-endpoint configuration or change server behavior.

Proof:

- focused unit tests for budget exhaustion and non-retryable 4xx;
- the existing client integration suite remains passing.

Write a compact task spec for a reviewer who cannot see this fixture.
