# Two-scale completed-square verification

`analyze_two_scale_completion.py` certifies the completed first-block form for
`N <= k < 2N` using exact rational floor matrices and 192-bit Arb balls.

## Certified structure

Let `F_X(k,d)=floor(k/d)` on the first block and let
`W=diag(1/(k(k+1)))`.  The analyzer first treats the signed quadratic kernel on
the independent two-channel coefficient space as

\[
 \operatorname{diag}(F_N^T W F_N,-F_{2N}^T W F_{2N}).
\]

Its nullspace is exactly `ker(F_N) direct-sum ker(F_2N)`.  Since `W` is
positive definite, exact row reduction gives the inertia

\[
 (n_+,n_-,n_0)=(rank(F_N),rank(F_{2N}),
 3N-rank(F_N)-rank(F_{2N})).
\]

This is not the inertia of the common-source Mobius restriction, where the two
coefficient vectors are linked.  On one source vector indexed by `d<=2N`, the
common-source kernel is

\[
 \mathcal H_N=D_\lambda F^TWF D_\lambda-D_\eta F^TWF D_\eta,
\]

where

\[
 \lambda_d=\mathbf1_{d\le N}{\log(N/d)\over\log N},\qquad
 \eta_d={\log(2N/d)\over\log(2N)}.
\]

It is already indefinite: `lambda_1=eta_1=1`, while for every active `e>1`
the `1,e` entry is negative, so that principal `2 by 2` minor has negative
determinant.

The Mobius coefficient vectors are the actual finite vectors
`mu(d) log(X/d)/log(X)`, not smooth or modal surrogates.  Their orthogonal
row-space and kernel projections are computed with exact rational Gram
inverses and Arb coefficient balls.  The analyzer certifies that each kernel
part maps to zero and each projected image equals the original transform.

For every cell it verifies

\[
 {1\over k(k+1)}\left[
 \left(kA+1-{Z_N(k)\over\log N}\right)^2-
 \left(k(A-\alpha D)+1-{Z_{2N}(k)\over\log(2N)}\right)^2\right]
 =\alpha\,w_k g_k.
\]

Thus the completed total is `alpha` times the independently reconstructed
`weighted_g` total.  The scale factor is required because `weighted_g` stores
the unnormalized drift-free coefficient `g_k`, while the completed square is
in the endpoint normalization.  The analyzer also checks
`Z_2N(k)=log(2N)+psi(k)` throughout the block.

## 192-bit run

| N | inertia | rank pair | nullity pair | completed total |
|---:|:---:|:---:|:---:|---:|
| 2 | `(2,2,2)` | `(2,2)` | `(0,2)` | `0.079383682775286` |
| 4 | `(3,4,5)` | `(3,4)` | `(1,4)` | `0.033448720983089` |
| 8 | `(7,8,9)` | `(7,8)` | `(1,8)` | `0.0088361116488780` |
| 16 | `(12,16,20)` | `(12,16)` | `(4,16)` | `0.0027228946972542` |
| 32 | `(25,32,39)` | `(25,32)` | `(7,32)` | `0.00060014454568958` |

At every listed `N`, the exact joint-kernel and inertia checks, both actual
Mobius projections, all cell identities, the `psi` identity, and the
`weighted_g` total comparison pass.

## Exact common-source scale relation

Set

\[
 \rho_d=\begin{cases}1,&d\le N,\\
 \log(2N/d)/\log2,&N<d\le2N.
 \end{cases}
\]

Then `eta=(1-alpha)lambda+alpha rho`.  If

\[
 P_k=kA+1-Z_N(k)/\log N,
\]

and

\[
 Q_k=k(A-D)+1-{Z_{2N}(k)-Z_N(k)\over\log2},
\]

the second completed center is exactly

\[
 \widetilde P_k=(1-\alpha)P_k+\alpha Q_k.
\]

Therefore

\[
 P_k^2-\widetilde P_k^2
 =\alpha(2-\alpha)
 \left(P_k-{1-\alpha\over2-\alpha}Q_k\right)^2
 -{\alpha\over2-\alpha}Q_k^2.
\]

The underlying coefficient matrix has determinant `-alpha^2`; this exact
compression is indefinite and supplies no generic positivity.

## Commands

```text
uv run --with python-flint python -m unittest -v test_two_scale_completion.py
uv run --with python-flint python analyze_two_scale_completion.py --N 2 4 8 16 32
```
