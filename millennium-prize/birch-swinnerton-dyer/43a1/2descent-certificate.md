# Exact full 2-descent certificate for `43a1`

## Result

For

\[
E/\mathbf Q:\quad y^2+y=x^3+x^2,\qquad P=(0,0),
\]

the full (multiplication-by-2, not 2-isogeny) descent gives

\[
\operatorname {Sel}^{(2)}(E/\mathbf Q)=\langle\delta(P)\rangle
 \simeq \mathbf F_2.
\]

Consequently `dim_F2 Sel_2(E/Q)=1`, `rank E(Q)=1`, and
`Sha(E/Q)[2]=0`.

No 2-isogeny descent is available: the 2-division polynomial

\[
4X^3+4X^2+1
\]

has no rational root, so `E(Q)[2]=0` and there is no rational subgroup of
order two.  The computation therefore uses the standard full 2-descent in
the cubic etale algebra.

## Finite certificate

PARI returns one basis element for the set of everywhere locally soluble
2-covers.  Its binary-quartic affine model is

\[
C:\quad V^2=U^4-2U^2+4U+1.                         \tag{1}
\]

The cover map is the exact pair of rational functions printed by
`ell2cover`.  Substitution in the Weierstrass equation modulo (1) verifies
the map identically.  The rational point `(U,V)=(0,1)` maps to

\[
(1,1)=-3P\equiv P\pmod {2E(\mathbf Q)}.
\]

Thus this nonzero locally soluble cover is the Kummer class of `P`.  Since a
basis of the complete everywhere-locally-soluble cover space has one member,
the Selmer dimension is exactly one, not merely at most one.  Local
solubility is explicit for the basis cover because it has a rational point;
the identity cover has the point at infinity.  The upper-bound step--that no
other locally soluble class exists--is the exact class-group/unit/local-image
calculation performed by the full 2-descent algorithm.

Two exact implementations are supplied:

```sh
gp -fq millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1_2descent.gp
magma millennium-prize/birch-swinnerton-dyer/43a1/verify_43a1_2descent.m
```

The GP checker starts only from `[0,1,1,0,0]`, calls `ell2cover`, checks that
the returned complete basis has cardinality one, checks the literal quartic,
checks the cover map as a function-field identity, and checks the rational
point and its image.  PARI documents `ell2cover(E)` as returning “a basis of
the set of everywhere locally soluble 2-covers.”

The Magma checker is the independent proof-enabled replay.  It is written
against the documented Magma V2.29 five-return-value interface and calls
`TwoSelmerGroup(E)`, whose five outputs expose the Selmer group, its map to
the etale algebra, the finite set of relevant primes, the global Kummer map,
and the local maps.  It asserts order two and verifies that the Kummer image
of `P` is its unique nonzero element.  It separately calls `TwoDescent(E)`
and prints the explicit cover basis.

## Theorem deduction

The Kummer sequence for multiplication by two gives the exact sequence

\[
0\longrightarrow E(\mathbf Q)/2E(\mathbf Q)
 \longrightarrow \operatorname {Sel}^{(2)}(E/\mathbf Q)
 \longrightarrow \Sha(E/\mathbf Q)[2]\longrightarrow0.       \tag{2}
\]

The irreducible cubic gives `E(Q)[2]=0`.  Rational torsion is trivial because
it injects into the good reductions of orders `5` and `6` at `2` and `3`.
The exact Kummer computation certifies `delta(P) != 0`; equivalently,
`P` is not twice a rational point.  Hence the left term of (2) has dimension
at least one.  The certified middle term has dimension one, so both dimensions
are one and the right term is zero.  In particular the descent itself proves
the rank upper bound one; the nontorsion point `P` proves the matching lower
bound.

This establishes only `Sha[2]=0`.  Vanishing of the entire 2-primary group
also follows once finiteness of `Sha` is independently known, since every
nonzero finite 2-group contains an element of order two.

## Trust boundary

The small transcript is a finite, exactly replayable certificate relative to
the published full 2-descent implementations; it is not a hand-expanded
formal proof of their class-group and local-field algorithms.  The Magma
replay is independent of PARI and exposes the Kummer and local-map objects,
closing the earlier single-backend gap when its transcript is retained.  In
an environment without Magma, only the PARI half can be executed and the
independent-backend claim remains pending rather than silently promoted.
