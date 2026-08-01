# Cycle 222: integral-general Chow lines force a linear carrier

## Question

Cycle 218 asks for a projective line in

\[
 \operatorname {Chow}_{3,D}(A_0),
 \qquad A_0=E_i^3\times E_i^3,
\]

whose two endpoints are the reducible cycles

\[
 Y^++C_0^- \quad\hbox{and}\quad Y^-+C_0^+,
\]

but whose general member is geometrically integral. The following elementary
degree-one argument makes the endpoint decomposition irrelevant: such a line
cannot occur on an abelian variety.

## Linear-carrier lemma

Let `X subset P^N` be projective over an algebraically closed field, and give
`Chow_(r,d)(X)` its standard Chow-form embedding. Suppose a nonconstant line
`T=P^1` in this Chow variety has geometrically integral and generically reduced
general member. Then `X` contains a linear `P^(r+1)`.

More precisely, let `W subset T x X` be the incidence support of the family
and let `S` be the closure of its image in `P^N`. General-fiber integrality
gives one component of `W` dominating `T`, and nonconstancy gives
`dim(S)=r+1`. For a general linear subspace `L subset P^N` of codimension
`r+1`, the Chow hyperplane

\[
 H_L=\{[Z]: |Z|\cap L\ne\varnothing\}
\]

meets the line `T` in one point, counted with multiplicity. Equivalently,

\[
 \operatorname {length}\bigl(W\cap(T\times L)\bigr)=1.           \tag{222.1}
\]

If `delta` is the generic degree of `W -> S`, the same intersection, now
counted after projection to `S`, has length

\[
 \delta\deg(S).                                                   \tag{222.2}
\]

Thus `delta deg(S)=1`. Hence `delta=1`, `deg(S)=1`, and
`S=P^(r+1)` is a linear subspace contained in `X`. Endpoint splitting causes
no extra component in this count: the endpoint components are special-fiber
divisors inside the closure of the unique dominating incidence component.

The statement also gives the familiar model for the surviving examples. On
the carrier `S=P^(r+1)`, a pencil of degree-`d` hypersurfaces has Chow forms
linear in its two defining equations. Reducible special fibers and an
integral general fiber are therefore possible in projective space, but only
inside this linear-carrier architecture (up to a common fixed cycle, which is
excluded when the general member itself is integral).

## Low-dimensional scouts

### Zero-cycles

Over an algebraically closed field an integral, generically reduced effective
zero-cycle has degree one. Therefore `Chow_(0,d)(P^n)` has no line with
integral general member when `d>1`. For `d=1` it is `P^n`, but its endpoints
are single points and cannot be reducible endpoint sums. Thus the requested
phenomenon has a complete zero-cycle no-go.

### Divisors

For divisors,

\[
 \operatorname {Chow}_{n-1,d}(P^n)=P(H^0(P^n,O(d))),
\]

so ordinary pencils give positive examples. Already for `d=2`, in coordinates
`x_0,x_1,x_2,...`, take

\[
 F_0=x_0x_1,
 \qquad F_1=x_2(x_0+x_1+x_2).                                    \tag{222.3}
\]

The two endpoints each have two distinct components and have no common
irreducible summand. The general member `sF_0+tF_1` is integral: on the
coordinate `P^2` it is a nonsingular conic away from finitely many parameter
values, and in larger projective space it is the corresponding integral cone.
Thus disjoint endpoint summands do not by themselves force a common component
or a reducible general member.

### Curves

The same pencil in a fixed plane `P^2 subset P^n` is a line in
`Chow_(1,2)(P^n)`. Its endpoints are unions of two distinct lines with no
common component, while its general member is an integral conic. More
generally, the linear-carrier lemma says that any Chow line with integral
general `r`-cycle sweeps a fixed `P^(r+1)` and is represented there by a
hypersurface pencil. Hence the divisor and plane-curve examples are the exact
projective-space analogue sought by the scout, not evidence that the same
secant can live on `A_0`.

## Cycle 218 consequence

An abelian variety contains no positive-dimensional projective linear space:
restricting its inclusion to any line in such a space would give a nonconstant
map `P^1 -> A_0`, while every map from `P^1` to an abelian variety is constant.
Applying the lemma with `r=3` shows

\[
 \boxed{\text{no nonconstant Chow-form line in }
 \operatorname {Chow}_{3,D}(A_0)
 \text{ has integral general member}.}                           \tag{222.4}
\]

Consequently the Cycle 218 open `U_mov` is empty already by condition 3. This
is independent of the enormous endpoint degrees, the graph summands, tangent
rank, and second-order equations. It retires the whole degree-one secant
architecture on `A_0`, not merely a selected support ansatz.

The obstruction is specific to Chow degree one. A rational curve of Chow
degree at least two, or a chain of such curves, need not have a linear swept
carrier and remains outside (222.4). No Hodge-conjecture result is claimed.
