# Cycle 197: Appell--Humbert closes the divisor-cube moving ansatz

Cycle 196 writes the denominator-cleared exceptional class on

\[
A_0=E_i^3\times E_i^3
\]

as a signed integral sum of the complete intersections

\[
\Gamma_a=D_{a,1}D_{a,2}D_{a,3},\qquad
D_{a,j}=\{z_{j+3}-az_j=0\}.
\]

Replacing these equations by general effective smooth divisors in the same
line bundles does not improve their PEL-base motion. The obstruction is the
Appell--Humbert class itself and is therefore independent of the chosen
section.

## Full-base Appell--Humbert condition

Let `R` be the Hermitian matrix of an integral divisor class on `A_0`. Write

\[
P=\operatorname {diag}(I_3,Q),\qquad Q=\operatorname {diag}(1,1,3).
\]

The tangent space to the local PEL base is `M_3(C)`, with Beltrami matrix

\[
\mu_B=\begin{pmatrix}0&B\\Q^{-1}B^t&0\end{pmatrix}.
\]

The `(0,2)` part acquired by the Appell--Humbert form of `R` is represented,
up to the fixed harmless scalar convention, by the alternating part of
`mu_B^t R`. Thus the exact infinitesimal Hodge condition is

\[
\boxed{\mu_B^tR=(\mu_B^tR)^t.}
\]

Imposing this for every `B in M_3(C)` gives 35 independent real linear
conditions on the 36-dimensional real space `Herm_6(C)`. Its kernel is

\[
\boxed{\mathbb R P}.
\]

Since `P` is primitive in `Herm_6(Z[i])`, the integral classes that remain of
type `(1,1)` over the full connected PEL germ are exactly

\[
\boxed{\mathbb Z P}.
\]

This also agrees with the generic-endomorphism description: generically the
PEL endomorphism algebra is `Q(i)`, and its Rosati-fixed part is `Q`.

## Consequences for the Cycle 196 divisors

The matrix of `D_(a,j)` has the rank-one block

\[
\begin{pmatrix}N(a)&-\bar a\\-a&1\end{pmatrix}
\]

on coordinates `j,j+3`. It is not a multiple of `P`, so no such class remains
`(1,1)` over all nine PEL directions. A relative effective Cartier divisor in
that fixed line bundle would force its first Chern class to remain `(1,1)`.
Consequently changing the section, taking a smooth member, translating it, or
replacing a multiplicity by a reduced smooth member of the corresponding
power cannot remove the obstruction.

More explicitly, `D_(a,j)` is the pullback of the origin divisor under the
surjective homomorphism `z -> z_(j+3)-a z_j`. A general divisor in
`|mD_(a,j)|` is the disjoint union of `m` smooth translated fibers. Thus the
signed coefficients can indeed be realized without nonreduced divisor
equations (and, after choosing the three point sets generically, by smooth
transverse complete intersections). Their classes are still `m[D_(a,j)]`, so
their Appell--Humbert kernels are unchanged. Smoothness repairs effectivity but
creates no new PEL-base direction.

For all three classes belonging to one scalar graph, the common first-order
condition is the graph condition already computed in Cycle 169,

\[
Q^{-1}B^t-N(a)B=0.
\]

For `a=u^k`, `u=2+i`, its rank for `k=0,...,6` is

\[
(6,9,9,9,9,9,9),
\]

so the common PEL-base dimensions are respectively

\[
(3,0,0,0,0,0,0).
\]

In particular, every nonunit graph triple in the Cycle 196 expansion is
already vertical, and the common base of either signed collection is zero.

## No rank-nine divisor-complete-intersection pair

The failure is not confined to the displayed factorization. If a
codimension-three complete intersection moves over the full PEL germ in three
fixed relative line bundles, each divisor class must be an integral multiple
of `P`. Its class is therefore an integral multiple of `P^3`. Any signed sum
or pair made from such complete intersections also lies in `Z P^3`.

But `P^3` is in the balanced `wedge^3 W tensor wedge^3 Wbar` sector and has
zero Weil projection, whereas `D_0 alpha_0` has nonzero pure determinant
projection. Hence

\[
\boxed{D_0\alpha_0\notin \mathbb Q P^3}
\]

and there is no signed pair of effective smooth divisor complete intersections
representing this class with rank-nine common PEL base. Adding a common ample
class does not help: `R+mP` is Hodge in a direction exactly when `R` is.

This closes only the fixed-line-bundle divisor-complete-intersection repair.
It does not obstruct connected, nonreduced, or rationally equivalent
codimension-three representatives that are not presented by three relative
Cartier divisors, and it does not prove the Hodge conjecture.

Reproduce the exact 36-variable Appell--Humbert rank and the seven graph-triple
ranks with

```sh
python3 millennium-prize/hodge/verify_cycle197_appell_humbert.py
```
