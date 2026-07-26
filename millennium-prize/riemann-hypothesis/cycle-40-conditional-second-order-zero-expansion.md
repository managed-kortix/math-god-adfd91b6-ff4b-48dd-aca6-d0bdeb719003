# Cycle 40: conditional second-order zero expansion for the logarithmic taper

## 1. Exact starting identity

Put `L=log N` and

\[
 V_N(s)=\sum_{n\leq N}\mu(n)\left(1-\frac{\log n}{L}\right)n^{-s}.
\]

For `0<Re(s)<1`, the exact Bettin--Conrey--Farmer contour shift gives

\[
 V_N(s)=\frac1{\zeta(s)}\left(1-\frac1L\frac{\zeta'}{\zeta}(s)\right)
 +\frac1L Z_N(s)+\frac1L H_N(s),                                      \tag{40.1}
\]

where

\[
 Z_N(s)=\sum_\rho R_N(\rho,s),\qquad
 R_N(\rho,s)=\mathop{\rm Res}_{z=\rho}
 \frac{N^{z-s}}{\zeta(z)(z-s)^2},                                    \tag{40.2}
\]

and

\[
 H_N(s)=F_s(1/N),\qquad
 F_s(z)=\pi z^s\sum_{m\geq1}
 \frac{(-1)^m(2\pi)^{2m+1}z^{2m}}
 {(2m)!\zeta(2m+1)(2m+s)^2}.                                         \tag{40.3}
\]

Zeros in (40.2) are distinct; for a zero of multiplicity greater than one,
`R_N` means the full residue, not the simple-zero expression. Under simplicity,

\[
 R_N(\rho,s)=\frac{N^{\rho-s}}{\zeta'(\rho)(\rho-s)^2}.                \tag{40.4}
\]

Set

\[
 A(s)=\frac{\zeta'}{\zeta^2}(s),\qquad B_N(s)=A(s)-Z_N(s)-H_N(s).
\]

Then

\[
 1-\zeta(s)V_N(s)=\frac{\zeta(s)}L B_N(s),                            \tag{40.5}
\]

and the complete Mellin norm is exactly

\[
 \mathcal P_N=\frac1{L^2}\mathscr K_N,
 \quad
 \mathscr K_N=\frac1{2\pi i}\int_{(1/2-\epsilon)}
 B_N(s)B_N(1-s)\frac{\zeta(s)\zeta(1-s)}{s(1-s)}\,ds.                \tag{40.6}
\]

This identity, rather than an asymptotic replacement of `V_N`, is the starting
point.

## 2. Cutoff convention and explicit strong hypotheses

Every zero expression below is first formed with the symmetric cutoff
`|Im rho|<=T`. No unqualified infinite zero sum is used. Let `Z_(N,T)` denote
that finite sum and let `mathscr K_(N,T)` be (40.6) with `Z_N` replaced by
`Z_(N,T)`.

The following hypotheses are deliberately stronger than the published
first-order theorem.

**H1 (RH and simplicity).** Every nontrivial zero is simple and has the form
`rho=1/2+i gamma`.

**H2 (uniform zero realization).** For one fixed `0<epsilon<1/2`, the symmetric
zero sums in (40.1) converge on both lines `Re(s)=1/2+-epsilon` in a weighted
space strong enough to pass `T->infinity` through (40.6), all stated contour
shifts, and all pair products. A sufficient version may be imposed by absolute
majorants for the one-zero and two-zero integrands. The usual estimate

\[
 \sum_{|\gamma|\leq T}|\zeta'(\rho)|^{-2}\ll T^{3/2-\delta}            \tag{40.7}
\]

is enough for the known first-order argument, but is not asserted here to be
enough for these second-order passages.

**H3 (combined finite-part convergence).** After the exceptional affine--zero
channel is shifted across the critical line, the iterated symmetric-cutoff
limit

\[
 D_{\rm full}:=
 \lim_{N\to\infty}\lim_{T\to\infty}
 \left(\mathscr K_{N,T}-C_0L\right)                                 \tag{40.8}
\]

exists as a finite real number. Here

\[
 C_0=\sum_\rho^{\rm sym}\frac1{|\rho|^2}
     =2+\gamma-\log(4\pi)                                           \tag{40.9}
\]

under H1. The finite pole packet `B_pole(T)` is displayed in (40.12) below,
but H3 requires convergence only after it is recombined with every regular,
zero--zero, and endpoint packet. Hypothesis H3 includes, rather than proves,
cancellation or convergence of every nonzero-frequency factor
`N^{i(gamma_1+gamma_2)}` in the zero--zero channel. This qualification is
essential: (40.7) alone supplies only an `O(L^-2)` remainder and does not force
a constant second coefficient.

**H4 (endpoint domination).** The terms containing `H_N` have a finite limit
after the operations in H2. For the exact entire endpoint packet (40.3), a
uniform dominated estimate implying that limit is zero is sufficient.

These hypotheses are explicit bookkeeping assumptions, not known theorems.

## 3. Channel decomposition

For

\[
 \mathcal I(X,Y)=\frac1{2\pi i}\int_{(1/2-\epsilon)}
 X(s)Y(1-s)\frac{\zeta(s)\zeta(1-s)}{s(1-s)}\,ds,                    \tag{40.10}
\]

finite symmetric cutoffs give the exact expansion

\[
\begin{aligned}
 \mathscr K_{N,T}={}&\mathcal I(A,A)
 -\mathcal I(A,Z_{N,T})-\mathcal I(Z_{N,T},A)
 +\mathcal I(Z_{N,T},Z_{N,T})\\
 &-\mathcal I(A,H_N)-\mathcal I(H_N,A)
 +\mathcal I(Z_{N,T},H_N)+\mathcal I(H_N,Z_{N,T})
 +\mathcal I(H_N,H_N).
\end{aligned}                                                        \tag{40.11}
\]

In particular the genuinely quadratic zero packet is the explicit finite sum

\[
 \mathcal I(Z_{N,T},Z_{N,T})
 =\sum_{\substack{|\Im\rho|\leq T\\|\Im\sigma|\leq T}}
 \frac{N^{\rho+\sigma-1}}{\zeta'(\rho)\zeta'(\sigma)}
 J(\rho,\sigma),                                                     \tag{40.11a}
\]

where

\[
 J(\rho,\sigma)=\frac1{2\pi i}\int_{(1/2-\epsilon)}
 \frac{\zeta(s)\zeta(1-s)}
 {s(1-s)(\rho-s)^2(\sigma-1+s)^2}\,ds.                              \tag{40.11b}
\]

On RH its scale factor is `N^{i(gamma_rho+gamma_sigma)}`. The conjugate pairs
`sigma=bar rho` are the zero-frequency part; all same-sign and nonconjugate
pairs remain in (40.11a). Likewise, the affine--zero terms are finite one-zero
sums obtained by inserting

\[
 Z_{N,T}(s)=\sum_{|\Im\rho|\leq T}
 \frac{N^{\rho-s}}{\zeta'(\rho)(\rho-s)^2}                           \tag{40.11c}
\]

into (40.10). This is more precise than treating their regular parts as an
unspecified error.

Thus the second coefficient retains four logically different packets:

1. the affine term `I(A,A)` and the regular parts of the two affine--zero
   cross terms;
2. the full zero--zero double sum, including conjugate, same-sign, and
   off-diagonal pairs;
3. the entire/trivial-zero endpoint terms containing `H_N`;
4. the finite part of the poles crossed in the exceptional affine--zero term.

For the convention `zeta(s)=chi(s)zeta(1-s)`, the pole at a simple zero
`rho` contributes `L/|rho|^2` plus the finite part

\[
 b_\rho=
 \frac1{|\rho|^2}\left(
 -\frac12\frac{\zeta''(\rho)}{\zeta'(\rho)}
 +\frac{\chi'}{\chi}(\rho)
 +\frac{1-2\rho}{|\rho|^2}\right),
 \qquad
 B_{\rm pole}(T)=\sum_{|\Im\rho|\leq T}b_\rho.                      \tag{40.12}
\]

Conjugate zeros make the symmetric finite sum real. We do not claim that the
infinite series of `b_rho` converges; H3 concerns its symmetric finite-part
combination with all remaining channels.

It is useful to display the coefficient without hiding that combination. At
finite `N,T`, define

\[
\begin{aligned}
 D_{\rm aff}(N,T)&=\mathcal I(A,A)-\mathcal I(A,Z_{N,T})
                  -\mathcal I(Z_{N,T},A)-C_0L-B_{\rm pole}(T),\\
 D_{00}(N,T)&=\mathcal I(Z_{N,T},Z_{N,T}),\\
 D_{\rm end}(N,T)&=-\mathcal I(A,H_N)-\mathcal I(H_N,A)
 +\mathcal I(Z_{N,T},H_N)+\mathcal I(H_N,Z_{N,T})
 +\mathcal I(H_N,H_N).
\end{aligned}                                                        \tag{40.13}
\]

Equations (40.8)--(40.13) give the convergence-safe channel formula

\[
 \boxed{D_{\rm full}=\lim_{N\to\infty}\lim_{T\to\infty}
 \{B_{\rm pole}(T)+D_{\rm aff}(N,T)+D_{00}(N,T)+D_{\rm end}(N,T)\}}.\tag{40.14}
\]

No limit of any displayed summand is claimed separately. Equivalently,

\[
 \boxed{D_{\rm full}=\lim_{N\to\infty}\lim_{T\to\infty}
       (\mathscr K_{N,T}-C_0\log N)}.                                \tag{40.15}
\]

Formula (40.14) records the zero, affine, and endpoint content while requiring
their combined limit; formula (40.15) is the compressed equivalent.

## 4. Conditional expansion and rank-one correction

By (40.6), H1--H4 imply

\[
 \boxed{\mathcal P_N=\frac{C_0}{\log N}
 +\frac{D_{\rm full}}{\log^2N}+o(\log^{-2}N).}                       \tag{40.16}
\]

The restricted Nyman--Beurling energy is

\[
 P_N=\mathcal P_N-A_N^2,
 \qquad
 A_N=\sum_{n\leq N}\frac{\mu(n)}n
 \left(1-\frac{\log n}{\log N}\right).                            \tag{40.17}
\]

The zero-free region gives

\[
 A_N=\frac1{\log N}+o(\log^{-1}N),
 \qquad A_N^2=\frac1{\log^2N}+o(\log^{-2}N).                        \tag{40.18}
\]

Therefore the exact omitted-tail rank-one square shifts only the second
coefficient:

\[
 \boxed{P_N=\frac{C_0}{\log N}
 +\frac{D_{\rm restricted}}{\log^2N}+o(\log^{-2}N),\qquad
 D_{\rm restricted}=D_{\rm full}-1.}                                \tag{40.19}
\]

## 5. Sign target

For the critical tail

\[
 T_N=\sum_{n\geq N}
 \left(\frac1{\log n}-\frac1{\log(n+1)}\right)\log n\,P_n,
\]

the Cycle 39 transform gives, conditionally on (40.19) with its pointwise
little-oh remainder,

\[
 P_N-T_N=\frac{D_{\rm restricted}}{2\log^2N}
 +o(\log^{-2}N).                                                     \tag{40.20}
\]

Hence the desired eventual reverse-tail inequality `P_N>=T_N` has the strict
second-order target

\[
 \boxed{D_{\rm restricted}>0,\quad\text{equivalently}\quad
 D_{\rm full}>1.}                                                    \tag{40.21}
\]

If `D_full<1`, the inequality is eventually reversed. If `D_full=1`, the
second order is inconclusive. If the nonzero-frequency zero pairs leave a
bounded oscillatory coefficient instead of a limit, there is no scalar `D`;
one must prove the pointwise lower target

\[
 \liminf_{N\to\infty}
 \{\mathscr K_N-C_0\log N-1\}>0                                    \tag{40.22}
\]

(with a margin adequate for the remainder), rather than quote a two-term
expansion.

## 6. Verdict

The exact Mellin formula does identify the candidate second-order coefficient:
it is the finite part of a pole zero sum plus the affine, zero--zero, and
endpoint channels, followed by the `-1` restricted rank-one correction. The
sign needed by the critical renewal inequality is `D_full>1`. The published
reciprocal-derivative hypothesis proves the first coefficient but neither the
existence of the finite-part limit in (40.15) nor its sign. No unconditional,
RH-only, or literature-proved second-order convergence is claimed here.
