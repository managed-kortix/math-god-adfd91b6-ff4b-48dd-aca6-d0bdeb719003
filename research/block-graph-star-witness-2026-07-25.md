# Block graphs: quantitative clique-star witness

## Target and outcome

For a block graph `G`, choose a center in every clique block, retain the
corresponding stars, and call the resulting spanning tree `T`.  If `F` is the
set of deleted clique edges, the witness in
`tree-equality-square-energy/paper.tex` gives

\[
s^+(G)\ge n-1+4S(T,F),\qquad
S(T,F)=\sum_{uv\in F}(A(T)_+)_{uv}.
\]

The proposed quantitative statement

\[
\max_{\text{clique-star choices}}S(T,F)\ge \frac14
\]

for cyclomatic number at least two is **false**.  Its infimum over block
graphs is zero, even for a fixed two-triangle core with pendant leaves.
Consequently this unscaled witness cannot prove `s^+(G)>=n` for all block
graphs.

## Exact Schur-resolvent formula

Let siblings `u,v` have common neighbor `r` in a tree `T`, choose the
bipartition with `u,v` in `L`, and put `Q=XX^T`.  Orient the incidence tree
away from the neighborhood node `r`.  For an oriented variable-to-neighborhood
edge and neighborhood-to-variable edge define recursively

\[
d_{x\to s}(a)=a+\sum_{t\in N_T(x)\setminus\{s\}}\rho_{t\to x}(a),
\]

\[
\rho_{s\to x}(a)=
\left(1+\sum_{y\in N_T(s)\setminus\{x\}}d_{y\to s}(a)^{-1}\right)^{-1}.
\]

At the root put

\[
d_x(a)=a+\sum_{s\in N_T(x)\setminus\{r\}}\rho_{s\to x}(a)
\quad (x\in N_T(r)).
\]

Successive Schur complementation and Sherman--Morrison then give the exact
entry

\[
(A(T)_+)_{uv}=\frac1{2\pi}\int_0^\infty
\frac{a^{1/2}\,d_u(a)^{-1}d_v(a)^{-1}}
{1+\sum_{x\in N_T(r)}d_x(a)^{-1}}\,da.                 \tag{1}
\]

Equivalently, the denominator of the integrand after clearing
`d_u d_v` is

\[
d_ud_v+d_u+d_v+\sum_{x\in N_T(r)\setminus\{u,v\}}\frac{d_ud_v}{d_x}. \tag{2}
\]

This is the useful blockwise optimization formula: changing a clique center
changes only the rooted branch responses entering the relevant `d_x`.

## Explicit degree and branch bounds

If a child neighborhood `s` has `c_s` child variables, then `d>=a` in every
descendant branch, so

\[
\frac{a}{a+c_s}\le \rho_{s\to x}(a)\le1.              \tag{3}
\]

Thus, writing `b_x=deg_T(x)-1` and

\[
L_x(a)=a+\sum_{s\in N_T(x)\setminus\{r\}}\frac{a}{a+c_s},
\qquad U_x(a)=a+b_x,
\]

we have `L_x<=d_x<=U_x`.  Equations (1)--(2) yield the completely explicit
lower bound

\[
(A(T)_+)_{uv}\ge\frac1{2\pi}\int_0^\infty
\frac{a^{1/2}\,da}
{U_uU_v+U_u+U_v+
 U_uU_v\sum_{x\in N_T(r)\setminus\{u,v\}}L_x^{-1}}.   \tag{4}
\]

Keeping (3) recursively instead of replacing all descendant `d` values by
`a` gives successively sharper bounds involving the complete rooted branch
sizes.  Formula (4) also explains the obstruction: a large pendant star makes
one or more `U_x` grow with its degree, and sibling correlations can decay on
the inverse-square-root scale.

## Clean asymptotic counterfamily

Let `G_L` consist of two triangles sharing a vertex `x`, together with `L`
pendant leaves at `x`.  It has

\[
n=L+5,\qquad m=L+6=n+1,
\]

so its cyclomatic number is exactly two.  Allowing the center of each triangle
to be chosen independently is a relaxation of the choices obtainable from a
single root, and there are only nine such choices.  Up to symmetry they fall
into three classes.  Put

\[
D=\sqrt{L+4+2\sqrt{L+2}}.
\]

The corresponding sums are

\[
S_{xx}=\frac1{\sqrt{L+4}},\qquad
S_{xo}=\frac{2+(L+2)^{-1/2}}{2D},\qquad
S_{oo}=\frac1{\sqrt{L+3+2\sqrt L}}.                    \tag{5}
\]

For example, in the mixed case the relevant side of `XX^T` is

\[
Q=\begin{pmatrix}L+3&1\\1&1\end{pmatrix},
\quad
Q^{1/2}=\frac{Q+\sqrt{L+2}\,I}{D},
\quad
Q^{-1/2}=\frac{I+\sqrt{L+2}\,Q^{-1}}D.
\]

The two deleted entries sum to
`((Q^(1/2))_12+(Q^(-1/2))_11)/2`, which is `S_xo`.
For two outer centers, symmetry reduces `Q` to
`[[L+2,sqrt(2)],[sqrt(2),1]]` plus a scalar eigenvalue `1`, giving
`S_oo`.  Elementary squaring shows `S_xo<=S_xx` and `S_oo<=S_xx` for
`L>=1`.  Therefore

\[
\max S(T,F)=\frac1{\sqrt{L+4}}.                         \tag{6}
\]

The maximizing choice centers both triangles at `x`; then `T=K_{1,L+4}` and
each of the two deleted edges has positive-part entry
`1/(2 sqrt(L+4))`.  Hence

\[
\inf_{\beta(G)\ge2}\max S(T,F)=0,
\qquad \max S(T,F)\sim L^{-1/2}.
\]

In this family the desired `1/4` bound already fails at `L=13` (`n=18`).
The variational lower bound itself is only

\[
s^+(G_L)\ge n-1+\frac4{\sqrt{L+4}},
\]

which falls below `n` for `L>12`.

An even stronger structured obstruction attaches `p` leaves to each of the
four non-shared triangle vertices and `h` leaves to `x`.  Every one of the
nine choices tends to zero as the pendant multiplicities grow.  This family
also supplies the smallest failures found by exhaustive enumeration.

## Exhaustive block-graph test through order 14

`positive-square-energy/experiments/block_star_witness.py` recursively
generates rooted block-cut trees, canonically deduplicates their unrooted
colored incidence trees, tests every clique-center choice, and diagonalizes
the resulting tree.  Testing independent blockwise choices again enlarges the
root-generated choice set, so every failure remains a failure under the
original rooting rule.  The census is over all unlabeled connected block
graphs, not a general graph census.

| `n` | block graphs | cyclomatic `>=2` | minimum optimized sum |
|---:|---:|---:|---:|
| 4 | 4 | 1 | 0.8660254038 |
| 5 | 9 | 3 | 0.5773502692 |
| 6 | 22 | 9 | 0.4472135955 |
| 7 | 59 | 30 | 0.4082482905 |
| 8 | 165 | 98 | 0.3574067443 |
| 9 | 496 | 332 | 0.3162277660 |
| 10 | 1,540 | 1,135 | 0.2898979486 |
| 11 | 4,960 | 3,932 | 0.2705980501 |
| 12 | 16,390 | 13,744 | 0.2531119798 |
| 13 | 55,408 | 48,500 | 0.2391689455 |
| 14 | 190,572 | 172,366 | 0.2278353395 |

Thus the first failure is at `n=13`.  One certificate is graph6
`LsaCGGA_C?_A?A`: two triangles share a vertex, each of the four outer
vertices has one leaf, and the shared vertex has four leaves.  The `n=14`
minimum is the same construction with five shared-vertex leaves, graph6
`MsaCCCA?S?O@?A?@?`.

The floating values were computed by symmetric eigendecomposition.  The
graph certificates and all nine center choices are small enough for an exact
algebraic-number check if a formal minimal-order certificate is needed; that
extra certification is unnecessary for the asymptotic disproof (5).

## Scaling the variational test matrix

Uniformly scaling the test matrix does not repair the method.  With
`P=A(T)_+` and `Y=tP`, the variational objective is

\[
(2t-t^2)(n-1)+4tS.
\]

Its optimum occurs at `t=1+2S/(n-1)` and equals

\[
n-1+4S+\frac{4S^2}{n-1}.                               \tag{7}
\]

For the family (6), the extra term in (7) is `O(L^-2)` and the total gain
over `n-1` is still `O(L^-1/2)`.  Any successful continuation therefore
needs a genuinely nonuniform positive-semidefinite perturbation (probably
one that places additional mass on the high-degree articulation/pendant-star
sector), not scalar scaling of `A(T)_+`.

This failure is only a failure of the proposed quantitative witness.  The
graphs above themselves satisfy AKMPZ Conjecture 1.2 with substantial slack;
they are not counterexamples to the conjecture.
