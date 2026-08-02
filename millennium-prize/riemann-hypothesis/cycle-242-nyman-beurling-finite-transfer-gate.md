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
Nyman--Beurling approximants. The gate below is finite, exactly falsifiable,
strictly weaker than the asymptotic Nyman--Beurling conclusion, and has a direct
transfer clause to the official statement if it can be repeated cofinally.

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

## Candidate lemma NB242

There is an integer `N>=3` such that

\[
 \boxed{P_{2N}\le {3\over4}P_N.}                       \tag{242.2}
\]

For a submitted witness `N`, both energies must be enclosed directly from the
finite Vasyunin cotangent Gram formula with directed interval arithmetic. The
certificate passes only if the upper endpoint for `P_(2N)` is at most three
quarters of the lower endpoint for `P_N`. It fails for that witness if the
lower endpoint for `P_(2N)` is greater than three quarters of the upper
endpoint for `P_N`. An overlapping enclosure is `INCOMPLETE`, not evidence for
either sign.

The factor `3/4` is frozen before the search. It is separated from equality,
and it asks for a genuine one-block decrease rather than a decimal table or
positivity already built into a Gram matrix.

## Why this is not RH-equivalent

Statement (242.2) concerns two explicitly defined finite sums at one finite
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
 P_{2N}\le qP_N                                             \tag{242.3}
\]

for every `N=2^jN_0`, `j>=0`. Then RH holds.

**Proof.** Iteration gives

\[
 P_{2^jN_0}\le q^jP_{N_0}\longrightarrow0.                 \tag{242.4}
\]

The prime number theorem with its standard zero-free-region remainder gives
`A_N=1/log N+o(1/log N)`, hence `A_(2^jN_0)^2->0`. Equation (242.1) therefore
gives

\[
 \|F_{2^jN_0}\|_2^2\longrightarrow0.
\]

The discrete Nyman--Beurling criterion then implies that every nontrivial zero
of zeta has real part `1/2`, exactly the official statement. QED.

For the frozen checkpoint (242.2), repeated success with `q=3/4` gives the
explicit decay `P_(2^jN_0)<=(3/4)^jP_(N_0)`. No such cofinal assertion is made
by the finite gate itself.

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
- Nyman--Beurling route: `GATE NB242`. Produce one exact finite witness to
  (242.2). Passing it advances the official transfer architecture by one
  certified contraction block without claiming the cofinal theorem or RH.

No Riemann-hypothesis result is claimed.
