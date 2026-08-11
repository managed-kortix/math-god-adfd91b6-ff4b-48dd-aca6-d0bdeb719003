# R10 exact chunk replay plan

This plan is scoped to exact R10 chunk replay checkpoints. It makes no theorem
claim. Checkpoints authenticate the selected manifest, current auditor,
transitive dependencies, chunk bytes, key stream, ownership stream, and exact
report; they are not substitutes for a fresh exact replay.

## Pinned executable

- auditor: `positive-square-energy/experiments/rank6_order10_pack_auditor.py`
- auditor SHA-256: `c6047843a29b9d6755855d165f9b4dac1ede39c8f1002a5fffa97ca663303d8e`
- promotion-owner pin: the same digest in
  `research/rank-six-order-ten-kernel-theorem-verifier.py`

## Current generation

The current manifest is
`positive-square-energy/experiments/rank6_order10_search_manifest.json`, with
SHA-256 `c75825324beb6d7e7b110a59c1ec9776d0b99522de24b9d6c93a177adf54b5a8`,
coverage `[0,110000)`, and 19 chunks. One authenticated transcript per chunk is
stored in this directory, and `aggregate.json` authenticates the complete set.
Its SHA-256 is
`86f7b2faf3dfebf86ff0a2292760fcea237f72a59dbc813796c6f0a51cc1cfd0`.

The exact replay command for each row is:

```sh
python3 positive-square-energy/experiments/rank6_order10_pack_auditor.py \
  --manifest positive-square-energy/experiments/rank6_order10_search_manifest.json \
  --chunk-index INDEX \
  --write-chunk-transcript positive-square-energy/experiments/rank6_order10_chunk_replays/chunk-START-STOP.json
```

| index | residual range | receipt |
|---:|:---:|:---|
| 0 | `[0,10000)` | `chunk-00000-10000.json` |
| 1 | `[10000,20000)` | `chunk-10000-20000.json` |
| 2 | `[20000,30000)` | `chunk-20000-30000.json` |
| 3 | `[30000,35000)` | `chunk-30000-35000.json` |
| 4 | `[35000,40000)` | `chunk-35000-40000.json` |
| 5 | `[40000,45000)` | `chunk-40000-45000.json` |
| 6 | `[45000,50000)` | `chunk-45000-50000.json` |
| 7 | `[50000,55000)` | `chunk-50000-55000.json` |
| 8 | `[55000,60000)` | `chunk-55000-60000.json` |
| 9 | `[60000,65000)` | `chunk-60000-65000.json` |
| 10 | `[65000,70000)` | `chunk-65000-70000.json` |
| 11 | `[70000,75000)` | `chunk-70000-75000.json` |
| 12 | `[75000,80000)` | `chunk-75000-80000.json` |
| 13 | `[80000,85000)` | `chunk-80000-85000.json` |
| 14 | `[85000,90000)` | `chunk-85000-90000.json` |
| 15 | `[90000,95000)` | `chunk-90000-95000.json` |
| 16 | `[95000,100000)` | `chunk-95000-100000.json` |
| 17 | `[100000,105000)` | `chunk-100000-105000.json` |
| 18 | `[105000,110000)` | `chunk-105000-110000.json` |

Authenticate and index exactly this generation with:

```sh
python3 positive-square-energy/experiments/rank6_order10_pack_auditor.py \
  --manifest positive-square-energy/experiments/rank6_order10_search_manifest.json \
  --aggregate-transcripts \
  positive-square-energy/experiments/rank6_order10_chunk_replays/chunk-*.json \
  --write-aggregate positive-square-energy/experiments/rank6_order10_chunk_replays/aggregate.json
```

## Final generation

Four final packs are in progress. Their expected final-manifest rows are:

| index | residual range | receipt |
|---:|:---:|:---|
| 19 | `[110000,113865)` | `final/chunk-110000-113865.json` |
| 20 | `[113865,117726)` | `final/chunk-113865-117726.json` |
| 21 | `[117726,121582)` | `final/chunk-117726-121582.json` |
| 22 | `[121582,125457)` | `final/chunk-121582-125457.json` |

After all four final XZ packs exist, rebuild and digest-audit the final manifest:

```sh
python3 positive-square-energy/experiments/rank6_orders9_10_main_lane.py \
  --order 10 > /tmp/r10-final-replay-plan.json
```

Require the generated report to show coverage `[0,125457)`, no missing
intervals, and 23 chunks. The final manifest changes the manifest SHA-256 and
therefore invalidates every current-generation transcript. Preserve the
current files as historical execution evidence, create
`rank6_order10_chunk_replays/final/`, and replay all indices 0 through 22 with
the command above, changing the output to the corresponding `final/` receipt.
The first 19 final receipt names retain the current range names; the four rows
in the table supply the remaining names.

Authenticate all final receipts and write the final aggregate with:

```sh
python3 positive-square-energy/experiments/rank6_order10_pack_auditor.py \
  --manifest positive-square-energy/experiments/rank6_order10_search_manifest.json \
  --aggregate-transcripts \
  positive-square-energy/experiments/rank6_order10_chunk_replays/final/chunk-*.json \
  --write-aggregate positive-square-energy/experiments/rank6_order10_chunk_replays/final/aggregate.json
```

The final aggregate must authenticate 23 distinct indices, coverage
`[0,125457)`, and 2,007,312 targets. The theorem-facing mandatory replay remains
separate and must run both modes after final aggregation:

```sh
python3 research/rank-six-order-ten-kernel-theorem-verifier.py --full
python3 -O research/rank-six-order-ten-kernel-theorem-verifier.py --full
```
