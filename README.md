# Hedley

Hedley is an experiment in code-shaped communication between a developer and
an AI collaborator. A Hedley document describes behavior at a higher level
than implementation syntax while keeping intent, implementation, and evidence
separate.

The language is provisional. There is no parser, and persuasive notation is
not proof that production code behaves the same way.

## Start here

1. Read [`spec/v0.2-intent.hedley`](spec/v0.2-intent.hedley).
2. Read [`examples/wander-import-v0.2.hedley`](examples/wander-import-v0.2.hedley).
3. For the original finite-model experiment, run:

   ```powershell
   python .\experiments\lease-v0.1\explore.py --self-test
   python .\experiments\lease-v0.1\explore.py `
       --trace 'claim A;expire;claim B;complete A;complete B'
   ```

The v0.1 notation and Python model are manually synchronized. Their
correspondence is a review obligation, not an established fact.

## Current direction

Hedley should be compact enough to read as code:

- model only state that changes a decision or guarantee;
- use explicit operation outcomes instead of inferring errors from guards;
- use workflows only when partial effects, interruption, or recovery matter;
- attach implementation and evidence through correspondence records;
- record missing language capability as a `language_gap` rather than filling it
  with prose or another programming language.

The first objective is useful communication during real work. A parser, proof
system, editor, and visual projections remain experiments to justify through
use rather than assumed requirements.

