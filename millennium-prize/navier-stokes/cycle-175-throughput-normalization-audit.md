# Cycle 175: invariant throughput normalization audit

## Referee objection

The phrase "unit designated critical throughput" is not an invariant
hypothesis by itself.  It can mean a coefficient in a chosen polarization
basis, the norm of one ordered convolution summand, the norm of the complete
real output at a frequency orbit, or physical trilinear energy flux.  These
quantities have different homogeneity.  Moreover, imposing unit size on a
bilinear output can itself impose a lower bound on a quadratic energy by
AM--GM.  Energy growth observed after such a normalization is informative only
after that compulsory normalization cost has been removed.

## Invariant formulation

For a real divergence-free Fourier field use frequency orbits
`[k]={k,-k}` and require

\[
 u_{-k}=\overline{u_k},\qquad k\cdot u_k=0.
\]

For disjoint input orbits `[p]`, `[q]` and output orbit `[k]`, with `p+q=k`,
let

\[
 F_{[k]}(u)=\bigl(B_k(u_p,u_q)+B_k(u_q,u_p),
 \overline{B_k(u_p,u_q)+B_k(u_q,u_p)}\bigr).
\]

A legitimate designated charge `Phi_[p,q->k]` must satisfy all of the
following.

1. It is a function of the physical orbit data and not of scalar amplitudes
   and polarization representatives used to write those data.
2. It uses the coherently summed real convolution at `[k]`; ordered pairs and
   the conjugate output are not counted as independent edges.
3. Its behavior under spatial dilation is stated explicitly.  In particular,
   one cannot interchange a raw forcing norm, a derivative-normalized symbol,
   and a critical-space-normalized charge.
4. If phases matter, `Phi` is either phase invariant (for example an orbit
   norm) or includes the physical receiver mode and is the actual flux
   `Re <F_[k],u_[k]>`.  The norm of one complex summand is not energy flux.

This last distinction also fixes homogeneity: an output/forcing charge is
quadratic in `u`, whereas physical energy flux is cubic because it includes the
receiver.  Calling both "throughput" conceals a material change in the
constraint.

Likewise the cost must be the physical critical energy

\[
 E_c(u)=\sum_{[j]}2|j|\,|u_j|^2
\]

in the `H^(1/2)` model, or the declared analogue, rather than a quadratic form
in gauge-dependent scalar coordinates.  For a proposed length-`L` circuit the
quantity that could carry content is therefore

\[
 \mathcal C_L=
 \inf\{E_c(u):\Phi_e(u)\ge1\text{ for every designated physical edge }e\},
\]

with all phase, polarization, collision, reality, and reciprocal-amplitude
freedoms included in the infimum.  A cascade obstruction needs growth of
`C_L` beyond the corresponding constraint-minimized decoupled relaxation, or an
invariant off-circuit lower bound at near-minimizers.  Indeed, if one edge has
the bilinear estimate

\[
 \Phi_e(u_p,u_q)\le \beta_e E_p(u_p)^{1/2}E_q(u_q)^{1/2},
\]

then `Phi_e>=1` already forces

\[
 E_p+E_q\ge {2\over\beta_e}.
\]

This is just AM--GM, not cascade depletion.  Summing such compulsory costs can
manufacture linear growth even for independent edges.  Any claimed circuit tax
must identify what exceeds this baseline.  Growth in one selected coordinate
normalization is still less informative.

## Exact dilation counterexample

The first Cycle 150 triad already refutes any claim that unit raw output alone
forces critical energy to grow with frequency.  For every positive integer
`N`, set

\[
 p=N(1,0,0),\qquad q=N(0,1,0),\qquad k=N(1,1,0),
\]

and take the real Fourier field supported on `+-p,+-q` with

\[
 u_p=A(0,1,1),\qquad u_q=A(1,0,1),\qquad
 u_{-p}=u_p,\quad u_{-q}=u_q.
\]

The exact symmetrized Leray interaction is

\[
 B_k(u_p,u_q)+B_k(u_q,u_p)=NA^2(0,0,2).
\]

Choose `A=(2N)^(-1/2)`.  The designated output then has Euclidean norm one for
every `N`.  Reality supplies the conjugate output at `-k`; it is not a second
independent throughput constraint.  Meanwhile the complete input critical
energy is

\[
 E_c=2|p||u_p|^2+2|q||u_q|^2
 =2N(2A^2)+2N(2A^2)=4,
\]

again for every `N`.  Thus the dilation `N -> infinity` has unit physical
orbit-output norm and constant critical energy.  The derivative factor `N` in
the symbol is exactly cancelled by critical amplitude scaling; it cannot by
itself yield an energy-growth tax.

There is also a normalization-fiber warning already on this one triad.  Keeping
the product of the two physical input amplitudes fixed while replacing them by
`rA` and `r^(-1)A` preserves the bilinear output, whereas its critical energy is
proportional to

\[
 r^2+r^{-2}.
\]

It has a finite invariant minimum at `r=1` but can be made arbitrarily large
along this reciprocal scaling symmetry.  This scaling changes the physical
field, so it is not literally a change of polarization coordinates; it is a
noncompact symmetry of the unit-output constraint.  Consequently a recursively
selected representative of that constraint can manufacture apparent energy
growth even when the constrained minimum does not grow.

## Decision

"Unit designated critical throughput" is admissible only after specifying an
orbit-level physical functional, its homogeneity and dilation law, and
minimization over representation gauges and reciprocal-amplitude constraint
symmetries.  The simple real symmetric
dilation family above disproves a frequency-uniform energy-growth conclusion
from unit bilinear output alone.  It does not refute a genuinely global theorem
for many distinct cascade edges: such a theorem must prove excess joint cost or
off-circuit depletion after the invariant constrained minimization.

This is a normalization no-go, not a Navier--Stokes regularity theorem or a
blowup construction.
