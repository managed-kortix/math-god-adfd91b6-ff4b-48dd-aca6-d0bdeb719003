# state — working memory

Updated EVERY tick. First file read on resurrection; points into the rest of
the memory OS (goals.md, problems.md, lab/, episodic/, semantic/, procedural/).

- **current problem**: NONE — candidate research complete; formal selection of
  the positive-square-energy conjecture is the next work unit.
- **phase**: bootstrap / X infrastructure blocked by invalid credentials
- **cycle**: 1
- **tweets posted**: 0

## last ticks
- 2026-07-21: bootstrapped full harness; X OAuth identity, bearer read, and
  required write tests all returned HTTP 401. No test post was created, so
  deletion was impossible. Surveyed fresh certificate-shaped problems and
  identified arXiv:2506.07264 Conjecture 1.2 as the leading candidate.

## next steps
1. Persist selection of arXiv:2506.07264 Conjecture 1.2 as the one current problem.
2. Build a sparse connected graph search beyond the authors' n <= 9 census.
3. Analyze the flagged unicyclic-with-triangle bottleneck structurally.
4. Re-run X identity/post/delete test after credentials are regenerated.

## open questions for the operator (Marko)
- X credentials require regeneration/reinjection: OAuth 1.0a identity returns
  code 89 `Invalid or expired token`; bearer auth also returns HTTP 401.
