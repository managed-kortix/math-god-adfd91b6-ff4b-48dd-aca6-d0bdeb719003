# Cycle 205: effective coordinate weights cannot isolate a nonhorizontal Pfaffian cubic

## Exact clean target

Continue Cycle 204 in the free three-direction weight model. Write

\[
 N_i=a_iX+b_iY+c_iZ,\qquad a_i,b_i,c_i\in\mathbb Z_{\geq0},
\]

with `2T=sum_i N_i`, and require all ten alternating-matrix entry classes

\[
                       T-N_i-N_j                              \tag{205.1}
\]

to have nonnegative coordinates. The clean cancellation target is the complete
identity

\[
                         C(N)=kXYZ,\qquad k\ne0,               \tag{205.2}
\]

not merely a match of the `XYZ` coefficient. Thus all pure cubes and all six
pair-mixed cubics must vanish. Requiring every generator and every entry class
to be nonzero can only shrink this feasible set.

## One-coordinate zero classification

Consider one coordinate vector `a=(a_1,...,a_5)`. Permute its entries and write

\[
\begin{aligned}
a_1&=x,&a_2&=x+p,&a_3&=x+p+q,\\
a_4&=x+p+q+r,&a_5&=x+p+q+r+z,
\end{aligned}
\]

where all variables are nonnegative. Effectivity of (205.1) is equivalent to
the strongest pair inequality `a_4+a_5<=t`, where `2t=sum_i a_i`. Together
with parity this gives

\[
                         x=q+2r+z+2u,
                         \qquad u\in\mathbb Z_{\geq0}.          \tag{205.3}
\]

Substitution in the scalar center coefficient

\[
 c(a)={\sum_i a_i^3-\sum_i(t-a_i)^3+t^3\over6}
\]

gives the following polynomial:

\[
\begin{aligned}
c(a)={}&p^2q+2p^2r+p^2z+2p^2u
 +3pq^2+10pqr+5pqz+9pqu\\
&+8pr^2+8prz+14pru+2pz^2+7pzu+6pu^2\\
&+2q^3+10q^2r+5q^2z+9q^2u
 +16qr^2+16qrz+28qru\\
&+4qz^2+14qzu+12qu^2+8r^3+12r^2z+21r^2u\\
&+6rz^2+21rzu+18ru^2+z^3+5z^2u+9zu^2+5u^3. \tag{205.4}
\end{aligned}
\]

Every displayed coefficient is positive. Hence `c(a)=0` forces
`q=r=z=u=0`, while `p` is free. Undoing the permutation proves the exact
classification

\[
 \boxed{c(a)=0\quad\Longleftrightarrow\quad
 a=\lambda U_m,\quad U_m=(1,\ldots,1)-e_m}                     \tag{205.5}
\]

for some `lambda>=0` and one of the five missing-coordinate indices `m`.

## Contamination certificate

Let `[X^2Y]C` denote the indicated coefficient. Direct polarization of the
center cubic gives, for nonnegative `lambda,mu`,

\[
 [X^2Y]C(\lambda U_m,\mu U_n)=
 \begin{cases}
 0,&m=n,\\
 \lambda^2\mu,&m\ne n,
 \end{cases}                                                    \tag{205.6}
\]

and the reversed pair has coefficient `lambda mu^2`. If any one of the three
coordinate vectors is zero, trilinearity already forces the `XYZ` coefficient
to vanish. Therefore a putative target has three nonzero coordinate vectors,
and two nonzero coordinate directions with no pair-mixed contamination must use the same ray
`U_m`. Applying this to all three pairs in (205.2) puts the `X`, `Y`, and `Z`
weight vectors on one common ray. But

\[
                  [XYZ]C(\lambda U_m,\mu U_m,\nu U_m)=0.        \tag{205.7}
\]

This contradicts `k!=0`.

Thus there is no smallest candidate: no integral coordinatewise effective
`5 x 5` weighted Pfaffian system has a clean center cubic `kXYZ` for any
nonzero `k`. In particular neither the identity-graph target `k=1` nor the
diagonal-graph target `k=3` is possible. This is an unbounded arithmetic no-go,
stronger than the Cycle 204 total-14 contaminated near miss.

The scope is the declared free nonnegative coordinate cone. Relations among
actual effective divisor classes, or classes outside a simplicial nef cone,
can invalidate coefficientwise effectivity and are not excluded. No Hodge-
conjecture result is claimed.

Reproduce the polarization formulas and an independent exhaustive check through
coordinate total `30` with

```sh
python3 millennium-prize/hodge/verify_cycle205_clean_weighted_pfaffian.py
```
