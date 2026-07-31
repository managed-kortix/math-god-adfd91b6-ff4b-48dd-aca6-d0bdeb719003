# Cycle 183: strategic referee and non-equivalence gate

## Decision

Do not promote the random-order OBDD route to the main funnel.  Cycle 182
already proves the clean theorem available from easy-table splice packing:
for most orders, exact decision `MCSP` has large midpoint width.  At the MMW
threshold, however, every such packing has

\[
 \log_2 |C|\leq O(s\log(n+s))=N^{o(1)}.
\]

The method therefore cannot force the fixed-power space lower bound required
by McKay--Murray--Williams.  It also has no mechanism for relational search,
per-item update time, SAT-oracle accounting, adaptive order, or repeated
reads.  These are independent model gaps, not missing constants in the Cycle
182 union bound.  Random OBDDs remain a bounded P-versus-NP scout and a valid
restricted-model theorem, but further optimization of the same Reed--Muller
packing is not worth main-funnel compute.

The only OBDD continuation worth a bounded scout is qualitatively different:
construct one explicit polynomial-time Boolean function with a polynomial-size
hidden matching family such that every variable order has a balanced cut where
one matching leaves `Omega(N)` independent residual bits.  A selector visible
in the input is disallowed, because the OBDD can read it first.  Success would
give an all-order OBDD lower bound, still not `P != NP`; failure on an explicit
matching family would be a finite combinatorial obstruction.  Until such a
construction is stated, stop the random-order MCSP line at Cycle 182.

## Six non-equivalence candidates

A viable main target must be an exact theorem or counterexample whose statement
is not merely an equivalent reformulation of the corresponding Millennium
problem.

| target | next exact non-equivalence target | referee status |
|---|---|---|
| BSD | For `E=433a1`, `p=7`, `P=(0,1)`, `Q=(-1,1)`, set `L_0=Q(E[7],7^{-1}P,7^{-1}Q)` and fix `ell=29`.  In `L'=L_0 Q(zeta_(8*7*433*29))`, find admissible primes `q_0,q_1` with the same Frobenius conjugacy class but `c(q_0,29)=0` and `c(q_1,29)!=0`, with the full three-layer Cycle 182 certificate; or prove that no such collision occurs in a declared finite search range. | **Select.** Finite, falsifiable, and directly tests the new governance hypothesis without asserting BSD. |
| Hodge | Construct, or obstruct by an explicit relative deformation calculation, a fixed-degree effective pair `(Y^+,Y^-)` representing the projected Cycle 151 seed, with both relative Chow germs dominating the PEL base, rank-nine tangent image, and vanishing primary obstruction. | Live second choice, but no bounded-degree support or finite deformation complex is currently named. |
| Navier--Stokes | For the Cycle 177 Laurent packet, solve the first-completion polynomial closure problem through quadratic order: either give a divergence-free finite completion whose undesignated Fourier coefficients and their first two time derivatives vanish, or give an exact elimination certificate of infeasibility for the declared support. | Bounded and non-equivalent, but the present frequency support and degree bound must be frozen before compute. |
| P versus NP | Give one explicit polynomial-time function and polynomial-size hidden-matching family for which every variable order exposes `Omega(N)` independent cross-cut bits, without an input-readable selector; or exhibit an order defeating the proposed family. | Keep as scout.  Even success is only an all-order OBDD theorem and has no current MMW transfer. |
| RH | Prove a uniform lower bound for the post-staircase two-row Schur residual `R` in the exact logarithmic Nyman--Beurling decrement, strong enough to close the lagged-prefix estimate, or produce an exact family where the bound fails. | Technically live but close to the existing RH-strength funnel; the candidate inequality still needs one canonical statement and constant before promotion. |
| Yang--Mills | On one fixed finite `SU(2)` lattice block, construct the interacting-vacuum anchored excitation synthesis and certify an explicit frame constant and two-sided temporal Schur norm uniformly over boundary gauge data in a declared weak-coupling interval. | Legitimate finite benchmark, but no present argument transports it uniformly in volume, cutoff, and continuum scale. |

## Selected Cycle 183 target

Continue the BSD rotation, not random OBDDs.  The next exact target is the
fixed-field, fixed-auxiliary-prime collision test in the first row.

The test is deliberately narrower than universal nonfactorization.  The field
`L_0` is the natural residual two-point Kummer field already governing the
localization data of `P,Q`; `ell=29` is fixed from the audited auxiliary-prime
packet.  Adjoin the cyclotomic factor so congruence and elementary twist-local
conditions are constant on a Frobenius fiber.  Then enumerate unramified twist
primes by conjugacy class, check every admissibility condition directly, and
compute the exact one-prime Kurihara coordinate from rational modular symbols.

Acceptance requires all artifacts in
`birch-swinnerton-dyer/cycle-182-q-collision-certificate-specification.md`:
pinned arithmetic replay, dependency-free reduction modulo seven, and a
class-separating Galois witness.  Polynomial factorization type alone is not a
Frobenius certificate.  A zero/nonzero collision retires governance by `L_0`;
absence of a collision in the finite range is only a negative search report and
does not prove factorization.  If `ell=29` fails the one-prime admissibility
conditions for every relevant Frobenius fiber, that exact failure is the first
result and the next auxiliary prime must be selected by a separately recorded
criterion.

No Millennium result is claimed.
