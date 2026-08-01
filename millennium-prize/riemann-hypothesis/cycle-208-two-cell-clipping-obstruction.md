# Cycle 208: exact two-cell fit and clipping obstruction

## Normalized two-cell ansatz

Take two unit cells, initial vector `y_0=e_1`, and rank-one symmetric
Hamiltonians

\[
 G_1=a e_1e_1^T,\qquad G_2=bvv^T,\qquad v=(c,1)^T.
\]

The matrices may be indefinite in the canonical-system sense: a negative
coefficient makes the corresponding cell negative semidefinite. Since
`(Juu^T)^2=0`, direct transfer through the cells gives

\[
 Y(1,z)=(1,-az)^T,
 \qquad v^TY(1,z)=c-az.
\]

The Lagrange identity therefore gives the exact endpoint kernel

\[
 \boxed{\pi K_G(z,w)=a+b(c-az)(c-a\bar w).}                 \tag{208.1}
\]

No exponential or numerical approximation enters this formula.

## Exact fit on two nodes

Let the nodes be `0,1`, and prescribe the real symmetric matrix

\[
 T=\begin{pmatrix}p&r\\r&s\end{pmatrix}
   =\pi[K_*(z_j,z_k)]_{j,k=0}^1.
\]

Put

\[
 d=p-2r+s,\qquad \Delta=ps-r^2.
\]

If `d Delta != 0`, the unique member of (208.1) fitting all three entries is

\[
 \boxed{
 a={\Delta\over d},\qquad
 b={d^3\over\Delta^2},\qquad
 c={\Delta(p-r)\over d^2}.}                 \tag{208.2}
\]

Indeed, the three interpolation equations imply

\[
 d=ba^2,\qquad p-r=bca,\qquad \Delta=ad,
\]

which proves both (208.2) and uniqueness in this normalized rank-one family.
For the shifted-xi target one may take

\[
 p=\pi K_E(0,0)=\xi(3/2)\xi'(3/2),\quad
 r=\pi K_E(0,1),\quad s=\pi K_E(1,1),
\]

with `K_E` as in Cycle 207. These are exact special-function expressions, but
the formulas themselves require no numerical evaluation. For the bounded
shift `E(z)=xi(3/2-iz)`, the classical zero-free half-plane `Re(s)>1` and the
shifted de Branges criterion make `K_E` positive; hence `d>=0` and
`Delta>=0`. With the usual strictness/nondegeneracy for the two distinct nodes,
both are positive. Formula (208.2) then gives `a,b>0` and the exact two-node xi
fit has `nu=0`: this normalized rank-one architecture does not produce an
indefinite xi candidate at these nodes. It is only a finite-node interpolant,
not a disk approximation.

## Integrated negative spectral mass

Each cell has only one nonzero eigenvalue. Hence the Cycle 207 defect is exactly

\[
 \boxed{
 \nu=(-a)_+ +(-b)_+(1+c^2),\qquad (x)_+=\max(x,0).}         \tag{208.3}
\]

Thus a negative determinant or a negative second-difference forces an
indefinite cell. In particular, if `d>0` and `Delta<0`, then only the first cell
is negative and `nu=-Delta/d`. If `d<0`, then the second cell is negative and
its contribution is `(-b)(1+c^2)`.

## Rational exact candidate

The smallest transparent indefinite instance is

\[
 T=\begin{pmatrix}1&2\\2&1\end{pmatrix},\qquad
 d=-2,\quad\Delta=-3.
\]

Formula (208.2) gives

\[
 a={3\over2},\qquad b=-{8\over9},\qquad c={3\over4},
\]

or, explicitly,

\[
 G_1=\begin{pmatrix}3/2&0\\0&0\end{pmatrix},\qquad
 G_2=\begin{pmatrix}-1/2&-2/3\\-2/3&-8/9\end{pmatrix}.
\]

Its endpoint kernel is

\[
 \pi K_G(z,w)={3\over2}-{8\over9}
 (3/4-3z/2)(3/4-3\bar w/2),                 \tag{208.4}
\]

and (208.4) equals `T` exactly on the two nodes. The second cell has eigenvalues
`0,-25/18`, so

\[
 \boxed{\eta=0,\qquad \nu={25\over18}.}                     \tag{208.5}
\]

Cellwise clipping deletes `G_2`. The resulting node matrix, in the same
pi-normalization, is the constant matrix with every entry `3/2`; its entrywise
error from `T` is exactly `1/2`.

## Can a clipping sequence decrease both defects?

Not for this target under the bounded-mass hypothesis of Cycle 207. The target
matrix has eigenvalues `3,-1`. Every clipped endpoint matrix is positive
semidefinite, so the finite-node obstruction (207.5), with two nodes, requires

\[
 \sup_{j,k}|K_{G_{N,+}}(z_j,z_k)-K_*(z_j,z_k)|
 \ge {1\over2\pi}.                            \tag{208.6}
\]

If the indefinite kernels have node defect `eta_N`, negative mass `nu_N`, and
a common total-mass bound `M`, the clipping lemma gives

\[
 \boxed{\eta_N+C(R,M,1)\nu_N\ge {1\over2\pi}.}             \tag{208.7}
\]

Consequently no bounded-mass clipping sequence can have both `eta_N -> 0` and
`nu_N -> 0`. Within the normalized family (208.1), exact interpolation is even
more rigid: (208.2) is unique, so its negative mass remains exactly `25/18`.

For a positive-semidefinite two-node target with `d>0` and `Delta>0`, (208.2)
instead has `a,b>0` and `nu=0`; finite-node fitting then needs no clipping. This
does not settle the shifted-xi problem, because fitting two nodes says nothing
about local uniform approximation on a disk or an exhaustion. If the uniform
mass bound is dropped, (208.7) no longer follows: a large positive transfer can
amplify a small negative cell, precisely the instability excluded by the
bounded lane.

`verify_cycle208_two_cell.py` checks every rational identity above using exact
integer arithmetic. No Riemann-hypothesis result is claimed.
