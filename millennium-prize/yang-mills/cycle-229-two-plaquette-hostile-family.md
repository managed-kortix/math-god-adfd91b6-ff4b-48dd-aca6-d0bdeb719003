# Cycle 229: hostile two-plaquette family and the Knabe threshold

## Scope

There is no valid implication from merely positive one- and two-plaquette gaps,
compatible local kernels, unit interaction norms, and nearest-neighbor overlap
to a volume-uniform gap. The exact family below defeats every proposed
two-plaquette criterion using only those qualitative data. It does not defeat a
criterion with a quantitative Knabe threshold or an additional bulk mass term.
In particular, it is not a counterexample to the Kogut--Susskind Hamiltonian.

## Exact moving-vacuum-complement family

On an open chain of `N` two-level plaquette sectors let

\[
 n_i=|1\rangle\langle1|_i,\qquad
 h_{i,i+1}={I-S_{i,i+1}\over2},\qquad
 H_N=n_1+\sum_{i=1}^{N-1}h_{i,i+1}.                       \tag{229.1}
\]

Every term is a projection, has coefficient one, and is supported on at most
two adjacent plaquettes. The Hamiltonian is frustration free. The common
kernel of the `h` terms is the permutation-symmetric subspace. In every
nonzero-particle symmetric sector the occupation of site one is nonzero, so
the boundary pin leaves the unique ground state

\[
                         \Omega_N=|0\rangle^{\otimes N}.   \tag{229.2}
\]

The interior two-site block `h` has nonzero gap one. The only exceptional
two-site block is the left boundary block `n_1+h_(1,2)`. In its one-particle
basis it is

\[
 \begin{pmatrix}3/2&-1/2\\-1/2&1/2\end{pmatrix},
\]

and hence has nonzero eigenvalues `1-1/sqrt(2)` and `1+1/sqrt(2)`; its
two-particle eigenvalue is one. Thus all one- and two-site nonzero local gaps
are bounded below by the volume-independent constant

\[
                         \delta_2=1-1/\sqrt2.              \tag{229.3}
\]

Nevertheless the global gap vanishes. In the one-particle basis `|j>` put
`M=N-1`, `theta=pi/(2M+1)=pi/(2N-1)`, and

\[
 v_N=\sum_{j=2}^N\sin((j-1)\theta)|j\rangle.              \tag{229.4}
\]

The pin annihilates this trial vector. The discrete Dirichlet--Neumann sine
identity gives exactly

\[
 {\langle v_N,H_Nv_N\rangle\over\langle v_N,v_N\rangle}
 =1-\cos {\pi\over2N-1}.                                  \tag{229.5}
\]

Therefore

\[
 0<\Delta_N\leq1-\cos {\pi\over2N-1}
 < {\pi^2\over2(2N-1)^2}\longrightarrow0.                \tag{229.6}
\]

The cruder uniform wave has energy `1/N`; (229.4) identifies the sharper
boundary mode. Both are moving vacuum-complement states whose density in any
fixed window tends to zero.

## Shared-link intertwiner realization of the obstruction sector

The smallest simultaneous-conjugation two-plaquette space from Cycle 226
contains the exact orthonormal vectors

\[
 \Omega=\Phi_{00}^0,\qquad
 L=\Phi_{1/2,0}^{1/2},\qquad R=\Phi_{0,1/2}^{1/2}.         \tag{229.7}
\]

The antisymmetric local projector in (229.1) is precisely

\[
       h_{LR}=|(L-R)/\sqrt2\rangle\langle(L-R)/\sqrt2|.   \tag{229.8}
\]

Thus every local exchange projector in the soft-chain mechanism has an exact
copy in the shared-link `c=1/2` intertwiner sector: it penalizes the difference
between the two placements of one fundamental loop. Consecutively identifying
the right placement in one abstract block with the left placement in the next
gives the tridiagonal quadratic form in (229.5). This is an exact compatibility
model for the overlap sector; it shows that local Gauss invariance and the
two-block intertwiner data alone do not prevent a diffusive boundary mode.

The qualification is essential. Equation (229.8) is not the magnetic-plus-
electric Kogut--Susskind interaction, and no full lattice-gauge restriction map
realizing the entire qubit chain is asserted here. It is a hostile compatibility
model for testing the logical hypotheses of a proposed local-to-global theorem.
Any claimed theorem using only the local shared-sector data and (229.3) is false
by (229.6); a theorem whose hypotheses include stronger global physical
restriction maps must be tested against those maps separately.

## Why the Cycle 226/228 Kogut--Susskind block rejects this mode

For the actual two-plaquette electric operator,

\[
 T\Phi_{ab}^c=(3C_a+3C_b+C_c)\Phi_{ab}^c.
\]

Both `L` and `R` in (229.7) have electric energy three. More generally the
triangle rule proves `T>=3Q`, and the Wilson potential is nonnegative. A
superposition which moves one `L/R` excitation therefore retains an order-one
bare electric cost; the shared Casimir has the helpful sign and cannot produce
(229.6). This disposes of the most direct moving-loop and `c=0` hostile
attempts in the two-plaquette model. It does not prove a volume gap, because
the global interacting vacuum complement is not the bare-vacuum complement and
subtracting the extensive interacting ground energy is not a local operation.

## Why standard Knabe survives

Knabe's argument does not infer a global gap from positivity of `delta_2`.
For a translation-invariant frustration-free chain of nearest-neighbor
projections, its finite-size hypothesis requires a strict patch-gap threshold;
in the usual normalization a length-`m` open patch must satisfy

\[
                         \gamma_m>{1\over m-1}.            \tag{229.9}
\]

At `m=2`, the local projection gap is one and the threshold is also one, so the
required inequality is not strict. The hostile family is additionally open and
boundary-pinned, outside the standard periodic translation-invariant statement.
Larger patches expose rather than hide the problem: the same sine wave gives
patch gaps of order `m^-2`, below the order `m^-1` Knabe threshold.

Algebraically, the patch threshold is what controls the potentially negative
adjacent anticommutators in `H_N^2`. In (229.1) these overlap terms accumulate
into the discrete Laplacian and create the soft mode. A proposed gauge
finite-size criterion must likewise include an explicit quantitative overlap
or patch threshold, with the physical restriction maps and boundary sectors
built in. Positive two-plaquette coercivity by itself is insufficient, while
standard Knabe is untouched.

## Verdict

The exact family (229.1)--(229.6) retires every qualitative two-plaquette
coercivity-to-global-gap proposal that records only uniformly positive local
gaps, bounded overlap, and compatible kernels. The exact shared-link local
sector admits the antisymmetric exchange projector, while the abstract glued
family exhibits both the moving wave and its boundary-softened version. The actual Cycle 226
Kogut--Susskind block excludes this particular mechanism through `T>=3Q`, but
that fact alone is not a local-to-global theorem. The live admission gate is a
declared quantitative Knabe-type inequality whose strict finite-patch threshold
can be tested in the untruncated gauge-reduced blocks.
