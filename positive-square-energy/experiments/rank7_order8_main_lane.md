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

Use 5,000-row shards: 99 shards cover the stream, with a final 2,812-row shard.
Each worker should use a private fragment directory and the same read-only
census cache. For shard `I`:

```text
python3 rank7_order8_exact_rational.py \
  --output rank7_order8_chunk_${I}.r7o8g.xz \
  --fragment-directory rank7_order8_fragment_${I} \
  --census-cache rank7_order8_rational_search_cache.r7o8c.xz \
  --shard-index ${I} --shard-count 99 --shard-rows 5000
```

Audit every completed shard with `--verify-pack`. Preserve the fragment trees
until audit succeeds; restart uses the maximal gap-free 500-row prefix. Merge
only by validated record bodies in ascending shard order, exactly as fragment
merge does, then replay the final pack and record both raw and XZ SHA-256.

Template-derived warm starts should be introduced only behind an explicit
experimental option. They must fall through to the current seeded starts and
must pass a byte-identity benchmark on the first 5,000 rows before entering the
main lane.

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
