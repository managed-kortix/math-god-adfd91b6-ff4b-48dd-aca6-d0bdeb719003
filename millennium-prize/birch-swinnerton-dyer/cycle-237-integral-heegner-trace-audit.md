# Cycle 237: exact integral Heegner trace audit for `HK236`

## Verdict

The classical Heegner datum for

\[
 A=433\mathrm a1^{(-1499)}:
 y^2+xy+y=x^3-46813x-3372156843,
 \qquad K=\mathbf Q(\sqrt{-115})
\]

passes exact arithmetic checks, but the requested integral trace cannot be
certified from the available data. The terminal obstruction occurs before an
exact rational coordinate can be assigned to the CM trace: neither an exact
evaluation of the optimal modular parametrization at the CM divisor nor a
directed analytic isolation of that value is present. PARI's candidate
`y=+/-8P` is deliberately not promoted.

Thus `HK236` item 1 fails closed. This is a terminal obstruction for the frozen
curve/field architecture, not evidence that the mathematical trace does not
exist.

## Exact checks that pass

The conductor is

\[
 N=433\cdot1499^2=972951433,
\]

the minimal discriminant is `-4912444914224609853433`, the root number of `A`
is `-1`, and `A(Q)_tors=0`. Its Neron differential on the displayed global
minimal equation is

\[
 \omega_A=\frac{dx}{2y+x+1}.
\]

The discriminant `-115` is fundamental, coprime to `N`, and has class number
two. Both conductor primes split, with exact witnesses

\[
 54^2\equiv-115\pmod {433},\qquad
 431^2\equiv-115\pmod {1499}.
\]

The stronger level condition is witnessed by

\[
 2219057073^2\equiv-115\pmod {4N}.
\]

Reducing this root modulo `2N` gives `b=273154207` and the primitive CM form

\[
 [N,b,c]=[972951433,273154207,19171877],
 \qquad b^2-4Nc=-115.                                      \tag{237.1}
\]

Its reduced class is `[5,5,7]`; squaring gives the principal form `[1,1,29]`.
This supplies an exact oriented CM datum and verifies the classical
`X_0(N)` Heegner hypothesis. It does not evaluate its image on `A`.

The exact reference point is

\[
 P=\left(\frac{399030891253207}{156180668809},
 \frac{7009131418974188521075}{61722131771310373}\right)\in A(\mathbf Q).
                                                               \tag{237.2}
\]

Cycle 195 supplies the directed real-period enclosure

\[
\frac{6258249033705717664048725789876108131610965835281}{10^{50}}
 <\Omega_A<
\frac{6258249033705717664048725789876108131610965835282}{10^{50}}.
                                                               \tag{237.3}
\]

This is the real Neron period for the differential above. It is sufficient to
pin the period convention, but not to identify a CM image.

## Auxiliary rank-zero factor

Twisting `A` by the character of `K` gives the global minimal model

\[
 A^{(-115)}:[1,1,1,-619095588,5128622847262406]
\]

of conductor `12867282701425` and exact root number `+1`. Relative to the base
curve `433a1`, this is the positive quadratic twist by
`1499*115=172385`. Exact level-433 plus modular symbols give

\[
 \sum_{a\bmod172385}
 \left(\frac{172385}{a}\right)
 [a/172385]^+_{433\mathrm a1}=64.                            \tag{237.4}
\]

The quadratic-twist Fourier identity expresses the central value as a nonzero
Gauss-sum and period factor times (237.4). Hence

\[
 L(A^{(-115)},1)\ne0
\]

exactly, so the auxiliary twist has analytic rank zero. This proof needs no
decimal recognition and does not depend on the exact period or Manin scaling:
those factors are nonzero. PARI's numerical value near
`0.6496776924156105724` is only a consistency check and is not used.

## Parametrization and Manin audit

The base curve `433a1` has an audited strong-Weil parametrization of degree 28
and Manin constant one. Those facts do not automatically certify that the
displayed high-conductor quadratic-twist model is the optimal quotient in its
isogeny class, nor do they determine the integral pullback

\[
 \pi_A^*\omega_A=c_A(2\pi i f_A(z)\,dz)
\]

with an exact signed integer `c_A`. An exact optimal-quotient/isogeny audit and
twist-side Manin constant are absent. Cycle 188 proves the Neron differential
comparison factor is one for the twist by `-1499`; that settles the twist
period scaling, not the high-level modular-parametrization lattice.

Consequently the divisor

\[
 D_K=\sum_{[\mathfrak a]\in\operatorname{Cl}(\mathcal O_K)}
       ([\mathfrak a]\cdot z_{(237.1)}-\infty)
\]

is exact as a degree-zero CM divisor over the Hilbert class field, but the
quantity `Tr(pi_A(D_K))` is not yet an integrally normalized point with audited
rational coordinates.

## Why `+/-8P` is rejected

PARI's `ellheegner` computation first obtains floating modular integrals and a
Gross--Zagier estimate `Index^2=63.996...`, rounds to index eight, and then
recognizes an exact rational point. Exactness of the final coordinates checks
only the recognized point. It does not prove that the floating CM logarithm is
the logarithm of that point or that the rounded integer is eight.

Conditional on that producer, the trace would be `+/-8P`; all group operations
afterward are exact. This audit forbids that nondirected recognition step, so
neither sign choice nor the coordinates of `8P` are a certificate for `y`.

The missing certificate must be one of:

1. exact algebraic evaluation of the optimal parametrization on both CM
   conjugacy classes, exact field trace, and exact Mordell--Weil comparison; or
2. directed complex modular integration and Gross--Zagier factors with an
   isolating elliptic-logarithm region proving both the rational point and the
   integer index, together with the optimal/Manin normalization audit.

The committed repository contains neither route. This obstruction is prior to
the later integral Kolyvagin factor and directed global lower-height gates.

## Reproduction

Run the exact, nonrecognition verifier:

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/verify_cycle237_heegner_datum.gp
```

It uses PARI only for exact curve, quadratic-form, root-number, and modular
symbol arithmetic. The exact central modular-symbol computation evaluates
172385 residue classes and may take several seconds. It does not call
`ellheegner`, `ellidentify`, lattice reduction on floating logarithms, or
numerical point recognition. Its terminal lines mark the three absent
certificates explicitly.

No exact Heegner-trace coordinates are claimed, and no Millennium problem is
claimed solved.
