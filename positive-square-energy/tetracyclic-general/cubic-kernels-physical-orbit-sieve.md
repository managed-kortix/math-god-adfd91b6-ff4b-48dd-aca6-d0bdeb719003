# Cubic kernels 13--15 and 17: exact physical orbit target

## Scope

This artifact freezes the complete finite physical-row frontier and the exact
equilateral three-color sieve for cubic rank-four kernels 13, 14, 15, and 17.
It is only a sieve statement: no claim beyond the 359 rows certified by the
sieve is made, and the 17 residual orbits remain explicit finite targets.

Rows use upper-triangle pair order

`01,02,03,04,05,12,13,14,15,23,24,25,34,35,45`.

For a bundle of multiplicity `m_uv`, its row coordinate `q_uv` is the number
of odd physical paths, so `0<=q_uv<=m_uv`. Canonicalization uses only genuine
vertex automorphisms preserving the full multiplicity vector. There is no
switching quotient.

## Exact census

| kernel | multiplicity vector | physical rows | automorphisms | orbits |
|---:|:---|---:|---:|---:|
| 13 | `(0,0,0,1,2,0,1,1,1,2,1,0,0,0,0)` | 288 | 4 | 102 |
| 14 | `(0,0,0,1,2,0,1,2,0,2,0,1,0,0,0)` | 216 | 6 | 56 |
| 15 | `(0,0,0,1,2,1,1,0,1,1,1,0,1,0,0)` | 384 | 4 | 144 |
| 17 | `(0,0,1,1,1,1,0,1,1,1,0,1,1,0,0)` | 512 | 12 | 74 |
| total | | 1400 | | 376 |

The fixture stores all 376 canonical representatives, each reconstructed
physical bundle ledger, and its complete labeled orbit. The sum of the stored
orbit sizes is 1400, independently recovering every physical row exactly once.

## Exact equilateral sieve

Assign one of three equilateral unit vectors to each of the six branch
vertices. Equal colors have correlation `1`; unequal colors have correlation
`-1/2`. A coloring is inadmissible when an odd path is monochromatic. For a
bichromatic bundle the exact worst physical cost is

| `(m,q)` | canonical lengths | cost |
|:---:|:---:|:---:|
| `(1,0)` | `(2)` | `2/3` |
| `(1,1)` | `(1)` | `1/3` |
| `(2,0)` | `(2,2)` | `4/3` |
| `(2,1)` | `(1,2)` | `1` |
| `(2,2)` | `(1,3)` | `1/3+a` |

Here `a=3 tan^2(pi/18)` is the unique root in `(93/1000,94/1000)` of

`a^3-27a^2+99a-9=0`.

The `(2,2)` row uses physical lengths `(1,3)`: two paths in one parallel
bundle cannot both be direct in a simple subdivision. The verifier compares
all costs exactly as `p+q*a`, using rational bisection of the isolated root.
For each canonical row it examines all `3^6=729` labeled colorings and records
the exact minimum and first minimizing coloring. The resulting partition is

`376 = 359 certified + 17 residual`.

The residual split by kernel is `5,6,5,1` for kernels 13, 14, 15, and 17,
respectively. This is the complete output of the equilateral sieve and is not
a theorem closing those residuals.

## Fail-closed artifacts

Run

```text
python research/rank-four-cubic-kernels-three-color-verifier.py
python -O research/rank-four-cubic-kernels-three-color-verifier.py
```

The verifier independently regenerates all physical rows, all genuine
automorphism groups, all orbit members, and every exact coloring minimum. It
uses explicit exceptions rather than `assert`, requires byte-identical normal
and optimized output, and rejects 11 hostile mutations covering deletion,
duplication, noncanonical rows, altered bundles or orbit members, changed exact
costs or witnesses, residual loss, algebraic data, pair order, and digest
policy.

The canonical fixture is

`research/fixtures/rank-four-cubic-kernels-three-color-sieve.json`

with SHA-256 digest

`531dfd4fc75703e01a57e5c030a374d7e563a566679d0b1618c5e4c9837997ed`.
