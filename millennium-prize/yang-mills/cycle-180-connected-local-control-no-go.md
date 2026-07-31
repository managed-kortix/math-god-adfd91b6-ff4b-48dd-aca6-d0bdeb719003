# Cycle 180: connected local control does not imply a gap

This hostile audit asks whether replacing the failed global Casimir cube by
anchored connected estimates could by itself close the Cycle 179 gap argument.
It cannot. There are uniformly finite-range local Hamiltonians whose selected
finite-volume ground states have exact connected clustering and exact local
tails, while their spectral gaps tend to zero. Two elementary families isolate
distinct missing hypotheses: an invisible decoupled sector and a rare
delocalized excitation.

Throughout, connected correlation means

\[
 \operatorname{Cor}_\Omega(A,B)
 =\langle\Omega,AB\Omega\rangle
  -\langle\Omega,A\Omega\rangle\langle\Omega,B\Omega\rangle .
\]

The examples concern the logical implication from ground-state local control to
a full-complement gap. They are not Yang--Mills models.

## Family I: an invisible soft sector

On a chain of `N` sites put two qubits `(a_i,b_i)` at every site and define

\[
 H_N^{(1)}=\sum_{i=1}^N n_{a_i}+\varepsilon_N\sum_{i=1}^N n_{b_i},
 \qquad n=|1\rangle\langle1|,
 \qquad \varepsilon_N=e^{-N}.
\tag{180.1}
\]

This is a translation-invariant, range-zero, frustration-free Hamiltonian apart
from the permitted `N`-dependent coupling. It has the unique product ground
state

\[
 \Omega_N=|0,0\rangle^{\otimes N}
\]

and exact gap

\[
 \Delta_N=\varepsilon_N\longrightarrow0,
\tag{180.2}
\]

witnessed by changing one `b` qubit to `|1\rangle`.

For observables on disjoint sets, the product state gives

\[
 \operatorname{Cor}_{\Omega_N}(A,B)=0.
\tag{180.3}
\]

Every reduced density matrix is also exactly supported on its local vacuum
vector. Thus any local tail defined relative to the actual one-site or
finite-block ground-state support vanishes identically, uniformly in `N`.
Nevertheless the full vacuum complement contains the soft `b` excitation and
has vanishing gap.

This example defeats a theorem whose assumptions only inspect the ground state.
Its loophole is explicit: the local interaction has no volume-independent lower
bound on nonzero excitation energies. Uniform interaction normalization from
above, finite range, frustration freeness, uniqueness, and perfect clustering
do not supply such a lower bound.

## Family II: a rare excitation with uniform local indistinguishability

The preceding coupling was visibly small. A second family uses only unit local
coefficients and makes the low-energy state globally delocalized. Take one
qubit per site on the open chain and let

\[
 H_N^{(2)}=n_1+\sum_{i=1}^{N-1} P^-_{i,i+1},
 \qquad P^-_{i,i+1}={I-S_{i,i+1}\over2},
\tag{180.4}
\]

where `S_(i,i+1)` swaps the two neighboring qubits. Every term is a projection
of range at most one and every displayed coefficient is one. The unique ground
state is the product vacuum

\[
 \Omega_N=|0\rangle^{\otimes N}.
\tag{180.5}
\]

Indeed, the common kernel of the swap-antisymmetry projections is the fully
permutation-symmetric spin multiplet: adjacent transpositions generate the
symmetric group. In its
sector with `k>=1` particles, no nonzero vector is annihilated by `n_1` (the
unique symmetric Dicke vector has occupation probability `k/N` at site one).
Thus the intersection with `ker(n_1)` is only the zero-particle vector.

The normalized uniform one-particle state

\[
 W_N={1\over\sqrt N}\sum_{j=1}^N |j\rangle
\tag{180.6}
\]

is annihilated by every bond projection and obeys

\[
 \langle W_N,H_N^{(2)}W_N\rangle={1\over N}.
\tag{180.7}
\]

The variational principle therefore gives

\[
 0<\Delta_N\le {1\over N}\longrightarrow0.
\tag{180.8}
\]

The ground state again has zero connected correlations at every positive
separation and exact ground-state-adapted local tails. More strongly, the soft
state is asymptotically invisible to every fixed local test. If `X` contains
`ell` sites, tracing out its complement gives

\[
 \rho_X(W_N)
 ={\ell\over N}|W_X\rangle\langle W_X|
  +\left(1-{\ell\over N}\right)|0_X\rangle\langle0_X|,
\tag{180.9}
\]

where `W_X=ell^(-1/2) sum_(j in X)|j>`. The two summands lie in orthogonal
number sectors, hence

\[
 \|\rho_X(W_N)-\rho_X(\Omega_N)\|_1={2\ell\over N}.
\tag{180.10}
\]

Consequently every norm-one observable supported on a fixed `X` distinguishes
the soft state from the vacuum by at most `2 ell/N`. Anchored local data can
therefore converge perfectly while a normalized state in the full vacuum
complement has energy `1/N`. The single order-one boundary pin selects a unique
vacuum but couples to the normalized delocalized excitation with probability
only `1/N`. This is a finite-volume rare-excitation obstruction with no small
Hamiltonian coefficient.

## Why GHZ and symmetry breaking are not the clean clustering example

The ferromagnetic Ising chain with exponentially weak tunneling has a small
finite-volume splitting, but its symmetric GHZ ground state does not satisfy
uniform connected clustering:

\[
 \langle Z_iZ_j\rangle-\langle Z_i\rangle\langle Z_j\rangle=1
\]

at arbitrary separation. Choosing one broken-symmetry product phase restores
clustering only after selecting a sector; the competing phase then exposes the
missing uniqueness or boundary-condition hypothesis. Thus GHZ is a useful
warning about sector mixing, not a counterexample to a theorem that genuinely
assumes uniform clustering of the selected finite-volume state.

Topological order gives the analogous conceptual warning: locally
indistinguishable sectors can have exact or exponentially small finite-volume
splittings. Invoking it rigorously would require specifying geometry,
boundaries, perturbations, and which ground state enters the clustering
assumption. Families (180.1) and (180.4) already prove the logical no-go without
those model-dependent inputs.

## Exact implication that remains missing

Exponential clustering is ordinarily a consequence of a gap under locality
hypotheses; the converse is false. Ground-state marginals and connected
correlators only test matrix elements inside the selected state. A spectral gap
is the coercive statement

\[
 \langle\psi,H_N\psi\rangle-E_{0,N}\|\psi\|^2
 \ge \Delta\|Q_N\psi\|^2
\tag{180.11}
\]

for every vector, including moving, delocalized, topological, and rare-droplet
states invisible to each fixed local window.

Therefore an anchored connected/polymer estimate is useful only if accompanied
by a separately proved local-to-global implication. Sufficient assumptions
would have to exclude the mechanisms above, for example through a uniform
finite-size criterion, local topological quantum order plus a local gap,
detectability/martingale bounds in an appropriate frustration-free setting, or
an explicit coercive decomposition controlling every sector. None follows
from clustering or summable local tails alone.

For the Yang--Mills funnel, Cycle 179's proposed replacement is thus narrowed:
one must not merely prove decay of connected dressed-vacuum polymers. One must
also prove a volume-uniform inequality of the form (180.11) on the entire
gauge-invariant vacuum complement, including global flux sectors and excitations
whose local density vanishes with volume. Connected local control without that
bridge cannot establish a mass gap. No Yang--Mills construction or mass gap is
claimed.
