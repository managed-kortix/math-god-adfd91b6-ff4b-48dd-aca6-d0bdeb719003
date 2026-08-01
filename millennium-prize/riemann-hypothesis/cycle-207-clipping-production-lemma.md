# Cycle 207: clipping lemma for positive endpoint production

## Bounded objective

Fix a shift bounded away from the critical line, for example

\[
 E(z)=\xi(\tfrac32-iz),
\]

and first work on one fixed bidisk.  The aim here is not to assume that the
target kernel is positive.  It is to isolate a quantitative, checkable
sufficient condition on an *indefinite* canonical ansatz which produces a
nearby positive Hamiltonian and a certified endpoint error.

This finite-shift, finite-disk lemma is not equivalent to RH.  Using it on
disks exhausting the plane and shifts tending to zero would still require new
estimates strong enough to pass the equivalence gate of Cycles 174 and 206.

## Quantitative clipping lemma

Let

\[
 JY'=zH(x)Y,\qquad Y(0,z)=y_0\in\mathbb R^2,
 \qquad q=\|y_0\|,
\]

on `[0,L]`.  Matrices are measured in operator norm.  Suppose
`G:[0,L] -> Sym_2(R)` is integrable but not necessarily positive, and write

\[
 G=G_+-G_-,\qquad G_\pm(x)\succeq0,
 \qquad \nu=\int_0^L\|G_-(x)\|\,dx.
\]

Let `H=G_+`, and assume

\[
 \int_0^L\|G(x)\|\,dx\le M,
 \qquad \int_0^L\|H(x)\|\,dx\le M.
\]

Denote the endpoint kernels by `K_G` and `K_H`, using the same real initial
vector and the convention of Cycle 174.

**Lemma (negative-mass clipping).** For `|z|,|w|<=R`,

\[
 \boxed{
 |K_H(z,w)-K_G(z,w)|
 \le {q^2\over\pi}
 \bigl(e^{2RM}+2RM e^{3RM}\bigr)\nu.}       \tag{207.1}
\]

Consequently, if a target kernel `K_*` obeys

\[
 \sup_{|z|,|w|\le R}|K_G(z,w)-K_*(z,w)|\le\eta,
\]

then the positive Hamiltonian `H=G_+` gives

\[
 \boxed{
 \sup_{|z|,|w|\le R}|K_H(z,w)-K_*(z,w)|
 \le \eta+C(R,M,q)\nu,}                    \tag{207.2}
\]

where `C(R,M,q)` is the displayed coefficient in (207.1).

Thus the concrete sufficient production condition is

\[
 \eta_N\longrightarrow0,\qquad
 \nu_N\longrightarrow0,\qquad
 \sup_N M_N<\infty.                         \tag{207.3}
\]

It yields positive Hamiltonian approximants with vanishing endpoint-kernel
error on the chosen disk.  Unlike an assumption that `K_*` is positive,
(207.3) is an ansatz-level condition: both defects can in principle be bounded
from explicit matrix cells before positivity of the target is known.

### Proof

Writing the equation as `Y'=-zJHY`, Gronwall gives

\[
 \|Y_H(x,z)\|,\|Y_G(x,z)\|\le q e^{RM}
\]

and variation of constants gives the deliberately coarse bound

\[
 \|Y_H(x,z)-Y_G(x,z)\|
 \le Rq e^{2RM}\int_0^x\|H-G\|.
\]

The integrated Lagrange identity, valid also for symmetric indefinite `G`, is

\[
 K_H(z,w)={1\over\pi}\int_0^L
 Y_H(x,w)^*H(x)Y_H(x,z)\,dx,
\]

and similarly for `G`.  Insert and subtract the two mixed terms.  The direct
matrix difference costs `q^2e^{2RM}\nu`; the two solution differences together
cost at most `2Rq^2Me^{3RM}\nu`.  Division by `pi` proves (207.1).

If `G` is piecewise constant, clipping is cellwise and fully explicit from the
two eigenvalues of each `2 by 2` matrix.  To retain rational arithmetic,
approximate each clipped cell by `Q Q^T+delta I`, with rational `Q` and positive
rational `delta`, and approximate the breakpoints rationally.  If the added
`L^1` error is `rho`, the same proof replaces `nu` by `nu+rho` (and uses the
correspondingly enlarged mass bound).  Hence algebraic clipping followed by
rational positive-definite rounding does not lose the vanishing-error result.

## Exact one-cell obstruction

There is a clean obstruction to obtaining a vanishing-error exhaustion while
keeping `N=1` constant.

Let `H` be any constant positive-semidefinite matrix on `[0,L]`, with real
initial vector `y_0`.  For real `t`,

\[
 {d\over dx}\{Y(x,t)^T H Y(x,t)\}=0
\]

because `HJH` is skew-symmetric.  The diagonal Lagrange identity therefore
gives the exact formula

\[
 \boxed{K_H(t,t)={L\over\pi}y_0^THy_0,\qquad t\in\mathbb R.} \tag{207.4}
\]

Every one-cell constant-Hamiltonian endpoint kernel has constant real-axis
diagonal.  This remains true for rank-one cells and does not depend on trace
normalization.

For `E(z)=xi(3/2-iz)`, the target diagonal is not constant.  The positive
Fourier-cosh representation of xi gives

\[
 K_E(0,0)={\xi(3/2)\xi'(3/2)\over\pi}>0,
\]

whereas Stirling's formula for the gamma factor, together with standard bounds
for `zeta(3/2-it)` and its derivative, gives

\[
 K_E(t,t)\longrightarrow0\qquad(|t|\longrightarrow\infty).
\]

It follows immediately that no sequence of one-cell constant positive
Hamiltonians can have endpoint kernels converging locally uniformly to `K_E`
on all of `C x C`: convergence at `t=0` fixes the limit of the constants in
(207.4), while convergence at any other real `t` would force the target
diagonal to have that same value.

This is stronger than failure of the particular `H=I/4` certificate in Cycle
206.  It rules out the entire constant one-cell architecture.  At least two
cells, a nonconstant Hamiltonian within a cell, or a different finite model is
necessary before an exhaustion can reproduce even the real diagonal profile.

## Finite-matrix obstruction certificate

There is also an exact obstruction on a fixed disk.  Choose nodes
`z_1,...,z_m`, let

\[
 T=[K_*(z_j,z_k)]_{j,k=1}^m,
\]

and suppose a positive canonical endpoint kernel approximates `K_*`
entrywise with error at most `epsilon`.  Its node matrix `P` is positive
semidefinite and

\[
 \|P-T\|_{op}\le m\epsilon.
\]

Weyl's inequality yields

\[
 \boxed{\lambda_{min}(T)<0
 \quad\Longrightarrow\quad
 \epsilon\ge{-\lambda_{min}(T)\over m}.}     \tag{207.5}
\]

An interval or exact-arithmetic enclosure proving that the right side is
positive is therefore a rigorous no-go certificate for *every* positive
Hamiltonian at the requested tolerance, not merely for a selected ansatz.
For shifted xi no such negative matrix is presently known; finding one for a
positive shift would disprove the corresponding Hermite--Biehler assertion.

## Production decision

The viable bounded lane is now precise: construct explicit indefinite
piecewise-constant cells `G_N`, certify their endpoint defect `eta_N`, and
drive their integrated negative spectral mass `nu_N` to zero while keeping the
total mass controlled.  Clipping then supplies the positive approximants and
the error theorem automatically.  The one-cell constant family is exactly
obstructed by (207.4), so the first meaningful computation starts at two cells.

No Riemann-hypothesis result is claimed.
