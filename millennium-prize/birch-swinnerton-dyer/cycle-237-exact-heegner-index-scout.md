# Cycle 237: exact auxiliary modular-symbol analytic factor

## Exact arithmetic result and retraction

Let

\[
 B=433\mathrm a1:y^2+xy=x^3+1,
 \qquad A=B^{(-1499)},
\]

where the global minimal model of `A` is

\[
 y^2+xy+y=x^3-46813x-3372156843.
\]

For the Cycle 209 Heegner field of discriminant `-115`, the rank-zero
auxiliary twist is `B^(172385)`, because

\[
 172385=115\cdot1499=5\cdot23\cdot1499.
\]

The exact plus modular-symbol calculation gives

\[
 S=\sum_{a=1}^{172384}
 \left(\frac{a}{172385}\right)
 \left[\frac{a}{172385}\right]^+_B=64.                 \tag{237.1}
\]

Every summand is rational and the verifier evaluates the sum in exact PARI
arithmetic. No real approximation or rounding occurs.

With the standard optimal-curve Manin normalization, the quadratic-twist
formula is

\[
 L(B^{(172385)},1)=\frac{\Omega_B}{\sqrt{172385}}S.
\]

The imaginary-period relation for `A=B^(-1499)` is

\[
 2|\operatorname{Im}\omega_2(A)|=
 \frac{\Omega_B}{\sqrt{1499}}.
\]

Substitution in the analytic index-square factor used by PARI's Gross--Zagier
point-search normalization gives the exact cancellation

\[
 I_{\rm an}^2=
 \frac{\sqrt{115}\,L(B^{(172385)},1)}
 {2|\operatorname{Im}\omega_2(A)|}
 =S=64.                                                \tag{237.2}
\]

Thus the former decimal `63.996...` is replaced by an exact analytic factor.
It is **not** the integral Mordell--Weil index without an independent `Sha`
input: in PARI's recovery convention
`I_A^2=I_an^2*Sha_an`.  The former claims `I_A^2=64` and `I_A=8` are retracted.

## Equality gate

Equation (237.2) does **not prove that the trace is the displayed
rational point `+/-8P`.  The point

\[
 P=\left(\frac{399030891253207}{156180668809},
 \frac{7009131418974188521075}{61722131771310373}\right)
\]

is checked exactly, as are `+8P` and `-8P`, but identifying the CM divisor's
modular-parametrization image with either candidate still requires one of:

1. a directed enclosure of the class-group modular-parametrization sum and of
   the elliptic logarithm of `8P`, with disjoint lattice translates; or
2. an exact algebraic construction of the CM divisor image and its trace.

PARI's `ellheegner` performs the first comparison with ordinary floating
arithmetic. Exactness of (237.1) repairs the index-rounding defect, but it does
not turn that separate floating elliptic-logarithm recognition into an exact
equality certificate. Accordingly this scout does not assert
`y_K=+/-8P`.

## Reproduction

Run

```sh
gp -fq -s 4G millennium-prize/birch-swinnerton-dyer/verify_cycle237_exact_heegner_index.gp
```

The costly part is the `172384`-term exact modular-symbol sum. The script fails
closed unless the result is exactly `64`; this certifies the analytic factor,
not an integral Heegner index. The unresolved trace and `Sha` gates are labelled
explicitly.
