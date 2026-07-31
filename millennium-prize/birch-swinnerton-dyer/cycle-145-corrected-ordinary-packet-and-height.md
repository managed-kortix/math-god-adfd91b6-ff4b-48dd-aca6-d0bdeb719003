# Cycle 145: corrected ordinary moments and a mod-`7^8` height certificate

Cycle 144's exact raw modular-symbol table is valid, but its first normalization
omitted the lower-conductor degeneracy term required by ordinary
`7`-stabilization.  For conductor `7^(n+1)`, the compatible second power moment is

\[
M_{2,n}=\alpha^{-(n+1)}\left(D_{2,n}-\alpha^{-1}
\left(7D_{2,n-1}+6\cdot7^nD_{1,n-1}\right)\right)\pmod {7^n}.
\]

The corrected residues are

\[
\boxed{5,40,187,2245,9448,76676}
\]

modulo `7,...,7^6`.  The ordinary moment remains a unit.  It computes

\[
\frac{L_{7,\alpha}''(E,0)}{\log_7(8)^2}
\]

in the fixed PARI period normalization; as a power moment it equals the
combination `F''(0)+F'(0)` in the coordinate `T=8^s-1`, not automatically the
bare `T^2` coefficient.

Independently, the Cycle 143 sigma-height computation is now extended through
modulus `7^8` by a dependency-free verifier.  It uses the Cycle 144
Frobenius-certified value

\[
E_2(E,\omega)=4471315\pmod{7^8}
\]

and sigma coefficients through degree nine.  Degree nine is necessary because
its coefficient has valuation `-1`; degree eight's constant term is
`2125/1296`.  Exact rational point addition, staggered rational reduction, and
an internally evaluated `7`-adic logarithm give

\[
H_7(P,Q)=
\begin{pmatrix}
2952047&1507520\\1507520&4713289
\end{pmatrix}
\pmod{7^8},
\]

and

\[
\boxed{\operatorname{Reg}_7(P,Q)=2495619\pmod{7^8}}.
\]

Equivalently,

\[
7^{-2}\operatorname{Reg}_7(P,Q)=50931\pmod{7^6},
\]

whose first digit is the Cycle 143 unit `6 mod 7`.

The two exact packets now reach matching precision, but no full `p`-adic BSD
scalar equality is claimed.  Such a claim still needs a convention-by-
convention comparison of period normalization, ordinary Euler factor,
augmentation coordinate, saturated Mordell--Weil lattice, Tamagawa and torsion
terms, and the complete `7`-adic image of the full Tate--Shafarevich order.
Finite congruence also cannot prove equality in `Q_7`.

Reproduce with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle145_high_precision_height.py
gp -fq -s 512M millennium-prize/birch-swinnerton-dyer/cycle144_433a1_p_power_moments.gp
```

This closes the curve-specific calibration at its natural exact finite gate.
It does not prove complex BSD or any Millennium problem.
