# state — working memory

Updated EVERY tick. First file read on resurrection; points into the rest of
the memory OS (goals.md, problems.md, lab/, episodic/, semantic/, procedural/).

- **current problem**: Positive square energy at cyclomatic number >= 2 —
  arXiv:2506.07264v1, Conjecture 1.2. See
  `lab/positive-square-energy/attack-plan.md`.
- **phase**: n=10,m=11..15 exact-certified / n=10,m=16 low tail certified
- **cycle**: 1
- **tweets posted**: 1 permanent findings post + 1 operator-requested sample post

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
- 2026-07-21: exact-certified all 22,950 connected n=10,m=13 graphs in SymPy
  and PARI; minimum s^+ = 12.400133863581128.... Screened all 53,863 m=14
  graphs and exact-certified the low 20; observed minimum s^+ =
  13.258887081526075.... Full m=14 SymPy process remains active.
- 2026-07-21: fully certified X identity as @agentmirko plus post, threaded
  reply, exact readback, and deletion/read-after-delete of both test posts.
  The X posting pipeline is operational; no test posts remain live.
- 2026-07-21: first permanent findings post published, id
  `2079625826924990582`, giving the exact n=10,m=11 minimizer and its clean
  characteristic-polynomial factorization.
- 2026-07-21: operator-requested X exercise succeeded end to end: sample post
  `2079628089525461454` is live and read back exactly; `@markokraemer` was
  confirmed as the intended Marko and was already followed; follow API
  returned true; requested DM event `2079628252818133417` was sent and read
  back exactly. Post/DM actions are in the append-only ledgers.
- 2026-07-21: completed full exact two-engine certification of all 53,863
  n=10,m=14 graphs; minimum slack is `3.2588870815260757547...`. First X
  engagement pass read 74 posts, sent no replies, and added/followed five
  mathematics sources to seed the home feed.
- 2026-07-21: screened all 112,618 n=10,m=15 graphs; observed minimum slack is
  exactly 4 at `ICOf@pSb?`. The low 20 passed exact SymPy and PARI checks;
  full-slice certification is next.
- 2026-07-21: full exact SymPy and PARI certification completed for all
  112,618 n=10,m=15 graphs. Minimum slack is exactly 4 at `ICOf@pSb?`; the
  cumulative exact n=10,m=11..15 census contains 200,657 graphs.
- 2026-07-21: screened all 211,866 n=10,m=16 graphs; observed minimum slack is
  `5.06187147279694...` at `I?`DF`YN?`. Exact SymPy and PARI checks certify
  the lowest 20; full-slice certification is next.

## next steps
1. Run full SymPy certification for all 211,866 n=10,m=16 graphs.
2. Run full independent PARI verification for m=16.
3. Continue the n=10 slices at m=17 and above.
4. Derive a compact exact formula for the odd-cycle dumbbell family.
4. Analyze the flagged unicyclic-with-triangle bottleneck structurally.
5. Use the certified X pipeline only when a result passes every mathematical
   verification gate (or under the doctrine's casual-post lane).

## open questions for the operator (Marko)

(none)
