# R321 complete physical closure — packet theorem and proof

## Status and scope

Status: **PROVED R321 PACKET THEOREM**. This note closes the complete physical
`R321` residual lane stated below. It does not prove the full multiblock
statement, the connected rank-seven theorem, or any single-block case. No
publication claim follows from this packet alone. The accompanying Python
program is finite corroboration and an adjacency-only semantic gate; it is not
the universal proof. This note supplies the universal block-cut argument.

For a finite graph `H`, write

```text
sigma(H) = s+(H) - |V(H)|.
```

### Theorem (physical R321)

Let `G` be a finite simple connected graph of cyclomatic rank seven. Suppose
its positive-rank maximal vertex-biconnected blocks, as reconstructed from its
adjacency, are exactly

* one literal, unsubdivided `K4` block `B`;
* one literal `Theta(1,2,r)` block `D`, `r>=2`; and
* two literal cycle blocks.

Suppose further that the exact rank-seven DNN residual sieve places the
adjacency-derived inventory in one of

```text
K4 + Theta(1,2,r) + C3 + C3,       r>=2,              (R321-a)
K4 + Theta(1,2,2) + C3 + C5.                            (R321-b)
```

Here `Theta(1,2,2)=K4-e` is the literal diamond. Arbitrary physical bridge
connectors, block-cut nesting, repeated articulation vertices, connector
branching, and arbitrary finite tree attachments at any vertices are allowed.
Then

```text
sigma(G) > 0.
```

No conclusion is asserted for a subdivided `K4`, a rank-two block outside the
displayed theta family, another cycle profile, another rank partition, or any
single-block/global rank-seven lane.

## 1. Independently pinned analytic inputs

The proof uses only these fixed estimates.

1. **Induced superadditivity.** For every original-vertex partition
   `V(G)=dot_union V_i`,

   ```text
   sigma(G) >= sum_i sigma(G[V_i]).
   ```

2. **Universal connected floor.** Every nonempty connected graph `H` has

   ```text
   sigma(H) >= -1.
   ```

3. **Fixed-rank connected results.** If connected `H` has cyclomatic rank
   two, three, or four, respectively, then

   ```text
   rank 2: sigma(H)>0,
   rank 3: sigma(H)>=0,
   rank 4: sigma(H)>=0.
   ```

4. **Triangular unicycle.** A connected graph whose unique positive block is a
   literal triangle, with arbitrary bridge-tree attachments, has `sigma>0`.

5. **Rooted literal K4.** A connected graph whose unique positive block is a
   literal `K4`, with arbitrary bridge trees, has

   ```text
   sigma>2.
   ```

6. **Direct shared-cut literal K4+C3.** If the only positive blocks are a
   literal `K4` and a literal triangle sharing exactly one articulation
   directly, with arbitrary bridge trees, then

   ```text
   sigma>3.
   ```

The fixed-rank statements in item 3 are used only after the induced away
component's rank is recomputed from adjacency. No rank is inferred by deleting
a vertex from an arbitrary biconnected block.

### Source pins on clean source commit `bf0d566e252715f4b9e19c9c4d08e043471881af`

| Contract | Source | SHA-256 | Location |
|---|---|---|---|
| exact R321 residual rows | `positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md` | `3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5` | residual table, especially row `3+2+1+1` |
| induced superadditivity; rank 3 | `all-tricyclic-graphs/paper.tex` | `4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02` | lines 61–87 |
| universal connected floor | `tree-equality-square-energy/paper.tex` | `66370f3cb81546325f0e9a4e19919aa2572f0d147cff6d8baa3f9425e7d82889` | lines 57–70 (and equality proof through line 555) |
| rank 2 | `all-bicyclic-graphs/paper.tex` | `56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da` | lines 56–62 |
| rank 4 | `all-tetracyclic-graphs/paper.tex` | `70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f` | lines 65–71 |
| triangular block graph; rooted K4; direct shared K4+C3 | `packing-two-square-energy/paper.tex` | `9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791` | lines 394–450 and 714–753 |

The last source proves the direct `K4+C3` estimate in the shared-cut branch of
the tetracyclic block-graph argument. It is not transported across a positive
bridge or an intermediate positive block.

## 2. Physical reconstruction and first-bridge partition

Run an edge-stack Tarjan decomposition on `G`. Include every physical `K2`
bridge as a block node. Build the full block-cut incidence tree and root it at
`B`, the literal `K4` block.

Call the other three positive blocks **external**. For each external block
`X`, inspect the unique `B`-to-`X` route. If it contains a physical `K2` block,
select the first such bridge block. Deduplicate the selected bridges over the
three routes.

The selected bridge blocks form an antichain. Indeed, if selected bridge `e2`
were strictly below selected `e1`, every external route through `e2` would
encounter `e1` first, contradicting selection of `e2`. This simultaneous,
deduplicated step precedes every demand/frontier classification; no
minimal-demand dichotomy is used.

Delete exactly the selected physical `K2` edges simultaneously. This gives:

* one root component `R` containing `B`; and
* one complete away component `A_j` for every selected bridge.

These are original-vertex, induced, connected, pairwise disjoint, and
exhaustive. Every later bridge, connector remnant, branch vertex, nested
positive block, and rooted payload remains in exactly one complete component.
A shared first-bridge prefix is cut only once: all external blocks beyond it
stay in the same `A_j`.

Every away component contains at least one external positive block. Its rank is
the sum of the ranks of its intact positive blocks and lies in `{1,2,3,4}`.
Recompute that rank from `G[A_j]`.

* If `rank(A_j)>=2`, the fixed-rank connected theorems give
  `sigma(A_j)>=0`.
* If `rank(A_j)=1`, it contains exactly one external cycle. In `(R321-a)` that
  cycle is a triangle, so `sigma(A_j)>0`. In `(R321-b)` it is either the
  triangle, again positive, or the unique pentagon `P`, for which only the
  universal floor `sigma(A_j)>=-1` is charged.

Consequently:

```text
all first-bridge away pieces are nonnegative,
except possibly one singleton-P away piece in (R321-b).              (2.1)
```

This is why one may not blindly charge every first-bridge component at `-1`.
It is also why one may not claim that cutting the first bridge on the route to
the triangle isolates that triangle: multiple external blocks may share that
bridge prefix.

After the simultaneous split, every external block retained in `R` has a
bridge-free route from `B`.

## 3. Frontier grouping in the bridge-free root component

Let `E_R` be the retained external positive blocks. Define its frontier

```text
F = { X in E_R : no Y in E_R\{X} lies strictly on the B-to-X route }.
```

Thus `F` is the ancestor-minimal antichain of retained external blocks. Every
block in `E_R` lies at or below exactly one member of `F`; hence the frontier
groups all nested demands at their first positive boundary. Since there are
three external blocks globally, `|F|<=3`.

### Exact boundary-open operation

For `X in F`, let `c_X` be its upstream articulation. Work in the current root
vertex set `U=V(R)`. Require `X` intact in `G[U]`. Delete the edges `E(X)` from
`G[U]` and compute components.

Because `X` is a maximal biconnected block, every component of
`G[U]-E(X)` meets `V(X)` in exactly one vertex. If an outside component met
`X` at two vertices, it would give an outside ear between two vertices of
`X`, contradicting maximality of the biconnected block. Let `C_x` be the
component meeting `X` at `x`. Define

```text
W_X = union_{x in V(X)\{c_X}} C_x.                            (3.1)
```

Equivalently, `W_X` consists of `X-c_X` plus all complete descendant owners
through vertices of `X-c_X`. It is nonempty and connected. Its edges are
always recomputed as `E(G[W_X])`, so it is induced by construction. It excludes
`c_X`, which stays upstream once. Since `F` is an antichain, the sets `W_X`
are pairwise disjoint; together with the retained root territory they exhaust
`U`. Every nested external block and every payload follows its first frontier
owner. No cut is copied.

Each `W_X` is a nonempty connected graph, regardless of the internal rank left
after opening `X`; therefore

```text
sigma(G[W_X]) >= -1.                                      (3.2)
```

The opened side may contain a residual local cycle manufactured by deleting
`c_X` from the boundary block (for example when `c_X` is an internal
articulation of `Theta(1,2,r)`). This is allowed: the authenticated fact is the
exact boundary-open operation, inducedness, and connectedness—not a bijection
between local positive blocks and intact original blocks. No false assertion
such as `rank(X-c_X)<=1` is used.

## 4. Exhaustive root ledgers

Let `p` be `1` when a singleton pentagon away component from `(R321-b)` is
present and `0` otherwise. By (2.1), all away components together contribute
at least `-p`.

### Case A: `|F|<=2` and `p=0`

Boundary-open every frontier block once. The retained root territory has
literal `K4` as its unique positive block, plus bridge trees, so it has credit
`>2`. By (3.2),

```text
sigma(G) > 2 - |F| >= 0.                                  (4.1)
```

This includes every non-direct triangle lying behind a theta or another cycle:
that triangle remains intact inside the first complete frontier side and is
not separately opened.

### Case B: `|F|=3`

Then no external block was sent away, and every external block is itself a
frontier block: with only three externals, three minimal blocks are pairwise
incomparable and exhaust the inventory. In particular, a guaranteed literal
triangle `T` belongs to `F`.

There is no bridge on its route in `R`, and no intervening positive block by
frontier minimality. The block-cut route therefore is exactly

```text
B - c - T.
```

Retain the direct shared-cut `K4+T` anchor and boundary-open the other two
frontier blocks. Thus

```text
sigma(G) > 3 - 1 - 1 = 1.                                 (4.2)
```

### Case C: the singleton pentagon is away (`p=1`)

This occurs only in `(R321-b)`. The root contains a subset of `{D,T}`.

* If `|F|<=1`, use the rooted `K4` anchor and open the at most one frontier:

  ```text
  sigma(G) > 2 - |F| - 1 >= 0.                            (4.3)
  ```

* If `|F|=2`, then both `D` and `T` are retained and frontier-minimal. The
  triangle is bridge-free and has no intervening positive block, so it is
  directly shared-cut with `B`. Retain `K4+T`, open `D`, and include the away
  pentagon floor:

  ```text
  sigma(G) > 3 - 1 - 1 = 1.                               (4.4)
  ```

Cases A–C exhaust the simultaneous first-bridge/root-frontier topology. In all
cases the strict inequality comes from the authenticated `K4` or `K4+T`
anchor, while every weak side floor is used additively through induced
superadditivity. This proves the packet theorem.

## 5. Hostile ownership checks

* **Shared first-bridge prefix:** deduplication cuts it once before frontier
  analysis. In the countertopology `K4--K2--y` with all three external blocks
  branching at `y`, the single complete away component owns all three
  externals, has recomputed rank four, and receives exactly the connected
  rank-four nonnegative contract. It is never mistyped as an isolated
  triangle or as three root frontiers.
* **Triangle behind theta:** theta is the sole frontier on that branch; opening
  theta once carries the intact triangle in `W_D`. The route does not invoke a
  direct `K4+T` contract.
* **Repeated common cut:** every opened side excludes the same physical cut;
  the retained territory owns it once.
* **Nested all three externals:** there is one frontier, hence one connected
  generic side, not three debits.
* **Long connectors and branches:** only the first selected bridge is deleted;
  all later connector vertices remain with one complete away component.
* **Arbitrary theta cut orbit:** no theta vertex is deleted analytically. The
  whole `D-c` descendant side is reconstructed and receives only the universal
  connected floor.
* **Positive-block subdivision:** not invariant. Subdividing the literal `K4`
  or changing `Theta(1,2,r)` typing changes or rejects the lane.
* **K2 subdivision / rooted-tree growth:** invariant at the semantic level;
  it changes vertex counts but not external-block grouping or the ledger
  branch.

## 6. Adjacency-only implementation contract

The companion verifier:

1. accepts only a nonempty `frozenset` of vertices and `frozenset` of unordered
   two-element `frozenset` edges;
2. reconstructs iterative Tarjan blocks and every physical bridge;
3. authenticates one literal `K4`, one adjacency-derived
   `Theta(1,2,r)`, and two literal cycles with exact residual profile;
4. builds and roots the full block-cut tree;
5. derives/deduplicates simultaneous first bridges;
6. recomputes every away component, rank, and positive inventory;
7. derives ancestor-minimal root frontiers;
8. performs (3.1) on original vertices and authenticates the exact removed
   boundary edge set and owner components;
9. verifies inducedness, connectedness, disjointness, exhaustiveness, and unique
   cut ownership; intact-block/no-merge inventory is enforced on physical-K2
   away components and retained anchors, while frontier residual cycles are
   deliberately allowed and charged only by the connected floor;
10. assigns only fixed source-pinned contracts and independently replays the
    structural plan and integer ledger;
11. audits opaque relabeling, K2/tree expansion, shared bridge prefixes,
    direct/nested/bridge rewires, hostile adjacency mutations, in-memory source
    mutation, and contract-table mutation. The release procedure separately
    runs the verifier normally and under `python -O`, then compares their output
    bytes externally.

Finite fixtures are corroboration only. Universal coverage follows from the
block-cut tree argument in Sections 2–4, not from extrapolation over fixture
sizes.
