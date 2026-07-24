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
