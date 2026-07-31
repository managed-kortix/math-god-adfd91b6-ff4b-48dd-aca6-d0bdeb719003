# Cycle 168: full Hecke transport has an exact degree--denominator no-go

The Cycle 151 diagonal seed cannot be saturated under all PEL Hecke
correspondences inside one finite-type relative Chow locus merely by changing
the normalization.  At every good inert prime, bounded geometric degree and a
uniform integral denominator are mutually exclusive.  This closes the direct
Hecke-image ansatz, but it does not exclude a new fixed-degree representative
whose relative Chow germ already dominates the PEL base.

## The exact tradeoff

Let

\[
 f:(A,L)\longrightarrow(B,M),\qquad f^*M=mL,
\]

be a polarized isogeny in the determinant-`-3`, signature-`(3,3)` PEL
component, and let `Gamma` be the transported Cycle 151 abelian threefold.  Put

\[
 Y=f(\Gamma),\qquad
 \delta=\deg(f|_\Gamma),\qquad
 \eta={m^3\over\delta}.
\]

The restriction of the seed polarization has volume

\[
 \chi(L|_\Gamma)=16.
\]

Cycles 161, 162, and 165 give the exact identities

\[
 f_*[\Gamma]=\delta[Y],
 \qquad
 \chi(M|_Y)=16\eta,
 \qquad
 m^{-3}f_*[\Gamma]={1\over\eta}[Y].
\]

The class `[Y]` is primitive in integral cohomology and hence is not divisible
in integral Chow.  Therefore the last displayed class has exact integral
denominator `eta`.

More generally, take any positive rational rescaling

\[
 Z_f=a_f f_*[\Gamma].
\]

If one fixed integer `D>0` clears its denominator, write

\[
 DZ_f=k_f[Y],\qquad k_f=D a_f\delta\in Z_{>0}.
\]

Its polarization degree is then

\[
 \boxed{\deg_M(DZ_f)=16k_f\eta.}
\]

In particular,

\[
 \boxed{\deg_M(DZ_f)\geq16\eta.}
\]

This formula is independent of how `a_f` is named.  It proves the following
dichotomy.

**Degree--denominator theorem.** For a collection of transported reduced
images with unbounded `eta`, no positive normalization can have both:

1. a common denominator bounded by one integer `D`; and
2. bounded degree after clearing that denominator.

For the middle-weight normalization, the degree is exactly 16 and the
denominator is exactly `eta`.  Clearing the denominator gives `[Y]`, whose
degree is exactly `16 eta`.  Multiplying by any additional positive integer
only makes the second quantity larger.

The assertion concerns effective Chow cycles.  Signed cancellation in a Chow
group is not a point of an effective Chow variety and cannot invalidate the
positive degree identity.

## Application to the full PEL Hecke correspondence

Let `p>=5` be inert in `Q(i)`.  Cycle 163 proves that every PEL-stable
Lagrangian `p`-kernel satisfies

\[
 \eta_p(K)\geq p,
\]

with equality for exactly `(p+1)^2(p^2+1)` kernels and with no `eta=1`
kernel.  Hence even the smallest-denominator branches at inert primes obey

\[
 \operatorname{den}\bigl(p^{-3}f_*[\Gamma]\bigr)\geq p,
 \qquad
 \deg_M[Y]\geq16p.
\]

As inert primes are unbounded, the theorem applies to the full Hecke system.
Passing from individual arrows to the full finite correspondence does not
repair it.  On the labeled Hecke cover every branch is still present and the
integrality condition is branchwise.  If

\[
 N_p=(p+1)(p^3+1)(p^5+1)
\]

is the number of inert PEL kernels, then the raw sum, middle-weight sum, and
probabilistic average have degrees respectively

\[
 16N_pp^3,
 \qquad 16N_p,
 \qquad 16.
\]

The corresponding coefficient of the reduced image on a branch is
`delta`, `1/eta`, and `1/(N_p eta)`.  Thus averaging adds the correspondence
denominator `N_p`; it cannot remove the geometric denominator `eta`.

This gives an exact finite-type consequence.  A finite-type subscheme of the
disjoint union of relative effective Chow spaces meets only finitely many
degree strata.  If rational cycles are admitted with a fixed denominator `D`,
multiplication by `D` places them in integral degree strata.  The boxed lower
bound shows that no such finite-type locus contains the middle-normalized
Cycle 151 images for all inert Hecke levels.  Equivalently:

\[
 \boxed{\text{the full normalized Hecke orbit of the diagonal seed is not a
 single bounded-denominator finite-type relative Chow family.}}
\]

The split `eta=1` chains of Cycle 166 are the sharp boundary case: they keep
degree 16 and denominator one, but remain in the proper closed locus `Z_16`.
Adding the inert branches removes boundedness rather than producing dominance.

## What remains a genuine candidate

The theorem does not say that every finite-type Chow component over the PEL
base is impossible.  It rules out only a component obtained by collecting the
normalized reduced Hecke images of `Gamma`.  A viable component would have to
be a new fixed-degree local germ.

Let `alpha_0` be the rational algebraic cycle obtained by applying the Cycle
152 interpolation correspondence to the Cycle 151 graph; its cohomology class
is the nonzero Weil projection.  Clearing the fixed coefficients in that
correspondence writes a multiple of `alpha_0` as a signed integral cycle

\[
 D_0\alpha_0=C_0^+-C_0^-
\]

for effective cycles `C_0^+` and `C_0^-` on the special fiber.  This supplies
a concrete finite-type parameter space

\[
 \operatorname{Chow}_{d_+}({\cal A}/S)
 \times_S
 \operatorname{Chow}_{d_-}({\cal A}/S),
\]

where `d_+` and `d_-` are the fixed polarization degrees of the two parts.
If a component through some pair representing the same difference dominated
the nine-dimensional PEL base and the difference of its universal cycle
carried the flat Weil class, generic algebraicity on this PEL component would
follow.  No varying Hecke denominator would occur because `D_0,d_+,d_-` are
fixed once at the seed.

The obvious pair obtained by expanding the projector is not presently such a
component.  Its supports are combinations of special-fiber graph cycles.  The
original diagonal has obstruction map

\[
 B\longmapsto Q^{-1}B^t-B
\]

of rank six, while the vanishing of the obstruction after projecting to the
Weil class occurs only in cohomology.  It does not make the positive and
negative effective Chow points deform together over all nine directions.
Thus the remaining exact candidate criterion is:

\[
 \boxed{\begin{array}{c}
 \text{find an effective pair representing }D_0\alpha_0\text{ whose relative}\\
 \text{Chow component has tangent image of rank nine and whose obstructions}\\
 \text{vanish, or prove that no such representative exists.}
 \end{array}}
\]

Degree renormalization and full Hecke averaging cannot supply that candidate.
This is a no-go for the direct Hecke-saturation mechanism, not a proof of the
Hodge conjecture and not a no-go for all rationally equivalent representatives.
