# Routes

Cycle 260 hostilely audits the proposed `43a1`, `K=Q(sqrt(-7))` shortcut and
records `GAPS`, not a theorem. The curve model and Heegner hypothesis pass.
Cha covers odd `p != 7`, including `p=3,43`, subject to irreducibility; the
ramified prime `7` needs residual surjectivity under Kolyvagin's theorem or a
direct Selmer computation. Odd-primary restriction from `Q` to `K` is
injective. The exact normalized Heegner identity and index, complete residual
certificates, and a proof-enabled independent 2-descent replay are absent. Do
not infer `Sha=0` from
`ellheegner`, LMFDB's rounded analytic value, or BSD. See
`cycle-260-43a1-heegner-generator-hostile-audit.md`.

Cycle 237 terminalizes the frozen checkpoint as `HK236 WALL`. The exact
modular-symbol index `8` does not certify the CM trace coordinates, the
residual images at `5,23,1499` are not certified in the proof packet, and the
undirected lower-height input plus unidentified trace prevents an unconditional
cutoff. Under the unchanged stop rule, the weaker support implication and
conditional `M=35` do not count as a pass. Retire this curve/field architecture,
do not cycle through nearby fields or isolated primary checks, and return to
the six-lane review recorded in `../cycle-237-strategic-rotation.md`.

Cycle 238 hostilely corrects the Cycle 237 explanation while retaining
`HK236 WALL`. Cha's irreducible theorem covers every odd prime except `5,23`
(ramified in `K`) and `1499` (additive reduction). Kolyvagin's original
surjective theorem as stated by Cha has neither local restriction, so all
three exceptional primes can be restored by certified residual-surjectivity
checks. The singleton non-CM isogeny class proves irreducibility but not
surjectivity. Thus the currently justified support statement is
`p | #Sha => p | I_A or p in {5,23,1499}`, not a sole structural exception at
`1499`. The exact auxiliary modular symbol certifies rank-zero nonvanishing;
the 2-descent handles `2`; and the `Q`-to-`K` free-lattice index is only known
to be 2-primary, which suffices for odd valuations but is not literal lattice
equality. See `cycle-238-hostile-kolyvagin-literature-audit.md` and
`cycle-237-integral-kolyvagin-factor-wall.md`.

Cycle 215 closes the seven-primary part for `D=-29023` without finding the
huge rational generator. Cycle 211 gives
`delta_tilde_113=-17186=6 mod 7`, so Kim identifies the residual Selmer group
with the one-dimensional quotient `A(F_113)/7A(F_113)`. Cycle 194 proves rank
one and PARI proves trivial rational torsion; hence `A(Q)/7A(Q)` is itself a
one-dimensional subspace of that Selmer group and must equal it. The rational
Kummer localization is therefore nonzero, `Sha[7^infty]=0`, and BSTW `corA'`
gives `v_7(L'(1,A)/(Omega_A R(A/Q)))=0`. No floating point or rational
generator coordinates enter this deduction. See
`cycle-215-D-29023-exact-kummer-localization.md`.

Cycle 209 closes the seven-primary part for `D=-1499` without real rounding.
The exact one-prime Kurihara value at `29` is `-150=4 mod 7`, and the displayed
rational point has nonzero image in `A(F_29)/7A(F_29)`. Under Kim's
Selmer-structure theorem this gives `Sel(Q,A[7^infty])=Q_7/Z_7` and
`Sha(A/Q)[7^infty]=0`. Under BSTW `corA'`, with the separately audited local
and normalization hypotheses, the normalized algebraic leading term has
valuation `v_7(L'(1,A)/(Omega_A R(A/Q)))=0`. The exact arithmetic is
fail-closed and hash-pinned; Kim and BSTW remain theorem trust boundaries.
This does not prove full `Sha=1` or full BSD. See
`cycle-209-D-1499-seven-adic-leading-term.md`.

Cycle 195 identifies the displayed `D=-1499` point as a saturated
Mordell--Weil generator using the exact 2-descent and the Cremona--Siksek
height calculation. The component and divisibility checks are exact, but the
eclib ANTS lower bound is a non-directed `bigfloat` result replayed at two
precisions, so the generator conclusion retains that numerical-library trust
assumption. Exact local arithmetic and directed Arb intervals put its
point-normalized BSD quotient in
`(0.9998891243271545,1.0001875109945714)`. Unconditionally, analytic rank one
and Gross--Zagier--Kolyvagin make `Sha` finite; 2-descent gives
`Sha[2^infty]=0`; Cassels--Tate makes its order an odd square. No odd prime is
proved to divide or not divide the order, and the real quotient interval is
not an odd-prime BSD theorem. Thus `Sha=1` remains predicted, not proved. See
`cycle-195-D-1499-exact-interval-bsd-quotient.md`.

Cycle 194 gives a rigorous analytic-rank certificate for the second collision
twist, `D=-29023`. Its fail-closed verifier pins `650000` exact integer
coefficients and uses rational enclosures for `pi`, every exponential-integral
weight, signed summation, and the infinite tail to prove
`9776577544974464/10^15 < L'(1) < 141618654480665006/10^15`. The exact root
number is `-1`, so the analytic rank is one. Together with Cycle 193 for
`D=-1499`, both collision twists now have certified analytic rank one.
Gross--Zagier--Kolyvagin then gives algebraic rank one and finiteness of the
full Tate--Shafarevich group for each twist. At that stage this proved neither
the refined BSD leading-term formula nor the order of `Sha`, a regulator, or a
generator; Cycle 195 later certifies the latter two for `D=-1499` only.
See `cycle-194-D-29023-rigorous-derivative-certificate.md`.

Cycle 193 gives a rigorous analytic-rank certificate for the first collision
twist, `D=-1499`. It derives
`L'(1)=2 sum a_n E1(2*pi*n/sqrt(N))/n`, pins `100000` exact integer
coefficients, encloses `pi`, all exponential-integral weights, and the infinite
tail with rational directed arithmetic, and obtains a strictly positive
rational interval for `L'(1)`. Together with exact root number `-1`, this proves
analytic rank one for this individual twist; Gross--Zagier--Kolyvagin gives
algebraic rank one and finite `Sha`, but no refined BSD formula. See
`cycle-193-rigorous-derivative-certificate.md`.

Cycles 192--193 run PARI's 2-descent on the two collision twists
`D=-1499,-29023`. Full `bnfcertify` certification of the common 2-division
cubic's class and unit data certifies the exact 2-Selmer upper bound one; it
does not itself prove a positive Mordell--Weil rank. The exact non-torsion point
for `D=-1499` therefore makes that rank exactly one. At the descent stage for
`D=-29023`, no point or certified analytic nonvanishing was known, so the
conservative rank interval was `[0,1]` and the descent alone made no claim of
`Sha[2]=0`. PARI found no point even at effort six and `ellheegner` exhausted a
1 GB stack; the conditional BSD height estimate was about `2659.76`. Cycle 194
later closes rank one and finite `Sha` by the independent certified analytic
and Gross--Zagier--Kolyvagin route, without retroactively strengthening the
descent. See `cycle-192-pari-2descent-and-point-obstruction.md`.

Cycle 191 surveys the exact modular-symbol distribution route to infinitely
many zero/nonzero `c(q,29)` values in one fixed `L_0` class.  The theorems of
Petridis--Risager, Constantinescu--Nordentoft, and Lee--Sun distribute
individual fixed-level symbols over all reduced rational cusps of bounded
denominator; they do not specialize to prime denominators in a nonabelian
Chebotarev class or to the Legendre-weighted `q-1`-symbol aggregate defining
`c(q,29)`.  Finite Fourier inversion reduces the desired result exactly to six
nontrivial exponential-sum cancellations on the fixed class.  Chebotarev gives
infinitely many primes in the local packet, but not cancellation of the
Kurihara coordinate.  See `cycle-191-modular-symbol-distribution-route.md`.

Cycle 186 audits the cyclotomic refinement in the selected collision target.
The compositum with `Q(zeta_(8*7*433*29))` is sufficient but nonminimal:
`Q(zeta_7)` is already in `L_0` by the Weil pairing, and fixed-`ell`
admissibility at `29` sees only `(q/29)`, hence only `Q(sqrt(29))`. Full
cyclotomic factors at `433` and `8` are justified only to the extent that the
frozen packet uses the corresponding residue data. The logically minimal test
matches Frobenius in `L_0` and checks admissibility directly; an automatically
filtered search should adjoin only the character field cut out by its exact
predicate. See `cycle-186-cyclotomic-modulus-minimality-audit.md`.
Cycle 187 corrects the earlier anchor calculation: `(1289/29)=1`, since
`1289=13 mod 29` and `10^2=13 mod 29`. The full-modulus progression is
admissible at `ell=29`, though still needlessly sparse.

Cycle 185 proves the maximal-group hypothesis for the named Kummer field.
Multiplicative reduction with `v_433(Delta)=1` supplies a mod-7 transvection,
and Frobenius at 3 has trace `5`, determinant `3`, and nonsquare discriminant
`6`; exhaustive relative-position generation gives the full `GL_2(F_7)`. The
localization determinant `6` proves `P,Q` independent in `E(Q)/7E(Q)`.
Inflation-restriction, Sah's lemma, and the submodule classification of
`E[7]^2` then give the full translation kernel. Thus
`Gal(L_0/Q)=E[7]^2 semidirect GL_2(F_7)`, of order `4,840,416`.

Cycle 184 proves the exact screening criterion in the two-point Kummer group.
Above nonidentity-unipotent linear Frobenius, full conjugacy is determined by
the zero/projective class of the localization row modulo the centralizer. The
certified rows `(1,5)` at `29` and `(1,4)` at `113` have determinant `6 mod 7`,
so their full Kummer Frobenius elements are not conjugate and they cannot form a
collision pair for `L_0`. Candidate searches must match the projective row as
well as the linear residual class.

Cycle 183 selects the first named collision target.  For `E=433a1`, `p=7`,
`P=(0,1)`, and `Q=(-1,1)`, take the residual two-point Kummer field
`L_0=Q(E[7],7^-1 P,7^-1 Q)` and fix `ell=29`.  Search the compositum
`L_0 Q(zeta_(8*7*433*29))` for two admissible twist primes in one Frobenius
conjugacy class with zero/nonzero `c(q,29)`.  Acceptance uses the complete
Cycle 182 certificate specification.  A collision refutes governance only by
this named field; a finite collision-free search does not prove governance.

Cycle 182 finds that the Cycle 181 report has no reconstructible collision
data.  A future fixed-`ell` zero/nonzero certificate must commit the named
Galois field and compositum, class-separating Frobenius witnesses, exact twist
models and normalizations, every rational modular symbol, grouped sums, and a
pinned producer.  Acceptance requires independent arithmetic replay,
dependency-free mod-7 reduction, and Galois verification.  See
`cycle-182-q-collision-certificate-specification.md`.

Cycle 181 defines `c(q,ell)` exactly as the first augmentation derivative of
the Mazur--Tate element of `E^(D_q)`, equivalently the one-prime Kurihara sum.
Its newform has conductor `433 q^2`, and the twist formula uses base symbols of
denominator `q ell`; therefore the fixed Selmer governing field does not
automatically govern `c`. Conductor growth obstructs that proof but does not
prove nonfactorization. For each explicitly proposed finite Galois field `L`,
the bounded test is a same-`ell`, same-Frobenius collision with different `c`
(preferably zero versus nonzero). One collision refutes only that `L`;
universal nonfactorization requires collisions along a cofinal tower. The
positive route now requires an explicit fixed determinant line, comparison
maps, exact Frobenius formula, and uniform twist/Kurihara hypotheses before any
Chebotarev certificate-density argument.
