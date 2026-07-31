# Cycle 189: exact `[0:1]` base-level-433 collision

## Result

Fix `E=433a1: y^2+xy=x^3+1`, `p=7`, `ell=29`, and primitive root
`eta=2 mod 29`.  The four requested members of the Cycle 187 full `L_0`
conjugacy class `(nonidentity unipotent,[0:1])` give

| `q` | `D_q` | base parity | completed rational sum | `c(q,29)` |
|---:|---:|:---:|---:|---:|
| 8191 | -8191 | minus | -1230 | 2 (nonzero) |
| 10949 | 10949 | plus | -125 | 1 (nonzero) |
| 19559 | -19559 | minus | 1381 | 2 (nonzero) |
| 31963 | -31963 | minus | -391 | 1 (nonzero) |

Since all four are nonzero, the exact computation continued in the same
`[0:1]` class, in increasing order, until

| `q` | `D_q` | completed rational sum | `c(q,29)` |
|---:|---:|---:|---:|
| 34679 | -34679 | 401 | 2 |
| 39439 | -39439 | -2530 | 4 |
| 45053 | 45053 | -97 | 1 |
| 66179 | -66179 | -418 | 2 |
| 77617 | 77617 | 870 | 2 |
| 99709 | 99709 | 1261 | 1 |
| 103811 | -103811 | -3177/2 | 4 |
| 109789 | 109789 | -1354 | 4 |
| 114311 | -114311 | 3311 | 0 |

Thus `(8191,114311)` is an explicit same-`L_0`-class nonzero/zero pair under
the Cycle 185 maximal semidirect-product theorem and Cycle 184 conjugacy
classification.  This refutes factorization of `c(q,29)` through the named
field `L_0`; it is not a BSD proof and does not establish universal
nonfactorization through every finite extension.

## Exact formula

For `epsilon_q=(-1/q)`, put

\[
 U_a(q)=\sum_{u=1}^{q-1}(u/q)
 \left[(aq+29u)/(29q)\right]_E^{\epsilon_q}.
\]

The exact period comparison is `kappa_q=1`. Pairing `a` with `29-a` gives

\[
 c(q,29)=\overline{\sum_{a=1}^{14}w_aU_a(q)}\in\mathbf F_7,
\]

where
`(w_1,...,w_14)=(0,2,3,4,2,5,3,6,6,4,1,0,1,5)`.
The producer uses `msfromell(E,epsilon_q)` and the endpoint path
`[oo,(a*q+29*u)/(29*q)]`, so every modular-symbol evaluation remains in the
fixed level-433 space. Rational sums are completed before reduction modulo 7.

## Artifacts and replay

- Requested four-prime rows: `cycle189_0_1_base433_symbol_sums.csv`.
- Continuation through the first zero: `cycle189_0_1_base433_symbol_sums_continuation.csv`.
- PARI producer: `cycle189_0_1_base433_symbol_formula.gp`.
- Dependency-free verifier: `verify_cycle189_0_1_base433_symbol_sums.py`.
- Producer logs: `cycle189_0_1_pari.log` and `cycle189_0_1_pari_continuation.log`.

Run from the repository root:

```sh
rm -f millennium-prize/birch-swinnerton-dyer/cycle189_0_1_base433_symbol_sums.csv && gp -fq -s 1G millennium-prize/birch-swinnerton-dyer/cycle189_0_1_base433_symbol_formula.gp
rm -f millennium-prize/birch-swinnerton-dyer/cycle189_0_1_base433_symbol_sums_continuation.csv && CYCLE189_CONTINUE=1 gp -fq -s 1G millennium-prize/birch-swinnerton-dyer/cycle189_0_1_base433_symbol_formula.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle189_0_1_base433_symbol_sums.py
```

The first GP command recomputes the requested four-prime artifact. The second
runs the increasing continuation and stops after the first zero. The Python
verifier checks both committed CSV files, their exact row sets and
normalizations, all rational weighted totals, 7-integrality, residues, and the
named zero/nonzero pair.  PARI/GP 2.15.4 was used for the committed run.
