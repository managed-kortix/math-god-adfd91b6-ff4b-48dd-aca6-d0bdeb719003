# Routes

## Cycle 234 direct boundary insertion

Cycle 234's proposed closure is retracted.  The finite endpoint-sector
decomposition and endpoint operator-norm bounds are sound, but full-face fusion
does not define an exact polymer factorization.  Spatially disjoint component
families can overlap in time, have no global vacuum cut, and still contain no
intersecting chain between the temporal faces.  Although their union charges
all time layers, that repair and an exact configuration-to-gas identity are not
proved, so the marked KP estimate and two-face decay do not follow as written.
The Cycle 232 endpoint remains bulk-only and the explicit Cycle
233 number remains a cyclic-subspace bound. See
`cycle-234-direct-boundary-insertion.md`.

## Cycle 232 hostile bulk-polymer correction

For a count robust under coincident `I/J` centers, the number of labelled
events is bounded by twice, not once, the support cardinality. The labelled
event graph still has degree at most 191 and at most 38 roots over a fixed
space-time point. A depth-first-walk injection therefore gives the explicit
rooted count `c'=2*191^4=2661726722`. With `q'=6c'=15970360332`, exact support
sizes 24 and 14 close the bulk Kotecky--Preiss criterion at
`|lambda|<=1/(8*(q')^416)` and allow `0<theta<log(3/e)` bulk tilt. This result is
strictly a bulk convergence certificate. It does not quantify the boundary
polymers created by the arbitrary-vector insertion and therefore does not give
a full-space spectral-gap constant. See
`cycle-232-independent-yarotsky-audit.md`.

## Cycle 231 bulk activity/KP candidate audit

Specializing Cycle 230 to square-lattice `SU(2)` verifies `c_G=3/4`, `r=3`,
`s=1`, local bounded norm `4|lambda|`, and the finite support cardinalities
`7,12,37,27,27,19`. The proposed overlap-degree bounds 191 and 137 follow from
those supports. Yarotsky's Lemma 3 arithmetic is correct conditionally on a
valid exponential polymer count. The earlier count is not valid: coincident
`I` and `J` events defeat the claimed injection of events into support points,
so the event count need not obey the asserted `m<=n` bound. The resulting
polymer constant and numerical coupling claim are retracted. Boundary
insertions and the quantitative passage from bulk KP convergence to a gap on
the full untruncated Hilbert space are also missing. Cycle 231 proves no
numerical endpoint; Cycle 232 separately gives a corrected bulk-only endpoint.
See
`cycle-231-explicit-yarotsky-threshold.md`.

## Cycle 230 theorem: electric-product strong coupling

The canonical strong-coupling route bypasses the incompatible local Wilson
vacua of Cycle 229. On the ambient link tensor product,
`T=sum_e C_e` has the unique constant product vacuum and gap `c_G`, while each
Wilson plaquette multiplier is bounded and finite-range. Yarotsky's
infinite-dimensional cluster theorem therefore gives an existential interval
`|lambda|<lambda_Y(G,rho,d_s)` with a unique ground state and a volume-uniform
ambient gap after grouping outgoing link orientations into unit-cell sites.
Since the Hamiltonian commutes with the Haar Gauss projector and the constant
vacuum is physical, restriction preserves the same gap on the physical Hilbert
space. No physical-space tensor factorization or frustration-free interacting
blocks are needed.

At the level of the printed theorem statements, the quantitative boundary is
decisive. Yarotsky's theorem and the later
unbounded Lie--Schwinger theorem state only a sufficiently small coupling;
neither prints a numerical threshold. The explicit
Bravyi--DiVincenzo--Loss interval
`|epsilon|<=2^-17 Delta/(D J)` and gap `Delta/2` assumes
finite-dimensional qubits and two-local edge interactions, so it cannot be
inserted unchanged for four-link Wilson plaquettes on `L^2(G)`. Thus the
untruncated model has a rigorous qualitative volume-uniform strong-coupling
gap, but no explicit lambda endpoint from these citations alone. Cycle 231's
attempted reconstruction remains incomplete because its polymer count and
later boundary/gap constants are not established.
Strong coupling also lies opposite the continuum path
`lambda=2/g^4 -> infinity`. See
`cycle-230-strong-coupling-product-gap.md`.

## Cycle 228 local admission check: untruncated, not thermodynamic

For the full two-plaquette `SU(2)` operator on
`L^2(SU(2)^2)^Ad`, the coupled-spin triangle rule gives `T>=3Q`.
The bounded nonnegative Wilson potential, a fixed vacuum/first-shell trial
space, compact resolvent, and form-core convergence of the natural spin
compressions then give
`gap(K_lambda)>=(3+sqrt(9+2lambda^2))/2-2lambda` for
`0<=lambda<12/7`; at `lambda=1` this is `(sqrt(11)-1)/2`.
This is an untruncated fixed-block result, not a volume-uniform lattice bound.
For the canonical cover below, the block coupling is `7lambda/4`, so the
positive Cycle 228 interval reaches only the lattice parameter
`lambda<48/49`; it supplies neither an overlap-pencil bound nor continuum
control. See `cycle-228-two-plaquette-uniform-ritz-bound.md`.

## Cycle 229 theorem: canonical-block frustration obstruction

The Gauss-law non-tensor issue is not itself an obstruction to a bounded
overlap theorem. On the unconstrained link tensor product, gauge-invariant
local operators commute with the global Haar Gauss projector. For bounded
nonnegative overlapping two-plaquette block operators, the Knabe square
estimate gives a physical common-kernel gap
`gamma-22eta` from `h_B^2>=gamma h_B` and
`{h_B,h_C}>=-eta(h_B+h_C)`; 22 is the exact bulk link-overlap degree. Natural
electric and plaquette weights sum exactly to Kogut--Susskind, and the smallest
block is the Cycle 226 simultaneous-conjugation model at block coupling
`7lambda/4` after multiplying by seven.

The theorem does not directly cover these natural blocks because their electric
Casimirs are unbounded. For unbounded overlap pencils, the generalized quotient
and cutoff Schur protocol are only conditional: a separate argument must fix
product/form domains, closed semibounded realizations, cutoff compatibility,
and positive tail/resolvent bounds, and must prove an unbounded overlap theorem.
Cycle 228's electric floor supplies none of those missing overlap-domain steps.

The canonical local-ground-space implementation fails at positive magnetic
coupling. Unique positivity-improving two-plaquette ground states on overlapping
blocks cannot have a common vector: membership in both extended kernels forces
product factorization across exclusive and shared links, while the crossing
Wilson term forbids it. Local shifts therefore produce an empty common kernel,
so their square estimate does not bound `K-E_0(K)`; local-excitation projectors
and the basic detectability lemma inherit the obstruction. A live route needs a
non-frustration-free finite-size theorem with larger windows and boundary-energy
corrections, or controlled global-ground-state conditional expectations. See
`cycle-229-gauss-projected-finite-size-coercivity.md`.

Thus Cycle 228 and Cycle 229 are consistent: the former certifies the isolated
untruncated block gap in a bounded coupling interval, while the latter shows
that canonical shifted block vacua cannot turn that local gap into a
frustration-free volume-gap argument. Neither statement supplies a
thermodynamic gap, a continuum estimate, or a Yang--Mills mass gap.

## Active Cycle 227 gate: shared-link finite-size coercivity

Cycle 229 supplies the hostile normalization test. Uniformly positive
one/two-block gaps and compatible kernels are insufficient: a unit-projector
shared-sector chain with one boundary pin has local gap at least
`1-1/sqrt(2)` but a boundary-wave energy
`1-cos(pi/(2N-1))`. Standard Knabe survives because its strict finite-patch
threshold fails (already at equality for patch size two), and the actual
Kogut--Susskind two-plaquette block rejects this particular wave by `T>=3Q`.
Any admitted criterion must therefore state and certify a quantitative overlap
or patch threshold, not merely local positivity. See
`cycle-229-two-plaquette-hostile-family.md`.

The main funnel now asks for a gauge-reduced finite-size criterion, not another
isolated Ritz gap.  A passing architecture must fix its blocks, overlaps,
boundary convention, coupling range, and physical Hilbert spaces; prove an
explicit noncircular inequality from finitely many untruncated block constants
to a volume-uniform physical gap; and certify those constants with Casimir-tail
enclosures.  The two-plaquette simultaneous-conjugation reduction is the
mandatory smallest check: shared intertwiner sectors and the coupled electric
Casimir forbid tensor-product plaquette embeddings.  The gate closes either by
one proved criterion plus one strict certified block instance, or by an exact
counterexample to the declared overlap/coercivity inequality.  Continuum
tightness, reflection positivity, nontriviality, and OS reconstruction remain
later gates.  See `../cycle-227-strategic-rotation.md`.

Cycle 181 records the smallest nontrivial gauge-invariant `SU(2)` benchmark.
One square reduces to the class-function Jacobi operator with diagonal
`n(n+2)+lambda` and off-diagonal `-lambda/2`.  Its centered character atoms give
an exact finite generalized temporal matrix test, and a Sturm script computes
its Ritz gap.  This validates the atomic/temporal machinery but cannot test the
volume-uniform moving sectors or the OS continuum limit required by the route.

Scout lemma for `SU(2)`: after fixing a physical scale, prove a cutoff- and
volume-uniform contraction `<f,T^ceil(r0/a)f> <= q||f||^2`, `q<1`, on the
entire gauge-invariant physical subspace orthogonal to the vacuum. This would
transfer a gap only conditional on a separate nontrivial OS continuum limit.

Cycle 178 refines the finite-lattice route. With electric
`P_D=1_[0,D](C)`, project the interacting-vacuum complement onto `Q P_D H` and
prove a whole-low-block Wilson contraction. Its exact orthogonal tail is
`QH intersect ker(P_D)`. Ordered Duhamel expansion supplies a finite-volume
Casimir-tail bound, but its raw constants contain extensive `E_0` and `||W||`.
Cycle 179 rules out repairing this by a fixed global cube of bare local Casimir
cutoffs: product rotors, realized exactly as gauge-invariant loops sharing an
edge, retain a one-particle tail contraction at least `exp(-s gamma)` in the
infinite-volume supremum. Ground-state conjugation may itself be nonlocal and
gauge constrained. Cycle 180 proves the abstract replacement: uniform
variance-normalized imaginary-time connected decay on a dense local form core
gives the full gap by the spectral theorem, while an anchored polymer norm gives
that estimate only if it has a volume-uniform stable synthesis and a two-sided
Schur-summable connected kernel. Its product benchmark is exact: the incomplete
tensor product over the dressed vacuum is the support-labeled direct sum of
finite excitations, with frame constant one, and dressed local spectral tails
contract independently of all vacuum spectators. The shared-edge `U(1)` gauge
quotient preserves that isometry. The next production lemma must establish the
corresponding stable synthesis and tail exhaustion for the interacting physical
gauge vacuum; equal-time clustering alone is insufficient.
Continuum promotion also requires reflection-positive RG basin entry from bare
`g(a)->0`, where the strong-coupling parameter `2/g(a)^4` is large, followed by
a nontrivial OS limit.

Cycle 180 referee verdict: this is now an equivalence wall for main-funnel
purposes. The variance-normalized temporal criterion is gap-level by the
spectral theorem, while the interacting stable synthesis, temporal Schur bound,
and OS limit have no weaker jointly falsifiable production lemma. The exact
product benchmark is preserved, but Yang--Mills rotates.
