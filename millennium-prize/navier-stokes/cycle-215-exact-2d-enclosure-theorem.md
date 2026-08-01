# Cycle 215: exact full 2D enclosure theorem

## Statement

Use the normalization (212.2), let `S_N={k:0<|k|_infinity<=N}`, and put
`z_n=sum_(|k|_infinity=n)|omega_k|`.  On a rational slab `[a,a+h]`, prescribe
compact rectangular complex boxes `A_k subset W_k`, endpoint boxes `B_k`,
nonnegative explicit-shell entries `e_n`, tubes `H_n`, and endpoints `b_n` for
`N<n<L`.  Prescribe also `C>0`, `rho>1`, and

\[
 z_n\le C\rho^{-n}\quad(n\ge L).                     \tag{215.1}
\]

For every retained mode let `R_k` contain the complete convolution contribution
with at least one input outside `S_N`.  The following exact, non-strict
conditions are sufficient:

1. the actual slab entry is in `A`, the explicit shell entries obey
   `z_n(a)<=e_n`, and (215.1) holds at `a`;
2. throughout `W` and `z_n<=H_n` (`n<L`) plus (215.1), the Cycle 213 ordered
   majorant is `Q_n`, and
   `e_n+h Q_n<=H_n` for `N<n<L`;
3. `e_n/(1+mu n^2 h)+h Q_n<=b_n` for `N<n<L`;
4. every cap face obeys `Q_n<=mu n^2 C rho^-n` for `n>=L`, including the
   complete finite-face and quadratic-ray checks of Lemma 213.A;
5. the exact interval evaluations satisfy

\[
 A+[0,h](F_N(W)+R)\subseteq W,\qquad
 A+h(F_N(W)+R)\subseteq B.                            \tag{215.2}
\]

All boxes are Fourier-real, all index sets are exact, and all inequalities may
be equalities.

**Theorem 215.A.**  A smooth 2D Navier--Stokes solution entering the slab under
condition 1 remains in the joint retained/shell tube.  At `a+h` its retained
coefficients lie in `B`, its explicit shell masses are at most `b_n`, and its
cap obeys (215.1).  A finite chain of such slabs encloses the unique smooth 2D
solution.  Bounds computed from the retained endpoint, every explicit endpoint
shell, and the geometric cap therefore enclose the full PDE endpoint.  This is
an enclosure theorem only; it implies no norm amplification.

## Non-strict and simultaneous contacts

A scalar slogan that "the derivative points inward at the first exit" is not a
proof when a face inequality is non-strict: a differentiable function can have
zero derivative at its first contact and then leave.  Choosing one face is also
invalid when infinitely many faces contact simultaneously.

The valid argument is comparison, not that slogan.  First use a finite Fourier
Galerkin cutoff `M`.  The shell Dini inequalities have a cooperative right-hand
side after absolute values: increasing any shell bound cannot decrease any
`Q_n`.  Replace every tube bound by an outward perturbation
`bound+epsilon exp(K(t-a))`, where `K` dominates the finite box's Lipschitz
constant.  The perturbed faces are strictly inward.  Taking the maximum of all
positive normalized face excesses handles all faces attaining the maximum at
the same time; its upper Dini derivative is negative at a positive first
maximum.  Thus no perturbed face exits.  Letting `epsilon` decrease to zero
proves invariance of the original closed, non-strict box.  Equivalently, this
is the standard cooperative comparison theorem proved by the same perturbation.

For this perturbation argument, at each fixed `M` the changes
`Q^epsilon-Q`, `R^epsilon-R`, and `F_N(W^epsilon)-F_N(W)` are controlled by a
finite-dimensional local Lipschitz constant, and `K=K_M` is chosen larger than
that constant.  One first lets `epsilon` decrease to zero at fixed `M`; no
cutoff-uniform bound on this auxiliary `K_M` is asserted or needed.  Only then
does one pass `M` to infinity.  The original comparison constants are uniform
in `M`: the Cycle 213 sums already majorize every ordered Galerkin interaction,
and the geometric cap is summable.  Dominated
convergence passes each fixed Fourier equation and shell inequality to the
limit.  Alternatively, because two-dimensional Navier--Stokes already has a
unique global smooth solution for this trigonometric datum, apply the uniform
finite comparison to its Fourier truncations and identify the limit by
uniqueness.  No cutoff-uniform existence claim is being smuggled out of the
certificate.

## Picard inclusion and the joint bootstrap

For a fixed admissible unresolved forcing `r(t) in R`, define on
`C([a,a+h],W)`

\[
 (Phi v)(t)=omega(a)+\int_a^t(F_N(v(s))+r(s))\,ds.
\]

The first inclusion in (215.2), interpreted componentwise with
`[0,h]D={tau d:0<=tau<=h,d in D}`, says exactly that `Phi` maps the closed box
into itself.  Polynomial `F_N` is locally Lipschitz, so Picard iteration (or
Schauder followed by ODE uniqueness) gives the retained solution in `W`; the
second inclusion gives `B` at the endpoint.  Merely checking an Euler endpoint,
or checking `A+hD subset W` without the whole `[0,h]D`, would not suffice.

There is no circular assumption between retained and shell bounds.  Apply the
same outward perturbation to the product of the retained Picard tube, the
explicit shell tubes, and the cap.  While the perturbed product holds, the
remainder calculation is valid; (215.2) controls the retained coordinates and
the cooperative inequalities control all shell coordinates.  The product
cannot have a first exit, even if retained and several shell faces contact at
once.  Remove the perturbation afterward.

For the explicit-shell endpoint, variation of constants gives

\[
 z_n(a+h)\le e^{-mu n^2h}e_n+
 {1-e^{-mu n^2h}\over mu n^2}Q_n
 \le {e_n\over1+mu n^2h}+hQ_n,                       \tag{215.3}
\]

which explains the validator's rational endpoint formula.  Its tube formula
`e_n+hQ_n` is conservative because dropping dissipation can only increase the
upper bound.

## Application to the published artifact

`cycle215-full-2d-enclosure-certificate.json` has `N=2`, `L=32`, 64 slabs of
width `1/4096`, the exact trigonometric datum, explicit shells 3 through 31,
and the common cap `(1/1024)(33/32)^(-n)`.  `validate_cycle214.py` recomputes
all hypotheses above with rational arithmetic.  It now includes explicit
endpoint shells in `U`, `G`, and the unresolved velocity component used by
cubature; the former retained-plus-cap calculation omitted those shells and
could not be a full norm enclosure.  Coefficientwise, a shell mass `z_n`
contributes at most `z_n/n`, `z_n`, and `n z_n` to a velocity component, its
coordinate gradient, and its coordinate second derivative.  The geometric cap
uses the corresponding exact zeroth and first moments.

For `f=|u|^3`, the directed midpoint rule uses
`|partial_jj f| <= 6 U G^2+3 U^2 H`; its normalized-Haar remainder is at most
`pi^2(6 U G^2+3 U^2 H)/(3 M^2)`.  At `M=256`, exact rational arithmetic gives

\[
  3.5186453989 < \int |u(0)|^3 < 3.5743550161,
  \qquad
  3.2477649584 < \int |u(1/64)|^3 < 3.3623114605.
\]

The final upper endpoint is strictly below the initial lower endpoint.  Thus
the artifact certifies endpoint `L^3` near-decay for the Cycle 214 datum (also
for the norm itself, since cubing is increasing), but no amplification result.
Successful replay prints `PASS FULL 2D PDE ENCLOSURE Cycle 215` and
`STRICT ENDPOINT L3 NEAR-DECAY CERTIFIED`.
