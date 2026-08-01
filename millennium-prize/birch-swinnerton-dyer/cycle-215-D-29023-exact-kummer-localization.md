# Cycle 215: exact `D=-29023` Kummer localization at `113`

## Result

Let

\[
 A=433\mathrm a1^{(-29023)}:
 y^2+xy+y=x^3+x^2-17548636x-24475377572834.
\]

No rational coordinates for a Mordell--Weil generator are required. Subject
to the same Kim theorem boundary used in Cycle 209, the exact Kurihara
certificate and the already certified rank prove

\[
 \operatorname{loc}_{113}:A(\mathbf Q)/7A(\mathbf Q)
 \xrightarrow{\ \sim\ } A(\mathbf F_{113})/7A(\mathbf F_{113}). \tag{215.1}
\]

Thus the rational Kummer line has nonzero localization at `113`. In
particular,

\[
 \boxed{\Sha(A/\mathbf Q)[7]=0},\qquad
 \boxed{\Sha(A/\mathbf Q)[7^\infty]=0}.                 \tag{215.2}
\]

BSTW `corA'`, with the hypotheses already audited for this twist, then gives

\[
 \boxed{v_7\!\left(\frac{L'(1,A)}{\Omega_A R(A/\mathbf Q)}\right)=0}. \tag{215.3}
\]

This is an exact Selmer/Kummer localization certificate, not an explicit
coordinate certificate for a rational generator and not a full BSD result.

## Dimension-forcing certificate

Cycle 211 computes, using exact rational modular symbols,

\[
 \widetilde\delta^{(1)}_{113}(A)=-17186\equiv6\pmod7.
\]

Here `113` is a genuine Kolyvagin prime: `113=1 mod 7`, `a_113(A)=2`, and
`#A(F_113)=112`. The root number is minus one, so the zero-prime Kurihara
coordinate is `L(A,1)/Omega_A^+=0`; nonvanishing at the one-prime integer
`113` therefore proves that the Kurihara order is exactly one. After the
audited residual-surjectivity, Manin, nonanomalous-at-seven, and seven-unit
Tamagawa hypotheses, Kim's Theorem 1.10 gives the exact classical residual
one-dimensional localization isomorphism

\[
 \operatorname{Sel}(\mathbf Q,A[7])
 \xrightarrow{\ \sim\ }A(\mathbf F_{113})/7A(\mathbf F_{113}). \tag{215.4}
\]

Cycle 194 proves analytic rank one by a directed rational interval and then
uses Gross--Zagier--Kolyvagin to prove `rank A(Q)=1` and finiteness of `Sha`.
PARI's exact torsion computation gives `A(Q)_tors=0`. Consequently

\[
 \dim_{\mathbf F_7} A(\mathbf Q)/7A(\mathbf Q)=1.       \tag{215.5}
\]

The Kummer sequence injects the space in (215.5) into the one-dimensional
Selmer space in (215.4). An injection between these two one-dimensional
spaces is an isomorphism. Composing it with (215.4) proves (215.1), without
choosing or numerically approximating a generator. The same Kummer exact
sequence has quotient `Sha(A/Q)[7]`, proving the first assertion in (215.2).
Since `Sha` is finite, a nontrivial seven-primary subgroup would contain an
element of order seven, proving the second assertion.

This also identifies the local image abstractly and exactly: if `P` is either
generator of the free rank-one group `A(Q)`, then `loc_113([P])` is nonzero and
generates the target. Coordinates of `P` are irrelevant to this conclusion.

## Exact local target

Dependency-free finite-field arithmetic verifies

\[
 A(\mathbf F_{113})\simeq\mathbf Z/112\mathbf Z,
 \quad G=(85,7),\quad \operatorname{ord}(G)=112,
\]

and

\[
 16G=(53,42),\qquad \operatorname{ord}(16G)=7.
\]

Thus the target in (215.1) is visibly one-dimensional and the class of `G`
is a concrete generator. This finite point is not asserted to be the reduction
of a particular displayed rational point; (215.1) proves that some, indeed
every primitive, rational generator maps to a nonzero class.

## Bounded search record

The coordinate search was also repeated exactly with eclib `mwrank` 20231211.
It entered its Type-3 quartic search for the invariant pair

```text
I=842334529, J=42293439810838910
```

and searched positive quartic coefficient `a` toward the exact bound `66586`,
but did not complete within `600` seconds and produced no point. The earlier
PARI effort-six, quartic height `10000`, four-cover height `10^8`, and
eight-cover height `3*10^13` failures remain bounded search obstructions only.
They are no longer an obstruction to the seven-primary deduction because the
dimension argument does not require rational coordinates.

## Reproduction and trust boundaries

Run

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/cycle211_D29023_p7_kurihara.gp
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle215_D29023_localization.py
python3 -O millennium-prize/birch-swinnerton-dyer/verify_cycle215_D29023_localization.py
gp -fq millennium-prize/birch-swinnerton-dyer/verify_bstw_p7_rank_one_twists.gp
```

All finite calculations use integers, rationals, or finite fields. The
Kurihara producer trusts PARI `msfromell`; the implications (215.4) and (215.3)
trust Kim arXiv:2203.12159v6, Theorems 1.8 and 1.10, and BSTW
arXiv:2409.01350v2 `corA'`, respectively. Cycle 194 retains its stated exact
coefficient-producer and Gross--Zagier--Kolyvagin theorem boundaries. No float
or bounded point-search failure is used in (215.1)--(215.3).
