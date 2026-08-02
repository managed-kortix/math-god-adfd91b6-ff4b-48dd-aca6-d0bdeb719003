# Cycle 251: tangent-intersection no-go for the F242 norm-one search

## Result

No triple of Gaussian matrices, norm-one or otherwise, makes the Cycle 248 map

\[
 f_L:C^3\longrightarrow E^6,
 \qquad (p_1,p_2,p_3)\longmapsto\sum_{r=1}^3L_r\phi(p_r)
\]

a closed immersion. Thus the proposed `5^54` enumeration has an empty
candidate family already at the source-level geometry gate. This is a no-go
for the F242 support architecture only; it is not a Hodge-conjecture result.

## Difference divisor and degree check

Work over an algebraic closure of the characteristic-zero base field.  Let
`Theta=eta_1+eta_2+eta_3` on `A=E^3`.  The factor eight in the divisor class
does not come from the degree-eight isogeny alone.  It follows from the
Cycle 248 curve class

\[
 [\phi(C)]=2(\eta_2\eta_3+\eta_1\eta_3+\eta_1\eta_2).
\]

In its Pontryagin product with the reflected class, equal-axis products have
one-dimensional image and contribute zero to the divisor class.  For each
pair of distinct axes, the two orders each contribute coefficient `2*2`.
Thus

\[
 [\phi(C)]*[-1]^*[\phi(C)]=8(\eta_1+\eta_2+\eta_3)=8\Theta.       \tag{251.1}
\]

This pushforward class is the class of `D`, rather than a generic-degree
multiple of it.  Before applying the isogeny, a second representation
`p-q=p'-q'` would give linearly equivalent effective divisors
`p+q'` and `p'+q` of degree two.  Since the plane quartic is
nonhyperelliptic, it has no `g^1_2`, so a general difference has a unique
representation.  After applying the isogeny, an extra representation would
put a general point of the difference divisor in its intersection with a
translate by a nonzero element of the finite isogeny kernel.  No such
translate equals the divisor: its principal-polarization ancestor has trivial
translation stabilizer.  Each intersection is therefore at most a curve, and
the finite union of these intersections is not dense in the divisor.  The
generic degree remains one.  Consequently

\[
 [D]=8\Theta,\qquad \operatorname{mult}_0D=4,
 \qquad \operatorname{TC}_0(D):Q(z)=z_1^4+z_2^4+z_3^4=0.         \tag{251.2}
\]

Here `D` is an integral effective Cartier divisor: it is a codimension-one
integral image in the smooth threefold `A`.  Its class is ample.

## Tangent cone and the kernel

Assume first that `M=[L_1 L_2 L_3]` has Gaussian rank six, since lower rank was
excluded in Cycle 243. Let

\[
 K=\ker(M)^0\subset A^3.
\]

Gaussian rank six makes `M:A^3->E^6` surjective.  In characteristic zero its
kernel is smooth, and its identity component `K` is therefore an abelian
threefold.  Also `T_0K=ker(dM)`; disconnected components of `ker(M)` play no
role in the argument below.

For `v=(v_1,v_2,v_3) in T_0K`, set `F_r(v)=Q(v_r)`, where a zero component is
allowed and satisfies `F_r(v)=0`.  The tangent map of `f_L` fails to be
injective somewhere exactly when there is a nonzero `v in T_0K` with

\[
 F_1(v)=F_2(v)=F_3(v)=0.                                        \tag{251.3}
\]

For a nonzero component, `Q(v_r)=0` says precisely that `[v_r]` is a canonical
tangent direction `dphi_p(T_pC)` of the plane quartic; for a zero component,
choose any source point and the zero tangent vector.  Thus (251.3) constructs
a source tangent vector killed by `df_L`.  Conversely, every vector killed by
some `df_L` gives (251.3).  Hence tangent injectivity is equivalent, not merely
implicated, to the three quartics `F_r` having no common zero in
`P(T_0K)`.  This explicitly includes tangent relations having one or two zero
components.

Consequently, tangent injectivity forces the three initial quartics to have no
common projective zero.  It also forces every `F_r` to be nonzero: if one were
identically zero, the other two positive-degree plane curves would have a
common projective point.  Therefore `K` is not contained in any
`pr_r^{-1}(D)`, and

\[
 D_r=(pr_r|_K)^*D
\]

is a nonzero effective Cartier divisor on the integral smooth variety `K`.
All three contain zero.  Their local equations have order exactly four and
initial forms `F_1,F_2,F_3`.  No common projective zero makes these initial
forms a homogeneous regular sequence.  The standard filtered regular-sequence
calculation in the three-dimensional regular local ring `O_(K,0)` then gives
an isolated local intersection of exact length

\[
 i_0(D_1,D_2,D_3;K)=4^3=64.                                    \tag{251.4}
\]

## Global intersection forces a collision

Let `Z=D_1 intersect D_2 intersect D_3` scheme-theoretically.  If `Z` has a
positive-dimensional component, its geometric support cannot consist only of
zero, so it contains a nonzero point and already gives a collision.  Otherwise
the three nonzero Cartier divisors meet properly.  Their intersection product
is the sum of their positive local lengths and includes the length 64 at zero.
In particular, it is a positive integer.  Moreover (251.1) gives
`[D_r]=8(pr_r|_K)^*Theta` in `NS(K)`, so

\[
 (D_1D_2D_3)_K
 =8^3\bigl((pr_1^*\Theta)(pr_2^*\Theta)(pr_3^*\Theta)\bigr)_K
 \in512\mathbb Z_{>0}.                                         \tag{251.5}
\]

The contribution at zero is exactly 64 by (251.4), whereas the total is at
least 512 by (251.5).  Thus `Z` has nonzero support.  Choose a nonzero geometric
point `x=(x_1,x_2,x_3) in K intersect D^3`.  Because `D` is the image of the
proper difference map `C x C->A`, every geometric point of `D` has an actual
preimage; choose `p_r,q_r` with `x_r=phi(p_r)-phi(q_r)`.  Some `x_r` is nonzero,
so `p_r != q_r` for that index (even injectivity of `phi` is more than is
needed).  The two source triples are distinct, while

\[
 f_L(p_1,p_2,p_3)-f_L(q_1,q_2,q_3)=Mx=0.
\]

Thus tangent injectivity implies geometric noninjectivity. If tangent
injectivity fails, `f_L` is already not a closed immersion. These alternatives
exhaust all full-rank matrices; the lower-rank cases were already impossible.

## Hostile counterexample checks

The proof would fail in each of the following superficially plausible cases;
the indicated earlier step rules each one out.

* A zero component in a tangent relation is not discarded: it is included in
  (251.3), so block-supported tangent failures are detected.
* A restriction `D_r` cannot silently become the whole of `K` on the
  tangent-injective branch: that would make `F_r` identically zero, after which
  the other two quartics have a common projective zero.
* The mixed intersection need not be positive merely because the three
  classes are nef.  Positivity here instead follows from the proper effective
  intersection already containing the isolated length-64 point at zero.
* A nonzero point of the contracted difference image is not treated as a
  formal difference only: properness of `C x C->D` supplies actual source
  pairs, and nonzeroness makes the two triples distinct.
* Replacing `K` by the full, possibly disconnected kernel is unnecessary.  A
  nonzero point forced inside `K` already lies in `ker(M)` and gives the needed
  collision.

Accordingly the no-go is conditional only on the explicit Cycle 248/250 inputs
reproved or recalled above: the curve class, closed immersion of `phi`, quartic
tangent cone, and characteristic-zero setting.  If any of those inputs is
changed, the conclusion is fail-closed and must not be reused without rerunning
the degree, tangent-cone, and Cartier-restriction checks.

## Valid symmetry and normal-form reductions

The no-go makes enumeration unnecessary, but it also clarifies which proposed
reductions would have been legitimate.

* Left multiplication by `GL_6(Z[i])` is an ambient automorphism and preserves
  the kernel and the closed-immersion question. Gaussian row Hermite reduction
  can therefore canonicalize the row lattice of `M` for geometry-only work; it
  cannot in general produce `[I_6 A]`, since the pivot minor need not be a unit.
  It also does not preserve the
  norm-one box, and a general element does not preserve the fixed Weil
  projector or the scalar `S`. It is therefore a geometric normal form after
  selection, not an orbit reduction for the combined boxed search.
* Smith reduction of the full `6 x 9` matrix uses right column operations that
  mix the three copies of `phi(C)`. Such operations are not domain symmetries,
  so the tempting normal form `[I_6 A]` does not classify F242 maps.
* The three deck involutions act on the elliptic factors, after recentering each
  elliptic quotient at a fixed point of the involution, by
  `D_X=diag(1,-1,-1)`, `D_Y=diag(-1,1,-1)`, and
  `D_Z=diag(-1,-1,1)`. In the fixed Cycle 248 basepoint convention the same
  identities include harmless translation constants. Hence each source
  independently permits
  `L_r -> L_r D` for `D in V_4`. These operations preserve the coefficient
  box, ranks, `S`, tangent injectivity, and geometric injectivity.
* Together with source permutation and common ambient multiplication by a
  Gaussian unit, this gives the certified gate-preserving action
  `V_4^3 semidirect S_3`, times `C_4`, of order `4^3*6*4=1536`. It improves
  the earlier factor 24, but no quotient count is needed after the no-go.

Arbitrary `GL_3(Z[i])` column operations are not allowed: they would require an
identity `T phi=phi composed with a curve automorphism plus a translation`.
Only the displayed deck matrices have been certified here.

## Search consequence

The cheapest logically complete gate order is now:

1. reject block rank below two or total rank below six;
2. reject `S=0` if the exceptional-coordinate diagnostic is desired;
3. apply the tangent-cone test;
4. if the quartics have a common projective zero, reject as non-unramified;
5. otherwise reject as noninjective by the `64 < 512` intersection argument.

There is therefore no small norm-one candidate family likely to be a closed
immersion: every candidate is rejected without source-level Groebner
elimination, and the full `5^54` search should not be run. Tangent-immersive
maps can still occur, as the Cycle 249 witness shows, but the argument forces
them to have a global source collision.
