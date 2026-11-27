# Exact `c=5,(C5,C5)` DNN candidate-evidence bundle

This is a read-only research handoff integrated as candidate computational
evidence. Start with `CANDIDATE-NOTE.md`.

Run:

```bash
python3 scripts/verify-certificates.py
python3 -O scripts/verify-certificates.py
cmp output/verify.normal.txt output/verify.optimized.txt
python3 scripts/test-hostile-mutations.py
```

`SHA256SUMS` is a strict closed lock over every bundled file except itself; the
verifier rejects missing, extra, duplicate, unsafe, changed, or self-referential
members. The Atlas-through-order-seven conclusion is conditional on the
standard Graph Atlas source being exhaustive through order seven.

## Vendored source provenance and license

`sources/networkx-3.7-atlas.dat.gz` is byte-identical to
`networkx/generators/atlas.dat.gz` in the pinned PyPI wheel
`networkx-3.7-py3-none-any.whl` (wheel SHA-256
`e3fd2c13a7814cee3746340d8d7f8598a67f16a58bf47fb7f8793fab6efca1b0`;
vendored member SHA-256
`73fc416df0164923607751cb759f4ae81deb5f6550bf25be59c86de3b747e41d`).
`THIRD-PARTY-NETWORKX-3.7-LICENSE.txt` is the byte-identical wheel member
`networkx-3.7.dist-info/licenses/LICENSE.txt` (SHA-256
`6025f323ea29dc2f0ee0abd9523bf910186f55b0e148e6ebf646c55566278e2e`).
That BSD-3-Clause text covers the redistributed NetworkX package bytes. The
graph collection is separately identified by NetworkX as Read-Wilson Graph
Atlas data. This bundle makes no additional claim about rights in the
underlying graph compilation.

The verified result refutes the universal all-center DNN threshold and records
Atlas-through-7 evidence plus the `n=8` multiblock obstruction. It is not a
graph counterexample, graph-theorem closure, one-positive-rank-block theorem,
or lane-closure claim.
