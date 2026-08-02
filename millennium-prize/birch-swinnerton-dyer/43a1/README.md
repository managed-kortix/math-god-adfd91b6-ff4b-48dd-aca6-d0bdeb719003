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
gp -fq millennium-prize/birch-swinnerton-dyer/43a1/verify_dminus7_cm_exact.gp \
  | tee millennium-prize/birch-swinnerton-dyer/43a1/output-dminus7-exact.txt
gp -fq millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1_K.gp \
  | tee millennium-prize/birch-swinnerton-dyer/43a1/output-K.txt
printf '0 1 1 0 0\n' | mwrank -v 2 -p 1000
```

The retained transcripts are `output-K.txt` and
`output-mwrank-saturation.txt`.

Optional independent backends are supplied but were not run here:

```sh
sage millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1.sage
magma millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1.m
```

The focused exact 2-descent certificate and checkers are in
`2descent-certificate.md`, `verify_43a1_2descent.gp`, and
`verify_43a1_2descent.m`.  The GP checker is runnable in this environment;
the Magma checker exposes the full Selmer group, Kummer map, relevant primes,
local maps, and explicit cover basis for an independent replay.

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
| group over `K=Q(sqrt(-7))` | `E(K)_tors=0`, `E(K)_free=Z P` | exact `-7`-twist 2-descent gives twist rank zero; prime-to-residue-characteristic reduction at 2 and 3 eliminates odd torsion, while the irreducible cubic gives `E(K)[2]=0`; hence `E(K)=E(Q)`, and eclib's full saturation gives `E(Q)=Z P` |
| Heegner, `D=-7` | the class-number-one CM point maps exactly to `(0,0)` | exact formal-`q` reconstruction of the descended trace and norm of the two `j`-invariants, followed by integer-resultant fiber elimination; see Cycle 261 |
| mod-p images | maximal for every prime `p` | proved without image-database input in Cycle 261 by the semistable reducibility lemma plus Mazur torsion, Tate inertia, Dickson classification, and exact small-prime witnesses |

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
subgroup. PARI's point `Q=(-3/4,1/8)` satisfies `Q=5P`, while direct
`ellisdivisible` checks exclude division of `P` by 2, 3, and 5. Eclib's full
Mordell--Weil calculation supplies the missing all-prime saturation: at
1000-bit precision it returns `[0:-1:1]=-P`, says the basis is already
saturated, and states that the full basis has been determined unconditionally.
The identification is therefore not taken from Cremona/LMFDB.

Over `K=Q(sqrt(-7))`, the exact `-7`-twist descent proves rank zero for the
anti-invariant part. Exact reductions give `#E(F_2)=5` (2 split) and
`#E(F_9)=12` (3 inert), eliminating odd torsion; the irreducible rational
2-division cubic remains irreducible over the quadratic field `K`, eliminating
2-primary torsion. Thus `E(K)_tors=0`. For every `Q in E(K)`, the
anti-invariant point `Q-sigma(Q)` is then both torsion and zero; hence
`E(K)=E(Q)=ZP`. See `K-mordell-weil-certificate.md`. This proves the literal
index `[E(K)_free:Z y_K]=1` after the exact CM certificate identifies `y_K=P`.

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

The independent Cycle 261 certificate upgrades this numerical recognition.
It reconstructs `j(z)+j(43z)` and `j(z)j(43z)` exactly as rational functions
on the optimal quotient from formal `q`-series. It also verifies the `+1`
Fricke eigenvalue, the positive differential normalization, trivial rational
torsion, equality of the reduced quadratic-form classes for `tau` and
`43*tau`, independent Riemann--Roch uniqueness coefficients, and the exact
gcd of three nonzero resultants. Substitution of `H_-7(T)=T+3375` then isolates
the unique point `(0,0)`. See `verify_dminus7_cm_exact.gp` and
`../cycle-261-43a1-dminus7-exact-cm-certificate.md`.

## Mod-p images

Cycle 261 now supplies the missing proof-grade all-prime argument. See
`../cycle-261-43a1-all-prime-residual-surjectivity.md` and reproduce its finite
checks with

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle261_43a1_residual.py
```

It proves `im(rho_bar_E,p)=GL(2,F_p)` for every prime, using no image database:
the semistable reducibility-to-rational-torsion lemma and Mazur's torsion
theorem close `p>=11` (not the general isogeny-degree list alone); exact Frobenius
discriminants close irreducibility at `3,5,7`; multiplicative `I_1` inertia at
43 supplies a transvection for every `p`; Dickson's classification closes
`p>=7`; and exhaustive exact matrix checks close `p=3,5`. The irreducible
2-division cubic of nonsquare discriminant closes `p=2`.

### Prior database evidence

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

Items 1--4 were formerly only evidence. They are now supplemented by the
Cycle 261 theorem argument; the optional Sage and Magma image commands remain
cross-checks and are not proof inputs.

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
