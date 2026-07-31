# Cycle 196: fixed degree does not make rational equivalence finite type

## The correction

Let

\[
 Z=D_0\alpha _0=C_0^+-C_0^-
\]

be the Cycle 169 signed cycle, with

\[
 d_+=\deg C_0^+=6072151396206990896,
 \qquad
 d_-=\deg C_0^-=2315779370123038256.
\]

The product

\[
 P:=\operatorname {Chow}_{3,d_+}(A_0)
 \times\operatorname {Chow}_{3,d_-}(A_0)
\]

is of finite type.  This makes the possible effective pairs of the two exact
degrees bounded, but it does **not** make the condition

\[
 [Y^+]-[Y^-]=Z\quad\hbox{in }CH_3(A_0)
\]

a single finite-type condition on `P`.

Indeed, put

\[
 A(Y)=Y^++C_0^-,\qquad B(Y)=Y^-+C_0^+.
\]

Both have degree

\[
 D=d_++d_-=8387930766330029152,
\]

and the desired equality is exactly `A(Y) ~rat B(Y)`.  A rational-equivalence
witness may require an auxiliary effective cycle and rational curves, or a
chain of rational curves, of unbounded parameter degree in a Chow variety.
The endpoint degree `D` gives no known bound for that witness complexity.

## Correct parameter schemes

Fix integers `e,n >= 0` and degrees `h=(h_1,...,h_n)` for maps to the chosen
projective embedding of

\[
 Q_e:=\operatorname {Chow}_{3,D+e}(A_0).
\]

Let `R_(e,n,h)` be the incidence scheme of tuples

\[
 (Y^+,Y^-,E,f_1,\ldots,f_n),
\]

where `Y` lies in `P`, `E` lies in `Chow_(3,e)(A_0)`, each
`f_i:P^1 -> Q_e` has degree `h_i`, and

\[
 \begin{aligned}
 f_1(0)&=A(Y)+E,\\
 f_i(\infty)&=f_{i+1}(0)\quad(1\leq i<n),\\
 f_n(\infty)&=B(Y)+E.
 \end{aligned}
\]

Addition of effective cycles is a morphism of Chow schemes.  The fixed-degree
`Hom` schemes and the endpoint fiber products therefore make every
`R_(e,n,h)` a finite-type scheme.  Constant maps cover the trivial cases.  The
standard characterization of rational equivalence by rational curves in
spaces of effective cycles gives

\[
 \{Y\in P:[Y^+]-[Y^-]=Z\}
 =\bigcup_{e,n,h}\operatorname {im}(R_{e,n,h}\longrightarrow P)
\]

on algebraically closed points.  Thus the exact relation is naturally a
countable ind-finite-type, or countable union of constructible, incidence; it
is not presently one finite-type subscheme.  One may use a one-curve version
after absorbing a finite chain into further auxiliary effective summands, but
the auxiliary degree and map degree remain unbounded, so the conclusion is the
same.

For the relative PEL family `cal A -> S`, the ambient pair space is the product
of relative Chow schemes.  The schemes `R_(e,n,h)` above sit over its special
fiber and select exactly those special-fiber points representing `Z`.  One
then studies the germ of the ambient relative Chow space at the image of a
chosen witness point and its map to `S`, including its second-order
obstruction.  The reference graphs `C_0^+` and `C_0^-` need not extend over
`S`; incorrectly replacing them by relative cycles would assume the desired
deformation.  If a relative reference pair is independently available after a
base change, the same construction can instead be made entirely with relative
Chow and relative `Hom` schemes.

## Why connected components do not repair the issue

Connected components of a Chow scheme detect algebraic connectedness and lead
to algebraic equivalence.  Rational equivalence is finer.  Already for
divisors on a positive-genus curve, effective divisors can lie in the same
connected symmetric power while defining different classes in `Pic`; hence
they are not rationally equivalent.  Replacing the incidence above by the
connected component of `Q_e` would silently weaken the Cycle 195 condition.

## Corrected gate

Fixed endpoint degrees suffice for a finite-type ambient pair space, but not
for a finite-type rational-equivalence locus.  The positive direction remains
well posed: exhibit a pair together with one explicit finite witness
`(e,n,h,E,f_i)` whose relative germ has rank-nine image and extends through
second order.

The proposed negative direction needs an additional theorem.  Either derive
an explicit bound

\[
 e\leq E_0,\qquad n\leq N_0,\qquad h_i\leq H_0
\]

for every rational equivalence between these endpoints, reducing the relation
to a finite union of the schemes above, or prove the obstruction uniformly on
all `R_(e,n,h)`.  An obstruction only on `P`, or only on one connected
component of a Chow scheme, is not a degree-wide obstruction to all signed
pairs representing `D_0 alpha_0`.

This is a formulation correction, not a construction of the required moving
cycle and not a Hodge-conjecture result.
