# Expected contract

- The skill must not require a docs layout, task specification, workflow, or another skill.
- It updates a suitable technical-design section in `issues/57.md` or proposes one small adjacent Markdown design.
- It preserves the supplied behavioral contract rather than inventing requirements.
- It references the behavioral contract without restating it and returns unresolved observable behavior to the specification.
- Every included section adds a review-critical implementation choice, material invariant, or consequence beyond the specification and repository conventions.
- It captures current constraints, module and interface responsibilities, data ownership and lifecycle, execution and side-effect boundaries, concurrency and failure mechanisms, genuine alternatives and rationale, and verification seams.
- It leaves mechanically derivable parsing, validation, normalization, mapping, and ordinary control flow to implementation unless their semantics define a material invariant.
- It uses pseudocode or a compact schema only if a non-trivial invariant or transition needs more precision than prose.
- It does not expand into complete code, file-by-file edits, commits, or migration sequencing.
