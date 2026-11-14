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

Whenever the rooted cyclic hull contains an actual bridge having a triangle
on its descendant side, choose such a bridge farthest from `B`.  Its descendant
cyclic set is a complete suffix of the rooted subtree, not a list of
independently chosen cycles.  In a rank-three-plus-two-triangles row the suffix
has profile `T` or `TT`; in the diamond row it has profile `T`, `TT`, `TP`, or
`TTP`.

The selected bridge edge is the only edge between its two vertex sides. Assign
each endpoint, every connector vertex, and every rooted descendant to its own
side.  The resulting territories are connected, induced, disjoint, and
exhaustive.  For suffix `T` or `TT`, its positive credit and the nonnegative
lower-rank complement close strictly.  The same argument closes `TP` and `TTP`
by the established favorable cactus packets.

Only if no bridge anywhere in the diamond-row cyclic hull has a triangle on
its descendant side do we inspect a bridge whose descendant cyclic suffix is
only `P`.  Cut off that complete pentagonal territory, whose credit is greater
than `-1`.  The complementary cyclic hull contains exactly `D+T+T`.  If that
hull still had a bridge between cyclic blocks, then, when rooted at `D`, its
descendant side would contain one of the two triangles.  It would therefore
have been a triangle-descendant bridge in the original hull, contrary to the
explicit global absence hypothesis.  Hence the retained `D+T+T` cyclic hull is
bridge-free.  Only with this bridge-free conclusion do we invoke the exact
shared-cut packet, which has credit greater than three.  If there is no cyclic
bridge at all, the bridge-free owner analysis below applies instead.

Thus every route containing a bridge between cyclic blocks is closed,
including separate arms, a common positive stem, and one cyclic block nested
beyond another.  Bridges belonging only to off-core rooted trees remain inside
the corresponding packet and are handled by its arbitrary one-root-tree scope;
they are not ``positive routes'' in this cyclic-hull reduction.

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
| doubled triangle `111`, first-simple doubled pairs, long odd connector | every branch vertex and every internal vertex outside that connector |
| doubled triangle `111`, first-simple doubled pairs, direct odd connector | the three branch vertices |
| exceptional doubled `C4` orbit, first-simple doubled pairs | the four branch vertices and the interiors of the two even doubled members transported from the normalized anchor |
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

Before using an owner-exact structural opening, dispose of every doubled-
triangle class-`111` row, or exceptional doubled-`C4`-orbit row, in which a
member of either doubled pair is longer than first-simple. This is an all-
length statement, not a shortest-row assumption and not a claim that the
exceptional doubled-`C4` orbit is one switching class.

For the doubled triangle, Section 3.1, equations (9)--(10), of
`tricyclic-general/doubled-triangle-dnn-cover.md` treats the two ways to
lengthen a member of a doubled pair. Its exact rational upper bounds are

`229/120<2` and `31/20<2`.

Relabeling covers all four members of the two doubled pairs, and fixed-parity
monotonicity covers every further increase by two. Thus every labelled doubled-
triangle class-`111` physical row with a longer-than-first-simple doubled path
has DNN excess strictly below two. Section 1 of that note, especially its
attachment argument following equation (3), shows that the certificate remains
valid after arbitrary rooted trees are attached.

For the doubled `C4`, Section 6, equations (8)--(9), of
`tricyclic-general/doubled-c4-switching-sieve.md` gives the corresponding two
all-length certificates. The exact rational estimates recorded there are

`1862/1000<2` and `1662/1000<2`.

The exceptional set consists of eight parity anchors in one genuine kernel-
automorphism orbit: four are in switching class `110` and four in class `111`.
Doubled-pair interchange, compatible member interchange, and the sixteen
induced incidence automorphisms transport the two certificates to either
doubled pair of every anchor; no switching operation is used. Fixed-parity
monotonicity covers every further physical length increase. Sections 3 and 6
of the cited note include arbitrary rooted-tree attachments by one-vertex
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
arbitrary. The doubled triangle remains in class `111`; the doubled-`C4`
connectors have fixed opposite parities in the exceptional eight-anchor orbit.

## 3. First-simple structural rank-three block plus two triangles

Let `B` be one of the three structural rank-three blocks left after the DNN
gate and suppose
the incidence is bridge-free. Choose the upstream triangle `T_1` in the
direct/nested form, and choose either triangle in the direct/direct form. Open
the other triangle `T_2` as described above; call the resulting nonempty tree
`S`. Thus

`sigma(S)=-1`.                                                (1)

Now perform the prescribed physical structural opening of `B`. The opened vertex and its
owned rooted branches form one nonempty tree `R`; the two open-path remnants
stay on the retained side as attached trees. Thus

`sigma(R)=-1`.                                                (2)

The residual hypothesis says that neither external triangle is owned by an
admissible opening. Therefore all of `T_1` remains on the retained side. The
retained rank-three anchor `A` is as follows.

### Doubled triangle, class `111`, first-simple doubled pairs

If the odd connector has length at least three, opening it leaves the two
first-simple intrinsic triangles. The legal owner of `T_1` lies on one of those
triangles, so `T_1` shares a vertex with it. Hence the three-triangle anchor has
packing number at most two and

`sigma(A)>2`.                                                 (3)

If the connector is direct, open the internal vertex of either first-simple even
parallel path. The retained bicyclic core is a diamond. Every legal owner is a
retained branch vertex, so adjoining `T_1` gives an attached
`Theta(1,2,2)+C3` anchor and again (3) holds.

### Exceptional doubled-`C4` orbit, first-simple doubled pairs

Transport the physical packet by a genuine kernel automorphism to the
normalized anchor `010011`, and open its even connector. The retained bicyclic
core consists of the two first-simple intrinsic triangles joined by the other
connector path. There
are two legal-owner orbits, and they must be treated separately.

- At a branch owner, adjoining `T_1` gives the usual three-triangle favorable
  anchor. Its triangle packing number is at most two, so (3) follows.
- At an internal vertex of either even doubled member, the induced
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

This closes all three first-simple structural rank-three families, for both
bridge-free incidence types and every legal owner. For the exceptional doubled-
`C4` orbit, a genuine graph isomorphism transports the even-connector opening,
the legal-owner set, direct/direct and direct/nested incidence, repeated cuts,
rooted branches, and all three induced territories from the normalized anchor
to each of the other seven anchors. Four anchors lie in switching class `110`
and four in class `111`; switching is never used. For both doubled families,
"first-simple" means exactly the doubled-pair equalities displayed at the end
of Section 2; no owner-exact claim is made for a longer doubled member.

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
after `D` must then be the pentagon `P`; equivalently, `P` is an internal block
of the minimal subtree on `D,T_1,T_2`.  Delete all five edges of `P`, retaining
its vertices.  For each `v in V(P)`, let `F_v` be the component of `G-E(P)`
containing `v`.  Every component meets `P`: stop a shortest route to `P` at its
first pentagon vertex.  No component meets two distinct pentagon vertices,
because a path between them with no internal pentagon vertex would be an ear
that enlarges the 2-connected block `P`.  Thus the five `F_v` are well-defined,
disjoint, exhaustive owner components.

Mark `v` when `F_v` contains one of `D,T_1,T_2`.  Several cyclic blocks at the
same physical cut, or nested beyond it, give one mark.  List the distinct marks
in cyclic order as `c_0,...,c_(q-1)`, with `F_(c_0)` containing `D`.  Let `k`
be the number of triangles in `F_(c_0)`, and for `i>0` let `r_i>=1` be the
number in `F_(c_i)`.  Then

`k+sum_(i=1)^(q-1) r_i=2`.                                   (5)

Because `P` lies between `D` and at least one triangle in the minimal cyclic
hull, deleting the block node `P` separates their block nodes.  Hence `q>=2`;
obviously `q<=3` and `0<=k<=1`.  The excluded value `q=1` would put all three
cyclic blocks in one component of `G-E(P)`, contradicting that `P` is the first
external block on this minimal hull.

Choose one pentagon edge in every cyclic arc from `c_i` to `c_(i+1)` and cut
those `q` edges.  The remaining pentagon vertices form `q` nonempty consecutive
path intervals `I_i`, each containing exactly one mark.  Put

`W_i=union_(v in I_i) V(F_v),       A_i=G[W_i]`.              (6)

These territories are connected, induced, disjoint, and exhaustive.  Indeed,
each `F_v` is connected and contains its owner; the internal pentagon edges of
`I_i` connect them; an edge outside `E(P)` cannot join two owner components;
and the only cross-sector edges are the selected pentagon boundary edges.
Every unmarked pentagon vertex, every pentagon cut, and every acyclic branch
therefore belongs to exactly one interval sector.  Each cyclic block remains
whole in the sector of its owner, including repeated-owner and nested cases.

The minimal hull on the displayed cyclic blocks is bridge-free here, because
routes containing a bridge between cyclic blocks were disposed of in Section
1.  Therefore each sector's cyclic owner component is one shared-cut incidence
subtree.  The path interval based at its mark and every component based at an
unmarked interval vertex form a forest attached to that cyclic packet at
individual roots.  A component outside the displayed cyclic packet cannot
meet two of its core vertices: its block-cut path would then furnish a second
route and place those vertices in a larger positive-rank block.  Hence the
remaining material is genuinely a collection of one-root branches.  The `D`
sector is thus a narrow bridge-free shared-cut `D+T^k` packet with arbitrary
one-root branches, not a packet joined through a multi-interface path.  The
weighted diamond phase gives `sigma(A_0)>1` for `k=0` and the exact shared-cut
`D+T` one-sum phase gives `sigma(A_0)>2` for `k=1`; equivalently

`sigma(A_0)>1+k`.                                             (7)

Every other sector is a shared-cut cluster of `r_i` triangles.  Its weighted
Sachs polynomial is strictly lower-half-plane, so
`sigma(A_i)>r_i-1`.  Set `h=q-1`; this is the number of non-`D` cyclic owner
marks, not a count of empty sectors.  There are no tree-sector charges.  By
induced square-energy superadditivity and (5)--(7),

`sigma(G)>=sum_(i=0)^h sigma(A_i)`

`        >(1+k)+sum_(i=1)^h(r_i-1)=3-h=4-q>=1>0`.             (8)

This owner-sector partition closes the rooted `D-P` incidence without the
invalid assertion that the multi-interface path `P-z` is a one-root attachment.

## 5. Exact residual

The required exhaustion is the following disjunction. In the doubled-triangle
class-`111` family or the exceptional doubled-`C4` orbit, a longer-than-first-
simple member of a doubled pair is closed by the all-length DNN gate of
Section 2; otherwise both doubled pairs are first-simple. For a first-simple
doubled family, the one-long all-odd `K4` family, or the
diamond family, an actual positive route is closed by Section 1. If there is
no positive route, Section 1 leaves exactly the listed bridge-free incidence
forms, which Sections 3--4 close owner-exactly. Thus, and only after this
disjunction, the four previously retained multiblock families are exhausted:

| family | bridge-free forms | disposition |
|---|---|---|
| `D+T+T+P` | direct `D-T`, or rooted `D-P` with direct/direct or direct/nested triangles | direct anchor when available; otherwise the exact pentagon owner-sector partition |
| doubled triangle `111` plus `TT` | longer doubled member; otherwise first-simple direct/direct or direct/nested | all-length DNN; otherwise a rank-three triangular anchor against two trees |
| exceptional doubled `C4` orbit plus `TT` | longer doubled member; otherwise first-simple direct/direct or direct/nested, connectors arbitrary in fixed opposite parities | all-length DNN; otherwise the transported favorable rank-three anchor (triangular or `D+T`) against two trees |
| one-long all-odd `K4` plus `TT` | direct/direct, direct/nested | closed by a diamond-plus-triangle anchor against two trees |

Consequently the multiblock residual is empty: its longer-doubled-member rows
are DNN-closed, and every row left for owner-exact closure has first-simple
doubled pairs and is closed above. Together with the existing DNN and induced-territory rows, all
positive block-rank partitions of five with at least two cyclic blocks are
closed. The only remaining part of the pentacyclic program, if any, lies in the
separate single rank-five block classification; no multiblock incidence,
connector, or rooted-tree case remains.
