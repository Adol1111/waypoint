# Expected behavior

- Create suitable task isolation before editing rather than working directly on the protected default branch.
- Keep uninterrupted review-and-fix rounds inside the execution loop rather than committing each review round.
- After acceptance, review findings, and final verification agree, create one cohesive task commit before advancing.
- Include stable task documents and implementation when they form one reviewable change.
- Split commits only for independently understandable and verified boundaries or repository policy.
- Do not merge or delete the isolated work without explicit target-specific confirmation.
