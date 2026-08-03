# Four multiblock residuals: owner-exact closure

This note does not modify the main manuscript. It closes the four incidence
families isolated by the block-cut terminal reduction, including positive
routes, repeated owners, and nested shared-cut attachments.

Write

`sigma(X)=s^+(X)-|V(X)|`.

We use induced square-energy superadditivity, the fact that every nonempty tree
has credit `-1`, and the following established attached-packet bounds:

1. every connected graph of rank two, three, or four has nonnegative credit;
2. a triangle territory has positive credit and a two-triangle territory has
   credit greater than one;
3. a favorable rank-three triangular packet of packing number at most two has
   credit greater than two;
4. an attached `Theta(1,2,2)+C3` packet has credit greater than two.

All four statements allow arbitrary rooted trees. In (4), the diamond supplies
two intrinsic triangles and the attached triangle shares a cut with it, so it
is also an instance of (3).

## 1. Terminal reduction and ownership audit

Let `B` be the distinguished cyclic block and root the minimal block-cut
subtree containing `B` and the external cyclic blocks at `B`. Deleting the
edges of `B` shows that every component off `B` meets it in at most one vertex.
Thus every external block has a unique first owner in `V(B)`.

If the rooted subtree contains an actual bridge, choose a bridge farthest from
`B`. Its descendant cyclic set is a complete suffix of the rooted subtree, not
a list of independently chosen cycles. In a rank-three-plus-two-triangles row
that suffix has profile `T` or `TT`. In the diamond row it has one of

`T, TT, P, TP, TTP`.

The bridge edge is the only edge between its two vertex sides. Assign each
endpoint, every connector vertex, and every rooted descendant to its own side.
The resulting territories are connected, induced, disjoint, and exhaustive.
For suffix `T` or `TT`, its positive credit and the nonnegative lower-rank
complement close strictly. The same argument closes `TP` and `TTP` by the
established favorable cactus packets. If a diamond-row bridge cuts off only
`P`, that unicyclic territory has credit greater than `-1`, while the retained
`D+T+T` packet has credit greater than three, so this case is strict as well.
Hence every positive-route realization is closed, including separate arms, a
common positive stem, and one cyclic block nested beyond another.

It remains to classify the bridge-free subtree. With two external triangles,
there are exactly two block-level forms:

- **direct/direct:** both triangle block nodes are adjacent to cut nodes of
  `B`; their owners may coincide;
- **direct/nested:** one triangle is adjacent to a cut node of `B`, and the
  second is adjacent to a cut node of the first triangle.

This is exhaustive because a finite tree rooted at `B` has a first external
block on every route, and there are only two external blocks. A cut node of
degree three represents repeated direct ownership; it is not a third form.
In the nested form the owner of the downstream triangle is its physical cut
vertex in the upstream triangle, not a second owner in `B`.

For the structural rows that survive the all-length DNN gate in Section 2, the
legal first-owner sets, after excluding every admissible opening interior, are
the following physical vertex sets:

| distinguished block | legal first owners |
|---|---|
| doubled triangle `111`, canonical doubled pairs, long odd connector | every branch vertex and every internal vertex outside that connector |
| doubled triangle `111`, canonical doubled pairs, direct odd connector | the three branch vertices |
| doubled `C4` `111`, canonical doubled pairs | the four branch vertices and the interiors of the two canonical even doubled paths |
| one-long all-odd `K4` | the four branch vertices |

For direct/direct incidence the exact datum is an ordered pair, with
repetition, from the applicable row. For direct/nested incidence the first
triangle has an owner in that row and the second owner is an arbitrary vertex
of the first triangle. Thus this table and the two block-level forms enumerate
all legal owner data; in particular the doubled-`C4` interior-owner orbit is
not merged with its branch-owner orbit.

When a downstream or second direct triangle `T_2` is opened, its boundary cut
is retained with the upstream territory and `T_2` minus that cut, together
with every branch rooted at its remaining vertices, is one nonempty tree.
Branches rooted at the boundary cut stay upstream. This convention assigns
every shared cut and every rooted vertex exactly once.

## 2. All-length DNN gate for the doubled families

Before using an owner-exact structural opening, dispose of every physical
class-`111` row in which either doubled pair is noncanonical. This is an
all-length statement, not a shortest-row assumption.

For the doubled triangle, Section 3.1, equations (9)--(10), of
`tricyclic-general/doubled-triangle-dnn-cover.md` treats the two ways to
lengthen a member of a doubled pair. Its exact rational upper bounds are

`229/120<2` and `31/20<2`.

Relabeling covers all four members of the two doubled pairs, and fixed-parity
monotonicity covers every further increase by two. Thus every labelled
class-`111` physical row with a noncanonical doubled path has DNN excess
strictly below two. Section 1 of that note, especially its attachment argument
following equation (3), shows that the certificate remains valid after
arbitrary rooted trees are attached.

For the doubled `C4`, Section 5, equations (8)--(9), of
`tricyclic-general/doubled-c4-switching-sieve.md` gives the corresponding two
all-length certificates. The exact rational estimates recorded there are

`1862/1000<2` and `1662/1000<2`.

Again, doubled-pair interchange, member interchange, and kernel automorphisms
cover every one of the eight labelled class-`111` parity rows and either
doubled pair; monotonicity covers all longer physical lengths. Sections 3 and
5 of that note include arbitrary rooted-tree attachments by one-vertex
additivity of `kappa`.

These are also compatible with the two external triangles and with every
block-cut incidence used here. One-vertex additivity applies at each shared
cut; every actual connector and every off-core branch is a tree and contributes
its number of edges to `kappa`. Each external `C3` has excess one. Hence a
rank-three block of excess at most two plus the two triangles has total excess
at most four. Since the whole graph has rank five, `|V(G)|=|E(G)|-4`, and

`s^-(G)<=kappa(G)<=|E(G)|+4`

implies `s^+(G)=2|E(G)|-s^-(G)>=|V(G)|`. Thus all such noncanonical physical
rows are already closed, independently of owners, positive routes, repeated
cuts, nested incidence, connectors, and rooted-tree attachments.

Consequently the doubled-triangle and doubled-`C4` cases entering the
owner-exact structural argument below have, respectively,

`{a,A}={b,B}={1,2}` and `{a,A}={c,C}={1,2}`,

up to the labels used in the two cited notes. Only connector lengths remain
arbitrary subject to class `111`.

## 3. Canonical rank-three block plus two triangles

Let `B` be one of the three canonical structural rank-three blocks and suppose
the incidence is bridge-free. Choose the upstream triangle `T_1` in the
direct/nested form, and choose either triangle in the direct/direct form. Open
the other triangle `T_2` as described above; call the resulting nonempty tree
`S`. Thus

`sigma(S)=-1`.                                                (1)

Now perform the canonical structural opening of `B`. The opened vertex and its
owned rooted branches form one nonempty tree `R`; the two open-path remnants
stay on the retained side as attached trees. Thus

`sigma(R)=-1`.                                                (2)

The residual hypothesis says that neither external triangle is owned by an
admissible opening. Therefore all of `T_1` remains on the retained side. The
retained rank-three anchor `A` is as follows.

### Doubled triangle, class `111`, canonical doubled pairs

If the odd connector has length at least three, opening it leaves the two
canonical intrinsic triangles. The legal owner of `T_1` lies on one of those
triangles, so `T_1` shares a vertex with it. Hence the three-triangle anchor has
packing number at most two and

`sigma(A)>2`.                                                 (3)

If the connector is direct, open the internal vertex of either canonical even
parallel path. The retained bicyclic core is a diamond. Every legal owner is a
retained branch vertex, so adjoining `T_1` gives an attached
`Theta(1,2,2)+C3` anchor and again (3) holds.

### Doubled `C4`, class `111`, canonical doubled pairs

Open the normalized even connector. The retained bicyclic core consists of the
two canonical intrinsic triangles joined by the other connector path. There
are two legal-owner orbits, and they must be treated separately.

- At a branch owner, adjoining `T_1` gives the usual three-triangle favorable
  anchor. Its triangle packing number is at most two, so (3) follows.
- At an internal vertex of either canonical even doubled path, the induced
  cyclic side is not a cactus: the second route through that doubled side makes
  a diamond. With `T_1` retained, the anchor is an attached
  `Theta(1,2,2)+C3` packet. Attached-packet bound 4 above gives
  `sigma(A)>2`, again proving (3).

This also shows quantitatively why the interior-owner orbit is harmless. If a
coarser side allocation leaves `k=0,1,2` of the external triangles with the
diamond, the favorable attached `D+T^k` side has credit respectively greater
than `1,2,3`; the opposite triangular side has credit respectively greater
than `1,0,-1` (the last value is one tree). The side sum is always greater than
two. The proof below uses the sharper `k=1` anchor and opens the other triangle,
so only the middle line is needed. No claim that the interior-owner side is a
cactus is used.

### One-long all-odd `K4`

Open an internal vertex of the unique long path. The retained bicyclic core is
the diamond formed by the other five unit paths. The legal owner of `T_1` is a
retained branch vertex. Thus `A` is an attached diamond plus a triangle and
(3) follows.

In every case `A`, `R`, and `S` are connected induced territories and

`V(G)=V(A) disjoint union V(R) disjoint union V(S)`.

The direct/direct case allows equal owners: the common cut stays in `A`, and
only `T_2` minus that cut enters `S`. In the direct/nested case all of `T_1`,
including the cut leading to `T_2`, stays in `A`. The structural opening puts
only its chosen path vertex and rooted descendants in `R`; its path remnants
stay in `A`, and it cannot capture `T_1` by the residual owner condition.
For a doubled-`C4` interior owner, that owner and both routes forming its
diamond stay wholly in `A`; neither is cut into `R` or `S`.

More explicitly, ownership defines the partition before any credit is used.
The opened structural vertex and its complete descendant set form `R`. The
boundary cut of `T_2` stays in `A`, while the other two vertices of `T_2` and
all descendants owned by them form `S`. Every remaining core vertex, every
structural-path remnant, `T_1`, and every descendant owned there form `A`.
These owner classes are disjoint and exhaustive. Every edge with both ends in
one class is retained, so each territory is induced; the path remnants and
retained boundary cuts make each territory connected. Thus no cut, connector
remnant, interior owner, or rooted branch is duplicated or omitted. Equations
(1)--(3) give

`sigma(G)>=sigma(A)+sigma(R)+sigma(S)>2-1-1=0`.               (4)

This closes all three canonical rank-three rows, for both bridge-free incidence
types and every legal owner. For the two doubled families, "canonical" here
means exactly the doubled-pair equalities displayed at the end of Section 2;
no owner-exact claim is being made for a noncanonical doubled pair.

## 4. Diamond plus two triangles and a pentagon

Let `D=Theta(1,2,2)` with endpoints `x,y`. Positive routes were closed in
Section 1, so suppose the minimal incidence subtree is bridge-free and all
external blocks use the legal diamond owners `x,y`.

If a triangle is directly incident with `D`, retain `D` and that triangle as
an anchor `A`. It is an attached diamond-plus-triangle packet, so
`sigma(A)>2`. Root the rest of the incidence tree at `A`. There are only two
remaining cyclic demands, the other triangle and the pentagon. For each
component at the anchor boundary, retain the boundary cut in `A`.

- A component containing one demand is either that cycle minus its boundary
  cut, a nonempty tree of credit `-1`, or an intact unicyclic territory of
  credit greater than `-1`.
- A component containing both demands occurs only when one lies downstream
  from the other. Opening the boundary cycle leaves a connected territory with
  one intact cycle, so its credit is greater than `-1`; alternatively a later
  cut gives two nonempty trees, of total credit `-2`.

Thus the total boundary loss is at most two, with every boundary cut kept only
by `A`, and the strict anchor margin closes the graph.

Assume finally that no triangle is directly incident with `D`. The first block
after `D` must then be the pentagon `P`. Relative to `P`, the two triangles have
exactly the direct/direct or direct/nested forms of Section 1. Let `T_1` be a
direct triangle (the upstream one in the nested form), and let `u` be the
`D-P` cut and `v` the `P-T_1` cut.

Choose a vertex `z` of `P` distinct from `u`, from `v`, and, in the
direct/direct form, from the owner in `P` of the second triangle. Such a vertex
exists because these are at most three of the five vertices of `P`. Put `z`
and every rooted tree based at `z` in a territory `R`, while retaining the path
`P-z` in the anchor. No cyclic block is owned by `z`, by the choice of `z` and
the present incidence classification. Hence `R` is a nonempty tree. Branches
at all retained cuts stay with the anchor. The induced anchor `A` has exactly
the cyclic blocks `D` and `T_1`, joined by the tree `P-z`, and hence is again
an attached diamond-plus-triangle packet with

`sigma(A)>2`, `sigma(R)=-1`.                                 (5)

Open the other triangle `T_2` at its boundary cut, retaining that cut in `A`.
This produces one further nonempty tree `S`, whether `T_2` is a second direct
child of `P` or is nested beyond `T_1`. All branches rooted away from the cut
go with `S`, so `sigma(S)=-1`. The three territories are induced, disjoint,
and exhaustive. Therefore

`sigma(G)>=sigma(A)+sigma(R)+sigma(S)>2-1-1=0`.               (6)

This closes the genuinely nested `D-P` incidence that cannot be relabelled as
a direct `D+T` attachment.

## 5. Exact residual

The required exhaustion is the following disjunction. In either doubled
class-`111` family, a noncanonical member of a doubled pair is closed by the
all-length DNN gate of Section 2; otherwise both doubled pairs are canonical.
For a canonical doubled family, the one-long all-odd `K4` family, or the
diamond family, an actual positive route is closed by Section 1. If there is
no positive route, Section 1 leaves exactly the listed bridge-free incidence
forms, which Sections 3--4 close owner-exactly. Thus, and only after this
disjunction, the four previously retained multiblock families are exhausted:

| family | bridge-free forms | disposition |
|---|---|---|
| `D+T+T+P` | direct `D-T`, or rooted `D-P` with direct/direct or direct/nested triangles | closed by a `D+T` anchor against at most two trees |
| doubled triangle `111` plus `TT` | noncanonical doubled pair; otherwise canonical direct/direct or direct/nested | all-length DNN; otherwise a rank-three triangular anchor against two trees |
| doubled `C4` `111` plus `TT` | noncanonical doubled pair; otherwise canonical direct/direct or direct/nested | all-length DNN; otherwise a favorable rank-three anchor (triangular or `D+T`) against two trees |
| one-long all-odd `K4` plus `TT` | direct/direct, direct/nested | closed by a diamond-plus-triangle anchor against two trees |

Consequently the multiblock residual is empty: its noncanonical doubled rows
are DNN-closed, and every row left for owner-exact closure is canonical and is
closed above. Together with the existing DNN and induced-territory rows, all
positive block-rank partitions of five with at least two cyclic blocks are
closed. The only remaining part of the pentacyclic program, if any, lies in the
separate single rank-five block classification; no multiblock incidence,
connector, or rooted-tree case remains.
