# Structural cycle-Gram I–III snapshot gate

Scope: committed snapshot `cd74bca89019f92b08a7d9ba4ab494ed7794fa7a` only.
No producer is imported or executed; every input is opened read-only. Eleven
SHA-256 roots pin the ledger, three reports and seven compressed streams.
All eleven pins were compared against the supplied git bundle at that commit.

Run from repository root:

```
python -B positive-square-energy/experiments/rank7_order8_structural_exact_verifier.py
python -O -B positive-square-energy/experiments/rank7_order8_structural_exact_verifier.py
python -B positive-square-energy/experiments/tests/test_rank7_order8_structural_exact_verifier.py
python -O -B positive-square-energy/experiments/tests/test_rank7_order8_structural_exact_verifier.py
```

The two replay outputs are byte-identical; the two hostile-test outputs are
byte-identical. Hostile test count: 20. No proof-critical `assert` is used.
Tests deliberately bypass immutable hashes to attack semantic validation.

Acceptance arithmetic is exclusively integers and `Fraction`. Decimal JSON
hints are parsed without binary floating-point and never affect acceptance.
JSON rows have unique object keys, canonical encoding and strict schemas.
Pinned reports have strict duplicate-key parsing but are not reserialized for
canonical comparison: their denominator-count object keys were serialized in
integer order by the producer, not in lexicographic order after JSON decoding.
Their exact original bytes are authenticated by independent literal hashes.

The verifier checks all 245 owners and 3675 costs, reconstructs the incidence,
projector and Gram decomposition, and compares ordered byte complements for
83856 → 83744 → 83647 → 83611. Certificate indices must equal `source_index`
(row field 1), not `stream_index` (row field 0).

For any integer k ≥ 0, a path numerator q ≥ 0 gives the symbolic identity
q/L − q/(L+2k) = 2kq/[L(L+2k)] ≥ 0. The code checks the exact k=1 identity
and every coordinate frontier; iteration proves the full same-parity lift.

**Dependency boundary:** rooted-tree lifting uses the external mathematical
DNN one-vertex-additivity lemma. This verifier checks the exact report contract
and verifies the unit-diagonal PSD branch Gram which is that lemma's input.
It does not purport to formally prove the external spectral/DNN lemma, nor
prove or promote the order-eight theorem, authenticate the upstream census,
or reproduce numerical optimizer classification of unowned candidates.
