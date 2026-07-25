# Triangle plus one cycle in a bicyclic cactus

## Scope and conclusion

Let `G` be a connected bicyclic cactus.  Assume that its two cyclic blocks are
`C_3` and `C_l`; they may share a cut vertex or be joined by an arbitrary
bridge path, and arbitrary rooted trees may be attached anywhere.  Thus
`m(G)=n(G)+1`.

The sharp effective-DNN lemma posited in the research prompt, together with
the packing-two Sachs theorem, settles all cases except

`C_3` together with `C_{4k+1}`, for `k>=1`.

For that residual, the tempting pointwise carrier inequality

`Z_{G-V(C_3)}(t) >= Z_{G-V(C_{4k+1})}(t)`

is false, even for a seven-vertex core with one pendant leaf.  Consequently
the proposed fixed-half-plane proof does not establish the residual theorem.
No counterexample to the AKMP inequality was found, but the argument below
does not prove it.  The exact unresolved statement is

`s^+(G) >= n(G)`

for arbitrary tree attachments in the mixed-phase `C_3,C_{4k+1}` class.

## Complete reduction

Write

`Psi_G(t)=i^{-n} phi_G(it)`

and

`Z_H(t)=sum_j m_j(H)t^{|H|-2j}`.

The grouped Sachs expansion is

`Psi_G(t)=sum_C prod_{D in C}(-2 i^{-|D|}) Z_{G-V(C)}(t)`,

where the sum is over vertex-disjoint cycle collections.  A bicyclic cactus
has cycle-packing number at most two.

The cases reduce as follows.

1. If `l` is even, apply the sharp effective-DNN estimate with
   `delta_even=1`.  In square-energy form this is the one-unit improvement
   `s^-(G)<=n+2` over the universal `s^-(G)<=n+3`; since
   `s^+(G)+s^-(G)=2m=2n+2`, it gives `s^+(G)>=n`.  This step is conditional
   here on that effective-DNN lemma: its proof was not present in the local
   research sources audited for this note.  Bipartiteness of the whole graph
   must not be invoked, because the triangle makes `G` nonbipartite.
2. If `l=3`, the graph is a triangular cactus.  The triangular block theorem
   with arbitrary bridges and attached trees gives `s^+(G)>n(G)`.
3. If `l=3 mod 4`, both cycles have Sachs phase `-2i`.  The packing-two phase
   theorem gives `s^+(G)>s^-(G)`.  Since `m=n+1`, this implies
   `s^+(G)>m=n+1`, which is stronger than AKMP.
4. The only remaining length is `l=1 mod 4`, necessarily `l=4k+1>=5`.

The reduction uses only the two cyclic blocks, so it is unaffected by the
length of the connector, a shared cut vertex, or arbitrary acyclic branches.

## Exact Sachs identity in the residual

Put `T=C_3` and `C=C_{4k+1}`.  Their singleton phases are

`q_3=-2i`, `q_{4k+1}=2i`.

The empty-cycle term is real.  If `T` and `C` are disjoint, their two-cycle
term has phase `(-2i)(2i)=4`, also real; if they share a cut vertex, that term
is absent.  Hence, in both configurations,

`Im Psi_G(t)=-2 Z_{G-V(T)}(t)+2 Z_{G-V(C)}(t)`.                 (1)

Thus the proposed route would work if deletion of the triangle always had the
larger signless matching carrier.  It does not.

## Small exact obstruction to carrier domination

Take a figure-eight consisting of `C_3` and `C_5` with common vertex `x`, and
attach one leaf at a triangle vertex different from `x`.  The graph has eight
vertices.  After deleting the triangle, the pendant leaf is isolated and the
four surviving vertices of the pentagon induce `P_4`.  Therefore

`Z_{G-V(C_3)}(t)=t Z_{P_4}(t)=t^5+3t^3+t`.

After deleting the pentagon, the two surviving triangle vertices and the leaf
induce `P_3`, so

`Z_{G-V(C_5)}(t)=Z_{P_3}(t)=t^3+2t`.

Their difference is

`Z_{G-V(C_3)}(t)-Z_{G-V(C_5)}(t)`
`=t^5+2t^3-t=t(t^4+2t^2-1)`.

This is negative for

`0<t<sqrt(sqrt(2)-1)`.

By (1), `Im Psi_G(t)>0` throughout that interval.  In particular, neither the
pointwise matching injection nor the claim that `Psi_G` remains in the lower
half-plane can hold in general.  The obstruction is caused exactly by an
asymmetric rooted tree: deleting the triangle strands its leaf, while deleting
the pentagon leaves a three-vertex path with an additional matching option.

For reference, direct numerical diagonalization of this example gives

`s^+(G)=9.509361818...`, `n=8`,

so it is an obstruction to the proof mechanism, not a counterexample to AKMP.

## Why the obvious repairs do not close the proof

### Matching injections

The two deletion forests do not have a common external forest.  Rooted
attachments on a vertex removed by one cycle and retained by the other alter
both the degree and the low-order matching coefficients.  Cycle size alone
therefore cannot order the carriers coefficientwise or pointwise.

### Induced partition

Separating the two cyclic territories and applying induced-subgraph
superadditivity gives a triangle-unicyclic packet and a connected residual
packet.  The known estimates are, schematically,

`s^+(triangle packet)>|V(packet)|`,

and the universal LTZ/DNN bound

`s^+(residual)>=|V(residual)|-1`.

Their sum is only strictly greater than `n-1`; strictness without a uniform
one-unit margin does not reach `n`.  Such a uniform triangle-packet margin is
not available with arbitrary rooted trees.  When the cycles share a cut
vertex, assigning that vertex to the even/long-cycle packet also breaks the
triangle into an edge and loses exactly the same unit.

### Weighted-core reduction

The exact tree-gluing reduction introduces diagonal penalties on the bicyclic
core.  Existing calculations already show that weighted endpoint inequalities
fail for `C_5` dumbbells and long handcuffs.  Hence a proof for arbitrary trees
cannot simply replace each rooted tree by an independent worst-case diagonal
penalty and appeal to the bare-core theorem.

### Sign of the imaginary part

The sign of `Im Psi_G` is sufficient but not necessary for positive
square-energy asymmetry.  The example above has positive imaginary part near
zero but still has `s^+>s^-`.  Any successful Coulson proof must therefore
control the lifted continuous argument or its weighted integral, rather than
the pointwise sign of (1).

## Precise remaining routes

A proof of the residual would follow from any one of the following genuinely
stronger statements.

1. A mixed-phase integral estimate showing

   `integral_0^infinity t Theta_G(t) dt <= pi/2`,

   because `s^+-s^-=-(4/pi) integral t Theta_G(t)dt` and, for `m=n+1`, AKMP
   is equivalent to `s^+-s^- >= -2`.
2. A one-unit improvement of the LTZ upper bound for the negative square
   energy in this class:

   `s^-(G)<=n+2`.

   The universal DNN theorem gives only `s^-(G)<=n+3`.
3. An induced-packet theorem that couples the triangle surplus to the deficit
   of the `C_{4k+1}` territory, rather than estimating the packets separately.
4. A tree-recursive invariant for the ratio

   `Z_{G-V(C)}(t)/Z_{G-V(T)}(t)`

   strong enough to bound the lifted phase area even though that ratio can
   exceed one on part of the positive axis.

The pointwise carrier-domination route is conclusively ruled out in its stated
form.  The theorem for triangle plus `C_{4k+1}` with arbitrary attachments
remains the sole residual after the listed parity and block reductions.
