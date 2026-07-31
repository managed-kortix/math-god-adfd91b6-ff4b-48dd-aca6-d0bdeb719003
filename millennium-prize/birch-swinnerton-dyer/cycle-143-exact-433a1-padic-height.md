# Cycle 143: exact nondegenerate cyclotomic height for `433a1` at seven

For

\[
E: y^2+xy=x^3+1,
\qquad P=(0,1),\quad Q=(-1,1),
\]

the Mazur--Tate cyclotomic `7`-adic height regulator on the displayed basis has

\[
\boxed{v_7(\operatorname{Reg}_7(P,Q))=2},
\qquad
\boxed{7^{-2}\operatorname{Reg}_7(P,Q)=6\pmod7}.
\]

This is certified directly from rational point addition and the first universal
coefficient of the `7`-adic sigma function; it does not use floating point,
LMFDB regulator data, or a Kurihara/localization determinant comparison.

In the Mazur--Tate normalization, since `#E(F_7)=11`, write

\[
11R=\left(\frac{a_R}{d_R^2},\frac{b_R}{d_R^3}\right),
\qquad t_R=-\frac{d_Ra_R}{b_R}.
\]

Then

\[
h_7(R)=-\frac2{11^2}
\log_7\left(\frac{\sigma_7(t_R)}{d_R}\right).
\]

For the model `a_1=1`, the normalized sigma function begins

\[
\sigma_7(t)=t+\frac12t^2+O(t^3).
\]

The exact denominators obtained from rational multiplication are

\[
d_P=1142645914879,
\quad d_Q=28947905964019,
\quad d_{P+Q}=616305335858646371.
\]

Their valuations are respectively `1,1,2`.  Consequently the displayed sigma
truncation suffices modulo `49`: for the first two points `t^2=0 mod 49`, and
for the third even `t=0 mod 49`.

Exact modular reduction gives

\[
\begin{array}{c|ccc}
R&t_R\pmod{49}&\sigma(t_R)/d_R\pmod{49}&
\log_7(\sigma(t_R)/d_R)\pmod{49}\\ \hline
P&28&44&7\\
Q&21&22&21\\
P+Q&0&8&7
\end{array}
\]

and hence

\[
h_7(P)=42,
\qquad h_7(Q)=28,
\qquad h_7(P+Q)=42
\pmod{49}.
\]

Polarization yields

\[
h_7(P,Q)=
\frac{h_7(P+Q)-h_7(P)-h_7(Q)}2
=35\pmod{49}.
\]

Thus

\[
H_7(P,Q)=
\begin{pmatrix}42&35\\35&28\end{pmatrix}
\pmod{49}.
\]

Every entry is divisible by seven, so knowledge modulo `49` determines the
determinant modulo `343`.  Directly,

\[
\det H_7=42\cdot28-35^2
=294=6\cdot7^2\pmod{343}.
\]

This proves both the valuation and leading unit.  With cyclotomic coordinate
`T=[8]-1`, one has `log_7(8)/7=1 mod 7`; therefore dividing the regulator by
`log_7(8)^2` has the same residual unit `6`.  Changing the topological generator
rescales the normalized determinant by a square unit, so nonvanishing is
generator-independent.

Under the standard Nekovář/Sano identification of the first cyclotomic
Bockstein pairing with the cyclotomic `p`-adic height (up to sign and the fixed
augmentation coordinate), the computation proves nondegeneracy of that
rank-two pairing for this curve.  It does **not** identify the scalar `6` with
the Cycle 136 localization determinant or Cycle 135 Kurihara number.  Their
matching residues are not a proved comparison theorem.

The direct auxiliary-to-cyclotomic transport proposed after Cycle 142 is also
closed: `I_q/I_q^2` is finite `p`-power torsion, whereas the cyclotomic
`J/J^2` is torsion-free, so every integral linear map between them is zero.
Class-field theoretically the auxiliary direction is tame inertia at `q`,
while the cyclotomic extension is unramified at `q` and kills that inertia.
Any actual comparison must therefore be global and cohomological; no direct
augmentation-line specialization exists.

Reproduce the height certificate with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle143_433a1_padic_height.py
```

This is a curve-specific exact `p`-adic regulator computation.  It does not
prove a complex leading-coefficient formula, a general BSD theorem, or any
Millennium problem.
