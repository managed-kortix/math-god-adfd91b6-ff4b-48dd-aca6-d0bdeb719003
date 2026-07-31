# Cycle 175: progression collisions give an exact finite-depth filter

The cross-output obstruction from Cycles 147--148 is not valid without an
additive-multiplicity hypothesis.  Arithmetic progressions support exact
telescoping cancellation of every interior output while preserving two
boundary outputs.  Equal-shell polarizations make the boundary outputs
admissible as the next rail, so the block can be iterated to arbitrary finite
depth.  The construction is sequential, not a simultaneously populated closed
Euler subsystem.

Fix nonzero integers `R,Y` and an even integer `m>=2`.  In the Laurent ring put

\[
A_R(z)=z^{-R}-z^R,
\qquad
B_{m,R}(z)=\sum_{j=0}^{m-1}z^{(2j-m+1)R}.
\]

The elementary geometric-series identity

\[
\boxed{A_R(z)B_{m,R}(z)=z^{-mR}-z^{mR}}
\]

is the entire collision mechanism.  Every interior coefficient has two
representations and cancels; the two extreme sums have unique representations
and survive.  Taking `m` even avoids a zero-frequency pump.

Here is an exact realization by the three-dimensional Euler/Navier--Stokes
Fourier symbol.  On the layer `k_2=Y`, populate the equal-shell rail pair

\[
k_-=(-R,Y,0),\quad u_{k_-}=e_3,
\qquad
k_+=(R,Y,0),\quad u_{k_+}=-e_3,
\]

and impose reality at `-k_-,-k_+`.  Populate the symmetric pump progression

\[
\ell_j=((2j-m+1)R,0,0),
\qquad u_{\ell_j}=e_2,
\qquad 0\le j<m.
\]

The progression is already closed under negation.  All rail--rail interactions
vanish because `e_3` is orthogonal to every planar frequency.  All pump--pump
interactions vanish because `e_2\cdot\ell_j=0`.  For a rail frequency
`k=(x,Y,0)` and a pump frequency `ell=(s,0,0)`, the symmetrized Leray symbol is

\[
\begin{aligned}
\mathcal S_{k,\ell}(e_3,e_2)
&=P_{k+\ell}\big((e_3\cdot\ell)e_2+(e_2\cdot k)e_3\big)\\
&=Y e_3.
\end{aligned}
\]

It is independent of `x,s`, and projection changes nothing.  Consequently the
complete ordered real convolution, after pairing the two orders of each
rail--pump interaction, is exactly the Laurent product above.  Its
only nonzero outputs are

\[
(\pm mR,Y,0),\qquad(\pm mR,-Y,0),
\]

with raw symmetrized coefficients `+Y e_3` at `(-mR,\pm Y,0)` and
`-Y e_3` at `(mR,\pm Y,0)`.  Thus `2(m-1)` interior output frequencies
cancel coherently across the two reality layers; these comprise `4(m-1)`
unordered rail--pump contributions and `8(m-1)` ordered summands.  The
designated boundary quartet survives.  The two
outputs on either reality layer again have equal norm and the same transverse
polarization.

This gives an exact arbitrary-finite-depth sequential construction.  Given any
even integers `m_0,...,m_{D-1}`, set

\[
R_{n+1}=m_nR_n.
\]

At stage `n`, rescale the surviving boundary pair from stage `n-1` to the rail
normalization above and insert the pump progression `B_{m_n,R_n}`.  The identity
maps it exactly to the equal-shell pair at radius parameter `R_{n+1}`.  Induction
works for every finite `D`; taking every `m_n=2` gives `R_n=2^nR_0`.  No
approximation or generic-position assumption enters.

There are two sharp limitations.

1. This is a sequence of exact instantaneous blocks.  If pumps from several
   stages and all intermediate rails are populated at once, cross-stage
   products appear and the one-variable telescoping identity does not cancel
   them.
2. The block gives no amplitude, critical-energy, dwell-time, or viscous
   estimate.  Rescaling a boundary output into the next normalized rail may
   spend an uncontrolled amount of energy.

Therefore additive uniqueness cannot underwrite a universal off-circuit tax:
arbitrarily many off-circuit channels can cancel exactly, and equal-shell
output compatibility survives arbitrary sequential depth.  What remains open
is a simultaneous multistage factorization with bounded critical normalization,
or a theorem proving that its cross-stage terms must carry a budgetable charge.
This is an exact Fourier-algebra adversary, not a Navier--Stokes solution,
blowup construction, or regularity theorem.

Reproduce the full signed convolution with

```sh
python3 millennium-prize/navier-stokes/verify_cycle175_progression_filter.py
```
