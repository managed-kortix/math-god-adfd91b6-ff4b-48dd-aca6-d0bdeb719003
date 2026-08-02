# Mordell--Weil certificate over `K=Q(sqrt(-7))`

## Result

Let

\[
 E:\ y^2+y=x^3+x^2,\qquad P=(0,0),\qquad
 K=\mathbf Q(\sqrt{-7}).
\]

The required integral statement is

\[
 E(K)_{\rm tors}=0,\qquad E(K)_{\rm free}=\mathbf ZP.       \tag{1}
\]

Consequently, after the exact CM calculation identifies the normalized
Heegner point with `y_K=P`,

\[
 [E(K)_{\rm free}:\mathbf Zy_K]=1.                         \tag{2}
\]

This is stronger than merely computing `E(Q)`.

## Rank over `K`

The `-7` quadratic twist has global minimal model

\[
 E^{(-7)}:[0,-1,1,-16,-106],
 \quad y^2+y=x^3-x^2-16x-106,
\]

discriminant `-43*7^6=-5058907` and conductor `43*7^2=2107`.
Full multiplication-by-two descent gives

\[
 \dim_{\mathbf F_2}\operatorname {Sel}^{(2)}(E/\mathbf Q)=1,
 \qquad
 \dim_{\mathbf F_2}\operatorname {Sel}^{(2)}(E^{(-7)}/\mathbf Q)=0.
\]

Both curves have trivial rational 2-torsion. The Kummer sequence therefore
gives

\[
 \operatorname {rank}E(\mathbf Q)=1,
 \qquad \operatorname {rank}E^{(-7)}(\mathbf Q)=0.
\]

The rational and anti-rational eigenspaces for the nontrivial element of
`Gal(K/Q)` yield the standard rank identity

\[
 \operatorname {rank}E(K)=
 \operatorname {rank}E(\mathbf Q)+
 \operatorname {rank}E^{(-7)}(\mathbf Q)=1.                \tag{3}
\]

The descent is replayed by two exact implementations. PARI 2.15.4 returns
`ellrank=[0,0,0,[]]` and an empty `ell2cover` basis for the twist. The supplied
Magma script calls `TwoSelmerGroup` on both curves and asserts Selmer orders
`2` and `1`. Retaining a Magma transcript is still required to realize the
claimed independent proof-enabled replay in an environment where Magma is
available.

## Torsion over `K`

At a rational good prime inert in `K`, reduction is into the group over the
quadratic residue field. At a split prime it is into the group over the prime
field. Exact point counts give

\[
 \#E(\mathbf F_2)=5 \quad (2\text{ split}),
\]

and, since `3` is inert and `a_3=-2`,

\[
 \#E(\mathbf F_9)=(3+1)^2-a_3^2=12.
\]

Good reduction is injective on torsion prime to the residue characteristic.
Reduction at `2` therefore shows that the odd-order torsion has order dividing
`5`; reduction at `3` then eliminates its possible `5`-primary part. For the
remaining `2`-primary part, the irreducible rational 2-division cubic remains
irreducible over the quadratic field `K` (a root has degree three and cannot
lie in a quadratic extension), so `E(K)[2]=0`. Every nonzero finite
2-primary group contains an element of order two. Thus

\[
 E(K)_{\rm tors}=0.                                      \tag{4}
\]

This proves the torsion claim without a database or a number-field torsion
routine. The Magma computation over `K` is an independent check.

## Integral saturation and primitivity

Equation (3) and the inclusion `P in E(Q) subset E(K)` do not alone prove
(1): an odd-index overgroup could exist. Here the twist and torsion results
reduce the integral question over `K` exactly to rational saturation. For any
`Q in E(K)`, the point

\[
 Q-\sigma Q
\]

is anti-invariant. Under the quadratic-twist isomorphism, the anti-invariant
subgroup is `E^(-7)(Q)`. It has rank zero, so `Q-sigma Q` is torsion. But (4)
says `E(K)` has no torsion. Hence `Q=sigma Q` and therefore

\[
 E(K)=E(\mathbf Q).                                      \tag{5}
\]

Eclib's full multiplication-by-two descent and saturation, run at 1000-bit
precision, reports the generator `[0:-1:1]=-P`, says that the points were
already saturated, and terminates with “The rank and full Mordell-Weil basis
have been determined unconditionally.” Thus

\[
 E(\mathbf Q)=\mathbf ZP.
\]

Together with (5), this proves (1) and saturates `P` at every prime. This is
not an inference from the rank alone: the final saturation is an integral
Mordell--Weil computation.

As an independent optional check, `verify_43a1_K.m` asks Magma's
`MordellWeilGroup(EK)` for the full number-field group and asserts

\[
 E(K)\simeq\mathbf Z,
\]

and asserts that the image of its abstract generator is exactly `P` or `-P`.
This directly certifies saturation at every prime and proves (1). It separately
checks the analogous rational computation, so the conclusion is not inferred
from `E(Q)` alone.

## Reproduction and trust boundary

Run

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1_K.gp
printf '0 1 1 0 0\n' | mwrank -v 2 -p 1000
magma millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1_K.m
```

The successful local outputs are retained as `output-K.txt` and
`output-mwrank-saturation.txt`.

The GP script provides the locally runnable exact twist descent and torsion
point-count certificate. Eclib supplies the unconditional rational
Mordell--Weil basis and saturation. Equations (4)--(5) then transfer the exact
integral equality to `K`; no number-field saturation oracle is logically
needed. The Magma script is an independent proof-enabled replay of both
descents and a direct number-field Mordell--Weil cross-check.

In the present environment PARI and eclib were run successfully; Magma is not
installed, so no Magma transcript is claimed. The proved result is relative to
the standard exact PARI/eclib descent and saturation implementations. A
kernel-independent proof would have to expand their class-group, local-solubility,
height-bound, and saturation algorithms into separately checkable primitive
certificates. This is a software trust boundary, not a remaining mathematical
index gap.
