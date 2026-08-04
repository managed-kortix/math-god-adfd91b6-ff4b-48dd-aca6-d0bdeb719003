# Hexacyclic multiblock items 5--7: owner-exact closure

This note proves five owner-exact packet templates used after the exact
rank-six pre-sieve and direct DNN gates:

5. an actual attached `K4` plus three exceptional cycles;
6. a structural rank-four block `S_4` plus two exceptional cycles;
7. an all-odd `K5-e` state in its favorable-theta structural class, plus the
   surviving triangle;
8. a kernel-22 attached-`K4` structural state plus an arbitrary cycle;
9. a kernel-71 triangle-plus-attached-`K4` structural state plus an arbitrary
   cycle.

Write `T=C3` and

`sigma(X)=s^+(X)-|V(X)|`.

In item 5, "exceptional" means that the three cycle excesses have sum greater
than two. In items 6 and 7 the triangle is supplied by the exact nontriangle
DNN gates in the combined ledger, not by an assumed seven-family exhaustion.
Items 8 and 9 permit every cycle length. The conclusion is `sigma(G)>0`
throughout the five packet templates.

## 1. Inputs and ownership

We use induced square-energy superadditivity and the following established
attachment-uniform packets.

1. Every connected graph of cyclomatic rank two through five has nonnegative
   credit.
2. A nonempty tree has credit `-1`; an intact unicyclic territory has credit
   greater than `-1`; a triangular territory has positive credit.
3. An attached actual `K4` has credit greater than two. An actual `K4` and a
   triangle in one bridge-free shared-cut incidence packet have credit greater
   than three.
4. A favorable rank-three triangular packet has credit greater than two. With
   one further triangle in the same shared-cut cluster it has credit greater
   than three. This includes both possible retained packets in a structural
   rank-four opening: actual `K4+T`, and a four-triangle packet.
5. The favorable theta retained by a structural all-odd-`K5-e` deletion has
   credit greater than one. After adjoining a triangle at any vertex as its
   shared cut, with arbitrary rooted trees, the resulting packet has credit
   greater than two. This is Theorem 1 of
   `hexacyclic-general/favorable-theta-triangle-shared-cut-packet.md`.

The shared `K4+T` assertion in (3) is the grouped rooted Sachs packet: its four
units of cyclic rank have favorable phase, so `sigma>3`. It does not assert
that the same margin survives an arbitrary positive connector; such connectors
are cut first below. Arbitrary rooted trees are allowed. The four-triangle
assertion in (4) includes the packing-three central-triangle/three-petal
incidence.

Fix a distinguished cyclic block `B`. After deleting its edges, every
remaining component meets `B` in at most one vertex. Its first vertex in `B`
is its unique owner. If a structural path vertex is opened, that vertex and
all descendants owned there travel together. Both path remnants stay on the
retained side. If a boundary cycle is opened, its boundary cut stays upstream
and the cycle minus that cut, with every descendant rooted away from the cut,
travels downstream.

This defines the vertex partition before credit is charged. Shared cuts are
never copied, and connector remnants and rooted branches follow exactly one
owner.

## 2. Two terminal principles

Root the minimal block-cut subtree containing the distinguished block and all
external cyclic blocks at the distinguished block.

**Terminal-allocation principle.** Suppose one distinguished external demand
is a triangle and there are at most two other demands. Cut actual bridges and
boundary-open cycles successively from the root. Keep the first territory that
contains the triangle intact after opening only its upstream boundary; it is a
triangular territory, possibly with acyclic remnants of boundary cycles, and
has positive credit. Assign each other demand at its first boundary, either as
an intact positive-rank territory or as one cycle-minus-cut tree. Each such
demand costs at most one unit. If two demands are nested, keep their complete
side together when it has rank at least two instead of opening the intermediate
cut twice. Thus a triangle plus two other demands has total credit greater than
`-2`, and a triangle plus one other demand has total credit greater than `-1`.

**Shared-cut principle.** If no actual bridge remains in the minimal subtree,
all relevant blocks form one block-cut incidence tree. A selected external
triangle can be retained with a favorable anchor. Every other external demand
is either kept as one intact component or boundary-opened once. Consequently
one remaining demand costs at most one unit and two remaining demands cost at
most two units. Nested blocks count as one component at the first boundary;
the intermediate cut is not used twice.

These principles include repeated owners, a common positive stem, separate
arms, and one cyclic block nested beyond another.

## 3. Item 5: actual `K4` plus three exceptional cycles

Let the external cycles be `Q_1,Q_2,Q_3`, and let `epsilon(Q)` be their sharp
cycle excess. Every nontriangle has excess at most

`epsilon(C5)=5-2sqrt(5)<2/3`.

Since the exceptional row satisfies

`epsilon(Q_1)+epsilon(Q_2)+epsilon(Q_3)>2`,

at least one external cycle is a triangle. Relabel it `T`.

First keep only the complete attached `K4` as an anchor. Its credit is greater
than two. Apply the terminal-allocation principle to the three external
demands, selecting `T` as the distinguished demand. Their total credit is
greater than `-2`; hence already

`sigma(G)>2-2=0`.                                           (1)

In the bridge-free subcase one may equivalently keep `K4` and `T` in one
shared packet `A`. Then

`sigma(A)>3`,

Root the remaining block-cut tree at `A`. There are only two cyclic demands.
For every component at the anchor boundary, keep it whole if it contains both
demands or has positive rank, and otherwise boundary-open its first cycle.
Each resulting component has credit at least `-1`, and there are at most two
of them. Therefore

`sigma(G)>3-1-1>0`.                                         (2)

Any actual bridges left after forming `A` lead only toward the two unselected
cycles. Their complete sides have credit greater than `-1` when unicyclic and
are nonnegative when they contain both demands. Thus (2) is uniform over every
connector topology and every choice, including equality, of the three first
owners.

## 4. Item 6: structural `S_4` plus two cycles

By definition of a structural rank-four row, there is a physical opening at
an internal path vertex `v`. Its owner class `R` is a nonempty tree unless it
contains an external cyclic block. The retained rank-three packet `F` is
either an attached actual `K4` or a favorable three-triangle packet, and

`sigma(F)>2`.                                                (3)

The exact item-6 sieve leaves a triangle among the two external cycles; call
it `T`, and call the other cycle `Q`.

First suppose `T` is owned by the opening at `v`. Open there before making any
other cut. The complete owner class is a strict triangular territory, while
the connected complement has rank at most five and nonnegative credit. This
closes the row.

We may therefore assume that `T` is not owned by the structural opening. If an
actual bridge occurs on the route to `T`, keep `F`, the structural tree `R`,
and use the terminal-allocation principle on `T,Q`. Their credits give

`sigma(G)>2-1-1=0`.

It remains that the route from `F` to `T` has no actual bridge. The other
cycle `Q` may nevertheless be an intermediate block on that route; thus it is
not valid simply to call `F+T` a shared packet in every such incidence. In
that nested case, boundary-open `Q` at its entry cut from `F`, keeping the cut
with `F`. The complete downstream territory contains `Q` minus that cut, the
intact triangle `T`, and all descendants on that side. It is a triangular
unicyclic territory and therefore has positive credit. The retained side
consists of `F` and the structural owner tree `R`, so

`sigma(G)>2-1+0>0`.                                           (4)

This is the nested repair: the intermediate cycle is opened once, its two path
remnants travel together downstream, and neither its entry cut nor the cut
toward `T` is duplicated.

We may now assume that `Q` does not lie between `F` and `T`. Retain `T` with
`F`. According to the two alternatives for `F`, the anchor `A` is respectively
a shared actual-`K4+T` packet or a four-triangle packet. In both cases

`sigma(A)>3`.                                                (5)

The structural owner class `R` is now a nonempty tree and has credit `-1`.
Treat the sole remaining demand `Q` at its first boundary from `A`: keep its
whole side if it has positive rank, or boundary-open it once. The resulting
territory `S` has `sigma(S)>=-1`, with a strict inequality when an intact
unicyclic side is used. Ownership gives the disjoint exhaustive partition

`V(G)=V(A) disjoint union V(R) disjoint union V(S)`,

where an empty `S` is simply omitted. Equation (5) and the tree bounds give

`sigma(G)>=sigma(A)+sigma(R)+sigma(S)>3-1-1>0`.              (6)

If `Q` is owned by the structural opening, it travels with `R`; this replaces
the tree by an intact unicyclic or higher-rank territory and can only improve
the displayed lower bound. If `Q` lies beyond `T`, retain `T` in `A` and treat
the complete `Q` side at its first boundary, exactly as above. Repeated owners
cause no overlap: their common cut stays in `A`, while only the opened side
enters `S`.

## 5. Item 7: favorable-theta `K5-e` plus a triangle

Let the missing edge of `K5-e` be `ab`, with degree-four branch vertices
`x,y,z`. An item-7 state is one of the structural states for which deletion of
the complete owner territory of a suitable center, say `z`, leaves the
favorable theta on `a,b,x,y`. Denote the deleted owner class by `R` and the
retained theta by `H`. Thus

`sigma(H)>1`.                                                (7)

The surviving external cycle in the item-7 DNN ledger is `T`.

If `T` is owned by `z`, delete the complete owner class. It is a strict
triangular territory, and the connected complement is the favorable theta,
which is nonnegative (indeed (7) is stronger). Hence the total is strict.

Assume that `T` is not owned by `z`. If an actual bridge occurs on its route,
take the first such bridge from the `K5-e` side. Its complete descendant side
has only the external triangle as a cyclic demand, so it is a triangular
territory and is strict; the pentacyclic complement is nonnegative by the
complete pentacyclic theorem. Otherwise the absence of an actual bridge means
that the two cyclic blocks meet at their unique block cut; retain `T` with `H`
there. The resulting anchor `A` is covered at every possible physical theta
root by the favorable-theta plus triangle shared-cut theorem, so

`sigma(A)>2`.                                                (8)

The deleted center territory `R`, including the interiors of all four paths
incident with `z` and every rooted branch owned there, is a nonempty induced
tree. Unit incident paths merely cross the partition; they do not duplicate an
endpoint. Therefore `sigma(R)=-1`, and

`sigma(G)>=sigma(A)+sigma(R)>2-1>0`.                         (9)

The choice among `x,y,z` is made from the physical residue state exactly as in
the complete all-odd-`K5-e` territory sieve. No switching operation changes a
path length or transports an owner.

## 6. Item 8: kernel 22 plus an arbitrary cycle

Use the physical kernel-22 opening, not merely its parity label. Delete branch
vertex `0`, the interiors of `P03,P04^0,P04^1`, and the complete descendant
set owned at every deleted vertex. The retained six unit paths on
`{1,2,3,4}` are the induced actual `K4`. The deleted core and all three path
remnants form one nonempty induced tree `R`; this remains true for every
allowed same-parity descendant because the only structural descendant path is
`P03`. Every branch, internal path vertex, connector component, and rooted-tree
descendant follows its unique first owner.

Let `Q` be the external cycle. Root the minimal block-cut subtree containing
the kernel block and `Q` at the retained `K4`.

- If `Q` is owned by a vertex of `R`, assign its complete route and descendants
  to `R`. That territory is unicyclic (or has larger positive rank if another
  cyclic component occurs on the route), hence has credit greater than `-1`
  (respectively nonnegative). Together with the attached-`K4` credit `>2` this
  is strict.
- Otherwise keep `R` as the original tree of credit `-1`. At the first
  boundary toward `Q`, cut an actual bridge and keep the complete cycle side,
  of credit `>-1`, or, at a shared cut, keep the cut upstream and boundary-open
  `Q`. The cycle-minus-cut side, including both path remnants and every
  descendant away from the cut, is one nonempty tree of credit `-1`.

Thus the worst owner-exact ledger is

`sigma(G)>2-1-1=0`.                                          (10)

A positive connector is cut at its first actual bridge; it is never absorbed
into a shared-cut packet. If the cycle is nested beyond another owner route,
the complete first-boundary side is used once. Hence no cut, route vertex, or
descendant is duplicated.

## 7. Item 9: kernel 71 plus an arbitrary cycle

For a structural kernel-71 state delete branches `1,2`, the interiors of
`12^0,12^1,15,24`, and all their owner descendants. The retained six unit
paths on `{0,3,4,5}` form an induced actual `K4`. The deleted territory `U` is
the favorable unicyclic subdivision formed by the two `12` paths, with the
`15` and `24` remnants and all attached trees. The complete structural
descendant set is exactly the canonical state and same-parity lengthening of
paths `15` and/or `24`; these path interiors remain in `U`, so the retained
actual `K4` is unchanged.

If the external cycle `Q` follows an owner in `U`, keep its complete route with
`U`. The result has rank at least two and nonnegative credit, while the
attached actual `K4` has credit `>2`. If `Q` does not follow `U`, retain `U` as
a strict favorable unicyclic territory. Treat `Q` at its first boundary from
the `K4`: an intact cycle side has credit `>-1`, and a boundary-open cycle side
is one tree of credit `-1`. Therefore

`sigma(G)>2+0-1>0`.                                          (11)

The partition is fixed before charging credit. Unit crossing paths contribute
no duplicated endpoint; all internal path vertices, connector remnants,
rooted trees, and deeper block-cut descendants stay with their unique owner.
The argument consequently covers common owners, repeated cuts, positive
routes, nested cycles, and arbitrary finite rooted trees.

## 8. Packet closure and exact scope

Sections 3--7 prove, with all physical owners and connector geometries
retained, that each of items 5--9 has empty owner-sensitive packet residual.
There is no residual owner pair, repeated-cut orbit, nested incidence, positive
connector, rooted-tree attachment, or physical-length subcase inside those
templates. Exhaustiveness belongs to the combined ledger, which also includes
the formerly omitted structural pre-sieve rows.

For fail-closed use, the only ledger facts imported before the owner argument
are: item 5 has cycle-excess sum greater than two and hence contains `T`; item
6 contains `T`; item 7 has external cycle `T`; and items 8--9 are precisely
the structural K22 and K71 physical descendant families and allow arbitrary
`Q`. If a broader provisional ledger drops the triangle gate for item 6 or 7,
this note closes exactly the
triangle-containing part and returns, rather than silently discarding, the
formal residual

`{S_4+Q_1+Q_2: Q_1,Q_2 are nontriangles}`

and/or

`{favorable-theta K5-e+Q: Q is not T}`.

Those broader rows are excluded by the exact nontriangle DNN gates in the
combined ledger.
