# Cycle 203: first Ferrand doubles have empty rank-zero locus

## Bounded parameter space

Let

\[
 A_0=E_i^3\times E_i^3,\qquad G_M=\Gamma_M\simeq E_i^3,
 \qquad M=I\ \hbox{or}\ D=\operatorname {diag}(3,1,1).
\]

Both graphs are regular embeddings of codimension three and

\[
 N^*_{G_M/A_0}\simeq O_{G_M}^{\oplus3}.
\]

A first Ferrand double supported on `G_M` is specified by a locally free
quotient

\[
 q:N^*_{G_M/A_0}\twoheadrightarrow L                         \tag{203.1}
\]

with `L` a line bundle. If `I_M` is the graph ideal, its ideal is

\[
 J_q=\ker(I_M\longrightarrow I_M/I_M^2\xrightarrow q L),     \tag{203.2}
\]

and it has the square-zero sequence

\[
 0\longrightarrow L\longrightarrow O_{Z_q}
 \longrightarrow O_{G_M}\longrightarrow0.                   \tag{203.3}
\]

For a fixed Hilbert polynomial `P_L`, all such quotients form the locally-free
open

\[
 \mathcal Q_{M,P_L}\subset
 \operatorname {Quot}_{G_M}(O_{G_M}^{\oplus3},P_L).           \tag{203.4}
\]

This is the required bounded parameter space. Allowing every Hilbert polynomial
gives a countable disjoint union, not one finite-type parameter scheme. There
is no additional embedded extension parameter after (203.1): (203.2) uniquely
determines the Ferrand algebra. In abstract ribbon language the extension class
lies in `Ext^1(Omega_G,L)`, but the class induced here is the pushout of the
conormal sequence. That sequence splits for a graph of a homomorphism between
abelian varieties, so the induced abstract class is zero. Adding an arbitrary
class in `Ext^1(Omega_G,L)` would parameterize abstract ribbons not necessarily
embedded as first Ferrand doubles in `A_0`.

## Universal local equations

Trivialize `L` and use normal equations `z_1,z_2,z_3`. On the quotient chart
where `q(z_r)=1`, write

\[
 q(z_j)=a_j\quad(j\ne r).
\]

Then the double is the complete intersection

\[
 J_q=(z_j-a_jz_r\ (j\ne r),\ z_r^2).                          \tag{203.5}
\]

If `s=(s_1,s_2,s_3)^t` is the reduced normal Kodaira--Spencer value, direct
differentiation of (203.5) gives the exact normal obstruction

\[
 A_r(a)s=\bigl(s_j-a_js_r\ (j\ne r),\ 2\epsilon s_r\bigr)^t, \tag{203.6}
\]

where `epsilon` is the nilpotent generator. After identifying the last target
line with its free rank-one coefficient, `A_r(a)` is a `3 by 3` matrix with

\[
 \det A_r(a)=\pm2.                                             \tag{203.7}
\]

Thus `A_r(a)` is invertible over every characteristic-zero quotient chart. This
is the first-double specialization of the curvilinear formula
`(m epsilon^(m-1)s_1,s_2,s_3)` from Cycle 202.

## Exact Atiyah obstruction matrix

Use row-major coordinates for `B=(b_ij) in T_0S=M_3(C)` and for the target.
Put `Q=diag(1,1,3)`. The graph part of the Atiyah/embedded obstruction is

\[
 R_M(B)=Q^{-1}B^t-MB.                                         \tag{203.8}
\]

On the chart above, the exact canonical graph-normal quotient of the first-
double Atiyah matrix is

\[
 \boxed{\mathcal O_{M,r}(a)=(A_r(a)\otimes I_3)R_M},          \tag{203.9}
\]

where `A_r` acts on the three normal rows and `I_3` records the three
`H^1(O_G)` directions. Formula (203.9) is obtained by applying (203.6) to each
cohomology direction. For a fixed Hilbert polynomial, a local presentation of
the universal Quot complex writes the full matrix in the structural form

\[
 \operatorname {At}_{M,r,P}(a,e)=
 \begin{pmatrix}(A_r(a)\otimes I_3)R_M\\
                 \Psi_{M,r,P}(a,e)
 \end{pmatrix}.                                                \tag{203.9a}
\]

Here `e` denotes universal quotient/extension coordinates and `Psi` is the
trace-free obstruction to deforming that quotient. Its size and entries depend
on `P_L` and on a chosen locally free resolution of the universal quotient;
there is no single finite matrix over the countable union of Hilbert
polynomials. This is why fixing the bounded campaign is essential. Crucially,
`Psi` can add target rows but cannot remove the displayed canonical block.
Equivalently, the semiregularity quotient contains `2R_M`; hence the elimination
below is uniform and does not require calculating `Psi`.

Since (203.7) is a unit, the exact ranks of the forced block are independent of
all quotient parameters:

\[
 \operatorname {rank}\mathcal O_{I,r}=6,\qquad
 \operatorname {rank}\mathcal O_{D,r}=8.                     \tag{203.10}
\]

Their kernels are respectively

\[
 \ker R_I=
 \left\{\begin{pmatrix}x&y&0\\y&z&0\\0&0&0\end{pmatrix}\right\},
 \qquad
 \ker R_D=
 \left\{\begin{pmatrix}0&0&0\\0&z&0\\0&0&0\end{pmatrix}\right\}.
                                                                    \tag{203.11}
\]

For a pair of doubles, stacking the two forced blocks gives rank eight and the
one-dimensional common kernel shown on the right of (203.11). The full Atiyah
rank is therefore at least `6`, `8`, and `8` respectively; quotient obstruction
rows can shrink these kernels but cannot enlarge them.

## Rank-zero elimination

On each standard chart, let `I_(M,r)` be the ideal generated by all entries of
`mathcal O_(M,r)(a)`. Multiplication by `adj(A_r)` and (203.7) imply

\[
 I_{M,r}\supseteq (\hbox{entries of }2R_M).
\]

The latter list contains a nonzero rational constant: for `M=I`, the
coefficient of `b_10` in `(R_I)_01` is `1`; for `M=D`, the coefficient of
`b_00` in `(R_D)_00` is `-2`. Therefore

\[
 I_{I,r}=I_{D,r}=(1)                                          \tag{203.12}
\]

after elimination to the quotient parameters. The three local quotient charts
cover the universal quotient over the graph, so

\[
 \boxed{V(\operatorname {rank}\mathcal O_M=0)=\varnothing}
\]

for either graph, and also for their paired parameter space. This is stronger
than the Cycle 202 traced obstruction for arbitrary thickenings: for first
Ferrand doubles the universal local normal matrix itself is invertible over the
reduced graph obstruction.

Thus first doubles do not pass the rank-zero gate, regardless of conormal line
quotient or bounded Hilbert polynomial. The surviving one-dimensional direction
for the pair is not rank zero and cannot dominate the nine-dimensional PEL
base. No Hodge-conjecture result is claimed.

Reproduce the exact forced matrices, ranks, chart determinants, and elimination
certificate with

```sh
python3 millennium-prize/hodge/verify_cycle203_ferrand_doubles.py
```
