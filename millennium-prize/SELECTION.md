# Cycle 1 funnel selection

Date: 2026-07-25

This is a strategic selection, not a claim that the selected problem is easier
or that any candidate lemma is new.

## Concrete candidates returned by the six route/breaker audits

| target | exact candidate bottleneck | official-target reach if proved | first exact test | principal breaker |
|---|---|---|---|---|
| BSD | rank-two ordinary cyclotomic-to-complex vanishing transfer | a restricted rank-two subfamily | `389a1`, `p=5` | cyclotomic derivatives are not complex derivatives |
| Hodge | Hilbert-component domination of a Hodge-locus component | codimension 2 for hypersurface fourfolds | Fermat cubic containing a plane | tangent equality need not imply actual/global dominance |
| Navier--Stokes | universal factor-2 amplification bound in critical `L^3` on the torus | full unforced periodic alternative | interval-validated triad search | pressure has no sign; the assertion may be stronger than regularity |
| P versus NP | polynomial anticheckers for unrestricted quadratic-size 3-COLOR circuits | only a fixed polynomial lower bound | finite circuit/hitting-set enumeration | memorization and lack of exponent amplification |
| RH | `O(1/log N)` norm bound for one explicit discrete Nyman--Beurling approximant | full RH, via the published discrete criterion | exact breakpoint integration with interval logarithms | estimate is already RH-strength and known analyses are conditional |
| Yang--Mills | cutoff/volume-uniform contraction of the physical block transfer operator | mass gap, conditional on a separate continuum construction | reflection-positive finite-lattice matrices | finite trial spaces give no lower bound on the whole spectrum |

## Scores

Scores are 1 (poor) through 5 (strong). “Reach” measures how directly the
lemma reaches the official quantifiers, not plausibility.

| target | exactness | falsifiability | transfer | formal/exact infrastructure | plausible local progress | reach | total |
|---|---:|---:|---:|---:|---:|---:|---:|
| BSD | 4 | 3 | 4 | 3 | 2 | 2 | 18 |
| Hodge | 4 | 3 | 3 | 3 | 3 | 2 | 18 |
| Navier--Stokes | 5 | 4 | 4 | 3 | 2 | 5 | 23 |
| P versus NP | 5 | 5 | 4 | 5 | 3 | 2 | 24 |
| RH | 5 | 5 | 4 | 5 | 4 | 5 | 28 |
| Yang--Mills | 5 | 3 | 4 | 2 | 2 | 2 | 18 |

## Decision

The first main funnel is **the Riemann hypothesis**, with the explicit
logarithmically smoothed discrete Nyman--Beurling norm bound as bottleneck.
The reason is operational: its implication reaches the full official target,
every finite approximant is explicit, and exact symbolic/interval artifacts
can attack transcription errors and candidate inequalities immediately. This
does not lower the epistemic estimate of the theorem: the breaker audit
correctly identifies it as RH-strength.

The other five candidates remain bounded scout lanes. Rotation requires a
proved checkpoint, decisive falsification, or a written strategic review.
