# Tick 49: m=5 B6 certificate and witness audit

## Status

This is a hostile repair of the durable-certificate route.  It does not close
the five-hole branch.  The direct 4,355-parent run remains a local observation
until its proof objects have immutable storage and survive complete fresh
readback.

## Exact witness-orbit correction

In each two-high residual row the three vertices of `C` form a transitive
tournament.  Write them as `x -> y -> z`, `x -> z`, where `x,y` are high, and
let `b0` be the head of the unique `C -> B` arc, necessarily `y -> b0`.
After this normalization `b0` is distinguished.  A robust witness in `B` for
deletion of `x` therefore has two orbits: `b0` and a non-tail `b1`.  A witness
for deletion of `y` is either the internal predecessor `x` or a vertex of `B`.
If the source witness is non-tail, a B-witness for `y` may equal it or be a
different non-tail.  Hence the complete feasible orbit list is

```
(b0->x, x->y),   (b0->x, b1->y),
(b1->x, x->y),   (b1->x, b1->y),   (b1->x, b2->y).
```

The formerly emitted pair `(b0->x,b0->y)` is impossible because the template
already fixes `y->b0`.  The old three-variant scout consequently omitted three
genuine orbits and included one contradictory orbit.  The scout now emits the
five rows above and rejects old numeric-variant ledgers using an explicit schema
version.  This correction affects only the proposed compact hierarchy;
the direct parent CNFs did not normalize witnesses and are not invalidated by
it.

## Two useful exact reductions

For a selected robust deletion witness `w->u`, the selector clauses state that
every old exact second neighbor of `w` retains an alternate midpoint after
deleting `u`.  Thus the witness arc has no private second-neighbor loss.  Any
later split of such an arc by a positive loss count is empty.

If `x` is the source of the transitive `C` row and `w in B` witnesses deletion
of `x`, an alternate two-walk `w->k->x` cannot have midpoint in the root, `A`,
or `C`: neither the root nor `A` points into `C`, and `x` has no internal
`C`-predecessor.  Therefore every gain midpoint lies in `B`.  This removes the
root, `A`, and `C` gain blocks from the compact refinement.

## Persistence defects repaired in code

`m5_b6_parent_campaign.py` previously trusted any existing metadata filename,
returned success despite failed leaves, and checked only the temporary LRAT
rather than the compressed persisted object.  It now:

1. unconditionally checks the 4,355-row cover identity and payload hash;
2. parses and validates every pre-existing metadata record;
3. regenerates and hashes its CNF;
4. constrains the object name to the recorded raw-proof digest;
5. hashes, decompresses, and independently checks the persisted object; and
6. exits nonzero unless every index is newly verified or readback-verified.

The CNF refinement API now also rejects negative parent indices, malformed
three-state rows, out-of-range counters, and invalid gain coordinates instead
of silently emitting a different shard.

## Remaining gate

No hash-only ledger substitutes for the unavailable proof bytes (7,655,223,816
compressed bytes, approximately 7.66 GB).  The next
certificate route must either secure immutable storage for the complete direct
archive and perform this new full readback, or construct a corrected compact
cover using all five witness orbits.  A selector-batched CNF for the 4,332 easy
parents is the leading compression experiment; every batch must carry an
independently checked exact cover manifest.
