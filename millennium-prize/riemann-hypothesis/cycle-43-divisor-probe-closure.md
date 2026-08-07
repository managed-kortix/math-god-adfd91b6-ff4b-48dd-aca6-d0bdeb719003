# Cycle 43: exact closure and tautology boundary for divisor probes

## 1. Finite block-cell Hilbert space

Fix `2 <= A < B` and a cell cutoff `K`. Work in the finite direct sum of the
two-dimensional completed-square cell spaces from (41.1). Put

\[
 \phi_{a,k}=(c_{a,k},-\sqrt{q_k}f_{a,k}),\qquad
 f_{a,k}=\lfloor k/a\rfloor,\qquad
 c_{a,k}=a^{-1}-\lambda_kf_{a,k}.
\]

For every divisor `a<B`, define its D-admission column

\[
 z_a^D=\left({\bf1}_{a\le n}\sqrt{\beta_n}\,\mu(a)(\log a)
 \phi_{a,k}\right)_{A\le n<B,\ k\le K}.                 \tag{43.1}
\]

Let

\[
 X=\left(\sqrt{\beta_n}
 (\ell_n+\lambda_kv_{n,k},\sqrt{q_k}v_{n,k})
 \right)_{A\le n<B,\ k\le K}.                           \tag{43.2}
\]

All statements through Section 4 are finite-dimensional exact identities. No
zero expansion or RH hypothesis occurs anywhere in this note; Section 5 then
passes explicitly to the complete cell space and records an asymptotic frame
upper bound.

## 2. Exact reconstruction theorem

Equations (41.8)--(41.9) give, cell by cell,

\[
 \ell_n+\lambda_kv_{n,k}
 =\sum_{a\le n}\mu(a)(\log a)c_{a,k},
 \qquad
 \sqrt{q_k}v_{n,k}
 =-\sum_{a\le n}\mu(a)(\log a)\sqrt{q_k}f_{a,k}.
\]

Therefore

\[
 \boxed{X=\sum_{a<B}z_a^D.}                              \tag{43.3}
\]

Let `Z_D` be the synthesis matrix with the nonzero columns `z_a^D`, let
`G_D=Z_D^*Z_D`, and let `b_D=Z_D^*X`. Since (43.3) says
`X=Z_D {\bf1}`, one has `b_D=G_D{\bf1}`. The Moore--Penrose identity
`GG^+G=G` now yields

\[
 \boxed{b_D^*G_D^+b_D
 ={\bf1}^*G_DG_D^+G_D{\bf1}
 ={\bf1}^*G_D{\bf1}
 =\|X\|^2.}                                               \tag{43.4}
\]

No independence or nonsingularity assumption is needed. Thus using every
D-admission probe makes the projection exact, but the proposed sufficient
condition `b_D^*G_D^+b_D >= ||Y||^2` becomes precisely the original packet
inequality `||X||^2>=||Y||^2`. The all-column projection is a reconstruction,
not a new lower bound.

## 3. Affine bookkeeping

For the U packet, define

\[
 a^U=\left(\sqrt{w_n}(\lambda_k,\sqrt{q_k})\right)_{
 A\le n<B,\ k\le K},
\]

and

\[
 z_a^U=\left({\bf1}_{a\le n}\sqrt{w_n}\mu(a)
 \phi_{a,k}\right)_{A\le n<B,\ k\le K}.
\]

Equations (41.7) and (41.9) give

\[
 \boxed{Y=a^U+\sum_{a<B}z_a^U.}                           \tag{43.5}
\]

Hence the U divisor span misses at most one distinguished global affine
generator. On the D side there is no missing affine generator: the `1/a`
part of `c_(a,k)` already reconstructs `ell_n` in (43.3).

If only fresh admissions `A<=a<B` are allowed, put

\[
 O_A=\left(\sqrt{\beta_n}
 (\ell_{A-1}+\lambda_kv_{A-1,k},\sqrt{q_k}v_{A-1,k})
 \right)_{A\le n<B,\ k\le K}.
\]

Then

\[
 \boxed{X=O_A+\sum_{A\le a<B}z_a^D.}                     \tag{43.6}
\]

The one extra vector here is the complete old history compressed into the
block, not an intrinsic D-affine mode. Adding it again makes the projection
exact and therefore tautological.

## 4. Exact loss for a proper selected set

Let `S` be a proper selected set of D columns, `V_S` their span, and write

\[
 X_S=\sum_{a\in S}z_a^D,\qquad
 X_T=\sum_{a\notin S}z_a^D,
 \qquad X=X_S+X_T.
\]

Since `X_S` lies in `V_S`, orthogonal projection gives

\[
 \boxed{
 b_S^*G_S^+b_S
 =\|X\|^2-\|(I-P_{V_S})X_T\|^2.}                          \tag{43.7}
\]

Consequently

\[
 \boxed{
 \|X\|^2-\|Y\|^2
 =b_S^*G_S^+b_S-\|Y\|^2
 +\|(I-P_{V_S})X_T\|^2.}                                 \tag{43.8}
\]

This identifies the entire multiprobe loss exactly. A proper family is useful
only if one can prove, from simpler arithmetic information, that its projected
mass already dominates `||Y||^2`. A family known algebraically to span `X`
only rewrites the original sign question.

## 5. Complete-cell Gram entries and upper frame bounds

The cell inner product expands to

\[
 \langle\phi_{a,k},\phi_{b,k}\rangle
 ={1\over ab}-\lambda_k\left({f_{a,k}\over b}
 +{f_{b,k}\over a}\right)
 +{f_{a,k}f_{b,k}\over k(k+1)}.                          \tag{43.9}
\]

The `lambda_k^2` terms cancel. At finite cutoff write

\[
 G^{0,K}_{a,b}=\sum_{k\le K}
 \langle\phi_{a,k},\phi_{b,k}\rangle.
\]

Then the exact finite-cutoff U-column Gram is

\[
 \langle z_a^U,z_b^U\rangle
 =\mu(a)\mu(b)G^{0,K}_{a,b}
 \sum_{n=\max(A,a,b)}^{B-1}w_n.                          \tag{43.10}
\]

Passing to the complete cell space gives the restricted fractional-part Gram
entry

\[
 \sum_{k\ge1}\langle\phi_{a,k},\phi_{b,k}\rangle
 =G^0_{a,b}=\langle\rho_a,\rho_b\rangle_{L^2(0,1)}.       \tag{43.11}
\]

In particular

\[
 G^0_{a,a}={C_0\over a}-{1\over a^2},
 \qquad C_0=\log(2\pi)-\gamma.                            \tag{43.12}
\]

For complete U columns the exact block Gram is

\[
 \boxed{
 \langle z_a^U,z_b^U\rangle
 =\mu(a)\mu(b)G^0_{a,b}
 \sum_{n=\max(A,a,b)}^{B-1}w_n.}                         \tag{43.13}
\]

For complete D columns one similarly has

\[
 \boxed{
 \langle z_a^D,z_b^D\rangle
 =\mu(a)\mu(b)(\log a)(\log b)G^0_{a,b}
 \sum_{n=\max(A,a,b)}^{B-1}\beta_n.}                    \tag{43.14}
\]

For a probe set `S`, positivity of each active principal Gram matrix and
`lambda_max <= trace` imply the rigorous upper frame bound

\[
 \left\|\sum_{a\in S}r_az_a^U\right\|^2
 \le\Delta_U(A,B;S)\sum_{a\in S}|r_a|^2,                 \tag{43.15}
\]

where

\[
 \boxed{
 \Delta_U(A,B;S)=
 \sum_{n=A}^{B-1}w_n
 \sum_{\substack{a\in S\\a\le n}}\mu(a)^2G^0_{a,a}.} \tag{43.16}
\]

For D columns, the same trace argument gives

\[
 \Delta_D(A,B;S)=\sum_{n=A}^{B-1}\beta_n
 \sum_{\substack{a\in S\\a\le n}}
 \mu(a)^2(\log a)^2G^0_{a,a}.                            \tag{43.17}
\]

Since `beta_n (log a)^2 <= beta_n log n log(n+1)=w_n` when
`a<=n`, one has

\[
 \Delta_D(A,B;S)\le\Delta_U(A,B;S).                      \tag{43.18}
\]

Since the inner trace is at most
`C_0 sum_(a<=n) 1/a - sum_(a<=n) 1/a^2`, the logarithm in it
cancels the `1/log n` in `w_n`; in particular

\[
 \Delta_U(A,B;S)\le C_0\log(B/A)+O(1/\log A+1/A).        \tag{43.19}
\]

Thus both displayed upper frame constants are at most `O(log(B/A))` on
bounded-ratio blocks. This is only a favorable scaling observation, not a
conditioning theorem. The unresolved direction is a lower bound for the signed
Mobius correlation numerator. Generic Gram positivity supplies no such lower
bound.

## 6. Verdict and next finite test

The all-D multiprobe route is algebraically closed by (43.3)--(43.4). The
non-tautological question is whether an arithmetically specified **proper**
subset reaches `b_S^*G_S^+b_S>=||Y||^2` on complete recovery blocks. The next
finite audit should rank proper subsets by admission time, divisor size, and
old/fresh status, record the exact deficit (43.7), and reject any selection
rule that is defined using the desired sign itself. A finite success would
only nominate an arithmetic lemma; it would not prove a uniform block theorem
or RH.
