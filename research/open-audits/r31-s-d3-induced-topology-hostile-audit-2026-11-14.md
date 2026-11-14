# OPEN hostile audit and candidate repair: the `R31-S:D3` topology is not physical

## Referee verdict

**FAIL for the inherited `D3` topology; PASS for the conditional physical split;
BLOCK for promotion as an `R31-S` closure.**

The committed finite transport correctly enumerates and transports 110 rooted
three-triangle incidence records. It does **not** reconstruct either induced
component before calling 28 records `D3`. Exact physical reconstruction shows:

* every transported occurrence is split into two induced triangular cacti;
* on the canonical oriented base split, the 110 actual rank pairs are
  `(1,4):28`, `(2,3):27`, `(3,2):27`, and `(4,1):28`; thus there is no forced
  `4+1` profile across all records (the 54 balanced records are `27+27` between
  the two orientations), while the unordered totals are `(2,3):54` and
  `(1,4):56`;
* every side's actual triangle-intersection graph is connected, so each side is
  one shared-cut cluster rather than merely a connected cactus;
* every old `D3` rank-four side has four actual `K_3` blocks and no diamond
  block; and
* the `z,Az,Bz` in the D3 diagnostic have no physical preimage.

Thus the old implication

```text
one-sided + an interior doubled-member owner  ==>  diamond plus three triangles
```

is semantic laundering. The interior of the unique even two-edge member,
together with the parallel odd one-edge member, is just the third vertex of an
actual triangle. It does not create a second two-edge route.

The exact split supports a **conditional** bypass for all 110 records. If its
two side ranks are `r_0,r_1`, then `r_i>=1` and `r_0+r_1=5`. The rooted
shared-cut estimates give `sigma(U_i)>r_i-1` for `r_i<=3`; every physical
rank-four side is separately checked to have exactly four triangle blocks in
one connected shared-cut cluster, so the existing marked four-triangle theorem
gives `sigma(U_i)>3`. Hence the side sum is strictly greater than three.

Promotion is blocked because the audit checker begins from the already retained
three-triangle incidence model and **models** the complete structural owner
class `T` as a tree; it does not derive that class from the full upstream graph.
The separately boundary-opened external-leaf territory `S` is not present in the
110-record graph at all: the checker imports it only from frontier prose. The
committed owner rules say how a known territory is assigned, but no pinned
upstream executable reconstructs the full `R31-S` graph and proves that both
`S` and `T` are distinct nonempty induced trees for every source row. Therefore
the two-debit calculation below is valid only under those two owner antecedents:

```text
sigma(H) >= sigma(U_0)+sigma(U_1)+sigma(T) > 3-1 = 2,
sigma(G) >= sigma(H)+sigma(S)                   > 2-1 = 1 > 0.
```

This is enough to close the frontier target `sigma(H)>1` and the parent target
`sigma(G)>0` **if and only if** the upstream owner antecedents are supplied.
This file and its checker are OPEN artifacts only; they do not change a theorem,
master verifier, state ledger, or publication.

## 1. Pinned source boundary

The audit pins these committed bytes (all at base commit
`72b978271828`):

| source | SHA-256 |
|---|---|
| `research/r31-s-doubled-c4-marked-cut-verifier.py` | `b14e7544bd8f5298fd425c68228e5fb4f5c49071dd3a7ec773ee5de610630c71` |
| `research/r31-s-d3-diamond-packet-verifier.py` | `f0b799d5fc7734749335bb6b344c58357bab69668b0dae40c5149146c66e9993` |
| `research/r31-s-c4-marked-four-triangle-verifier.py` | `d405f644467ab59e615a4cf6fdf5ada1a3ba8c21eadcd1ee7035b3fa37d159e0` |
| `packing-two-square-energy/paper.tex` | `9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791` |
| `positive-square-energy/heptacyclic-general/r31-s-c4-marked-four-triangle-theorem.md` | `78344337226ae5c5b42645dd563390eec9eb462824e78fd4e42d7fa54051309d` |
| `positive-square-energy/heptacyclic-general/r31-s-doubled-c4-three-triangle-frontier.md` | `ef6f646a0a4416a161dae588940c271a73104c6e86a243baba22928234a082d6` |
| `positive-square-energy/heptacyclic-general/complete-multiblock-theorem.md` | `f7a3e009b9b617b0ea5f245702e7e93d2f74116ef7d388d65222069cb06ac347` |
| `positive-square-energy/heptacyclic-general/nested-induced-piece-packet-theorem.md` | `79b44180ff2d3ca44b5537e2913709fa6c2334b2e475990b34508475592a000b` |
| `research/fixtures/heptacyclic-multiblock-owner-ledger.json` | `0630cd96fd341b9017b31d6a36341cfead0c6bca64517c1073797ffc14747f42` |
| `positive-square-energy/pentacyclic-general/four-residual-owner-exact-closure.md` | `b182d37b472808cc2c000e61958471bc6c998ade17e02ec8ea14f7329653cd46` |


The transport verifier itself warns that it authenticates only finite transport,
not analytic topology or packet inequalities
(`r31-s-doubled-c4-marked-cut-verifier.py:2-16`). Its classification function
looks only at top-root side labels and whether one is an interior label
(lines 354-413). It never constructs a physical graph, deletes the opening
territory, cuts a connector edge, computes connected components, or identifies
biconnected blocks.

By contrast, the D3 diagnostic starts from

```python
vertices = {"A", "B", "x", "z"}
edges = {AB, Ax, Bx, Az, Bz}
```

(`research/r31-s-d3-diamond-packet-verifier.py:62-67`). This is a newly
constructed `K_4-e`, not a component recovered from the physical split.

## 2. Exact physical graph and vertex partition

### 2.1 Paths and owners

For an anchor row `q`, let the six suppressed paths be `P_e`, in committed
order

```text
a,A,b,c,C,d
```

with endpoints

```text
01,01,12,23,23,30.
```

The doubled fibres are `{a,A}` and `{c,C}` and the connectors are `{b,d}`
(`r31-s-doubled-c4-marked-cut-verifier.py:38-55`). First-simple scope applies
to the **four doubled members**: in each fibre the even member has length two
and the odd member has length one. Connector paths may have arbitrary positive
lengths of their fixed opposite parities; this distinction is explicit in the
frontier at lines 79-95 and in the earlier retained packet at
`positive-square-energy/pentacyclic-general/doubled-c4-111-two-triangles-retained-packet.md:112-132,207-225`.

Write

```text
P_e=(p_e(0),p_e(1),...,p_e(L_e)),
```

where the endpoints are branch vertices and all internal path vertices are
physical vertices. The six legal top owners are the four branch vertices and
the interiors `x,y` of the two even doubled members. A direct triangle meets
its owner in one actual cut vertex. In a chain or fork, a child triangle meets a
fresh vertex of its parent triangle. No attachment adds a second edge or route
between two older vertices.

### 2.2 Opening and cut

Let `e_o` be the even connector and choose an arbitrary internal opening vertex

```text
v=p_eo(j),       1 <= j < L_eo.
```

For the conditional split model, let `T` be `v` plus its complete rooted owner
class and assume that class contains only tree descendants. Under this
antecedent `H[T]` is a nonempty induced tree and

```text
σ(T)=-1.
```

Let `e_c` be the odd connector and choose an arbitrary actual edge

```text
f=p_ec(k)p_ec(k+1),       0 <= k < L_ec.
```

Delete `T`, and remove `f` only to determine the two connected sectors. Denote
their vertex sets by `U_0,U_1`. The induced pieces used in superadditivity are
`H[T]`, `H[U_0]`, and `H[U_1]`; deleting cross edges is not an edge-monotonicity
claim.

Within this conditional model, the checker verifies the exact identities

```text
V(H) = T disjoint-union U_0 disjoint-union U_1,
E_cross = {the two opening-boundary edges} union {f}.
```

Every physical owner and its entire two-edge witness tree occur in exactly one
of these three sets. Each top triangle and all nested descendants follow its
unique first owner. Consequently no cut vertex, descendant, connector vertex,
or remnant is copied or omitted.

### 2.3 Arbitrary connector-remnant lemma—not a bounded experiment

Deleting `v` leaves two endpoint remnants with edge lengths

```text
a=j-1,  b=L_eo-j-1.
```

Since `L_eo` is even, `a+b=L_eo-2` is even, so `a,b` have the same parity.
Each remnant is a path meeting the rest of its endpoint sector in exactly one
root. It has no edge to the other sector: its only former continuation was
through deleted `v`. It therefore is a one-root tree, cannot meet two cyclic
cores, and cannot change any biconnected cyclic block or cyclomatic rank.

Cutting `f` leaves odd-connector remnants of edge lengths

```text
c=k,  d=L_ec-k-1.
```

Since `L_ec` is odd, `c+d=L_ec-1` is even and again `c,d` have the same parity.
Each is a one-root endpoint path. The only edge between them was the actual
cut edge `f`; it is a cross edge and is absent from both induced sector edge
sets. Every descendant rooted at any remnant vertex remains in that remnant's
unique sector.

This proves arbitrary-length and arbitrary-position scope directly. The five
pairs

```text
(0,0), (0,2), (2,0), (1,1), (2,2)
```

are merely canonical representatives of the exhaustive cases “both empty,”
“only left nonempty even,” “only right nonempty even,” and “both positive of
common odd/even parity.” The checker realizes all 25 open/cut combinations to
hostile-test the invariant, but the scope proof is the preceding path lemma,
not finite sampling or an unsupported claim of spectral subdivision
invariance.

## 3. Why each intrinsic side is exactly one triangle

Fix one doubled fibre with branch endpoints `A,B`. Its first-simple physical
members are:

```text
odd member:   A--B,
even member:  A--x--B.
```

Their union has exactly the edges

```text
AB, Ax, xB,
```

hence exactly the triangle `ABx`. A diamond `Theta(1,2,2)=K_4-e` would require
another physical vertex `z` and another route `A--z--B`. There is no such
member: the fibre has lengths `{1,2}`, not `{2,2}`. Opening one connector and
cutting the other only removes a vertex/edges outside the fibre; it cannot
create `z,Az,Bz`.

Tarjan edge-block regeneration in the checker is fail-closed: each side's
cyclic biconnected blocks must equal its registered actual triangle edge sets
exactly. Every other block must be a single bridge. Thus a hidden diamond,
extra cycle, omitted cycle, or bridge-separated “cluster” is rejected.

## 4. Concrete byte-level counterexample

Use base anchor `010011`, whose first-simple vector is

```text
(a,A,b,c,C,d)=(2,1,2,2,1,1).
```

Take the old-D3 record

```text
direct3(x,x,x).
```

Name the branch vertices `A=0,B=1,C=2,D=3`. Let `x=p_a(1)` and
y=`p_c(1)`. Open the unique internal vertex `w=p_b(1)` and cut the actual
edge `d=DA`. Attach the three external triangles at `x`, with private vertices
`u_i,v_i`.

The rank-four side has the exact cyclic-hull edge set

```text
AB, Ax, Bx,
xu_1, u_1v_1, v_1x,
xu_2, u_2v_2, v_2x,
xu_3, u_3v_3, v_3x.
```

Its exact simple cycles/cyclic blocks are

```text
(A,B,x), (x,u_1,v_1), (x,u_2,v_2), (x,u_3,v_3).
```

Their intersection graph is the star `K_1,3`, with actual shared cut `x` on
each star edge. The opposite rank-one side has exact cyclic-hull edges

```text
CD, Cy, Dy
```

and exact cycle `(C,D,y)`. The opened territory contains `w` and its rooted
tree descendants. There is no physical `z` on either side.

This is not just one counterexample. Across the 1,760 first-simple transported
occurrences, the checker finds zero diamond blocks. Across the stronger 44,000
parametric remnant realizations it again finds zero.

## 5. Exact exhaustive reconstruction

Run from repository root:

```text
python3 research/open-audits/r31-s-d3-induced-topology-hostile-audit.py
python3 -O research/open-audits/r31-s-d3-induced-topology-hostile-audit.py
```

The checker independently regenerates the 110 records rather than trusting the
imported set, then requires exact equality. It realizes every one of

```text
8 anchors * 2 genuine witnesses * 110 records * 25 remnant classes = 44,000
```

splits. For each split it:

1. transports exact path orientation and cut/open roles;
2. constructs every physical path and attachment triangle;
3. adds a nontrivial rooted tree at every physical vertex as an ownership
   witness;
4. removes the complete opening-owner territory;
5. cuts one actual odd-connector edge and computes actual connected components;
6. checks the induced, disjoint, exhaustive vertex partition and exact cross
   edges;
7. checks every owner class and nested descendant is wholly in one territory;
8. regenerates biconnected edge blocks and requires exact triangular cyclic
   blocks plus bridges only;
9. checks triangle-intersection connectedness, not merely graph connectedness;
10. checks exact component ranks and exact external-triangle ownership.

The exact result is. First, the canonical oriented 110-record ledger is:

| oriented actual ranks `(r_0,r_1)` | records |
|---|---:|
| `(1,4)` | 28 |
| `(2,3)` | 27 |
| `(3,2)` | 27 |
| `(4,1)` | 28 |

Thus rank `3+2` and `2+3` genuinely occur; only the 56 records historically
called one-sided have unordered rank pair `(1,4)`. Across all transported
witness/remnant probes:

| inherited label | base records | first-simple transports | all 25 remnant classes | unordered actual ranks | actual topology |
|---|---:|---:|---:|---:|---|
| `balanced` | 54 | 864 | 21,600 | `(2,3)` | two shared-cut triangular clusters |
| `C4` | 28 | 448 | 11,200 | `(1,4)` | two shared-cut triangular clusters |
| `D3` | 28 | 448 | 11,200 | `(1,4)` | two shared-cut triangular clusters; **zero diamonds** |

The former-D3 remnant-class totals cover every decorated shape:

| shape | base D3 records | audited occurrences |
|---|---:|---:|
| `direct3` | 12 | 4,800 |
| `chain2+direct` | 10 | 4,000 |
| `fork` | 4 | 1,600 |
| `chain3` | 2 | 800 |

The counts include repeated owners, same/split fork occupancy, and nested
chains. The two genuine witnesses at each anchor separately cover global
side-preserving and side-swapping transport.

## 6. Shared-cut theorem scope, conservatively stated

The checker does not infer the needed analytic estimate from “cactus” alone.
For every side it proves:

* every cyclic biconnected block is an actual triangle;
* any two such blocks meet in at most one actual vertex;
* the graph on actual triangle blocks, adjacent exactly when they share an
  actual cut vertex, is connected; and
* every noncyclic biconnected block is one bridge.

Therefore each side's cyclic blocks form one **bridge-free shared-cut cluster**.
Connector remnants and rooted attachments occur only as one-root trees; they
do not mediate an edge of the triangle-intersection graph.

For ranks `1,2,3`, the rooted shared-cut estimate quoted and proved in
`positive-square-energy/pentacyclic-general/doubled-c4-111-two-triangles-retained-packet.md:32-60`
gives

```text
σ(U_i)>r_i-1.
```

For rank four, the statement in
`r31-s-c4-marked-four-triangle-theorem.md:7-16` applies to a cactus side with
four triangle blocks in one shared-cut cluster, allowing arbitrary acyclic
connector remnants and arbitrary finite attached trees. The checker proves
those statement-level hypotheses for **every** physical rank-four side,
including all interior-owner, repeated, fork, and nested shapes. This use does
not rely on the old verifier's narrower branch-owner record generation.

Hostile caveat: the theorem prose at lines 14-16 correctly excludes four
cyclic blocks separated by bridges, while line 65's phrase “regardless of
bridge subdivisions” is potentially ambiguous. Here no cyclic blocks are
joined only through a bridge: actual triangle-intersection connectedness is
checked. Bridge paths occur only as attached one-root forest material.

## 7. Exact graph hierarchy and conditional two-debit ledger

The intended hierarchy has two openings:

```text
G = full parent R31-S graph,
S = territory of one boundary-opened external triangle leaf,
H = G-S = doubled-C4 block plus three retained external triangles,
T = territory of the later internal even-connector opening,
U_0,U_1 = sectors after deleting T and cutting one odd-connector edge.
```

The intended vertex equations and tree antecedents are

```text
V(G)=V(S) disjoint-union V(H),       sigma(S)=-1,
V(H)=V(T) disjoint-union V(U_0) disjoint-union V(U_1),  sigma(T)=-1.
```

These claims have unequal evidential status. Frontier lines 5--11 **state** the
first opening and `sigma(S)=-1`; the 110-record transport starts only after that
opening and cannot regenerate `S`. The audit checker constructs the three-
triangle model for `H`, then attaches synthetic two-edge owner-witness trees at
every modeled vertex; it proves the second equality and `T`'s tree status for
that model. That is a fail-closed test of the split mechanics, not a derivation
that the actual upstream owner class of the chosen connector vertex has no
external cyclic descendant. The general rules at
`complete-multiblock-theorem.md:33-43` and the owner-ledger string
`rooted_descendants=follow-unique-first-owner` prescribe assignment after an
owner class is known; they do not enumerate the full parent vertices or prove
acyclicity of these two particular classes.

Conditioned on those upstream antecedents, the checker proves for all 44,000
modeled splits

```text
beta(H)=6,
beta(U_0)+beta(U_1)=5,
r_0,r_1>=1,
(r_0,r_1) in {(1,4),(2,3),(3,2),(4,1)}.
```

Each sector has one connected shared-cut cluster of exactly `r_i` triangles and
only attached forest material. The proved bounds therefore give

```text
sigma(U_0)+sigma(U_1)
  > (r_0-1)+(r_1-1)
  = r_0+r_1-2
  = 3.
```

The exact conditional ledger is

```text
sigma(H) >= sigma(U_0)+sigma(U_1)+sigma(T) > 3-1 = 2 > 1,
sigma(G) >= sigma(H)+sigma(S)                   > 2-1 = 1 > 0.
```

The strict endpoint is `sigma(G)>1`; `>0` is merely the target. No territory is
charged twice in this notation. But the audit must remain **BLOCKED for
closure** until an upstream owner-exact reconstruction proves that `S` and `T`
are the actual, distinct, induced, nonempty tree territories represented by
this hierarchy. Merely asserting the generic owner convention is insufficient.

## 8. Hostile tests and residual caveats

The checker rejects at least these semantic mutations:

1. reinsert `z,Az,Bz` and attempt to register only the physical triangle;
2. connect two triangles only by a bridge and call them one shared-cut cluster;
3. use opposite-parity remnant lengths;
4. use a negative remnant length; or
5. omit one actual triangle from the cyclic-block registry.

The audit does **not** claim that arbitrary lengthening of a doubled member
stays in this structural theorem. That is outside the first-simple doubled-
member scope and is already routed through the exact DNN bounds
`1862/1000<2` or `1662/1000<2` in the committed frontier. Only the two
connector paths have arbitrary same-parity lengths here.

The same false “interior owner creates a diamond” sentence appears in
`positive-square-energy/pentacyclic-general/doubled-c4-111-two-triangles-retained-packet.md:145-149,175-187`.
The physical argument above indicates a conservative downstream repair: after
the analogous split, the two sides are triangular cacti of ranks summing four,
so their credits total `>2`, and the opened tree leaves `>1`. That file and all
dependent consumers should be audited before any publication claim changes.
This OPEN artifact does not itself promote that repair.

## 9. Candidate patch surface (do not apply blindly)

After independent replay, an authoritative repair should:

1. replace `D3` as a physical topology with a historical/abstract label only;
2. delete every claim that an interior first-simple doubled-member owner creates
   `Theta(1,2,2)`;
3. replace the C4/D3 one-sided split with the exact uniform rank-pair/shared-cut
   partition above;
4. keep the exact two-debit `G,S,H,T,U_0,U_1` hierarchy explicit;
5. extend a fail-closed upstream verifier to reconstruct the full parent graph,
   derive both actual owner territories as distinct induced trees, and own
   `R31-S` only after normal/optimized replay; and
6. audit the inherited pentacyclic and downstream hexacyclic consumers before
   changing master status.

**Firm referee conclusion:** the D3 packet is not merely analytically
unfinished; it is the wrong graph. The physical coupled-cactus topology passes
for all 110 modeled retained records, including genuine `3+2/2+3` profiles, but
`R31-S` closure remains **BLOCKED**: both tree-territory antecedents must be
derived from the actual upstream graph rather than imported or synthetically
modeled.
