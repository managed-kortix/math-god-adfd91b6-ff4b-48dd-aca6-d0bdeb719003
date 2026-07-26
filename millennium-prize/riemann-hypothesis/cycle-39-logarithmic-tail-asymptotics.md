# Cycle 39: logarithmic Nyman--Beurling tails and the critical constant

## 1. Normalization

Put

\[
 V_N(s)=\sum_{n\leq N}\mu(n)
 \left(1-\frac{\log n}{\log N}\right)n^{-s},
\]

and let

\[
 \mathcal P_N={1\over2\pi}\int_{-\infty}^{\infty}
 \left|1-\zeta(\tfrac12+it)V_N(\tfrac12+it)\right|^2
 {dt\over\tfrac14+t^2}.
\tag{39.1}
\]

Under the Mellin realization of the Nyman--Beurling space this is the complete
`L^2(0,infinity)` norm of the logarithmically tapered approximant. The
restricted energy used in the renewal calculations is

\[
 P_N=\mathcal P_N-A_N^2,
 \qquad
 A_N=\sum_{n\leq N}{\mu(n)\over n}
 \left(1-\frac{\log n}{\log N}\right).
\tag{39.2}
\]

The zero-free region gives unconditionally

\[
 A_N={1\over\log N}+o(1/\log N),
\tag{39.3}
\]

with a Vinogradov--Korobov error. Hence

\[
 \boxed{P_N=\mathcal P_N+O(1/\log^2N).}
\tag{39.4}
\]

Every first-order `C/log N` statement therefore has the same constant in the
full and restricted normalizations. This distinction matters for exact finite
Gram calculations but not for first-order analysis.

Write

\[
 w_n=\left({1\over\log n}-{1\over\log(n+1)}\right)\log n
 ={\log(1+1/n)\over\log(n+1)}.
\tag{39.5}
\]

The proposed tail inequality is

\[
 P_a\geq2\kappa\sum_{n\geq a}w_nP_n.
\tag{39.6}
\]

The value `kappa=1/2` is therefore the coefficient-one inequality

\[
 \boxed{P_a\geq T_a:=\sum_{n\geq a}w_nP_n.}
\tag{39.7}
\]

## 2. The logarithmic tail transform

The weight has the elementary expansion

\[
 w_n={1\over n\log n}
 +O\left({1\over n^2\log n}+{1\over n^2\log^2n}\right).
\tag{39.8}
\]

**Lemma 39.1.** If

\[
 P_n={C\over\log n}+o(1/\log n)
\tag{39.9}
\]

for some finite `C`, then

\[
 T_a={C\over\log a}+o(1/\log a),
 \qquad {T_a\over P_a}\longrightarrow1
\tag{39.10}
\]

when `C>0`.

*Proof.* Given `epsilon>0`, (39.9) bounds the tail between
`(C-epsilon)/log n` and `(C+epsilon)/log n`. In fact the normalization was
chosen so that the relevant sum telescopes exactly:

\[
 \sum_{n\geq a}{w_n\over\log n}
 =\sum_{n\geq a}\left({1\over\log n}-{1\over\log(n+1)}\right)
 ={1\over\log a}.
\tag{39.11}
\]

The squeeze gives (39.10). QED.

More generally, if

\[
 P_n\sim C(\log n)^{-\alpha},\qquad C>0,\quad\alpha>0,
\tag{39.12}
\]

then the same argument, or Karamata's theorem after `u=log x`, gives

\[
 \boxed{T_a\sim {1\over\alpha}P_a.}
\tag{39.13}
\]

Thus a tail inequality with coefficient `c=2 kappa` is asymptotically
compatible with this model exactly when `c<=alpha`. The expected exponent is
`alpha=1`; accordingly `kappa=1/2` is critical, not supercritical.

Indeed `P_n=C/log n` is not merely an asymptotic model: by (39.11) it satisfies
`P_a=T_a` exactly at every start. This is the equality profile selected by the
normalization.

At the critical exponent the leading constants cancel completely:

\[
 P_a-T_a=o(1/\log a).
\tag{39.14}
\]

Neither the sign nor the scale of this residual follows from a first-order
asymptotic. A claimed contradiction based only on the Burnol constant therefore
loses one full asymptotic order.

## 3. What is known and what is conditional

Let `d_N` be the optimal Nyman--Beurling distance among Dirichlet polynomials
of length `N`. Since (39.1) is one admissible polynomial,

\[
 d_N^2\leq\mathcal P_N.
\tag{39.15}
\]

Báez-Duarte--Balazard--Landreau--Saias, sharpened by Burnol, proved the
unconditional lower bound

\[
 \liminf_{N\to\infty}d_N^2\log N
 \geq C_{\rm B}:=
 \sum_{\substack{\rho:\,\Re\rho=1/2\\\rho\ {\rm distinct}}}
 {m(\rho)^2\over|\rho|^2}.
\tag{39.16}
\]

It follows from (39.4) and (39.15) that

\[
 \boxed{\liminf_{N\to\infty}P_N\log N\geq C_{\rm B}.}
\tag{39.17}
\]

Notice that (39.16) sums only critical-line zeros; by itself it neither asserts
RH nor gives an upper bound for this fixed taper.

The expected sharp law is

\[
 d_N^2\sim {C_{\rm B}\over\log N}.
\tag{39.18}
\]

For the particular logarithmic polynomial `V_N`, Bettin--Conrey--Farmer prove,
assuming RH and

\[
 \sum_{|\Im\rho|\leq T}{1\over|\zeta'(\rho)|^2}
 \ll T^{3/2-\delta},
\tag{39.19}
\]

that

\[
 \mathcal P_N\sim {C_0\over\log N},
 \qquad C_0=2+\gamma-\log(4\pi).
\tag{39.20}
\]

Condition (39.19) implicitly assumes that every nontrivial zero is simple.
Under simplicity and RH,

\[
 C_{\rm B}=\sum_\rho{1\over|\rho|^2}
 =2+\gamma-\log(4\pi)=C_0.
\tag{39.21}
\]

Equations (39.4), (39.20), and Lemma 39.1 therefore show that, under the
Bettin--Conrey--Farmer hypotheses,

\[
 P_a\sim T_a\sim {C_0\over\log a}.
\tag{39.22}
\]

This supports the size and sharpness of `kappa=1/2`; it does not prove the
one-sided inequality `P_a>=T_a`, whose truth depends on the next term and on
oscillation.

Under RH alone, Balazard--de Roton prove for the optimal distance only

\[
 d_N^2\ll_\epsilon
 { (\log\log N)^{5/2+\epsilon}\over\sqrt{\log N}}.
\tag{39.23}
\]

This is not an upper bound for the fixed polynomial (39.1). Báez-Duarte proves
convergence under RH for a differently damped explicit family, again not
(39.1). These results supply no RH-alone convergence or first-order asymptotic
for the exact taper used here.

## 4. Rigorous implications of the critical tail inequality

Assume (39.7) for every `a>=a_0`. Then every conclusion below is unconditional
given that inequality.

First, `T_(a_0)<=P_(a_0)<infinity`, so

\[
 \sum_{n\geq a_0}w_nP_n<\infty.
\tag{39.24}
\]

Since `sum w_n=infinity`, (39.24) gives `liminf P_n=0`. The previously proved
off-critical-zero floor then gives RH. Thus (39.7) is at least RH-strength.

Second, after RH is known, (39.17) has `C_B>0`. For each `epsilon>0`, eventually

\[
 P_n\geq{C_{\rm B}-\epsilon\over\log n}.
\tag{39.25}
\]

Inserting this lower bound into `T_a` and using (39.11) yields

\[
 T_a\geq{C_{\rm B}-\epsilon\over\log a}
 +o(1/\log a).
\tag{39.26}
\]

The tail inequality therefore reproduces

\[
 \liminf_{a\to\infty}P_a\log a\geq C_{\rm B},
\tag{39.27}
\]

the already known Burnol lower constant, not a larger one. There is no
multiplicity contradiction at first order.

Third, the tail inequality is stronger than the presently known consequences
of RH for this approximant. RH is a zero-location assertion; (39.7) additionally
gives weighted summability and a pointwise reverse Hardy constraint at every
start. Existing literature does not derive either from RH alone. Absent a
separation theorem, the precise statement is "RH plus a new fixed-approximant
regularity/dissipation theorem not known to follow from RH," not a claim of
formal logical independence.

Fourth, if the full adaptive-renewal assertion is desired, (39.7) and
summability are not quite sufficient at equality indices. With

\[
 Q_a=P_a-T_a,
\tag{39.28}
\]

the exact Cycle 38 characterization additionally requires that the zero set
`{a:Q_a=0}` have no largest element. Strict inequality eventually removes this
boundary issue.

## 5. Multiplicity audit

The Burnol constant weights a zero of multiplicity `m` by `m^2`, not `m`:

\[
 C_{\rm B}=\sum_{\rho\ {\rm distinct}}{m(\rho)^2\over|\rho|^2}.
\tag{39.29}
\]

Under RH the Hadamard product gives the linearly weighted identity

\[
 \sum_{\rho\ {\rm distinct}}{m(\rho)\over|\rho|^2}
 =C_0=2+\gamma-\log(4\pi).
\tag{39.30}
\]

Therefore

\[
 C_{\rm B}=C_0+
 \sum_{\rho\ {\rm distinct}}{m(\rho)(m(\rho)-1)\over|\rho|^2}
 \geq C_0,
\tag{39.31}
\]

with equality exactly when all nontrivial zeros are simple.

This does not conflict with `kappa=1/2`. If the true first-order law is
`P_N~C_B/log N`, then its tail has the same constant `C_B`; (39.7) is saturated
to first order for every finite value of `C_B`, simple or multiple. The factor
`m^2` changes amplitude, while the critical tail operator tests the logarithmic
decay exponent.

Nor does (39.7), even combined with a coarse upper bound
`P_N<=C/log N`, force simplicity unless the numerical upper constant is at
most `C_0`. Indeed (39.17) gives only `C_B<=C`. Conversely, the sharp upper law

\[
 \limsup P_N\log N\leq C_0
\tag{39.32}
\]

would combine with (39.17) and (39.31) to force every zero simple (and, because
`P_N->0`, RH). That simplicity implication comes from the sharp constant
`C_0`, not from `kappa=1/2`.

The Bettin--Conrey--Farmer theorem is consistent with this audit: its reciprocal
derivative hypothesis assumes simplicity before obtaining the constant `C_0`.
It cannot be used to argue that (39.20) independently proves simplicity.

## 6. Second-order criterion at the critical boundary

Suppose, more strongly, that

\[
 P_N={C\over L}+{D\over L^2}+o(L^{-2}),
 \qquad L=\log N.
\tag{39.33}
\]

Since `w_n/log n` telescopes exactly and

\[
 \sum_{n\geq N}{w_n\over\log^2n}
 ={1\over2\log^2N}+o(1/\log^2N),
\]

summation of (39.33) gives

\[
 T_N=\int_L^\infty
 \left({C\over u}+{D\over u^2}+o(u^{-2})\right){du\over u}
 ={C\over L}+{D\over2L^2}+o(L^{-2}).
\tag{39.34}
\]

Hence

\[
 \boxed{P_N-T_N={D\over2\log^2N}+o(1/\log^2N).}
\tag{39.35}
\]

A two-term expansion would support eventual `kappa=1/2` when its second
coefficient is positive, contradict it when that coefficient is negative, and
remain inconclusive when it vanishes or oscillations dominate. For the
restricted energy, subtracting `A_N^2~1/log^2N` shifts this second coefficient
by `-1`; full versus restricted normalization becomes critical precisely at
the order needed to decide (39.7).

No cited theorem supplies the required second term with a signed error for the
fixed logarithmic taper. This, rather than zero multiplicity, is the sharp
literature-level obstruction.

## 7. Verdict

1. The known/conditional first-order scale is `P_N` of order `1/log N`.
2. The tail operator sends `C/log N` to the same `C/log N`; therefore
   `kappa=1/2` is the critical, asymptotically saturated value.
3. The inequality would prove RH and substantial fixed-approximant regularity,
   but it does not force simplicity or contradict Burnol's `m^2` constant.
4. Multiplicity changes the leading amplitude and is compatible with critical
   saturation. A sharp upper constant `C_0`, not the tail inequality, would
   force simplicity.
5. Deciding the pointwise sign requires a second-order expansion or comparably
   strong oscillation control. First-order asymptotics cannot decide it.

## References

- L. Báez-Duarte, *A strengthening of the Nyman--Beurling criterion for the
  Riemann hypothesis*, arXiv:math/0202141; part 2, arXiv:math/0205003.
- L. Báez-Duarte, M. Balazard, B. Landreau, E. Saias, *Notes sur la fonction
  zeta de Riemann, 3*, Adv. Math. 149 (2000), 130--144.
- J.-F. Burnol, *A lower bound in an approximation problem involving the zeros
  of the Riemann zeta function*, Adv. Math. 170 (2002), 56--70;
  arXiv:math/0103058.
- M. Balazard, A. de Roton, *Sur un critere de Baez-Duarte pour l'hypothese de
  Riemann*, Int. J. Number Theory; arXiv:0812.1689.
- S. Bettin, J. B. Conrey, D. W. Farmer, *An optimal choice of Dirichlet
  polynomials for the Nyman--Beurling criterion*, arXiv:1211.5191.
- L. Báez-Duarte, M. Balazard, B. Landreau, E. Saias, *Etude de
  l'autocorrelation multiplicative de la fonction partie fractionnaire*,
  Ramanujan J. 9 (2005), 215--240; arXiv:math/0306251.
- B. Bagchi, *On Nyman, Beurling and Baez-Duarte's Hilbert space reformulation
  of the Riemann hypothesis*, Proc. Indian Acad. Sci. Math. Sci. 116 (2006),
  137--146; arXiv:math/0607733.
