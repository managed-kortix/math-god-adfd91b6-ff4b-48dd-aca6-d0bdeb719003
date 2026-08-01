# Routes

## Active Cycle 227 gate: shared-link finite-size coercivity

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
