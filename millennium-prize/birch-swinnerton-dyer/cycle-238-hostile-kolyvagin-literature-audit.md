# Cycle 238: hostile Cha--Jetchev applicability audit

## Verdict

The Cycle 237 conclusion that `p=1499` is the sole structural exception is
retracted. Cha's irreducible theorem excludes `5,23` by ramification and
`1499` by additive reduction, but Kolyvagin's original surjective theorem, as
quoted by Cha's Theorem 3, has none of those local restrictions. Thus all
three primes are residual-image checks, not structural exceptions.

The unconditional artifact-level support statement is only

\[
 p\mid\#\Sha(A/\mathbf Q)
 \Longrightarrow p\mid I_A\quad\hbox{or}\quad p\in\{5,23,1499\}.
\]

After certified surjectivity at all three primes, there is no exceptional odd
prime. Checking only `5,23` would leave `1499` unchecked, but would not make it
a theorem-forced additive-prime exception.

## Literature hypotheses

- Cha, Theorem 21: `p` is odd, `p` does not divide the field discriminant,
  the curve has good or multiplicative reduction at `p`, and `A[p]` is
  irreducible.
- Kolyvagin, as stated by Cha, Theorem 3: `p` is odd, the Heegner point is
  non-torsion, and the residual image is `GL_2(F_p)`. The displayed statement
  has no condition `p` prime to the conductor and no semistability condition.
- Jetchev, Theorem 1.4 and Corollary 1.5: `p` is prime to the conductor and the
  residual representation is surjective. Jetchev bounds the nonnegative
  global-divisibility correction from below; the exact formula containing
  that correction is Kolyvagin's formula. Jetchev therefore does not apply at
  `1499` and is not needed for the coarse upper bound.

For `K=Q(sqrt(-115))`, Cha excludes `5,23` because they ramify. At `1499`, the
curve has additive reduction, so Cha excludes it as well. These exclusions do
not carry over to the original surjective theorem.

## Arithmetic transitions

The certified 2-descent gives `Sha(A/Q)[2]=0`. Finiteness is known from the
analytic-rank-one Gross--Zagier--Kolyvagin argument, and any nonzero finite
2-primary group has nonzero 2-torsion. Hence `Sha(A/Q)[2^infty]=0`.

The exact modular-symbol computation for the auxiliary twist certifies
`L(A^(chi_K),1) != 0`. Therefore

\[
 rank A(K)=rank A(Q)+rank A^{(chi_K)}(Q)=1.
\]

This does not make `A(Q)_free` and `A(K)_free` equal as integral lattices.
Their quotient is killed by two: modulo torsion, conjugation is trivial on the
rational rank-one space and `R+conj(R)` is rational. Consequently their
Heegner indices have equal odd-prime valuations, which is sufficient for the
odd-primary bounds.

For odd `p`, restriction from `Q` to `K` is injective on `Sha[p^infty]` because
restriction followed by corestriction is multiplication by two. This passage
does not prove anything at `p=2`; descent handles that prime separately.

## Residual representations

A singleton rational isogeny class for a non-CM elliptic curve rules out a
rational prime-degree isogeny, and hence proves irreducibility of `A[p]` after
twisting. It does not imply that the image is all of `GL_2(F_p)`: irreducible
images can lie in Cartan normalizers or exceptional subgroups. Therefore the
singleton computation activates Cha away from `5,23,1499`, but cannot by
itself activate Kolyvagin at those three primes.

The repository's external `galrep` table records no exceptional prime for the
base curve `433a1`, but the present proof packet neither certifies that table
nor proves the image statement for the `-1499` twist prime by prime. Those
finite checks must be supplied before removing `5,23,1499` from the support
statement.

## Corrected status

The Cycle 237 `WALL` status remains because no all-prime divisibility is yet
certified. Its former explanation is corrected: there is no established
`1499` structural wall in the cited Kolyvagin theorem. The open tasks are
finite residual-image certificates (or direct primary Selmer computations)
and the separate exact Heegner-index/height gates.
