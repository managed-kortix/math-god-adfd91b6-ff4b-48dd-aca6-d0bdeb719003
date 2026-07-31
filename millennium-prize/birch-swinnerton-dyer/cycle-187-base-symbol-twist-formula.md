# Cycle 187: direct base-symbol formula for `c(q,29)`

## Result

Fix

\[
 E=433\mathrm a1:y^2+xy=x^3+1,
 \qquad D_q=\begin{cases}q,&q\equiv1\pmod4,\\-q,&q\equiv3\pmod4,
 \end{cases}
\]

where `q` is an odd prime away from `7*433`, and put
`chi_q(u)=(u/q)`.  Fix `eta=2 mod 29`.  It has order 28.

There is no need to construct the level-`433*q^2` modular-symbol space.  It is
enough to evaluate the fixed level-433 symbols of `E` at the `28(q-1)` cusps

\[
 r_{a,u}=\frac{aq+29u}{29q},\qquad 1\leq a\leq28,
 \quad1\leq u\leq q-1.                                    \tag{187.1}
\]

Let

\[
 \epsilon_q=\chi_q(-1)=\operatorname {sgn}(D_q)
\]

and use the base plus symbol if `epsilon_q=1` and the base minus symbol if
`epsilon_q=-1`.  Define the positive rational period-comparison factor

\[
 \kappa_q=
 \begin{cases}
 \displaystyle\frac{\Omega_E^+}{\sqrt q\,\Omega_{E^{(q)}}^+},
       &q\equiv1\pmod4,\\[8pt]
 \displaystyle\frac{\Omega_E^-}{\sqrt q\,\Omega_{E^{(-q)}}^+},
       &q\equiv3\pmod4.
 \end{cases}                                                \tag{187.2}
\]

Although written with periods, `kappa_q` is rational.  It should be obtained
exactly from the pullback of Neron differentials under the quadratic-twist
isomorphism, not from decimal periods.  If the chosen global minimal twist
model has differential comparison factor one, then `kappa_q=1`; this must be
checked from the actual model rather than assumed.

Put

\[
 T_a(q)=\kappa_q\sum_{u=1}^{q-1}\left(\frac uq\right)
 \left[\frac{aq+29u}{29q}\right]^{\epsilon_q}_E\in\mathbf Q. \tag{187.3}
\]

The exact identity below shows that `T_a(q)` is the twist symbol
`[a/29]^+`; in particular it is the right quantity on which to perform the
7-integrality check.  Reducing only these completed rational sums gives

\[
 \boxed{
 c_2(q,29)=
 \sum_{a=1}^{28}\overline{\log_2(a)}\,\overline{T_a(q)}
 \quad\in\mathbf F_7.}                                     \tag{187.4}
\]

Here a bar means reduction in `F_7`, and (187.4) is used only after checking
that every `T_a(q)` is 7-integral.  The notation
`[r]^{epsilon_q}_E` means `[r]^+_E` for `q=1 mod 4` and `[r]^-_E` for
`q=3 mod 4`.

Pairing `a` with `29-a` gives a smaller explicit sum.  Put
`R_a(u)=[r_{a,u}]^{epsilon_q}_E`.  Since
`log_2(-a)=log_2(a)+14`, hence the two logarithms agree modulo 7, and the
symbol and quadratic-character signs cancel in the odd-character case,
(187.4) is equivalently

\[
\boxed{\begin{aligned}
c_2(q,29)=\overline{\kappa_q\sum_{u=1}^{q-1}
 \left(\frac uq\right)\big(&2R_2(u)+3R_3(u)+4R_4(u)+2R_5(u)\\
 &+5R_6(u)+3R_7(u)+6R_8(u)+6R_9(u)\\
 &+4R_{10}(u)+R_{11}(u)+R_{13}(u)+5R_{14}(u)\big)
 }\pmod7 .                                                  \tag{187.5}
\end{aligned}}\]

Thus only `12(q-1)` weighted base-symbol evaluations are needed after the
elementary `a <-> 29-a` pairing.  Continued-fraction reduction computes all of
them in the one fixed level-433 modular-symbol space.

## Derivation and sign audit

Use the endpoint convention

\[
 A_f(r)=2\pi i\int_{i\infty}^{r}f(z)\,dz,
 \qquad
 A_E(r)=[r]^+_E\Omega_E^+ +[r]^-_E i\Omega_E^- .             \tag{187.6}
\]

This is the divisor convention `[r]-[infinity]` and agrees with evaluating the
path `[infinity,r]`.  For

\[
 \tau_q=\sum_{u\bmod q}\left(\frac uq\right)e^{2\pi iu/q}
 =\begin{cases}\sqrt q,&q\equiv1\pmod4,\\i\sqrt q,&q\equiv3\pmod4,
 \end{cases}                                                \tag{187.7}
\]

Fourier expansion gives, with no additional sign,

\[
 A_{f_E\otimes\chi_q}(r)=\frac1{\tau_q}
 \sum_{u\bmod q}\left(\frac uq\right)A_E(r+u/q).           \tag{187.8}
\]

The `u=0` term vanishes.  If `q=1 mod 4`, both `tau_q` and the character are
 real, so taking real parts of (187.8) selects the base plus symbol.  If
`q=3 mod 4`, division by `i*sqrt(q)` converts the imaginary part of the base
integral into the real part of the twist integral, so it selects the base
minus symbol with a positive sign.  Dividing by the positive twist period
gives

\[
 [a/29]^+_{E^{(D_q)}}=\kappa_q
 \sum_{u=1}^{q-1}\left(\frac uq\right)
 [r_{a,u}]^{\epsilon_q}_E.                                  \tag{187.9}
\]

Substitution of (187.9) into the defining Kurihara sum proves (187.4).
For the shortened formula, modular-symbol parity gives

\[
 [-r]^\epsilon_E=\epsilon[r]^\epsilon_E,
 \qquad
 R_{29-a}(u)=\epsilon_qR_a(q-u).
\]

After `u -> q-u`, the second factor `epsilon_q` comes from
`chi_q(-u)=epsilon_q chi_q(u)`, so every `a,29-a` pair contributes twice the
same sum.  The coefficients displayed in (187.5) are therefore
`2 log_2(a) mod 7` for `1<=a<=14`; the zero coefficients at `a=1,12` are
omitted.

The sign in (187.9) depends on all three conventions in (187.6)--(187.8).
Using paths `[r,infinity]` changes both sides together and does not change the
formula.  Replacing `r+u/q` by `r-u/q`, or replacing `tau_q` by its conjugate,
multiplies the odd-character formula by `-1`.  Therefore an implementation
 must pin the additive character in (187.7) and test one Fourier coefficient;
the zero/nonzero value is unaffected, but an exact nonzero residue is not.

## Normalization audit

1. **Periods.**  The only period factor is `kappa_q`.  Compute it from the
   exact change of variables between the generated twist and its global
   minimal model.  Decimal periods are only a consistency check.
2. **Real components.**  `Delta(E)=-433<0`, and a quadratic twist multiplies
   the discriminant by a positive sixth power, so both the base curve and every
   twist here have one real component.  No unrecorded factor from a second real
   component is allowed in (187.2).
3. **Manin constants.**  Formula (187.9) compares analytically normalized
   newform symbols.  There is no extra Manin factor if `[r]^+` and `[r]^-` are
   defined by (187.6).  If software instead returns a generator of a geometric
   integral symbol lattice, its Manin and modular-parametrization scaling must
   be inserted into `kappa_q`.  For the base optimal curve the audited Manin
   constant is one; the twist-side convention still has to be recorded.
4. **Minus-symbol orientation.**  The positive number `Omega_E^-` is defined
   by writing the anti-invariant period as `i*Omega_E^-`.  Reversing that cycle
   negates every base minus symbol.  Pin this orientation once for all `q=3
   mod 4` computations.
5. **Reduction modulo seven.**  Do the character sums in `Q`, multiply by the
   exact rational `kappa_q`, and only then reduce.  Require each completed
   `T_a(q)` to have denominator prime to seven.  Formula (187.5) can be reduced
   as one completed rational sum if only the final scalar, rather than all 28
   twist-symbol rows, is being certified.  A cancellation may make the
   completed sum 7-integral even if an unnecessarily fine intermediate
   presentation is not.
6. **Primitive root.**  The residues of `log_2(a)` for `a=1,...,28` are pinned
   by `2^j mod 29`; changing the primitive root rescales `c` by a unit.  The
   coefficients in (187.5) already include the `a <-> 29-a` factor of two.

This replaces varying-level modular-symbol construction by exact evaluations
in one fixed base space.  It does not make `c(q,29)` a fixed-field Frobenius
function: the endpoint denominator still contains the varying prime `q`.
