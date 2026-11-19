# R31-K residual lane: complete physical closure

## Status, exact scope, and nonclaim

Status: **PROVED R31-K PACKET THEOREM**.  This note closes one residual lane of
the rank-seven multiblock program.  It does not prove the full multiblock
statement, the connected rank-seven theorem, or any single-block case.  No
publication claim follows from this packet alone.

For a graph `X`, put

```text
sigma(X)=s+(X)-|V(X)|.
```

**Theorem (full physical R31-K lane).**  Let `G` be a finite simple connected
graph of cyclomatic rank seven.  Suppose its positive-rank maximal
vertex-biconnected blocks are one literal, unsubdivided `K4` and four literal
cycle blocks, and suppose the exact `R31-K` DNN residual inequality holds:

```text
sum_(four cycles Q) epsilon(Q)>3,

epsilon(C_l)=0                         (l even),
epsilon(C_l)=l tan^2(pi/(2l))          (l odd).
```

Arbitrary block-cut incidence, physical bridge connectors of arbitrary
positive length, repeated or nested cuts, and arbitrary finite rooted-tree
attachments are allowed.  Then

```text
sigma(G)>0.
```

The theorem concerns an actual `K4` block.  A subdivision of a `K4` edge is
not silently identified with `K4`; it belongs to a different rank-three row.

## 1. Exact residual profiles

The sharp cycle facts are

```text
epsilon(C3)=1,
epsilon(C5)=5-2sqrt(5),
epsilon(C_l) strictly decreases through odd l>=3,
epsilon(C_l)=0 for even l,
3(5-2sqrt(5))<2,
2(5-2sqrt(5))>1,
(5-2sqrt(5))+epsilon(C7)<1.
```

Sort the four cycle lengths.  An even cycle contributes zero, so the strict
sum cannot exceed three.  If all four lengths are odd and `h` is the number
of nontriangles, then:

* `h=0` gives `T4`;
* `h=1` gives `T3+odd>=5`;
* `h=2` survives only as `T2+C5+C5`, because replacing either pentagon by a
  cycle of length at least seven makes the two nontriangle excesses less than
  one; and
* `h>=3` fails since `1+3(5-2sqrt(5))<3`.

Thus the residual profiles are exactly

```text
T4,              T3+odd>=5,              T2+C5+C5.       (1)
```

In particular every residual cycle is odd, every residual contains at least
two triangles, and

```text
h<=2.                                                   (2)
```

No profile name or threshold is accepted from an input record by the verifier.

## 2. Analytic packet contracts

Only the following independently proved estimates are used.

1. **Induced superadditivity.**  If the sets `V_i` partition `V(G)`, then
   `sigma(G)>=sum_i sigma(G[V_i])`.
2. **Trees.**  A nonempty tree has `sigma=-1`.
3. **Odd unicyclic floor.**  A unicyclic cactus whose cycle has length
   `q=1 mod 4` satisfies
   `sigma>=-delta_q`, where `delta_q=sec(pi/q)-1<1`; a cycle of length
   `3 mod 4` has positive credit.  In particular every intact residual
   unicycle has `sigma>-1`, and a triangular unicycle has `sigma>0`.
4. **Triangular block graphs.**  Every connected graph whose cyclic blocks are
   triangles and which contains a triangle has `sigma>0`.
5. **Nonunicyclic cacti.**  Every connected cactus of cyclomatic rank at least
   two has `sigma>0`.
6. **Rooted actual `K4`.**  A connected territory whose unique positive-rank
   block is the actual `K4`, with arbitrary bridge trees, has `sigma>2`.
7. **Direct actual `K4+T`.**  A connected territory whose only positive-rank
   blocks are the actual `K4` and one triangle sharing a cut vertex directly,
   with arbitrary bridge trees, has `sigma>3`.  This estimate is never carried
   across a positive connector or an intermediate cycle.

The rooted-`K4` reserve cannot be uniformly increased: if `t` leaves are
attached at every `K4` vertex, exact equitable decomposition gives

```text
sigma=2+(3/2)(sqrt(4t+9)-sqrt(4t+1)) -> 2.
```

Likewise a triangle with `t` leaves at each vertex has credit tending to zero.
The proof below therefore uses strict inequalities exactly; it invents no
uniform positive margin.

## 3. Original-vertex ownership

Run Tarjan on the physical adjacency.  Singleton edge blocks are the actual
bridges, and the full block-cut graph (including bridge-block nodes and cut
vertices) is a tree.  Root it at the `K4` block `B`.

All partitions below are performed on original vertices before any credit is
charged.

### 3.1 Simultaneous first-bridge split

For each of the four cycle blocks whose `B`-to-cycle route contains a bridge,
choose the first bridge block on that route and deduplicate.  The chosen
bridges form an antichain: a bridge below another chosen bridge could not be
first on any route through the upper bridge.  Delete their physical edges
simultaneously.

This produces one induced connected root component `R` containing `B` and
complete induced connected away components `A_1,...,A_a`.  They are pairwise
disjoint and exhaustive.  Every later bridge, connector remnant, nested cycle,
Steiner branch, and rooted payload stays in its first away component.

Every away component is a cactus.  If it contains at least two cycles it has
positive credit.  If it is unicyclic, it is positive when its cycle is a
triangle (or more generally has length `3 mod 4`) and has credit greater than
`-1` otherwise.  Consequently a potentially negative away component contains
a distinct original nontriangle cycle.

No cycle remaining in `R` has a bridge block on its route from `B`.

### 3.2 Ancestor-minimal nontriangles in the root

Among the nontriangle cycle blocks remaining in `R`, select those having no
other root nontriangle strictly between them and `B`.  They form an antichain.
For a selected block `Q`, let `c` be its upstream articulation.  Keep `c`
upstream and let `W_Q` be the complete descendant side consisting of
`Q-c` and every block-cut descendant rooted through a vertex of `Q-c`.

The path `Q-c` is connected.  Maximality of the cycle block implies that a
component outside `Q` cannot meet two vertices of `Q`; otherwise an outside
ear together with a path in `Q` would enlarge its biconnected block.  Hence
each `W_Q` is connected and induced.  Distinct selected blocks give disjoint
sides, every articulation is owned once, and all deeper connectors, cycles,
and rooted payloads remain with their unique first side.

Opening `Q` destroys only that cycle.  Thus `W_Q` is:

* a nonempty tree, with credit `-1`, if no descendant cycle remains;
* an intact residual odd unicycle, with credit greater than `-1`, if one remains; or
* a cactus of rank at least two, with positive credit, otherwise.

A potentially negative `W_Q` is charged to its selected original nontriangle.
The first-bridge away pieces and selected root nontriangles are disjoint.
Therefore, if `s` is the total number of potentially negative pieces produced
in Sections 3.1 and 3.2, then

```text
s<=h.                                                    (3)
```

After removing the `W_Q`, the retained root core `C` has exactly one actual
`K4`, say `k` intact triangle blocks, and bridge-tree material.  It contains no
nontriangle cycle, and every `B`-to-triangle route in `C` is bridge-free.
Also

```text
0<=k<=4-h.                                               (4)
```

## 4. The actual `K4+kT` core decomposition

This phrase denotes the following physical construction, not a profile label.

If `k=0`, the core has the actual `K4` as its unique positive-rank block, so

```text
sigma(C)>2.                                              (5)
```

Suppose `k>=1`.  Choose a triangle `T` of minimum block-cut depth from `B`.
There is no bridge on its route and no intervening positive block: an
intervening triangle would have smaller depth, while all nontriangles were
removed.  Therefore `B` and `T` share one cut vertex directly.

Retain the direct actual `K4+T` anchor.  For every other triangle, open only
its ancestor-minimal unselected triangle at its upstream cut.  Nested
triangles stay in that one complete side.  The resulting sides are connected,
induced, disjoint, and number at most `k-1`.  Each is either a tree of credit
`-1` or a triangular block graph of positive credit.  The retained anchor has
credit greater than three.  If `b` is the number of tree sides, then

```text
b<=k-1,                  sigma(C)>3-b.                   (6)
```

The direct `K4+T` estimate is invoked only after physical adjacency proves the
shared cut.  A triangle behind a bridge was already separated in Section 3.1,
and a triangle behind a nontriangle was already assigned in Section 3.2.

## 5. Exact final ledger

Apply induced superadditivity to the anchor/core pieces and all complete sides.
Every side not counted by `b` or `s` is positive.  The strictness always comes
from the rooted `K4` or direct `K4+T` anchor.

If `k=0`, (2), (3), and (5) give

```text
sigma(G)>2-s>=2-h>=0.                                   (7)
```

If `k>=1`, (3), (4), and (6) give

```text
sigma(G)>3-b-s
        >=3-(k-1)-h
         =4-k-h
        >=0.                                             (8)
```

Both displayed endpoint bounds are strict.  This proves `sigma(G)>0` for all
three profiles in (1).

The formerly rejected four-arm topology is now immediate.  If all four cycles
lie in separate first-bridge away components, the exact worst profile is
`T2+C5+C5`: the two triangle arms are positive, the two pentagon arms have
credit greater than `-1`, and the rooted `K4` has credit greater than two.
Thus the ledger is strictly `>2-1-1=0`.  The sharper exact value for bare
pentagons is `>2-2(sqrt(5)-2)=6-2sqrt(5)>0`, but that refinement is not needed.

## 6. Quotient and expansion invariance

The proof suppresses nothing when deciding ownership.  Arbitrary sizes follow
from the physical block-cut construction.

* **K2-chain expansion.**  Subdividing a bridge replaces one bridge node by a
  chain of bridge nodes and routing cuts.  If the bridge lies on a `K4`-to-cycle
  route and replaces a selected first bridge, its first new edge is selected;
  otherwise all inserted vertices remain with the pre-existing owner.  Every
  later inserted vertex on a selected route remains in the same complete away
  component.
* **Rooted-tree expansion.**  Adding a one-root tree adds rank-zero leaf blocks
  below one existing owner.  Induction on tree edges assigns every new vertex
  to that owner without changing any positive block, first bridge, selected
  nontriangle, or direct anchor.
* **Repeated cuts and nesting.**  A physical cut vertex is retained upstream
  once.  An ancestor-minimal opening takes the complete far side, so a deeper
  demand is not opened a second time merely because it is nested.

These observations cover arbitrary connector lengths, arbitrary finite rooted
payloads, repeated cuts, and unbounded nesting depth.

## 7. Finite corroboration and static implementation replay

The universal theorem is proved in Sections 1--6.  The executable artifact below
is finite corroboration and a static implementation replay; its generated fixtures
do not constitute an exhaustion of arbitrary block-cut trees, cycle lengths, or
rooted payloads.  The artifact is

```text
research/r31-k-adjacency-semantic-verifier.py
```

For each supplied finite simple adjacency it reconstructs Tarjan blocks, the
literal `K4`, the four literal cycle blocks, all physical bridges and ports,
the exact residual profile, the simultaneous first-bridge antichain,
ancestor-minimal nontriangle openings, the direct anchor when present, and all
original-vertex owner sets.  It recomputes connectedness, inducedness,
disjointness, exhaustive union, piece ranks, cactus structure, and the strict
integer ledger.  Its generated suite includes all three profiles, four
independent arms, mixed bridge/shared-cut routes, nesting, repeated cuts, long
connectors, opaque relabeling, and rooted payloads.  Hostile adjacency and
source mutations fail closed, and normal/optimized output must be identical.

The fixed analytic source pins are:

| use | source | SHA-256 |
|---|---|---|
| induced superadditivity | `all-tricyclic-graphs/paper.tex` | `4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02` |
| trees; triangular block graphs; rooted `K4`; direct shared-cut `K4+T` | `packing-two-square-energy/paper.tex` | `9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791` |
| odd-unicyclic lower bound | `all-tricyclic-cacti/paper.tex` | `d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8` |
| connected cactus rank at least two | `all-nonunicyclic-cacti/paper.tex` | `26939326e2ad71062617503e106dbd46d99f3d8fe82a98fca858fd3f2f8323f9` |
| exact `R31-K` residual sieve/classification input (not a standalone full-lane theorem) | `positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md` | `3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5` |

Run

```text
python3 research/r31-k-adjacency-semantic-verifier.py
python3 -O research/r31-k-adjacency-semantic-verifier.py
```

Passing this finite gate corroborates the implementation and replays the stated
contracts on its exact suite; it does not replace the universal proof in Sections
1--6.  Those sections establish the complete physical `R31-K` lane only.  Other
unauthenticated rank-seven hull-bridge packet families and the separate
single-block program remain open.  No global theorem is claimed.
