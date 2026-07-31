# Rank-five four-vertex kernels: exact tetrahedral sieve

## Scope and certified result

The 13 four-vertex rows in the exact rank-five kernel classification use edge
order

`01,02,03,12,13,23`.

For a kernel multiplicity row `m`, a physical row `q` records the number of odd
paths in each bundle, with `0<=q_e<=m_e`. Direct Cartesian enumeration gives
exactly 1281 physical rows. Quotienting only by genuine vertex automorphisms of
each kernel gives exactly 821 orbits.

The regular-tetrahedron four-color sieve at pentacyclic excess budget four
certifies 808 orbits and leaves 13 residual orbits:

| kernel | code | physical | automorphisms | orbits | certified | residual |
|---:|:---|---:|---:|---:|---:|---:|
| 4 | `(0,1,2,1,2,2)` | 108 | 2 | 63 | 62 | 1 |
| 5 | `(0,1,2,2,1,2)` | 108 | 2 | 63 | 62 | 1 |
| 6 | `(0,1,2,2,2,1)` | 108 | 1 | 108 | 107 | 1 |
| 7 | `(0,1,3,3,1,0)` | 64 | 4 | 30 | 29 | 1 |
| 8 | `(0,2,1,1,3,1)` | 96 | 1 | 96 | 95 | 1 |
| 9 | `(0,2,2,2,2,0)` | 81 | 8 | 21 | 20 | 1 |
| 10 | `(1,0,2,1,1,3)` | 96 | 1 | 96 | 95 | 1 |
| 11 | `(1,0,2,2,0,3)` | 72 | 2 | 48 | 47 | 1 |
| 12 | `(1,1,1,1,1,3)` | 128 | 4 | 56 | 55 | 1 |
| 13 | `(1,1,1,1,2,2)` | 144 | 2 | 84 | 83 | 1 |
| 14 | `(1,1,2,2,1,1)` | 144 | 8 | 39 | 38 | 1 |
| 15 | `(1,2,0,0,3,2)` | 72 | 1 | 72 | 71 | 1 |
| 16 | `(2,0,1,1,0,4)` | 60 | 2 | 45 | 44 | 1 |
| total | | 1281 | | 821 | 808 | 13 |

This is deliberately a sieve statement, not a theorem for all four-vertex
rank-five subdivisions. The 13 residual orbits below remain open in this
artifact, so its machine-readable status is `full_theorem=false` and
`theorem_status=residual_open`.

## Exact coarse certificate

Assign each branch vertex one of four unit vectors whose Gram matrix has
diagonal one and off-diagonal `-1/3`. This is the positive-semidefinite regular
tetrahedron Gram matrix. Equal-colored endpoints permit even paths at zero cost
but forbid odd paths. For unequal colors the verifier uses the rational bounds

| physical path | certified cost bound |
|:---|:---|
| first odd path in a bundle | `1/2` |
| each additional odd path | `<1/6` |
| each even path | `<3/5` |

The first odd path may have length one. Every additional odd path in the same
bundle has length at least three in a simple subdivision, and every even path
has length at least two. The exact regular-tetrahedron path costs satisfy the
displayed strict bounds; longer paths of the same parity only decrease cost.
The verifier sums the corresponding rational upper bound for every one of the
`4^4=256` labeled colorings and accepts an orbit only when its minimum is at
most four. Thus all 808 accepted rows have actual DNN excess strictly below
four whenever a strict term occurs, and at most four in all cases.

## Exact residual

The residual list contains one orbit per kernel:

| kernel | canonical physical row | minimum coarse upper bound |
|---:|:---|:---|
| 4 | `(0,1,1,1,1,1)` | `43/10` |
| 5 | `(0,1,1,1,1,1)` | `43/10` |
| 6 | `(0,1,1,1,1,1)` | `43/10` |
| 7 | `(0,1,1,1,1,0)` | `22/5` |
| 8 | `(0,1,1,1,1,1)` | `43/10` |
| 9 | `(0,1,1,1,1,0)` | `22/5` |
| 10 | `(1,0,1,1,1,1)` | `43/10` |
| 11 | `(1,0,1,1,0,1)` | `22/5` |
| 12 | `(1,1,1,1,1,1)` | `21/5` |
| 13 | `(1,1,1,1,1,1)` | `21/5` |
| 14 | `(1,1,1,1,1,1)` | `21/5` |
| 15 | `(1,1,0,0,1,1)` | `22/5` |
| 16 | `(1,0,1,1,0,1)` | `22/5` |

No residual is promoted through a numerical search, switching parity, or an
unstated structural argument.

## Fail-closed artifacts

Run:

```text
python3 research/rank-five-four-vertex-tetrahedral-sieve-verifier.py
python3 -O research/rank-five-four-vertex-tetrahedral-sieve-verifier.py
```

The verifier digest-locks the 118-kernel source classification, extracts the
13 four-vertex kernels, regenerates all physical rows and automorphism orbits,
checks that orbit sizes sum to 1281, recomputes all 821 exact coloring minima,
and compares the result byte-for-byte with
`research/fixtures/rank-five-four-vertex-tetrahedral-sieve.json`. Each orbit
record includes its canonical row, physical orbit size, exact rational upper
bound, first minimizing coloring, and certified status. Nine hostile mutations
must be rejected, including deletion of an orbit, a forged cost, loss of a
residual, and either attempted theorem promotion.
