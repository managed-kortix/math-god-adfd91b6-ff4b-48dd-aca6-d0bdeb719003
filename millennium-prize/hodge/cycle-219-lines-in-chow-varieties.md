# Cycle 219 research note: projective lines in a Chow embedding

## Decision

For the case needed by Cycle 218, yes: a nonconstant projective line whose
general member is geometrically integral and generically reduced has the
proposed form:

\[
\boxed{Z_t=F+H_t,}
\]

where `F=0` under general integrality, and the moving cycles `H_t` form a pencil
of hypersurfaces in one fixed linear `P^(p+1)`.  For three-cycles the moving
part is therefore a hypersurface pencil in a fixed `P^4`.

Applied to the secant joining `Y^++C_0^-` and `Y^-+C_0^+`, this obstructs
Cycle 218 immediately: the ambient abelian sixfold contains no `P^4`.  Thus the
secant incidence is empty on its declared integral-general open, before
tangent and second-order conditions.

## Integral-general classification theorem

Let `X subset P^N` be projective over an algebraically closed field, and use
the standard Cayley--Chow embedding of effective pure `p`-cycles of degree
`D`.  Suppose a projective line `ell=P^1` is contained in this Chow variety and
its general member is geometrically integral and generically reduced.  Then
there is a fixed linear space `Lambda=P^(p+1) subset P^N` such that every cycle
represented by `ell` is

\[
Z_t=V_\Lambda(sf_0+tf_1),                                      \tag{219.1}
\]

for two degree-`e` forms `f_0,f_1` on `Lambda`, after removal of their common
hypersurface factor.  Every moving hypersurface in (219.1) is contained in
`X`; equivalently its support is contained in `X cap Lambda`.

The constant line is excluded.  Special members of the pencil may be reducible
or nonreduced and need not share a component.

## Proof

### 1. General integrality removes fixed components

For an effective cycle `Z=sum m_i Z_i`, its Cayley--Chow form satisfies

\[
R_Z=\prod_i R_{Z_i}^{m_i},\qquad R_{Z+W}=R_ZR_W.                \tag{219.2}
\]

Write the line as

\[
R_t=sR_0+tR_\infty.
\]

The common irreducible Chow-form factors of `R_0` and `R_infty` correspond,
with their minimum multiplicities, to a maximal common effective cycle `F`.
The same factors divide every `R_t`.  General integrality and nonconstancy force
`F=0`: otherwise a general member is reducible, or is the constant cycle `F`.

### 2. The universal cycle has bidegree `(D,1)`

Let `U subset P^1 x P^N` be the universal cycle, with projections
`q` and `ev`.  Put `a=c_1(O_(P^1)(1))` and
`h=c_1(O_(P^N)(1))`.  Since a fiber has degree `e`, its cycle class is

\[
[U]=e h^{N-p}+m\,a h^{N-p-1}                                  \tag{219.3}
\]

in `A^(N-p)(P^1 x P^N)` for some nonnegative integer `m`.

The integer `m` is the degree of the parameter curve in the Chow-form
embedding.  Indeed, intersecting with a general complementary
`P^(N-p-1)` gives on `P^1` the incidence divisor

\[
\{t:Z_t\cap P^{N-p-1}\ne\varnothing\},
\]

whose defining section is the restriction of the Chow form.  Because the
parameter curve is a projective line in Chow coordinates, `m=1`.

### 3. The swept variety has degree one

General-fiber integrality gives a unique component of `U` dominating `P^1`.
Its image has dimension `p+1`; otherwise all fibers have the same irreducible
support and the Chow line is constant.  Let

\[
W=ev(U),\qquad \delta=\deg(U/W).
\]

Pushing (219.3) to `P^N` kills the first term and gives

\[
ev_*[U]=h^{N-p-1}.
\]

On the other hand `ev_*[U]=\delta[W]`, hence

\[
\delta\deg W=1.                                                \tag{219.4}
\]

Thus `delta=1` and `deg W=1`.  Every irreducible nondegenerate projective
variety of degree one is a linear space, so

\[
W=\Lambda=P^{p+1}.                                             \tag{219.5}
\]

Each residual fiber is consequently an effective hypersurface of degree `e`
in `Lambda`.  The family is a divisor on `P^1 x Lambda`; its equation has
bidegree `(1,e)`, hence is

\[
sf_0+tf_1=0.
\]

This proves (219.1).  Conversely, such a pencil has Chow form

\[
R_t(L)=s f_0(\Lambda\cap L)+t f_1(\Lambda\cap L)
\]

for a general complementary plane `L`, so it is a projective line in Chow
coordinates.  This classification is exact under the stated integral-general
hypothesis.  Without that hypothesis, fixed components and several dominating
incidence components require a componentwise formulation and are not needed
for Cycle 218.

The pushforward argument is intersection-theoretic; general integrality is
used to isolate one dominating component and identify its image with the whole
sweep.  The result is intrinsic to the standard Chow line bundle.  An
arbitrary re-embedding by another Veronese power changes what "line" means.

## Abelian varieties contain no linear carrier

An abelian variety contains no positive-dimensional projective linear space.
Indeed, a `P^m` with `m>0` contains a line, while every morphism
`P^1 -> A` is constant.  In characteristic zero this follows, for example,
from Riemann--Hurwitz after composing with a quotient or from the absence of
rational curves on an abelian variety.  Hence the abelian sixfold `A_0`
contains no `P^4`.

## Exact Cycle 218 obstruction

Cycle 218 condition 3 requires the general member of its secant to be
geometrically integral, and condition 4 requires a nonconstant line.  The
classification would therefore put a `P^4` inside `A_0`, contradicting the
preceding paragraph.  The endpoint decomposition is irrelevant to this
stronger obstruction.

Thus

\[
\boxed{R_{\rm sec}\cap U_{\rm mov}=\varnothing.}               \tag{219.7}
\]

No endpoint degree arithmetic, graph-support analysis, Chow equation list,
Jacobian minor, or Hessian lift is needed.  This retires the degree-one
Chow-secant architecture of Cycle 218, not higher-degree rational curves or
chains in the Chow variety.

## Surviving production mechanisms

The obstruction leaves these possibilities:

1. drop integral general member and use a reducible moving family;
2. replace the line by a higher-degree rational curve in the Chow embedding;
3. use a chain of such curves, possibly after adding an auxiliary effective
   cycle; or
4. change the ambient variety to one containing a `P^4` and use a genuine
   hypersurface pencil there.

Options 2 and 3 return to the larger finite-type strata `R_(e,n,h)` of Cycle
196.  Cycle 218 condition 3 rules out option 1, while the abelian ambient rules
out option 4.

## Primary literature

1. W.-L. Chow and B. L. van der Waerden, "Zur algebraischen Geometrie IX:
   Ueber zugeordnete Formen und algebraische Systeme von algebraischen
   Mannigfaltigkeiten," *Math. Ann.* **113** (1937), 692--704,
   DOI `10.1007/BF01571660`.  Original associated-form construction and
   algebraic systems.
2. W.-L. Chow, "On equivalence classes of cycles in an algebraic variety,"
   *Ann. of Math.* **64** (1956), 450--479, DOI `10.2307/1969596`.  Primary
   source for cycle families and equivalence through Chow parameter spaces.
3. M. L. Green and I. Morrison, "The equations defining Chow varieties,"
   *Duke Math. J.* **53** (1986), 733--747,
   DOI `10.1215/S0012-7094-86-05339-1`.  Equations of the Chow-form image.
4. I. M. Gelfand, M. M. Kapranov, and A. V. Zelevinsky,
   *Discriminants, Resultants, and Multidimensional Determinants*, Chapter 3,
   Birkhaeuser, 1994, DOI `10.1007/978-0-8176-4771-1_5`.  Modern account of
   Cayley--Chow forms, incidence divisors, and multiplicativity.

The line classification itself follows directly from the universal-cycle
class and the incidence interpretation of the Chow line bundle, as proved
above; the cited sources provide those foundational ingredients rather than a
separately named line-classification theorem.
