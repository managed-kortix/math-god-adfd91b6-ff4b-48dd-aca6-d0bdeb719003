# Cycle 209: the seven-part for `D=-1499`

## Result

Let

\[
 A=E_0^{(-1499)}:\quad
 y^2+xy+y=x^3-46813x-3372156843,
 \qquad E_0=433\mathrm a1.
\]

Subject to the theorem trust boundaries below, the exact one-prime Kurihara
certificate proves

\[
 \operatorname{Sel}(\mathbf Q,A[7])\simeq\mathbf F_7,
 \qquad \Sha(A/\mathbf Q)[7^\infty]=0.                 \tag{209.1}
\]

The ordinary rank-one theorem `corA'` of
Burungale--Skinner--Tian--Wan (BSTW) then gives the requested valuation

\[
 \boxed{
 v_7\!\left(\frac{L'(1,A)}{\Omega_A R(A/\mathbf Q)}\right)=0
 }
 \qquad\text{and}\qquad
 \boxed{v_7(\#\Sha(A/\mathbf Q))=0}.                  \tag{209.2}
\]

There is no rounding of a real `L`-value, period, height, or BSD quotient in
this argument.  In particular, (209.1) does not use the Cycle 195
non-directed eclib height bound or its generator conclusion.

## What is, and is not, being evaluated exactly

Write

\[
        \mathcal L_A=\frac{L'(1,A)}{\Omega_A R(A/\mathbf Q)}.
\]

The practical exact target is the discrete invariant `v_7(L_alg)`, where
`L_alg=mathcal L_A`, not a decimal approximation to `L_alg` and not the full
rational number.
The modular-symbol route below computes the finite 7-Selmer group exactly;
BSTW then converts that answer into `v_7(L_alg)=0`.  Thus no exact real
period or canonical-height evaluation enters the valuation certificate.

There is also an unconditional algebraicity route in rank one.  Choose an
imaginary quadratic field satisfying the Heegner hypothesis for `A`, with the
quadratic twist of analytic rank zero.  Gross--Zagier expresses a product of
`L'(A,1)` and that rank-zero central value as the Neron--Tate height of a
normalized Heegner trace, with explicit rational local, period, Manin, and
parametrization factors.  If `G` is a Mordell--Weil generator and the trace is
`mG`, then its height is `m^2 R(A/Q)`.  The modular-symbol formula for the
auxiliary central value is algebraic.  After every normalization is fixed,
this proves that `L_alg` is rational and reduces its exact evaluation to
an exact Heegner index `m` and exact rational modular-symbol data.

That route is not made automatic by knowing the modular degree.  The modular
degree controls the polarization/composition of the optimal parametrization
and is one normalization factor in a Gross--Zagier formula; it does not
determine the image, trace, or index of a CM divisor.  Computing `m` requires
constructing the normalized Heegner trace (or an equivalent Kolyvagin-index
certificate) and comparing it with `G`.  None of this is needed for the
seven-adic valuation because the one-prime Kurihara certificate is strictly
shorter.

## Exact Kurihara certificate

Take the genuine Kolyvagin prime `ell=29` and primitive root `eta=2`.  Exact
point counting gives

\[
 \#A(\mathbf F_{29})=28,\qquad a_{29}(A)=2,
\]

so `29=1 mod 7` and `a_29(A)=29+1 mod 7`.  Cycle 187's exact twist identity,
with the globally minimal differential comparison `kappa_1499=1`, converts
the fixed-level-433 symbols into the plus symbols of `A`.  The 28 exact rows
in `cycle188_base_twist_sums.tsv` give

\[
 \widetilde\delta^{(1)}_{29}(A)
 =\sum_{a=1}^{28}\log_2(a)[a/29]^+_A
 =-150\equiv4\pmod7.                                  \tag{209.3}
\]

All row denominators are `1` or `2`; reduction modulo seven is therefore
defined.  The equality is an exact rational modular-symbol calculation, not
an approximation to a complex leading term.

The displayed rational point

\[
 P=\left(\frac{399030891253207}{156180668809},
 \frac{7009131418974188521075}{61722131771310373}\right)
\]

reduces at `29` to `(0,11)` and has exact order `28` in `A(F_29)`.  Hence its
image in `A(F_29)/7A(F_29)` is nonzero.

## Selmer deduction

Apply Chan-Ho Kim, *The structure of Selmer groups and the Iwasawa main
conjecture for elliptic curves*, arXiv:2203.12159v6, Theorems 1.8 and 1.10.
The required inputs are:

1. `p=7>=5`, the residual representation is surjective, and the Manin
   constant is prime to seven;
2. `A(Q_7)[7]=0`: the good-reduction exact sequence has torsion-free formal
   kernel over `Q_7`, while `#A(F_7)=5`;
3. every Tamagawa number is a seven-unit: `c_433=1`, `c_1499=2`;
4. (209.3) is nonzero.

For residual surjectivity, Cycle 185 certifies
`rho_(E_0,7)(G_Q)=GL_2(F_7)`.  The quadratic character of `Q(sqrt(-1499))` is
ramified at `1499`, while `Q(E_0[7])` is unramified there.  It is therefore
independent of the base mod-seven field.  Multiplying the full image by this
independent scalar character leaves the twist image equal to `GL_2(F_7)`.
Kim explicitly notes that the Manin-constant assumption is vacuous when the
curve has semistable reduction at `p`; here `A` has good, hence semistable,
reduction at seven.  The analytic Neron-period normalization in the actual
Kurihara sum is checked independently in Cycles 187--188.

Equation (209.3) makes Kim's Kurihara vanishing order finite and at most one.
It cannot be zero: the exact root number is `-1`, so `L(A,1)=0` and the
zero-prime Kurihara value vanishes.  Thus the vanishing order is exactly one.
Kim's Theorem 1.10 now identifies

\[
 \operatorname{Sel}(\mathbf Q,A[7])
 \xrightarrow{\sim} A(\mathbf F_{29})/7A(\mathbf F_{29}). \tag{209.4}
\]

The target has dimension one.  The exact reduction of `P` is nonzero in that
target, so the rational Kummer class already spans (209.4).  The Kummer exact
sequence gives `Sha(A/Q)[7]=0`.  Cycle 193's certified analytic rank one and
Gross--Zagier--Kolyvagin make the full `Sha` finite; a nonzero finite
seven-primary group would contain an element of order seven.  This proves
(209.1).

## BSTW conversion

Cycle 209's BSTW applicability audit checks `7` ordinary, `7` prime to `2N`,
residual absolute irreducibility, residual ramification at `433`, analytic
rank one, trivial rational torsion, and Tamagawa product `2`.  BSTW `corA'`
therefore states

\[
 v_7\!\left(\frac{L'(1,A)}{\Omega_A R(A/\mathbf Q)}\right)
 =v_7\!\left(\#\Sha(A/\mathbf Q)\prod_{q\mid N}c_q(A)\right).
\]

The Tamagawa product and `#Sha` are seven-units, proving (209.2).  The
regulator uses a Mordell--Weil basis as in BSTW.  No claim that the displayed
point is a generator is needed for the valuation.

## Trust boundary and reproduction

The arithmetic verifier is dependency-free and fail-closed.  It locks the
Cycle 188 symbol table by SHA-256, reconstructs the discrete logarithms and
exact sum (209.3), verifies the rational point, counts `A(F_29)`, and proves
that the reduced point has order `28`:

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle209_D1499_seven_selmer.py
python3 -O millennium-prize/birch-swinnerton-dyer/verify_cycle209_D1499_seven_selmer.py
gp -fq millennium-prize/birch-swinnerton-dyer/verify_bstw_p7_rank_one_twists.gp
```

The committed symbol rows were produced by PARI/GP `msfromell`; the Python
verifier checks their exact arithmetic and hash but is not an independent
modular-symbol implementation.  The implication from (209.3) to (209.4)
trusts Kim v6, Theorems 1.8 and 1.10, including their Kato/Iwasawa inputs and
normalizations.  The final leading-term identity trusts BSTW
arXiv:2409.01350v2, Theorem `corA'`.  Both are used as external mathematical
theorems, not re-proved here.  The directed analytic-rank certificate and the
Cycle 185 residual-image certificate retain their previously stated producer
boundaries.

This proves the seven-primary assertion for this individual curve under those
published/preprint theorem trust boundaries.  It does not prove full
`Sha(A/Q)=1`, the full BSD formula, or the Millennium BSD conjecture.

## Fail-closed certificate plan

The minimal auditable packet has four independent layers:

1. **Exact arithmetic:** verify the minimal model, `P`, good reduction at
   `7,29`, `#A(F_7)=5`, `#A(F_29)=28`, and that `P mod 29` has order `28`.
2. **Exact modular symbols:** pin the PARI producer and raw table by SHA-256;
   reconstruct all 28 discrete logarithms, period factors, rational symbols,
   and the equality `delta_29=-150=4 mod 7` without floating point.
3. **Theorem hypotheses:** record Kim's precise running hypotheses and Theorem
   1.10, prove residual surjectivity for the twist, invoke good reduction for
   the Manin condition, and check all Tamagawa factors are seven-units.  Use
   the exact sign to prove `delta_1=L(A,1)/Omega_A=0`, so the nonzero one-prime
   value has the required minimal support.
4. **Leading-term conversion:** separately pin the directed analytic-rank-one
   certificate and every hypothesis and normalization of BSTW `corA'`.  Apply
   Kim first to obtain `Sha[7^infty]=0`, then BSTW to obtain
   `v_7(L_alg)=0`.  Never infer a 7-adic valuation by rounding the real
   Cycle 195 quotient.

For a fully independent certificate, the remaining producer trust boundary is
an implementation of the level-433 modular-symbol computation independent of
PARI `msfromell`.  Such a replay strengthens provenance but does not change the
mathematical deduction.
