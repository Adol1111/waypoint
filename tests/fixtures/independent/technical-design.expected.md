# Expected contract

- The skill must not require a docs layout, task specification, workflow, or another skill.
- It updates a suitable technical-design section in `issues/57.md` or proposes one small adjacent Markdown design.
- It preserves the supplied behavioral contract rather than inventing requirements.
- It references the behavioral contract without restating it and returns unresolved observable behavior to the specification.
- Every included section adds a review-critical implementation choice, material invariant, or consequence beyond the specification and repository conventions.
- It captures current constraints, module and interface responsibilities, data ownership and lifecycle, execution and side-effect boundaries, concurrency and failure mechanisms, genuine alternatives and rationale, and verification seams.
- It leaves mechanically derivable parsing, validation, normalization, mapping, and ordinary control flow to implementation unless their semantics define a material invariant.
- For material relational persistence changes, it records tables, logical column types, keys, nullability/defaults, constraints, justified indexes, ownership, and migration or compatibility impact.
- For material durable payloads, it records shape, identity/versioning, producer/consumer ownership, compatibility, and a representative payload when useful.
- It uses a state table or diagram for material lifecycle transitions, a flowchart for branching or failure paths, a sequence diagram for cross-boundary ordering and async behavior, and a component diagram for ownership or dependency boundaries.
- Diagrams use repository-native diffable formats such as Mermaid when supported, consistent terminology, and an explanation of the decision or invariant they clarify; a single linear sequence stays prose or a short ordered list.
- It uses pseudocode only if a non-trivial algorithm or protocol needs more precision than prose.
- It does not expand into complete code, file-by-file edits, commits, or migration sequencing.
