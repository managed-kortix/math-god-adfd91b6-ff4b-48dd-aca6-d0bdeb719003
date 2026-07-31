# Cycle 189: a zero in the small `[1:5]` bucket

## Exact result

For `E=433a1: y^2+xy=x^3+1`, `p=7`, `ell=29`, and primitive root
`eta=2 mod 29`, the validated level-433 formula gives

| `q` | `D_q` | base symbol | completed rational sum | `c(q,29)` |
|---:|---:|:---:|---:|---:|
| 7589 | 7589 | plus | 359/2 | 1 (nonzero) |
| 14071 | -14071 | minus | 1243/2 | 2 (nonzero) |
| 29023 | -29023 | minus | 77/2 | 0 |

The two requested primes are nonzero. Continuing to the next member of the
same Cycle 187 `[1:5]` Frobenius bucket finds a zero at `q=29023`. Since Cycle
188 computed `c(1499,29)=4`, the pair

\[
 (q_0,q_1)=(29023,1499),\qquad
 c(q_0,29)=0,\quad c(q_1,29)=4\ne0
\]

is the sought zero/nonzero comparison for primes assigned the same full `L_0`
conjugacy class by the Cycle 184--187 classification. This report certifies the
symbol values, not that class assignment; Cycle 190 supplies the fail-closed
combined class-and-symbol certificate. The resulting conclusion is strict and
no-exception only, not eventual Frobenian nonfactorization.

## Formula and normalization

For `epsilon_q=(-1/q)` and the endpoint path `[infinity,r]`, set

\[
 U_a(q)=\sum_{u=1}^{q-1}(u/q)
 \left[(aq+29u)/(29q)\right]^{\epsilon_q}_E.
\]

The exact computation uses

\[
 c(q,29)=\overline{\sum_{a=1}^{14}w_aU_a(q)},\qquad
 (w_1,\ldots,w_{14})=(0,2,3,4,2,5,3,6,6,4,1,0,1,5),
\]

with reduction modulo 7 only after summing in `Q`. The producer uses
`msfromell(E,epsilon_q)` at fixed level 433 and evaluates the 12 nonzero-weight
rows; it never constructs a level `433*q^2` modular-symbol space.

PARI gives global-minimal changes `[1,-632,1,-316]`, `[1,1173,1,587]`, and
`[1,2419,1,1210]` for `q=7589,14071,29023`, respectively. Thus the
differential scale and `kappa_q` are 1 in every case. The corresponding minimal
models are

```text
7589:  [1,1,0,-1199852,437578048685]
14071: [1,1,1,-4124855,-2789186289434]
29023: [1,1,1,-17548636,-24475377572834]
```

and each conductor is exactly `433*q^2`. Every committed denominator is 1 or
2, hence a 7-adic unit. In particular, `77/2` reduces exactly to zero modulo 7.

## Reproduction

Run from the repository root:

```sh
gp -fq -s 4G millennium-prize/birch-swinnerton-dyer/cycle189_base433_symbol_sums.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle189_base433_symbol_sums.py
python3 -O millennium-prize/birch-swinnerton-dyer/verify_cycle189_base433_symbol_sums.py
```

The GP producer recomputes all 36 exact Legendre-weighted raw sums from the
level-433 symbols and fails closed against the committed values. The separate
Python verifier checks the CSV schema, row sets, weights, signs, exact rational
totals, 7-integrality, and residues without invoking PARI. It replays output
from the same PARI modular-symbol backend and is not an independent arithmetic
backend. Environment: PARI/GP 2.15.4
and Python 3.

This establishes the exact modular-symbol zero/nonzero input. A final Cycle 182
certificate still needs to package the already proved common `L_0` class with
the explicit comparison maps required there.
