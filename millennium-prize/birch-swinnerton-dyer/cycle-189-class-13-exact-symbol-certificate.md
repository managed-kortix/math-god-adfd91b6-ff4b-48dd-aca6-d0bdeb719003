# Cycle 189: exact `c(q,29)` certificate for class `[1:3]`

Fix `E=433a1`, `p=7`, `ell=29`, and primitive root `eta=2 mod 29` as in
Cycle 187.  The three requested primes `11831,14897,48889` all pass the frozen
packet and are assigned the same full `L_0` conjugacy label
`(nonidentity unipotent,[1:3])`.  The exact finite-field data are

| `q` | `#E(F_q)` | `a_q` | projective row |
|---:|---:|---:|---:|
| 11831 | 11970 | -138 | `[1:3]` |
| 14897 | 15106 | -208 | `[1:3]` |
| 48889 | 48678 | 212 | `[1:3]` |

The producer evaluates the shortened Cycle 187 formula in the fixed level-433
modular-symbol space.  For each active `a`, the committed CSV records the exact
rational sum

```text
U_a(q) = sum_{u=1}^{q-1} (u/q) [(aq+29u)/(29q)]_E^{epsilon_q}.
```

Cycle 188 proves `kappa_q=1` for this entire prime-twist family.  Summing the
committed rows with weights
`(2,3,4,2,5,3,6,6,4,1,1,5)` gives

| `q` | `D_q` | sign | exact rational lift | `c(q,29) mod 7` | class |
|---:|---:|---:|---:|---:|---:|
| 11831 | -11831 | minus | 74 | 4 | nonzero |
| 14897 | 14897 | plus | -17/2 | 2 | nonzero |
| 48889 | 48889 | plus | -341 | 2 | nonzero |

All denominators are prime to seven.  Thus all three coordinates are nonzero,
so there is no zero/nonzero collision in this requested initial segment of the
`[1:3]` bucket.  The stop condition never fires; all three primes are computed.
The differing exact residue at `11831` versus the other two does not by itself
meet the requested zero/nonzero criterion.

Reproduce and verify from the repository root with

```sh
gp -q millennium-prize/birch-swinnerton-dyer/cycle189_433a1_base_symbol_sums.gp \
  > /tmp/cycle189_base_symbol_sums.csv
cmp /tmp/cycle189_base_symbol_sums.csv \
  millennium-prize/birch-swinnerton-dyer/cycle189_base_symbol_sums.csv
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle189_base_symbol_sums.py
python3 -O millennium-prize/birch-swinnerton-dyer/verify_cycle189_base_symbol_sums.py
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle189_frobenius_class.py
python3 -O millennium-prize/birch-swinnerton-dyer/verify_cycle189_frobenius_class.py
sha256sum -c millennium-prize/birch-swinnerton-dyer/cycle189_SHA256SUMS
```

The Python rational verifier is dependency-free and does not call PARI. The
separate finite-field verifier replays point counts, packet predicates, and
localization rows. The modular-symbol provenance itself is replayed by the
exact PARI producer and byte comparison; these are separate checks around the
same PARI modular-symbol backend, not independent arithmetic backends.
