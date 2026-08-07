# Order-nine rank-six sparse witness generator

`rank6_order9_sparse_witness.py` specializes the order-eight `R8G2` pipeline
to the exact order-nine frontier. It regenerates the 186,295 residual orbits
from the locked kernel fixture instead of storing their rows.

The XZ-compressed binary format uses magic `R9G1` and authenticates the source
fixture hash. Each residual has one of four modes: unresolved, shared exact
witness, payload-free K971 signed-five-cycle template, or a 15-bit individual
fallback map followed by exact per-target witnesses. Signed stereographic
numerators use zig-zag varints and one denominator per witness. Kernels, parity
rows, target keys, path lengths, and costs are reconstructed by the verifier.

The K971 template is recognized only for singleton forest
`07,16,25,34`, doubled quotient cycle `08,18,27,36,45`, and one odd path in
each doubled bundle. The verifier rebuilds its rational Gram, audits every
principal minor, and checks exact cost five for all 15 targets.

Generate and exactly verify a bounded chunk:

```sh
python3 positive-square-energy/experiments/rank6_order9_sparse_witness.py \
  --start 0 --search-count 1000 --restarts 1 --iterations 120 \
  --fallback-restarts 1 --fallback-iterations 180 \
  --output /tmp/rank6-order9-smoke-0000.r9g.xz
python3 positive-square-energy/experiments/rank6_order9_sparse_witness.py \
  --verify-pack /tmp/rank6-order9-smoke-0000.r9g.xz
```

This remains an experimental finite frontier. A partial chunk, even when every
target in it verifies exactly, does not establish the full theorem.

## 1000-residual smoke

On the current host, the bounded command above closes all 15,000 targets: 990
residuals use shared witnesses and the first 10 use K971 templates. There are no
individual fallbacks or unresolved targets in this interval. The proof stream
is 552,024 bytes raw and 328,368 bytes after XZ (about 328 bytes per residual,
or 21.9 bytes per target), with compressed SHA-256
`e57d12d5591e8566693c2ca99d70f9dc94394cbcf348edf18e7df751d9ca9c2b`.

The full generation command takes 106.4 seconds, including 67.7 seconds to
regenerate and authenticate the complete sparse census. A fresh exact verifier
run takes 89.4 seconds (73.4 seconds under `python3 -O`); assertions are not
used for acceptance. A synthetic all-15-target individual record also survives
binary round-trip and exact audit, while bad magic, truncation, and trailing
bytes are rejected.
