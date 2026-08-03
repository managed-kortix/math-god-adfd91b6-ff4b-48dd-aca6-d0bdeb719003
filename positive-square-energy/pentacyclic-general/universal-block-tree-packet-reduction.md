# Universal induced block-tree packets for the pentacyclic multiblock rows

## 1. Statement

For a graph `X`, put

`sigma(X)=s^+(X)-|V(X)|`.

Consider a connected pentacyclic graph with at least two positive-rank cyclic
blocks. Arbitrary bridge connectors and arbitrary rooted trees are allowed.
After the exact block-additive DNN sieve, every remaining row is closed by the
packet theorem below except the following two incidence families:

1. `D+T+T+P`, where `D=Theta(1,2,2)`, `T=C3`, and `P=C5`, and none of the
   three external cycles is owned by either admissible internal-arm opening of
   `D`;
2. a canonical structural rank-three block plus `T+T`, where neither external
   triangle is owned by any admissible structural opening. The rank-three block
   is one of:
   - canonical doubled-triangle class `111`;
   - canonical doubled-`C4` class `111`;
   - an all-odd `K4` subdivision with exactly one long path.

The following formerly listed rows are completely closed, with no incidence
restriction:

- an unsubdivided `K4` plus any two residual cycles;
- `K4+Theta(1,2,r)`, including the exceptional diamond;
- every structural rank-four block plus one cycle.

Thus the exact multiblock proof residual is smaller than the block-family
residual: it consists only of the two routed obstructions above. This is a
proof-theoretic residual, not a claim that these graphs are counterexamples.

## 2. Packet theorem

Let `G` be connected and let `B` be a distinguished cyclic block. Delete the
edges of `B`; each remaining component is owned by its unique first vertex of
`B` on the block-cut-tree route. If `v` is an internal vertex of an openable
path of `B`, let `U_v` contain `v`, every off-block component owned by `v`, and
every rooted branch based there. The two opened path remnants remain with
their endpoint side. Put `R_v=G-U_v`.

Whenever the chosen opening is one of the structural openings used below,
`U_v` and `R_v` are connected induced graphs, partition `V(G)`, and `R_v` is
connected. The following three rules hold.

### Rule A: routed favorable guard

Suppose `U_v` contains at least one complete triangle, all its complete cyclic
blocks are triangles except possibly one cycle `Q`, and `Q` is arbitrary.
Then

`sigma(U_v)>0`.                                                (A)

Indeed, for `Q` even or `3 mod 4` this is the all-rank nonhostile one-cycle
cactus theorem; for `Q=1 mod 4` it is the all-rank hostile one-cycle theorem.
The case with no distinguished `Q` is the all-triangular theorem. These
theorems allow shared cuts, bridge connectors, and arbitrary attached trees.

Consequently, if `beta(R_v)` is between two and four, the already established
rank-two through rank-four theorem gives `sigma(R_v)>=0`. If `beta(R_v)=1`
and its cycle is favorable, its credit is positive. In either case induced
superadditivity yields

`sigma(G)>=sigma(U_v)+sigma(R_v)>0`.                           (B)

This is the universal routing rule: one favorable guard on the opened side
removes the tree payment altogether. No quantitative triangular margin is
being added to a hostile deficit.

### Rule B: high-credit anchor

Suppose an induced connected anchor `A` has `sigma(A)>c` for an integer `c`, and the complement
can be partitioned into at most `c` connected induced pieces, each of credit
at least `-1`. Then `sigma(G)>0`.

For the applications here `c=2`. The anchor is either an attached `K4` or a
favorable rank-three packet. A cycle opened at a shared cut is a nonempty tree
and has credit `-1`; an intact unicyclic packet has credit greater than `-1`;
and a connected packet of rank at least two has nonnegative credit. Thus the
strict anchor inequality pays every possible boundary loss.

### Rule C: structural opening with one external cycle

Suppose opening `v` leaves a favorable rank-three packet `F` with
`sigma(F)>2` and creates one nonempty tree. Adjoin one external cycle `Q`.
Then every block-tree incidence is positive:

- if `Q` follows the opened side, that side is unicyclic and has credit `>-1`;
- if `Q` is bridge-separated from `F`, use credits `>2`, `-1`, and `>-1`;
- if `Q` shares a cut with `F`, open `Q` at that cut, producing a second tree.

In all cases the strict credit `>2` pays the at most two negative units.

These rules depend only on induced ownership in the block tree. They never
switch physical path lengths and never assign a shared cut to two territories.

## 3. The diamond row `D+T+T+P`

Write the diamond paths as the edge `xy`, the two length-two paths `xay` and
`xby`. Opening `a` or `b` leaves the other intrinsic triangle and lowers the
rank by one.

If either external triangle is owned by one of these two openings, choose that
opening. Its territory is a cactus containing a triangle and at most the other
triangle and the pentagon, so Rule A gives it positive credit. The connected
complement has rank at most four and has nonnegative credit. Hence the whole
graph is strict.

If no external triangle is owned but the pentagon is owned by an opening, its
territory has credit at least `-(sqrt(5)-2)`. The complement is a connected
three-triangle cactus. If its packing number is at most two, its credit is
`>2`. If its packing number is three, an actual bridge splits it into a
two-triangle packet and a triangular packet, of total credit `>1`. Thus this
case has total credit `>1-(sqrt(5)-2)>0` as well.

This proves every incidence in which any external cyclic block is routed
through `a` or `b`. The only remaining diamond incidences are therefore those
in which all three external cycles route through the endpoints `x,y`.

There is one further automatic closure inside this fail-closed row.

- If an actual bridge partition realizes `TT+TP` after the opening, its credit
  is `>1+(1-(sqrt(5)-2))>1`; it pays the opened tree.

Accordingly, a genuinely unresolved diamond incidence has all external cycles
routed through `x,y` and must evade the `TT+TP` refinement. In the resulting
tree-opening channel the available general bound for the retained `TTTP`
cactus is only

`sigma(TTTP)>1-(sqrt(5)-2)<1`,                                (C)

so it does not pay the tree. In the pentagon-opening channel, three dispersed
triangle territories are individually strict but have no uniform total margin
against the pentagon deficit. This is precisely where a formal sum of strict
inequalities would be invalid.

## 4. Canonical rank three plus two triangles

Each canonical structural block has an admissible opening whose deleted
territory is a tree and whose complement is a favorable bicyclic packet of
credit `>1`:

- doubled triangle class `111`: open the odd connector when it is long, or an
  even member of a canonical doubled pair when the connector is direct;
- doubled-`C4` class `111`: open an internal vertex of an available connector;
- one-long all-odd `K4`: open an internal vertex of the unique long path.

If an external triangle is owned by any admissible opening, Rule A makes the
opened territory strict; the complement has rank at most four and is
nonnegative. Therefore the graph is strict.

The only surviving incidences are exactly those in which both external
triangles avoid every admissible opened territory. The opening then leaves one
tree and a connected tetracyclic packet obtained by adjoining both triangles
to the favorable bicyclic remainder. The known statements give positivity of
that tetracyclic packet, but not the uniform credit `>1` required to pay the
tree. If the retained triangles disperse through long bridge routes, the
individual triangular credits are strict but not uniformly bounded away from
zero. Hence favorable phase alone does not justify the missing unit.

## 5. `K4` plus cycle pairs

Keep the complete attached `K4` packet, whose credit is `>2`, and root the
reduced block tree there. There are at most two external cyclic demands.

Across an actual bridge, an intact unicyclic demand has credit `>-1`, while a
component containing both demands has nonnegative credit by the bicyclic
theorem. At a shared cut, assign the cut to the `K4` anchor and open the
incident cycle; the cycle-minus-cut side is a nonempty tree of credit `-1`.
If one cycle lies between the anchor and the other, treat their connected side
as one rank-two component rather than duplicating the intermediate cut.

Thus there are at most two negative units and Rule B applies. This closes every
`K4+Q_1+Q_2` incidence, including two hostile cycles and nested cycle pairs.

## 6. `K4` plus an exceptional theta

If the blocks are separated by an actual bridge, the attached `K4` has credit
`>2` and the theta, being bicyclic, has nonnegative credit. If they share a cut
`z`, keep `z` with the complete `K4`. The induced graph `Theta-z` is connected
and has rank at most one: it is a tree when `z` is a theta endpoint and is
unicyclic when `z` is internal to an arm. Its credit is therefore `>-1`.
Rule B closes the row, in particular `K4+Theta(1,2,2)`.

## 7. Structural rank four plus one cycle

The structural rank-four proof opens one path, creates one tree, and retains
either an attached all-odd `K4` packet or a three-favorable-triangle packet.
In both cases the retained credit is `>2`. Rule C then handles every position
of the external cycle. All nonstructural rank-four rows were already direct
DNN rows with excess at most three and absorb one cycle excess at most one.
Hence the complete `4+1` partition is closed.

## 8. Exact frontier and missing quantitative input

Combining the DNN sieve with Rules A--C closes the multiblock partitions

`2+2+1`, `3+2`, and `4+1`,

and all noncanonical rows in `2+1+1+1` and `3+1+1`. It also closes every
routed-triangle incidence in the two exceptional families.

What remains is exactly:

1. `D+T+T+P` incidences in which all three external cycles route through the
   diamond endpoints and the retained `TTTP` packet evades the `TT+TP`
   refinement in Section 3;
2. no-routed-triangle canonical rank-three plus `T+T` incidences.

A complete universal theorem would follow from either of these genuinely new
quantitative statements:

- every retained `TTTP` packet arising from a diamond opening has credit `>1`;
- every tetracyclic packet formed from one of the three canonical favorable
  bicyclic remainders and two triangles has credit `>1`.

The existing all-rank cactus theorem supplies only positivity in the first
generality, and the general tetracyclic theorem supplies only nonnegativity in
the second. Strict triangular phase margins cannot be promoted to one uniform
unit: attached triangular unicyclic packets have no quoted positive lower
bound. Therefore the two displayed quantitative claims, or a new opening that
forces a triangle onto the opened side, are the exact remaining multiblock
obligation.
