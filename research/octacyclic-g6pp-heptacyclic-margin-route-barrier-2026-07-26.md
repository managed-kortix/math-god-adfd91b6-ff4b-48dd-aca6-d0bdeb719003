# The heptacyclic-margin route for `G6PP`: exact reduction and barrier

**Date:** 2026-07-26

## Verdict

Cutting the last connector bridge before the remote pentagon is a valid and
useful reduction. It reduces the disconnected octacyclic row

```text
T^6P_0 | P_1
```

to one precise uniform heptacyclic estimate. The generic heptacyclic theorem,
the sharp DNN inequality, and the presently available packing-one phase lemma
do not prove that estimate, even after recording that `P_0` intersects one
triangle. Thus this route is not currently a census-free proof. Its exact
missing input is the following quantitative strengthening:

> **Leaf-pentagon margin lemma.** Every connected cactus `H` whose cyclic
> blocks are six triangles and one pentagon, with the pentagon an incidence
> leaf, and with arbitrary finite trees attached at arbitrary vertices,
> satisfies
> `sigma(H)>delta`, where `delta=sqrt(5)-2`.

In fact the stronger bound `sigma(H)>1-delta` would be enough and is the natural
rooted-phase target. Proving either statement by a winding-sensitive spectral
argument would give the requested alternative. None of the existing generic
inputs implies it.

## 1. The connector cut and the exact required margin

Write

```text
sigma(X)=s+(X)-|V(X)|,  T=C3,  P=C5,
delta=sqrt(5)-2.
```

Let `G` be in the entry-locked disconnected class `G6PP`. Cut the last actual
bridge before the remote pentagon `P_1`. Let `H_1` be the resulting remote
pentagonal unicyclic territory and let `H_0` be the other territory. Every
connector vertex and every branch off the connector belongs to exactly one of
these territories. In particular, the connector remnant on the `H_0` side is
only an attached tree; it is not discarded or shortened.

The sharp unicyclic estimate gives

```text
sigma(H_1)>=-delta.
```

The other side `H_0` is a heptacyclic cactus with cyclic multiset `T^6P_0`, and
`P_0` is an incidence leaf. Induced-partition superadditivity therefore gives

```text
sigma(G)>=sigma(H_0)+sigma(H_1)>=sigma(H_0)-delta.       (1.1)
```

Consequently `sigma(H_0)>delta` is exactly sufficient. Notice that the cyclic
attachment of `P_0` and the root of the connector remnant are generally two
different marks. A theorem uniform over arbitrary attached trees absorbs the
second mark, but a finite rooted census must not silently identify the two.

The established heptacyclic theorem supplies only

```text
sigma(H_0)>0.
```

Substitution in (1.1) gives only `sigma(G)>-delta`, not positivity. Strict
positivity on an unbounded class of tree attachments cannot be upgraded to a
fixed margin by compactness: the attachment parameter space is neither finite
nor compact, and the theorem states no quantitative gap.

## 2. Why sharp DNN does not supply the missing amount

Put

```text
a=epsilon_5=5-2sqrt(5).
```

For a heptacyclic cactus the sharp cactus DNN estimate is

```text
sigma(H)>=6-sum_C epsilon_|C|.
```

On `T^6P` this becomes

```text
sigma(H_0)>=6-(6+a)=-a=2sqrt(5)-5.                       (2.1)
```

Thus a DNN refinement would have to recover more than

```text
a+delta=3-sqrt(5),
```

approximately `0.7639`, uniformly over every incidence and every tree
attachment, merely to reach `sigma(H_0)>delta`.

The existing DNN functional cannot see the proposed extra datum "one triangle
intersects the pentagon." Its sharp cactus constant is block additive:

```text
kappa(H)=b+sum_C kappa(C),
```

so it depends on the bridge blocks and cycle lengths, not on which cyclic
blocks share a cut. In particular, every `T^6P` incidence receives exactly the
same right side (2.1). Any successful strengthened DNN proof must add a new
stability statement showing that the particular spectral matrix `B circ B`
coming from the negative part of the adjacency matrix stays a uniform distance
from the DNN optimizer. Such a stability theorem is not contained in sharpness
or block additivity, and no uniform gap of size `3-sqrt(5)` is presently known.

## 3. Why one intersecting triangle is not by itself a phase proof

If a triangle `T_*` intersects `P_0`, the valid packing-one rooted Sachs lemma
does give the strong local packet estimate

```text
sigma(P_0+T_*)>1-delta>delta.                             (3.1)
```

Equation (3.1) would prove the leaf-pentagon margin lemma if the other five
triangles could always be put into disjoint induced nonnegative territories.
That separation is the missing structural assertion, not a consequence of
the existence of `T_*`.

For example, if another retained triangle and `T_*` use the same shared cut,
both cycles require ownership of that vertex. They cannot be retained in two
different members of a vertex partition. More generally, triangle routers can
force a split cycle to carry several incidence branches, and opening triangles
to restore ownership costs one unit per nonempty tree territory. Therefore the
local credit in (3.1) can only be used after proving a global induced ownership
decomposition. Establishing that decomposition for every six-triangle
incidence is essentially the finite rooted problem that this proposed route was
meant to avoid.

Putting additional non-pairwise-intersecting triangles into the phase packet
does not repair the argument. The grouped Sachs expansion then contains
alternating terms from collections of two or more disjoint triangles. The
packing-one sign argument no longer applies.

There is an exact bare-core obstruction to the most natural replacement. For
the explicit six-triangle rooted pentagon core recorded in
`multiple-triangle-rooted-phase-obstruction-2026-07-26.md`, its normalized
Schur--Sachs polynomial `Psi=R+iI` satisfies, as `t` decreases to zero,

```text
R(t)=-75t+O(t^3)<0,
I(t)=6+O(t^2)>0.
```

Its inertia is `(7,10,0)`, so the continuous Coulson phase tends to `-3pi/2`,
not to the principal value `pi/2`. Hence a proof based on `R>0`, a principal
arctangent, or the packing-one coefficient signs is impossible even before
trees are attached. Exact activity-polynomial calculations also give negative
monomials and realizable negative evaluations after arbitrary rooted trees are
eliminated. These facts do not disprove the desired energy margin; they show
that it requires winding control rather than a positivity-only phase chart.

## 4. What would complete this alternative

There are two genuinely census-free ways to finish (1.1).

1. Prove the leaf-pentagon margin lemma directly, uniformly over all rooted-tree
   activities. A sufficient stronger statement is the correctly unwrapped
   Coulson-phase comparison that yields
   `sigma(T^6P)>1-delta`. It must control negative-real-axis crossings; a
   principal-phase or coefficientwise proof is ruled out by Section 3.
2. Prove a structural guard-extraction theorem for every rooted triangular
   incidence tree: retain a packing-one `P_0+K` packet, where `K` is a nonempty
   pairwise-intersecting family, and split the remaining routers into induced
   all-triangle packets with total nonnegative ledger. The theorem must include
   the two independent marks (the `P_0` cut and the connector-tree root), shared
   cut ownership, and arbitrary off-hull trees. Without such a theorem, saying
   "choose one intersecting triangle" omits the central ownership step.

The packing-two triangular estimate can help in option 2, because a retained
`h`-triangle packet of packing number at most two has surplus `>h-1`. But the
fact that one triangle intersects `P_0` does not force the complementary
packets to have packing number at most two, nor does it produce their induced
partition. A separate structural lemma is still required.

## 5. Conclusion

The connector sacrifice is exact:

```text
G6PP -> (leaf-pentagon T^6P_0 side) + P_1,
required ledger:  >delta-delta=0.
```

The proposed shortcut stops at the first term. Generic heptacyclic positivity
has no fixed margin, sharp DNN gives the negative bound `-a` and is incidence
blind, and one intersecting triangle only gives a local phase packet whose
global ownership is not automatic. Therefore there is presently a rigorous
barrier, not a census-free proof. The exact new theorem needed is the uniform
leaf-pentagon margin lemma above (or the stronger unwrapped-phase bound
`>1-delta`).
