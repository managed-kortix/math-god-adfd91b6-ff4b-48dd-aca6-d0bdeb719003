# attack plan — positive square energy

## Target

Conjecture 1.2 of arXiv:2506.07264v1: every connected n-vertex simple graph
with m >= n+1 satisfies s^+(G) >= n.

## Ranked lines of attack

1. **Sparse census beyond n=9.** Enumerate nonisomorphic connected graphs at
   n=10, beginning m=n+1 and increasing m. Float-screen s^+-n, retain a wide
   safety margin, then certify all near-minimizers by exact characteristic
   polynomial/root isolation. A counterexample is immediately certificate-shaped.
2. **Extremal family discovery.** Mine low-slack graphs for common cores,
   pendant-tree attachments, inertia, and equitable partitions; conjecture and
   prove a reduction or an infinite-family formula.
3. **Triangle-unicyclic bridge.** Although outside Conjecture 1.2 at m=n,
   understand the paper's bottleneck (Conjectures 9.1/9.4) to derive a gluing
   inequality robust under adding one edge.
4. **Local transformations.** Test whether leaf relocation, subdivision, or
   edge addition monotonically controls s^+ in the low-slack regime.

## Current line

Line 1: n=10,m=11 through 17 fully exact-certified in SymPy and independently
checked in PARI. Full m=18 passed both engines on all 561,106 graphs, with all
chunk hashes/counts aggregated; cumulative total 1,334,971. Fresh reproduction
passed. Full m=19 now passes both engines on 795,630 graphs; cumulative total
2,130,601. Fresh m=19 reproduction is active in 32 checkpointed chunks. The
m=20 slice has been float-screened and its low 50 certified in both engines.

## Next experiments

1. Complete and aggregate the active fresh m=19 reproduction.
2. Run full paired certification for m=20; the 1,032,754-graph count remains
   tractable under the compact chunk pipeline.
4. Package the cumulative n=10 census and compare precisely with what the paper
   already proves via diameter two or claw-free hypotheses.
4. Extend structural fingerprints from each minimizer to the low 50, especially
   testing triangle-free, claw, inertia, and diameter-two frequencies.
5. Package the completed gluing-lemma proof for all equal odd-cycle dumbbells
   and adversarially check every inequality and hypothesis against the paper.

## Running jobs

- `job-m18-sympy.pid`: 24 atomic input chunks, 12 outer jobs x 2 SymPy
  workers, COMPLETE, exact rational isolation width <10^-6. Input SHA-256
  `b47af8111f2d07caf6fa2d09bba7351d9fa5969bbac63ea0ae3669e2cfe8bdc2`.
- `job-m18-pari.pid`: COMPLETE, 24/24 atomic chunks, 561,106 total graphs,
  every exact charpoly parsed and every 80-digit slack positive.
- `job-m18-fresh.pid`: COMPLETE. Final standalone aggregate exactly reproduced
  both engines, all counts/hashes, minimizer, and bounds.
- `job-m19-sympy.pid`: active, 32 atomic chunks, 16 outer x 2 workers,
  COMPLETE, exact rational isolation width <10^-6; input hash
  `2178cc8ac8ce524cc43ab6671573c0830e2b57df387b8b95c7d275e93d62e041`.
- `job-m19-pari.pid`: COMPLETE, 32/32 chunks and 795,630 graphs; aggregate
  pairing completed successfully.
- `job-m19-fresh.pid`: ACTIVE, regenerated input with 32 atomic chunks; fresh
  SymPy stage precedes fresh PARI and standalone aggregation.
- `job-known-classes.pid`: active count of diameter-two/claw-free theorem
  coverage for the complete m=18,19 slices.

## Verification discipline

Numerical eigenvalues are search heuristics only. Any claimed inequality,
counterexample, or extremizer requires a standalone exact certificate, a fresh
process, a second engine, and statement/novelty checks.

## Retreat criteria

After roughly two weeks without either a new certified finite bound, a proved
structural lemma, or a promising extremal family despite census and theory
work, write a post-mortem and reconsider the queue.
