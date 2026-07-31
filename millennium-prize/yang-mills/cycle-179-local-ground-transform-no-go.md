# Cycle 179: local ground-transform and Casimir-tail no-go

This hostile audit tests the proposed volume-uniform repair of the Cycle 178
tail estimate: conjugate by the interacting ground state, cancel the extensive
vacuum energy, and then impose a local electric/Casimir cutoff.  The first step
need not be local after the physical quotient, and the second step fails in
global operator norm even in a product model where the ground-state transform
is exactly local.  An overlapping-plaquette gauge model contains the same exact
counterexample.

## Why the ground-state transform is not automatically local

For a positive finite-volume ground state `Omega`, the formal Doob transform is

\[
 \widetilde H=\Omega^{-1}(H-E_0)\Omega.
\]

For a Schrödinger operator its first-order coefficient is the logarithmic
derivative of `Omega`.  Locality of `H` therefore does not imply locality of
`widetilde H`; it would require a separate finite-range or summable-cluster
theorem for `log Omega`.

The harmonic chain gives an exact elementary warning.  Let

\[
 H={1\over2}(-\Delta+q^TAq),\qquad A=m^2I+\kappa L,
\]

where `L` is the nearest-neighbor graph Laplacian.  Its ground state and
transform are

\[
 \Omega(q)=Z^{-1/2}e^{-q^TA^{1/2}q/2},\qquad
 \widetilde H=-{1\over2}\Delta+(A^{1/2}q)\mathbin\cdot\nabla.
\tag{179.1}
\]

Although `A` has nearest-neighbor range, `A^(1/2)` is generically dense on a
connected finite chain.  It decays when `m>0`, but it is not finite range, and
its decay constants become nonuniform as `m` tends to zero.  Compact interacting
rotors have the analogous linked-cluster expansion: connected terms in
`log Omega` occur at arbitrarily large diameter unless a convergence theorem
sums them with volume-independent constants.  Calling the transform local is
thus the desired cluster theorem, not a consequence of conjugation.

Gauge theory adds a second issue.  Both `Omega` and transformed test functions
must satisfy every Gauss constraint.  Individual link derivatives do not
preserve that subspace; the drift must be interpreted horizontally on the gauge
quotient.  Plaquette coordinates are also redundant on closed cells because of
Bianchi relations.  Thus independent plaquette derivatives and tensor-product
plaquette cutoffs generally do not define operators on the physical Hilbert
space.  Gauge fixing merely moves these constraints into a nonproduct quotient
measure, a Faddeev--Popov factor, or nonlocal residual variables.

## Product-rotor test

Let

\[
 h=-{d^2\over d\theta^2}+\lambda(1-\cos\theta),\qquad \lambda>0,
\]

on `L^2(S^1)`.  Write its normalized positive ground state as `phi`, its ground
energy as `e_0`, and choose a normalized first excited state `psi` with
`psi perpendicular phi` and energy `e_0+gamma`.  Let `p_D` project onto Fourier
modes `|n|<=D`.  The Fourier recurrence for the Mathieu ground state shows

\[
 a_D:=\|p_D\phi\|^2<1
\tag{179.2}
\]

for every finite `D`: if its Fourier series had a highest nonzero coefficient,
the recurrence one index beyond it would force that coefficient to vanish.

On `N` rotors set

\[
 H_N=\sum_{i=1}^N h_i,\quad
 \Omega_N=\phi^{\otimes N},\quad
 P_{D,N}=p_D^{\otimes N},\quad
 Q_N=I-|\Omega_N\rangle\langle\Omega_N|.
\]

The most favorable local Casimir low space is the cube in which every site has
degree at most `D`.  As in Cycle 178, let `Pi_(D,N)` project in `Q_N H_N` onto
`Q_N Ran(P_(D,N))`.  Its exact orthogonal tail is

\[
 {\cal T}_{D,N}=Q_N{\cal H}_N\cap\ker P_{D,N}.
\tag{179.3}
\]

The one-particle state

\[
 \Psi_N=\psi\otimes\phi^{\otimes(N-1)}
\]

is vacuum orthogonal and has exact excitation energy `gamma`.  Put

\[
 A_N=(I-P_{D,N})\Psi_N,\qquad B_N=(I-P_{D,N})\Omega_N,
\]

and remove the remaining vacuum component by

\[
 F_N=A_N-
 {\langle\Omega_N,A_N\rangle\over1-a_D^N}B_N.
\tag{179.4}
\]

Then `F_N` belongs to `cal T_(D,N)`.  Moreover

\[
 \|P_{D,N}\Psi_N\|
 =\|p_D\psi\|a_D^{(N-1)/2}\longrightarrow0,
\]

and

\[
 |\langle\Omega_N,A_N\rangle|
 =|\langle\phi,p_D\psi\rangle|a_D^{N-1}\longrightarrow0.
\]

Consequently `F_N -> Psi_N` in norm.  For the vacuum-normalized semigroup

\[
 S_N(s)=Q_Ne^{-s(H_N-Ne_0)}Q_N
\]

contractivity and `S_N(s)Psi_N=e^(-s gamma)Psi_N` give the exact obstruction

\[
 \liminf_{N\to\infty}
 \|S_N(s)(I-\Pi_{D,N})\|\ge e^{-s\gamma}
 \qquad(D<\infty).
\tag{179.5}
\]

The transform by `Omega_N` is a tensor product and is exactly local, so (179.5)
does not arise from a defective cluster expansion.  It arises because one
low-energy excitation can be accompanied by infinitely many spectator sites
whose dressed vacua have a nonzero bare-Casimir tail.  The probability that all
spectators lie in the local low cube is `a_D^(N-1)`, which tends to zero.

Thus a fixed local Casimir cube does not yield a volume-uniform global tail that
becomes small with `D`.  To keep the dressed vacuum inside the cube with fixed
probability one needs

\[
 N(1-a_D)=O(1).
\tag{179.6}
\]

The cutoff must therefore move with volume.  Exponential one-site Fourier tails
still require `D` of logarithmic order in `N` (up to the precise decay exponent).

## Exact overlapping-plaquette realization

The same example survives gauge invariance and plaquette overlap.  Take a
two-vertex `U(1)` graph with reference edge `e_0` and parallel edges
`e_1,...,e_N`.  The `N` loops

\[
 y_i=\theta_i-\theta_0
\]

are gauge invariant and all share `e_0`.  Haar measure on the physical quotient
is exactly product Haar measure in `(y_1,...,y_N)`.  Define the gauge-invariant
local loop Hamiltonian

\[
 H_N^{\rm loop}=\sum_{i=1}^N
 \left[-\partial_{y_i}^2+\lambda(1-\cos y_i)\right].
\tag{179.7}
\]

Every magnetic term is supported on a loop overlapping all the others at the
reference edge, yet after the Gauss quotient (179.7) is exactly the product
rotor Hamiltonian.  Plaquette Fourier/Casimir cutoffs are precisely
`P_(D,N)`, so (179.5) is an exact physical counterexample in a
plaquette-overlap model.  Adding overlap cannot establish a proposed estimate
that already fails in this gauge-invariant overlapping subclass.

For genuine higher-dimensional cell complexes the situation is less favorable,
not more: Bianchi constraints prevent independent plaquette coordinates, while
the electric metric on loop coordinates contains mixed derivatives.  A valid
positive theorem would have to control those effects in addition to defeating
the spectator mechanism.

## Consequence for the Cycle 178 route

Vacuum-energy subtraction is necessary, but it is not sufficient.  No estimate
of the form

\[
 \sup_N\|S_N(s)(I-\Pi_{D,N})\|\le r_D,
 \qquad r_D\longrightarrow0,
\tag{179.8}
\]

can hold for the fixed bare local-Casimir cube in the product rotor or the
overlapping-loop model above.  The lower bound is the physical one-particle
contraction, not an extensive artifact.

The surviving possibilities must change the norm or the decomposition: use an
anchored connected tail for a local observable, a polymer norm with spectator
vacua factored out, or local spectral projectors adapted to the interacting
ground state.  Any of these requires a new theorem relating that local control
to contraction on the entire vacuum complement.  A global union of bare local
Casimir tails does not provide it.  No Yang--Mills construction or mass gap is
claimed.
