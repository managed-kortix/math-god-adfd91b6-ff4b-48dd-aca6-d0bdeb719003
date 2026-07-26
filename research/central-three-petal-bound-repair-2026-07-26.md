# Internal repair: central triangle with three triangular petals

## Status

This is an internal verification note, not a public theorem announcement.

For a graph `G`, write

`sigma(G)=s+(G)-|V(G)|`.

The premise that the bare central-triangle/three-petal core has `sigma=3` is
false. Its exact value is `6`. The previously used strict packet bound

`sigma(G)>3`

is valid, including arbitrary finite trees attached at arbitrary core
vertices. Thus the rank-four through rank-seven opening recurrence needs no
new compensating packet.

## 1. Exact spectrum of the bare core

The recorded characteristic polynomial is correct:

`phi(x)=x^9-12x^7-8x^6+42x^5+48x^4-36x^3-72x^2-27x`.

Its factorization should be completed:

`phi(x)=x(x-3)(x^2-3)(x^5+3x^4-8x^2-9x-3)`

`      =x(x-3)(x^2-3)^2(x+1)^3`.

Indeed,

`x^5+3x^4-8x^2-9x-3=(x^2-3)(x+1)^3`.

Hence the adjacency spectrum, with multiplicity, is

`3, sqrt(3), sqrt(3), 0, -sqrt(3), -sqrt(3), -1, -1, -1`.

Therefore

`s+=3^2+2(sqrt(3))^2=15`,

`s-=2(sqrt(3))^2+3=9`,

and, since the core has nine vertices,

`sigma=15-9=6`.

The erroneous value `3` came from counting the distinct positive roots `3`
and `sqrt(3)` once each and omitting the second occurrence of `sqrt(3)`.
The prior exact Sturm script isolated distinct roots but its surplus
calculation summed one square per isolating interval without restoring
algebraic multiplicity. Consequently every energy or increment in the prior
certificate that can involve a repeated eigenvalue was unaudited. The script
and regenerated certificate now attach a multiplicity to every isolated root
and weight its squared interval accordingly.

## 2. Uniform strict bound with arbitrary attached trees

Let `T0` be the central triangle and `T1,T2,T3` the pairwise vertex-disjoint
petals. Let

`U=V(T1) union V(T2) union V(T3)` and `F=G-U`.

The set `U` contains all nine core vertices. Thus `F` is the forest left from
the arbitrary attached trees after their core roots are removed. For the
signless matching polynomial

`Z_H(t)=sum_j m_j(H)t^(|V(H)|-2j)`,

the grouped Sachs expansion gives, for every `t>0`,

`Im Psi_G(t)=-2 sum_(j=0)^3 Z_(G-V(Tj))(t)+8Z_F(t)`.             (1)

After deleting `T0`, the three edges opposite the petal roots are disjoint and
disjoint from `F`. Ignoring all additional forest edges gives a
coefficientwise matching injection, so

`Z_(G-V(T0))(t)>Z_F(t)`.                                        (2)

For `i=1,2,3`, the six core vertices in `U-V(Ti)` have a perfect matching:
use the central edge between the other two petal roots and the two opposite
petal edges. Their induced graph `Hi` consequently satisfies `Z_Hi(t)>1`.
Taking the disjoint union of a matching of `Hi` and a matching of `F`, while
ignoring any extra edges between them, gives

`Z_(G-V(Ti))(t)>=Z_Hi(t)Z_F(t)>Z_F(t)`.                          (3)

Equations (2)-(3) imply

`sum_(j=0)^3 Z_(G-V(Tj))(t)>4Z_F(t)`.

By (1), `Im Psi_G(t)<0` for every `t>0`. The normalized characteristic curve
therefore remains in the open lower half-plane. Its continuous argument is
the eigenvalue argument tending to zero at infinity, so the signed Coulson
identity gives

`s+(G)-s-(G)>0`.

Every such connected four-cyclic cactus has `|E(G)|=|V(G)|+3`, including all
tree attachments. Since `s+(G)+s-(G)=2|E(G)|`, it follows that

`s+(G)>|E(G)|=|V(G)|+3`,

and hence

`sigma(G)>3`.                                                    (4)

Strictness in (4) is universal for this incidence and does not depend on a
nontrivial attachment. The bare core is not an equality case; it has surplus
`6`.

This proves only a strict inequality, not a uniform numerical gap above `3`
over all attached trees.

## 3. Exact rank-four through rank-seven routes

Let `A_r` be a connected shared-cut cluster of `r` triangles with arbitrary
attached trees.

### Rank four

If the cycle-packing number is at most two, the favorable-cycle phase theorem
gives `sigma(A_4)>4-1=3`. If it is three, shared-cut connectivity forces the
central-triangle/three-petal incidence, and Section 2 gives the same strict
bound. Thus

`sigma(A_4)>3`.

### Rank five

Open a private vertex of an incidence-leaf triangle. The opened induced
territory is a nonempty tree `F1`, so `sigma(F1)=-1`; the complement is an
`A_4` packet with all remnants treated as attached trees. Therefore

`sigma(A_5)>=sigma(A_4)+sigma(F1)>3-1=2`.

### Rank six

Perform two successive incidence-leaf openings. The two opened territories
are disjoint nonempty trees and the retained packet is `A_4`. Hence

`sigma(A_6)>=sigma(A_4)-2>3-2=1`.

### Rank seven

Perform three successive incidence-leaf openings. Then

`sigma(A_7)>=sigma(A_4)-3>3-3=0`.

The weak superadditivity steps do not lose strictness because the retained
rank-four packet is strict and each tree contribution is the exact equality
`-1`.

## 4. What would happen under the false equality premise

If one discarded Section 2 and assumed only `sigma(A_4)>=3`, the same opening
ledger would yield only

`sigma(A_4)>=3`, `sigma(A_5)>=2`, `sigma(A_6)>=1`, `sigma(A_7)>=0`.

At rank seven that route would not prove strict positivity. A disjoint packet
with strictly positive surplus would restore strictness only when the rest of
the ledger has no additional unpaid negative cost. More generally, if the
other territories have certified total lower bound `L`, one needs a packet
whose strict lower bound is greater than `-L`; a merely qualitative positive
packet cannot pay a fixed hostile-cycle deficit or another tree cost.

In applications where an independent strict triangle, `TT`, `TQ`, or another
strict packet survives after all integer costs are exactly balanced, that
packet can supply final strictness. It is not needed for the pure `A_4` through
`A_7` recurrence, because (4) supplies strictness at the retained base.

## 5. Repair consequences

1. Retain the strict packet statement `sigma(A_4)>3` and its rank-five through
   rank-seven consequences.
2. Delete or quarantine the claim that the bare central-petal core has
   `sigma=3`; the exact value is `6`.
3. Do not use the current distinct-root Sturm surplus sums for exact energies,
   attachment increments, or monotonicity comparisons until root
   multiplicities are restored.
4. No public announcement is warranted from this repair. Public manuscripts
   that cite the matching-injection proof have the correct strict conclusion;
   only explanations relying on the erroneous exact surplus need correction.
