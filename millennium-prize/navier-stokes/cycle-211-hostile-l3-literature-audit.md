# Cycle 211: hostile literature and scaling audit of the universal `L^3` gate

## Verdict

No immediate theorem or scaling identity found in this audit proves or refutes

\[
 \sup_{0\le t<T_*}\|u(t)\|_{L^3(\mathbb T^3)}
 \le 2\|u_0\|_{L^3(\mathbb T^3)}.                    \tag{211.1}
\]

The statement is not a known standard a priori estimate. It is much stronger
than global regularity and should be treated as a deliberately fragile
production lemma, not as a literature-supported conjecture. The most relevant
recent rigorous arbitrary-growth theorem controls the initial datum in
`BMO^{-1}` or `B^{-1}_{infinity,1}`, not in `L^3`, and therefore does not
falsify (211.1). Recent periodic `L^3` optimization exhibits transient growth
but is numerical and stays far below a factor two in the reported runs.

## Scaling check

The Navier--Stokes scaling on `R^3`,

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
\]

preserves the `L^3` norm on `R^3` and hence preserves the amplification ratio.
On a fixed torus it is available only for compatible integer spatial
dilations; periodic replication makes each endpoint norm scale by the same
factor `lambda`, so the ratio is again unchanged.

Amplitude--time rescaling without spatial dilation gives

\[
 u(t,x)=\lambda w(\lambda t,x),\qquad \mu=\nu/\lambda.
\]

Both endpoint `L^3` norms acquire the same factor `lambda`. Thus large
amplitude only sends the effective viscosity toward zero; it does not iterate
or amplify a fixed Euler growth factor. Positive initial derivative likewise
does not contradict (211.1), because its physical persistence time shrinks by
`lambda^{-1}`. This agrees with the Cycle 50 and Cycle 59 calculations.

There is also no semigroup iteration contradiction. If (211.1) is restarted at
successive times it yields the weaker bound `2^n ||u_0||_3`, not a contraction
or a factor-one estimate. Conversely, endpoint continuation only needs some
finite bound along each trajectory, so regularity would not imply the linear,
data-independent factor in (211.1).

## Rigorous literature checks

1. Stan Palasek, *Arbitrary norm growth in the 3D Navier--Stokes equations*,
   arXiv:2509.18595, Theorem 1.1, constructs smooth global solutions on
   `T^3` whose initial data have a uniform `B^{-1}_{infinity,1}` bound and
   which later approximate an arbitrarily large prescribed shear. Its
   corollaries rule out many a priori bounds from `BMO^{-1}` data. This does
   not compare the later `L^3` norm with the initial `L^3` norm: the embedding
   is `L^3 -> BMO^{-1}`, not the reverse, and the construction supplies no
   uniform upper bound for `||u_0||_3`. It is therefore a close hostile warning,
   but not a falsifier of (211.1).

2. Bourgain--Pavlovic, *Ill-posedness of the Navier--Stokes equations in a
   critical space in 3D*, JFA 2008, proves norm inflation in
   `B^{-1}_{infinity,infinity}`. Later norm-inflation results found in this
   search concern similarly weak critical spaces or scaling-supercritical
   Sobolev/Besov spaces. They do not transfer to `L^3`, where mild solutions
   are locally well posed and small data are globally controlled.

3. Elkin Ramirez and Bartosz Protas, *The Ladyzhenskaya--Prodi--Serrin
   Conditions and the Search for Extreme Behavior in 3D Navier--Stokes
   Flows*, arXiv:2604.13338, Section 6.1, directly optimizes final `L^3` on a
   periodic domain. It reports transient `L^3` growth for all displayed
   extremizers but describes it as weak. Reading the plotted values gives
   ratios only around `1.04--1.10`, not two. These are floating spectral
   computations and local optimization, so they neither prove a lower bound
   nor exclude a factor-two crossing elsewhere.

4. Palasek's introduction points to Jia--Sverak's `L^3` critical compactness
   theory and notes that critical `L^3` quantitative control is expected to be
   tied to regularity. That literature concerns existence of a
   data-dependent control function or smoothing bound, not a universal linear
   multiplier such as two.

## Embedded two-dimensional check

For 2D Euler, vorticity is rearranged, so every vorticity `L^p` norm is
conserved. Biot--Savart and Sobolev give

\[
 \|u(t)\|_3\le C\|\omega_0\|_{6/5},
\]

but this is data-dependent relative to `||u_0||_3`: highly oscillatory
vorticity can have a large `L^{6/5}` norm while its velocity has small `L^3`.
Hence 2D conservation does not supply a universal amplification factor.

The converse idea would be a decisive falsifier: construct a smooth 2D Euler
orbit that unmixes fine-scale vorticity into low frequencies and has velocity
`L^3` ratio greater than two, then transfer it to sufficiently small positive
viscosity on a fixed finite interval and embed it in `T^3`. The literature
search found rigorous vorticity-gradient growth and inviscid-damping results,
but not this same-norm velocity `L^3` statement on `T^2`. The AIM problem list
*Small scale dynamics in incompressible fluid flows*, item 8, explicitly poses
2D Euler norm inflation for velocity in `H^s`, `0<s<1`, and asks the same
question for `L^p`, `p != 2`; this is useful evidence that the required 2D
falsifier is not a routine known theorem, but the problem list is not itself a
primary theorem source.

Time reversal makes any rigorous Euler mixing trajectory a possible unmixing
trajectory, but viscosity is not reversible. A usable argument must first
produce a strict finite-time Euler ratio greater than two and then invoke a
quantitative inviscid limit with enough margin. Vorticity-gradient growth alone
does not imply velocity `L^3` growth; it may instead move vorticity to high
frequencies and reduce negative-order velocity norms.

## Immediate gate

There is no theoretical contradiction to record. The quickest credible
falsifier remains either:

1. a full-PDE interval certificate for one periodic 2D Navier--Stokes
   trajectory with ratio greater than two; or
2. a rigorous finite-time 2D Euler unmixing example with ratio `>2+delta`,
   followed by a quantitative inviscid-limit transfer.

The first frozen five-frequency campaign is still logically valid, but the
Ramirez--Protas computations suggest that a factor-two crossing is not a small
perturbation of their numerically optimized 3D extremizers. Failure of that
box should trigger a structural unmixing/inverse-cascade search rather than
blind enlargement. No Navier--Stokes regularity result is claimed.
