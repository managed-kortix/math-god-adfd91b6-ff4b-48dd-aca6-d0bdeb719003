# Cycle 223: integral-general Chow conics have degree-two carriers

## Question

After Cycle 222 retires Chow-form lines, replace the rational-equivalence
witness by a nonconstant map

\[
 c:{\mathbb P}^1\longrightarrow \operatorname {Chow}_{r,d}(X)
\]

of Chow degree two, and require its general member to be geometrically
integral and generically reduced. For the active Hodge gate, `r=3` and
`X=A_0=E_i^3 x E_i^3`.

## Swept-carrier formula

Embed `X` in `P^N` and let `U subset P^1 x P^N` be the pulled-back universal
incidence cycle. Put

\[
 a=c_1(O_{{\mathbb P}^1}(1)),\qquad h=c_1(O_{{\mathbb P}^N}(1)).
\]

The class of the component containing the general fiber is

\[
 [U]=d h^{N-r}+2a h^{N-r-1}.                                  \tag{223.1}
\]

General geometric integrality makes this dominating component integral.
Nonconstancy implies that its swept image `S` has dimension `r+1`: an
`r`-dimensional image would give the same integral support, multiplicity, and
hence Chow point for every general parameter. Thus the evaluation map

\[
 e:U\longrightarrow S
\]

is generically finite. If `delta=deg(e)`, pushing (223.1) to `P^N` gives

\[
 e_*[U]=2h^{N-r-1}=\delta[S],
 \qquad
 \boxed{\delta\deg(S)=2}.                                      \tag{223.2}
\]

Equivalently, intersecting with a general codimension-`r+1` linear space
counts two points on the parameter conic and also `delta deg(S)` points over
the carrier. This argument includes a degree-two parametrization of a Chow
line; it does not assume that the image of `c` is a plane conic.

## Exact carrier dichotomy

There are only two positive-integer cases.

1. `delta=1`, `deg(S)=2`. The integral carrier is a quadric hypersurface in
   its linear span:

   \[
    S=Q^{r+1}\subset {\mathbb P}^{r+2}.
   \]

   Indeed, an integral variety nondegenerate in its span satisfies
   `deg(S) >= codim(S)+1`. Degree two forces codimension one (codimension zero
   would make `S` its degree-one linear span). The incidence is birational to
   this quadric carrier.

2. `delta=2`, `deg(S)=1`. Then

   \[
    S={\mathbb P}^{r+1},
   \]

   and the universal incidence is generically a double cover of the linear
   carrier. This includes the possibility that the Chow map factors as a
   degree-two cover of a Chow line, but does not require that factorization.

For three-cycles the alternatives are therefore a quadric fourfold
`Q^4 subset P^5` swept once or a linear `P^4` swept twice.

## Abelian no-go

Neither carrier can lie in an abelian variety. The linear case contains
projective lines. In the quadric case, an integral quadric of positive
dimension at least two over an algebraically closed field contains a
projective line; in particular every integral `Q^4` does. Composing such a
line with `S subset A_0` would give a nonconstant morphism
`P^1 -> A_0`, whereas every morphism from `P^1` to an abelian variety is
constant.

Consequently

\[
 \boxed{\text{no Chow-degree-two map to }
 \operatorname {Chow}_{3,d}(A_0)
 \text{ has geometrically integral general member}.}            \tag{223.3}
\]

This is an exact no-go for the integral-general conic mechanism, independent
of endpoint splitting, endpoint degree, graph support, PEL tangent rank, and
second-order lifting. It does not exclude reducible general members, Chow
degree at least three, or chains whose individual components have larger Chow
degree.

## Stop-rule decision

The degree-two rational curve is the second consecutive new support mechanism:
Cycle 222 retires the degree-one linear secant, and (223.3) retires the
degree-two integral-general mechanism. Apply the Cycle 216 stop rule and return
the main funnel to portfolio discovery rather than testing Chow degree three
or enumerating further rational-curve strata. No Hodge-conjecture result is
claimed.
