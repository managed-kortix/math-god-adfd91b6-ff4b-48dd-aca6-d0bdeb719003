# Notebook

Bounded scout is queued to formalize the two rank computations in the Fermat
cubic calibration and then check obstruction/smoothness data; equality of
Zariski tangent dimensions alone is not actual dominance.

## Bounded scout tick 2

For the Fermat cubic plane, the normal sequence is
`0 -> N_(P/X) -> O_P(1)^3 -> O_P(3) -> 0`, with map `(u^2,v^2,w^2)`.
Thus `H^0(N)=0` and `H^1(N)=C[uvw]`. The fixed-fiber Hilbert point is isolated
and reduced despite the nonzero ambient obstruction space. The incidence of
cubics containing a plane is a smooth dimension-54 projective bundle over
`Gr(3,6)` and maps unramifiedly to the 55-dimensional cubic parameter space,
so its image is locally a genuine divisor. This validates the calibration but
does not identify arbitrary Hodge components with incidence images.

## Bounded scout cycle 36

The plane calibration also fixes the primitive intersection form exactly.  If
`h` is the hyperplane class and `P` is a plane in a smooth cubic fourfold, then
`h^4=3`, `P.h^2=1`, and the normal sequence gives

`c(N_(P/X))=(1+h)^3/(1+3h)`, hence `P^2=c_2(N_(P/X))=3`.

Therefore the integral primitive class `gamma=3[P]-h^2` satisfies
`gamma.h^2=0` and `gamma^2=24`.  Equivalently,
`([P]-h^2/3)^2=8/3`.  This identifies the exact lattice vector carried by the
plane-incidence divisor; tangent-space dominance alone still says nothing
about Hodge components carrying other primitive lattices.

## Bounded scout cycle 39

The plane self-intersection calibration extends exactly to every smooth
degree-`d` hypersurface fourfold `X_d` in `P^5` containing a plane.  The normal
sequence gives

`c(N_(P/X_d))=(1+h)^3/(1+d h)`

and hence `P^2=d^2-3d+3`.  Because `h^4=d` and `P.h^2=1`, the primitive rational
class `P-h^2/d` has square `d^2-3d+3-1/d`.  At `d=3` this is `8/3`, so
`3[P]-h^2` has square `24` as before.  This fixes the entire normal-sequence
lattice calculation; it supplies no dominance statement for other Hodge
components.

## Bounded scout cycle 41

For the Fermat-type degree-`d` plane calibration, `d>=3`, the map on global
sections induced by the normal sequence is

`H^0(O_P(1)^3) -> H^0(O_P(d))`,
`(l_1,l_2,l_3) |-> l_1u^(d-1)+l_2v^(d-1)+l_3w^(d-1)`.

Its nine monomials are distinct, so it is injective and
`h^0(N_(P/X_d))=0`, while
`h^1(N_(P/X_d))=binom(d+2,2)-9`.  The latter is exactly the expected
codimension of the plane-incidence image: a fixed plane imposes
`binom(d+2,2)` conditions and `Gr(3,6)` has dimension nine.  At `d=3` this
recovers a one-dimensional obstruction space beside a reduced isolated plane
and a smooth incidence divisor.  Nonzero `H^1(N)` therefore cannot by itself
be used as a failure-of-dominance certificate.

## Bounded scout cycle 42

The cubic calibration gives an exact local counterexample to treating
`H^1(N)` as a nonreducedness test. The normal map has cokernel `C[uvw]`, so
`H^1(N_(P/X))` is one-dimensional, but the Hilbert tangent space is
`H^0(N_(P/X))=0`. For the local Hilbert ring `(A,m)` this says `m/m^2=0`;
Nakayama gives `m=0`. Hence the plane is a reduced isolated Hilbert point even
though its standard obstruction space is nonzero. No conclusion follows for
other Hodge-locus components.

## Bounded scout cycle 43

Reduced isolated fibers and tangent equality still do not prove component
dominance. In `S=Spec C[x,y]`, let `W=V(y)`, `V=V(y-x^2)`, and immerse
`Z=W` into `S`. The fiber over the origin is one reduced point, the
differential is injective, and `T_0 W=T_0 V=V(y)`. Nevertheless the image is
`W`, not `V`; indeed `W intersect V=V(y,x^2)` is supported only at the origin.
First-order data cannot distinguish the tangent branches `(y)` and
`(y-x^2)`. Thus the Fermat cubic plane calibration still needs branch
identification plus equal dimension inside a specified irreducible Hodge
component. This is a local logical obstruction, not a claim about the actual
cubic Hodge locus or a Hodge result.
