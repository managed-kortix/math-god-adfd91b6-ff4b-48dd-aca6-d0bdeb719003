# Hostile audit of the integrated `m=9` final-row chain

## Scope and verdict

This audit covers the source and certificate composition for ticks 46--48:
the reduced `k=6` model and 1,110-leaf campaign, the common reduced `k=5`
model and 931-leaf campaign, and their composition with the human `k<=4` and
perfect-matching branches.  It does not claim SNC or all order 18.

Verdict: the mathematical one-way reductions and both finite covers are
accepted.  A genuine counterexample in one of the three final cells projects to
the corresponding reduced model, then to at least one covered leaf; every leaf
has a retained checked LRAT.  The reduced models deliberately omit conditions
and need not lift back to counterexamples.  UNSAT is used only in the sound
one-way direction.

## Reduction map

For `(rho,k)=(0,6)`, all seven B vertices dominate both deleted C vertices.
Deleting C leaves degree sequence `8^9,6^7`, hence exactly six holes.  Robust
root conditions give `w -> {z} union A'`, no `w -> B`, a complete z row, and an
A' predecessor in every B column.  Every A' vertex has a B outneighbor; those
two deleted C vertices are exact second neighbors, so badness requires at least
two inaccessible T vertices.  These are exactly necessary clauses of
`k6_reduced_cnf.py`.

For `(rho,k)=(0,5)` and `(1,5)`, six B vertices dominate both C vertices and
one exceptional B vertex dominates one.  Deleting C leaves the common degree
sequence `8^9,7,6^6`, hence exactly five holes.  Every A' row hits B.  A row
hitting the degree-six class sees two deleted exact second neighbors and needs
two inaccessible T vertices; otherwise its exceptional-B hit supplies one and
it needs one.  These are exactly necessary clauses of `k5_reduced_cnf.py`.

For a selected inaccessible pair `{t,u}`, summing exact rows and partitioning
all global holes gives the packet identity used by the leaf generators.  In
`k=6` the defect is two for each B endpoint; in `k=5` it is two on K, one on
the exceptional B vertex, and zero elsewhere.  The singleton `k=5` identity is
the corresponding one-row specialization.  The exact-pressure clauses are
therefore redundant necessary conditions, not extra assumptions.

## Independent cover census

A separately written labelled enumeration confirms:

- `k=6`: 1,110 unique semantic orbits, labelled multiplicity 3,171,168,
  payload SHA-256
  `3979f9dca4f134055b87b3485b95e9601f3263c50031471fbf0659902abbb970`;
- `k=5`: 931 unique semantic orbits, labelled multiplicity 758,181,
  payload SHA-256
  `020cbf130cd806d3a91fa11a29dfdbae67e89e97a47d6e1708c10f3a9f45deb5`.

For `k=5`, the audit explicitly compared the independently generated key set to
the production key set: 931 versus 931, with no missing, extra, or duplicate
key.  The committed checker was hardened to perform this equality test rather
than merely looking up production rows in the independent multiplicity table.

## Archive and replay identities

- `k=6`: 103,486,540 bytes, SHA-256
  `e44f8ff81d272a9f9e4b060d37aa51cdbd560552fd3ced2a1d5f98d94bb80402`;
  1,110 leaf records, 651 content-addressed proof objects, and 602,210,046
  referenced raw LRAT bytes.
- `k=5`: 120,197,280 concatenated bytes, SHA-256
  `d3f845d980390cac63930b8b7228eba295dbb598f6d261148aab22cf137c0f1d`;
  931 leaf records, 853 proof objects, and 917,003,695 referenced raw LRAT
  bytes.

Fresh source-identical checker replay accepted all 2,041 leaves.  The checker
source is drat-trim commit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, source SHA-256
`bf07c2ac96b9035da1ebcc578cb95e956a2b795629d613154cdb307f8a8f4a95`.
Current compiler output is not bit-identical to the historical checker ELF, so
this is explicitly source-identical semantic replay, not historical binary
reproduction.  The verifier scripts were hardened to use explicit exceptions,
require exactly one literal `c VERIFIED`, and create their work directories;
`python -O` can no longer bypass their integrity gates.

## History integration

The historical closure tip `8964032c` was preserved remotely before
integration.  Current commits have different parents and hashes because the
chain was composed onto the current lane.  Every tick 46--48 source, cover,
verifier, note, and archive used by the result was blob-identical before the
verifier hardening.  The composition did not silently alter the mathematical
models or proof bytes.

## Exact conclusion

The complete nine-missing-pair branch of an order-18 minimal counterexample is
empty: a missing graph with no isolate is `9K2`, while an isolate yields one of
the 28 rooted cells, closed by the written `k<=4` proofs or the retained
`k=5,6` packages.  The remaining order-18 frontier is `m in {5,6,7}`.  This is
not an order-18 theorem and not a solution of Seymour's conjecture.
