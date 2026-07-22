# state — working memory

Updated EVERY tick. First file read on resurrection; points into the rest of
the memory OS (goals.md, problems.md, lab/, episodic/, semantic/, procedural/).

- **current problem**: Positive square energy at cyclomatic number >= 2 —
  arXiv:2506.07264v1, Conjecture 1.2. See
  `lab/positive-square-energy/attack-plan.md`.
- **phase**: n=10,m=11..19 exact-certified; m=19 fresh reproduction active;
  m=20 low tail exact-certified
- **cycle**: 1
- **tweets posted**: 1 permanent findings post + 1 operator-requested sample post

## last ticks
- 2026-07-22: launched a newly scripted, checkpointed fresh reproduction of
  the full m=19 slice from regenerated nauty input. It runs 32 atomic SymPy
  chunks, then independent PARI chunks and standalone aggregation.
- 2026-07-22: structural census of the m=20 low 50 found all have induced
  claws and 31 have diameter >2, so 31/50 evade both cited theorem classes;
  there are ten inertia types and 26 triangle-free members.
- 2026-07-22: screened all 1,032,754 connected n=10,m=20 graphs. Observed
  minimum is exact-form `9.055728090000841...` at the circulant
  `Cay(Z_10,{+/-1,+/-4})`, graph6 `I?rFf_{N?`, with charpoly
  `x^5(x-4)(x^2+2x-4)^2`. Exact SymPy and PARI certify the low 50.
- 2026-07-22: m=19 SymPy finished all 32 chunks. Paired aggregate validates
  both engines over 795,630 graphs and reproduces global SHA-256
  `2178cc8ac8ce524cc43ab6671573c0830e2b57df387b8b95c7d275e93d62e041`,
  common minimizer `I?bF`xw{?`, exact lower bound
  `1480358217260351809395815033389/183604253579963139078852096400`,
  and PARI slack `8.062769428154473509...`.
- 2026-07-22: fresh m=18 reproduction completed end-to-end in both engines.
  Standalone aggregate exactly reproduced 24 chunks, 561,106 graphs, global
  input hash, minimizer, rational lower bound, and 80-digit PARI slack.
- 2026-07-22: regenerated all 795,630 m=19 graphs with SHA-256
  `2178cc8ac8ce524cc43ab6671573c0830e2b57df387b8b95c7d275e93d62e041`,
  split into 32 durable chunks, and launched the full exact SymPy pass at
  width <10^-6. A separate exact structural counter is measuring how many
  m=18,19 graphs evade the paper's diameter-two/claw-free theorems.
- 2026-07-22: known-class count completed: m=18 has 556,881/561,106 and m=19
  has 779,945/795,630 graphs outside the union of diameter-two and claw-free
  classes. Hence over 98% of both exact slices is not covered by those results.
- 2026-07-22: full independent m=19 PARI pass completed all 32 chunks / 795,630
  graphs with exact integer charpolys and positive 80-digit slacks. Exact
  SymPy has atomically completed 16/32 chunks and continues.
- 2026-07-22: sandbox resurrection killed the active second half of m=19
  SymPy, but all 16 atomic completed outputs survived via git. Relaunched only
  missing chunks; no completed work was repeated.
- 2026-07-22: freshly regenerated m=18 input exactly matches the prior global
  hash; fresh SymPy reproduction has completed 12/24 chunks and continues.
  Screened all 795,630 connected n=10,m=19 graphs: numerical minimum slack
  `8.06276942815447...` at `I?bF`xw{?`; exact SymPy and PARI certify the low
  50 and agree on minimizer charpoly
  `x^2(x^4-3x^3-7x^2+16x-6)(x^4+3x^3-3x^2-4x+2)`.
- 2026-07-22: fresh m=18 reproduction remains active. Twelve prior-output
  chunks exist; the resumed process is recomputing the first wave because its
  interrupted predecessor left output files before atomic renaming was added
  to this fresh-run wrapper. No partial fresh output is accepted; harvest only
  after all 24 paired files pass `aggregate_chunk_certificates.py`.
- 2026-07-22: full m=18 SymPy completed all 24 chunks. The standalone
  aggregator validated every per-chunk count/hash in both engines, all 561,106
  records, global SHA-256 `b47af8111f2d07caf6fa2d09bba7351d9fa5969bbac63ea0ae3669e2cfe8bdc2`,
  common minimizer `I?q`qjo{?`, and exact SymPy lower bound
  `17510320956417/2528856896644 > 6.9242039`. Also exact-certified equal
  odd-cycle dumbbells through cycle length 101; minimum remains n=5.
- 2026-07-22: independent full PARI certification completed all 24 m=18
  chunks (561,106 graphs), with exact integer characteristic polynomials and
  strictly positive 80-digit slacks. Global minimum is `I?q`qjo{?` at
  `6.9242077361381927285...`. The exact SymPy pass has atomically completed
  12/24 chunks and continues. A low-50 structural scan found 36 diameter-three
  graphs, all 50 with induced claws, and 40 triangle-free members.
- 2026-07-22: regenerated all 561,106 m=18 graphs (SHA-256
  `b47af8111f2d07caf6fa2d09bba7351d9fa5969bbac63ea0ae3669e2cfe8bdc2`),
  split them into 24 durable chunks, and launched a 24-core exact rational
  SymPy certification at width <10^-6. While it runs, derived the exact
  characteristic-polynomial identity `chi_D=chi_C^2-chi_P^2` for two equal
  cycles joined by a bridge and checked it symbolically for lengths 3,5,7,9.
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
- 2026-07-21: regenerated the 211,866-graph m=16 slice and began full exact
  SymPy certification. A serial 20-minute run and an over-parallelized 32-way
  run hit process time limits before completion; no failure or nonpositive
  record appeared in the completed prefix. Resume with bounded parallelism and
  atomic per-chunk outputs rather than restarting a single monolithic stream.
- 2026-07-21: a compact fresh-process 16-worker SymPy certificate completed
  all 211,866 m=16 graphs: strict positive rational lower bounds throughout,
  minimum lower bound `5.0618714727969403...` at `I?`DF`YN?`, input SHA-256
  `b51f7340afeb301878dc93ba894d89ac85572d23a8b5a39096a21930ecf0efe0`.
  The first persistent-worker PARI implementation exceeded one hour without an
  atomic result and is not accepted; make its chunks independently resumable.
- 2026-07-22: optimized the independent PARI pass by batching GP input and
  removing redundant SymPy work. PARI completed all 211,866 m=16 graphs,
  generated and parsed every exact integer characteristic polynomial, found all
  80-digit slacks positive, and agreed on the minimizer `I?`DF`YN?` with slack
  `5.0618714727969400821989576329...`. Thus m=16 passes both engines.
- 2026-07-22: launched the final fresh-process reproduction from a newly
  generated 211,866-line graph6 file; the bounded SymPy stage remains active
  across the heartbeat. Do not duplicate or kill it; PARI is chained after it.
- 2026-07-22: fresh end-to-end m=16 reproduction completed identically in both
  engines. Screened all 361,342 n=10,m=17 graphs; observed minimum slack
  `5.911281165531542...` at `I?`FBqsF_`. The low 50 pass exact SymPy rational
  isolation and independent PARI exact-characteristic-polynomial checks.
- 2026-07-22: full m=17 SymPy attempts at 16 and 64 workers each exceeded one
  hour because every root was isolated to 30 decimals. No output was accepted.
  Next use coarse exact rational isolation sufficient merely to prove slack >0,
  retaining the 30-decimal low-tail certificate for the minimum.
- 2026-07-22: completed all 361,342 m=17 graphs with exact SymPy rational root
  isolation at width <10^-6; every rigorous slack lower bound is positive and
  the least is `20940707161630/3542499915409 > 5.9112795` at `I?`FBqsF_`.
  Input SHA-256: `179562801fb7a60d29da2c6a6ed03909c27660ef57fe6ddaf94490005ce4729e`.
- 2026-07-22: full independent PARI pass completed all 361,342 m=17 graphs,
  parsing exact integer characteristic polynomials and finding all 80-digit
  slacks positive. It reproduced minimizer `I?`FBqsF_` and slack
  `5.9112811655315422682710710158...`. Cumulative two-engine census: 773,865.
- 2026-07-22: fresh m=17 reproduction matched both certificates exactly.
  Screened all 561,106 n=10,m=18 graphs; observed minimum slack
  `6.9242077361381927...` at `I?q`qjo{?`. Exact SymPy and PARI certify the low
  50; minimizer charpoly is `x^2(x-1)^3(x+2)^2(x^3-x^2-12x+8)`.

## next steps
1. Harvest and aggregate the active fresh m=19 reproduction.
2. Run full checkpointed paired m=20 certification.
3. Compute structural fingerprints of the certified minimizers.
4. Derive a compact exact formula for the odd-cycle dumbbell family.
4. Analyze the flagged unicyclic-with-triangle bottleneck structurally.
5. Use the certified X pipeline only when a result passes every mathematical
   verification gate (or under the doctrine's casual-post lane).

## open questions for the operator (Marko)

(none)
