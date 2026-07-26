# Cycle 40: second-order literature audit for the logarithmic approximant

## 1. Question and answer

Put

\[
 V_N(s)=\sum_{n\leq N}\mu(n)\left(1-\frac{\log n}{\log N}\right)n^{-s}
\]

and

\[
 \mathcal P_N={1\over2\pi}\int_{-\infty}^{\infty}
 \left|1-\zeta(\tfrac12+it)V_N(\tfrac12+it)\right|^2
 {dt\over\tfrac14+t^2}.
\tag{40.1}
\]

The Cycle 39 restricted energy is

\[
 P_N=\mathcal P_N-A_N^2,\qquad
 A_N=\sum_{n\leq N}{\mu(n)\over n}
 \left(1-\frac{\log n}{\log N}\right).
\tag{40.2}
\]

The question is whether the literature proves, even conditionally,

\[
 \mathcal P_N={C_0\over\log N}+{D_{\rm full}\over\log^2N}
 +o(\log^{-2}N),
 \qquad C_0=2+\gamma-\log(4\pi).
\tag{40.3}
\]

Here `C_0=0.046191417932242...`. The answer from the primary sources and the
indexed forward literature is **no**. Bettin--Conrey--Farmer (BCF) prove a
one-term conditional equivalent. Their proof bounds several discarded terms at
`O(log^-2 N)` but neither evaluates their sum nor proves convergence after
rescaling by `log^2 N`. Burnol proves a liminf lower bound for the optimal
distance, not a second term for this fixed polynomial.

## 2. Exact BCF theorem

BCF define

\[
 d_N^2=\inf_{A_N}{1\over2\pi}\int_{-\infty}^{\infty}
 |1-\zeta(\tfrac12+it)A_N(\tfrac12+it)|^2
 {dt\over\tfrac14+t^2},
\tag{40.4}
\]

with the infimum over `A_N(s)=sum_(n=1)^N a_n n^-s`. Their Theorem 1 states:
if RH holds and, for some `delta>0`,

\[
 \sum_{|\Im\rho|\leq T}{1\over|\zeta'(\rho)|^2}
 \ll T^{3/2-\delta},
\tag{40.5}
\]

then the particular polynomial `V_N` satisfies

\[
 \boxed{\mathcal P_N\sim{2+\gamma-\log(4\pi)\over\log N}.}
\tag{40.6}
\]

The sum in (40.5) is over nontrivial zeros. BCF explicitly note immediately
after the theorem that (40.5) implicitly assumes all nontrivial zeros are
simple. RH also supplies the Lindelof-type bounds used in their contour proof.
They quote Gonek's conjecture

\[
 \sum_{|\rho|\leq T}{1\over|\zeta'(\rho)|^2}
 \sim {6\over\pi^3}T
\tag{40.7}
\]

only to motivate the strength of (40.5). It is not another assumption in the
theorem and does not produce a second coefficient. Under RH and simplicity,

\[
 \sum_\rho{1\over|\rho|^2}=2+\gamma-\log(4\pi),
\tag{40.8}
\]

where both conjugate zeros are included.

Primary text: [arXiv:1211.5191](https://arxiv.org/abs/1211.5191). The Russian
original is *Sovremennye Problemy Matematiki* 16 (2012), 38--44, DOI
[10.4213/spm32](https://doi.org/10.4213/spm32). The English translation is
*Proceedings of the Steklov Institute of Mathematics* 280, Suppl. 2 (2013),
30--36, DOI
[10.1134/S0081543813030036](https://doi.org/10.1134/S0081543813030036).

## 3. Why the BCF proof does not determine `D`

BCF Lemma 2 gives unconditionally, for `0<Re s<1`,

\[
 V_N(s)={1\over\zeta(s)}
 \left(1-{1\over\log N}{\zeta'\over\zeta}(s)\right)
 +{1\over\log N}\sum_\rho R_N(\rho,s)
 +{1\over\log N}F_s(1/N),
\tag{40.9}
\]

where

\[
 R_N(\rho,s)=\mathop{\rm Res}_{z=\rho}
 {N^{z-s}\over\zeta(z)(z-s)^2}.
\tag{40.10}
\]

Under RH, simplicity, and (40.5), Lemma 3 gives on
`Re s=1/2+-epsilon`

\[
 \sum_\rho R_N(\rho,s)
 \ll N^{\mp\epsilon}|s|^{3/4-\delta/2+\epsilon}.
\tag{40.11}
\]

In the proof of Theorem 1, all but one residue channel are bounded at
`O(log^-2 N)`. The residue in the distinguished channel is displayed exactly
as

\[
 {1\over|\rho|^2}\left(
 \log N-\frac12{\zeta''(\rho)\over\zeta'(\rho)}
 +{\chi'\over\chi}(\rho)+{1-2\rho\over|\rho|^2}
 \right),
\tag{40.12}
\]

then reduced to its `log N/|rho|^2` part plus an error. After the exterior
factor `1/log^2 N`, BCF obtain

\[
 {1\over\log N}\sum_\rho{1\over|\rho|^2}
 +O(\log^{-2}N)
\tag{40.13}
\]

for this channel and conclude the equivalent (40.6).

At the same second order the proof discards:

- the bounded terms in (40.12), including `zeta''(rho)/zeta'(rho)`;
- the zero--zero quadratic channel
  `sum R_N(rho_1,s) sum R_N(rho_2,1-s)`;
- other mixed logarithmic-derivative/zero channels;
- shifted contour integrals and the entire trivial-zero term.

Some retain `N`-dependence through `N^(rho-s)`. An `O(log^-2 N)` estimate only
shows boundedness at the desired scale; it does not show that

\[
 (\log N)^2\left(\mathcal P_N-{C_0\over\log N}\right)
\tag{40.14}
\]

has a limit. Determining `D_full` requires evaluating the total of all these
channels, proving convergence of the resulting zero sums/correlations, and
improving the residual error to little-oh. Even assuming Gonek's (40.7) does
not by itself do this. No candidate formula for `D_full` appears in BCF.

## 4. Exact Burnol constant and scope

For the continuous Nyman--Beurling distance `D(lambda)`, Burnol proves

\[
 \liminf_{\lambda\to0}D(\lambda)\sqrt{\log(1/\lambda)}
 \geq\left(\sum_{\rho:\Re\rho=1/2}
 {m_\rho^2\over|\rho|^2}\right)^{1/2}.
\tag{40.15}
\]

The sum is over distinct critical-line zeros and weights each by the square of
its multiplicity. Burnol notes that if RH fails the left side is infinite, so
the bound is then trivial; the substantive proof is carried out under RH. Let
`Z_(1/2)` denote the set of distinct critical-line zeros. In the discrete
notation used by BCF, the corresponding squared statement is

\[
 \boxed{\liminf_{N\to\infty}d_N^2\log N\geq
 C_{\rm B}:=\sum_{\rho\in Z_{1/2}}
 {m(\rho)^2\over|\rho|^2}.}
\tag{40.16}
\]

It is conventionally unconditional: off RH the left side is infinite. It is a
lower bound for the optimal distance only. It supplies no upper bound, no
second order, and no fixed-`V_N` theorem beyond `d_N^2<=mathcal P_N`.

Primary source: J.-F. Burnol, *Advances in Mathematics* 170 (2002), 56--70,
DOI [10.1006/aima.2001.2066](https://doi.org/10.1006/aima.2001.2066),
[arXiv:math/0103058](https://arxiv.org/abs/math/0103058).

The predecessor theorem of Baez-Duarte--Balazard--Landreau--Saias has weight
one rather than `m(rho)^2`:

\[
 \liminf d_N^2\log N\geq
 \sum_{\rho\in Z_{1/2}}{1\over|\rho|^2}.
\tag{40.17}
\]

See *Notes sur la fonction zeta de Riemann, 3*, *Advances in Mathematics* 149
(2000), 130--144, DOI
[10.1006/aima.1999.1861](https://doi.org/10.1006/aima.1999.1861).

## 5. Nearby results and forward search

Under RH alone, Balazard--de Roton prove only for the optimal distance

\[
 d_N^2\ll_\epsilon{(\log\log N)^{5/2+\epsilon}\over\sqrt{\log N}}.
\tag{40.18}
\]

This is not a bound for the fixed `V_N`, let alone a two-term asymptotic. See
DOI [10.1142/S1793042110003307](https://doi.org/10.1142/S1793042110003307)
and [arXiv:0812.1689](https://arxiv.org/abs/0812.1689).

Baez-Duarte obtains RH-conditional convergence for a different exponential
damping, not the logarithmic taper: [arXiv:math/0205003](https://arxiv.org/abs/math/0205003).
Later indexed papers citing BCF concern generalized criteria, zero-free
regions, cotangent sums, or Gram representations. Werner Ehm's recent exact
Gram-matrix work does not state a `D` asymptotic:
[arXiv:2405.06349](https://arxiv.org/abs/2405.06349).

Searches covered the primary BCF/Burnol chain, arXiv's Nyman--Beurling corpus,
Crossref/OpenAlex records, and Google Scholar forward citations through the
search date. No two-term theorem for (40.1) was located. This cannot exclude an
unindexed or unpublished result, but it supports the precise literature claim:
`D_full` is not known from the standard published chain, even under the BCF
hypotheses or Gonek's conjecture.

## 6. Full versus restricted coefficient

Writing `M_1(x)=sum_(n<=x) mu(n)/n`, partial summation gives

\[
 A_N={1\over\log N}\int_1^N{M_1(x)\over x}\,dx.
\tag{40.19}
\]

The classical zero-free-region estimate and
`int_1^infinity M_1(x)dx/x=1` yield

\[
 A_N={1\over\log N}+o(1/\log N),\qquad
 A_N^2={1\over\log^2N}+o(\log^{-2}N).
\tag{40.20}
\]

Therefore, if either two-term expansion exists, so does the other, with

\[
 \boxed{D_{\rm restricted}=D_{\rm full}-1.}
\tag{40.21}
\]

For the Cycle 39 critical tail transform this would give

\[
 P_N-\sum_{n\geq N}w_nP_n
 ={D_{\rm full}-1\over2\log^2N}+o(\log^{-2}N).
\tag{40.22}
\]

Thus even a hypothetical positive `D_full` would not establish the restricted
reverse-tail inequality; one needs `D_full>1` (or a direct signed estimate).

## 7. Verdict

1. Burnol gives the unconditional optimal-distance liminf constant
   `sum m(rho)^2/|rho|^2`, with no second term.
2. RH plus (40.5), implicitly including simplicity, gives BCF's fixed-taper
   first-order law with exact constant `2+gamma-log(4pi)`.
3. BCF expose but only bound contributions of order `log^-2 N`; big-oh does not
   define a second coefficient.
4. No conditional or unconditional value of `D_full` was located. Hence
   `D_restricted=D_full-1` and the critical tail-surplus sign remain unknown.
5. Progress requires a new evaluation of the second-scale residue, zero--zero,
   mixed, and contour channels, or a different signed estimate.

Search date: 2026-07-26.
