# Bounded novelty and publishability audit: finite-lattice gap and KI240

## Decision

This is an internal research audit, not a publication action. Neither result
solves a Millennium Prize Problem, and no submission, public announcement,
author contact, or publication-manifest entry is authorized by this audit.

The explicit finite-lattice strong-coupling gap is the stronger paper candidate.
It appears to add a quantitative specialization and a repaired full-Hilbert
boundary argument to an existing qualitative perturbation theorem. The Hodge
`KI240` result is mathematically useful inside the project, but its abstract
Karoubi theorem is close to standard connective/minimal-model and idempotent-
completion technology; its potentially new content is the specialized
application to the seven graph sheaves, not the general categorical principle.

Both candidates remain `HOLD` pending independent line-by-line proof review and
a primary-source literature audit. This bounded search supports no priority
claim.

## 1. Explicit finite-lattice strong-coupling gap

### Audited statement

For the square-spatial-lattice `SU(2)` Kogut--Susskind rotor, on periodic tori
large enough to realize the declared cells without self-identification, the
Cycle 235 packet claims

\[
 |\lambda|\le {1\over8(15970360332)^{416}},\qquad
 \Delta_\Lambda(K_\lambda)\ge
 {\log3-1\over56\log15970360332}.
\]

The lower bound is volume independent and is claimed first on the ambient link
Hilbert space and then on the reducing Gauss-invariant subspace. It is a
finite-lattice, extremely strong-coupling theorem. It is not a weak-coupling
continuum theorem, and it advances none of OS reconstruction, nontriviality,
Euclidean invariance, or a continuum physical mass.

### Relation to prior theorems

1. Yarotsky's 2005/2006 weak-interaction theorem already gives a unique ground
   state and a positive volume-uniform gap for sufficiently small local
   perturbations of a product system, including suitable infinite-dimensional
   one-site spaces. After grouping outgoing links into cell sites, the bounded
   Wilson plaquette interaction fits that qualitative framework. Thus existence
   of some strong-coupling lattice interval is not new.
2. Later Lie--Schwinger/block-diagonalization results likewise provide small-
   coupling gap stability, but the cited statements use an unspecified small
   threshold in the relevant infinite-dimensional setting. The explicit qubit
   constant of Bravyi--DiVincenzo--Loss does not directly cover four-link
   Wilson multipliers on `L^2(SU(2))`.
3. The claimed increment is quantitative and proof-level: an explicit rooted
   event count allowing coincident `I/J` centers, an explicit KP tilt, a typed
   marked-boundary gas for arbitrary entangled endpoint vectors, a treatment of
   the all-`J` transmission string, an open-ball full-Hilbert spectral argument,
   and transfer through the commuting Gauss projector.
4. Consequently the theorem should be described as an explicit quantitative
   specialization/reconstruction of Yarotsky's mechanism, not as the first
   strong-coupling lattice gap and not as a Yang--Mills mass-gap result.

### Novelty and publishability assessment

- **Potential novelty: moderate.** The bounded searches performed for this
  audit did not locate a prior printed numerical interval and numerical
  volume-uniform gap for this untruncated Hamiltonian rotor with the same
  full-Hilbert and Gauss-projected scope. That is only negative search evidence,
  not a priority finding.
- **Mathematical value: real but specialized.** The constants are intentionally
  enormous and nonoptimal; their value is effectivity and the repair of a
  boundary-completeness step, not physical scale.
- **Publishability: plausible after reworking.** A paper could be viable as an
  effective perturbation/cluster-expansion result if it is made self-contained,
  states the exact spatial dimension and boundary convention in the theorem,
  and reproduces every imported Yarotsky identity with source-compatible
  notation.
- **Current status: not submission-ready.** The key marked-polymer identity and
  activity majorant are project proofs rather than independently reviewed
  literature facts. Their dependence on the exact `I/J` expansion must be
  checked directly against the primary paper, including signs, supports,
  periodic wraparound, compact-resolvent continuity, and endpoint sector sums.

### Internal paper-worthy partial result

The paper-worthy partial result to retain is:

> An effective full-Hilbert-space version of the product-vacuum cluster
> expansion for the periodic square-lattice `SU(2)` Kogut--Susskind Hamiltonian,
> including arbitrary entangled temporal boundary vectors and Gauss restriction,
> with the explicit sufficient coupling and gap bounds above.

This is narrower and more defensible than any continuum framing. It should be
kept internal under `HOLD`; this audit does not create a manuscript, manifest
record, announcement, contact, or submission task.

## 2. Hodge `KI240`

### Audited statement

Let `F_k=O_{Gamma_(u^k)}` for `u=2+i`, `0<=k<=6`, on the declared CM abelian
sixfold, and let `C=thick<F_0,...,F_6>`. Cycle 241 claims that the finite twisted-
complex category is already idempotent complete because its minimal Ext
category is connective and has degree-zero algebra `C^7`. Combined with the
Cycle 200 finite-twisted-complex obstruction theorem, this gives

\[
 E\in C,\quad [E]=\xi
 \quad\Longrightarrow\quad
 o_v(E)\ne0\text{ for some declared PEL direction }v.
\]

This excludes one graph-generated support category as a source of a fully
deformable representative of `xi`. It neither constructs an algebraic cycle on
a general fiber nor proves a case of the Hodge conjecture.

### Relation to prior theorems

1. Idempotent/Karoubi completion of triangulated and dg categories is a mature
   subject; Keller's dg-category framework, Balmer--Schlichting-type completion
   results, work on homotopy categories and idempotent completeness, and
   weight/t-structure methods are the immediate prior-theorem neighborhood.
2. The conceptual assertion that a connective dg or `A_infinity` category with
   an idempotent-complete semisimple degree-zero heart has an idempotent-complete
   finite pretriangulated hull is therefore unlikely to be novel as a bare
   existence theorem. Cycle 241 itself calls it a familiar statement.
3. The displayed defect iteration
   `delta -> -3 delta^2 + 4 delta^3`, the terminating strictification in a
   packet-dependent nilpotent filtration, and the finite conjugator
   `ep+(1-e)(1-p)` may provide a useful explicit normal-form proof, but an
   explicit proof of a standard consequence is not automatically a new theorem.
4. The specialized increment is the combination with the graph Ext calculation,
   generic Euler-multiplicity coordinates, the Cycle 200 no-go, and Atiyah
   naturality to close the previously open noncentral-retract corner for this
   particular seven-generator category.

### Novelty and publishability assessment

- **Abstract Theorem 241.A: low novelty confidence.** It should not be marketed
  as new until a specialist maps it precisely to existing results on minimal
  perfect dg modules, bounded weight structures, and idempotent completeness.
- **Specialized `KI240` application: possible narrow novelty.** The exact graph
  configuration and obstruction conclusion may be new, but its interest depends
  on the significance and correctness of the upstream Cycle 151--200
  construction. It is an exclusion theorem for one support category, not a
  positive Hodge result.
- **Publishability: insufficient as currently isolated.** A categorical note
  containing only Theorem 241.A risks being regarded as folklore with an
  overlong proof. A Hodge-facing paper would need the entire graph construction,
  Ext computation, deformation setup, and obstruction theorem presented
  self-containedly, followed by expert validation of the global obstruction
  step.
- **Proof-risk concentration:** the most consequential step is not the
  polynomial idempotent correction itself but the finite dg realization and
  transfer claim: the filtration must be multiplicative and nilpotent for every
  packet, the quotient differential must vanish, strictification must survive
  transfer and restoration of contractible pairs, and the resulting image must
  fall literally within the scope of Cycle 200. These points need an external
  categorical referee.

## 3. Bounded literature evidence

The audit checked the project's cited primary relations and ran bounded metadata
searches through Crossref and OpenAlex. Relevant located records included
Yarotsky's *Ground States in Relatively Bounded Quantum Perturbations of
Classical Lattice Systems* (DOI `10.1007/s00220-005-1456-9`), Keller's *On
Differential Graded Categories* (DOI `10.4171/022-2/8`), Schnurer's *Homotopy
categories and idempotent completeness, weight structures and weight complex
functors* (arXiv `1107.1227`), and Liu--Sun's *Idempotent completion of
pretriangulated categories* (DOI `10.1007/s10587-014-0114-9`). Search results
were noisy and not theorem-text complete. No claim of exhaustive coverage,
novelty, or priority follows.

## 4. Internal disposition

1. Retain the finite-lattice theorem as the principal paper-worthy partial
   result, labelled `HOLD -- independent proof and primary-source audit needed`.
2. Retain `KI240` as an internal structural closure theorem, with the abstract
   component presumed prior-adjacent until a specialist citation map proves a
   sharper novelty distinction.
3. Preserve all explicit non-Millennium scope statements. Do not use "mass gap"
   without the modifiers "finite-lattice" and "strong-coupling" for the Yang--
   Mills result, and do not call `KI240` a Hodge-conjecture result.
4. Do not initiate publication workflow unless a separate solved-problem or
   publication instruction is issued after independent validation.
