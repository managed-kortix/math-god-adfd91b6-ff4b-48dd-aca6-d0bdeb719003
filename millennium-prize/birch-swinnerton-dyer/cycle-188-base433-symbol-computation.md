# Cycle 188: exact base-level-433 computation at two twist primes

## Result

For `E=433a1: y^2+xy=x^3+1`, `p=7`, `ell=29`, and primitive root
`eta=2 mod 29`, the Cycle 187 base-symbol identity gives

| `q` | `D_q` | base parity | completed rational sum | `c_2(q,29)` |
|---:|---:|:---:|---:|---:|
| 3823 | -3823 | minus | -90 | 1 (nonzero) |
| 8317 | 8317 | plus | -1413/2 | 4 (nonzero) |

Thus the requested zero/nonzero classification is **nonzero for both primes**.

## Independently implemented formula

Write `epsilon_q=(-1/q)` as `+1` for `q=1 mod 4` and `-1` for
`q=3 mod 4`, and let `[r]_E^epsilon` denote the corresponding PARI plus or
minus symbol. With the endpoint path `[infinity,r]`, define

\[
 U_a(q)=\sum_{u=1}^{q-1}(u/q)
 \left[(aq+29u)/(29q)\right]_E^{\epsilon_q}.
\]

The twist identity, using the additive character `exp(2*pi*i*u/q)`, is

\[
 [a/29]^+_{E^{(D_q)}}=\kappa_q U_a(q).
\]

Pairing `a` with `29-a` and reducing the doubled discrete logarithms modulo 7
gives

\[
 c_2(q,29)=\overline{\kappa_q\sum_{a=1}^{14}w_aU_a(q)},
\]

where `(w_1,...,w_14)=(0,2,3,4,2,5,3,6,6,4,1,0,1,5)`. The zero-weight
rows `a=1,12` are not evaluated. This uses only the fixed level-433 symbol
space returned by `msfromell(E,+/-1)`; no level `433*q^2` space is built.

## Normalization and sign audit

- The curve input is exactly `[1,0,0,0,1]`, with conductor 433 and
  discriminant -433.
- `D_q=-3823` and `D_q=8317` are fundamental discriminants. PARI global
  minimal twist models are respectively `[1,1,1,-304486,-55939199084]` and
  `[1,0,1,-1441094,575973336189]`; both have conductor `433*q^2`.
- PARI reports minimal-model changes `[1,319,1,160]` and
  `[1,-693,1,-346]`. In PARI's `[u,r,s,t]` convention the differential scale
  is `u=1`, so the exact Neron comparison is `kappa_q=1` in both computations.
- `msfromell(E,1)` is used for `q=8317`; `msfromell(E,-1)` is used for
  `q=3823`. `mseval(M,x,[oo,r])` pins the path from infinity to `r`.
- The odd-character sign uses
  `tau=sum_u (u/q)exp(2*pi*i*u/q)=i*sqrt(q)` and the translated cusp
  `r+u/q`; this makes the minus-symbol contribution positive. Reversing this
  orientation could negate the residue 1, but cannot alter zero/nonzero.
- Rational character sums are completed before reduction. Every committed
  denominator is 1 or 2, hence a unit modulo 7. The primitive root is pinned by
  `ord_29(2)=28`; changing it only rescales `c` by a nonzero element.

## Reproduction

Run from the repository root:

```text
gp -fq -s 1G millennium-prize/birch-swinnerton-dyer/cycle188_base433_symbol_formula.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle188_base433_symbol_sums.py
```

The GP producer recomputes all 24 exact Legendre-weighted character sums from
the level-433 symbols and fails closed against the committed values. The Python
verifier has no PARI dependency: it validates the CSV schema, row set,
normalizations, exact rational totals, 7-integrality, and finite-field
reduction. The CSV is an aggregate base-symbol certificate, not a dump of all
`12(q-1)` individual cusp evaluations; arithmetic provenance is supplied by
the pinned producer.

Environment used here: PARI/GP 2.15.4 and Python 3. The GP script allocates up
to 4 GB and takes several minutes because it performs 145,656 exact base-symbol
evaluations.
