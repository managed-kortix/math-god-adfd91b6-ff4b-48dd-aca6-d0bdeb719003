# Routes

Cycle 186 audits the cyclotomic refinement in the selected collision target.
The compositum with `Q(zeta_(8*7*433*29))` is sufficient but nonminimal:
`Q(zeta_7)` is already in `L_0` by the Weil pairing, and fixed-`ell`
admissibility at `29` sees only `(q/29)`, hence only `Q(sqrt(29))`. Full
cyclotomic factors at `433` and `8` are justified only to the extent that the
frozen packet uses the corresponding residue data. The logically minimal test
matches Frobenius in `L_0` and checks admissibility directly; an automatically
filtered search should adjoin only the character field cut out by its exact
predicate. See `cycle-186-cyclotomic-modulus-minimality-audit.md`.
In particular, the Cycle 185 anchor `1289` has `(1289/29)=-1`, so its entire
full-modulus progression fails the Cycle 182 condition at `ell=29` and cannot
produce an admissible collision under the currently frozen predicate.

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
