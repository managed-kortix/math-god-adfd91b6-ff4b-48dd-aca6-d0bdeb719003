# Cycle 206: exact small-N canonical Hamiltonian and the production threshold

## Question separated into two claims

Fix

\[
 E_\omega(z)=\xi(\tfrac12+\omega-iz),\qquad
 K_\omega=K_{E_\omega}.
\]

There are two materially different meanings of finite-disk approximation.

1. A single pair `(N,epsilon)` on one disk is not RH-equivalent.  It can be
   produced unconditionally, with a coarse but rigorous error, even at `N=1`.
2. Positive approximants with errors tending to zero on disks exhausting the
   plane, for positive shifts tending to zero, are already RH-equivalent.  The
   asymptotic production theorem, not exact small `N`, is the missing content.

The first statement is certified below.  The second sharpens the equivalence
gate in Cycle 174.

## An unconditional exact N=1 certificate

Take `omega=1`, the bidisk `|z|,|w|<=1`, one interval `[0,1]`, initial vector
`Y(0,z)=(1,0)^T`, and the rational positive-definite Hamiltonian

\[
 H(x)=\frac14 I_2.
\]

For `JY'=zHY`, direct exponentiation gives

\[
 Y(1,z)=(\cos(z/4),-\sin(z/4))^T,
 \qquad E_H(z)=e^{-iz/4},
\]

and hence

\[
 K_H(z,w)=\frac{\sin((z-\bar w)/4)}{\pi(z-\bar w)}.
\]

This is a genuinely positive canonical kernel: its increments have the Gram
integral from Cycle 174, and `H` is positive definite everywhere.  All
Hamiltonian entries and breakpoints are rational.

## Rational bound for the xi kernel

Use the classical absolutely convergent representation

\[
 \xi(s)=\frac12+\frac{s(s-1)}2\int_1^\infty
 \psi(x)\{x^{s/2}+x^{(1-s)/2}\}\,\frac{dx}{x},
 \quad \psi(x)=\sum_{n\ge1}e^{-\pi n^2x}.
\]

Suppose `r>=0`, `|s-c|<=r`, where `c=1/2+omega>0`, and put

\[
 S=c+r,\qquad
 \alpha=\max\{(c+r)/2,(1-c+r)/2\}<3.
\]

Since `pi>3`, `x^alpha<=e^{alpha(x-1)}` for `x>=1`, `n^2>=n`, and
`e^{-3}<1/20`, termwise integration gives

\[
 \int_1^\infty\psi(x)
 (x^{\Re(s)/2}+x^{(1-\Re(s))/2})\frac{dx}{x}
 \le \frac{2}{19(3-\alpha)}.
\]

The elementary bounds `|s|<=S` and `|s-1|<=S+1` therefore yield

\[
 |\xi(s)|\le M(r):=\frac12+
 \frac{S(S+1)}{19(3-\alpha)}.                 \tag{206.1}
\]

For `omega=1`, exact rational evaluation gives

\[
 M(1)=\frac{203}{266},\qquad M(2)=\frac{221}{190}.
\]

Cauchy's estimate on the unit circle about each point in the radius-one disk
gives `|xi'(s)|<=M(2)`.  Write `u=bar(w)`.  The numerator

\[
 E(z)E^\#(u)-E^\#(z)E(u)
\]

vanishes at `z=u`.  Integrating its derivative along the segment from `u` to
`z` (the disk is convex), and using `1/pi<1/3`, proves the removable-diagonal
bound

\[
 \sup_{|z|,|w|\le1}|K_1(z,w)|
 \le \frac{M(1)M(2)}3
 =\frac{44863}{151620}.                       \tag{206.2}
\]

Also `|sin q|<=|q|e^{|q|}` and `|z-bar(w)|<=2`.  Because
`e^{1/2}<sum_(n>=0)(1/2)^n=2`,

\[
 \sup_{|z|,|w|\le1}|K_H(z,w)|<\frac16.       \tag{206.3}
\]

Combining (206.2)--(206.3) gives the fully rational certificate

\[
 \boxed{\sup_{|z|,|w|\le1}|K_H(z,w)-K_1(z,w)|
 <\frac{70133}{151620}<\frac12.}              \tag{206.4}
\]

`verify_cycle206_canonical_small_n.py` checks the side conditions and recomputes
every rational consequence of the displayed elementary inequalities.  It does
not numerically evaluate xi.  The analytic inputs `pi>3`, `e^{-3}<1/20`, and
the geometric-series bound for `e^{1/2}` are not floating-point assumptions.

## Exact equivalence threshold

Let `omega_j>0` tend to zero.  For each `j`, suppose positive canonical
endpoint kernels `K_(j,N)` obey bounds

\[
 \sup_{|z|,|w|\le R}|K_{j,N}(z,w)-K_{\omega_j}(z,w)|
 \le \epsilon_{j,N}(R),\qquad
 \epsilon_{j,N}(R)\longrightarrow0\quad(N\longrightarrow\infty)
\]

for every finite `R`.  Every finite matrix of `K_(j,N)` is positive
semidefinite.  Entrywise convergence therefore makes every finite matrix of
`K_(omega_j)` positive semidefinite.  This only gives a non-strict inequality.
Assume separately that the approximants retain a fixed positive-definite
initial interval (or any equivalent hypothesis giving
`K_(omega_j)(z,z)>0` for every `Im z>0`).  The diagonal kernel identity then
gives the strict Hermite--Biehler inequality.  Thus every `E_(omega_j)` is
Hermite--Biehler, which implies RH.

Conversely, under RH every shifted `E_omega` is Hermite--Biehler.  The de
Branges inverse theorem and canonical chain then give positive canonical
exhaustions converging locally uniformly to its kernel.  Piecewise-constant
positive Hamiltonians approximate a fixed finite canonical interval in
`L^1`; Gronwall's inequality gives locally uniform transfer-matrix and kernel
convergence.  Rational positive-definite matrices and rational breakpoints are
dense, so rational piecewise-constant approximants may be inserted.  This last
density step is existential: absent effective moduli for the inverse
Hamiltonian and both approximations, it does not provide an algorithm producing
the arithmetic data or a computable endpoint-error theorem.

Therefore the precise existential statement is

\[
 \boxed{\text{existence of rational positive vanishing-error exhaustions}
 \Longleftrightarrow \mathrm{RH},}
\]

up to the stated normalization and strictness clauses.  Requiring
`rational/algebraic piecewise constant` does not weaken this existential
equivalence.  In contrast, an effective procedure with certified errors
implies RH, but the reverse effective implication is not established here.

## Hostile assessment

- The `N=1` certificate is an exact positive approximation, but its error is
  coarse and does not imply positivity of the xi kernel.
- A fixed finite disk cannot detect zeros whose corresponding spectral points
  lie outside it; one fixed shift bounded away from zero cannot imply RH.
- An error bound smaller than a known negative eigenvalue would obstruct an
  approximant, but no such eigenvalue is known without disproving the relevant
  shifted Hermite--Biehler assertion.
- Exact small `N` is therefore not the bottleneck.  The first potentially new
  production lemma must give explicit Hamiltonian data and errors vanishing
  through both disk exhaustion and `omega -> 0` without importing RH-level
  positivity.
- Claims of an *effective* RH equivalence require computable inverse-canonical
  moduli not supplied by the existential de Branges argument.

No Riemann-hypothesis result is claimed.
