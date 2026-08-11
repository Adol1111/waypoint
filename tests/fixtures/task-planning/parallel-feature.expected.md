# Expected contract

- Present the draft before writing durable task artifacts.
- Define the shared event and endpoint contracts before treating producer, query, and viewer work as parallel.
- Audit coverage and identify ownership overlap or shared mutable surfaces.
- Show real blockers and distinguish them from recommended list order.
- Ask about task granularity, dependencies, overlap, and any integration proof; publish only after user approval.
- Report which confirmed tasks are ready, blocked, or safely parallelizable.
- Treat automatic tool approval as a tool-layer setting and stop without modifying production code.
