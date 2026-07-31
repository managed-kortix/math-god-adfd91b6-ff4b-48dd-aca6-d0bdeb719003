# Cycle 194: rigorous derivative certificate for `D=-29023`

## Result

Let

\[
 E:y^2+xy=x^3+1
\]

be `433a1`. For its quadratic twist by `D=-29023`, the producer reports the
minimal model

\[
 y^2+xy+y=x^3+x^2-17548636x-24475377572834,
\]

conductor `N=364730851057=433*29023^2`, and root number `w=-1`. The
fail-closed Python verifier proves by integer and rational arithmetic that

\[
 \frac{9776577544974464}{10^{15}}
 \leq L'(E^{(-29023)},1)
 \leq \frac{141618654480665006}{10^{15}}.              \tag{194.1}
\]

In particular,

\[
 \boxed{L'(E^{(-29023)},1)>0.}
\]

The wider-than-numerical interval is intentional: it is an auditable
nonvanishing proof, not a decimal evaluation.

## Exact AFE and rational bounds

Write `L(E^(-29023),s)=sum(a_n*n^-s)` and put

\[
 \alpha=\frac{2\pi}{\sqrt N},\qquad
 E_1(x)=\int_x^\infty\frac{e^{-t}}t\,dt.
\]

The weight-two functional equation with `w=-1` gives

\[
 L'(E^{(-29023)},1)
 =2\sum_{n\geq1}\frac{a_n}{n}E_1(\alpha n).             \tag{194.2}
\]

For completeness, with

\[
 \Lambda(s)=N^{s/2}(2\pi)^{-s}\Gamma(s)L(s),\qquad
 H(s)=N^{s/2}\sum_{n\geq1}\frac{a_n}{(2\pi n)^s}
                    \Gamma(s,\alpha n),
\]

splitting the Mellin integral at `1/sqrt(N)` gives
`Lambda(s)=H(s)-H(2-s)`.  At `s=1`,
`partial_s Gamma(s,x)=e^(-x) log(x)+E1(x)`; the logarithmic term cancels
the derivative of `N^(s/2)(2*pi*n)^(-s)`.  Finally
`Lambda'(1)=sqrt(N)*L'(1)/(2*pi)` because `L(1)=0`, proving (194.2),
including its factor two and its conductor normalization.

Machin's identity and alternating arctangent series prove the exact rational
enclosure

\[
\begin{split}
0.000010403838892284317869514074224245190037638796397013123501815663368931838482295672
 <\alpha\\
 <0.000010403838892284317869514074224245190037638796397013123501815663368931838482295673.
                                                               \tag{194.3}
\end{split}
\]

The verifier checks (194.3) by squaring against rational bounds for
`4*pi^2/N`; no decimal square root is trusted. It encloses the exponential by
its alternating rational series. Since `u -> exp(-alpha*u)/u` is positive and
convex, midpoint and trapezoid rules on each unit cell respectively give lower
and upper bounds for all `E1(alpha*n)`, `n<=650000`. At the final endpoint it
uses

\[
 \frac{e^{-x}}{x+1}\leq E_1(x)\leq\frac{e^{-x}}x.       \tag{194.4}
\]

Sign-aware summation of the exact integer coefficients gives

\[
 \frac{75518458081702825}{10^{15}}
 \leq 2\sum_{n\leq650000}\frac{a_n}{n}E_1(\alpha n)
 \leq \frac{75876773943936645}{10^{15}}.                \tag{194.5}
\]

This bound includes both bad primes.  At `433 || N`, the reduction is
multiplicative, the local factor is `(1-a_433*433^(-s))^(-1)`, and the
producer checks `a_433=1`; hence `|a_(433^r)|=1`.  At `29023^2 | N`, the
reduction is additive, the local factor is `1`, and the producer checks
`a_29023=0`; hence `a_(29023^r)=0` for `r>=1`.  At every good prime,
Deligne and the degree-two Euler factor give
`|a_(p^r)|<=(r+1)p^(r/2)`. Multiplicativity and
`d(n)<=2*sqrt(n)` therefore imply `|a_n|<=2n` for every `n`. Consequently

\[
 \left|2\sum_{n> M}\frac{a_n}{n}E_1(\alpha n)\right|
 \leq\frac{4e^{-\alpha(M+1)}}
 {\alpha(M+1)(1-e^{-\alpha})}
 \leq\frac{65741880536728361}{10^{15}},                 \tag{194.6}
\]

with `M=650000`. Combining (194.5) and (194.6) yields (194.1).

## Producer trust boundary

The Python verifier independently checks all transcendental enclosures,
quadrature inequalities, coefficient parsing, signed summation, tail
arithmetic, and positivity. It uses `require(...)`, never Python `assert`, so
`python3 -O` cannot disable a certificate check.

The verifier does not independently derive the modular form coefficients,
minimal model, conductor, or root number. Those are the explicit producer
trust boundary. `cycle194_generate_D29023_coefficients.gp` asks PARI/GP 2.15.4
to construct the twist, minimize it, compute `ellglobalred`, `ellrootno`, and
`ellan`, and fails unless the expected model, conductor, and sign occur. It
writes these facts to a metadata file. The consumer pins and parses both
files:

```text
coefficient_sha256=cc7f4e63833e33728233bc8b69a60b6a0609a84cabaafb3c2919b4d79b0992b1
metadata_sha256=b3c1fa2a7f2c7237d76e3e7696d3507f668d66c8c7b4bb25d9433372bfbc9905
```

Thus the mathematical implication certified by the consumer is conditional
only on the pinned producer data being the coefficients and metadata of the
stated twist. Re-running the GP producer re-establishes that boundary with
PARI's exact elliptic-curve routines.

## Analytic rank and arithmetic consequence

The root number `-1` gives `L(E^(-29023),1)=0`, while (194.1) gives a nonzero
first derivative. Hence

\[
 \operatorname{ord}_{s=1}L(E^{(-29023)},s)=1.
\]

The Gross--Zagier--Kolyvagin theorem says, without a square-freeness hypothesis
on the conductor, that for any modular elliptic curve `A/Q`,

\[
 \operatorname{ord}_{s=1}L(A,s)=1
 \quad\Longrightarrow\quad
 \operatorname{rank}A(\mathbf Q)=1
 \quad\hbox{and}\quad
 \Sha(A/\mathbf Q)\ \hbox{is finite}.
\]

Applied here, it therefore gives
`rank E^(-29023)(Q)=1` and finiteness of its Tate--Shafarevich group.  For
clarity, this application is not restricted to square-free conductor.  One
chooses an imaginary quadratic field `K` in which every prime dividing `N`
splits and for which the auxiliary quadratic twist has nonzero central value;
the required `K` exists by quadratic-twist nonvanishing with prescribed local
conditions.  Then

\[
 L(E^{(-29023)}/K,s)
 =L(E^{(-29023)},s)L((E^{(-29023)})^{D_K},s)
\]

has a simple zero.  Gross--Zagier makes the corresponding Heegner point
non-torsion (its trace lies in the `E^(-29023)` eigenspace), and Kolyvagin gives
rank one over `K` and finite Tate--Shafarevich group; restriction and the
quadratic eigenspace decomposition give the assertions over `Q`.  The factor
`29023^2` in `N` causes no Heegner-hypothesis gap: the splitting condition is
imposed on primes dividing `N`, not on their exponents.  Thus no Shimura-curve
extension is needed here.  This is an unconditional rank-one route independent
of BSD, subject to the stated producer boundary; it does not prove the full BSD
leading-term formula.

The inputs are B. Gross and D. Zagier, *Heegner points and derivatives of
L-series*, Invent. Math. 84 (1986), 225--320; V. Kolyvagin, *Euler systems*,
in *The Grothendieck Festschrift*, Vol. II, Progr. Math. 87 (1990), 435--483;
and D. Bump, S. Friedberg, and J. Hoffstein, *Nonvanishing theorems for
L-functions of modular forms and their derivatives*, Invent. Math. 102 (1990),
543--618, which supplies the auxiliary twist with the prescribed local
splitting conditions.  For a reference that presents the resulting arithmetic
theorem, see B. Gross, *Kolyvagin's work on modular elliptic curves*, in
*L-functions and arithmetic* (Durham, 1989), London Math. Soc. Lecture Note
Ser. 153, Cambridge University Press, 1991, 235--256.  The modularity input for
elliptic curves over `Q` is now a theorem.  Alternatively, the general
Gross--Zagier formula on Shimura curves is available in X. Yuan, S.-W. Zhang,
and W. Zhang, *The Gross--Zagier Formula on Shimura Curves*, Annals of
Mathematics Studies 184, Princeton University Press, 2013, but that generality
is unnecessary for the all-split choice of `K` just described.

## Reproduction

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/cycle194_generate_D29023_coefficients.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle194_D29023_afe.py
python3 -O millennium-prize/birch-swinnerton-dyer/verify_cycle194_D29023_afe.py
```

The two verifier invocations must print identical rational intervals and
`Lprime_positive=PASS`.
