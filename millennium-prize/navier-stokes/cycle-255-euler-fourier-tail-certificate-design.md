# Cycle 255: finite Euler Fourier-tail certificate design

## Decision

Cycle 215 cannot be used for Euler by setting `mu=0`. Its fixed geometric
shell cap is held in place by `-mu n^2 z_n`; without that term the quadratic
face test generally points outward. The Euler replacement is a shrinking
analytic weight. This gives a rigorous full-PDE tail for smooth, genuinely
infinite-support data while retaining the low-mode interval and endpoint
cubature architecture of Cycle 215.

This document specifies a finite production family and a fail-closed
certificate. It does not exhibit a factor-two orbit. A Galerkin ratio used to
select a family member is not a PDE claim.

## 1. Exact analytic tail lemma

Use the Cycle 212 vorticity normalization with `mu=0` and put

\[
 A_q(\omega)=\sum_{k\ne0}q^{|k|_1}|\omega_k|,
 \qquad
 D_q(\omega)=\sum_{k\ne0}|k|_1q^{|k|_1}|\omega_k|.       \tag{255.1}
\]

Let `q(t)>1` be differentiable. The ordered Euler multiplier obeys

\[
 { |p^\perp\!\cdot r|\over |p|_2^2}
 \le {|r|_2\over |p|_2}\le |r|_1,
 \qquad q^{|p+r|_1}\le q^{|p|_1}q^{|r|_1}.
\]

Termwise differentiation in a finite Galerkin system, followed by the upper
Dini derivative at zero coefficients, gives

\[
 D^+A_{q(t)}\le
 \left(A_{q(t)}+{q'(t)\over q(t)}\right)D_{q(t)}.        \tag{255.2}
\]

Choose rational `q0>1`, `alpha>0`, and `M>0`, and set

\[
 q(t)=q_0(1-\alpha t),\qquad
 A_{q_0}(\omega(0))\le M,\qquad \alpha\ge M,            \tag{255.3}
\]

with `q(T)>1`. Since `q'/q=-alpha/(1-alpha t)<=-M`, scalar comparison in
(255.2) proves

\[
 A_{q(t)}(\omega(t))\le M\quad(0\le t\le T),
 \qquad z_n(t)\le Mq(t)^{-n}.                           \tag{255.4}
\]

For completeness, use an outward perturbation at each finite cutoff, where the
scalar face is strictly inward, and then send the perturbation to zero. The
common radius `log q(T)>0` gives dominated convergence of the convolution as
the cutoff tends to infinity. Equivalently, local analytic existence plus
(255.4) continues the analytic solution through `T`; uniqueness identifies it
with the global smooth 2D Euler solution. Equality in (255.3) is allowed.

The linear `q` is intentional: all weights at rational slab endpoints are
rational, so no interval exponential enters the trusted core.

## 2. Full-PDE retained enclosure

Let `S_N={k:0<|k|_infinity<=N}` and partition `[0,T]` into rational slabs
`I_j=[t_j,t_(j+1)]`. On slab `j` use the worst-case tail

\[
 z_n(t)\le M q(t_{j+1})^{-n},\qquad n>N.                \tag{255.5}
\]

For each retained mode, compute the omitted convolution radius with the
existing `shell_convolution_bound`, taking

```text
head[n] = sum_{|k|inf=n} sup |W_k|,  1 <= n <= N,
cap_start = N+1,
cap = M,
rho = q(t_(j+1)),
unresolved_cutoff = N.
```

The Cycle 213 expression is an absolute convolution bound and does not use
viscosity. Only `check_dissipative_shell_cap` is forbidden. The exact retained
vector field uses the paired coefficient (214.1), and each slab verifies

\[
 A_j+[0,h_j](F_N(W_j)+R_j)\subseteq W_j,
 \qquad
 A_j+h_j(F_N(W_j)+R_j)\subseteq B_j.                   \tag{255.6}
\]

The first inclusion is the full Picard tube, not an endpoint Euler step. The
tail follows independently from (255.4), while (255.6) encloses the retained
equations driven by every tail consistent with (255.5). Chaining
`B_j subset A_(j+1)` encloses the full Euler trajectory.

For efficiency, explicit shells `N<n<L` may instead be represented by
coefficient boxes and treated as ordinary retained coordinates in (255.6).
They must not be propagated by a dissipative shell inequality. The analytic
cap then starts at `L`.

## 3. Smooth infinite-support production family

Define the low streamfunction packets

\[
\begin{aligned}
 P_1&=\cos x+2\cos y,\\
 P_2&=\sin x-2\sin y,\\
 P_3&=\cos(x+y)+\cos(2x-y),\\
 P_4&=\sin(x-2y)+\sin(2x+y),\\
 P_5&=\cos(3x+y)-\cos(x-3y).
\end{aligned}                                           \tag{255.7}
\]

Let `a=(a1,...,a5)`. Its first nonzero entry is `1`, and every later entry is
in `{-2,-1,0,1,2}`. There are exactly
`5^4+5^3+5^2+5+1=781` projective low profiles. This removes amplitude
duplicates while retaining signs and non-isometric shape dynamics.

For `K=4`, define the real-even infinite vorticity template

\[
 g_{\sigma,k}=\sigma^{|k|_1}\quad
 (|k|_\infty>K),\qquad g_{\sigma,k}=0\quad(|k|_\infty\le K),              \tag{255.8}
\]

where `sigma` is in `{1/16,1/24}`. Set

\[
 \omega_0={1\over64}\Delta\sum_{i=1}^5a_iP_i+\epsilon g_\sigma,
 \qquad \epsilon\in\{1/256,1/512,1/1024\}.             \tag{255.9}
\]

Every member is real, mean zero, analytic, and has genuinely infinite Fourier
support. For rational `q0` with `q0 sigma<1`, its tail analytic norm is exactly

\[
 \epsilon\left[
 \left({1+q_0\sigma\over1-q_0\sigma}\right)^2
 -\sum_{|k|_\infty\le K}(q_0\sigma)^{|k|_1}
 \right].                                               \tag{255.10}
\]

No unknown smooth-tail constant is admitted. The fixed factor `1/64` is part
of the family, not an optimization variable; without an amplitude factor of
this order even the first terminal time can be rejected by the deliberately
coarse Wiener-norm lifespan gate. Euler amplitude scaling means it changes the
represented time scale, not the attainable norm ratios.

Use terminal times `T=m/16`, `1<=m<=32`. Before exact feasibility filtering,
the family has `781*2*3*32=149,952` members. A member is admissible only if one
tuple in the frozen grid `q0 in {33/32,17/16,9/8,5/4}` and
`M,alpha in {j/64:1<=j<=256}` satisfies (255.3), `q(T)>1`, and directed initial
cubature has positive lower bound. Choose the lexicographically first feasible
tuple, with `q0` ordered as displayed and then `M,alpha` increasing. Optimize
both endpoint directions;
time reversal is invoked only after the full forward orbit is enclosed.

## 4. Deterministic optimization funnel

Optimization means a finite lexicographic argmax, not random restarts.

1. Enumerate `(a,sigma,epsilon,T)` in the order above and reject analytic
   infeasibility exactly.
2. Run one floating `2/3`-dealiased Euler screen at `N=64`, RK4 step `1/2048`,
   evaluating both endpoint directions. This stage only ranks candidates.
3. Promote at most 64 members with ratio at least `3/2`. Rerun at `N=128` and
   `N=256`, steps `1/4096` and `1/8192`. Reject unless both spatial changes and
   both step-doubling changes are at most `1/50` and the finest ratio exceeds
   `9/4`.
4. Sort survivors by decreasing finest ratio, then by enumeration index.
   Attempt interval certification in that order. Stop at the first rigorous
   crossing or after 16 failed interval attempts.

The `9/4` threshold reserves `1/4` absolute ratio for full-PDE and cubature
uncertainty. The screen is neither necessary nor sufficient for a certificate.
Failure excludes only these 149,952 members under this funnel.

A new coarse run is not justified yet. Existing Cycle 213 and Cycle 214 screens
peaked near `1.0133` and were spatially unstable near `1.17`, respectively, and
neither implements (255.7)--(255.9). Running an old binary would not rank this
family and would create no reusable evidence. Compute becomes justified after
a screen records the exact enumeration index and all four resolution checks.

## 5. Finite certificate

A successful ASCII JSON artifact has format
`cycle255-euler-tail-enclosure-v1`. Rational numbers are canonical strings. Its
finite fields are:

- `family`: enumeration index, five integers `a`, fixed amplitude `1/64`,
  `sigma`, `epsilon`, `T`, `K`, the packet-formula version, and the generator's
  SHA-256 digest;
- `analytic_tail`: `q0`, `M`, `alpha`, exact finite low contribution, exact
  value (255.10), and margins `M-A_q0`, `alpha-M`, and `q(T)-1`;
- `partition`: every rational `t_j`, retained cutoff, and exact Fourier-real
  entry, tube, endpoint, and omitted-convolution box for every retained mode;
- `tail_replay`: each slab-end `q_j`, retained shell masses, and every
  recomputed low-mode remainder radius from the Cycle 213 geometric sums;
- `invariants`: directed Parseval energy and enstrophy enclosures on every slab,
  including the analytic tail; these are redundant breakers, not substitutes
  for (255.6);
- `cubature`: initial and final full-PDE enclosures for normalized Haar
  `integral |u|^3`, including unresolved velocity, gradient, and second
  derivative contributions;
- `conclusion`: the strict rational inequality

\[
       L_T>8U_0.                                        \tag{255.11}
\]

Here `[L_T,U_T]` and `[L_0,U_0]` enclose the cubed `L^3` norms. Cubing avoids
root division, and (255.11) proves `||u(T)||_3>2||u(0)||_3`.

## 6. Fail-closed replay rules

The validator succeeds only after recomputing every derived quantity. It
rejects on any of the following:

1. duplicate or unknown JSON keys, noncanonical rationals, NaN/infinity,
   reversed intervals, unknown normalization, generator digest mismatch, or an
   enumeration index inconsistent with the displayed member;
2. failure of Fourier reality, zero mean, genuine infinite support
   (`epsilon>0`), exact initial coefficients, (255.10), or any analytic margin;
3. partition failure, `q_j<=1`, a missing retained mode or slab,
   endpoint-chain failure, or a tail evaluated at the slab start rather than
   its smaller endpoint weight;
4. a declared remainder smaller than the recomputed complete remainder, use of
   a Galerkin projection as a remainder, or either failed inclusion (255.6);
5. invariant intervals with empty common intersection, or initial invariant
   values not contained in every slab enclosure;
6. endpoint cubature omitting retained modes or the infinite cap, nonpositive
   initial lower norm, or failure of the strict integer inequality (255.11).

The validator catches decoding, JSON, arithmetic, resource-limit, and internal
errors and exits nonzero with `FAIL CLOSED`. It prints
`PASS FULL 2D EULER L3 RATIO > 2` only after (255.11). No weaker status contains
the word `PASS`.

## 7. Scope

The shrinking-weight lemma removes the viscosity dependence that made Cycle
215 unusable for ND251 and supplies generated-scale bounds for smooth
infinite-support data. The family and certificate make the next search finite,
falsifiable, and deterministic. They do not prove that a member crosses two,
establish the Cycle 211 inviscid-limit constant, or resolve Navier--Stokes. If
(255.11) is eventually certified, the next artifact must append the explicit
Cycle 211 `mu0` and physical-amplitude threshold.
