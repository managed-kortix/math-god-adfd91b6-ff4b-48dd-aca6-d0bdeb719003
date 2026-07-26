# Certified separated expansion of the weighted sine kernel

## 1. Complex endpoint expansion

For `Q>0` and real `d != 0`, put

\[
J_Q(d)=\int_Q^\infty e^{idt}t^{-2}\,dt,
\qquad C_Q(d)=\operatorname{Re}J_Q(d).
\]

Repeated integration by parts gives, for every integer `n>=0`,

\[
J_Q(d)=-e^{iQd}\sum_{k=0}^{n}
\frac{(k+1)!}{(id)^{k+1}Q^{k+2}}+R_n(d),
\tag{1.1}
\]

and

\[
\boxed{|R_n(d)|\le
\frac{(n+1)!}{Q^{n+2}|d|^{n+1}}.}
\tag{1.2}
\]

Notice the indexing: (1.1) has `n+1` displayed terms. The estimate follows
from the exact residual

\[
R_n(d)=\frac{(n+2)!}{(id)^{n+1}}
\int_Q^\infty e^{idt}t^{-n-3}\,dt.
\]

The first real terms are

\[
C_Q(d)=-\frac{\sin(Qd)}{Q^2d}
+\frac{2\cos(Qd)}{Q^3d^2}
+\frac{6\sin(Qd)}{Q^4d^3}
-\frac{24\cos(Qd)}{Q^5d^4}+\cdots .
\]

The oscillatory phase is already separated:
`exp(iQ(a-b))=exp(iQa)exp(-iQb)` and
`exp(iQ(a+b))=exp(iQa)exp(iQb)`.

## 2. Half-next-term enclosure

Let

\[
T_{n+1}(d)=-\frac{e^{iQd}(n+2)!}
{(id)^{n+2}Q^{n+3}}.
\]

The normalized residual is a positive average of points on the circle with
center `1/2` and radius `1/2`. Consequently

\[
\boxed{\left|R_n(d)-\frac12T_{n+1}(d)\right|
\le\frac{(n+2)!}{2Q^{n+3}|d|^{n+2}}.}
\tag{2.1}
\]

This is half the magnitude of the *next term*, not half of (1.2). The complex
constants in (1.2) and (2.1) are uniformly optimal: the normalized terminant
approaches the endpoints `0` and `1` as `|Qd|` approaches zero and infinity.
No corresponding parity-specific sharpness claim for the real projection is
made.

## 3. Certified amplitude compression

For integer `m>=1`, let `d=d_0+h`, where `|h|<=H<|d_0|`. The degree-`p`
Taylor polynomial of `d^{-m}` has the exact uniform remainder bound

\[
\boxed{
\left|d^{-m}-\sum_{j=0}^{p}(-1)^j
\binom{m+j-1}{j}d_0^{-m-j}h^j\right|
\le \binom{m+p}{p+1}
\frac{H^{p+1}}{(|d_0|-H)^{m+p+1}}.}
\tag{3.1}
\]

This follows directly from the integral Taylor remainder and is valid for
either sign of `d_0`.

## 4. Separated-block theorem

Let `A=[a_0-r_A,a_0+r_A]` and `B=[b_0-r_B,b_0+r_B]` be positive intervals,
with `A` strictly to the right of `B`. Set

\[
d_0=a_0-b_0,\quad s_0=a_0+b_0,\quad H=r_A+r_B,
\]

and assume `H<d_0`. Apply (1.1) through order `n` to both arguments `a-b` and
`a+b`, and apply (3.1) through degree `p` to every retained inverse power.
For

\[
D_Q(a,b)=C_Q(a-b)-C_Q(a+b),
\]

the resulting separated approximation `Dtilde` obeys

\[
\sup_{A\times B}|D_Q-\widetilde D|
\le E_{\rm far}+E_{\rm amp},
\tag{4.1}
\]

where

\[
E_{\rm far}=\frac{(n+1)!}{Q^{n+2}}
\left[(d_0-H)^{-n-1}+(s_0-H)^{-n-1}\right]
\tag{4.2}
\]

and

\[
E_{\rm amp}=\sum_{k=0}^{n}
\frac{(k+1)!}{Q^{k+2}}
\binom{k+p+1}{p+1}H^{p+1}
\left[(d_0-H)^{-k-p-2}+(s_0-H)^{-k-p-2}\right].
\tag{4.3}
\]

These are absolute entrywise bounds. A degree-`p` polynomial in either `a-b`
or `a+b`, after phase extraction, has complex separated rank at most `p+1`.
The two channels share their left basis, so the combined real rank is at most

\[
\boxed{2(p+1).}
\tag{4.4}
\]

The rank does not contain `Q` or `n`; summing the inverse-power amplitudes first
still produces one degree-`p` polynomial in each channel. However, useful error
requires both fixed geometric admissibility `H/d_0<1` and a lower threshold on
`Q(d_0-H)`. There is no geometry-free uniform-rank theorem.

For the sine kernel

\[
K_Q(a,b)=\frac12[D_Q(a,b)],
\]

the entrywise radius is half of (4.1). Its quadratic-form radius must then be
propagated with the local coefficient theorem in
`hierarchical-error-propagation.md`; signed block centers may cancel, but
unstructured radii may not.

## 5. Near-field obstruction

The identity

\[
K_Q(a,b)=\frac\pi2\min(a,b)
-\int_0^Q\sin(at)\sin(bt)t^{-2}\,dt
\]

shows that the diagonal cusp is a Brownian-covariance kernel plus a smooth
correction. On the rational grid `a_i=ih`, the matrix
`(min(i,j))_(i,j=1)^N` has eigenvalues

\[
\frac1{4\sin^2((2k-1)\pi/(4N+2))},\qquad 1\le k\le N.
\]

Thus overlapping blocks are not uniformly low rank. A valid hierarchy must
leave them dense or represent the cusp explicitly. Entrywise residuals require
local `l1` propagation; an `l2` bound is valid only after certifying a spectral
residual norm.
