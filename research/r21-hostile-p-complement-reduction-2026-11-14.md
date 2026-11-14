# R21 hostile-pentagon complement: narrow block-cut reduction

Date: 2026-11-14. Status: **NONPROMOTIONAL / conditional analytic lemma**.

## Scope and exclusions

Let `sigma(X)=s+(X)-|V(X)|`. This note treats only the following oriented
`R21` situation. As a **separate prior physical input**, require a typed-row
certificate that an actual bridge of the full rank-seven graph isolates a
rank-one side whose unique cyclic block is literally `P=C5` (with arbitrary
one-root tree branches). **This artifact does not prove that typing.** Its
other induced side is a connected rank-six graph `H` whose positive-rank
blocks are exactly

```text
D + T0 + T1 + T2 + T3,
D=K4-e,  Ti=C3 literally.
```

Under that prior certificate, the isolated rank-one side is the actual
pentagonal unicycle `P=C5`, not an arbitrary nontriangular cycle silently
renamed `P`. The symbolic letter `P` in the `D+T^4+P` residual-sieve line does
not itself establish this physical type.

Root the block-cut tree of `H` at `D`. No statement here concerns the theta
row of `R21`, any other packet key, an arbitrary rank-one/rank-six split, or a
generic bridge theorem.

The following four inequalities are external hypotheses, not outputs of this
note:

1. every attached diamond with arbitrary **one-root** tree branches has
   `sigma(D)>1`;
2. every bridge-free shared-cut `D+T` packet with arbitrary one-root tree
   branches has `sigma(D+T)>2`;
3. every bridge-free shared-cut `D+T+T` packet, including direct/direct and
   direct/nested incidences and arbitrary one-root tree branches, has
   `sigma(D+T+T)>3`;
4. every connected triangular block graph with at least one triangle,
   allowing bridge blocks and arbitrary attached trees, has `sigma>0`.

For later bookkeeping write `W` for a complete connected territory. A nonempty
rank-zero `W` is a tree and has `sigma(W)=-1`; a rank-one triangular unicyclic
`W` has `sigma(W)>0`; and every rank-at-least-two nonunicyclic all-triangle
cactus `W` also has `sigma(W)>0` by hypothesis 4. Only this `>0` conclusion,
never `>r-1`, is used below.

The exact source statements and symbolic-row receipt are

* `positive-square-energy/pentacyclic-general/
  doubled-c4-111-two-triangles-retained-packet.md`, lines 34--90: the narrow
  attached `D+T^k`, `0<=k<=2`, estimates, with explicit exclusion of a
  multi-interface acyclic connector;
* `positive-square-energy/pentacyclic-general/
  diamond-two-triangle-exact-packet.md`, lines 14--31, and executable child
  `research/diamond-two-triangle-packet-verifier.py`: direct/direct and
  direct/nested bridge-free `D+T+T`, arbitrary rooted trees, and positive
  bridge connectors excluded;
* `packing-two-square-energy/paper.tex`, Corollary
  `cor:triangular-block`: every connected triangular block graph containing a
  triangle satisfies `s^+>|V|`; bridge blocks and arbitrary attached trees are
  expressly allowed;
* `all-tricyclic-cacti/paper.tex`, Lemma `lem:packets`(2): with arbitrary tree
  attachments, a unicyclic `C_q` cactus for `q=1 mod 4` has
  `s^+>=|V|-delta_q`, `delta_q=sec(pi/q)-1`; and
* `positive-square-energy/heptacyclic-general/
  rank-seven-multiblock-debit-ledger.md`: the exact residual text contains the
  symbolic row `D+T^4+P` and, separately, displayed `C5` debit/credit formulas.
  It does **not** identify that occurrence of `P` as `C5`; the prior physical
  typed-row certificate above is an additional hypothesis, not a conclusion
  drawn from this source.

Conditional on the prior typing `P=C5`, the pinned hostile-unicycle source
states `delta_q=sec(pi/q)-1` and, in its explicit pentagon specialization,
`delta_5=sec(pi/5)-1=sqrt(5)-2`. The exact integer inequalities
`2^2<5<3^2` give `2<sqrt(5)<3`, hence `0<delta_5<1`. Therefore its
`q=5` unicycle inequality gives

```text
sigma(P)>=-delta_5>-1.                                      (P)
```

The companion verifier checks pinned bytes and exact statement/scope tokens
for all five prose sources, including both the symbolic residual line and the
separate exact `C5` arithmetic. Those text checks do not supply the missing
physical typed-row certificate. The verifier also **executes** the `D+T+T`
semantic child and
the 307-state selector child in both normal and `-O` modes and checks canonical
outputs. It does not execute the prose-only `D`, `D+T`, triangular-block,
hostile-unicycle, or residual-sieve sources, and it does not reprove any
spectral inequality. Thus the hashes are change detectors, the token checks
are statement receipts, and only the two named programs are replayed semantic
children.

## First-hull-bridge operation

Let `C` be the minimal block-cut subtree spanning `D,T0,T1,T2,T3`; call it the
**cyclic hull**. Starting at `D`, delete each first actual `K2` bridge block of
`C`: that is, on every root-to-triangle route, delete the first bridge block
encountered, and do not make a second cut inside the resulting away component.
This is not a cut of an arbitrary bridge in an attached rooted tree.

Each away component contains at least one `Ti`, because the cut bridge lies in
`C`. In this profile it contains only triangle cyclic blocks, so it is a
connected triangular block graph and hypothesis 4 gives strict positive
credit (only the weaker floor zero is booked). No acyclic away component is
created or booked as nonnegative.

Work in the original graph before taking any quotient. Every maximal acyclic
off-core component meets the retained cyclic/connector structure at exactly
one physical root: two distinct roots would give that tree component plus the
unique retained route between the roots as an additional cyclic block,
contrary to maximal acyclicity and the stated block inventory. Assign each such
component separately by that root. A component rooted at a represented cut
stays upstream; one rooted at a private vertex of a complete away territory
follows that territory. Physical connector branch points and all their acyclic
branches likewise remain inside the complete induced territory containing
their roots.

After those cuts, the root component has a bridge-free shared-cut cluster
consisting of `D` and `k` of the four triangles, for some `0<=k<=4`. Contracting
a maximal positive `K2` chain to the predicate `length>0` preserves which
first-hull bridge is cut and the marked-block owner sets. It may not be
contracted to length zero, because that changes a bridge incidence into a
shared cut. Physical connector branch points are retained during the
original-vertex ownership proof; their internal topology is forgotten by the
finite quotient only afterward, because the triangular-block theorem is
uniform over bridge blocks.

## Root-cluster least-depth lemma

**Lemma.** If `k>=2`, choose the two triangle block nodes `Ta,Tb` of least
depth from `D` in the rooted shared-cut incidence tree, breaking ties
arbitrarily. The minimal block-cut subtree spanning `D,Ta,Tb` contains no
other triangle block node.

**Proof.** Its vertex set is `P(D,Ta) union P(D,Tb)`. If a third marked
triangle `Tc` lay in that union, it would be a proper ancestor of `Ta` or
`Tb`: it is distinct from the two endpoints, and every node on a rooted path
other than its endpoint has strictly smaller depth. Hence `Tc` would have
strictly smaller depth than one of the two least-depth triangle nodes, a
contradiction. The retained subtree has no `K2` block because the simultaneous
first/rootmost actual K2 blocks on all `D`-to-triangle cyclic-hull routes were
deleted before forming the root cluster. It is therefore in the narrow
bridge-free shared-cut `D+T+T` scope. QED.

Let `K0` be this minimal `D,Ta,Tb` incidence hull and form its cut closure
`S` by adjoining every represented cut incident with a retained `D/T` block.
The fact that every cyclic edge leaving `S` is
`represented cut c -> unselected T` uses **both** this cut closure and the
prior simultaneous removal of the rootmost actual K2 blocks on cyclic-hull
routes; cut closure alone would still permit a retained block--new cut--`K2`
frontier.

Now return to original vertices. Let `A` denote the whole root component
remaining after the simultaneous first-hull-bridge cuts. Put every vertex of
each retained block and every represented cut in its upstream anchor set
`A0`. Fold into `A0` every cycle-free off-`S` component rooted at a vertex of
`A0`, one component at a time. For each edge `c->T` leaving `S`, remove the
upstream cut `c` and put all
original vertices in that connected downstream block-cut component into one
set `W`; if two unselected triangles leave the same `c`, they define two
separate `W` sets. Include every physical K2-chain remnant, connector branch
point, private rooted acyclic component, and nested triangle in the unique set
containing its physical root. First-hull-bridge away sides were already made
separate `bridge:<triangle-set>` sets by the preceding simultaneous deletion.

Thus `A0` and the opened `W` sets partition `A`; together with the first-hull-
bridge away sets they partition `H`. This is an original-graph vertex
partition, not a conclusion of the finite verifier. Connectivity follows
because each `W` is a complete component after its one upstream articulation
is removed, and `A0` contains the connecting incidence hull plus every
upstream cut. Disjointness follows because the
block-cut object is a tree and each boundary cut is kept only in `A`; two
different downstream components cannot share any other vertex. Exhaustiveness
follows by assigning every block-cut component at its first boundary and every
acyclic component at its unique physical root. Finally, use the graphs induced
by these vertex sets. Any original edge whose endpoints lie in one set is then
present, while edges crossing sets are simply discarded for induced
square-energy superadditivity. Thus the pieces are connected, induced,
pairwise vertex-disjoint, and exhaustive.

Let `m` be the number of opened `W` territories. Each contains at least one of
the `k-2` unselected triangles, so `m<=k-2`. The conservative lower bound
`sigma(W)>=-1` for each complete first-boundary territory is enough (although
the trichotomy above is stronger whenever `W` keeps positive rank).

## Credit dispatch

The first-hull-bridge away components add a nonnegative amount. For the root
component:

* `k=0`: `A=A0`, and hypothesis 1 gives `sigma(A)>1`;
* `k=1`: `A=A0`, and hypothesis 2 gives `sigma(A)>2`;
* `k>=2`: induced superadditivity, hypothesis 3 for `A0`, and the `m`
  opened first-boundary debits give the exact arithmetic

  ```text
  sigma(A) >= sigma(A0) + sum_W sigma(W)
           > 3-m >= 3-(k-2) >= 1,
  ```

  because `m<=k-2` and `k<=4`.

Thus `sigma(H)>1` in every case. Combining this with the already isolated
physically authenticated pentagonal side's `(P)` bound `sigma(P)>-1` gives
strict positive total credit by induced square-energy superadditivity. The
conclusion is conditional on the four analytic hypotheses **and** the separate
prior physical typed-row certificate `P=C5`. Neither this note nor its
companion verifier proves that typing. It does not close any other row.

## Exact finite quotient and the `307` versus `606,783` counts

The companion verifier is

```text
research/r21-reduced-block-cut-hull-verifier.py
```

It generates **labelled decorated abstract quotient states**, not physical
graphs and not graph-isomorphism classes. For fixed `k` it records:

1. which labelled triangles remain in the root cluster;
2. the labelled bipartite shared-cut incidence tree;
3. a physical port number at each incidence (`4` ports of `D`, `3` per
   triangle), with one block vertex not reused by two distinct cut nodes;
4. a set partition of the other labelled triangles into complete
   first-cyclic-hull-bridge away groups;
5. the positivity of each rootmost bridge connection, exact destination
   labels for aggregate `payload_mass`, and literal-triangle witnesses.

The record does **not** contain internal connector branch topology or physical
payload components. Those data are quotient-erased only after the preceding
original-vertex proof assigns every branch point and every separately rooted
acyclic component to exactly one destination territory. `payload_mass` is the
total erased vertex count in all such components for destination `upstream`,
each `opened:<triangle-set>`, and each `bridge:<triangle-set>`; it is not one
physical rooted tree.

For `k=4`, before port decoration there are exactly `307` realizable labelled
shared-cut incidence skeletons. This is the formalizer's count. The unrestricted
abstract hyper-tree generator has four additional stars centred at one
triangle with four distinct cut nodes; those are not realizable by a literal
`C3`, which has only three physical vertices, and are rejected. Adding all
port maps gives `559,872` decorated root clusters for `k=4`. Summing over all
choices of `k`, all valid port maps, and all Bell partitions of the `4-k`
away triangle labels gives `606,783` labelled decorated states. The large
number is therefore not a competing skeleton count.

The census is exhaustive for the stated abstract quotient because, **after**
the original-vertex territory assignment, every physical `H` maps
deterministically to these data: Tarjan's root-cluster block-cut tree supplies
(1)--(3), the rootmost cyclic-hull bridge cuts supply (4), and post-proof
quotienting supplies (5). Conversely, each generated root-cluster record
respects every retained block's port capacity and each Bell part names one
complete already-owned bridge territory. It does not reconstruct internal
bridge branching, payload roots, or adjacency. The verifier checks exact
marked-block ownership and quotient labels only; the connected/induced/
disjoint/exhaustive original-vertex lift is the prose proof above. It also does
not reprove the external spectral inequalities.

## Safe and unsafe normalizations

* **Safe:** shorten a maximal degree-two K2-only chain from any positive length
  to one edge, while retaining its endpoints and first-hull-bridge status.
* **Unsafe before ownership:** contract that chain to length zero, suppress a
  connector branch point, merge or split represented cut nodes, reuse one
  physical port for two cuts, or move a triangle across a first hull bridge.
  **After** complete original-vertex territory ownership is proved, internal
  bridge branching may be forgotten because hypothesis 4 is topology-uniform.
* **Safe only post-proof:** assign every maximal acyclic component separately
  by its unique physical root, then erase roots/internal shapes and retain only
  per-destination aggregate `payload_mass`; mass is not a physical component
  and never a rank-zero credit group.
* **Unsafe:** suppress a multi-interface acyclic connector as if it were a
  one-root branch, or duplicate/omit an exact destination label.
* **No triangle-length quotient:** each `Ti` is literally the block `C3`, so
  its three segments are `(1,1,1)`. Replacing a segment by a longer path
  changes the physical block away from `T` and leaves this theorem's scope.
* **Never suppressed by the retained root-cluster census:** `D`, any `Ti`,
  represented cut equality, D/triangle port incidence, or the partition into
  first-hull-bridge groups. Internal branch topology is absent only under the
  post-proof quotient just stated.

The verifier fail-closes on the exact `606,783` count, all by-`k` and
port-coloured subtotals, unique canonical signatures, exact channel counts,
and canonical digest. Its hostile tests reject zero-length bridge contraction,
duplicated bridge groups/destination labels, omitted rootmost-K2 deletion, a
subdivided alleged triangle, and a repeated-cut port merge; they also check
that changing aggregate mass within an already fixed destination leaves
dispatch and the ledger unchanged.
