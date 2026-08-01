# Cycle 218: frozen Chow-secant moving-support candidate

## Decision

Freeze one new finite architecture and no search family around it.  The
candidate is a degree-one rational curve in a Chow variety, with two integral
non-graph endpoint cycles of the exact Cycle 169 degrees.  It uses the singular
Chow space directly rather than an ordered collection of moving graph branches.

The ambient sixfold and constants are

\[
 A_0=E_i^3\times E_i^3,\qquad P=(1,1,1,1,1,3),
\]

\[
 d_+=6072151396206990896,\quad
 d_-=2315779370123038256,\quad
 D=d_++d_-=8387930766330029152.
\]

Write `C_0^+`, `C_0^-` for the Cycle 169 graph pair and
`Z=C_0^+-C_0^-=D_0 alpha_0`.  Set

\[
 P_0=\operatorname {Chow}_{3,d_+}(A_0)\times
     \operatorname {Chow}_{3,d_-}(A_0),\qquad
 Q_0=\operatorname {Chow}_{3,D}(A_0).
\]

Fix once and for all Chow-form projective embeddings of these three schemes.
The frozen rational-equivalence stratum is

\[
 \boxed{(e,n,h)=(0,1,(1)).}                                      \tag{218.1}
\]

Thus there is no auxiliary cycle and no chain-length or map-degree search.

## The secant incidence

For `Y=(Y^+,Y^-) in P_0`, put

\[
 A(Y)=Y^++C_0^-,\qquad B(Y)=Y^-+C_0^+\quad\hbox{in }Q_0.          \tag{218.2}
\]

On an affine Chow-form chart write their coordinate vectors as `a(Y)` and
`b(Y)`.  Freeze the unique parametrized projective line

\[
 f_Y([s:t])=[s\,a(Y)+t\,b(Y)].                                   \tag{218.3}
\]

If homogeneous equations for `Q_0` in the chosen embedding are
`F_1,...,F_r`, the finite secant equations are

\[
 [s^{q-j}t^j]F_\ell(sa(Y)+tb(Y))=0
 \quad(1\leq\ell\leq r,\ 0\leq j\leq q=\deg F_\ell).           \tag{218.4}
\]

They say exactly that the whole line (218.3), not merely its endpoints, lies
in `Q_0`.  Equations (218.2)--(218.4) define a closed finite-type incidence
`R_sec` inside the fixed endpoint charts.  The endpoints give the explicit
one-step chain

\[
 Y^++C_0^- = f_Y([1:0])\sim_{\mathbb P^1}
 f_Y([0:1])=Y^-+C_0^+,                                           \tag{218.5}
\]

and cancellation in the Chow group gives

\[
 \boxed{[Y^+]-[Y^-]=[C_0^+]-[C_0^-]=D_0\alpha_0.}                \tag{218.6}
\]

This is an explicit rational-equivalence formula conditional only on solving
the displayed finite polynomial equations.  It does not replace rational
equivalence by connectedness or algebraic equivalence.

## Moving-support open

Restrict `R_sec` to the declared open `U_mov` on which

1. `Y^+` and `Y^-` are geometrically integral and generically reduced;
2. neither endpoint is a translate, thickening, clean union, complete-
   intersection residual, Ferrand double, or weighted-Pfaffian residual of any
   of the seven scalar graphs;
3. the general member of (218.3) is geometrically integral; and
4. `a(Y) != b(Y)` and the line meets the smooth locus of `Q_0` generically.

For a machine elimination these conditions are represented by fixed witness
minors, discriminants, and noncontainment resultants, and the product `Delta`
of those witnesses is inverted.  A candidate point must print the witnesses;
the words "general" and "non-graph" are not accepted as certificates.

The first condition deliberately excludes the huge split symmetric-product
cover of the Cycle 169 multiplicities.  The local model
`Sym^m(A^3)` explains where Chow-only tangent coordinates can occur, but an
ordered moving-point arc sees only the three degree-one traces and obeys the
old graph obstruction.  Here any useful direction must occur in the actual
Jacobian of the secant incidence at an integral non-graph point.

## Exact ambient-relative tangent formula

Let `S` be the nine-dimensional PEL base with coordinates
`tau=(tau_1,...,tau_9)`, and let `x_+`, `x_-` be affine coordinates on the two
relative Chow charts.  Write their equations as

\[
 G_+(\tau,x_+)=0,\qquad G_-(\tau,x_-)=0.                          \tag{218.7}
\]

At a proposed point define

\[
 J_\pm=\partial_{x_\pm}G_\pm,\qquad K_\pm=\partial_\tau G_\pm.   \tag{218.8}
\]

The full tangent matrix is

\[
 \mathcal J=
 \begin{pmatrix}
 J_+&0&K_+\\
 0&J_-&K_-
 \end{pmatrix}.                                                   \tag{218.9}
\]

Surjectivity to `T_0S` is certified by matrices `U_+`, `U_-`
satisfying

\[
 J_+U_++K_+=0,\qquad J_-U_-+K_-=0.                               \tag{218.10}
\]

Equivalently, compute an exact basis matrix `N` for `ker(mathcal J)`, with
columns equal to tangent vectors, and let `N_tau` be its last nine rows.  The
requested tangent minor is any named set `I` of nine columns such that

\[
 \boxed{\det (N_\tau)_{[1,\ldots,9],I}\ne0.}                      \tag{218.11}
\]

The certificate must name the nine columns and give this determinant exactly.
Equation (218.10), normalized to base block `I_9`, is a stronger witness of the
same fact.  This prevents a large absolute Chow tangent from being mistaken for
nine independent base directions.

Equations (218.4) select and certify the special-fiber point.  They are not
silently treated as relative equations over `S`: the reference graphs
`C_0^+` and `C_0^-` do not extend over the full PEL base.  Following the Cycle
196 gate, rank and jet are computed in the ambient relative Chow product at
the selected endpoint pair.  Requiring the secant itself to deform would
reinsert the obstructed reference graphs and define a different architecture.

## Exact second-order formulas

Write `z=(x_+,x_-)` and collect (218.7) into `Phi(tau,z)=0`.  For the
first-order solution `z=U tau`, a second-order section

\[
 z(\tau)=U\tau+\sum_{1\leq a\leq b\leq9}W_{ab}\tau_a\tau_b
          \pmod{(\tau)^3}                                        \tag{218.12}
\]

exists exactly when, for all `a<=b`,

\[
 \boxed{
 J_z\Phi\,W_{ab}+
 [\tau_a\tau_b]\,\frac12
 D^2\Phi\big((\tau,U\tau),(\tau,U\tau)\big)=0.}                \tag{218.13}
\]

In components the quadratic forcing is

\[
 [\tau_a\tau_b]\left(
 \tfrac12\Phi_{\tau\tau}(\tau,\tau)
 +\Phi_{\tau z}(\tau,U\tau)
 +\tfrac12\Phi_{zz}(U\tau,U\tau)\right).                       \tag{218.14}
\]

Equations (218.10), (218.13), the special-fiber secant coefficient equations
(218.4), and `w Delta-1=0` are one finite polynomial system over the exact
coefficient field of the Chow charts.  Only the relative Chow equations enter
the derivatives in (218.10) and (218.13).

## Frozen pass/fail rule

The architecture passes only with a point of `R_sec cap U_mov`, an exact
nonzero minor (218.11), and all 45 ambient-relative second-order systems
(218.13).  It fails only with a unit-ideal certificate after saturation by
`Delta` and by the selected tangent minor.  Failure retires this degree-one
secant architecture only.

No point, Chow-form equation list, tangent minor, or unit-ideal certificate is
produced here.  In particular this note is a finite candidate specification,
not a production certificate and not a Hodge-conjecture result.  The
determinantal alternative is not frozen: a `2 x 4` rank-one locus would be the
next genuinely non-complete-intersection support, but no globally compatible
bundle matrix with the required two exact endpoint degrees and graph-combination
specialization is currently available; freezing it now would repeat the Cycle
155 Picard-label error.

The exact numerical data are frozen in
`cycle218_frozen_chow_secant.json` and checked by

```sh
python3 millennium-prize/hodge/verify_cycle218_frozen_chow_secant.py
```
