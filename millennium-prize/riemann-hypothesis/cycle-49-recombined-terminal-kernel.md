# Cycle 49: recombined terminal kernel and cell no-go

## Increment kernel

Fix `2<=M<=B`, set `f=F_M`, and write

\[
e_r=F_{r+1}-F_r=h_rD_r\qquad(M\le r<B).
\]

Let

\[
W=\sum_{n=M}^Bw_n,\qquad
T_r=\sum_{n=r+1}^Bw_n,
\qquad K_{rs}=T_{\max(r,s)}.
\]

Expanding every future endpoint before splitting packet and coherent channels
gives the exact finite identity

\[
\boxed{
Q_{M,B}=(1-W)\|f\|^2
-2\sum_{r=M}^{B-1}T_r\langle f,e_r\rangle
-\sum_{r,s=M}^{B-1}K_{rs}\langle e_r,e_s\rangle.} \tag{49.1}
\]

The double sum is over ordered pairs. In terms of the physical increments,

\[
Q_{M,B}=(1-W)P_M
-2\sum_{r=M}^{B-1}h_rT_r\langle F_M,D_r\rangle
-\sum_{r,s=M}^{B-1}h_rh_sT_{\max(r,s)}
 \langle D_r,D_s\rangle.                         \tag{49.2}
\]

Index rows by `n=M+1,...,B`, columns by `r=M,...,B-1`, and put
`L_(nr)=1_(r<n)`. Then

\[
\boxed{K=L^*\operatorname{diag}(w_{M+1},\ldots,w_B)L>0.}  \tag{49.3}
\]

Thus the increment quadratic channel has full negative rank. If
`t=(T_M,...,T_(B-1))`, then `t=K e_1`. The augmented scalar matrix

\[
\begin{pmatrix}1-W&-t^*\\-t&-K\end{pmatrix}
\]

has inertia `(1,B-M,0)`: its Schur complement over `-K` is `1-w_M>0`.
Completing that one positive anchor direction reconstructs

\[
\boxed{
Q_{M,B}=(1-w_M)P_M-\sum_{n=M+1}^Bw_nP_n,}        \tag{49.4}
\]

which is the definition with its first term combined. Hence recombining the
Cycle 47--48 channels creates no independent favorable square; the genuine
off-diagonal increment correlations remain inside the future endpoint norms.

The singleton recurrence gives the second exact reconstruction

\[
\boxed{
Q_{M,B}=P_{B+1}+\sum_{n=M}^B\beta_nH_n.}         \tag{49.5}
\]

The endpoint `P_(B+1)` and the final `H_B` are essential. Thus the unsplit
kernel returns either the original terminal budget or the known weighted-`H`
block. Finite Hilbert algebra alone produces no narrower sign inequality.

## Fully combined reciprocal cells

In reciprocal coordinates, on `k<t<k+1`, write

\[
F_n(t)=A_nt+b_{n,k},
\]

where

\[
A_n=\sum_{a\le n}{\mu(a)\over a}
-{1\over\log n}\sum_{a\le n}{\mu(a)\log a\over a},
\]

\[
b_{n,k}=1-\sum_{a\le n}\mu(a)
\left(1-{\log a\over\log n}\right)\lfloor k/a\rfloor.
\]

Put `lambda_k=log(1+1/k)` and `tau_k=1/[k(k+1)]`. The complete terminal cell
is

\[
\boxed{q_{M,B}(k)=C+2Z_k\lambda_k+H_k\tau_k,}     \tag{49.6}
\]

with

\[
C=A_M^2-\sum_{n=M}^Bw_nA_n^2,
\]

\[
Z_k=A_Mb_{M,k}-\sum_{n=M}^Bw_nA_nb_{n,k},\qquad
H_k=b_{M,k}^2-\sum_{n=M}^Bw_nb_{n,k}^2.
\]

The sum of (49.6) over complete cells is `Q_(M,B)`. Its three unshifted
channels must not be summed separately at infinity.

For `k<=M`, every divisor convolution is complete:

\[
b_{n,k}=-{\psi(k)\over\log n}\qquad(M\le n\le B).
\]

Define

\[
D={A_M\over\log M}-\sum_{n=M}^Bw_n{A_n\over\log n},
\qquad
E={1\over\log^2M}-\sum_{n=M}^B{w_n\over\log^2n}.
\]

Then

\[
\boxed{q_{M,B}(k)=C-2D\psi(k)\lambda_k+E\psi(k)^2\tau_k,} \tag{49.7}
\]

and telescoping comparison gives

\[
\boxed{E>{1\over\log^2(B+1)}>0.}                 \tag{49.8}
\]

Therefore the initial cell has the exact completion

\[
q_{M,B}(k)=E\tau_k
\left(\psi(k)-{D\lambda_k\over E\tau_k}\right)^2
+C-{D^2\lambda_k^2\over E\tau_k}.                \tag{49.9}
\]

The last remainder has no algebraic sign, so even the complete initial packet
is not certified positive by this square.

## Summable coordinates and tail obstruction

Put `u=t-k` and `r_(n,k)=kA_n+b_(n,k)`. Then `F_n=A_nu+r_(n,k)` and the three
cell metrics

\[
\alpha_k=1-2k\lambda_k+{k\over k+1},\quad
\delta_k=\lambda_k-{1\over k+1},\quad
\tau_k={1\over k(k+1)}
\]

are positive and of summable size. This yields an absolutely convergent cell
representation

\[
q_{M,B}(k)=C\alpha_k+2R_k\delta_k+S_k\tau_k,
\]

but `S_k` remains an indefinite difference of physical intercept squares.
Thus shifting removes the artificial divergent-channel problem without
creating positivity.

The tail is genuinely not Chebyshev-controlled. Choose distinct primes
`p<=M<=B<q` and set `k=p^2q`. For every `M<=n<=B`, the only nonzero-Mobius
divisors of `k` not exceeding `n` are `1,p`; `q` and `pq` exceed `B`, while
`mu(p^2)=0`. Hence

\[
\boxed{b_{n,k}-b_{n,k-1}=-{\log p\over\log n}\ne0,}       \tag{49.10}
\]

although `Lambda(k)=0`. There are infinitely many such nonsquarefree,
non-Chebyshev impulses. Abel summation preserves them as signed truncated
divisor-floor terms rather than eliminating them.

## Conclusion

The joint packet/coherent expansion collapses exactly to the old terminal
kernel and weighted-`H` recurrence. Its coefficient kernel has one positive
anchor direction and full negative future rank. The cell representation has a
positive initial Chebyshev quadratic coefficient, but an unsigned remainder and
an infinite post-`M` family of non-Chebyshev impulses. The remaining problem is
therefore the same prescribed coupling of the Mobius reciprocal-log vectors to
the complete restricted Vasyunin Gram matrix.

This is a structural checkpoint and route no-go, not a terminal positivity
theorem or an RH result.
