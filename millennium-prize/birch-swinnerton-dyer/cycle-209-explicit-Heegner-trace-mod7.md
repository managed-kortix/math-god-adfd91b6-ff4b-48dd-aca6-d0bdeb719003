# Cycle 209: explicit Heegner trace coefficient modulo `7`

## Hostile-audit verdict

On the global minimal curve

\[
 E:y^2+xy+y=x^3-46813x-3372156843,
 \qquad N=433\cdot1499^2,
\]

let

\[
 P=\left(\frac{399030891253207}{156180668809},
 \frac{7009131418974188521075}{61722131771310373}\right).
\]

The numerical PARI run reports auxiliary discriminant `D=-115`, hence

\[
 K=\mathbf Q(\sqrt{-115}).
\]

The field arithmetic is exact. The fundamental discriminant is `-115`, the
class number is `2`, and `gcd(115,N)=1`. Both conductor primes split:

\[
 54^2\equiv-115\pmod {433},\qquad
 431^2\equiv-115\pmod {1499}.
\]

Indeed `-115` is a square modulo `4N`; one root is `2219057073 mod 4N`.
Thus the classical `X_0(N)` Heegner hypothesis holds. The exponent two at
`1499` introduces no additional inertness condition once `1499` splits.

The trace claim has a different status. PARI's floating
modular-parametrization and Gross--Zagier computation reports
`Index^2 = 63.996...`, rounds this to `ind=8`, and recognizes the
index-divided rational point as `+/-P`. Under that numerical recognition, the
candidate class-group trace is

\[
 y_K^{\mathrm{PARI}}=\mathord{+/-}8P,
 \qquad 8\equiv1\pmod 7.
\]

This is not a rigorous certificate that the mathematical Heegner trace equals
`+/-8P`. Consequently this artifact does not rigorously prove that the
mathematical Heegner index is prime to `7`.

## PARI normalization audit

The factor bookkeeping is clear from the source. For trivial rational torsion,
PARI's `heegner_find_disc` numerically estimates the square of the quotient of
the class-group Heegner sum by the point of predicted BSD height and rounds its
square root to `ind`. It then sets the lattice-search multiplier to
`indx=2*ind`. The extra factor `2` removes the conjugation/torsion ambiguity;
it is not another trace-index factor. Thus, for the reported `ind=8`, `16` is
the lattice-search multiplier and `8` is PARI's candidate trace quotient.

The subsequent descent searches for an exact rational point of the predicted
height whose multiple agrees numerically with the computed elliptic logarithm.
The returned coordinates are exact rationals, but exactness starts only after
the floating recognition. It does not make the provenance of the point or the
rounded value `ind=8` exact. Newer PARI source exposes the internal operation
through the library-only `ellheegner_z` contract: `[z,n]` represents `[n]P`.
That contract explains the multiplier; it does not certify its floating
inputs.

Conditionally on PARI's producer, undoing only the index division gives
`y_K=+/-8P`. Trivial rational torsion rules out a remaining rational torsion
translation. Reversing complex orientation changes the sign, which is
irrelevant modulo `7`.

Exact finite-field arithmetic gives

\[
 P\bmod7=(6,5),\qquad 8P\bmod7=(4,2),
 \qquad \#E(\mathbf F_7)=5.
\]

Moreover `P mod 7` has order `5`. This checks exact multiplication of the
candidate and shows that the hard-coded coefficient `8` is nonzero modulo
`7`. It does not check that `8` is the true trace coefficient.

## Scope

Cycle 195's Cremona--Siksek calculation gives `P=+/-G` for a primitive
generator `G`, subject to its separate nondirected eclib `bigfloat` trust
boundary. If the PARI trace identification is correct, then

\[
 [E(\mathbf Q)/E(\mathbf Q)_{tors}:\mathbf Z y_K]=8.
\]

Neither this conditional conclusion nor the weaker assertion that the trace
coefficient relative to `P` is a `7`-adic unit is proved by this computation.
This file therefore does not close a rigorous Heegner-index gate and is not an
independent Heegner-primitivity certificate. It is numerical corroboration of
the separate Cycle 209 Kurihara/Selmer seven-part result, which does not depend
on this file.

## Reproduction and missing certificate

Run:

```sh
gp -fq -s 4G millennium-prize/birch-swinnerton-dyer/verify_cycle209_heegner_trace.gp
```

The expensive step is `ellheegner`. The script checks the returned rational
coordinates and exact downstream group arithmetic, but it hard-codes `8`; it
neither extracts nor certifies PARI's internal index.

The field, rational-point, and finite-field checks are fail-closed. The link
between the class-group trace and `8P` remains a nondirected floating
computation: `63.996...` being close to `64` is not a proof that the
Gross--Zagier expression equals `64`, and exact recognition of a rational point
does not prove that the approximated logarithm is its exact logarithm.

A rigorous replacement needs either:

1. directed error bounds for the modular parametrization and every
   Gross--Zagier/L-value factor, including an isolating interval proving the
   integer index is exactly `8`; or
2. an exact algebraic construction and trace of the CM point, followed by an
   exact Mordell--Weil comparison.

Until one of these is supplied, `y_K=+/-8P` is numerical/conjectural rather
than rigorous.
