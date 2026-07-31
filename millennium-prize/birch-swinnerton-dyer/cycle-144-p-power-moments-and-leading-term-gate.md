# Cycle 144: exact cyclotomic moments and the finite leading-term gate

For `433a1` at `p=7`, exact period-normalized modular-symbol arithmetic at
conductors `7^5,7^6,7^7` gives a reproducible finite cyclotomic packet.  This
advances the `p`-adic leading-term comparison but deliberately stops short of
claiming an equality in `Q_7`.

Let `gamma=8`.  At level `n`, of conductor `7^(n+1)`, write every unit as

\[
a=\omega(a)\gamma^{\ell_n(a)}\pmod {7^{n+1}},
\qquad0\le\ell_n(a)<7^n,
\]

and let `[a]^+_n` be PARI's exact period-normalized plus modular symbol on the
path from infinity to `a/7^(n+1)`.  Define raw moments

\[
D_{j,n}=\sum_{7\nmid a}[a]^+_n\ell_n(a)^j.
\]

The exact integer output is

\[
\begin{array}{c|r|r|r}
n&D_{0,n}&D_{1,n}&D_{2,n}\\ \hline
4&0&-4802&967053944\\
5&0&621859&12876477045\\
6&0&78942479&9062036974073
\end{array}
\]

These are power moments.  If `Theta_n` is the finite Mazur--Tate element in the
coordinate `T=gamma-1`, then

\[
D_{1,n}=\Theta_n'(0),
\qquad
D_{2,n}=\Theta_n''(0)+\Theta_n'(0).
\]

Thus they must not be confused with the falling-factorial `T^2` coefficient or
with an analytic `s`-derivative.

For the unit root `alpha` of

\[
X^2+3X+7,
\qquad\alpha=4\pmod7,
\]

the normalized values `alpha^(-(n+1))D_(2,n)` stabilize as

\[
5,33,278,1650,16056,32863
\]

modulo successive powers `7,...,7^6`.  In particular the normalized second
power moment is a unit.  This is an exact finite modular-symbol certificate,
not yet a convention-free `p`-adic BSD coefficient.

An independent crystalline packet records geometric Frobenius on
`dx/v,x dx/v`, where `v^2=4x^3+x^2+4`, modulo `7^8`:

\[
F=\begin{pmatrix}
3443986&4648947\\124425&2320812
\end{pmatrix}.
\]

It has trace `-3`, determinant `7`, and unit root

\[
\alpha=3795817\pmod{7^8}.
\]

The unit-root eigenvector `(s_2,1)` has

\[
s_2=2509791,
\]

so Katz's relation `s_2=(1-E_2)/12` gives

\[
E_2(E,\omega)=4471315\pmod{7^8}.
\]

This pins the nontrivial parameter needed for higher-precision sigma-height
arithmetic.  The current committed height verifier remains the lower-precision
fully reconstructed certificate of Cycle 143; the Frobenius matrix here is a
compact certificate whose Kedlaya production is not reimplemented by the
integer verifier.

The finite comparison frontier is strict.  A high-precision computation reports
agreement between the ordinary `s`-derivative leading term and the height
regulator through `7^8`, after the inverse-square ordinary Euler factor.  That
agreement is not persisted as a proved congruence here because:

- Cycle 143's committed sigma reconstruction certifies the regulator only
  modulo `7^3`;
- `s`-derivatives, `T`-coefficients, and power moments differ by explicit
  logarithm and lower-moment terms;
- finite precision never proves equality in `Q_7`;
- the full BSD scalar also requires compatible period, lattice, Tamagawa,
  torsion, and complete `Sha` factors, whereas Cycle 135 controls only the
  seven-primary part of `Sha` under published hypotheses.

Reproduce the exact moments with PARI/GP 2.17.2:

```sh
gp -fq -s 512M millennium-prize/birch-swinnerton-dyer/cycle144_433a1_p_power_moments.gp
```

Audit the compact Frobenius/E2 packet with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle144_frobenius_e2.py
```

This is exact finite cyclotomic data and a normalization audit, not a proof of
the `p`-adic BSD leading-coefficient identity, complex BSD, or any Millennium
problem.
