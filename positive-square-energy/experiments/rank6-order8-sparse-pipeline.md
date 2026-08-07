# Order-eight rank-six sparse exact-Gram pipeline

## Design

Order eight has 325 kernels, 13 physical paths, and degree excess two.  Every
degree sequence is therefore either `5,3^7` or `4,4,3^6`.  The prototype
`rank6_order8_sparse_pipeline.py` uses this rigidity in four places:

1. it stores only nonzero support coordinates (at most 13), never dense
   28-coordinate rows;
2. it tests automorphisms only inside equal-degree classes, reducing the raw
   permutation search from `8!` to at most `7!` or `2!6!` per kernel;
3. it enumerates each mixed-radix parity orbit once with a compact byte-array
   visited set;
4. it replaces a row-by-coloring tetrahedral scan by one superset-min transform
   on support masks.

The exact run gives `1,598,512` physical parity rows and `1,045,292`
automorphism orbits.  The tetrahedral sieve closes `942,304` orbits and leaves
`102,988`; canonical plus 13 one-coordinate frontiers therefore gives
`1,441,832` targets before templates.  The signed-cycle recognizer removes 12
orbits (168 targets), leaving `1,441,664` numerical-search targets.  The census
finishes in about 14 seconds on the current host and emits a 96 KB summary,
rather than a residual/frontier JSON corpus.

For a support edge of multiplicity `m` containing `o>0` odd paths, a crossing
tetrahedral coloring contributes

```text
18m + 10 - 13o
```

in units of `1/30`; a noncrossing coloring is forbidden.  Give every crossing
support edge its baseline weight `18m`.  For every mandatory odd-support mask
`M`, a Boolean-lattice transform computes the minimum baseline weight of a
four-color crossing mask containing `M`.  The row cost is this cached value
plus `sum(10-13o)`.  Thus all rows with the same odd support share the expensive
part of the sieve.

## Certificate format

The search format is binary `R8G2`, then XZ compressed.  A chunk authenticates
the rank-six kernel source hash and records only its residual source range.
Rows, kernels, path lengths, costs, and 14 target keys are regenerated.

For a shared successful residual orbit the chunk stores:

```text
common denominator D
8 x 7 signed stereographic branch numerators
13 canonical path-interior numerator arrays
13 replacement (+2) path-interior numerator arrays
```

Integers use zig-zag varints.  Fractions use a shared denominator and therefore
need no JSON pairs, field names, repeated denominators, or stored costs.  One
branch realization and the 13 canonical paths serve all 14 targets.  The exact
auditor reconstructs rational unit vectors and every step cost with `Fraction`.
When no shared realization succeeds, an individual-mode record stores a
14-target success bitmap followed by one independently exact witness for each
successful target. The bitmap may be full because independently successful
witnesses need not share branch vectors. Null records and symbolic templates
remain explicit one-byte modes; template data is regenerated from the source.

The signed-five-cycle families `K744` and `K756` are recognized before search.
Their three singleton contractions and five mixed doubled bundles give exact
cost five for the canonical row and all 13 coordinate frontiers.  This is the
order-eight instance of the existing signed-cycle quotient lemma.

An independent dense census in `rank6_order8_orbit_frontier_census.py` agrees
on all five global counts.  Its ordered residual and frontier commitments are
respectively
`b451837e04a30e5b71eba5fe631841eee73bbb8f3722a0b6bd25b666ad4fe900`
and
`52439257eaa2b5a6bc2976f5c4199a5a06e3e3b6ab8afc61b2ad7c734876e97d`.

A 100-residual shared-witness smoke run closed all 1,400 targets exactly.  Its
uncompressed binary proof stream was 46,531 bytes and its XZ artifact was
26,412 bytes, about 264 bytes per residual orbit or 19 bytes per target.  This
is an early easy interval, not an estimate of the final unresolved rate.

## Run

Generate the exact census and a small summary JSON (the residual ledger itself
is deliberately not serialized):

```sh
python3 positive-square-energy/experiments/rank6_order8_sparse_pipeline.py \
  --output /tmp/rank6-order8-census-summary.json
```

Prototype a compact shared-witness search on a residual interval:

```sh
python3 positive-square-energy/experiments/rank6_order8_sparse_pipeline.py \
  --start 0 --search-count 100 --output /tmp/rank6-order8-00000.r8g.xz
python3 positive-square-energy/experiments/rank6_order8_sparse_pipeline.py \
  --verify-pack /tmp/rank6-order8-00000.r8g.xz
```

For checkpointed runs, use 2,000 residuals per chunk. On the current host this
keeps each serial process near 60 MB of witness state and limits lost work while
amortizing the roughly 14-second regenerated census. Run disjoint ranges in
parallel rather than increasing one chunk; `--restarts 1 --iterations 120`
with the default fallback and denominator settings is the economical first
pass. Retry only unresolved targets with stronger settings after exact audit.

The manifest/auditor accepts arbitrary chunk widths but requires their embedded
residual ranges to form the pinned ordered prefix `[0,N)` without gaps,
overlaps, or reordered packs. It locks both compressed and decompressed bytes,
derives the complete ordered target-key digest, exactly verifies every covered
witness, and compares all observed cost-five keys with the symbolic fixture.
Build or extend the manifest from the complete prefix, then audit it:

```sh
python3 positive-square-energy/experiments/rank6_order8_pack_auditor.py \
  --build-manifest positive-square-energy/experiments/rank6_order8_search_ckpt/*.r8g.xz
python3 positive-square-energy/experiments/rank6_order8_pack_auditor.py
```

The current manifest pins `[0,28000)`. Until the ordered prefix reaches all
102,988 residual rows and every target has an exact certificate, the auditor
prints `status=incomplete` in its JSON report and exits with status 1.

This is an experimental census/search format, not a theorem fixture. The
format supports per-target fallback records, but a full pipeline still needs a
completed search and exact classification of any final equality residuals.
