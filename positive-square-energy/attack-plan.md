# attack plan — positive square energy

## Target

Conjecture 1.2 of arXiv:2506.07264v1: every connected n-vertex simple graph
with m >= n+1 satisfies s^+(G) >= n.

## Ranked lines of attack

1. **Sparse census beyond n=9.** Enumerate nonisomorphic connected graphs at
   n=10, beginning m=n+1 and increasing m. Float-screen s^+-n, retain a wide
   safety margin, then certify all near-minimizers by exact characteristic
   polynomial/root isolation. A counterexample is immediately certificate-shaped.
2. **Extremal family discovery.** Mine low-slack graphs for common cores,
   pendant-tree attachments, inertia, and equitable partitions; conjecture and
   prove a reduction or an infinite-family formula.
3. **Triangle-unicyclic bridge.** Although outside Conjecture 1.2 at m=n,
   understand the paper's bottleneck (Conjectures 9.1/9.4) to derive a gluing
   inequality robust under adding one edge.
4. **Local transformations.** Test whether leaf relocation, subdivision, or
   edge addition monotonically controls s^+ in the low-slack regime.

## Current line

Line 1: n=10,m=11 through 17 fully exact-certified in SymPy and independently
checked in PARI. Full m=18 passed both engines on all 561,106 graphs, with all
chunk hashes/counts aggregated; cumulative total 1,334,971. Fresh reproduction
passed. Full m=19 now passes both engines on 795,630 graphs; cumulative total
2,130,601. Fresh m=19 reproduction passed in 32 checkpointed chunks. The
m=20 full paired fresh certification is complete on all 1,032,754 graphs.

## Next experiments

1. Run full paired certification for m=20; the 1,032,754-graph count remains
   tractable under the compact chunk pipeline.
4. Package the cumulative n=10 census and compare precisely with what the paper
   already proves via diameter two or claw-free hypotheses.
4. Extend structural fingerprints from each minimizer to the low 50, especially
   testing triangle-free, claw, inertia, and diameter-two frequencies.
5. Package the completed gluing-lemma proof for all equal odd-cycle dumbbells
   and adversarially check every inequality and hypothesis against the paper.
6. Formalize the exact Euler-summation identity for the C5--Cq band. The tail
   constants pass with error <1/100, but endpoint/sign correspondence must be
   explicit before accepting this unequal-family result.
7. C5--Cq is now internally proved for every odd q>=3 by a fresh-process
   master certificate with independent PARI tail reproduction. Run adversarial
   literature/novelty review and proof exposition before publicizing.
8. Exploit `weighted-core-reduction.md`: first settle core vertices with one
   pendant branch, whose gluing penalty is sharply at most 1/2, then formulate
   the constrained weighted-theta inequality for the bridgeless bicyclic case.
9. Extend `bipartite-theta-attachments.md` beyond its sharp supporting-plane
   method to nonbipartite theta cores. Bipartite theta cores need no budget:
   arbitrary tree attachments remain bipartite and have `s^+=m=n+1` exactly.
10. Use `nonbipartite-theta-p3.md`: the improved P3 lemma settles singleton-
    parity path length at least four. Prove the three residual Chebyshev
    families `(even,even,1)`, `(odd,odd,2)`, `(even,even,3)`.
11. `odd-odd-two-theta-proof.md` settles the middle family via an explicit PSD
    bordered-cycle witness. Transfer that witness to the chord family
    `(even,even,1)` and the length-three ear family `(even,even,3)`.
12. `even-even-one-theta-proof.md` settles the chord family. For the final
    length-three ear family, combine symmetric and antisymmetric square-energy
    channels; do not substitute a positive-first-energy Ky Fan bound.
13. `even-even-three-theta-proof.md` settles the final family via a congruence
    witness around `C_N disjoint K2`. The full simple-theta theorem is proved;
    compile and hostile-audit `paper.tex` and its exact displayed algebra.
14. Weighted one-tree extension: prove the scaled-positive-part baseline for
    every rooted theta outside the three exact-certified branch exceptions
    `(2,3,3),(1,4,4),(2,2,3)`. Do not reuse penalized P3 deletion or the bare
    family witnesses without a new root-aware term; exact counterexamples show
    those proof strategies fail.
15. Replace item 14's scaled baseline by the stronger root-congruence witness
    in `experiments/root-congruence-witness.md`.  Prove its `k=6/7` moment
    inequality uniformly.  Use exact short cases plus local walk-polynomial
    bounds and a Chebyshev/phase tail; a pointwise global minorant cannot keep
    the exact infinite-path bulk.
16. Bare bicyclic classification now leaves only two odd cycles joined by a
    connector path of length at least two. Develop a connector-aware phase or
    PSD witness, starting with the symmetric `C5--P_l--C5` family.
17. `experiments/local-four-fifths-reduction.md` settles the local moments:
    the witness loss is uniformly `<4/5`.  Prove the bare signed-square theorem
    `tr(A|A|)>=-2/5` outside the three already certified exceptions.  Focus the
    phase attack on the `(2,3,c)` and `(1,4,c)` short-base channels; census
    indicates every nonexceptional theta below `0.9` lies there.
18. Use `experiments/theta-imaginary-phase.md`: the exact phase carrier
    `H=R+i sqrt(z)S` has `R>=0`, and `tr(A|A|)` is a weighted principal-phase
    area.  Bound that area by `pi/5` using its `O(z^(3/2))` origin behavior and
    the path exponents; do not use a finite-mass `Arg<=pi/2` shortcut.
19. `theta-phase-sign-theorem.md` removes every theta whose shortest odd cycle
    is `3 mod 4`; only the `1 mod 4` negative-trace class remains.  Package and
    verify the mod-four pointwise monotonicity certificate for `(2,3,c)` and
    `(1,4,c)`, then combine it with the safe exact limits in
    `theta-short-base-limits.md` and finite Sturm endpoint gates.
20. The two `C5` short-base channels are now fully proved by
    `theta-short-base-four-fifths.md`.  Do not use structural path shortening:
    it has exact counterexamples.  For the remaining negative-trace class the
    shortest odd cycle is at least 9; prove its phase area `<pi/5` from the
    normalized denominator bound and finite `g=9` exponent/multiplicity cases.
    The eight-cap certificate is exact for same-residue carriers.  Complete
    the 16-case parameterized certificate for opposite-residue companions,
     preserving sign correlations via power variables `X,Y,W` and tensor
     Bernstein subdivision on `[0,3/4]x[0,1]^3`.
21. Rank-eleven cactus induction: sharp DNN and actual-bridge pruning leave
    five marked/shared endpoint families. All ten fully shared `T^9PP`
    ordinary-ledger exceptions now have final-owner repairs. The naive N7
    extension fails numerically, but a one-router packing-one `T^8P` repair
    closes `U7`. The remaining obstacle is existential router reachability R11.
    Build a port-aware verifier over cyclic realizations and concrete owner
    refinements; never quotient by the 144-state arithmetic ledger alone.
22. `A_10|Q` is now exact-closed as `12099=12089+10` with a theorem-aware
    post-ownership ledger. For `P|A_9|P`, retain the exact provisional frontier
    `43151=43116+35` but do not call the 43116 rows positive from the old score:
    41863 put a pentagon inside a credited triangular packet. Reclassify every
    final packet after attaching its zero, one, or two demands, using only
    proved mixed lower-rank/common-cut/packing-one bounds. Then revisit the
    `6+28+1` residual templates with theorem-derived ledgers and recursive
    adhesion owners.
23. The shared-cut hinge extends to triangular root `y=x`, but does not apply
    to remote pentagons merely sharing an entry mark. A theorem-aware search
    leaves six of 43151 `P|A_9|P` rows, with smallest
    `X[AB](T()^9)`. Attack the packing-one separated two-interface polynomial
    `(Z+4C-4D)+i(2(B-A)+8E)`. The joint-cycle homotopy is phase-increasing on
    the smallest fan, so do not delete it. Develop a winding-sensitive two-
    pivot Schur/message inequality or a direct integrated estimate retaining
    `D-2iE`.
24. The six rank-eleven `P|A_9|P` rows do not require that analytic theorem:
    two split as `TP +` packing-one `A_7P`, and four open one pentagon while
    retaining packing-one `A_9P`. The completed fail-closed census is
    `43151=43145+6`. Integrate this endpoint with `A_10|Q`, `T^9P|P`, and the
    fully shared families; identify the exact remaining rank-eleven marked
    endpoint. Do not infer an all-rank `T^rPP` theorem.
25. `T^9P|P` has 50399 exact geometry-aware marked rows. Do not restore the
    rejected symbolic `50382/50399` closure. Implement final-owner theorem
    records over explicit pentagon/connector/triangle geometry. The candidate
    residuals are K1=`A_8+PP`, K2=open remote P plus packing-one `A_9P`, and a
    15-row nested two-arm family `A_aP+A_bP+A_(7-a-b)`. Apply the same hardened
    geometry and independent theorem checks to the ordinary 50382 rows.
26. The shared router bridge now certifies an exact 43151-row projection and
    concrete intervals for 43145 ordinary triangular-hull plans, with canonical
    identity maps and hostile alias/swap gates. Next extend its final-owner
    domain from triangles/cuts to complete clustered and remote pentagons,
    connector edges/remnants, and attachments; then adapt the 7248 private-P
    rows and integrate K1/K2/K3--K17. Keep theorem status fail-closed until all
    physical owner domains are exhaustive.
27. Physical final owners are now accepted for 43145 triangular-hull ordinary
    plans, including independent expected graph/attachment domains and complete
    C5/connector ownership. Remaining finite tasks are exactly six projected
    A9 repairs plus 7248 private-P rows. Implement the private leaf-pentagon
    router lemma over the same physical checker, then K1/K2/K3--K17 or project
    the six hardened A9 repairs where geometry matches. Keep the 115502 fully
    shared rows queued after this endpoint.
28. `T^9P|P` is now fully exact-certified on all 50399 rows, including 7248
    private-P orbits and six projected repairs. The only rank-eleven bulk gap is
    the 115502 ordinary fully shared `T^9PP` rows: port the shared physical
    owner core to that unmarked incidence universe, rederive each mixed packet
    theorem after final ownership, and combine with the ten already proved
    U1--U10 repairs. Then synthesize the rank-eleven theorem and run fresh
    hostile topology/certificate gates.
29. The 115502 ordinary fully shared `T^9PP` rows are now physically certified;
    every one of 517923 abstract SAFE choices passes post-ownership theorem
    reclassification. The new C5 router handles 2--5 ports. Implement U1--U10
    physical repairs through the same graph/owner/theorem pipeline, including
    corrected U7 and degree-four U8. Then combine DNN, bridge pruning, all
    marked endpoints, all-rank `T^rQ`, and fully shared closure into the complete
    rank-eleven theorem.
30. Fully shared `T^9PP` is now complete on all 115512 rows, including U1--U10
    with interval/branch owner binding and nested refinement replay. Before
    claiming rank eleven, resolve the dependency audit's remaining nonhostile
    `T^10Q` branch (even Q and q=3 mod 4): either prove it follows directly from
    favorable-cycle Sachs phase for arbitrary incidence topology, or build a
    physical rank-eleven verifier. Then synthesize paper and run ultimate gates.
31. The nonhostile `T^10Q` branch is now closed at all ranks by the maximum-
    packing mixed-phase theorem in
    `research/all-rank-nonhostile-one-cycle-theorem-2026-07-30.md`; no finite
    verifier is needed. The next obligation is the global rank-eleven synthesis:
    enumerate the sharp-DNN reduction, actual-bridge pruning, every marked and
    fully-shared endpoint, and audit that every branch invokes only earlier or
    independently proved packets. Build the paper only after a hostile dependency
    referee accepts this exhaustive tree.
32. Rank eleven is complete and accepted. The authoritative synthesis is
    `all-rank-eleven-cacti/paper.tex`; its finite core is `266=253+13`,
    `43151=43145+6`, `50399/50399`, and `115512=115502+10`. Do not reopen it
    without a concrete audit failure. Next: run the publication acceptance
    workflow for this major partial AKMPZ result, then move the mathematical
    frontier to rank twelve only after deriving its exact sharp-DNN residual
    profiles and writing a victory/non-victory prompt.
33. The rank-uniform `T^rPP` obstruction is now solved. The accepted proof is
    `all-rank-triangle-two-pentagon-cacti/paper.tex`: Voronoi first, unrestricted
    local packing-one one-P Sachs margin, actual-bridge induction, and exact
    H1--H7 one-cluster topology. Since rank-twelve DNN leaves only `T^11Q` and
    `T^10PP`, both all-rank families are closed. Next synthesize the short
    rank-twelve cactus paper, audit dependency scopes, build PDF, and publish
    only after definitive acceptance.
34. Rank twelve is complete and independently accepted. Authoritative paper:
    `all-rank-twelve-cacti/paper.tex`. Next apply the publication workflow to
    the two verified results (all-rank `T^rPP` and rank twelve) without OCB
    resolution overclaim, then derive the exact rank-thirteen DNN frontier.
35. The uniform frontier synthesis now proves every connected cactus with at
    least two cycles. The next sharp sparse class is every connected bicyclic
    graph. Reduce to theta 2-core plus arbitrary multi-root forests and attack
    the exact right-half-plane continuant kernel in
    `positive-square-energy/bicyclic-theta/prompt.md`. Do not return to lossy
    multi-diagonal weighted cores or false attachment monotonicity.
36. The arbitrary-attached-theta kernel is solved, so every connected bicyclic
    graph is strict. Authoritative synthesis: `all-bicyclic-graphs/paper.tex`.
    Apply publication workflow, then attack promotion from a spanning connected
    bicyclic subgraph to arbitrary `m>=n+1`: the next bottleneck is a connected
    chord-addition/basis-exchange certificate, not the sparse base theorem.
37. Nonnegative chord correlation is false for every spanning bicyclic base in
    a small four-path example, and a claimed generic bicyclic edge-phase SOS
    was not proved. Keep edge monotonicity as a parallel conjecture, but make the
    next proof target all connected tricyclic graphs via block/kernel analysis;
    see `positive-square-energy/tricyclic-general/prompt.md`.
38. Tricyclic block rank `2+1` is complete. Exact block-additive DNN leaves only
    `Theta(1,2,r)+C3` and `Theta(1,2,2)+C5`; induced-territory partitions close
    both with strict surplus. See `tricyclic-general/theta-cycle-completion.md`.
    The remaining tricyclic frontier is one rank-three 2-connected block:
    doubled triangle, K4 subdivision, and doubled C4 (four-path is complete).
35. Rank thirteen is complete. Sharp DNN gives `sigma>=12-sum epsilon_l`, and
    the exact fail-closed frontier is `T^12Q,T^11PP`. The complementary
    all-rank one-cycle results close every parity of `Q`, including `q=3`, and
    the all-rank two-pentagon theorem closes `T^11PP` at `r=11`. The
    authoritative synthesis is `all-rank-thirteen-cacti/paper.tex`; its
    verifier rejects four hostile mutations and agrees normally and under
    `python -O`. Do not infer an all-rank cactus theorem from this synthesis.
36. The rank-uniform synthesis is now complete: every finite simple connected
    cactus of cyclomatic rank `k>=2` has `s+>n`. The exact DNN deficiency
    frontier is `T^(k-1)Q,T^(k-2)PP`; all-rank hostile/nonhostile one-cycle
    theorems close the first, and the all-rank two-pentagon theorem closes the
    second for `k>=3`. The pure `PP` boundary at `k=2` uses the separate bouquet
    and connector theorems. Rank one remains excluded (`C4` has equality).
    Authoritative synthesis: `all-nonunicyclic-cacti/paper.tex`; proof note and
    constant-size fail-closed verifier are under `research/`. Do not promote
    this cactus theorem to a claim for arbitrary graphs, and do not publish it
    under the present instruction.
33. Rank twelve now has an exact fail-closed sharp-DNN frontier:
    `T^11Q,T^10PP`. The one-`Q` branch is covered by the all-rank parity
    theorems, but this frontier calculation is not a rank-twelve proof. Follow
    `rank12/prompt.md`: attack the all-rank `T^rPP` family next; a finite census
    or one special endpoint alone is progress, not victory.

## Running jobs

- `job-m18-sympy.pid`: 24 atomic input chunks, 12 outer jobs x 2 SymPy
  workers, COMPLETE, exact rational isolation width <10^-6. Input SHA-256
  `b47af8111f2d07caf6fa2d09bba7351d9fa5969bbac63ea0ae3669e2cfe8bdc2`.
- `job-m18-pari.pid`: COMPLETE, 24/24 atomic chunks, 561,106 total graphs,
  every exact charpoly parsed and every 80-digit slack positive.
- `job-m18-fresh.pid`: COMPLETE. Final standalone aggregate exactly reproduced
  both engines, all counts/hashes, minimizer, and bounds.
- `job-m19-sympy.pid`: active, 32 atomic chunks, 16 outer x 2 workers,
  COMPLETE, exact rational isolation width <10^-6; input hash
  `2178cc8ac8ce524cc43ab6671573c0830e2b57df387b8b95c7d275e93d62e041`.
- `job-m19-pari.pid`: COMPLETE, 32/32 chunks and 795,630 graphs; aggregate
  pairing completed successfully.
- `job-m19-fresh.pid`: COMPLETE, regenerated input with 32 paired atomic
  chunks; whole-input multiset/hash and standalone aggregation passed.
- `job-known-classes.pid`: active count of diameter-two/claw-free theorem
  coverage for the complete m=18,19 slices.
- `job-m20-known-classes.pid`: COMPLETE, 1,032,754 graphs; 979,340 outside
  both diameter-two and claw-free classes.
- `job-m20-full.pid`: COMPLETE after 2026-07-23 resurrection. All 40 paired
  chunks / 1,032,754 graphs passed; global input SHA-256
  `ed8bf95b309ef084a785ab93040a137a2f5f1767338855b81089f53965e42d21`;
  minimizer `I?rFf_{N?`; exact lower slack `23095806/2550409`.

## Adversarial C5--Cq audit

- Three independent audits reproduced the graph definition, bridge determinant,
  characteristic factorization, energy translation, finite moment gate, phase
  root count, outlier, and tail constants. No mathematical counterexample was
  found.
- They exposed one certificate-packaging gap: the finite minorant script merely
  asserted a sharp root interval. Replaced it by exact Sturm checks on `[-3,3]`,
  justified immediately because `S_q` is a characteristic factor of a graph of
  maximum degree three. The fresh master certificate passes after this repair.
- Literature search found no prior C5--Cq positive-square-energy theorem or
  stronger applicable result. The q=3 case alone already follows from induced-
  subgraph superadditivity. Current framing: a new narrow bicyclic special case
  of Conjecture 1.2, not yet strong enough for public results-lane publication.

## Verification discipline

Numerical eigenvalues are search heuristics only. Any claimed inequality,
counterexample, or extremizer requires a standalone exact certificate, a fresh
process, a second engine, and statement/novelty checks.

## Retreat criteria

After roughly two weeks without either a new certified finite bound, a proved
structural lemma, or a promising extremal family despite census and theory
work, write a post-mortem and reconsider the queue.
