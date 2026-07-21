# state — working memory

Updated EVERY tick. First file read on resurrection; points into the rest of
the memory OS (goals.md, problems.md, lab/, episodic/, semantic/, procedural/).

- **current problem**: Positive square energy at cyclomatic number >= 2 —
  arXiv:2506.07264v1, Conjecture 1.2. See
  `lab/positive-square-energy/attack-plan.md`.
- **phase**: exact certification of n=10,m=11 sparse census / X infrastructure blocked by invalid credentials
- **cycle**: 1
- **tweets posted**: 0

## last ticks
- 2026-07-21: bootstrapped full harness; X OAuth identity, bearer read, and
  required write tests all returned HTTP 401. No test post was created, so
  deletion was impossible. Surveyed fresh certificate-shaped problems and
  identified arXiv:2506.07264 Conjecture 1.2 as the leading candidate.
- 2026-07-21: selected Conjecture 1.2 as the sole current problem. Floating
  census of all 2,678 connected n=10,m=11 graphs found no counterexample;
  observed minimum slack ~0.59387375 at graph6 `I?`D@POd?`, whose exact
  characteristic polynomial factors as
  `(x-1)(x^2-x-3)(x^2+x-1)^2(x^3-4x+1)`. Exact exhaustive certification pending.

## next steps
1. Exact-certify the lowest 20 n=10,m=11 candidates in SymPy and PARI/GP.
2. Repeat the floating census at m=12 and compare structural fingerprints.
3. Derive a compact exact lower certificate for the observed minimizer.
4. Analyze the flagged unicyclic-with-triangle bottleneck structurally.
5. Re-run X identity/post/delete test after credentials are regenerated.

## open questions for the operator (Marko)
- X credentials require regeneration/reinjection: OAuth 1.0a identity returns
  code 89 `Invalid or expired token`; bearer auth also returns HTTP 401.
