# Cycle 248: fixed dyadic contraction is impossible

## Decision

For the Cycle 247 logarithmic Nyman--Beurling energies, every eventual fixed
dyadic contraction factor is ruled out unconditionally. More precisely, for
every integer `N_0>=3` and every real `q<1`,

\[
 P_{2^{j+1}N_0}\leq qP_{2^jN_0}
\]

fails for infinitely many `j`. Thus the cofinal hypothesis proposed in Cycle
242 cannot hold for this approximant, whether or not RH is true. This is an
exact asymptotic obstruction, not an extrapolation from the Cycle 247 finite
ratios.

Under the stronger Bettin--Conrey--Farmer hypotheses, the precise first-order
law gives

\[
 {P_{2N}\over P_N}\sim {\log N\over\log(2N)}\longrightarrow1.
\]

RH alone is not known to give this ratio asymptotic for the fixed taper. That
literature gap does not weaken the unconditional no-fixed-`q` theorem.

## Unconditional lower barrier

For an integer `N>=2`, define

\[
 d_N^2=\inf_{Q(s)=\sum_{n=1}^Nq_nn^{-s}}{1\over2\pi}
 \int_{-\infty}^{\infty}
 |1-\zeta(\tfrac12+it)Q(\tfrac12+it)|^2
 {dt\over\tfrac14+t^2},                              \tag{248.1}
\]

where the coefficients `q_n` are arbitrary complex numbers and degree at most
`N` is allowed. Put

\[
 V_N(s)=\sum_{n=1}^N\mu(n)
 \left(1-{\log n\over\log N}\right)n^{-s}
\]

and define its complete energy by

\[
 \mathcal P_N={1\over2\pi}\int_{-\infty}^{\infty}
 |1-\zeta(\tfrac12+it)V_N(\tfrac12+it)|^2
 {dt\over\tfrac14+t^2}.                              \tag{248.2}
\]

The endpoint coefficient at `n=N` is zero, but this still makes `V_N` an
admissible polynomial of length at most `N`; hence `d_N^2<=mathcal P_N` with
no index shift. The discrete Báez-Duarte--Balazard--Landreau--Saias lower
bound, sharpened by Burnol's multiplicity argument, is

\[
 \liminf_{N\to\infty}d_N^2\log N\geq C_{\rm B},
 \qquad
 C_{\rm B}=\sum_{\substack{\rho:\Re\rho=1/2\\
                     \rho\ {\rm distinct}}}
 {m(\rho)^2\over|\rho|^2}>0.                         \tag{248.3}
\]

Positivity needs no RH: the existence of critical-line zeros is known. Since
the fixed logarithmic polynomial is admissible, the comparison is exactly

\[
 d_N^2\leq\mathcal P_N.
\]

For clarity, set

\[
 c_a(N)=\mu(a){\log(N/a)\over\log N},\qquad
 F_N(x)=1_{(0,1)}(x)+\sum_{a\leq N}c_a(N)\{1/(ax)\},
\]

and define the restricted energy and scalar tail by

\[
 P_N=\int_0^1|F_N(x)|^2\,dx,\qquad
 A_N=V_N(1)=\sum_{a\leq N}{c_a(N)\over a}.
\]

The Mellin transform is
`\widehat F_N(s)=(1-zeta(s)V_N(s))/s`; in particular there is no sign
change in `c_a(N)`. Also `F_N(x)=A_N/x` for `x>1`. Mellin--Plancherel and the
tail integral therefore give the exact normalization

\[
 \boxed{\mathcal P_N=\|F_N\|_{L^2(0,\infty)}^2=P_N+A_N^2.} \tag{248.4}
\]

Writing `M_1(x)=sum_(n<=x)mu(n)/n`, partial summation gives

\[
 A_N={1\over\log N}\int_1^N{M_1(x)\over x}\,dx.       \tag{248.5}
\]

The prime-number-theorem zero-free-region estimate for `M_1`, together with
`int_1^infinity M_1(x)dx/x=1` (equivalently
`1/zeta(1+s)~s` as `s->0+`), yields

\[
 A_N={1\over\log N}+o(1/\log N).                       \tag{248.6}
\]

Thus the sign in the restriction formula is `P_N=mathcal P_N-A_N^2`, and
`A_N^2 log N -> 0`. Consequently

\[
 \boxed{\liminf_{N\to\infty}P_N\log N\geq C_{\rm B}>0.} \tag{248.7}
\]

In particular, for any fixed `c` with `0<c<C_B`, there is `N_c` such that

\[
 P_N\geq {c\over\log N}\qquad(N\geq N_c).             \tag{248.8}
\]

## No-fixed-contraction theorem

**Theorem 248.1.** Fix `N_0>=3` and `q<1`. There is no `J` such that

\[
 P_{2^{j+1}N_0}\leq qP_{2^jN_0}\qquad(j\geq J).       \tag{248.9}
\]

Equivalently,

\[
 \boxed{\limsup_{j\to\infty}
 {P_{2^{j+1}N_0}\over P_{2^jN_0}}\geq1.}              \tag{248.10}
\]

*Proof.* By (248.8), the energies are strictly positive at every sufficiently
large scale, so `q<=0` is immediately impossible. Suppose `0<q<1`. If (248.9)
held, iteration would give

\[
 P_{2^jN_0}\leq P_{2^JN_0}q^{j-J}.                   \tag{248.11}
\]

Multiplication by
`log(2^jN_0)=log N_0+j log 2` shows that the right-hand side times the
logarithm tends to zero. Hence

\[
 \liminf_{j\to\infty}P_{2^jN_0}\log(2^jN_0)=0,
\]

contradicting (248.7), which applies to every subsequence. Therefore (248.9)
is impossible. Since this holds for every `q<1`, (248.10) follows. QED.

The same proof rules out the stronger assertion `P_(2N)<=qP_N` for every
sufficiently large integer `N`, because restricting it to any dyadic ray would
give (248.9).

## Consequence for the Cycle 247 recurrence

Cycle 247 proved, with `L=log N`, `h=log 2`, and
`alpha_N=L/(L+h)`,

\[
 P_{2N}=\alpha_N^2P_N+2\alpha_NC_N+B_N.              \tag{248.12}
\]

For fixed `q<1`, contraction is exactly

\[
 C_N\leq
 {\bigl(q-\alpha_N^2\bigr)P_N-B_N\over2\alpha_N}.   \tag{248.13}
\]

Theorem 248.1 therefore proves that (248.13) fails infinitely often on every
dyadic ray. The signed old/new interaction cannot meet the fixed geometric
threshold cofinally. This conclusion uses the complete energy lower barrier;
it does not require separate estimates for `C_N` and `B_N`, and the recurrence
alone does not provide such estimates.

The result also corrects the logical status of the Cycle 242 transfer lemma.
That lemma remains a valid implication: its hypothesis would imply RH. But its
hypothesis is now unconditionally false for these energies, because it would
force decay faster than the universal Nyman--Beurling `1/log N` floor.

## Strong conditional asymptotic

Bettin--Conrey--Farmer prove for this exact logarithmic taper that, if RH holds
and there is a `delta>0` such that

\[
 \sum_{\substack{\rho\ \text{ nontrivial}\\|\Im\rho|\leq T}}
 {1\over|\zeta'(\rho)|^2}\ll T^{3/2-\delta},           \tag{248.14}
\]

then

\[
 \mathcal P_N\sim {C_0\over\log N},
 \qquad C_0=2+\gamma-\log(4\pi).                     \tag{248.15}
\]

This is the primary source's two-sided ordinate convention; replacing it by a
positive-ordinate `J_-1(T)` changes only an inessential factor of two in the
hypothesis. As BCF explicitly state, (248.14) implicitly assumes every
nontrivial zero is simple: at a multiple zero `zeta'(rho)=0`, so the displayed
finite moment bound cannot hold. It is strictly additional to RH. Removing
`A_N^2=O(1/log^2 N)` preserves the
first-order law, so

\[
 P_N\sim {C_0\over\log N}.                            \tag{248.16}
\]

It follows that

\[
 \boxed{{P_{2N}\over P_N}\sim
 {\log N\over\log N+\log2}\longrightarrow1.}         \tag{248.17}
\]

Thus under (248.15), every fixed `q<1` fails not merely infinitely often but at
every sufficiently large `N`. Substitution in (248.12) also gives only

\[
 {2\alpha_NC_N+B_N\over P_N}
 ={P_{2N}\over P_N}-\alpha_N^2\longrightarrow0.       \tag{248.18}
\]

The first-order theorem does not determine a sign or a `1/log N`-accurate
second term for this normalized recurrence residual.

## Exact wall

1. `UNCONDITIONAL THEOREM`: no fixed `q<1` contracts all sufficiently late
   links of any dyadic ray.
2. `STRONG CONDITIONAL THEOREM`: under RH plus the Bettin--Conrey--Farmer
   reciprocal-derivative moment bound, the dyadic ratio tends to one.
3. `RH-ALONE LITERATURE WALL`: no known theorem gives convergence or a
   first-order law for this exact fixed taper from RH alone.
4. The Cycle 247 finite ratios neither prove nor motivate the conclusion; the
   proof is entirely the published asymptotic lower barrier plus iteration.
5. Any viable dyadic decay statement must have contraction factors tending to
   one, with nonsummable cumulative loss if it is intended to force vanishing.

No Riemann-hypothesis result is claimed.

## References

Primary-source normalization checks: BCF, Introduction and Theorem 1, defines
`d_N^2`, `V_N`, (248.14), and (248.15) exactly as used here, and quotes the
discrete BDBLS/Burnol bounds with sums over distinct critical-line zeros.
Burnol, Theorems 1.2, 1.3, and 5.5, states the continuous distance bound before
squaring, with `sqrt(log(1/lambda))` and the square root of
`sum m(rho)^2/|rho|^2`; this is consistent with (248.3), not an extra factor of
two. The full/restricted identity (248.4) is an exact Mellin--Plancherel and
`x>1` tail calculation, not a theorem imported with a changed convention.

- L. Báez-Duarte, M. Balazard, B. Landreau, E. Saias, *Notes sur la fonction
  zeta de Riemann, 3*, Adv. Math. 149 (2000), 130--144.
- J.-F. Burnol, *A lower bound in an approximation problem involving the zeros
  of the Riemann zeta function*, Adv. Math. 170 (2002), 56--70;
  arXiv:math/0103058.
- S. Bettin, J. B. Conrey, D. W. Farmer, *An optimal choice of Dirichlet
  polynomials for the Nyman--Beurling criterion*, Proc. Steklov Inst. Math. 280
  Suppl. 2 (2013), 30--36; arXiv:1211.5191.
