# Cycle 190: separate same-backend full-28-row replay of the `[1:5]` pair

## Exact result

An alternate GP producer recomputed all 28 base-level-433 rows for each of
`q=1499` and `q=29023`. It does not import either earlier 12-row table or any
earlier expected row value. For `E=433a1`, `p=7`, `ell=29`, and generator
`2 mod 29`, the exact results are

| `q` | full 28-row lift | paired 12-row lift | reduction mod 7 |
|---:|---:|---:|---:|
| 1499 | -150 | 365/2 | 4 (nonzero) |
| 29023 | -3108 | 77/2 | 0 |

Thus the separate computation agrees exactly with the prior reductions

\[
 c(1499,29)=4,\qquad c(29023,29)=0\pmod 7.
\]

It confirms the zero/nonzero modular-symbol comparison for the pair
`(29023,1499)`. This certificate separately checks the coordinate calculation,
but it uses the same PARI/GP modular-symbol backend and is not an independent
arithmetic backend. It does not add a new proof of the common full-`L_0`
conjugacy class or claim a BSD result.

## Alternate formula

For both primes `D_q=-q` and the minus base symbol is used. The producer first
computes every row

\[
 U_a(q)=\sum_{u=1}^{q-1}(u/q)
 \left[(aq+29u)/(29q)\right]^-_E,\qquad 1\le a\le28,
\]

then forms the unpaired integer-discrete-log lift

\[
 C_{28}(q)=\sum_{a=1}^{28}\log_2(a)U_a(q).
\]

Only after all 28 rows are complete does it separately derive the paired lift
with weights `(0,2,3,4,2,5,3,6,6,4,1,0,1,5)`. It verifies
`U_a=U_{29-a}` and equality of the two reductions modulo 7. The two rational
lifts need not be equal over `Q`: their differences are

| `q` | `C_28 - C_pair` | quotient by 7 |
|---:|---:|---:|
| 1499 | -665/2 | -95/2 |
| 29023 | -6293/2 | -899/2 |

All denominators are 1 or 2 and hence 7-adic units. The alternate PARI run returns
minimal changes `[1,125,1,63]` and `[1,2419,1,1210]`, so the differential
factor is `kappa_q=1`; the twist conductors are `433*q^2`.

## Reproduction

From the repository root run:

```sh
gp -fq -s 4G millennium-prize/birch-swinnerton-dyer/cycle190_independent_full28_base433.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle190_independent_full28.py
python3 -O millennium-prize/birch-swinnerton-dyer/verify_cycle190_independent_full28.py
sha256sum -c millennium-prize/birch-swinnerton-dyer/cycle190_SHA256SUMS
```

The GP run performs 56 separately generated exact character sums from the
level-433 symbol space. The Python verifier reconstructs discrete logarithms,
checks the complete row sets and pairing symmetry, computes both exact lifts,
and compares their reductions without PARI. Environment used: PARI/GP 2.15.4
and Python 3.
