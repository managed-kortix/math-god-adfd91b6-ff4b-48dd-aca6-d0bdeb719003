# Universal DNN theorem for physical hostile unit-stars

## Exact theorem and scope

For a finite graph `H`, write

```text
beta(H)=|E(H)|-|V(H)|+1                         (H connected),
s+(H)=sum_{lambda_i(H)>0} lambda_i(H)^2,
s-(H)=sum_{lambda_i(H)<0} lambda_i(H)^2.
```

Delete every actual bridge of a finite simple connected graph `G`, and let `T`
be the resulting component quotient.  Give a quotient vertex the cyclomatic
rank of its bridge-free component.  Prune zero-rank branches outside the
positive hull and suppress zero-rank degree-two hull vertices, as in
`physical-hull-bridge-reduction/theorem-note.md`.

**Theorem (PHYSICAL-UNIT-STAR-DNN).** Suppose `beta(G)=7` and the reduced
positive hull is a star whose center has weight `c` and whose `k=7-c` leaves
all have weight one.  Suppose every leaf cycle has length

```text
q_i = 1 (mod 4).
```

Then:

1. if `0<=c<=4`, one has `s+(G)>|V(G)|`;
2. if `c=5` and at least one of the two leaf cycles has length at least nine,
   one again has `s+(G)>|V(G)|`.

The theorem is uniform over the actual connected bridge-free center component,
including centers with several positive blocks and internal articulation
vertices.  It is also uniform over repeated or coincident attachment ports,
arbitrary restored physical bridge chains, zero-rank branching vertices, and
arbitrary finite tree payloads on the center, chains, and arms.

For `c=5`, hostile lengths are `5,9,13,...`, so item 2 leaves exactly the arm
length pair `(5,5)` unresolved by this universal estimate.  This is a residual
of the certificate, not a graph counterexample.

The normative machine-readable scope is
`research/fixtures/physical-unit-star-dnn-theorem-manifest.json`.

## Imported analytic facts

For a connected edge-containing graph `H`, let `kappa(H)` be the optimized DNN
constant of `sharp-cactus-dnn/paper.tex`.  We use four established facts from
that source.

1. **Universal LTZ bound:**

   ```text
   kappa(H)<=2|E(H)|-|V(H)|+1.                              (1)
   ```

2. **One-vertex-sum additivity:** if two connected edge-containing graphs meet
   in one actual vertex and have no other cross-edges, then their `kappa`
   constants add exactly.
3. **Atomic values:** `kappa(K2)=1` and

   ```text
   kappa(C_q)=q+epsilon_q,
   epsilon_q=q tan^2(pi/(2q))              (q odd).          (2)
   ```

4. **Spectral inequality:** `s-(H)<=kappa(H)`.

We also use the proved monotonicity and exact comparison

```text
epsilon_5=5-2sqrt(5),
epsilon_q strictly decreases through odd q>=3,
epsilon_5+epsilon_7<1.                                     (3)
```

A digest authenticates the cited bytes; it does not replace the mathematical
proof in those bytes.

## Exact all-bridge decomposition

Let the components obtained after deleting all global bridges be `X_v`.  Their
quotient `T` is a tree.  In the stated star schema, its positive components are
exactly one center component `C` of rank `c` and `k=7-c` rank-one leaf
components.

A connected bridge-free rank-one simple graph is a bare cycle.  Indeed, it is
unicyclic, and every edge off its unique cycle would be a bridge.  Write its
leaf cycles as `C_{q_1},...,C_{q_k}`.  A bridge-free rank-zero component is a
single vertex: a connected rank-zero component is a tree, and any edge of a
nontrivial tree would be a global bridge.  Consequently every edge outside
`C` and the leaf cycles is one of the deleted physical bridges, hence one
`K2` block.  Let `B` be their number.

Root `T` at `C` (or at the central singleton when `c=0`) and reconstruct the
graph outward.  Across each quotient edge, glue its actual `K2` first and then
the child component.  Every gluing intersection is one actual vertex and there
are no other cross-edges.  A child cannot meet the part already built through
a second quotient edge, because that would form a quotient cycle and those
edges would not be bridges.  This remains true at branching singleton
vertices and when several ports coincide.

Finite iteration of exact one-vertex-sum additivity therefore gives

```text
kappa(G)
 = kappa(C)+B+sum_i kappa(C_{q_i})
 = kappa(C)+B+sum_i(q_i+epsilon_{q_i}).                      (4)
```

No articulation is copied in (4).  The center is retained whole, so its
internal block structure is irrelevant to this step.  Every tree-payload edge
is counted once among the global bridges.

For `c>0`, write `e_C=|E(C)|` and `v_C=|V(C)|`.  Then `C` is edge-containing
and

```text
v_C=e_C-c+1.
```

The universal bound (1), applied once to the entire center, gives

```text
kappa(C)<=2e_C-v_C+1=e_C+c.                                 (5)
```

For `c=0`, the reduced-star center is a singleton.  Omit it from the additivity
induction and set `e_C=kappa(C)=0`; (5) remains valid as an identity.  Since
edge sets partition,

```text
m:=|E(G)|=e_C+B+sum_i q_i.                                  (6)
```

Equations (4)--(6) yield the universal physical unit-star estimate

```text
kappa(G)<=m+c+sum_i epsilon_{q_i}.                           (7)
```

This is why no classification of center kernels, blocks, or marked ports is
needed.

## The rows `0<=c<=4`

Put

```text
a=epsilon_5=5-2sqrt(5).
```

Every hostile `q_i` is at least five, so monotonicity gives

```text
kappa(G)<=m+c+(7-c)a.                                       (8)
```

Since `a<1`, the excess on the right of (8) increases with `c`.  For
`0<=c<=4`, its largest value is therefore

```text
4+3a=19-6sqrt(5)<6.                                         (9)
```

The last inequality is exact: it is equivalent to `13<6sqrt(5)`, and both
sides are positive while `169<180` after squaring.

Because `beta(G)=7`, one has `m=|V(G)|+6`.  Combining (8)--(9) with the spectral
inequality gives

```text
s-(G)<m+6,
s+(G)=2m-s-(G)>m-6=|V(G)|.                                (10)
```

Thus all center ranks through four close strictly, independently of the
center's class.

## The `c=5` long-arm refinement

Now `k=2`.  If one hostile arm has length at least nine, the two excesses are
at most `epsilon_5+epsilon_9`.  By strict monotonicity,

```text
epsilon_9<epsilon_7.                                        (11)
```

For completeness, the exact comparison used in (3) can be certified without
decimals.  From `pi<22/7` and `cos x>1-x^2/2`,

```text
cos(pi/7)>1-(22/49)^2/2=2159/2401>7/8,
```

where `8*2159=17272>16807=7*2401`.  Hence

```text
epsilon_7
 =7(1-cos(pi/7))/(1+cos(pi/7))
 <7/15
 <2sqrt(5)-4
 =1-epsilon_5.                                               (12)
```

The second strict inequality is equivalent to `67/30<sqrt(5)`, whose square
is `4489<4500`.  Equations (11)--(12) prove

```text
epsilon_5+epsilon_9<1.                                      (13)
```

The estimate (7) now gives

```text
kappa(G)<m+5+1=m+6,
```

and (10) again yields `s+(G)>|V(G)|`.

When both arms are `C5`, the same coarse estimate gives only

```text
5+2epsilon_5=15-4sqrt(5)>6,
```

because `4sqrt(5)<9` follows from `80<81`.  No conclusion for this row is
claimed here.

## Verification boundary and nonclaims

Run from the repository root:

```text
python3 -I -B research/physical-unit-star-dnn-theorem-verifier.py --print-manifest
python3 -m unittest research/test_physical_unit_star_dnn_theorem_verifier.py
```

The verifier checks canonical scope and dependency locks, the exact symbolic
ledger, the radical inequalities, and hostile scope mutations.  It also
contains a dependency-free Tarjan instance checker.  Given a finite simple
adjacency list, that checker independently finds all global bridges, forms the
component quotient, reduces its positive hull, authenticates the literal
unit-star structure and hostile leaf cycles, and emits the edge ledger (6).
It does not optimize `kappa(C)` numerically; that is unnecessary because (1)
is universal.

This theorem does **not** close the `c=5,(5,5)` row, any `c=6` unit-star, a
one-component rank-seven positive hull, a non-unit-star configuration, or all
heptacyclic graphs.  It does not prove `Gamma>=delta_q`, spectral equality in
the DNN estimate, or any publication or peer-review statement.  Its verifier
imports rather than reproves the LTZ bound, exact DNN additivity, cycle
optimization, spectral DNN inequality, and elementary trigonometric facts.
