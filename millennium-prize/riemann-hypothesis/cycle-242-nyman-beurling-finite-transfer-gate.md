# Cycle 242: finite Nyman--Beurling transfer gate after clipping

## Decision

The Cycle 207 clipping estimate is a useful perturbation theorem, but Cycle 208
shows that it cannot manufacture positivity for a target having a negative
finite kernel matrix. More importantly, successful vanishing-error canonical
exhaustions through shifts tending to zero are RH-equivalent by Cycles 174 and
206. The canonical-system continuation therefore supplies no admissible
non-equivalent production checkpoint beyond the already proved finite-disk
lemmas. This is a `WALL` for the clipped canonical architecture, not for
canonical systems in general.

The bounded scout returns instead to the explicit logarithmic
Nyman--Beurling approximants.  The proposed one-block checkpoint is finite and
strictly weaker than the asymptotic Nyman--Beurling conclusion.  The hostile
audit below shows, however, that it is already passed at `N=3` and carries no
meaningful official-transfer credit.  Only a cofinal contraction theorem would
activate the transfer clause.

## Exact finite energy

For `N>=3`, put

\[
 c_a=\mu(a){\log(N/a)\over\log N},\qquad
 F_N(x)=1_{(0,1)}(x)+\sum_{a\le N}c_a\{1/(ax)\},
\]

and

\[
 P_N=\int_0^1|F_N(x)|^2\,dx,
 \qquad A_N=\sum_{a\le N}{c_a\over a}.
\]

The complete norm splits exactly as

\[
 \|F_N\|_{L^2(0,\infty)}^2=P_N+A_N^2.                 \tag{242.1}
\]

Indeed, `F_N(x)=A_N/x` for `x>1`.

The signs and normalization are as displayed.  With
`rho_a(x)={1/(ax)}` and `chi=1_(0,1)`, the plus sign in
`F_N=chi+sum c_a rho_a` combines with the standard negative Mellin transform
of `rho_a` to give `1-zeta(s)V_N(s)`.  No extra minus sign belongs in `c_a`.
The term `a=N` is harmless because `c_N=0`.

For an exact restricted-energy evaluation, put

\[
 g_a={\log a+1-\gamma\over a},\qquad
 G_{a,b}=\langle\rho_a,\rho_b\rangle_{L^2(0,1)}.
\]

If `d=(a,b)`, `p=a/d`, `r=b/d`, `ell=lcm(a,b)`, and

\[
 V(p,r)=\sum_{k=1}^{r-1}\{kp/r\}\cot(\pi k/r),\qquad V(p,1)=0,
\]

then the exact restricted Vasyunin entry is

\[
 G_{a,b}={
 (r-p)\log(p/r)+(p+r)(\log(2\pi)-\gamma)
 -\pi[V(p,r)+V(r,p)]
 \over2\ell}-{1\over ab}.                              \tag{242.2}
\]

The final `-1/(ab)` is essential: the published full-half-line Gram entry has
no such term, while restriction to `(0,1)` removes the rank-one `x>1` tail.
Thus

\[
 \boxed{P_N=1+2\sum_{a\le N}c_ag_a
 +\sum_{a,b\le N}c_ac_bG_{a,b}.}                       \tag{242.3}
\]

This includes the affine, diagonal, and off-diagonal terms.

## Candidate lemma NB242

There is an integer `N>=3` such that

\[
 \boxed{P_{2N}\le {3\over4}P_N.}                       \tag{242.4}
\]

For a submitted witness `N`, both energies must be enclosed directly from the
finite Vasyunin cotangent Gram formula with directed interval arithmetic. The
certificate passes only if the upper endpoint for `P_(2N)` is at most three
quarters of the lower endpoint for `P_N`. It fails for that witness if the
lower endpoint for `P_(2N)` is greater than three quarters of the upper
endpoint for `P_N`. An overlapping enclosure is `INCOMPLETE`, not evidence for
either sign.

The factor `3/4` was frozen before the search.  Nevertheless, the existing
256-bit directed complete-Gram evaluator certifies

\[
 P_3\in 1.5452502053206377116175981184777757298738500108594
       \mathbin{+/-}8.4\times10^{-50},
\]

\[
 P_6\in 0.7518756442522699710403001762894590039496417262768
       \mathbin{+/-}3.1\times10^{-49},
\]

and hence

\[
 {P_6\over P_3}\in
 0.4865721044160978480137872264894075901748339676077
 \mathbin{+/-}1.7\times10^{-49}<\frac34.              \tag{242.5}
\]

So NB242 is already a `PASS`, but only as a small finite calculation.

## Why this is not RH-equivalent

Statement (242.4) concerns two explicitly defined finite sums at one finite
integer. It is decidable by a finite directed computation and neither asserts
a limiting norm nor quantifies over zeros. In particular, one successful block
cannot imply RH: the Nyman--Beurling criterion requires a sequence with norm
tending to zero.

Nor is (242.2) known here to follow from RH. RH gives existence of suitable
approximants, but convergence of this fixed logarithmic taper is not known from
RH alone. The gate is therefore deliberately a finite behavior lemma rather
than a disguised equivalent criterion.

## Official transfer theorem

The finite gate has an exact conditional transfer.

**Lemma (geometric dyadic transfer).** Suppose there are `N_0>=3` and `q<1`
such that

\[
 P_{2N}\le qP_N                                             \tag{242.6}
\]

for every `N=2^jN_0`, `j>=0`. Then RH holds.

**Proof.** Iteration gives

\[
 P_{2^jN_0}\le q^jP_{N_0}\longrightarrow0.                 \tag{242.7}
\]

The prime number theorem with its standard zero-free-region remainder gives
`A_N=1/log N+o(1/log N)`, hence `A_(2^jN_0)^2->0`. Equation (242.1) therefore
gives

\[
 \|F_{2^jN_0}\|_2^2\longrightarrow0.
\]

The discrete Nyman--Beurling criterion then implies that every nontrivial zero
of zeta has real part `1/2`, exactly the official statement. QED.

For the frozen checkpoint (242.4), repeated success with `q=3/4` gives the
explicit decay `P_(2^jN_0)<=(3/4)^jP_(N_0)`. No such cofinal assertion is made
by the finite gate itself.

## Hostile score audit

One finite block has no meaningful gate score.  It does not cross the analytic
barrier, constrain any later dyadic descendant, or contribute a quantitative
fraction of the universal quantifier in (242.6).  Moreover, the existential
statement "there is an `N`" is semidecidable by witness search, not finitely
falsifiable as a global statement; only each submitted witness is finitely
decidable.  Since `N=3` already passes, further isolated witnesses are numerical
calibrations rather than proof architecture.  Relative to the portfolio score,
the proved one-block fact has zero barrier-crossing and zero official-transfer
coordinates.  The cofinal theorem (242.6), not any finite prefix of it, is the
RH-strength target.

## Hostile controls

1. A single passing `N` is only a finite lemma and must not be called evidence
   for eventual contraction.
2. The implication to RH begins only after proving the same bound on every
   dyadic descendant of one base scale; verifying finitely many descendants is
   insufficient.
3. The certificate must evaluate the complete restricted energy, including
   affine and off-diagonal Vasyunin terms. Oscillatory-only, local-cell, or
   diagonal truncations do not test (242.2).
4. Floating arithmetic may select `N`, but only directed intervals can pass or
   fail a witness.
5. No continuation of `1/zeta(s)=sum mu(n)n^-s` to the critical line is allowed
   in proving the finite inequalities or the cofinal law.

## Gate or wall

- Clipped canonical-system route: `WALL`. Its finite clipping lemma survives,
  but its asymptotic shifted-xi production endpoint is RH-equivalent, and the
  two-cell exercise supplies no route around that equivalence.
- Nyman--Beurling route: `NB242 PASS / CALIBRATION`.  The witness `N=3` proves
  (242.4), but an isolated block does not advance the official transfer.  The
  missing statement is the cofinal dyadic law (242.6), which remains unproved
  and is RH-strength through the displayed transfer.

No Riemann-hypothesis result is claimed.
