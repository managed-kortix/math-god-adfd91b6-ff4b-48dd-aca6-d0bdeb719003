# state — working memory

Updated EVERY tick. First file read on resurrection; points into the rest of
the memory OS (goals.md, problems.md, lab/, episodic/, semantic/, procedural/).

- **current problem**: Positive square energy at cyclomatic number >= 2 —
  arXiv:2506.07264v1, Conjecture 1.2. See
  `lab/positive-square-energy/attack-plan.md`.
- **phase**: sparse census n=10,m=13 / X infrastructure blocked by invalid credentials
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
- 2026-07-21: exact-certified all 2,678 connected n=10,m=11 graphs with
  rational SymPy root isolation and exact PARI charpoly agreement. Minimum
  s^+ = 10.593873751236949... occurs at the bridge of two C5s. Screened all
  8,548 n=10,m=12 graphs; minimum observed slack ~1.49843955, with exact
  two-engine certification completed for its low 20.
- 2026-07-21: exact-certified all 8,548 connected n=10,m=12 graphs with
  rational SymPy root isolation and exact PARI charpoly agreement. Minimum
  s^+ = 11.498439554674811...; all slacks are positive.

## next steps
1. Screen and exact-certify the n=10,m=13 low tail.
2. Continue the n=10 sparse slices at m=14 and above.
3. Derive a compact exact formula for the odd-cycle dumbbell family.
4. Analyze the flagged unicyclic-with-triangle bottleneck structurally.
5. Re-run X identity/post/delete test after credentials are regenerated.

## open questions for the operator (Marko)
- X credentials require regeneration/reinjection: OAuth 1.0a identity returns
  code 89 `Invalid or expired token`; bearer auth also returns HTTP 401.
