# Cycle 237: exact height/index audit for `A=433a1^(-1499)`

## Verdict

No unconditional finite cutoff `M` is presently certified for the Heegner
index in checkpoint `HK236`. Two independent inputs remain unavailable:

1. a directed proof of the Cremona--Siksek ANTS VII test giving the strict
   everywhere-good-reduction bound `hhat(R)>7`; and
2. a certified identity between the integral Heegner trace `y` and the
   numerical candidate `+/-8P`.

Thus the exact outcome is an obstruction, not a finite `M`. The calculations
below isolate what would follow if each missing certificate were supplied.

## Exact Silverman constant

For the global minimal model

\[
 A:y^2+xy+y=x^3-46813x-3372156843
\]

the exact invariants used here are

\[
 b_2=1,\quad c_4=2247001,\quad
 \Delta=-4912444914224609853433,\quad j=-1/433.
\]

Silverman's explicit height-difference constant, in the normalization used by
eclib and with Bremner's corrected `2*0.961=1.922`, is

\[
 \mu_S=1.922+\frac{h(j)}{12}+\frac{\log|\Delta|}{6}
       +\frac{\log^+|j|}{6}+\log^+|b_2/12|+\log 2.
\]

Here `h(j)=log(433)` and both `log+` terms vanish. Arb interval arithmetic,
converted outward to rationals of denominator `10^50`, gives the explicit
interval printed by the verifier. This is a certified height-difference
constant, but by itself it does not give a positive global lower bound for all
non-torsion rational points: one also needs an exact finite search/exclusion
step. It therefore does not close the requested index bound.

## Siksek lower bound and globalization

The eclib 20231211 Cremona--Siksek computation reports

\[
 \widehat h(R)>7
\]

for every non-torsion point in the everywhere-good-reduction subgroup. Its
public implementation evaluates real roots, elliptic logarithms, exponentials,
and interval intersections with nondirected `bigfloat` arithmetic; replaying at
200 and 300 digits is strong numerical evidence but is not an interval proof.

The globalization step after that bound is exact. The component groups at
`433`, `1499`, and the real place have global exponent `2`. Hence `2G` lies in
the everywhere-good-reduction subgroup for every `G in A(Q)`, and quadraticity
would give

\[
 4\widehat h(G)=\widehat h(2G)>7,
 \qquad \widehat h(G)>7/4.                     \tag{237.1}
\]

Thus `h_min=7/4` is a valid strict global bound conditional only on replacing
the nondirected Siksek computation by a directed certificate.

## Exact upper bounds and cutoffs

Cycle 195 already certifies the rational interval

\[
 \frac{3396338096796685137401217818912911624353760513342938}{10^{50}}
 <\widehat h(P)<
 \frac{3396338096796685137401217818912911624353760513342939}{10^{50}}.
\]

Combining its upper endpoint with (237.1) gives the exact point-index cutoff

\[
 \left\lfloor\sqrt{\widehat h(P)/(7/4)}\right\rfloor=4.
\]

This does not bound the frozen Heegner index, because `HK236` defines
`I=[A(Q)_free:Zy]`, not the index of `P`.

Cycle 209's nondirected computation suggests `y=+/-8P`. If that identity were
certified, exact quadraticity and the same rational upper endpoint would give

\[
 \widehat h(y)=64\widehat h(P)<2174,
 \qquad M=\left\lfloor\sqrt{2174/(7/4)}\right\rfloor=35. \tag{237.2}
\]

Using the tighter rational endpoint directly also gives `M=35`. Equation
(237.2) is explicitly conditional: a rational point recognized after a
floating modular-parametrization calculation does not certify the mathematical
CM trace or its integral normalization.

## Reproduction

Run

```sh
uv run --with python-flint python3 millennium-prize/birch-swinnerton-dyer/verify_cycle237_exact_height_index.py
```

The verifier checks the exact `j`-invariant reduction, evaluates Silverman's
constant in Arb, converts to outward rational endpoints, performs all height
scaling and square-root floors in exact rational/integer arithmetic, and exits
with `NO_UNCONDITIONAL_FINITE_M`. It does not promote either missing numerical
input to a theorem.

Consequently this part of `HK236` is a `WALL`: the arithmetic after the two
missing certificates is finite and exact, with conditional cutoff `M=35`, but
the current artifacts do not supply a certified `hhat(y)` upper bound or a
directed Siksek lower bound.
