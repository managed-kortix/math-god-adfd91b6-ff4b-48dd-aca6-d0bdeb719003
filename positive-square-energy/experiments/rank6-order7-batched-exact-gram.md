# Order-seven rank-six batched exact Gram frontier

## Result

The batched generator covers the complete finite frontier of 319,202 targets.
It supplies 319,163 independently checked exact rational DNN certificates and
leaves 39 equality-frontier targets outside its stereographic witness format.
Those 39 targets are now closed by the exact templates and fail-closed verifier
in `rank6-order7-equality-frontier-closure.md`. The batched artifact itself
remains unchanged and continues to report its original 39 null witnesses.

The 39 residuals are three frontiers on each of 13 source rows. They occur on
kernels 469, 511, 534, and 548. In each case the optimum is exactly five at the
canonical target and two coordinate frontiers. Numerical values are not
accepted as certificates; the separate closure reconstructs rational PSD Gram
matrices and exact costs.

## Batched representation

For one residual row, one optimized branch realization is tested against the
canonical ledger and all twelve coordinate lengthenings. The seven rational
branch parameters and twelve canonical path interiors are stored once. Each
coordinate frontier stores only its replacement extended path interior. The
verifier reconstructs all 13 targets independently with `Fraction` and checks
that every accepted total is at most five.

Compared on the first 1,000 residual rows (13,000 targets):

| generator | wall seconds | output bytes | exact targets |
|:--|--:|--:|--:|
| legacy per-target JSON | 56.64 | 16,694,618 | 13,000 |
| batched, 16 workers | 35.79 | 6,023,278 | 13,000 |

The generator phase reported 27.426802 seconds; the remaining batched wall time
was canonical serialization and exact self-verification. The batched artifact
is 2.77 times smaller and the end-to-end run is 1.58 times faster. Generation
alone runs at 474.0 targets/second on this host.

## Durable chunks

The six committed XZ artifacts contain all 24,554 source rows in contiguous,
nonoverlapping ranges. They are deterministic XZ (`preset=6`) encodings of the
canonical JSON chunks. Their total stored size is 45,176,376 bytes, versus
144,432,072 bytes after decompression.

| source range | exact / targets | stored bytes | XZ SHA-256 | JSON SHA-256 |
|:--|--:|--:|:--|:--|
| 00000--03999 | 52,000 / 52,000 | 7,389,700 | `7973e5e36baf73814b542301cd2da4674bf1bc66bc4cacd796dfcf18c05415e8` | `3731079c31db0dd8613836ca69e4e21bcd6533f876964492d38d4d773ec7ecf0` |
| 04000--07999 | 52,000 / 52,000 | 7,453,436 | `7af9efd2a8fe37e787540ad25dcab19ecea2f0a1b917b860eb1d0dc3401f493e` | `4f1746f60bb1d6e32daf77371f0790d0f711e3c98c79dc04f079f094aee7a75c` |
| 08000--11999 | 51,988 / 52,000 | 7,352,544 | `c66e94e4443bff1aa67d6576c42a8338703e1d1d23d1b70d25d23e4cc056da8d` | `0d9425d33fe780d305ab3c0ff22873285861b4196157cbd080c843f6dd8d02a3` |
| 12000--15999 | 51,982 / 52,000 | 7,297,724 | `1ea2e870017d62c8b53a00d9264182aca0a2081c85396f629abc5777d033a51a` | `e4b1a2cc5e235a3eed356090703525a986548af2ba26c2f62a1d972269f955bd` |
| 16000--19999 | 51,991 / 52,000 | 7,293,660 | `714efdc1d5a4105c4034e587b8dabcce235323987f69590edd90d88d9e91160c` | `b2e8d70e14ac7fb8f8430c6af7c949e1cb7a0c6a11c3f18f44c8813257a059d4` |
| 20000--24553 | 59,202 / 59,202 | 8,389,312 | `c15c4488106b036f2a846df4df3bd2804785e2054670323cd711470990019469` | `491afa09d32f772e74bafc8b498544b3894411cdd74097b7229830602f03c318` |

The ordered digest manifest SHA-256 is
`5a3693a15beb0a6c37089c5fe15f78eaf76875dcd3096b98a2fc3dbf0f339324`.
This commits to the six decompressed canonical JSON digests in source-range
order. The corresponding ordered compressed-artifact manifest SHA-256 is
`836ce3a25de9a3f3dd2f83bc5cdfe340b022bc72a73bf7a169a4d7cdd872cca7`.

## Reproduction

No Kortix roots or subagents are launched. The generator uses local Python
worker processes only.

```sh
python3 positive-square-energy/experiments/rank6_order7_batched_exact_gram.py \
  --audit positive-square-energy/experiments/rank6_order7_batched_chunks/*.json.xz
```

The full exact audit reports:

```text
chunks=6 records=24554 targets=319202 exact=319163 unresolved=39
complete_frontier=true manifest_sha256=5a3693a15beb0a6c37089c5fe15f78eaf76875dcd3096b98a2fc3dbf0f339324
artifact_manifest_sha256=836ce3a25de9a3f3dd2f83bc5cdfe340b022bc72a73bf7a169a4d7cdd872cca7
```

The audit took 197.31 wall seconds on this host. `complete_frontier=true` means
that every finite target key is present; it does not promote the unresolved 39
targets or claim the theorem.

The verifier uses only the Python standard library. It pins each compressed
byte stream before XZ decoding, pins each decompressed canonical JSON stream,
reconstructs every accepted rational witness with `Fraction`, rejects duplicate
or shifted source indices, and requires the exact full source-index universe.
