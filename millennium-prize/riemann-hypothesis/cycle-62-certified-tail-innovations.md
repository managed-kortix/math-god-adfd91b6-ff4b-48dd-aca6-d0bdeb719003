# Cycle 62: certified tail innovations and exact boundary completion

## Durable finite verifier

The script `verify_cycle62_tail_innovations.py` computes the cumulative
finite-tail certificate `Omega_[M,N]`. All floor constraints are represented by
exact rational numbers; logarithms and Schur solves use outward-rounded Arb
balls. The associated unit tests reproduce the Cycle 60 consecutive-cell value
and certify a strict crossing.

For `[M,B)=[220,231)`, at 320-bit precision,

\[
\Omega_{[220,880]}
=0.0199129219732127171093129916316\ldots,
\]

while the corrected exact physical target is

\[
\beta_2+\delta_{220,231}
=0.0186371960000083830592811401588\ldots.
\]

Arb certifies

\[
\boxed{\Omega_{[220,880]}-(\beta_2+\delta)
>0.0012757259732043340500318514.}                  \tag{62.1}
\]

The first integer endpoint found by the same nested computation is `N=742`.
This is a compact finite certificate for that historical block. Since
`R>=Omega`, Cycle 58 gives `G_2>=R-beta_2>delta`, so the lag-two gain pays the
post-staircase deficit and the exact block recurrence is nonnegative on
`[220,231)`. It is not a uniform window theorem.

## Certified dyadic profile

The cumulative values through `16M` are:

| window | `Omega_(2M)` | `Omega_(4M)` | `Omega_(8M)` | `Omega_(16M)` |
|---|---:|---:|---:|---:|
| `[98,99)` | `0.01781169` | `0.02407568` | `0.02686722` | `0.02853287` |
| `[219,231)` | `0.01303754` | `0.01956248` | `0.02306703` | `0.02499716` |
| `[220,231)` | `0.01327179` | `0.01991292` | `0.02348290` | `0.02555856` |
| `[222,226)` | `0.01499272` | `0.02153622` | `0.02504942` | `0.02686551` |

Only `[220,231)` crosses its positive target through this range. The other
three remain below their targets at `16M`. Their positive dyadic increments
decrease numerically, but no asymptotic ratio is inferred.

## Exact tail Gram reduction

For `H_N=L^2([N,infinity),dt/t^2)`, every tail correlation of reciprocal rows
reduces to the complete restricted Vasyunin Gram entry minus a finite prefix.
On a cell `[k,k+1)`,

\[
\rho_q(t)=t/q-\lfloor k/q\rfloor.
\]

Thus for a dyadic block `[N,2N)`,

\[
\int_N^{2N}\rho_q(t)\rho_r(t){dt\over t^2}
=\sum_{k=N}^{2N-1}\left[
{1\over qr}-\lambda_k\left({\lfloor k/r\rfloor\over q}
+{\lfloor k/q\rfloor\over r}\right)
+\tau_k\lfloor k/q\rfloor\lfloor k/r\rfloor\right].             \tag{62.2}
\]

Consequently the complete pure-tail value is a finite Vasyunin Schur
complement

\[
\boxed{\Omega_\infty=d-b^TA^{-1}b,}                \tag{62.3}
\]

where `A` is the tail Gram matrix of `U_(M-1),rho_M,...,rho_(B-1)`, `b` their
tail correlation with `D_(M-1)`, and `d` the tail norm of `D_(M-1)`. The rows
are linearly independent on the tail, so `A` is positive definite. This proves
strict positivity for each fixed parameter set, but no uniform scale.

## Rigorous infinite-tail topology

All infinite constraints are defined as actual `L^2` inner products with the
bounded physical rows. One must not separately extend `A=sum A_k`, which is an
unbounded functional on the tail Hilbert space. The compensated row and score
functionals are bounded because `U_(M-1)`, the new reciprocal rows, and the
finite old state `D_(M-1)` are bounded affine-cell functions.

Finite constrained supports are dense in the full constraint kernel: finite
cell functions are dense, the constraint map is onto a finite-dimensional
space, and a fixed finite-support right inverse corrects every approximation.
This validates the Cycle 61 Parseval innovation expansion without manipulating
divergent split moments.

## Exact boundary scalar

Pure tail omits exactly one useful below-`M` coordinate. Put

\[
\phi_M=t\mathbf1_{(1,M)},\qquad q_M=M-1,
\qquad d_M=\ell_{M-1}+c_M.
\]

After imposing orthogonality to `g_M`, every useful below-`M` witness is
`b phi_M/q_M`, with norm `b^2/q_M`. Let `C` be the tail constraint map,
`a_M=(m_(M-1),1/M,...,1/(B-1))`, and `sigma` the tail old-`D` vector. Then

\[
\boxed{
R=\sup_{Cx+a_Mb=0}
{|\langle\sigma,x\rangle+d_Mb|^2
\over\|x\|^2+b^2/(M-1)}.}                         \tag{62.4}
\]

The tail rows are independent, so `C` is onto. If

\[
u_M=C^*(CC^*)^{-1}a_M,
\qquad
\delta_M=d_M-\langle\sigma,u_M\rangle,
\]

orthogonal decomposition of feasible vectors gives

\[
\boxed{R=\Omega_\infty+
{\delta_M^2\over(M-1)^{-1}+\|u_M\|^2}.}            \tag{62.5}
\]

Equality is exact because, after extracting `g_M`, the physical score and every
constraint row restrict below `M` to the `phi_M` line. Components orthogonal to
both `phi_M` and `g_M` therefore pair with neither and only increase the norm.
Formula (62.5) closes the topology/bookkeeping gap, but supplies no lower bound
for either term.

The remaining problem is quantitative: prove that the finite-tail innovations
or the compensated boundary channel pay every additive-12 deficit uniformly.
No additive-12 theorem or RH result is claimed.
