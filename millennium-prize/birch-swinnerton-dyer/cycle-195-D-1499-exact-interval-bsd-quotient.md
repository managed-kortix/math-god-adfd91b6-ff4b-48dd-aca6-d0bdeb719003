# Cycle 195: exact generator and interval BSD quotient for `D=-1499`

## Certified data

On the global minimal model

\[
 E:y^2+xy+y=x^3-46813x-3372156843
\]

the exact point is

\[
 P=\left(\frac{399030891253207}{156180668809},
 \frac{7009131418974188521075}{61722131771310373}\right).
\]

Exact substitution verifies `P in E(Q)`. Exact PARI local arithmetic gives

\[
 E(\mathbf Q)_{\rm tors}=0,\qquad
 c_{433}=1,\quad c_{1499}=2,\quad \prod_p c_p=2.
\]

The reduction records are `[1,5,[1,0,0,0],1]` at `433` and
`[2,-1,[1,0,0,0],2]` at `1499`. The conductor is
`433*1499^2=972951433`, the minimal discriminant is
`-4912444914224609853433`, and the exact root number is `-1`.

The independent Arb replay, converted outward to rational denominator
`10^50`, proves

\[
\frac{6258249033705717664048725789876108131610965835281}{10^{50}}
 < \Omega_E <
\frac{6258249033705717664048725789876108131610965835282}{10^{50}},
\]

where `Omega_E` is the real Neron period, and

\[
\frac{3396338096796685137401217818912911624353760513342938}{10^{50}}
 < \widehat h(P) <
\frac{3396338096796685137401217818912911624353760513342939}{10^{50}}.
\]

The period uses certified roots of

\[
4x^3+x^2-187250x-13488627371
\]

and Carlson's `R_F`. The height replay follows PARI's AGM archimedean-height
algorithm. Exact rational arithmetic finds
`gcd(numerator(psi_2(P)),numerator(phi_2(P)))=1`, so the finite local correction
sum in that algorithm is empty. PARI's independent 100-digit `ellheight`
value lies in the resulting interval.

Cycle 193 supplies the rigorous rational derivative interval

\[
\frac{425055458712371550288205049784482504359146782438892}{10^{50}}
 < L'(E,1) <
\frac{425182303658182754137303934460410663840644112448588}{10^{50}}.
\]

## BSD point quotient

Define the point-normalized leading-term quotient

\[
 Q_P=\frac{L'(E,1)|E(\mathbf Q)_{\rm tors}|^2}
 {\Omega_E(\prod_p c_p)\widehat h(P)}.
\]

Outward rational division gives

\[
\frac{3542128822603096252401708748204020869659556520324100000000000000000000000000000000000000000000000000}
 {3542521602069295157789615887132856839075485197706721293059415462763512034051382759138227805375295633}
 <Q_P<
\frac{3543185863818189617810866120503422198672034270404900000000000000000000000000000000000000000000000000}
 {3542521602069295157789615887132856839075485197706154193668443730954334489627265627849480243462099263}.
\]

In decimals this is contained in

\[
 0.9998891243271545<Q_P<1.0001875109945714.
\]

Under the refined rank-one BSD leading-term formula only, if
`m=[E(Q)_free:ZP]`, then

\[
 Q_P=\frac{|\Sha(E)|}{m^2}.
\]

This interval isolates `1` among integers. That observation cannot be applied
to `Q_P`, because `Q_P` is not known unconditionally to be an integer: the
conditional formula involves the rational ratio `|Sha|/m^2`, not the product
`|Sha|m^2`. Even after imposing the refined BSD identity and the unconditional
Cycle 193 finiteness of `Sha`, the interval alone does not isolate the pair
`(|Sha|,m)` or prove saturation. It is consistent with `|Sha|=1,m=1`; it does
not prove either statement. Indeed `Q_P=1` would also be compatible with
`|Sha|=9,m=3`, and similarly with other equal square factors. Cycle 192
separately proves `Sha[2]=0`, which does not close these odd-index and
odd-primary alternatives.

Thus the quotient interval by itself proves the arithmetic inputs and
intervals, not the refined BSD formula, the order of `Sha`, or saturation.

## Full Tate--Shafarevich audit

The strongest unconditional conclusion from the present artifacts is

\[
 \Sha(E/\mathbf Q)\ \text{is finite},\qquad
 \Sha(E/\mathbf Q)[2^\infty]=0,
 \qquad |\Sha(E/\mathbf Q)|\ \text{is an odd square}.             \tag{195.1}
\]

Here finiteness follows from Cycle 193's certified analytic rank one and the
Gross--Zagier--Kolyvagin theorem. The Kummer sequence and the certified
2-Selmer computation give

\[
 0\longrightarrow E(\mathbf Q)/2E(\mathbf Q)
 \longrightarrow \operatorname{Sel}^{(2)}(E/\mathbf Q)
 \longrightarrow \Sha(E/\mathbf Q)[2]\longrightarrow0.
\]

Both of the first two vector spaces have dimension one, so `Sha[2]=0`. A
nonzero finite 2-primary group always has an element of order two; hence the
entire 2-primary part vanishes, not just its order-two subgroup. Finally, the
Cassels--Tate pairing on the now finite `Sha` is nondegenerate and alternating
for this principally polarized elliptic curve. Therefore every primary order
has even valuation. Combining this with the 2-descent proves (195.1): if
`Sha` is nontrivial, every prime divisor is odd and occurs in its order with
positive even exponent.

No odd prime divisor is proved to occur, and no odd prime is excluded by the
committed descent. A 2-descent cannot see odd-primary classes. The
Gross--Zagier--Kolyvagin theorem used for finiteness supplies a bound in terms
of a Heegner/Kolyvagin index and theorem-dependent local factors, but the
present certificate does not construct the normalized Heegner trace or
compute that index. The fact that `P` is a saturated rational generator is not
an identification of `P` with a primitive Heegner trace, so it does not turn
the qualitative Kolyvagin theorem into the numerical bound `|Sha|=1`.

Likewise, a proved `p`-part BSD formula would determine `v_p(|Sha|)` because
the generator, torsion, and Tamagawa factors are now known. The real interval
for `Q_P`, however, is not a proof of any odd `p`-part formula and does not
determine a `p`-adic valuation. No curve-specific verification of the
hypotheses and normalizations of a published odd-prime BSD theorem is included
in this cycle. It would be circular to round `Q_P` to one and call that a BSD
`p`-part computation.

Consequently the exact answer to the requested triviality question is:

\[
 \boxed{\Sha(E/\mathbf Q)=1\ \text{is strongly predicted but is not proved by
 these artifacts}.}
\]

The only rigorously determined information about prime divisors of its order
is that `2` is absent; any hypothetical divisor is an odd prime, with even
valuation in the order.

## Generator calculation and numerical scope

There is nevertheless a separate route to saturation, independent of BSD. It
uses the certified 2-descent and the Cremona--Siksek canonical-height bound.
The exact component-group and divisibility steps are unconditional. The
present replay of the lower-height constant uses eclib `bigfloat` arithmetic,
however, and is not a directed-interval implementation; the final generator
claim therefore retains that numerical-library trust assumption.

Cycle 193 certifies

\[
 \dim_{\mathbf F_2}\operatorname{Sel}^{(2)}(E/\mathbf Q)=1,
 \qquad E(\mathbf Q)[2]=0.
\]

The displayed point represents a nonzero Mordell--Weil class modulo `2`.
This can be checked in either of two exact ways. It is the image, up to sign,
of the exact rational point

\[
 (1367/2987,592400303/8922169)
\]

on the unique nontrivial everywhere locally soluble 2-cover recorded in Cycle
192. Independently, eclib's exact division-polynomial routine returns an empty
list of rational halves of `P`. Hence, if `G` generates the rank-one free
quotient and `P=mG`, then `m` is odd. This is the 2-saturation step.

For odd primes, eclib 20231211 applies the Cremona--Siksek ANTS VII lower
height bound to the everywhere-good-reduction subgroup. The verifier now
replays the calculation at 200 and 300 decimal digits and gives

```text
CANONICAL_HEIGHT=33.963380967966851374012178189129116243537605133429...
RATIONAL_HALVES_OF_P=[ ]
TWO_SATURATION=PROVED
COMPONENT_PLACE=433 GROUP=[1] EXPONENT=1 P_IMAGE=[[0]]
COMPONENT_PLACE=1499 GROUP=[2,2] EXPONENT=2 P_IMAGE=[[0,0]]
COMPONENT_PLACE=REAL GROUP=[1] EXPONENT=1 P_IMAGE=[[0]]
GLOBAL_COMPONENT_GROUP_EXPONENT=2
INDEX_OF_EGR_SUBGROUP_IN_ZP=1
ECLIB_BIGFLOAT_EGR_HEIGHT_BOUND_PRECISION_200=7.3192919957294903386...
ECLIB_BIGFLOAT_EGR_HEIGHT_BOUND_PRECISION_300=7.3192919957294903386...
ECLIB_BIGFLOAT_BOUND_SCOPE=not_a_directed_interval; strict_comparison_replayed_at_200_and_300_digits
SATURATOR_GET_INDEX_BOUND_RESULT=2
CANDIDATE_ODD_SATURATION_PRIMES=[ ]
ODD_SATURATION_CONCLUSION=subject_to_eclib_bigfloat_ANTS_bound
PASS_WITH_STATED_BIGFLOAT_SCOPE
```

The inequalities needed for the certificate are only

\[
 \widehat h(P)<34,
 \qquad \widehat h(R)>7
\]

for every non-torsion point `R` in the everywhere-good-reduction subgroup.
The printed local groups, exponents, and point images check rather than assume
the component assertion. Their global exponent is `2`. Since `m` is odd and
`P=mG` maps to zero, multiplication by `m` is invertible on every component
group, so `G` also maps to zero. Quadraticity of canonical height then gives

\[
 7<\widehat h(G)=\frac{\widehat h(P)}{m^2}<\frac{34}{m^2}.
\]

Thus `m^2<34/7<5`. Since `m` is a positive odd integer, `m=1`. This is the
direct mathematical argument once the ANTS lower bound `>7` is accepted. It
must not be conflated with `saturator::get_index_bound()`: that separate eclib
routine returns the integer `2`, interpreted as an upper bound for possible
saturation primes, so its prime loop has no odd candidate. The two routes
agree, while descent excludes `2`. Subject to the stated eclib numerical
assumption, they give

\[
 \boxed{E^{(-1499)}(\mathbf Q)=\mathbf ZP_{1499}}
\]

because the rational torsion subgroup is trivial. This argument uses neither
BSD nor the Cycle 193 analytic-rank certificate. A fully directed replay of the
ANTS constant would remove the remaining numerical-library qualification. The
BSD quotient interval remains useful only as an independent consistency check;
it still does not determine `|Sha|`.

## Reproduction

Run

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/verify_cycle195_exact_data.gp
uv run --with python-flint python3 millennium-prize/birch-swinnerton-dyer/verify_cycle195_exact_interval.py
g++ -O2 -std=c++17 millennium-prize/birch-swinnerton-dyer/verify_cycle195_generator.cpp -o /tmp/verify_cycle195_generator -lec -lntl -lpari
/tmp/verify_cycle195_generator
```

The GP script checks the exact model, point, torsion, local data, Tamagawa
product, and an independent height reference. The Python verifier uses Arb
balls for the period and archimedean height, emits outward rational endpoints,
pins those endpoints, combines them with Cycle 193's pinned rational derivative
interval, and verifies that the quotient interval isolates `1` among integers
while explicitly refusing the unavailable integrality premise. The C++
verifier requires the eclib, NTL, and PARI development libraries. It checks
the exact projective point and absence of rational halves, computes the ANTS
VII lower-height and saturation-index bounds, prints every finite and real
component group, exponent, and image of `P`, checks `height(P)<34`, and replays
the non-directed `bigfloat` comparison `lambda>7` at two precisions. The public
eclib 20231211 API exposes `CurveHeightConst::get_value()` as a `bigfloat`, not
as directed endpoints, so no directed ANTS interval is claimed here.

The reference environment reports eclib API version `20231211`, Ubuntu package
`libec-dev=20231212-1.1build2`, and
`sha256(/usr/lib/x86_64-linux-gnu/libec.so.10.3.0) =
5c6b5a684cdb531c22eb04204ae4809f38d879270c3cd25b7665eec68f431e09`.
These metadata pin the tested binary, not a portable proof that another build
has identical floating-point behavior.
