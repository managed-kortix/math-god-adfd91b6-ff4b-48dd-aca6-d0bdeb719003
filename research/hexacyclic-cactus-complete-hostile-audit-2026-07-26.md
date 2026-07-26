# Hostile completeness audit: connected hexacyclic cacti

## Verdict

**ACCEPT.** The existing research, read cumulatively rather than by the stale
status sentences in the earlier planning and disconnected-audit notes, proves

`s+(G)>|V(G)|`

for every connected hexacyclic cactus `G`, with arbitrary bridge connectors and
arbitrary attached trees.

I found no remaining mathematical blocker. The proof is scattered and has not
yet been assembled into a hexacyclic manuscript. In particular,
`research/hexacyclic-ttttpp-disconnected-audit-2026-07-26.md` still says that E1
is unresolved, but the later note
`research/hexacyclic-ttttpp-e1-resolution-2026-07-26.md` closes exactly that
family. Likewise, disclaimers saying that an individual census or local lemma
is not a global theorem correctly describe that individual file; they do not
survive the cumulative synthesis below.

## 1. Exact DNN classification

For six cyclic blocks of lengths `l1,...,l6`, bridge-block counting and the
sharp cactus DNN theorem give

`sigma(G)=s+(G)-|V(G)| >= 5-sum_i epsilon_li`,

where even lengths contribute zero, `epsilon_3=1`,
`epsilon_5=5-2sqrt(5)`, and the odd sequence decreases strictly. The symbolic
comparisons

`3 epsilon_5<2`, `2 epsilon_5>1`, and
`epsilon_5+epsilon_7<1`

leave exactly

`TTTTTQ={3,3,3,3,3,q}`, `q>=3`, and
`TTTTPP={3,3,3,3,5,5}`.

This classification in
`research/hexacyclic-dnn-residuals-2026-07-26.md` is exhaustive. In particular,
the `q=3` six-triangle case is included, even `q` is not accidentally discarded
at the zero DNN boundary, and no other four-triangle multiset survives. Every
nonresidual cycle multiset has a strictly positive DNN lower bound, so only the
two displayed residual families require structural work.

## 2. Connected/disconnected shared-cut dichotomy

The shared-cut graph either has one component or more than one. These are
respectively the fully shared incidence-census cases and the disconnected
reduced-cluster-tree cases. Singleton cyclic blocks count as singleton
shared-cut clusters, so the dichotomy omits no bridge-separated incidence.

The reduced cluster tree used throughout is obtained from the actual block-cut
tree. Its territory lemma cuts actual bridge edges, handles nonpath and Steiner
connector trees, and assigns each hanging tree wholly through its unique cyclic
hull attachment. Therefore a reduced-tree packet is an induced vertex
territory, not a formal cycle-multiset decomposition.

## 3. Disconnected `TTTTTQ`

`research/hexacyclic-tttttq-disconnected-2026-07-26.md` is complete.

- If `q=3`, the all-triangle theorem applies directly.
- Otherwise a reduced tree with at least two marked cluster nodes has a leaf
  not containing the unique `Q`; that leaf is one shared-cut cluster of `r`
  triangles.
- For `1<=r<=4`, its strict triangular surplus combines with the established
  nonnegative or positive lower-cyclic remainder.
- For `r=5`, the only possible adverse remainder is a hostile unicyclic `Q`.
  The proved five-triangle shared-cluster estimate `sigma>2`, including packing
  three and arbitrary attached trees, combines with
  `sigma(Q)>=-delta_q`, where `delta_q<1`.

Thus every disconnected `TTTTTQ` configuration is strict. The argument does
not assume that the reduced tree is a path or that connector entry occurs at a
preferred cycle vertex. The crucial five-triangle input has also received the
independent adversarial audit
`research/five-triangle-shared-cluster-surplus-audit-2026-07-26.md`, including
its incidence-leaf opening, packing-three exception, multiway cuts, attached
trees, and strict `>2` budget.

## 4. Disconnected `TTTTPP` and all 28 partitions

The 28 proper colored set partitions of four `T` symbols and two `P` symbols
listed in `research/hexacyclic-ttttpp-disconnected-audit-2026-07-26.md` are the
complete colored partition set. Their cumulative resolution is:

1. Twenty-three partitions close by direct induced cluster-packet addition.
2. `T|T|T|T|P|P` closes for every reduced-tree topology: either a singleton
   triangle is a leaf, or the two pentagons are the only leaves, forcing a path
   and the packetization `TP+TT+TP`.
3. `TTP|TTP` closes by coordinated pentagon interval splits at both ends of the
   same connector, yielding `TT+T+T` without duplicating a cut vertex.
4. `TTP|T|T|P` closes by the reduced-tree leaf/two-two tests and, in the sole
   surviving path position, an entry-sensitive split yielding `TT+T+TP`.
5. The former E2 row `TTTP|T|P` closes in
   `research/hexacyclic-e2-tttp-two-entry-resolution-2026-07-26.md`. Seven of
   the eight colored `TTTP` incidence trees have the uniform `>1` margin. The
   remaining three-petal pentagon hub has 26 ordered labelled-entry orbits, all
   certified as `TP+TTT` or `TTP+TT` by
   `research/hexacyclic-e2-tttp-entry-census.py`.
6. The former E1 row `TTTTP|P` closes in
   `research/hexacyclic-ttttpp-e1-resolution-2026-07-26.md`. Deleting the
   internal pentagon node partitions the four triangles as `(4)`, `(3,1)`,
   `(2,2)`, or `(2,1,1)`, with six possible marked-component rows. The five
   multi-component rows have legal interval packets; the `(4)` row opens both
   pentagons and uses `sigma(TTTT)>3` against exactly two tree costs.

The E1 classification covers entry on a triangle, at an off-pentagon
triangle-triangle cut, at a pentagon attachment cut (including a multiway cut),
and through a tree branch rooted at any such point. The E2 census covers
private roots, shared roots, petal roots, coincident roots, and both cyclic gap
patterns. Hence the original 28-row table is now resolved in all 28 rows, not
merely 27. The independent note
`research/hexacyclic-e1-e2-resolution-adversarial-audit-2026-07-26.md` further
reconstructs the E1 incidence classification (`25` internal incidence trees),
checks all `250` raw E2 entry placements before dihedral quotienting, and
confirms packet hypotheses, ownership, and strictness.

## 5. Fully shared `TTTTTQ`

The exact color-preserving incidence census enumerates every bipartite
cycle-cut tree, enforcing cut degree at least two, triangle degree at most
three, and the correct `Q` capacity. The capacity regimes are exhaustive:

`q=3: 68`, `q=4: 70`, `q>=5: 71` incidence trees.

Every nonbouquet tree has a SAFE one-cycle interval split. The acceptance
logic is sound in each potentially hostile branch case:

- a singleton hostile `Q` loses less than one, while another branch contains
  `TT` and contributes more than one;
- `TQ` is strict positive for every parity;
- generic `TTQ` is nonnegative and another triangular branch is strict;
- larger branches are covered by the proved tetracyclic or pentacyclic
  theorem, with no negative singleton left to charge against qualitative
  positivity.

The unique exception is the six-cycle bouquet. Opening `Q` and one designated
triangle at private vertices leaves one connected four-triangle bouquet with
surplus `>3`; the two opened tree territories cost exactly two. This gives
`sigma(G)>1`, including `Q=T`.

## 6. Fully shared `TTTTPP`

The exact census gives `150` colored incidence trees by cut count

`1, 9, 40, 62, 38`.

The SAFE ledger resolves `148`. It checks retained incidence rather than
assigning bounds from colors alone: shared `PP`, `TTT`, `TTTT`, `TPP`,
shared-pair `TTP`, and intersecting-pair `TTTP` bounds are used only when the
corresponding retained cuts occur in that branch. Generic tricyclic branches
receive only `>=0`, and generic qualitative tetracyclic or pentacyclic
positivity is never used to cancel a negative singleton pentagon.

The two exceptions close directly:

- In the six-cycle bouquet, open both pentagons. The retained four-triangle
  bouquet has surplus `>3`, and two tree costs leave `>1`.
- In the saturated five-mark pentagon hub, merge the unique pentagonal petal
  mark with either adjacent triangular mark and give the other three marks
  separate proper intervals. The induced packetization is `TP+T+T+T`, with
  total surplus `>1-delta>0` plus triangular strictness.

Thus every fully shared incidence in both residual families is covered.

## 7. Incidence-census acceptance audit

I inspected and reran all three hexacyclic scripts unchanged:

```bash
python research/hexacyclic-tttttq-incidence-census.py
python research/hexacyclic-ttttpp-incidence-census.py
python research/hexacyclic-e2-tttp-entry-census.py
```

All embedded assertions passed and reproduced the stated totals, exception
sets, `900` fully shared `TTTTPP` cycle choices, eight E2 incidence trees, and
26 E2 entry orbits.

The generators impose the exact incidence-tree conditions and quotient only by
color-preserving permutations. A component produced after deleting a split
cycle node is an actual connected branch of the retained incidence tree. The
stronger packet tests inspect retained internal cuts where needed. Degree caps
ensure that the number of branch marks does not exceed the split cycle length,
so every accepted abstract branch split can be realized by nonempty proper
consecutive intervals in any actual cyclic order.

The scripts are certificates for finite combinatorics, not substitutes for the
spectral packet lemmas. Their acceptance ledgers use only previously proved
packet inequalities, and no floating-point near-equality controls a verdict.
The decimal arithmetic in the `TTTTPP` script evaluates fixed radical margins
far from zero; the corresponding signs are also immediate symbolically from
`delta=sqrt(5)-2<1/2`.

## 8. Opening and interval inducedness

The two structural operations used in the synthesis are legal vertex
partitions.

1. A private-vertex opening assigns the chosen vertex and every tree branch
   rooted there to one nonempty tree territory. The remaining cycle path keeps
   every cyclic cut. Each opened tree has exactly `sigma=-1`.
2. A cycle interval split partitions all cycle vertices into nonempty proper
   consecutive intervals. Every shared cut has exactly one owner, crossing
   cycle edges are simply absent from the induced parts, and each incidence
   branch and hanging tree follows its unique attachment. A split cycle incurs
   no separate `-1` cost.

These constructions cover adjacent marks, marks at every vertex of a short
cycle, multiway cuts, coincident external roots, private entries, entries
through attached cycles, and branch connectors. No argument allocates a common
cut to two territories, and no argument uses edge monotonicity.

## 9. Arbitrary connectors and attached trees

All disconnected arguments are performed in the actual reduced cluster tree,
not an assumed linear cycle order. A path is invoked only after proving that
the two pentagons are exactly the two leaves. Genuine Steiner branches are
assigned to one side and separated from other sides on actual bridges. Long
connectors, subdivisions, irrelevant connector branches, and arbitrary trees
at core or connector vertices therefore change neither retained cycle counts
nor packet bounds.

In fully shared arguments, outside components are acyclic and have a unique
cyclic-hull attachment. Assigning each one wholly to the territory owning that
attachment preserves connectedness and inducedness. Every packet theorem cited
in the ledgers explicitly permits arbitrary attached trees, and the mixed
packets permit arbitrary bridge connectors.

## 10. Strictness audit

No strict `>0` term is charged as a fixed positive margin.

- Openings are paid only by uniform bounds `>1`, `>2`, or `>3` as required.
- Hostile pentagons and hostile `Q` cycles are paired only with uniform credits
  exceeding `delta` or `delta_q`.
- Qualitative tetracyclic/pentacyclic positivity is added only to nonnegative or
  strict-positive companions, never to a negative singleton or a tree cost.
- Equality-level integer budgets remain strict because the paying packet bound
  is strict, e.g. `TTT>2` against two openings and `TTTT>3` against up to three.
- SAFE zero totals are accepted only when at least one summand is strict.

Therefore every residual construction ends with a genuine strict inequality,
and every nonresidual construction is strict already at the DNN step.

## Final synthesis

The sharp DNN classification reduces all connected hexacyclic cacti to
`TTTTTQ` and `TTTTPP`. The shared-cut connected/disconnected dichotomy is
exhaustive. Disconnected `TTTTTQ` is proved by the triangular leaf-cluster
argument and the five-triangle margin. All 28 disconnected `TTTTPP` colored
partitions are proved after incorporating the E1 and E2 supplements. The two
fully shared exact censuses resolve every ordinary incidence split, and the
three canonical exception mechanisms (the bouquets and the saturated pentagon
hub) are proved by explicit induced territories. Connector topology, interval
ownership, arbitrary attached trees, and strict budgets all survive audit.

**ACCEPT.** The theorem is mathematically complete in the existing research
files. The remaining work is expository integration into a single manuscript,
not a proof obligation. This verdict agrees with the separately produced
premise-by-premise reconstruction in
`research/hexacyclic-independent-reconstruction-2026-07-26.md`, which rederived
the residual frontier and regenerated the partition and incidence totals rather
than assuming this synthesis.
