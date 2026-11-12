# Rank-seven/order-nine marked-deletion map: exact scope audit

This note audits the topology/provenance mapper in
`research/rank-seven-order-nine-marked-deletion-mapper.py`. It is an exact
finite combinatorial artifact, **not** a spectral owner or theorem.

## Authenticated inputs

The mapper digest-locks and replays:

- the 1,615-row post-three-stream, post-induced-rank-partition obstruction
  frontier through `rank-seven-order-nine-favorable-cycle-residual-miner.py`;
- the durable 80 finite favorable-cycle residual targets;
- the complete canonical rank-six kernel fixture for orders 2 through 10.

Every selected physical path is identified by its zero-based path index and
`[support_index, occurrence_within_support]`. The graph is expanded into
ordinary physical edges before deletion. Connectivity, cyclomatic rank, and
edge-biconnected blocks are then recomputed from that expanded graph.

## What is proved by the artifacts

The 82-case pilot contains the 80 durable finite misses and the hostile source
`78714` descendant with increments on occurrences 1 and 13, deleting each of
those occurrences in turn. All 82 deletions are connected single rank-six
blocks. Each is mapped to exactly one rank-six fixture kernel; the artifact
records a deterministic full vertex isomorphism, every oriented surviving
physical chain, the two deleted-endpoint provenance tuples, a finite target
selection, and an explicit marked descendant lift using odd runs of identical
transformed vectors. Suppressed marks must map to distinct selected-target
coordinates; otherwise mapping fails closed.

The full-schema replay covers all `1,615 * 15 = 24,225` coordinate-deletion
cases. It finds 18,353 single rank-six blocks and 5,872 multiblock cases. The
multiblock cases are only topology records and are not sent to a single-block
fixture owner. Their positive-rank profiles are:

- rank 5 + rank 1: 4,223;
- rank 4 + rank 2: 630;
- rank 4 + rank 1 + rank 1: 575;
- rank 3 + rank 3: 444.

The 18,353 single-block maps have fixture orders 7 (7,909 cases), 8 (8,961),
and 9 (1,483). The committed full artifact is summary-only; the mapper can
regenerate all transient records deterministically without committing a
163 MB JSON file.

## Claim boundary

**Rank-six owner payload import is not attempted.** In particular, these
artifacts do not:

- retrieve or authenticate rational, coarse, symbolic, or structural owners;
- compute exact owner excess `E` or marked correlation `r`;
- decide `E + f_q(r) <= 6`;
- turn structural theorem tags into Gram data;
- glue multiblock Gram owners;
- infer an all-length or spectral conclusion.

The recorded descendant lift is only an exact index/provenance construction.
It states how a selected transformed-chain vector can be repeated in odd runs
so inserted steps have dot product one and zero cost. It does not assert that
the as-yet-unimported selected finite owner exists or passes the marked
restoration inequality.

## Reproduction

From repository root:

```bash
python3 research/rank-seven-order-nine-marked-deletion-mapper.py --audit
python3 research/rank-seven-order-nine-marked-deletion-mapper.py \
  --scope full --audit \
  --output research/rank-seven-order-nine-marked-deletion-full-summary.json
python3 -O research/rank-seven-order-nine-marked-deletion-mapper.py --audit
python3 -O research/rank-seven-order-nine-marked-deletion-mapper.py \
  --scope full --audit \
  --output research/rank-seven-order-nine-marked-deletion-full-summary.json
pytest -q research/test_rank_seven_order_nine_marked_deletion_mapper.py
```

Committed artifact SHA-256 values:

- pilot map: `6c90f9a55034c4e22d1003a9c6c0f1f1e5603265c63b712b7a80077984e0259d`;
- full summary: `bb82cc5b477c9e5340c41028bc08f6b4196d2b93dc77998c6e419bcfea9d374a`.
