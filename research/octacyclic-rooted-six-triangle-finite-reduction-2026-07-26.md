# Rooted six-triangle hostile packet: exact finite reduction

## Verdict

Put

```text
sigma(G)=s+(G)-|V(G)|,  T=C3,  P=C5,
delta=sec(pi/5)-1=sqrt(5)-2.
```

The previously stated all-rank rooted-guard proof is invalid.  The assertion
that a nearest-selected-cycle Voronoi territory has cycle-packing number one
does not follow from maximality: two disjoint unselected cycles in one
territory need not replace its selected cycle if either intersects that
selected cycle.  Nothing below uses that claim.

This note records an exact incidence-and-marked-root finite reduction for the
statement needed at rank eight.  The finite certificate proves 107 of the 111
marked incidence orbits by explicit interval/packet decompositions.  Section 6
closes the four residual marked kernels by kernel-specific induced partitions:
three use a second-stage split at the private root, and the common-cut kernel
uses one two-triangle arm as a rooted Sachs packet.  Consequently Target R6P,
and hence the required `G6PP` consequence, is complete.

## 1. Target statement and the `G6PP` consequence

The required finite theorem is:

> **Target R6P.** Let `A` be a connected cactus whose cyclic blocks are exactly
> six triangles in one shared-cut cluster, let `r` be any vertex of its cyclic
> hull, and coalesce a pentagon `P` with `A` at `r`.  Arbitrary finite trees may
> be attached at arbitrary vertices.  Then
> `sigma(A dot_r P)>1-delta`.

A positive connector between `r` and `P` is already allowed as an attached
tree on the packet spine, so the same formulation covers a single rooted
bridge interface.

Target R6P is exactly what the disconnected entry-locked class `(G6PP)` needs.
Cut the last actual bridge before the remote pentagon `P_1`.  The component
`H_0` on the cluster side consists of six triangles, the leaf pentagon `P_0`,
and arbitrary trees at one root/bridge interface; the other component `H_1` is
pentagonal unicyclic.  Hence R6P and the sharp unicyclic bound would give

```text
sigma(G) >= sigma(H_0)+sigma(H_1)
         > (1-delta)-delta
          = 5-2sqrt(5)>0.
```

Accordingly it remains only to close the four finite-certificate residuals in
Section 5; this is done in Section 6.

## 2. Exact incidence objects and root marks

Let `I(A)` be the bipartite cycle-cut incidence tree.  Its cycle nodes are the
six triangles; its cut nodes are vertices lying in at least two triangles.
Every cycle node has degree at most three and every cut node has degree at least
two.  Conversely every such colored tree has a cactus realization.  Cyclic
order causes no additional choice for a triangle: its at most three incidence
marks occupy distinct vertices.

There are exactly 19 unmarked isomorphism classes of the triangular incidence
tree.  A root orbit is either

1. a cut node of `I(A)`, or
2. a private cyclic vertex on a triangle of incidence degree one or two.

Private vertices on the same triangle are equivalent because that triangle has
an automorphism fixing all incidence marks and exchanging those vertices.
Canonical colored-tree coding gives exactly 111 marked-root orbits, representing
247 labelled cyclic-root positions, over these 19 triangular trees.  (This is
not the separate count of 111 unmarked
`T^6P` incidence trees in which `P` is an incidence leaf.) This number is
independent of attached trees: each off-hull tree has a unique hull
attachment and follows the owner of that attachment in every decomposition.

## 3. Allowed decomposition certificate

For a marked incidence tree choose a nonempty family `K` of pairwise
intersecting triangles containing the root: if the root is private, its
triangle belongs to `K`; if it is a cut, at least one triangle at that cut
belongs to `K`.  Pairwise intersecting triangles have vertex-packing number one,
so the proved one-hostile-cycle Sachs packet applies directly to `P+K` and
gives

```text
sigma(P+K)>|K|-delta.                                    (3.1)
```

This is the only use of a packing-one statement in the first-stage
certificate.  It is checked directly from incidence, not inferred from a
Voronoi partition.

For every triangle `S` outside `K` that meets `K`, split `S` into consecutive
vertex intervals at its incidence marks.  The certificate accepts the split
only when all of the following exact ownership tests hold:

1. `S` has one inward incidence mark toward `K`;
2. no two split triangles meet each other;
3. each outward mark of `S` leads to one retained incidence component; and
4. distinct outward marks lead to distinct retained components.

Give the inward interval to the rooted hostile packet and each outward interval
to its corresponding retained component.  If `S` has no outward component,
opening one private vertex produces one nonempty tree territory and incurs the
exact charge `-1`.  Conditions 1--4 guarantee that all pieces are proper
consecutive intervals, every shared cut has one owner, no retained cyclic
component is joined to another through a split remnant, and all resulting
territories are induced.

Let `s` be the number of terminal split triangles and let the retained
triangular components have sizes `r_1,...,r_j`.  Use the established exact
shared-cluster margins

```text
L_1=0, L_2=1, L_3=2, L_4=3, L_5=2, L_6=1,
sigma(A_r)>L_r.
```

Equations (3.1), induced-partition superadditivity, and the terminal tree
charges give the strict certificate

```text
sigma(A dot_r P) > |K|-delta-s+sum_i L_(r_i).             (3.2)
```

Thus the desired bound follows whenever the integer packet score

```text
M=|K|-s+sum_i L_(r_i)                                    (3.3)
```

is at least one.  Notice that (3.2) is uniform over arbitrary attached trees:
tree branches are never suppressed or spectrally approximated, but are assigned
whole to the interval owning their attachment.

## 4. Exact census result

The executable certificate is
`research/octacyclic-rooted-six-triangle-certificate.py`.  It generates all
incidence trees by inverse leaf deletion/insertion, canonicalizes every root
mark, exhausts all possible `K`, verifies the four interval ownership tests,
and evaluates (3.3) in integer arithmetic.  It also asserts the four
second-stage groupings of Section 6, checks their incidence separation and
packing numbers, and prints their integer margins `3,3,3,2`.

Its asserted output is

```text
unmarked incidence trees: 19
marked cyclic-root orbits: 111
labelled cyclic-root positions: 247
certified marked orbits: 107
certificate margins: {1: 5, 2: 14, 3: 28, 4: 58, 6: 2}
exact residual marked orbits: 4
```

Therefore (3.2) proves Target R6P for 107 marked-root classes.  The five score-1
classes are strict because the hostile packet inequality (3.1) is strict.  The
four rows below are residuals only for that particular certificate grammar,
not for the theorem.

## 5. Exact residual

Cycle labels are `0,...,5`; cut labels start at `6`.  A private mark on cycle
`0` is written `root=private(0)`, and a cut mark is written `root=cut(6)`.
Up to marked color-preserving isomorphism, the four unresolved kernels are:

```text
R1 root=private(0)
   ((0,6),(0,7),(1,6),(2,7),(3,6),(4,6),(5,7))

R2 root=private(0)
   ((0,6),(0,7),(1,6),(1,8),(2,7),(3,6),(4,7),(5,8))

R3 root=private(0)
   ((0,6),(0,7),(1,6),(1,8),(2,7),(3,6),(3,9),(4,8),(5,9))

R4 root=cut(6)
   ((0,6),(0,7),(1,6),(1,8),(2,7),(3,6),(3,9),(4,8),(5,9))
```

For R1 and R2 no decomposition satisfying the packet interface tests exists.
For R3 and R4 the best score in (3.3) is zero, not one.  R3 and R4 are the two
root orbits of the same unmarked kernel: a three-arm subdivided star, each arm
consisting of a router triangle and a terminal triangle.

These four rows are the exact residual for the first-stage interval/packing-one
packet system.  The next section gives the required kernel-specific second
stage.

## 6. Exact resolution of R1--R4

We use only three already established spectral statements, all uniform under
arbitrary tree attachments:

```text
sigma(pentagonal unicyclic packet) >= -delta,              (6.1)
sigma(triangular unicyclic packet) > 0,                    (6.2)
sigma(h-triangle packet)>h-1 if its packing number <=2.    (6.3)
```

For (6.3), the grouped Sachs expansion has only singleton and two-cycle
collections.  Its imaginary part is
`-2 sum_T Z_(H-V(T))(t)<0`; signed Coulson and
`|E(H)|=|V(H)|+h-1` give the displayed strict bound.  This is the exact
packing-two phase theorem and includes (6.2) when `h=1`.

We also use (3.1) with two intersecting triangles:

```text
sigma(P plus two intersecting triangles)>2-delta.          (6.4)
```

Statement (6.4) permits a positive joining path between the triangular lobe
and `P`; it is the packing-one rooted Sachs packet, not an additive use of the
isolated pentagon bound.  In every partition below, an off-hull tree is given
whole to the part containing its unique hull attachment.  Thus every part is
induced.  Edges between distinct parts are discarded, and induced-partition
superadditivity gives `sigma(G)>=sum sigma(G_i)`.

We shall repeatedly split at a private root `r` of triangle `(r,6,7)`.  The
pentagonal part owns `r`; the opposite edge `67` then runs between two retained
parts and is discarded by the induced partition.  This is the required
second-stage split of the connector remnant.  No spectral estimate is assigned
to that edge.

### R1

Let `r` be the private root of triangle `0`.  The other two vertices of
triangle `0` are cuts `6` and `7`; after `r` is put with `P`, the edge `67`
remains.  Put `P`, its root-to-`r` connector (possibly of length zero), `r`,
and every tree branch owned there in the first part.  The first part is
pentagonal unicyclic, so (6.1) applies.

Make a second part from all vertices on the cut-`6` side, carrying triangles
`1,3,4`, and a third part from the cut-`7` side, carrying triangles `2,5`.
Within each part all triangles have a common cut, so their packing numbers are
one.  Equation (6.3) gives surpluses `>2` and `>1`, respectively.  Consequently

```text
sigma(G)>=sigma(G[P side])+sigma(G[6 side])+sigma(G[7 side])
        > -delta+2+1
         >1-delta.                                         (6.5)
```

This proves R1 for every assignment of attached trees.

### R2

Use the same split at the private vertex of triangle `0`.  Again its opposite
edge is `67`.  The cut-`6` side consists of triangles `1,3,5`: triangle `1`
meets `3` at `6` and `5` at `8`, while `3` and `5` are disjoint.  Its packing
number is exactly two, so (6.3) gives surplus `>2`.  The cut-`7` side consists
of the intersecting triangles `2,4` and has surplus `>1`.  Together with
(6.1), these are exactly the ledger (6.5), proving R2.

### R3

Split once more at the private root of triangle `0`.  In the complement the
cut-`6` side consists of triangles `1,3,4,5`: routers `1,3` meet at `6`, and
terminals `4,5` meet routers `1,3` at `8,9`, respectively.  Any three of these
four include an intersecting pair; equivalently, the only disjoint pair of
maximum size is the two terminals.  Thus its packing number is two and (6.3)
gives surplus `>3`.  The cut-`7` side is the single triangle `2`, with surplus
`>0` by (6.2).  With the pentagonal part, induced-partition superadditivity
therefore gives `sigma(G)>3-delta>1-delta`, proving R3.

The preceding three arguments therefore cover a nonzero connector to `P`
without an additional spectral approximation: the connector is retained
whole in the pentagonal unicyclic part.

### R4

Write `x=6`.  The kernel has three arms at `x`:

```text
(router 0, outer cut 7, terminal 2),
(router 1, outer cut 8, terminal 4),
(router 3, outer cut 9, terminal 5).                       (6.6)
```

Form an induced part `H_0` from `P`, the joining interface, `x`, and the whole
first arm (triangles `0` and `2`).  These two triangles intersect at cut `7`,
so their packing number is one.  The pentagon meets the lobe at `x` (or is
joined to it by the allowed connector).  Therefore the exact rooted Sachs
packet (6.4) gives

```text
sigma(H_0)>2-delta.                                       (6.7)
```

For each of the other two arms, form one induced part from all its vertices
except `x`.  Deleting `x` opens its router triangle into the edge from its
outer cut to its private vertex.  The terminal triangle remains intact.
Thus each of these two parts is triangular unicyclic with the opened router
edge, connector stubs, and arbitrary owned branches merely attached as trees.
By (6.2), their surpluses are both strictly positive.  Hence

```text
sigma(G)>=sigma(H_0)+sigma(H_1)+sigma(H_2)
        >2-delta
         >1-delta.                                         (6.8)
```

This is the missing multi-pivot resolution: rather than Schur-complement all
three arms simultaneously, it keeps one complete arm in the hostile rooted
packet and performs a second-stage interval split at `x` on the other two.
No attachment variable is specialized or suppressed.

Combining (3.2), (6.5), and (6.8) proves Target R6P for all 111 marked-root
orbits.  Substitution in the bridge cut calculation of Section 1 gives

```text
sigma(G)>1-2delta=5-2sqrt(5)>0
```

for the `G6PP` class.

## Reproduction

Run from the repository root:

```bash
python research/octacyclic-rooted-six-triangle-certificate.py
```

The script uses no floating point, numerical eigensolver, or unproved Voronoi
ownership assertion.  Its second-stage rows are finite incidence certificates;
the uniform spectral content is supplied by the Sachs inequalities
(6.1)--(6.4), whose attachment variables remain arbitrary.
