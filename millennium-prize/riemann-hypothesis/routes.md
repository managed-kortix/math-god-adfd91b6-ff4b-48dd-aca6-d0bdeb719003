# Routes

## Active route: explicit discrete Nyman--Beurling approximants

For `N >= 3`, put

\[
c_a=\mu(a)\frac{\log(N/a)}{\log N},\qquad
F_N(x)=1_{(0,1)}(x)+\sum_{a\le N}c_a\{1/(ax)\}.
\]

Candidate lemma: there are absolute `C,N0` such that

\[
 \|F_N\|_{L^2(0,\infty)}^2\le C/\log N\quad(N\ge N_0).
\]

By Báez-Duarte's discrete Nyman--Beurling criterion this implies RH. The route
is knowingly RH-strength. The proof may not use critical-line convergence of
`sum mu(n)n^-s`, an RH-level Mertens bound, or an RH-conditional mollifier
estimate.

Primary route references: Báez-Duarte, arXiv:math/0202141 and
arXiv:math/0205003; Burnol, arXiv:math/0103058; Bettin--Conrey--Farmer,
arXiv:1211.5191.

## Current sharpened bottleneck

The exact reduced-rational Fourier representation exposes the needed signed
Möbius cancellation but creates a dense weighted sine kernel. Global low rank,
common-period bounds, and Farey-neighbor-only near fields have been falsified.
Coefficient-aware hierarchical error propagation and a phase-extracted
separated-block theorem are now proved: geometrically admissible far blocks
have explicit factorial-over-power/Taylor radii and rank independent of the
cutoff after phase extraction, while overlapping cusp blocks must remain dense.

The active next step is an outward-rounded hierarchy implementation preserving
the direct two-channel endpoint cancellation. A finite implementation survives
dense, Farey-cluster, rational-grid, and exact multiplicity audits, but
fixed-order absolute radii grow rapidly with mode count. The next refinement
extracts the `min(omega,nu)` cusp exactly and approximates the remaining Gram
kernel by an orthogonal projection whose PSD residual is charged only to
`d-u/alpha`. This is now certified for piecewise constants and shows quadratic
mesh convergence, but hostile carriers impose a time-frequency cell cost. The
weighted Legendre and signed shadow shells now certify the finite oscillatory
piece efficiently. Completing the constant and linear terms, however, reverses
its sign, and direct sawtooth integration proves the untruncated `N=4 -> 8`
tail is positive. Oscillatory-only sign is therefore abandoned. The active
refinement is a scalable inequality for the complete endpoint functional,
including constants and the retained interval. Direct unit-cell certificates
are sparse, but explicit negative cells rule out local positivity. The active
form is a grouped divisor-impulse or fixed-length dyadic block inequality. The
exact Abel form is now known, but fixed windows and local pairings are
falsified. The exact initial Chebyshev reserve also cancels at leading order
against slope terms. Drift-free cells isolate the remaining signed truncated
Möbius endpoint correlation; the active route seeks to sum that correlation
before bounding it. The exact first-block kernel is a positive max kernel, not
a gcd kernel, and controlling it alone is square-root-cancellation strength.
The finite Perron and exact continuum low-eigenmode representations are now
derived. Routine contour shifting is blocked by reciprocal-zeta poles, and a
fixed number of low moments is decisively insufficient. Exact harmonic
completion cancels the explicit degree-one von Mangoldt channel before
squaring, but leaves a two-scale difference of dense floor Gram forms; degree
two has an explicit generalized-von-Mangoldt residual. The active route now
targets cancellation between these two completed scale transforms, together
with a cumulative-sum bound for their high-mode residual. The exact common-
source kernel and fixed signed-square decomposition are indefinite. A minimal
rational `N=2` source certificate rules out generic Loewner order, contraction,
and martingale orthogonality. Any favorable inequality must use the actual
Mobius coefficients. The ultimate positive target remains
`liminf P_N=0`, where `P_N` is the restricted `(0,1)` energy. Any off-critical
zero gives an explicit uniform positive floor for every `P_N`, so that target
implies RH. It is not known to follow from RH for this exact logarithmic taper.
