# Cycle 189: exact `c(q,29)` for `[1:2]` members 9521 and 11131

## Result

For `E=433a1: y^2+xy=x^3+1`, `p=7`, `ell=29`, and primitive root
`eta=2 mod 29`, the validated Cycle 187 base-symbol identity gives

| `q` | `D_q` | base parity | completed rational sum | `c_2(q,29)` |
|---:|---:|:---:|---:|---:|
| 9521 | 9521 | plus | -867/2 | 4 (nonzero) |
| 11131 | -11131 | minus | 186 | 4 (nonzero) |

Neither member is zero. Together with the known nonzero value at `q=3823`,
this `[1:2]` continuation does not produce the sought zero/nonzero collision.

## Exact formula and normalization

With `epsilon_q=(-1/q)`, path `[infinity,r]`, and

\[
 U_a(q)=\sum_{u=1}^{q-1}(u/q)
 \left[(aq+29u)/(29q)\right]_E^{\epsilon_q},
\]

the calculation uses the validated paired formula

\[
 c_2(q,29)=\overline{\sum_{a=1}^{14}w_aU_a(q)}\in\mathbf F_7,
\]

where `(w_1,...,w_14)=(0,2,3,4,2,5,3,6,6,4,1,0,1,5)`.
The exact twist-period factor is `kappa_q=1` for this family. PARI confirms
prime inputs, conductor `433*q^2`, and minimal-model changes with scaling
coordinate one. Every aggregate row has denominator 1 or 2 and is therefore
7-integral before reduction.

The exact reductions are

\[
 -867/2\equiv4\pmod7,\qquad 186\equiv4\pmod7.
\]

## Twist audits

| `q` | conductor | minimal model `[a1,a2,a3,a4,a6]` | change `[u,r,s,t]` |
|---:|---:|---|---|
| 9521 | 39251207953 | `[1,1,1,-1888530,864071468336]` | `[1,-793,1,-396]` |
| 11131 | 53648336713 | `[1,1,0,-2581232,-1380718842115]` | `[1,928,1,464]` |

## Reproduction

Run from the repository root:

```text
gp -fq -s 1G millennium-prize/birch-swinnerton-dyer/cycle189_1_2_base433_symbol_formula.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle189_1_2_base433_symbol_sums.py
sha256sum -c millennium-prize/birch-swinnerton-dyer/cycle189_1_2_SHA256SUMS
```

The GP producer recomputes and checks all 24 Legendre-weighted base-symbol
sums in the fixed level-433 symbol space. The dependency-free Python replay
checks the committed CSV schema, exact weighted totals, 7-integrality, and
finite-field reductions. Environment: PARI/GP 2.15.4 and Python 3.
