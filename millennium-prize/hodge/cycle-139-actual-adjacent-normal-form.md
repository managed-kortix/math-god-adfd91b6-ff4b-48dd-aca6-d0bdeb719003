# Cycle 139: actual adjacent Fermat normal form and its Witt carry

The abstract adjacent normal form of Cycle 138 can be specialized exactly to
the Cycle 122 alpha-visible Hermitian plane and a preferred adjacent neighbor.
The characteristic-two Fermat polynomial becomes exceptionally sparse, but its
coefficientwise Teichmüller lift is **not** the transformed standard Fermat
`W_2` model.  A nonzero 76-term Witt carry must be retained in every cone
obstruction calculation.

For

\[
z=(1,t+1,t)^t,\qquad Az=(0,1,1)^t,
\]

an explicit invertible linear coordinate change

\[
(x_0,x_1,x_2,y_0,y_1,y_2)
\longmapsto(z_0,z_1,p,q,r,s)
\]

has determinant

\[
\det T=t\ne0.
\]

It sends the two adjacent graph planes to

\[
L_A=V(q,r,s),\qquad L_B=V(p,r,s).
\]

In these coordinates, the characteristic-two standard Fermat equation is

\[
\boxed{
F=pqA_{31}+rB_{32}+sC_{32},
}
\]

where

\[
A_{31}=p^{31}+q^{31},
\]

\[
\begin{aligned}
B_{32}={}&r^{32}
+\beta(z_0+p+q)r^{31}+\gamma z_1r^{31}\\
&+\beta(z_0^{32}+p^{32}+q^{32})+\gamma z_1^{32},
\end{aligned}
\]

\[
\begin{aligned}
C_{32}={}&s^{32}+(z_0+tp+(t+1)q)s^{31}\\
&+z_0^{32}+tp^{32}+(t+1)q^{32},
\end{aligned}
\]

with

\[
\beta=t^4+t+1,\qquad\gamma=t^4+t.
\]

The supports of `A31,B32,C32` have sizes `2,9,7`; the complete transformed
polynomial has 18 terms.  The verifier checks the coordinate map, its inverse,
both plane ideals, and this identity coefficientwise over `F_32`.

## Mixed-characteristic warning

Let `G` denote the fixed standard Fermat polynomial over `W_2(F_32)`.  In the
new coordinates the correct target is

\[
G_T(u)=G(\widetilde T^{-1}u),
\]

where `widetilde T^{-1}` is computed using genuine Witt arithmetic.  It is not
obtained by merely Teichmüller-lifting the 18 coefficients of
`pqA31+rB32+sC32`.

Exact computation finds a nonzero pure carry between these two lifts:

```text
support = 76
SHA-256 = 883504597c5e7284aa84d9742da8c651fc259d6f0abf088d6dca86a38633b69b
```

Thus a cone that squares to the multiplicatively lifted sparse normal-form
potential need not lift to the fixed standard Fermat model.  The scalar carry
is part of

\[
\Omega=\frac{\widetilde D^2-G_T I}{2}\bmod2
\]

and cannot be discarded unless it is proved to be a boundary in the complete
cone endomorphism complex.

The obstruction class is independent of the chosen lift of `D` for a fixed
target potential, modulo endomorphism boundaries.  Replacing the potential by
an unrelated lift changes the class by the corresponding scalar endomorphism;
there is no arbitrary potential-lift invariance.

This cycle supplies the exact missing geometric input for the 33 adjacent-cone
gate.  It does not decide cone liftability: unrestricted lower-left first-order
corrections can alter diagonal defects, so separate nonliftability of the two
components is not by itself a proof that every cone is obstructed.  The next
step is the contracted full endomorphism calculation including this 76-term
carry.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle139_actual_adjacent_normal_form.py
```

No Hodge or Millennium solution is claimed.
