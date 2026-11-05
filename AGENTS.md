# Hedley agent instructions

Hedley is an experimental communication language for a developer and an AI
collaborator. Optimize for a compact causal model the developer can mentally
execute, not for language completeness.

## Required reading

Before proposing or editing Hedley, read:

1. `README.md`
2. `spec/v0.2-intent.hedley`
3. the smallest relevant example

The v0.1 lease experiment is historical evidence, not the current language
specification.

## Communication contract

- When the user selects Hedley for a discussion, communicate the semantic model
  in Hedley. Do not silently complete missing semantics with English, Python,
  pseudocode, or implementation details.
- If Hedley cannot express a necessary claim, emit a `language_gap`. Explain or
  extend the notation only after the gap is visible.
- Default to the smallest contract that captures the current decision. Keep the
  main reading path near one screen when practical. Move detailed evidence,
  correspondence, and uncommon failure paths into referenced blocks or files.
- Do not restate source code line by line. Include only state, cases, effects,
  invariants, failure boundaries, and unknowns that affect reasoning.
- Use stable IDs for operations, cases, properties, gaps, and evidence so the
  human and agent can refer to the same claim without repeating it.

## Semantic boundaries

- `rule` models an internal state transition. A false `enabled when` guard only
  blocks that transition; it never implies an error, exception, or response.
- `operation` models an externally invoked behavior. Its cases must state their
  outcomes explicitly and should be disjoint and exhaustive.
- `workflow` models important intermediate phases, commit points, partial
  effects, interruption, or recovery. Do not expand an atomic operation into a
  workflow unless those details affect a decision or guarantee.
- `adapter` maps semantic outcomes to protocol-visible behavior such as exit
  codes, diagnostics, HTTP responses, MCP responses, or UI messages.
- `correspondence` maps a contract claim to stable implementation symbols and
  evidence. Correspondence must be inspected; it cannot be inferred from names.
- `evidence` states what was checked and its limits. Keep `PROPOSED`,
  `SOURCE_INSPECTED`, `TESTED`, `MODEL_CHECKED`, and `PROVED` distinct.

## Human ownership

- Separate user-confirmed intent, agent proposals, observed implementation, and
  unresolved decisions.
- Prefer retrieval questions that reference Hedley IDs. Evaluate answers only
  against the referenced contract, never against unstated implementation facts.
- A readable model is not evidence of comprehension. A passing test is not
  evidence of contract-to-implementation correspondence.

## Repository discipline

- Preserve experiments as experiments; do not upgrade them into a specification
  without an explicit decision.
- Do not build a parser, type system, editor, or proof integration merely because
  it is an attractive language-design problem. Let repeated real-work friction
  justify each addition.
- For the lease experiment, run `python experiments/lease-v0.1/explore.py
  --self-test` after changes and report its finite scope accurately.

