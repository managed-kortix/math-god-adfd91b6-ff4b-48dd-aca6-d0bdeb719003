# `R31-S C4`: the marked four-triangle side

## Theorem

Put `sigma(G)=s+(G)-|V(G)|` and `D(G)=s+(G)-s-(G)`.

**Marked four-triangle theorem.** Every cactus side of type `C4` in the
canonical doubled-`C4` marked-cut packet satisfies

`sigma(C)>3>2`.                                                 (1)

This is uniform over all legal marks, all subdivisions of the acyclic
connector remnants, and arbitrary finite trees attached at arbitrary vertices.
The theorem concerns the 28 `C4` records in the classified packet. Their four
triangle blocks form one shared-cut cluster. It does not assert (1) for an
arbitrary four-triangle cactus whose cyclic blocks are separated by bridges.

## Proof

Tree elimination in the grouped Sachs formula extracts a common positive
forest factor and replaces the core variables by positive activities. Thus it
is enough to retain all attached forests in the signless matching polynomials;
no monotonicity under tree attachment is being assumed.

Let `p` be the maximum number of pairwise vertex-disjoint triangle blocks. If
`p<=2`, the packing-two half-plane theorem gives `D(C)>0`.

Suppose `p=3`. In a connected shared-cut cluster of four cactus triangles,
choose three disjoint blocks. The fourth block must meet all three, since the
triangle intersection graph is connected. Their three intersection vertices
are distinct, since otherwise two of the chosen blocks meet. Hence the core is
exactly a central triangle `T0` with three pairwise disjoint petals
`T1,T2,T3`, one at each central vertex. This is the only packing-three case.

For `t>0`, write `Z_J(t)` for the signless matching polynomial after all rooted
trees have been retained. Put

`F=C-(V(T1) union V(T2) union V(T3))`.

The only odd-cardinality collections of disjoint cycles are the four singleton
triangles and the collection of all three petals. Therefore the imaginary part
of the normalized Sachs polynomial is

`Im Psi_C(t)=-2 sum_(j=0)^3 Z_(C-Tj)(t)+8 Z_F(t)`.              (2)

After deleting `T0`, the private edge of each petal remains. Adjoining any
subset of these three independent edges to a matching of `F` gives

`Z_(C-T0)(t)>Z_F(t)`.                                          (3)

For `i=1,2,3`, the six-vertex core induced by the vertices of the other two
petals and the surviving part of `T0` has a perfect matching: use the central
edge opposite `Ti` and the private edge of each other petal. Taking its union
with a matching of `F`, while ignoring all additional forest-boundary edges,
gives

`Z_(C-Ti)(t)>Z_F(t)`.                                          (4)

These injections preserve the signless-matching monomial weights and remain
valid after arbitrary rooted trees are attached. Equations (2)--(4) give
`Im Psi_C(t)<0` for every `t>0`. The continuous argument is consequently
negative, and the signed Coulson identity gives `D(C)>0`.

In both cases `D(C)>0`. A connected cactus with four cyclic blocks has
`|E(C)|-|V(C)|=3`, regardless of bridge subdivisions and attached trees. Since

`s+(C)=|E(C)|+D(C)/2`,

we obtain

`sigma(C)=3+D(C)/2>3>2`,

proving (1).

## Packet consequence

The `C4` orbit in the `R31-S` frontier is closed. The marked-cut census now
leaves only the complementary interior-owner packet

`sigma(D+T^3)>3`                                               (D3)

as the obstruction to the one-sided route. The theorem does not resolve `D3`.

## Verification

Run

```text
python3 research/r31-s-c4-marked-four-triangle-verifier.py
python3 -O research/r31-s-c4-marked-four-triangle-verifier.py
```

The verifier regenerates all 28 marked `C4` records, realizes their four
triangle blocks, checks the cactus and shared-cut hypotheses, classifies every
record into packing at most two or the central-three-petal case, and checks the
symbolic Sachs coefficient ledger `-2*4+8=0` in the exceptional case; the
matching injections make the domination strict.
