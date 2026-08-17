# Rank-seven/order-eight main lane

The witness engine consumes the authenticated 492,812-row rational-search
stream and preserves the existing `R7O8G1` binary format. Numerical results are
still proposals only; each checkpoint and merged pack receives exact
`Fraction` replay.

## Deterministic acceleration

- `--census-cache PATH` writes or reads a source-pinned canonical binary/XZ
  cache. The header authenticates the residual manifest plus selected-index
  digest. Cache records retain stream order, source indices, supports,
  multiplicities, parity rows, and orbit sizes.
- Objective and gradient evaluation memoize each `(u,v)` correlation within an
  evaluation. Parallel paths in the same bundle therefore share their dot
  product. Summation and gradient update order remain
  path order, so optimizer trajectories and output bytes do not change.
- `mine-templates` emits a canonical JSON inventory of deterministic signed
  degree/edge signatures. It is an analysis lane only and cannot alter witness
  selection or pack encoding.
- `--shard-index I --shard-count N --shard-rows R` expands to the existing
  half-open `--start/--count` selection. The engine requires
  `N=ceil(492812/R)`, preventing gaps and superfluous shards.

## First 5,000 rows

The committed baseline pack contains 5,000 shared exact witnesses, all at
denominator 256, with no fallback or unresolved target. Its artifact SHA-256 is
`2f3773dc99c930f9aeacff1e3566e037eb6d7d106d866e81a829c1b53797a2ee`.
The profile identifies numerical descent as the search hot path and exact replay
as the audit hot path. Mining finds 1,262 structural signatures; 4,547 rows
belong to a signature occurring more than once, with maximum multiplicity 56.
These are warm-start candidates, not interchangeable certificates: the 5,000
exact payloads and endpoint branches are all distinct.

## Completion plan

Use durable 1,000-row scheduler shards, each retaining two 500-row exact
checkpoint fragments. Workers use private fragment directories and the same
authenticated read-only census cache. Atomic per-range locks prevent duplicate
active work; stale locks are reclaimed, completed result manifests are skipped,
and interrupted ranges resume from their maximal gap-free fragment prefix.
Launch the immediate four-shard range with:

```text
python3 positive-square-energy/experiments/rank7_order8_scheduler.py launch \
  --start 5000 --stop 9000 --shard-rows 1000
```

The scheduler builds the cache once if absent, adopts compatible fragments from
the interrupted 5,000-row job, runs `--verify-pack` after every merge, and only
then writes a completed result containing the XZ SHA-256. Logs, PID records,
state, results, output packs, and fragment trees persist under the experiment
directory. Reissuing the launch command is safe. Merge larger intervals only by
validated record bodies in ascending shard order, exactly as fragment merge
does, then replay the final pack and record both raw and XZ SHA-256.

Template-derived warm starts should be introduced only behind an explicit
experimental option. Cache misses must fall through to the current seeded
starts, and exact replay must remain mandatory before entering the main lane.

## Refined-signature warm-start experiment

`build-warm-cache` deterministically selects the first solved row for each
refined incidence signature in an exactly replayed source pack. It stores only
the branch Gram as canonical hexadecimal binary64 values; Cholesky
factorization supplies a numerical optimizer start. The search still
rationalizes the resulting vectors and replays every stored witness exactly.
Cache misses retain the original seeded starts, and cache hits replace one
random restart rather than increasing the amount of descent work.

On held-out rows 5,000--9,999, the first-5,000 cache contained 2,177 signatures
and hit 2,762 rows. Both baseline and warm runs produced 5,000 shared exact
witnesses with no fallback or unresolved target. Search elapsed time changed
from 432.453256 seconds to 424.738455 seconds, a 1.78% improvement; wall time
changed from 436.310 seconds to 428.457 seconds, a 1.80% improvement. The output
packs differ because the numerical proposals differ, but both pass exact
`Fraction` replay. This is not a substantial gain, so the cache remains an
explicit experiment and is not enabled or committed for main-lane shards.

```text
python3 rank7_order8_exact_rational.py build-warm-cache \
  --source-pack rank7_order8_chunk_000000_005000.r7o8g.xz \
  --output rank7_order8_warm_cache.json.xz
python3 rank7_order8_exact_rational.py \
  --warm-start-cache rank7_order8_warm_cache.json.xz \
  --start 5000 --count 5000 --output heldout.r7o8g.xz
```

## Exact finite-library experiment

`rank7_order8_exact_gram_library.py` authenticates and exactly replays the
first-5,000 pack, mines rational branch Grams together with their complete
canonical and length-plus-two waypoint formulas, and builds support/parity
keys modulo vertex relabeling.  The full 492,812-row rational-search stream is
then recognized without floating point.

The mined sample has 1,262 signed-degree signatures, 2,177 refined incidence
signatures, and 50,932 exact structural orientations.  Their signatures occur
on 166,072, 66,416, and 5,000 rows respectively.  Exact structural matching
certifies only the 5,000 source rows: all 5,000 witness formulas are distinct,
and none transfers to a second row.  Thus the sample supports useful warm-start
classes but not a reusable certificate library covering a majority.  The exact
coverage is 5,000 rows and 75,000 targets, leaving 487,812 rows and 7,317,180
targets.

```text
python3 positive-square-energy/experiments/rank7_order8_exact_gram_library.py
python3 positive-square-energy/experiments/rank7_order8_exact_gram_library.py \
  --audit positive-square-energy/experiments/rank7_order8_exact_gram_library_coverage.json
```

The committed report reproduces byte-for-byte with SHA-256
`32a54cf46be560a260bb7b65b53cd6d042390e7f8dec062a894c3b19e32bd094`.

## Typed-diagonal theorem-owner verification

The typed-diagonal search report owns 402,712 of the 492,812 rational-search
rows, but rerunning its monolithic `--audit` couples theorem verification to one
long process. `rank7_order8_typed_diagonal_segmented_verifier.py` separates
that obligation into independently replayable half-open segments. It does not
trust the search lane's acceptance bit: for every row it reconstructs
`X=D0+D1*S` with `Fraction`, checks the exact nonnegative diagonal completion of
`XX^T/M`, recomputes the canonical cost and all fourteen length-plus-two costs,
and emits a canonical receipt with an ownership bitmap and coverage digest.

The resumable full command writes 25,000-row receipts, reuses compatible
completed receipts, and merges them only after exact validation:

```text
mkdir -p positive-square-energy/experiments/rank7_order8_typed_diagonal_receipts
python3 positive-square-energy/experiments/rank7_order8_typed_diagonal_segmented_verifier.py \
  verify-all --workers 8
```

Each receipt can also be rerun in isolation with `audit-receipt`. The `merge`
command rejects gaps, overlaps, changed source endpoints, malformed bitmap
padding, altered exact-check totals, and any owner total other than the
committed 402,712-row scan. Its coverage digest is recomputed from every
`(stream index, source index, owner bit)` tuple rather than accepted from a
receipt.

The resulting `rank7_order8_combined_owner_accounting.json` applies the
disjoint precedence `payload-free` then `typed-diagonal-rational-gram`: 605 plus
402,712 owners leave exactly 90,100 of 493,417 coarse rows, or 1,351,500 of
7,401,255 frontier targets, for later lanes. This is an owner theorem for the
accepted rows, not a full order-eight theorem.

```text
python3 positive-square-energy/experiments/rank7_order8_typed_diagonal_segmented_verifier.py \
  merge positive-square-energy/experiments/rank7_order8_typed_diagonal_receipts/receipt-*.json
```
