# Cycle 249: exact exceptional-Weil prefilter for F242

## Determinant coordinate

Write each candidate matrix in upper and lower blocks

\[
 L_r=\begin{pmatrix}U_r\\V_r\end{pmatrix},\qquad U_r,V_r\in
 M_3(\mathbb Z[i]),\qquad r=1,2,3,
\]

and denote its columns by `ell_(r,a)`. Cycle 248 gives

\[
 z_L=8\sum_{a,b,c=1}^3
 (\ell_{1,a},\ell_{2,b},\ell_{3,c})_*[E^3].
\]

In the Cycle 151 integral determinant convention, define the Gaussian integer

\[
 \boxed{
 S(L)=\sum_{a,b,c=1}^3
 \det(U_{1,a},U_{2,b},U_{3,c})
 \overline{\det(V_{1,a},V_{2,b},V_{3,c})}.}
 \tag{249.1}
\]

This is an exact bidegree `(3,3)` polynomial in the columns and their Gaussian
conjugates, hence an ordinary integral polynomial in their real and imaginary
parts. For one summand, pullback of

\[
 \Omega_W=dz_1dz_2dz_3\,d\bar z_4d\bar z_5d\bar z_6
\]

is the product of the two determinants in (249.1). This period pairs with the
coefficient on the opposite determinant line. Cycle 151 fixes the normalization
by the diagonal, whose integral coordinate is one and whose normalized
coefficients are `-i/8,+i/8`. Therefore the 27 summands and the leading factor
eight give

\[
 \boxed{
 P_Wz_L=-i\overline{S(L)}\Omega_W+iS(L)\Omega_{\bar W}.}
 \tag{249.2}
\]

In particular, the exact Cycle 152 interpolation projector has no denominator
in this final coordinate formula: it acts as the identity on the two displayed
determinant lines and kills the other five sectors. For the F242 structure
sheaf, conditional on the G0 closed-immersion certificate,
`P_W c_3(O_(Y_L))=2P_Wz_L`, so G1 is equivalent to the single Gaussian test
`S(L) != 0`. Before G0, this is an exact necessary prefilter, not yet a
structure-sheaf G1 certificate.

## Seven finite determinants

Put

\[
 H_r=U_r\overline{V_r}^{\,t}\in M_3(\mathbb Z[i]),\qquad
 F(t_1,t_2,t_3)=\det(t_1H_1+t_2H_2+t_3H_3).
\]

Cauchy--Binet identifies (249.1) with the square-free coefficient
`S(L)=[t_1t_2t_3]F`. Polarization of the homogeneous cubic gives

\[
\boxed{
\begin{aligned}
S(L)={}&\det(H_1+H_2+H_3)
-\det(H_1+H_2)-\det(H_1+H_3)-\det(H_2+H_3)\\
&+\det H_1+\det H_2+\det H_3.
\end{aligned}}
\tag{249.3}
\]

Thus G1 costs seven `3x3` Gaussian determinants, rather than a 924-coordinate
exterior expansion or 27 pairs of determinants.

## Universal-zero decision and prefilter

The polynomial is not universally zero, even after the universal necessary
rank conditions. One sparse norm-one witness is

\[
L_1=\begin{pmatrix}
0&0&0\\-i&0&0\\0&0&i\\i&0&0\\0&0&0\\0&0&-i
\end{pmatrix},\quad
L_2=\begin{pmatrix}
0&0&-1\\0&0&0\\-i&0&1\\0&1&0\\1&0&0\\0&0&i
\end{pmatrix},\quad
L_3=\begin{pmatrix}
0&-1&0\\-1&0&0\\0&1&-1\\1&0&0\\0&1&-1\\0&0&0
\end{pmatrix}.
\]

Exact elimination gives block ranks `(2,3,3)`, total rank
`rank[L_1 L_2 L_3]=6`, and (249.1)--(249.3) give `S(L)=-i != 0`.
The corrected (249.2) therefore gives
`P_Wz_L=Omega_W+Omega_(bar W)`.
This only disproves universal vanishing; it does not certify that the witness
is a closed immersion or passes any deformation gate.

The enumeration order can now be fixed exactly:

1. reject if some `rank(L_r)<2`;
2. reject if `rank[L_1 L_2 L_3]<6`;
3. form the three `H_r` and reject if the seven-determinant value is zero;
4. send only survivors to the difference-scheme, tangent, graph-span, and
   deformation calculations.

The first two failures already preclude a closed immersion, while the third is
exactly `REJECT_WEIL_ZERO`. No modular or floating-point decision is needed.

Reproduce the generic symbolic identity, direct 27-term comparison, sparse
witness, ranks, and reusable prefilter with

```sh
python3 millennium-prize/hodge/verify_cycle249_f242_weil_prefilter.py
```

The script also accepts a candidate or list of candidates over
`{0,1,-1,i,-i}` through `--json`. This closes the F242 exceptional-projector
calculation and supplies a cheap exact candidate filter. The projective
difference scheme, exhaustive enumeration, and deformation gates remain
incomplete; no Hodge result is claimed.
