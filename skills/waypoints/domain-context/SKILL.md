---
name: domain-context
description: Maintain durable domain terminology and qualifying architecture decisions in repository-local Markdown. Use when repeated or ambiguous terms need a shared glossary, or when a hard-to-reverse, surprising choice among genuine alternatives needs an ADR; do not use for temporary task discussion or ordinary implementation detail.
---

# Domain Context

Preserve context that a future collaborator would otherwise have to rediscover.

## Work independently

1. Inspect repository instructions and search for an existing glossary, domain guide, decision log, or ADR convention.
2. Read only the relevant artifacts and code needed to verify the term or decision.
3. Update the existing artifact when one fits. Otherwise propose the smallest useful Markdown file and a location consistent with the repository.
4. Write in the repository's documentation language and style.
5. Report what became durable and what intentionally stayed task-local.

Do not require another skill, a `docs/` directory, a tracker, or a workflow stage. Chat may supply evidence, but facts needed to understand or review the result must appear in the artifact.

## Glossary

Add a term only when it is durable and ambiguous, overloaded, domain-specific, or repeatedly used. For each entry, capture the concise meaning, important boundaries, and aliases only when useful.

Exclude implementation mechanics, file paths likely to move, temporary task vocabulary, speculative future terms, and conversation history. Consolidate duplicate entries instead of creating parallel definitions.

Use [references/glossary-template.md](references/glossary-template.md) only when no local pattern exists.

## ADR threshold

Create an ADR only when all three conditions hold:

- the decision is expensive or risky to reverse;
- the result would be surprising without its context;
- genuine alternatives were considered.

If any condition fails, record a short rationale in the task, spec, code comment, or existing design note instead. Never inflate a routine choice into an ADR.

For a qualifying ADR, record context, decision, material alternatives, consequences, and status. Describe durable constraints and rationale, not a chronological chat transcript. Use [references/adr-template.md](references/adr-template.md) only when the repository has no ADR format.

## Companion skills

Use an installed `research` skill when external evidence is material. Use `grilling` when stakeholder terminology or decision tradeoffs require sustained clarification. These companion names refer to [mattpocock/skills](https://github.com/mattpocock/skills); install one with `npx skills add mattpocock/skills --skill <name>`. Do not reproduce those protocols here.
