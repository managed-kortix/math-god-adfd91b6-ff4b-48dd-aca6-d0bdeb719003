# Cycle 278: spacetime `L^4` scaling no-go

## Verdict

`L4-SCALING-NO-GO`.

The estimate required by the Cycle 276 low-amplitude chain,

\[
 \int_0^\tau \|u(t)\|_4^4\,dt
 \le C\nu X(\tau)^{2/3},
 \qquad X(t)=\|u(t)\|_3^3,                         \tag{278.1}
\]

does not follow from the first-record bound `X(t) <= X(tau)`, the energy
scale, and either unweighted energy dissipation or a natural cubic budget for
the weighted dissipation. Three-dimensional Ladyzhenskaya--Gagliardo--Nirenberg
gives the sharp available interpolation, but it leaves a time scale. A
concentrating divergence-free family realizes every exponent in that
interpolation and makes the missing dimensionless parameter unbounded.

This is a no-go for deriving (278.1) from those scalar inputs. It is not a
Navier--Stokes counterexample and does not refute `CEB`. No second amplitude
split is used.

## The sharp weighted interpolation

The standard three-dimensional Ladyzhenskaya--Gagliardo--Nirenberg estimate

\[
 \|u\|_4^4\le C\|u\|_2\|\nabla u\|_2^3             \tag{278.2a}
\]

already fails to integrate from
`u in L_t^infinity L_x^2` and `grad u in L_t^2 L_x^2`, because it requires a
third power of the gradient. Using the weighted dissipation gives the more
relevant sharp interpolation as follows.

Put `f=|u|^(3/2)`. On the three-torus, after including the harmless mean term
in the Sobolev inequality,

\[
 \|f\|_{8/3}
 \le C\|f\|_2^{5/8}
       \bigl(\|\nabla f\|_2+\|f\|_2\bigr)^{3/8}.
\]

Since

\[
 \|f\|_2^2=X,
 \qquad
 \|\nabla f\|_2^2={9\over4}
       \int |u||\nabla|u||^2\le {9\over4}\mathcal D(u),
\]

raising to the power `8/3` yields, up to the lower-order torus term,

\[
 \|u\|_4^4
 \le C X^{5/6}\mathcal D(u)^{1/2}+CX^{4/3}.        \tag{278.2}
\]

Consequently the first-record condition supplies only

\[
 \int_0^\tau\|u\|_4^4dt
 \le C X(\tau)^{5/6}\tau^{1/2}
          \left(\int_0^\tau\mathcal D(u)dt\right)^{1/2}
       +C\tau X(\tau)^{4/3}.                         \tag{278.3}
\]

Even if one grants the additional natural weighted budget

\[
 \nu\int_0^\tau\mathcal D(u)dt\le C_0X(\tau),       \tag{278.4}
\]

(278.3) becomes

\[
 \int_0^\tau\|u\|_4^4dt
 \le C C_0^{1/2}X(\tau)^{4/3}(\tau/\nu)^{1/2}
       +C\tau X(\tau)^{4/3}.                         \tag{278.5}
\]

To recover (278.1), one would still need, at the relevant scale,
`tau <= C nu^3 X(tau)^(-4/3)` (and the analogous restriction for the torus
term). Neither a first record nor energy dissipation supplies this time bound.
Equivalently, applying Young directly to (278.2) leaves

\[
 {X(\tau)^{1/3}\over\nu}\|u\|_4^4
 \le \varepsilon\nu\mathcal D(u)
   +C_\varepsilon {X(\tau)^{7/3}\over\nu^3}
   +C{X(\tau)^{5/3}\over\nu},                       \tag{278.6}
\]

whose time integral contains precisely the missing scale-sensitive term.

## Concentrated test family

Choose a nonzero smooth divergence-free vector field `phi` supported in the
unit ball, and place its rescalings inside one coordinate chart of the torus.
For `0<r<r_*` and `M>0`, set

\[
 u_{M,r}(x)=M^{1/3}r^{-1}\phi((x-x_0)/r),
\]

with one fixed normalization of `phi`. Exact change of variables gives fixed
positive constants `c_j`, independent of `M` and `r`, such that

\[
\begin{aligned}
 X(u_{M,r})&=c_3M,\\
 \|u_{M,r}\|_4^4&=c_4M^{4/3}r^{-1},\\
 \|u_{M,r}\|_2^2&=c_2M^{2/3}r,\\
 \|\nabla u_{M,r}\|_2^2&=c_gM^{2/3}r^{-1},\\
 \mathcal D(u_{M,r})&=c_DM r^{-2}.                  \tag{278.7}
\end{aligned}
\]

Thus this family saturates the homogeneous part of (278.2): both sides scale
as `M^(4/3)/r`.

Take a smooth path on which the mass parameter increases from `(1-epsilon)M`
to `M`, for any fixed sufficiently small `epsilon>0`, while the radius decreases
from `2r` to `r`. Then `X(t)<X(T)` before the endpoint, and the energy scale in
(278.7) still decreases by `asymp M^(2/3)r`. Choosing the interval length

\[
 T=c_*r^2/\nu                                             \tag{278.8}
\]

with a sufficiently small fixed `c_*>0` makes both the unweighted energy
dissipation and the weighted quantities have their natural sizes:

\[
 \nu\int_0^T\|\nabla u\|_2^2dt\asymp M^{2/3}r,
 \qquad
 \nu\int_0^T\mathcal D(u)dt\asymp M.                \tag{278.9}
\]

Indeed, for fixed `M`, because `E(r)=c_2M^(2/3)r` and
`G(r)=c_gM^(2/3)r^(-1)`, the scalar energy identity gives
`r'(t)=-c nu/r(t)` and hence exactly the time scale (278.8). The same ODE,
with an additional bounded term, has a decreasing-radius solution when the
mass parameter makes the small relative increase just specified. Thus the
obstruction is not caused by assigning inconsistent energy and unweighted-
dissipation sizes.

The spacetime quartic norm, however, is

\[
 \int_0^T\|u\|_4^4dt\asymp {M^{4/3}r\over\nu}.      \tag{278.10}
\]

Dividing (278.10) by the right side of (278.1) gives

\[
 {\int_0^T\|u\|_4^4dt\over \nu X(T)^{2/3}}
 \asymp {rM^{2/3}\over\nu^2}
 =\left({r^{1/2}M^{1/3}\over\nu}\right)^2.          \tag{278.11}
\]

For fixed admissible `r` and `nu`, this tends to infinity as `M` tends to
infinity, while (278.9) remains exactly at the energy and weighted-dissipation
scales. The strict increase of the mass parameter makes the endpoint a first
record; the relative factor `(1-epsilon)` does not change (278.8)--(278.11).
This construction is purely kinematic: it asserts compatibility with the named
scalar controls, not with the Navier--Stokes equation.

## Consequence for the one-split chain

Known Ladyzhenskaya/Gagliardo--Nirenberg inequalities plus weighted
`mathcal D` do not close the missing estimate. They close it only after adding
a scale-sensitive time or Reynolds-type restriction. Therefore the Cycle 276
term

\[
 {X(\tau)^{1/3}\over4\nu}
 \int_0^\tau\|u(t)\|_4^4dt
\]

cannot be charged to a universal cubic endpoint reserve using first-excursion
`L^3`, energy, and weighted dissipation alone. Any successful continuation of
this route must use genuinely dynamical trajectory information; introducing a
second `CEB` split is outside this scout.
