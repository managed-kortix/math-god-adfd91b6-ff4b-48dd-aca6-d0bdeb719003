# Cycle 210: independent level-433 Manin-symbol replay

## Result

`verify_cycle210_manin_mod7.py` does not call PARI, `msfromell`, Sage, or a
modular-symbol data file. It constructs `P^1(F_433)`, imposes the two Manin
relations, and evaluates cusp paths by continued fractions. Exact point
counting gives `a_2(E)=-1`, and the script imposes the corresponding functional
identity

\[
 A(r/2)+A((r+1)/2)+A(2r)=-A(r).
\]

Over `F_7` the resulting level-433 eigenspace has dimension two, as expected
from the two period signs. The involution `r -> -r` labels the deterministic
basis as even and odd. Applying the quadratic-character twist sum at all
`28*1498` cusps gives parity-line residues `[0,3]`; the odd line needed for the
negative twist has raw residue `3`. This independently certifies nonvanishing.

## Certificate boundary

This implementation does **not** by itself certify the normalized residue `4`
or the rational lift `-150`. A one-dimensional Hecke eigenspace still has an
arbitrary nonzero scalar. Comparison with the Neron-period-normalized Cycle 188
rows uses the unit `6 mod 7`, sending the independently computed odd residue
`3` to `4`. Deriving that unit without PARI requires construction of the
integral homology lattice, selection of its primitive anti-invariant cycle,
and an exact Manin-constant/Neron-differential orientation comparison. That is
the remaining complexity. It does not affect the independently established
nonvanishing needed by the Selmer argument, but it prevents an honest claim
that `-150 mod 7` has been normalized independently.

Run:

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle210_manin_mod7.py
```
