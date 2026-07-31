# Cycle 202: ample linkage gives new connected support but preserves the graph obstruction

## Linkage construction

Let

\[
 A_0=E_i^3\times E_i^3,\qquad
 P=\operatorname {diag}(1,1,1,1,1,3),
\]

and retain the seven graphs `Gamma_k=Gamma_(u^k)`, where `u=2+i`. Fix an
integer `m` sufficiently large that `I_(Gamma_k)(mP)` is globally generated for
every `k`. Choose three general members of this system and put

\[
 W_k=H_{k,1}\cap H_{k,2}\cap H_{k,3}=\Gamma_k\cup R_k,
 \qquad H_{k,j}\in |mP|.                                           \tag{202.1}
\]

The residual is the ideal quotient

\[
 I_{R_k}=(I_{W_k}:I_{\Gamma_k}).                                  \tag{202.2}
\]

For a general regular sequence, standard complete-intersection liaison makes
`R_k` a pure locally Cohen--Macaulay codimension-three cycle. After increasing
`m`, Bertini on the blow-up along `Gamma_k` gives a geometrically integral
residual away from the exceptional divisor; its closure is therefore connected
and has genuinely new support. None of the calculation below relies on
smoothness.

The linkage identity is an equality of Chow classes, not merely cohomology:

\[
 \boxed{[R_k]=m^3P^3-[\Gamma_k]},\qquad
 \boxed{[\Gamma_k]+[R_k]=m^3P^3}.                                 \tag{202.3}
\]

It supplies an explicit rational-equivalence witness by varying each of the
three divisors in its complete linear system. In particular, this is the most
favorable common ample-envelope version of the proposed liaison ansatz.

## Exact residual pair

Write the projector coefficients as `c_k=p_k-n_k`, with `p_k,n_k>=0`, and set

\[
 A_+=\sum p_k=317144491810662771,
 \qquad
 A_-=\sum n_k=2074005086710131.
\]

Then

\[
 A_+-A_-=315070486723952640.
\]

Substitution of (202.3) into `Z=D_0 alpha_0=sum c_k Gamma_k` gives the exact
candidate

\[
 \boxed{
 Y_m^+=(A_+-A_-)m^3P^3+\sum_{c_k<0}(-c_k)R_k,
 \qquad
 Y_m^-=\sum_{c_k>0}c_kR_k,}                                      \tag{202.4}
\]

and

\[
 \boxed{[Y_m^+]-[Y_m^-]=D_0\alpha_0\quad\text{in }CH^3(A_0).}     \tag{202.5}
\]

Both endpoints are effective. The common `P^3` bridge in (202.4) may be
chosen connected to the residual union, so connected endpoint support is not
the issue. Formula (202.5) is an exact finite liaison witness with new support.

## Classes and degrees

Since `P` has type `(1,1,1,1,1,3)`,

\[
 P^6=6!\,3=2160,
 \qquad
 \deg_P(m^3P^3)=m^3\frac{P^6}{3!}=360m^3.                         \tag{202.6}
\]

For `n_k=5^k`, the graph degree and residual degree are

\[
 g_k=\deg_P\Gamma_k=(1+n_k)^2(1+3n_k),
 \qquad
 \boxed{\deg_P R_k=360m^3-g_k}.                                  \tag{202.7}
\]

The seven exact values of `g_k` are

\[
 (16,576,51376,5969376,735159376,91621109376,11445800859376).
\]

Using the Cycle 169 endpoint degrees `d_+` and `d_-`, (202.4) has

\[
 \boxed{
 \deg_PY_m^+=360m^3A_+-d_-,\qquad
 \deg_PY_m^-=360m^3A_+-d_+.}                                    \tag{202.8}
\]

Consequently both degrees exceed the frozen Cycle 169 degrees by the same
amount

\[
 e_m=360m^3A_+-d_+-d_-,                                          \tag{202.9}
\]

while their difference remains `d_+-d_-`, as it must. Therefore liaison
produces a valid higher-degree rational-equivalence incidence, but it does not
produce a point of the active fixed-degree pair space
`Chow_(3,d_+) x Chow_(3,d_-)`.

For the concrete arithmetic specialization `m=15626`, put
`M=m^3=3815429734376`. Then the coefficient of `P^3` in `Y_m^+` is

\[
 1202129303470887655672003952640,
\]

and

\[
\begin{aligned}
 \deg_PY_m^+&=435615308693266367131405038684304,\\
 \deg_PY_m^-&=435615308693262610759378954731664.
\end{aligned}                                                     \tag{202.10}
\]

This numerical specialization records the exact cycle arithmetic; it is not
an effective-regularity claim that `m=15626` is the least linkage level.

## PEL tangent potential

The complete-intersection class `m^3P^3` remains Hodge over the entire PEL
base. Contracting (202.3) with a PEL tangent `B` therefore gives

\[
 \iota_B[R_k]=-\iota_B[\Gamma_k].                                 \tag{202.11}
\]

Hence semiregularity imposes on every embedded or Chow deformation of `R_k`
the same necessary base condition as for the graph:

\[
 \operatorname {im}(dp_{R_k})\subseteq\ker\rho_k,
 \qquad
 \rho_k(B)=Q^{-1}B^t-5^kB.                                      \tag{202.12}
\]

The exact potential dimensions and obstruction-rank lower bounds are

\[
\begin{array}{c|rrrrrrr}
k&0&1&2&3&4&5&6\\ \hline
\dim\ker\rho_k&3&0&0&0&0&0&0\\
\operatorname {rank}\rho_k&6&9&9&9&9&9&9.
\end{array}                                                       \tag{202.13}
\]

These are upper bounds on the actual relative-Chow tangent images; linkage can
make them smaller, never larger. The positive residual endpoint contains
`R_1,R_3,R_6`, and the negative endpoint contains `R_2,R_4,R_5`. Thus every
decomposition-preserving liaison germ for either endpoint contains a residual
whose cohomological obstruction is injective on the full nine-dimensional PEL
tangent. For the explicit product of residual liaison spaces one obtains

\[
 \boxed{\operatorname {im}(dp_{\mathrm{liaison},+})=
        \operatorname {im}(dp_{\mathrm{liaison},-})=0.}           \tag{202.14}
\]

The common `P^3` bridge is horizontal and cannot cancel either residual's raw
deformation condition in this parameter space. Equation (202.14) does not by
itself compute every tangent of the ambient Chow scheme at the summed cycle: a
branch that does not preserve the residual decomposition could have additional
tangents. Certifying or excluding such a branch requires a local equation for
that Chow point.

## Outcome

Ample complete-intersection liaison succeeds at the two geometric tasks that
the graph union did not: it gives connected codimension-three residuals with
new support and an explicit Chow rational equivalence. It nevertheless fails
both active numerical gates. It raises both endpoint degrees by `e_m`, and,
more decisively, replacing `Gamma_k` by `m^3P^3-Gamma_k` negates rather than
cancels its PEL variation. The constructed residual-liaison germ has PEL
tangent potential zero.

Thus common-class linkage cannot be the Cycle 202 positive candidate. A viable
liaison construction would need different ample envelopes whose signed
variations cancel separately inside each effective endpoint, while preserving
the frozen degrees; merely giving the graphs new connected support is
insufficient. No Hodge-conjecture result is claimed.

Reproduce all coefficients and degree identities with

```sh
python3 millennium-prize/hodge/verify_cycle202_ample_linkage.py
```
