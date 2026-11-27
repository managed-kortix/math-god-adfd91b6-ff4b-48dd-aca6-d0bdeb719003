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

The verified result refutes the universal all-center DNN threshold and records
Atlas-through-7 evidence plus the `n=8` multiblock obstruction. It is not a
graph counterexample, graph-theorem closure, one-positive-rank-block theorem,
or lane-closure claim.
