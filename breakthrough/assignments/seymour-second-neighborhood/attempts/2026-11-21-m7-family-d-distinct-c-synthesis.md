# Family D outside the common-`C` branch: exact geometry and limits of the row searches

## Status and exact scope

This report concerns only the order-18, seven-hole normal form and the
**distinct-low, disjoint-witness-set** family D.  Let the two high vertices be
`r,q`, let all other vertices be low, and choose distinct low witnesses
`u->r`, `v->q` such that no low vertex robustly witnesses both highs.  For
`s in {u,v}` put

```
A_s=N+(s),  B_s=N++(s),
C_s=V(D)\({s} union A_s union B_s),  S_s={s} union A_s.
```

Thus `|A_s|=8`, `|B_s|=7`, `|C_s|=2`.  Robustness means

```
N++_{D-r}(u)=N++_D(u),  N++_{D-q}(v)=N++_D(v),       (R)
```

where `N++` is directed distance **exactly** two.  This report treats

```
k=|C_u intersect C_v| in {0,1}.                      (K)
```

The certified branch `k=2`, equivalently `C_u=C_v`, is outside scope.  Nothing
here eliminates either remaining value of `k`, all of family D, `m=7`, or the
Seymour conjecture.

There are two different products below which must not be confused:

* the overlap table `M` is an exact partition cell;
* a hole-zone vector is a further exact projection once the geometry is fixed;
* the older stage-1/stage-2 solver statuses are exploratory and are **not**
  retained as theorems.

## 1. Exact overlap geometry

Record the four distinguished locations

```
lambda_u = layer of q in the u-partition,
lambda_v = layer of r in the v-partition,
sigma_u  = layer of v in the u-partition,
sigma_v  = layer of u in the v-partition,             (1)
```

in `{A,B,C}`.  The pair `(sigma_u,sigma_v)=(A,A)` is impossible because it
would give the digon `u<->v`.

For the fourteen ordinary vertices `V\{u,v,r,q}`, define the `3 x 3`
overlap-count table

```
M_XY = |(X_u intersect Y_v) \ {u,v,r,q}|,  X,Y in {A,B,C}.       (2)
```

For fixed data `(lambda_u,lambda_v,sigma_u,sigma_v,k)`, the table is exact
precisely when it is nonnegative, `M_CC=k`, and its margins are

```
row_X(M) = |X_u| - 1[sigma_u=X] - 1[A=X] - 1[lambda_u=X],
col_Y(M) = |Y_v| - 1[sigma_v=Y] - 1[lambda_v=Y] - 1[A=Y],        (3)
```

with layer sizes `(8,7,2)`.  Conversely, assigning the fourteen distinct ordinary labels to cells of a
table satisfying (3), then adjoining

```
u:(root,sigma_v), v:(sigma_u,root),
r:(A,lambda_v),   q:(lambda_u,A),                    (4)
```

produces a pair of set partitions with the recorded data, and every such pair
has exactly this data.  Thus `(1)--(3)`, modulo the exchange
`(u,r)<->(v,q)` and matrix transpose, give an exhaustive, disjoint cover by
**overlap-count types**.  A type is a quotient cell, not a single labelled
partition and not a graph cell.

### Pair-status restrictions forced by exact layers

For each root `s`, exact rooted semantics force

```
s -> A_s;
s !-> B_s union C_s;
({s} union A_s) !-> C_s.                              (5)
```

The last line is necessary: an arc from `s` or an `A_s` vertex into `C_s`
would make that endpoint first or exact-second from `s`.  Conditions (5), for
both roots, determine for every unordered pair a set of permitted statuses
`{hole, x->y, y->x}`.  An empty status set kills the geometry.

Exact outdegrees (nine at `r,q`, eight elsewhere) can then be checked by an
integral lower-bound flow: every unordered pair supplies either one unit to its
tail or zero units if it is a hole, and each vertex receives its prescribed
outdegree.  Since there are `153` pairs and total outdegree is `146`, any such
assignment automatically has exactly seven holes.  This is an exact test for
**degree/status feasibility**, but still does not test exact second
neighborhoods for vertices other than the two roots, global badness, or arc
minimality.

The transparent companion audit obtains:

```
                         k=0       k=1
raw overlap-count types  1216       462
root-exchange orbits      647       253
degree-feasible orbits    212        50
```

The first two numbers are a census of exact overlap-count types.  The third
is an exact finite projection under (5) and the prescribed degrees.  It is not a
census of graph completions: many status assignments can project to one row,
and some rows may have no completion once omitted hypotheses are imposed.

## 2. Sound robustness and disjoint-witness-set constraints

For every `b in B_u`, (R) requires an alternate predecessor after deleting
`r`; symmetrically at `v`:

```
exists a in A_u\{r}: a->b,
exists a in A_v\{q}: a->b.                            (6)
```

This is pointwise support, not a demand for distinct supporting vertices.
At the status-projection level, retaining a row only when each clause in (6)
has at least one permitted arc is a sound necessary filter.  It leaves

```
                         k=0       k=1
support-feasible orbits   201        42.               (7)
```

These `201+42=243` rows form the sharpest exact, transparent next cover
retained here.  “Exact” means each row fixes all four distinguished locations
and all nine entries of `M`; “next cover” means every genuine family-D graph
with `k=0` or `1` maps to one of them.  The list is intentionally generated by
the checker rather than copied as 243 opaque lines into this note.

The disjoint top-level classification adds another necessary condition.  If
`q in A_u`, then `u->q`; since `u` is tight and no low vertex robustly witnesses
both highs, deletion of `q` is not robust for `u`.  Vertex deletion can only
remove old exact-two paths.  Therefore there is an endpoint `b_q in B_u` with

```
{a in A_u : a->b_q} = {q}.                            (8u)
```

Likewise, if `r in A_v`, there is `b_r in B_v` with

```
{a in A_v : a->b_r} = {r}.                            (8v)
```

No such endpoint is required when the corresponding cross-high is not in the
root's `A` layer.  The endpoints in (8u),(8v) need not be distinct unless an
additional argument proves that.  Forcing some admissible endpoint for every
applicable clause and rerunning degree flow leaves, observationally,

```
                         k=0       k=1
private-endpoint orbits   128        22.               (9)
```

The implication (8) is a theorem; the count (9) is a checked finite projection.
It is **not** promoted to the retained exact next cover because the present
small checker verifies feasibility by finding one status assignment, not by
emitting all assignments or an independently checkable infeasibility
certificate for each of the other 93 support rows.  It is a useful proposed
refinement, not an UNSAT result.

## 3. Exact hole synchronization and overlap zones

Let `M_h` be the common seven-hole set.  Define the rooted zone

```
Z_s = {holes with one endpoint in C_s and the other in S_s union C_s}.       (10)
```

Put

```
epsilon_u=1[q in C_u], epsilon_v=1[r in C_v],
rho_s=e(C_s,B_s).                                      (11)
```

The exact one-root ledger gives

```
|Z_s|=3+rho_s-epsilon_s,
|M_h\Z_s|=4+epsilon_s-rho_s.                           (12)
```

Partition the same seven holes into the four synchronized bins

```
h_ij = |{e in M_h : 1[e in Z_u]=i, 1[e in Z_v]=j}|.   (13)
```

Then, exactly,

```
h_00+h_10+h_01+h_11=7,
h_10+h_11=3+rho_u-epsilon_u,
h_01+h_11=3+rho_v-epsilon_v.                           (14)
```

In particular

```
h_11 >= rho_u+rho_v-1-epsilon_u-epsilon_v.             (15)
```

Equation (15) is only inclusion-exclusion; using its lower bound as though it
were the actual value of `h_11` is unsound.

The geometry of `Z_u intersect Z_v` is exact as follows.  Write
`S_s={s} union A_s`.

* If `k=0`, put `C_u={x_0,x_1}`, `C_v={y_0,y_1}`.  The common-zone candidate
  pairs are exactly

  ```
  {x--y : x in C_u intersect S_v, y in C_v intersect S_u}.       (16)
  ```

  Thus the familiar `2 x 2` cut is an overcover unless the cross-membership
  conditions in (16) are retained.  After also removing pairs whose status
  cannot be a hole under (5), the number of candidates is an exact geometry
  capacity `cap(g)`.  In every feasible synchronized vector, `h_11<=cap(g)`.

* If `k=1`, write `C_u={z,x}`, `C_v={z,y}`.  The common-zone candidate pairs
  are exactly

  ```
  {z--w : w != z, w in (S_u union C_u) intersect (S_v union C_v)}
  union ({x--y} if x in S_v and y in S_u),             (17)
  ```

  again intersected with hole-permitted statuses.  This includes holes
  incident with `z`; replacing it by a `2 x 2` cross-cut is false.

The formulas (16),(17) follow directly by requiring an unordered pair to meet
the definition (10) for both roots.  They are the sharpest proved overlap
geometry statement in this report.

For reference, an additional exact-flow enumeration of feasible four-bin
vectors over the private-endpoint rows found

```
                         k=0       k=1
geometry rows             128        22
(geometry, h-vector)      553       366
seven-feature signatures   81       282.               (18)
```

Here an `h-vector` is `(h_00,h_10,h_01,h_11)`.  Each pair
`(exact geometry, exact h-vector)` is a well-defined projection cell.  But the
553 and 366 enumerated rows are only the rows for which the particular flow
relaxation found a status assignment; they are not independently certified as
an exhaustive minimal cover, and the compressed 81/282 seven-feature
signatures overlap many exact geometries.  They must not be called graph cells.

## 4. What the stage-1/stage-2 experiments actually meant

The exploratory Z3 routine fixed one row from (18), introduced one Boolean arc
per ordered pair, and imposed:

1. looplessness and no digons;
2. the pair-status restrictions (5);
3. exact outdegrees;
4. the exact four hole-bin cardinalities;
5. the selected robustness support clauses (6);
6. the private-endpoint clauses (8) when applicable.

It then defined exact-two variables by

```
Q(i,j) = not(i->j) and exists m distinct from i,j: i->m and m->j.            (19)
```

Thus this particular routine did preserve exact-distance semantics.

**Stage 1** (`badmode=1`) did *not* impose global badness.  It imposed the
strict badness bound only on a selected local candidate set:

```
C_u intersect C_v, if nonempty; otherwise all of C_u.  (20)
```

So for `k=1` it constrained only the shared inaccessible vertex; for `k=0` it
constrained the two `u`-inaccessibles.  The initial five-second run reported

```
k=0: SAT 269, UNSAT 250, UNKNOWN 34  (553 rows),
k=1: SAT 187, UNSAT 165, UNKNOWN 14  (366 rows).        (21)
```

A ten-second rerun for `k=1` reported

```
SAT 187, UNSAT 168, UNKNOWN 11; 198 non-UNSAT rows.     (22)
```

**Stage 2** (`badmode=2`) reran those 198 `k=1` non-UNSAT rows with the strict
badness bound on every vertex and a 30-second timeout.  It reported

```
UNSAT 176, UNKNOWN 22, SAT 0.                           (23)
```

The attempted analogous `k=0` campaign was aborted and has no result.

### Why none of (21)--(23) is a theorem

These were temporary, timeout-dependent solver calls.  No retained CNF,
manifest, model decoding, proof trace, DRAT/LRAT certificate, independent
formula reconstructor, or independent UNSAT replay exists.  An `UNKNOWN` is no
mathematical status; a bare `UNSAT` is not a certificate; absence of `SAT` in
one timed run proves nothing.  Even the SAT rows were not decoded into full
family-D graphs.  Accordingly:

* no row is eliminated here on the strength of (21)--(23);
* the 22 stage-2 unknowns are not “survivors” in a theorem-level cover;
* there is no stage-2 statement at all for `k=0`;
* the temporary special-cell probes and forced-arc experiments are likewise
  non-retained evidence only.

The only legitimate use of these outputs is heuristic prioritization if a
future campaign reconstructs exact CNFs and emits checkable proof artifacts.

## 5. Theorem-level outcome and exact next task

> **Finite overlap-cover lemma.**  Under the hypotheses at the start of this
> report and `k in {0,1}`, every graph determines, up to exchanging
> `(u,r)` with `(v,q)`, an exact overlap cell `(1)--(3)` satisfying the forced
> statuses (5), exact degrees, and pointwise support (6).  A transparent
> exhaustive audit lists exactly 201 such cells for `k=0` and 42 for `k=1`.
> In each cell the common holes obey (12)--(15), and their possible common-zone
> pairs are exactly (16) or (17).

The mathematical proof is the bijection (2)--(4), the layer implications (5),
the deletion-support implication (6), and the direct zone-membership
calculation (12)--(17).  The script is a finite arithmetic audit and emits no
global SNC conclusion.

The sharpest safe next finite cover **established in this report** is therefore
the **243 exact geometry cells** in (7).  This is not a proof that no coarser
exact quotient exists; it is the furthest one reached here without relying on
uncertified pruning.  For each one, the next proof-producing refinement
should add:

1. the conditional private endpoints (8), without presuming the two endpoints
   distinct;
2. one exact synchronized hole vector satisfying (14), actual pair capacities
   (16)/(17), and all one-root row identities;
3. full exact-distance biconditionals (19), global strict badness, both full
   deletion equalities (R), and only proved minimality clauses;
4. deterministic CNF bytes plus independently reconstructed bytes and a
   checkable proof for every UNSAT leaf, or a decoded graph for every SAT leaf.

Until that campaign exists, 128/22, 553/366, 81/282, and the solver status
counts remain observations at the exact scopes stated above.

## Reproduction

From the assignment directory:

```
python3 experiments/m7_family_d_distinct_low_overlap_audit.py
```

Expected terminal lines are

```
PASS k=0: raw=1216, root-swap-orbits=647, degree-orbits=212, support-orbits=201, private-orbits=128
PASS k=1: raw=462, root-swap-orbits=253, degree-orbits=50, support-orbits=42, private-orbits=22
PASS exact finite projection audit (not a completion/UNSAT proof)
```
