# Cycle 224: bounded all-primary control scout

## Scope and verdict

Let

\[
 A_D=433\mathrm a1^{(D)},\qquad D\in\{-1499,-29023\}.
\]

The existing certificates prove analytic and algebraic rank one, finiteness of
`Sha`, trivial rational torsion, Tamagawa product two, and
`Sha(A_D)[2^infty]=0`.  They also prove the seven-primary vanishing for both
curves and the eleven-primary vanishing for `D=-1499`.

There is a sound route from these isolated certificates to a finite list of
remaining primes, but it does not come from repeating Kurihara computations at
all primes.  The correct global integer is the index of one normalized Heegner
trace.  An effective upper bound for that index, together with an explicit
integral Kolyvagin bound, would exclude every prime above one computable bound.
Neither required input is presently certified in the repository.

This is a fixed-curve reduction, not a bound uniform in an unbounded twist
parameter.  No bound independent of `D` is suggested.

## Conditional finite-prime theorem

For each `D`, choose an explicit imaginary quadratic field `K_D` such that all
primes dividing `N_D=433D^2` split in `K_D` and

\[
 L(A_D^{\chi_{K_D}},1)\ne0.
\]

Let `y_D in A_D(Q)` be the integrally normalized trace of the corresponding
Heegner divisor and put

\[
 I_D=[A_D(Q)_{\rm free}:\mathbf Z y_D].
\]

The following is the exact theorem packet needed here.

**Effective integral Kolyvagin bound.**  There is a computable integer
`C_D=C(A_D,K_D)` such that

\[
 \#\Sha(A_D/\mathbf Q)\mid (C_DI_D)^2,                 \tag{224.1}
\]

where `C_D` is given explicitly from the chosen optimal parametrization,
Manin denominator, Tamagawa and Heegner local factors, residual exceptional
primes, and the primes at which the integral Kolyvagin-system comparison is
not primitive.  In particular, no unnamed phrase such as "up to bad primes"
or "for all sufficiently large primes" is allowed.

If, independently, certified height estimates give

\[
 0<h_{\min,D}\le \widehat h(G)
 \quad\hbox{for every non-torsion }G\in A_D(Q),
 \qquad
 \widehat h(y_D)\le H_D,
\]

then `y_D=I_DG_D` for a primitive generator and

\[
 I_D\le M_D:=\left\lfloor\sqrt{H_D/h_{\min,D}}\right\rfloor. \tag{224.2}
\]

Equations (224.1)--(224.2) imply the effective support statement

\[
 p\mid\#\Sha(A_D/\mathbf Q)
 \quad\Longrightarrow\quad
 p\le B_D:=\max\{M_D,\ P^+(C_D)\}.                    \tag{224.3}
\]

Thus `Sha=1` reduces to exact `p`-Selmer or primitive Kurihara certificates for
the finite set

\[
 \{p\le B_D:p\text{ prime}\},
\]

after deleting `2`, the already closed primes, and primes excluded directly by
the factorization of `C_DI_D` if the exact index is eventually obtained.
The finite checks may use descent, Kurihara systems, or Kolyvagin localization;
they need not use one method uniformly.

## How to make the index bound effective

This route does not require rational coordinates for the large generator of
`A_{-29023}`.  It requires the following finite data instead.

1. Name `K_D` and certify the Heegner splitting conditions and
   `L(A_D^{chi_K},1) != 0` by a directed approximate-functional-equation
   calculation.
2. Fix the optimal quotient, CM divisor, trace, differential, period, and
   Manin conventions defining the integral point `y_D`.
3. Apply an explicit Gross--Zagier formula to enclose `hhat(y_D)` from the
   already certified `L'(A_D,1)` and the new rank-zero central value.
4. Produce a directed, curve-specific positive lower bound for the canonical
   height of every non-torsion rational point.  For `D=-1499`, the existing
   Cremona--Siksek calculation is close, but its ANTS constant is not presently
   directed.  For `D=-29023`, a new lower-height certificate is needed.
5. Evaluate every exceptional factor in the integral Kolyvagin theorem and
   output `C_D`, `M_D`, and `B_D` as integers.

The numerical Cycle 209 candidate `K=Q(sqrt(-115))`, `y=+/-8P` for `D=-1499`
does not supply these data: the trace normalization and index eight were
obtained through a nondirected numerical stage.  It is useful evidence, not an
integral Heegner-index certificate.

## Assessment of the proposed mechanisms

- **Kolyvagin systems:** This is the viable large-prime mechanism.  A single
  normalized Heegner class controls all primary parts through its integral
  index.  Mod-`p` nonvanishing is then automatic for every `p` not dividing the
  index or the explicit comparison factor.
- **Kurihara systems:** They are excellent finite-prime certificates, as the
  existing `p=7,11` calculations show, but no theorem presently makes one
  Kurihara coordinate nonzero for every large `p`.  Searching separately at
  each `p` is not an all-prime proof.
- **Visibility:** Visibility turns a pre-existing `Sha[p]` class into a point
  on an auxiliary quotient; it does not by itself show that the class is zero.
  Uniform auxiliary-level and saturation bounds would merely repackage the
  same integral-index problem.
- **Discriminant and height bounds:** These can bound `I_D` after an integral
  Heegner trace is fixed.  The minimal discriminant alone does not bound
  `Sha`: it supplies only a lower-height ingredient and no Euler-system
  content.
- **Euler-system primitivity:** Residual primitivity prime by prime is
  insufficient unless its exceptional support is explicitly bounded.
  Multiplying the Euler system by an arbitrary integer preserves its rational
  norm relations and inserts arbitrary exceptional primes, so rational
  nonvanishing, open image, and height bounds cannot determine integral
  content.

## Exact missing lemma and obstruction

The sharp missing lemma for the two fixed twists is:

> Construct an integrally normalized Heegner/Kolyvagin system for each `A_D`
> and prove the divisibility (224.1) with a completely explicit, computable
> exceptional factor `C_D`; simultaneously certify a numerical upper bound for
> its initial index `I_D` via (224.2).

The essential obstruction is integral normalization and primitivity, not
analytic rank or residual Galois image.  The committed work controls a
Kurihara class modulo selected primes and proves qualitative Kolyvagin
finiteness, but it does not control the common integral content of the global
Euler system.  Neither visibility nor discriminant estimates recover that
content.  Without `C_D` and a certified bound for `I_D`, the assertion that
only finitely many primary parts remain is qualitative and supplies no finite
list to check.

Even after this lemma, proving `Sha=1` still requires the finite primary
computations below `B_D`; the lemma reduces the problem but does not itself
force the remaining primary parts to vanish.

No full `Sha=1` or BSD result is claimed.
