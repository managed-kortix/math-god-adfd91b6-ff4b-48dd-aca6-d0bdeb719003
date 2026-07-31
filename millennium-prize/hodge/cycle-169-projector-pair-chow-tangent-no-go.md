# Cycle 169: the explicit projector pair has zero PEL tangent image

Cycle 168 left one concrete fixed-degree candidate: clear the coefficients of
the Cycle 152 Weil projector and represent the resulting signed class by an
effective positive/negative pair.  The obvious graph expansion is even more
rigid than the original diagonal.  Each side contains a graph whose embedded
obstruction is injective on the nine-dimensional PEL tangent, so the pair has
zero relative base tangent.

## Exact effective pair

For `u=2+i`, put

\[
D_0=930187500000000000.
\]

Expanding the interpolation polynomial gives

\[
D_0q(t)=\sum_{k=0}^6c_kt^k
\]

with

\[
(c_0,\ldots,c_6)=
(317131927490234375,-2073948378906250,12564289203125,
-56707735500,27598945,3626326,-68381).
\]

Let `Gamma_k` be the transformed diagonal associated with `u^k`.  Then

\[
\begin{aligned}
C_0^+={}&317131927490234375\Gamma_0
+12564289203125\Gamma_2\\
&+27598945\Gamma_4+3626326\Gamma_5,\\
C_0^-={}&2073948378906250\Gamma_1
+56707735500\Gamma_3+68381\Gamma_6,
\end{aligned}
\]

and

\[
\boxed{D_0\alpha_0=C_0^+-C_0^-.}
\]

## Componentwise obstruction

For a scalar Gaussian graph associated with `a`, the exact embedded
obstruction on the PEL tangent `B in M_3(C)` is

\[
\rho_a(B)=Q^{-1}B^t-N(a)B,
\qquad Q=\operatorname{diag}(1,1,3).
\]

Since `N(u^k)=5^k`, write

\[
\rho_k(B)=Q^{-1}B^t-5^kB.
\]

For `k=0`, this map has rank six and a three-dimensional kernel.  For every
`k=1,...,6`, it has rank nine and is injective.  Indeed its coordinate
equations have diagonal coefficients `1/Q_i-5^k` and paired off-diagonal
determinants `1/(Q_iQ_j)-5^(2k)`, all nonzero when `k>0`.

The obstruction of an effective union lies in the direct sum of the component
obstruction spaces.  Multiplicities and translations do not change its kernel.
Therefore

\[
\rho_+=(\rho_0,\rho_2,\rho_4,\rho_5),
\qquad
\rho_-=(\rho_1,\rho_3,\rho_6)
\]

are both injective, as is their direct sum.  Consequently

\[
\boxed{
\operatorname{im}\left(T_{(C_0^+,C_0^-)}\operatorname{Chow}_{/S}
\longrightarrow T_0S\right)=0.
}
\]

Thus the explicit fixed-degree pair is vertical to first order in the full
nine-dimensional Weil base.

More generally, for unions of scalar Gaussian graphs and translates, a
unit-norm graph contributes at most the three-dimensional kernel of `rho_0`,
while any nonunit graph makes the common kernel zero.  Hence the exact base-
tangent ceiling in this model is three, never nine.

## Why cohomological cancellation does not help

The signed total Weil class is horizontal, so the semiregularity images of the
component obstructions cancel after mapping to cohomology.  The effective pair,
however, is parametrized by a product of Chow spaces.  Its obstruction lies in
the direct sum of the component obstruction spaces, where signs do not cancel.
Semiregularity cancellation is necessary for some rationally equivalent
representative to move, but it does not deform these supports or construct the
required rational equivalence.

A viable fixed-degree germ must therefore use a genuinely different connected,
nonreduced, or rationally equivalent representative whose relative Chow tangent
surjects onto the PEL tangent and whose higher obstructions vanish.  Graphs,
their multiplicities, and their translations cannot do this.

No generic algebraicity or Hodge-conjecture result is claimed.
