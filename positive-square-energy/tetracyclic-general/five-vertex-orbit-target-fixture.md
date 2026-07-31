# Five-vertex rank-four target fixture

This artifact freezes the finite physical-row frontier for suppressed kernels
9--12. It is bookkeeping for subsequent exact work, not a theorem and not a
numerical DNN certificate.

## Exact universe

Rows use upper-triangle pair order

`01,02,03,04,12,13,14,23,24,34`.

An entry `q_uv` is the number of odd paths in physical bundle `uv`; hence
`0 <= q_uv <= m_uv`. The four canonical kernel multiplicity vectors are

| kernel | multiplicities | physical rows | automorphisms | orbits |
|---:|:---|---:|---:|---:|
| 9 | `(0,0,1,2,1,0,2,2,0,0)` | 108 | 2 | 63 |
| 10 | `(0,0,1,2,1,1,1,1,1,0)` | 192 | 2 | 120 |
| 11 | `(0,0,1,2,1,1,1,2,0,0)` | 144 | 1 | 144 |
| 12 | `(0,1,1,1,1,1,1,0,1,1)` | 256 | 8 | 51 |
| total | | 700 | | 378 |

Canonicalization uses only genuine vertex automorphisms preserving the complete
kernel multiplicity vector. There is no switching quotient. In particular,
the fixture keeps physical odd/even bundle counts and does not pretend that a
switch changes canonical path lengths.

## Fixture partition

`research/fixtures/rank-four-five-vertex-orbits.json` stores all 378 canonical
orbit representatives. Every record includes:

- the kernel number and ten-entry canonical row;
- each nonzero physical bundle's multiplicity and odd/even counts;
- the complete labeled row orbit under the kernel automorphism group.

The target partition is exactly

`378 = 282 incidence-certificate records + 96 explicit residual records`.

The residual section is the exact complement of the 282 keys, not a count-only
placeholder. The words "incidence certificate" here certify finite incidence
membership and bundle reconstruction only. The artifact contains no floating
point values, SDP output, Gram-cost bound, PSD claim, or spectral conclusion.

## Fail-closed verifier

Run

```text
python research/rank-four-five-vertex-orbit-verifier.py
python -O research/rank-four-five-vertex-orbit-verifier.py
```

The verifier independently regenerates all 700 physical rows, all four exact
automorphism groups, and all 378 canonical representatives. It reconstructs
the physical bundles and labeled automorphism orbit for every one of the 282
certificate records and every one of the 96 residuals, checks that they form a
disjoint exhaustive partition, and freezes the canonical JSON digest.

The normal invocation also runs the verifier under `python -O` and requires
byte-identical output. Nine hostile checks reject deletion, duplication,
noncanonical rows, changed bundle counts, lost orbit members, certificate
promotion, injected numerical claims, changed pair order, and digest mutation.
All acceptance gates use explicit exceptions rather than `assert`.

This fixture creates the exact target for later proof artifacts. It does not
promote any of the 282 incidence rows to an analytic certificate and does not
claim that any of the 96 residual rows fails the desired inequality.

## Exact three-color extension

The subsequent exact coarse sieve is recorded in
`five-vertex-three-color-dnn-sieve.md` and
`research/fixtures/rank-four-five-vertex-three-color-sieve.json`. It preserves
this 96-key target verbatim, adds exact physical bundle costs and minimizing
colorings for all 378 orbits, and computes a 370/8 sieve partition. Its eight
residuals intersect this fixture's 96 targets in exactly two kernel-11 rows.
