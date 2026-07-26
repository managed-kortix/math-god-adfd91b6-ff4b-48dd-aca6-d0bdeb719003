# Cycle 39: reverse-tail Hardy kernel after complete Gram interchange

## 1. Target and finite cutoff

Retain the Cycle 38 notation

\[
x_n={1\over\log n},\qquad
w_n=(x_n-x_{n+1})\log n
={\log(1+1/n)\over\log(n+1)},
\]

\[
c_q(n)=\mu(q)\left(1-{\log q\over\log n}\right)\mathbf 1_{q\le n},
\qquad
u_n=(1,(c_q(n))_{q\ge1}).
\]

If `Gamma` is the augmented complete physical Gram matrix

\[
\Gamma_{00}=1,\qquad \Gamma_{0q}=g_q,\qquad
\Gamma_{qr}=G_{q,r},
\]

with `g_q` and `G_(q,r)` given by (38.1a)--(38.1b), then
`P_n=u_n^T Gamma u_n`. At `kappa=1/2`, the reverse-tail Hardy target is

\[
\boxed{P_a\ge \sum_{n=a}^{\infty}w_nP_n.}                 \tag{39.1}
\]

Because an entrywise infinite coefficient interchange is not automatically
legitimate, first truncate at `B>=a`. The exact scale-side kernel is

\[
\boxed{M_{a,B}=u_au_a^T-\sum_{n=a}^{B}w_nu_nu_n^T,}       \tag{39.2}
\]

and hence

\[
P_a-\sum_{n=a}^{B}w_nP_n
=\sum_{i,j\le B}M_{a,B}(i,j)\Gamma_{ij}.                  \tag{39.3}
\]

Thus the complete Gram sums preserve the common scale `n`; no product of
separately summed coefficients occurs.

## 2. Exact coefficient entries

For `m>=1` and `j=0,1,2`, define

\[
S_j^{a,B}(m)=\sum_{n=\max(a,m)}^B w_nx_n^j,
\]

with an empty sum equal to zero. Direct interchange in the finite sum gives

\[
\boxed{M_{a,B}(0,0)=1-S_0^{a,B}(1),}                     \tag{39.4}
\]

\[
\boxed{M_{a,B}(0,q)=c_q(a)-\mu(q)
\left[S_0^{a,B}(q)-(\log q)S_1^{a,B}(q)\right],}          \tag{39.5}
\]

and, with `m=max(q,r)`,

\[
\boxed{\begin{aligned}
M_{a,B}(q,r)={}&c_q(a)c_r(a)\\
&-\mu(q)\mu(r)\left[S_0^{a,B}(m)
-(\log q+\log r)S_1^{a,B}(m)
 +(\log q)(\log r)S_2^{a,B}(m)\right].
\end{aligned}}                                           \tag{39.6}
\]

Equations (39.4)--(39.6) are the exact coefficient kernel requested by the
tail target. They also expose a basic obstruction to taking `B` to infinity:
`S_0^{a,B}(m)` diverges, since `sum_n w_n=infinity`. In particular, for
fixed squarefree `q,r`, the separate scalar, linear, and quadratic entries do
not have finite limits. Any finite value of the physical contraction in
(39.1) must retain cancellations across the growing complete coefficient
system; it cannot be obtained by taking the limits of (39.4)--(39.6) entry by
entry.

## 3. Natural domain of the limiting quadratic form

The obstruction is exact on every finitely supported coefficient test vector
`z=(z_0,(z_q))`. Put

\[
A(z)=z_0+\sum_q\mu(q)z_q,
\qquad
B(z)=\sum_q\mu(q)(\log q)z_q.
\]

Once `n` exceeds the support of `z`,

\[
\boxed{z\mathbin\cdot u_n=A(z)-{B(z)\over\log n}.}        \tag{39.7}
\]

Consequently

\[
z^TM_{a,B}z=(z\mathbin\cdot u_a)^2
-\sum_{n=a}^Bw_n(z\mathbin\cdot u_n)^2.                 \tag{39.8}
\]

If `A(z)\ne0`, the second term tends to infinity and (39.8) tends to
`-infinity`. If `A(z)=0`, the tail is finite because

\[
\sum_n{w_n\over(\log n)^2}<\infty.
\]

Thus the only natural finite-support domain for a finite limiting coefficient
form is the codimension-one balanced space

\[
\mathcal D_0=\{z:A(z)=0\}.                               \tag{39.9}
\]

On that space the exact limit is

\[
\boxed{\mathfrak m_a[z]=(z\mathbin\cdot u_a)^2
-\sum_{n=a}^{\infty}w_n(z\mathbin\cdot u_n)^2.}          \tag{39.10}
\]

There is an exact signed integral representation. For
`t in [log n,log(n+1))`, set `U(t)=u_n`. Since

\[
w_n=\int_{\log n}^{\log(n+1)}{dt\over\log(n+1)},
\]

one has, on its finite domain,

\[
\boxed{\mathfrak m_a[z]=(z\mathbin\cdot u_a)^2
-\int_{\log a}^{\infty}
 {|z\mathbin\cdot U(t)|^2\over
  \log(\lfloor e^t\rfloor+1)}\,dt.}                     \tag{39.11}
\]

This is an endpoint rank-one square minus a positive integral, not a positive
integral representation.

## 4. Explicit balanced negative direction

The failure of positivity persists after removing the divergent constant
mode. Choose squarefree integers `q,r` with `a<q<r` and define

\[
z_q=\mu(q),\qquad z_r=-\mu(r),\qquad z_j=0\quad(j\ne q,r).
\tag{39.12}
\]

Then `A(z)=0` and `z dot u_a=0`. Moreover,

\[
z\mathbin\cdot u_n=
\begin{cases}
0,&n<q,\\
1-\dfrac{\log q}{\log n},&q\le n<r,\\
\dfrac{\log(r/q)}{\log n},&n\ge r.
\end{cases}                                              \tag{39.13}
\]

Substitution into (39.10) gives the exact strictly negative value

\[
\boxed{\begin{aligned}
\mathfrak m_a[z]={}&-
\sum_{n=q}^{r-1}w_n
\left(1-{\log q\over\log n}\right)^2\\
&-(\log(r/q))^2\sum_{n=r}^{\infty}{w_n\over(\log n)^2}<0.
\end{aligned}}                                           \tag{39.14}
\]

The second series converges and is positive. Therefore the limiting kernel
is not positive semidefinite even on its balanced domain. A fortiori it
cannot be represented as an integral of positive rank-one coefficient kernels.
For every sufficiently large finite `B`, the same vector is already a strict
negative direction of `M_(a,B)`.

## 5. Verdict

At `kappa=1/2`, complete Gram interchange yields the finite kernel
(39.2), equivalently the entries (39.4)--(39.6). The formal infinite matrix
does not exist entrywise because its unbalanced modes have infinite negative
mass. Balancing removes that divergence but not the sign obstruction: the
two-squarefree-coordinate vector (39.12) gives the finite strict negative
value (39.14).

This falsifies a generic coefficient-space PSD or positive-integral proof of
the reverse-tail Hardy inequality. It does not falsify (39.1) for the fixed
Mobius endpoint vectors, because (39.1) contracts the scale kernel with the
specific physical Gram matrix and depends on cancellations across the entire
growing coefficient system. Any proof must use that arithmetic/physical
interaction rather than positivity of the interchanged scale kernel alone.
