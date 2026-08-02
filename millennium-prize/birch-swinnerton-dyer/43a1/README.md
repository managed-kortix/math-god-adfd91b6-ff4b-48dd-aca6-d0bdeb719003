# 43a1 independent arithmetic packet

This packet starts from the integral equation

\[
E:\quad y^2+y=x^3+x^2
\]

and does not use a curve label in its primary computations.  The label `43a1`
is checked separately against PARI's optional `elldata` table and the LMFDB.

## Reproduction

The tools installed in the present environment are Python 3.12.13 and
PARI/GP 2.15.4.  Reproduce the available runs with

```sh
python3 millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1_exact.py \
  | tee millennium-prize/birch-swinnerton-dyer/43a1/output-exact.txt
gp -fq millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1.gp \
  | tee millennium-prize/birch-swinnerton-dyer/43a1/output-pari.txt
```

Optional independent backends are supplied but were not run here:

```sh
sage millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1.sage
magma millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1.m
```

## Conclusions and status

| Item | Result | Status in this packet |
|---|---|---|
| model | `[0,1,1,0,0]` | input, exact |
| discriminant, conductor | `-43`, `43` | exact PARI calculation; independently the displayed equation has discriminant `-43` |
| local data at 43 | Kodaira `I_1`, nonsplit multiplicative, `c_43=1` | exact Tate-algorithm output; nonsplit also follows from `a_43=-1` |
| point | `P=(0,0)` | exact substitution |
| rational torsion | trivial | proof: reductions at good primes 2 and 3 have orders 5 and 6, so torsion order divides `gcd(5,6)=1` |
| rank | 1 | PARI exact 2-descent returns `[1,1]`, and `P` supplies the lower bound |
| 2-Selmer | dimension 1 | interpretation of PARI's complete 2-descent: one nonzero locally soluble cover, together with trivial `E(Q)[2]`; Sage/Magma scripts request independent implementations |
| generator | `P=(0,0)` | PARI's descent point is `[-3/4,1/8]=5P`; `P` is a primitive generator once the rank-one 2-descent/saturation result is accepted; direct tests show no division by 2, 3, or 5 |
| Heegner, `D=-7` | the class-number-one CM point maps numerically to `(0,0)`; `ellheegner` returns `(0,0)` | Heegner hypothesis exact, modular parametrization numerical/arbitrary precision, final rational point exactly verified; not a symbolic CM evaluation certificate |
| mod-p images | maximal for every prime `p` | LMFDB/Sutherland-Zywina database theorem-backed data; this packet independently supplies Frobenius traces and absence of rational isogenies as evidence, not a proof of all images |

### Rank and 2-Selmer caution

PARI reports

```text
ellrank(E,4,[P]) = [1,1,0,[[-3/4,1/8]]]
ell2cover(E) has one basis element
R(x) = x^4-2*x^2+4*x+1.
```

The Kummer sequence is

\[
0\longrightarrow E(\mathbf Q)/2E(\mathbf Q)
 \longrightarrow \operatorname{Sel}^{(2)}(E/\mathbf Q)
 \longrightarrow \Sha(E/\mathbf Q)[2]\longrightarrow0.
\]

Since `P` is nontorsion and `E(Q)[2]=0`, a one-dimensional 2-Selmer group gives
rank one and `Sha[2]=0`.  PARI's `ell2cover` documentation says it returns a
basis of the everywhere locally soluble 2-covers; this is an algorithmic exact
descent claim, not database lookup.  For a proof audit requiring independently
certified class- and unit-group subroutines, rerun the Sage `proof=True` and
Magma `TwoSelmerGroup` alternatives and retain their transcripts.

The 2-descent alone proves only odd saturation of the visible rank-one
subgroup.  PARI's point `Q=(-3/4,1/8)` satisfies `Q=5P`, while direct
`ellisdivisible` checks exclude division of `P` by 2, 3, and 5.  A fully general
generator proof is supplied by the complete Mordell--Weil/saturation routines
requested in the Sage and Magma alternatives.  The identification of `P` as
the generator is also database data in Cremona/LMFDB, but database agreement is
not substituted for saturation.

## Heegner point with discriminant -7

The exact checks are

\[
h(-7)=1,\qquad \left(\frac{-7}{43}\right)=1,
\qquad 37^2+7=4\cdot43\cdot8.
\]

Thus 43 splits in `K=Q(sqrt(-7))`, and

\[
\tau=\frac{-37+\sqrt{-7}}{86}
\]

defines the unique class-number-one Heegner orbit on `X_0(43)`.  The GP script
computes the modular logarithm

\[
z=\sum_{n\ge1}\frac{a_n}{n}e^{2\pi i n\tau}
\]

from coefficients counted directly from `E`; applying the complex
uniformization gives `(0,0)` to the displayed precision.  PARI's independent
`ellheegner(E)` implementation also returns the exact point `(0,0)`.

What is proved exactly here is the Heegner hypothesis and that the rational
output lies on `E`.  The equality between the CM divisor's modular image and
that output is obtained through rapidly convergent floating-point evaluation,
not interval arithmetic or a symbolic algebraic CM certificate.  It is strong
reproducible evidence, and enough to recover the candidate, but should not be
mislabelled as an exact proof of the modular parametrization evaluation.

## Mod-p images

LMFDB release 1.2.1 records `nonmax_primes=[]`: every prime-adic image is
maximal, and records an adelic image of index 2 and level 86.  These are
database assertions based on published image-classification algorithms, not
derived by the local scripts.

The packet's exact independent evidence is narrower:

1. `j=-4096/43` is nonintegral, so the curve has no CM.
2. `ellisomat` finds no nontrivial rational isogeny.
3. The irreducible 2-division cubic `4x^3+4x^2+1`, whose discriminant is
   `-16*43`, has Galois group `S_3`; hence the mod-2 image is `GL(2,F_2)`.
4. Exact point counts through 97 provide Frobenius characteristic polynomials
   `T^2-a_q T+q`, useful as reproducible witnesses against proposed exceptional
   images for any fixed `p`.

Items 1--4 do **not** by themselves prove surjectivity for every prime.  A
proof-grade all-prime statement needs an effective exceptional-prime theorem
plus subgroup elimination, or a trusted Sage/Magma implementation.  The Sage
script asks `non_surjective()` and per-prime `image_type`; the Magma script asks
`GaloisRepresentation` through 47.  Their outputs should be described as
theorem-backed software computations, with the exact software version retained.

## Database comparison

PARI's optional table returns

```text
ellsearch("43a1") = ["43a1", [0,1,1,0,0], [[0,0]]]
```

LMFDB 43.a1 records rank 1, trivial torsion, generator `(0,0)`, Tamagawa
product 1, analytic rank 1, analytic `|Sha|=1`, no nonmaximal primes, modular
degree 2, and Manin constant 1.  These are useful checks but are not inputs to
the exact model/descent/local calculations.

The numerical `ellanalyticrank` and BSD leading-term agreement in
`output-pari.txt` are corroboration only.  PARI decides analytic vanishing by a
floating-point threshold, and no claim here relies on that output.
