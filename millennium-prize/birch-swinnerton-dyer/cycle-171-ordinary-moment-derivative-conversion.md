# Cycle 171: exact ordinary-moment/derivative conversion for `433a1` at seven

Cycles 144--145 computed the correct ordinary second power moment, but did not
fully separate three normalizations: ordinary stabilization, the change from an
augmentation coordinate to an analytic cyclotomic variable, and the real
period used by the modular symbol.  Once these are named, the conversion is an
identity rather than an unspecified unit.

## The period-normalized ordinary measure

Let

\[
E:y^2+xy=x^3+1,\qquad p=7,\qquad a_7=-3,
\]

and let `alpha` be the unit root

\[
\alpha^2+3\alpha+7=0,\qquad \alpha\equiv4\pmod7.
\]

PARI's `msfromell(E,1)` returns the plus symbol `x^+` characterized by

\[
2\pi i\int_\delta f(z)\,dz
 =x^+(\delta)\Omega_E^+ + x^-(\delta)i\Omega_E^-,
\]

where `Omega_E^+` is the positive Neron period of the supplied minimal model.
Thus the values used in Cycle 144,

\[
[a]^+_n=x^+([a/7^{n+1}]-[\infty]),
\]

already contain division by `Omega_E^+`.  There is no hidden numerical period
in the subsequent conversion.

The ordinary level-`7` symbol is

\[
x_\alpha^+=x^+-\alpha^{-1}x^+|V_7.
\]

Normalizing its conductor-`7^(n+1)` distribution by `alpha^(-(n+1))` gives the
ordinary measure `mu_alpha`.  Tracing the `V_7` term over the seven lifts gives,
for the second power moment,

\[
M_{2,n}=\alpha^{-(n+1)}\left(D_{2,n}-\alpha^{-1}
 \left(7D_{2,n-1}+6\cdot7^nD_{1,n-1}\right)\right)\pmod {7^n}.
\tag{1}
\]

Consequently the Cycle 145 residues

\[
5,40,187,2245,9448,76676
\]

are the compatible residues of one element

\[
M_2=\int_{\mathbf Z_7^\times}\ell(x)^2\,d\mu_\alpha(x)\in\mathbf Z_7,
\]

where `<x>=8^ell(x)`.  Applying only `alpha^(-(n+1))` to the raw symbol is not
the ordinary projection; the lower-conductor subtraction in (1) is essential.

## Exact coordinate conversion

Put

\[
F(T)=\int_{\mathbf Z_7^\times}(1+T)^{\ell(x)}d\mu_\alpha(x)
\]

on the trivial Teichmuller branch.  Differentiation at `T=0` gives

\[
F'(0)=\int\ell(x)d\mu_\alpha(x),\qquad
F''(0)=\int\ell(x)(\ell(x)-1)d\mu_\alpha(x),
\]

and hence

\[
\boxed{M_2=F''(0)+F'(0).}
\tag{2}
\]

Now use the analytic cyclotomic variable `s`, with

\[
T=8^s-1=\exp(s\log_7(8))-1,
\qquad L_{7,\alpha}^{E}(s)=F(8^s-1).
\]

The chain rule, without any vanishing assumption, gives

\[
(L_{7,\alpha}^{E})''(0)
=\log_7(8)^2\bigl(F''(0)+F'(0)\bigr).
\]

Therefore the exact conversion is

\[
\boxed{
M_2=\frac{(L_{7,\alpha}^{E})''(0)}{\log_7(8)^2},
\qquad
\frac{(L_{7,\alpha}^{E})''(0)}{2}
=\frac{\log_7(8)^2}{2}M_2.
}
\tag{3}
\]

The first equality converts the ordinary power moment to a second derivative;
the second converts it to the quadratic Taylor coefficient.  The factor `1/2`
must not be inserted into the power moment itself.  Also, replacing (2) by the
bare `F''(0)` is valid only when `F'(0)=0` has separately been proved.

Thus the requested computable scalar is exactly

\[
\boxed{\log_7(8)^2}
\]

for the second derivative, or `log_7(8)^2/2` for its Taylor coefficient.  For
example,

\[
\log_7(8)=1157779\pmod {7^8},\qquad
\log_7(8)^2=3389918\pmod {7^8}.
\]

## Period changes and the Euler factor

Formula (3) uses the Neron-period normalization built into `msfromell`.  If a
different plus period `Omega_*^+` is used to normalize the same complex
integrals, then

\[
L_{7,\alpha}^{*}
=\frac{\Omega_E^+}{\Omega_*^+}L_{7,\alpha}^{E},
\qquad
M_2^*=\frac{\Omega_E^+}{\Omega_*^+}M_2^E.
\tag{4}
\]

This explicit rational period ratio is the only period scalar.  For the
minimal strong-Weil model `433a1` in the audited normalization, the Manin
constant is one, so no additional Manin factor is present.  Equation (4) is the
safe formula if one changes curve, differential, or canonical-period
convention.

The ordinary interpolation factor at the trivial character is

\[
e_7(\alpha)^2=(1-\alpha^{-1})^2.
\]

It is already produced by the stabilized measure `mu_alpha`; it is not an
extra multiplier in (3).  It appears only when comparing the p-adic
L-leading term with an unstabilized arithmetic regulator.  The Cycle 145
packets satisfy the finite congruence

\[
\boxed{
\frac{M_2}{2}\equiv
(1-\alpha^{-1})^2
\frac{\operatorname{Reg}_7(P,Q)}{\log_7(8)^2}
\pmod {7^6}.
}
\tag{5}
\]

Indeed, modulo `7^6`,

\[
\begin{aligned}
M_2/2&=38338,\\
(\log_7(8)/7)^2&=69182,\\
(\operatorname{Reg}_7/7^2)/(\log_7(8)/7)^2&=91398,\\
(1-\alpha^{-1})^2&=22779,
\end{aligned}
\]

and `91398*22779=38338 mod 7^6`.  Equivalently, the finite packet identifies
the regulator-comparison scalar as

\[
2(1-\alpha^{-1})^2
\]

after both sides are expressed in the `T=[8]-1` coordinate.  This last statement
is an exact congruence of the committed finite data, not a proof of equality in
`Q_7` and not a p-adic BSD theorem.

Reproduce the scalar audit with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle171_moment_conversion.py
```
