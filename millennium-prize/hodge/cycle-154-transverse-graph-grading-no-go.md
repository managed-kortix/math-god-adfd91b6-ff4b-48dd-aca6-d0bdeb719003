# Cycle 154: grading closes all transverse-graph return paths

Let `F_a,F_b` be structure sheaves of two distinct transverse codimension-three
graphs in the Cycle 151 sixfold. Their cross Ext groups are concentrated in
degree three:

\[
\operatorname{Ext}^r(F_a,F_b)=0\ (r\ne3),
\qquad
\operatorname{Ext}^3(F_a,F_b)\simeq H^0(\Gamma_a\cap\Gamma_b,O).
\]

For shifts `F_a[r],F_b[s]`, opposite cross classes have total degrees

\[
3+r-s,\qquad3+s-r.
\]

Their sum is always six. A bidirectional Maurer--Cartan differential would
require both to have degree one, whose sum is two. Therefore

\[
\boxed{\text{opposite degree-one cross arrows cannot coexist}.}
\]

Their return product lies in top self-Ext degree six, not in self-Ext degree two
containing the PEL/Atiyah obstruction. Longer cycles do not help: shifts
 telescope around a closed path. In a minimal `A_infinity` model, an all-cross
`m_k` operation has output degree `2k+2`; for `k>=2` it never lands in self
degree two. Homotopy-transfer degrees are already included in this formula.

This closes every twisted complex whose vertices are shifts of pairwise
transverse graph sheaves and whose return mechanism uses cross-`Ext^3` classes.
The first viable escape must use nontransverse clean intersections with lower-
degree cross Ext, or a genuinely non-graph connected object.

A concrete candidate is the four-graph staircase

\[
Z_0=\Gamma_{M_0}\cup\Gamma_{M_1}\cup\Gamma_{M_2}\cup\Gamma_{M_3},
\]

where

\[
M_0=\operatorname{diag}(1,1,1),\quad
M_1=\operatorname{diag}(2,1,1),\quad
M_2=\operatorname{diag}(2,2,1),\quad
M_3=\operatorname{diag}(2,2,2).
\]

Its components intersect in positive dimensions and its exceptional coefficient
is `1+2+4+8=15` times the diagonal seed. Near the common origin, with
`a_j=y_j-2x_j`, `b_j=y_j-x_j`, its reduced ideal is the `2x2` minors of

\[
\begin{pmatrix}a_1&a_2&a_3&0\\0&b_1&b_2&b_3\end{pmatrix}.
\]

Unlike two transverse three-planes, it has an explicit local determinantal
smoothing obtained by replacing the two zero corner entries by a parameter
`t`. The nearby local rank-one locus is smooth of dimension three.

This local smoothing is not yet a global cycle deformation. Globalization must
preserve the nonzero exceptional class and produce base tangents beyond the
extra-endomorphism locus. A generic Thom--Porteous construction from deformable
divisor-generated bundles would fall into the balanced sector and lose the
Weil coefficient. The next gate is the global Eagon--Northcott
deformation/obstruction map of this exact staircase union.

This is a grading no-go for the transverse graph category and a precise
nontransverse replacement candidate, not a generic Hodge theorem.
