# Cycle 68: strategic retirement of the additive-12 tactic

## The adjusted barrier collapses to the normalized budget

Retain the exact Cycle 67 quantities

\[
F_r=R_r-\Theta_r={S_M(r)\over A_{M,r}},
\qquad
p_r=R_r-R_{r+1}.
\]

For an anchor endpoint `a`, define

\[
H_r^{adj}=\Theta_r+\sum_{j=a}^{r-1}p_j.
\]

Since the payment sum is `R_a-R_r`,

\[
\boxed{H_r^{adj}=R_a-{S_M(r)\over A_{M,r}}.}         \tag{68.1}
\]

Therefore

\[
R_a\ge\min_rH_r^{adj}
\iff
\max_r{S_M(r)\over A_{M,r}}\ge0.                    \tag{68.2}
\]

The sharp barrier of Cycle 67 is an exact reformulation of the original
normalized block budget, not an independent coercive estimate. Its increment

\[
c_r=p_r+\Theta_{r+1}-\Theta_r
\]

is exactly `F_r-F_(r+1)`. Sign crossings and convexity of the adjusted demand
are merely shape statements about the already desired normalized budget.

The physical demand and reserve remain independently meaningful. What is
tautological is adding their exact cumulative difference and treating the
result as a new proof barrier.

## Exact telescoping audit

If

\[
\overline H_r={1\over A_{M,r}}
\sum_{n=M}^{M+r-1}\beta_nH_n={S_M(r)\over A_{M,r}},
\]

then direct summation of the Cycle 67 increment gives

\[
\boxed{c_r=\overline H_r-\overline H_{r+1}.}         \tag{68.3}
\]

All projection, variance, `U`-cost, center-shift, and Schur channels recombine
to this one endpoint-energy contrast. For `r<t`,

\[
\sum_{j=r}^{t-1}c_j=\overline H_r-\overline H_t.     \tag{68.4}
\]

Equivalently, if `bar H_(r,t)` is the weighted physical energy over the newly
appended block,

\[
\sum_{j=r}^{t-1}c_j
={A_{r,t}\over A_t}(\overline H_r-\overline H_{r,t}).              \tag{68.5}
\]

This is useful bookkeeping and an audit of all constants, but no simpler than
the original renewal budget.

## What remains non-tautological

The following survive as genuine results or possible inputs:

- the independent complete-Gram definition of `R_r`;
- the independent Cycle 52 definition of `Theta_r`;
- finite dual lower certificates `L_(M,r)(N)<=R_r`;
- the exact physical signed correlation in the one-step demand update;
- any new arithmetic theorem bounding that correlation before evaluating the
  desired budget.

A concrete independent candidate would assert that, for a demand-selected
endpoint, a fixed-dilation finite tail-plus-boundary certificate already exceeds
the physical demand. This is falsifiable and non-tautological, but existing
finite evidence does not justify a uniform theorem.

## Rotation decision

Cycles 51--68 collectively establish structural exhaustion of the current
additive-12 tactic:

- local, sparse, and fixed-dimensional witnesses are too weak;
- complete tail and boundary bookkeeping is exact but lacks a uniform angle;
- dilation introduces an uncontrolled odd Möbius covariance;
- centered covariance has the favorable opposite sign but does not become the
  short-window budget;
- reserve-demand barriers telescope back to that budget;
- generic Gram geometry permits arbitrary payment patterns.

The additive-12 statement remains unfalsified and is certified through the
finite frontier, but it may be strictly stronger than RH. The rotation gate is
therefore met for this tactic. It is preserved as an open stronger candidate,
not the active main funnel.

The next calibration asks whether RH alone even implies convergence of the
exact logarithmically tapered approximants. No RH or additive-12 result is
claimed.
