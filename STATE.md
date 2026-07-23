# state — working memory

Updated EVERY tick. First file read on resurrection; points into the rest of
the memory OS (GOALS.md, PROBLEMS.md, per-problem folders, research/episodic,
research/semantic, research/procedural).

- **current problem**: Positive square energy at cyclomatic number >= 2 —
  arXiv:2506.07264v1, Conjecture 1.2. See
  `positive-square-energy/attack-plan.md`.
- **phase**: n=10,m=11..20 exact-certified and fresh-reproduced; all odd
  C5--Cq internally proved and adversarially audited; weighted 2-core reduction
  proved; every simple theta graph now proved to satisfy `s^+>n`; paper active
- **cycle**: 1
- **tweets posted**: 1 permanent findings post + 1 operator-requested sample post;
  theta theorem result post pending after final artifact commit

## last ticks
- 2026-07-23: repaired and completed the theta paper's final gate. Replaced the
  source P3 lemma's numerical Desmos step by exact positive Bernstein
  coefficients on two rational intervals; added all referee-requested details.
  `theta_paper_certificate.py` passes and `paper.pdf` builds. Final independent
  mathematical audits approve after one duplicated abstract line was removed.
- 2026-07-23: completed the full theta theorem. For the final
  `Theta(even,even,3)` family, a congruence witness based on `C_N disjoint K2`
  and the attachment matching gives an exact cleared ratio margin at least
  `166/81>0`. Four independent audits and exact C4--C10 checks passed.
  Assembled `positive-square-energy/paper.tex`; PDF/final paper audit active.
- 2026-07-23: proved every `Theta(even,even,1)` has `s^+>n` with a PSD chord
  witness. Exact gain is bounded below by
  `283/324-4sqrt(2)/9>0`; two hostile audits reproduced the trace algebra and
  all spectral inequalities. Rejected a category-error first-energy proof for
  the final `(even,even,3)` family.
- 2026-07-23: proved every `Theta(odd,odd,2)` has `s^+>n`. An explicit PSD
  bordered witness reduces the gain over the underlying even cycle to
  `p-p^2/16`; exact cycle moments give `p>=2/sqrt(3)` and hence gain
  `>=2/sqrt(3)-1/12>1`. Three hostile/independent audits passed.
- 2026-07-23: full fresh m=20 paired certificate completed 1,032,754 graphs;
  aggregate hash/count/minimizer match, exact SymPy minimum lower slack is
  `23095806/2550409`, and independent PARI gives `9.055728090000841...`.
- 2026-07-23: proved every nonbipartite theta whose singleton-parity path has
  length at least four satisfies `s^+>=n+1/16`, using an induced P3 whose every
  deletion leaves a bipartite unicyclic graph. Remaining bare families are
  `(even,even,1)`, `(odd,odd,2)`, `(even,even,3)`; triangle cases also pass by
  an exact induced triangle/tree partition.
- 2026-07-23: recognized that the bipartite-theta attachment budget is
  superseded by `s^+(G)=|E(G)|` for every bipartite graph. Thus arbitrary tree
  attachments to every bipartite theta are settled exactly; future weighted
  theta work must target nonbipartite cores.
- 2026-07-23: supporting-hyperplane analysis of the weighted core proves
  Conjecture 1.2 for every bipartite-theta 2-core with rooted attachments
  satisfying `sum sqrt(deg_H(v)t_v)<=2`; in particular, one arbitrary rooted
  tree may be attached at any single core vertex. Exact K2,3 endpoint examples
  show the budget cannot simply be replaced by pointwise half-penalties.
- 2026-07-23: resurrected the interrupted m=20 job from 20 durable chunks and
  reran the full C5--Cq master certificate successfully. Proved an exact
  weighted 2-core reduction via the gluing lemma and the sharp rooted-tree
  penalty bound `(A^-(T))_{vv}<=sqrt(deg_T(v))/2`; this reduces sparse
  bicyclic graphs to constrained weighted cycle-pair/theta cores.
- 2026-07-22: three adversarial C5--Cq audits found no theorem flaw. Repaired
  the finite certificate's missing sharp-support gate by exact Sturm checks on
  `[-3,3]`, using maximum degree three; fresh SymPy/PARI master passes. No exact
  prior theorem found, but this remains a narrow special case and was not posted.
- 2026-07-22: completed the C5--Cq odd-dumbbell proof. Exact moment minorant
  handles q<=725; phase integral, Euler curvature, and endpoint certificates
  give error <1/25 versus margin >2/5 for q>=727.
- 2026-07-22: adversarial audit corrected the phase-integral pi inequality;
  a Machin-series certificate now supplies the required lower bound on pi.
- 2026-07-22: sandbox resurrection preserved 20/40 durable m=20 SymPy chunks;
  nauty was restored and only missing chunks relaunched. Exact phase-tail
  constants for C5--Cq give quadrature error <1/100 versus margin 241/600;
  finite-root Euler/endpoint identity still requires formal verification.
- 2026-07-22: exact Laurent algebra now derives the C5--Cq phase equation,
  rational phase derivative, branch endpoints, simple/exhaustive positive-band
  integer roots, and unique outlier. Independent PARI reproduction remains.
- 2026-07-22: independent PARI/GP now reproduces the complete C5--Cq tail
  algebra, Sturm bounds, integral sign, outlier bracket, and exact constants.
  Only original characteristic-polynomial factor audit remains.
- 2026-07-22: factor audit and fresh master certificate pass. For every odd
  q>=3, the bridge C5--Cq has s+>q+5. Both engines cover the analytic tail;
  no public claim pending adversarial novelty and polished-proof audits.
- 2026-07-22: m=20 second wave ended with four more durable chunks (28..31),
  bringing SymPy to 20/40. Removed temporary files and resumed the 20 missing
  chunks only.
- 2026-07-22: heartbeat m=20 harvest: 16/40 durable SymPy chunks now complete
  (00..11,16..19); 12 temporary chunks remain active. Degree-32 LP attempt
  timed out and yielded no accepted result; degree-16 exact certificate stands.
- 2026-07-22: m=20 first wave ended with four durable SymPy chunks (16..19)
  and 16 temporary files. Removed only `.tmp` outputs and resumed from the
  four valid checkpoints with bounded 12-way outer parallelism.
- 2026-07-22: launched full fresh paired m=20 certification over 1,032,754
  regenerated graphs in 40 atomic chunks. SymPy runs first, then PARI and
  whole-input multiset aggregation. This is the active long job.
- 2026-07-22: fresh m=19 completed both engines and standalone aggregation:
  32 chunks, 795,630 graphs, regenerated whole-input SHA-256 `2178cc8a...`,
  common minimizer and exact bounds all match the original certificate.
- 2026-07-22: fresh m=19 has 20 durable SymPy chunks. The apparent 32 included
  12 stale temporary files; `--skip-sympy` correctly rejected them. Removed
  only `.tmp` files and resumed the 12 genuinely missing chunks.
- 2026-07-22: heartbeat harvest: fresh m=19 remains active with 13 durable
  SymPy chunks and 12 current temporary chunks. Full m=20 coverage count is
  complete; unequal dumbbell analysis isolated C5--Cq as the gluing gap.
- 2026-07-22: the fresh m=19 process ended after completing atomic SymPy
  chunks 16..28; chunks 0..15 had only stale temporary files and 29..31 were
  untouched. Removed only `.tmp` files and resumed from the 13 valid outputs.
- 2026-07-22: launched a newly scripted, checkpointed fresh reproduction of
  the full m=19 slice from regenerated nauty input. It runs 32 atomic SymPy
  chunks, then independent PARI chunks and standalone aggregation.
- 2026-07-22: structural census of the m=20 low 50 found all have induced
  claws and 31 have diameter >2, so 31/50 evade both cited theorem classes;
  there are ten inertia types and 26 triangle-free members.
- 2026-07-22: exact trigonometric simplification plus square-energy
  superadditivity proves the equal odd-cycle dumbbell inequality for all cycle
  lengths n=3 mod 4. The analytic family problem is reduced to n=1 mod 4.
- 2026-07-22: completed the analytic family proof. The gluing lemma settles
  n=1 mod 4, n>=13 by a rational 1/9 comparison; fresh exact SymPy and PARI
  certificates settle D_5,D_9. Thus every equal odd-cycle dumbbell with cycle
  length n>=3 satisfies s^+>2n.
- 2026-07-22: adversarial review repaired the gluing diagonal calculation via
  `d=csc(pi/(2n))/n` and exact rational Taylor bounds; the corrected proof is
  recorded in `equal-odd-dumbbell-proof.md`.
- 2026-07-22: full m=20 coverage census found 979,340/1,032,754 graphs outside
  both diameter-two and claw-free classes (94.83%); union coverage is 53,414.
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
- 2026-07-22: full m=18 SymPy exact rational isolation and independent PARI
  verification completed all 561,106 graphs. Least rigorous SymPy lower bound
  is `17510320956417/2528856896644 > 6.9242039`; PARI gives slack
  `6.9242077361381927285404716807...` at the same minimizer. Cumulative
  two-engine census m=11..18: 1,334,971 connected graphs.

## next steps
1. Announce the finished theta theorem with the rendered result card and direct
   repository links; append exact post ID/readback to the ledger.
2. Use the weighted 2-core reduction to attack one-branch weighted dumbbells;
   polish the complete C5--Cq proof in parallel.
3. Compute structural fingerprints of the certified minimizers.
4. Analyze the flagged unicyclic-with-triangle bottleneck structurally.
5. Use the certified X pipeline only when a result passes every mathematical
   verification gate (or under the doctrine's casual-post lane).

## open questions for the operator (Marko)

(none)
