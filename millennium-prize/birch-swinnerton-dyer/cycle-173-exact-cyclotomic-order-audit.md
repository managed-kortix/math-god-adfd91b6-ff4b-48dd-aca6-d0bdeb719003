# Cycle 173: exact cyclotomic order audit for `433a1` at seven

The proposed conclusion

\[
 \operatorname{ord}_{T=0}F(T)=2
\]

is correct for the Neron-period-normalized ordinary trivial-branch
`7`-adic L-function of `433a1`, but only after separating four logically
different inputs. In particular, the functional equation alone gives the
linear zero only after the constant zero is already known, and the unit in the
functional equation cannot be discarded merely because its value at zero is
one.

## Setup

Let

\[
 E:y^2+xy=x^3+1,
 \qquad p=7,
 \qquad \gamma=8,
\]

and let

\[
 F(T)=\int_{\mathbf Z_7^\times}(1+T)^{\ell(x)}\,d\mu_\alpha(x)
 \in \mathbf Q_7[[T]]
\]

be the ordinary trivial-Teichmuller branch fixed in Cycle 171. Here `alpha`
is the unit root of `X^2+3X+7` and `<x>=8^ell(x)`.

## 1. The positive-rank input is unconditional

The points

\[
 P=(0,1),\qquad Q=(-1,1)
\]

are rational points on `E`. Cycle 136 proves that their images modulo seven
have localization matrix

\[
 \begin{pmatrix}1&5\\1&4\end{pmatrix}
\]

at `29` and `113`, with determinant `-1` modulo seven. Hence their Kummer
classes in `E(Q)/7E(Q)` are independent. They are therefore independent in
`E(Q)`, so

\[
 \operatorname{rank}E(\mathbf Q)\ge2.
\]

For the present vanishing argument, one non-torsion point would suffice. The
Kurihara/Kim upper bound and the conclusion that the rank is exactly two are
not needed.

## 2. What the Gross--Zagier--Kolyvagin contrapositive gives

Use only the established rank-zero implication for modular elliptic curves
over `Q`:

\[
 L(E,1)\ne0
 \quad\Longrightarrow\quad
 E(\mathbf Q)\text{ is finite}
\]

(indeed `Sha(E/Q)` is finite as well). Its literal contrapositive is

\[
 E(\mathbf Q)\text{ infinite}
 \quad\Longrightarrow\quad
 L(E,1)=0.
\]

Since `P` is non-torsion, this proves `L(E,1)=0`. This does not use BSD and it
does not claim that algebraic rank at least two implies analytic rank at least
two. The rank-one Gross--Zagier--Kolyvagin theorem is not being contraposed;
the only contrapositive used is the rank-zero implication above.

Ordinary interpolation at the trivial character has the form

\[
 F(0)=c\,(1-\alpha^{-1})^2\frac{L(E,1)}{\Omega_E^+},
 \qquad c\in\mathbf Q_7^\times,
\]

with `c=1` in the Cycle 171 normalization. Since `alpha != 1`, this gives

\[
 F(0)=0.
\]

## 3. Root number and the exact functional equation

The minimal invariants are `Delta=-433`, `c_4=1`, and `c_6=-865`, so the curve
has multiplicative reduction at its sole bad prime. The standard splitness
criterion is that `-c_6` be a square in the residue field. Here
`-c_6 = 865 = -1 mod 433`, and `179^2 = -1 mod 433`; hence the reduction is
split and

\[
 w_{433}=-1,
 \qquad w_\infty=-1,
 \qquad w(E)=+1.
\]

Equivalently, this sign can be obtained exactly from the local reduction data;
it is not inferred from a numerical analytic-rank entry.

Write the cyclotomic involution as

\[
 \iota(T)=(1+T)^{-1}-1=-T+T^2-\cdots.
\]

After fixing the ordinary stabilization, period, topological generator, and
modular-symbol conventions, the functional equation has the form

\[
 F(T)=w(E)\,u(T)F(\iota(T)),
 \qquad u(T)\in\mathbf Z_7[[T]]^\times.
 \tag{FE}
\]

The unit is not an unspecified scalar. In the convention
`F(T)=w(E)u(T)F(iota(T))` used here, the Mazur--Tate conductor factor is

\[
 u(T)=(1+T)^{-\ell(433)},
 \qquad
 \ell(433)=\frac{\log_7\langle433\rangle}{\log_7(8)}.
\]

Here `<433>=-433` because the Teichmuller part of `433` is `-1`. Thus

\[
 u(0)=1,
 \qquad u'(0)=-\ell(433)
 =-\frac{\log_7(-433)}{\log_7(8)}.
\]

If the functional equation is instead written with `F(iota(T))` on the left,
the unit is inverted and the displayed derivative changes sign. This is only a
rearrangement of the same identity, not a normalization ambiguity. It also
recovers the finite-level tangent relation
`2B=-ell(433)A`. The unit derivative contributes to the exact coefficient
identity, but it is multiplied by the already-proved constant term `F(0)`.

For sign `+1`, write

\[
 F(T)=a_0+a_1T+O(T^2),
 \qquad u(T)=u_0+u_1T+O(T^2).
\]

Comparing constant and linear terms in (FE) gives

\[
 (1-u_0)a_0=0,
 \qquad (1+u_0)a_1=u_1a_0.
 \tag{*}
\]

Thus `u(0)=1` is sufficient only together with `a_0=0`: then
`2a_1=0`, hence `a_1=0`. More generally, after the constant zero, any
`u(0)=1` gives the same conclusion. The derivative `u'(0)` is present in the
exact linear identity, but it is multiplied by `F(0)` and therefore vanishes.

The sign matters. If `w(E)=-1` and `u(0)=1`, the constant term is forced to
zero, while the linear comparison is tautological and does not force `a_1=0`.
Likewise, `u(0)=1` by itself does not force either coefficient to vanish when
the sign is `+1`.

Applying (*) with `w(E)=+1`, the group-like unit `u(0)=1`, and the interpolation
zero proves

\[
 F'(0)=a_1=0,
 \qquad T^2\mid F(T).
\]

If a cited functional equation uses a unit with `u(0) != 1`, it must not be
silently replaced by one with value one. One must either compute its actual
constant term in the chosen normalization or explicitly renormalize `F` by a
unit and track the change. Formula (*) is the convention-safe statement.

## 4. Exact nonvanishing of the quadratic coefficient

Cycle 171 gives the formal identity

\[
 M_2=F''(0)+F'(0),
 \qquad
 M_2=\int\ell(x)^2\,d\mu_\alpha(x).
\]

The exact compatible modular-symbol computation gives

\[
 M_2\equiv5\pmod7.
\]

Since `F'(0)=0`,

\[
 F''(0)=M_2\equiv5\pmod7,
\]

so `F''(0)` is nonzero. Because `2` is a `7`-adic unit, the coefficient of
`T^2` is `F''(0)/2 != 0`. Therefore

\[
 \boxed{\operatorname{ord}_{T=0}F(T)=2.}
\]

This proves an exact order of vanishing for the cyclotomic `7`-adic
L-function. It does not identify its quadratic coefficient with the
cyclotomic height regulator, does not prove the rank-two `p`-adic BSD leading
term, and does not by itself determine the complex analytic order at `s=1`.

## Dependency ledger

- Positive rank: exact rational points plus the Cycle 136 localization
  determinant.
- Complex central zero: contrapositive of the established rank-zero
  Gross--Zagier--Kolyvagin implication.
- Constant `p`-adic zero: ordinary interpolation and `alpha != 1`.
- Linear `p`-adic zero: root number `+1` and the fully normalized functional
  equation, including its unit factor.
- Quadratic nonzero: the exact modular-symbol congruence `M_2 = 5 mod 7` and
  the identity `M_2=F''(0)+F'(0)`.
