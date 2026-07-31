# Cycle 184: exact semidirect Kummer conjugacy criterion

Cycle 141 used the projective localization row as the intrinsic Frobenius
datum above a nonidentity-unipotent residual Frobenius. This cycle proves the
exact group statement and applies it to the two certified rows for `433a1`.

## General semidirect-product theorem

Let `H` act linearly on an abelian group `M`, and write

\[
G=M\rtimes H,
\qquad (m,A)(n,B)=(m+An,AB).
\]

For `(m,A),(m',A')` in `G`, the following are equivalent:

\[
\boxed{
(m,A)\sim_G(m',A')
\iff
\text{there is }B\in H\text{ such that }
A'=BAB^{-1},\quad
m'\equiv Bm\pmod{(I-A')M}.}
\tag{1}
\]

Indeed, direct multiplication gives

\[
(n,B)(m,A)(n,B)^{-1}
=\bigl(Bm+(I-BAB^{-1})n,\,BAB^{-1}\bigr).
\tag{2}
\]

Thus (2) proves necessity in (1), and the congruence in (1) supplies an `n`
which proves sufficiency. In particular, over a fixed `A`, conjugacy classes
are exactly the orbits

\[
\boxed{
C_H(A)\backslash M/(I-A)M.}
\tag{3}
\]

The left action in (3) is well defined because every element of `C_H(A)`
preserves `(I-A)M`. Formula (1), rather than equality of chosen coordinates,
is the exact criterion when the linear parts are merely conjugate.

## Two-point Kummer specialization

Let `k=F_p`, let `V=k^2`, and take

\[
M=V\oplus V,\qquad H=\operatorname{GL}(V),
\]

with diagonal `H`-action. Let `A` be a nonidentity unipotent. Put `N=A-I`.
Then `N!=0`, `N^2=0`, and `rank(N)=1`, so

\[
C_A=V/NV
\]

is a line and

\[
M/(I-A)M\simeq C_A^2.
\]

After conjugating `A` to `J=[[1,1],[0,1]]`, its centralizer is

\[
C_H(J)=
\left\{
\begin{pmatrix}a&b\\0&a\end{pmatrix}:
a\in k^\times,\ b\in k
\right\}.
\]

Its action on `V/(J-I)V` is multiplication by `a`. Consequently the
centralizer orbits on `C_A^2` are exactly

\[
(0,0)
\quad\text{and}\quad
[x:y]\in\mathbf P^1(k).
\tag{4}
\]

Combining (1) and (4) gives the precise Kummer criterion. For two elements
whose linear parts are nonidentity unipotents, choose any linear conjugacy
between those parts and transport one localization row to the other quotient.
They are conjugate in `(V^2) semidirect GL(V)` if and only if both rows vanish,
or both are nonzero and have the same projective direction. Changing the
linear conjugacy composes with a centralizer element and therefore only rescales
the transported row; the criterion is independent of every choice.

Changing the chosen division-point lifts changes the affine coordinates by an
element of `(I-A)M`, so it creates no invariant beyond (3).  Changing a basis of
the one-dimensional local quotient rescales both entries together.  It does
not permit independent rescaling of the `P` and `Q` coordinates or interchange
of their ordered labels.  Therefore numerical localization rows computed in
unrelated bases must be compared projectively through explicit transport maps,
not entry by entry.

Equivalently, for nonzero rows `r,s in k^2`,

\[
(r,A)\sim(s,A')\iff \det(r,s)=0,
\tag{5}
\]

provided `A,A'` are nonidentity unipotents and the rows are compared after a
linear conjugacy. The nonzero qualification matters: a zero row and a nonzero
row also have determinant zero but are not conjugate.

## Application to the certified rows

For `E=433a1`, `p=7`, `P=(0,1)`, and `Q=(-1,1)`, Cycle 136 gives

\[
r_{29}=(1,5),\qquad r_{113}=(1,4).
\]

Both auxiliary primes have nonidentity-unipotent linear Frobenius. Indeed,
`q=1 mod 7` and `a_q=2 mod 7`, so the residual characteristic polynomial is
`(X-1)^2`; but `#E(F_29)=28` and `#E(F_113)=112` are not divisible by `49`, so
Frobenius cannot act as the identity on all of `E[7]`. The projective rows are
distinct because

\[
\det\begin{pmatrix}1&5\\1&4\end{pmatrix}
=4-5=-1=6\ne0\pmod 7.
\]

Therefore

\[
\boxed{
\operatorname{Frob}_{29}\not\sim
\operatorname{Frob}_{113}
\quad\text{in}
(E[7]\oplus E[7])\rtimes\operatorname{GL}_2(\mathbf F_7).}
\]

Thus `29` and `113` cannot be used as a same-Frobenius pair in the fixed
two-point Kummer field `L_0`. Their distinct projective localization rows are
exactly what separates their full Kummer conjugacy classes, while their
invertible two-row matrix is what makes the Cycle 136 localization determinant
nonzero. This is a finite-group classification and a screening criterion for
the Cycle 183 collision search; it proves no twist-symbol collision and no BSD
case.

This conclusion assumes that the actual Galois group is identified with the
maximal semidirect product above.  If the translation kernel or the image of
`GL(V)` is smaller, conjugacy must instead be computed in that actual subgroup;
maximality is a certificate hypothesis, not a formal consequence of the
localization row.

Reproduce the finite-group checks with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle184_kummer_conjugacy.py
```
