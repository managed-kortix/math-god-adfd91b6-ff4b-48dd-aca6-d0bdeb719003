# Routes

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
