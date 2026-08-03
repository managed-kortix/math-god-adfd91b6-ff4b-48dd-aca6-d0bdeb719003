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

Precisely, this is a no-go for deriving (278.1) from inequalities involving
only those scalar quantities: below is an exact family of scalar histories
that satisfies the record condition, the exact unweighted energy identity,
and a uniform weighted-dissipation budget, but violates (278.1) by an
arbitrarily large factor. The histories are not asserted to solve the
Navier--Stokes equation. Thus this is not a Navier--Stokes counterexample and
does not refute `CEB`. No second amplitude split is used.

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

Choose nonzero `psi in C_c^infinity(B(0,1))` and set
`phi=(partial_2 psi,-partial_1 psi,0)`. Thus `phi` is smooth, compactly
supported, nonzero, and divergence-free. Choose `r_*` so that the Euclidean
ball `B(x_0,r_*)` embeds in a fixed fundamental cube of the flat torus, and
extend each rescaling by zero and then periodically. This gives a smooth
periodic divergence-free field. It is also mean-zero: for each component,
`int phi_i=int div(y_i phi)=0`. For `0<rho<r_*` and `m>0`, set

\[
 u_{m,\rho}(x)=m^{1/3}\rho^{-1}
       \phi((x-x_0)/\rho).
\]

Exact change of variables gives fixed positive constants `c_j`, independent
of `m` and `rho`, such that

\[
\begin{aligned}
 X(u_{m,\rho})&=c_3m,\\
 \|u_{m,\rho}\|_4^4&=c_4m^{4/3}\rho^{-1},\\
 \|u_{m,\rho}\|_2^2&=c_2m^{2/3}\rho,\\
 \|\nabla u_{m,\rho}\|_2^2&=c_gm^{2/3}\rho^{-1},\\
 \mathcal D(u_{m,\rho})&=c_Dm\rho^{-2}.             \tag{278.7}
\end{aligned}
\]

Thus this family saturates the homogeneous part of (278.2): both sides scale
as `m^(4/3)/rho`.

There is already an exact static counterexample if the named controls mean
only their scalar bounds. Hold `u_{M,r}` constant on `[0,T_0]`, where

\[
 T_0={c_2r^2\over2c_g\nu}.
\]

Then the record bound holds (with equality at every time), and

\[
 \nu\int_0^{T_0}Gdt={1\over2}E,
 \qquad
 \nu\int_0^{T_0}\mathcal Ddt={c_2c_D\over2c_g}M
 ={c_2c_D\over2c_gc_3}X,                             \tag{278.8}
\]

whereas

\[
 {\int_0^{T_0}\|u\|_4^4dt\over\nu X^{2/3}}
 ={c_2c_4\over2c_gc_3^{2/3}}
       {rM^{2/3}\over\nu^2}\longrightarrow\infty.  \tag{278.9}
\]

Thus the supremum energy scale, unweighted dissipation bound, weighted budget,
and record inequality cannot imply (278.1). This static slab does not satisfy
the dynamical energy identity, because its energy is constant. The following
exact history shows that adding that identity and requiring a strict endpoint
record still does not repair the scalar implication.

Fix `0<r<r_*/2`, put

\[
 K={4c_g\over c_2},\qquad
 \rho(t)^2=4r^2-2K\nu t,\qquad
 m(t)=M\left({r\over\rho(t)}\right)^{3/4},            \tag{278.10}
\]

and stop at

\[
 T={3r^2\over2K\nu},
 \qquad \rho(0)=2r,\quad \rho(T)=r.                 \tag{278.11}
\]

Set `u(t)=u_{m(t),rho(t)}`. Since `rho` strictly decreases, `m` and hence
`X` strictly increase; in particular `X(t)<X(T)=c_3M` for `t<T`. Moreover,
with `E=||u||_2^2` and `G=||grad u||_2^2`, (278.7) and (278.10) give the exact
scalar energy identity

\[
 E'(t)=-2\nu G(t).                                    \tag{278.12}
\]

Indeed `E=c_2M^{2/3}r^{1/2}\rho^{1/2}` and
`rho'=-K nu/rho`; the definition of `K` then gives (278.12). Direct integration
also gives

\[
 \nu\int_0^T G(t)dt
 ={c_2\over2}(\sqrt2-1)M^{2/3}r,
 \qquad
 \nu\int_0^T\mathcal D(u(t))dt
 ={4c_D\over3K}(1-2^{-3/4})M.                        \tag{278.13}
\]

Thus the unweighted budget is exactly the energy drop divided by two, while
the weighted budget is exactly
`[4c_D(1-2^(-3/4))/(3Kc_3)]X(T)`, uniformly in `M`, `r`, and `nu`. Also
`sup_t E(t)/X(T)^(2/3)` is a fixed constant times `r`, so no hidden
amplitude-dependent energy ratio is being discarded.

The spacetime quartic norm, however, is

\[
 \int_0^T\|u\|_4^4dt
 ={c_4\log2\over K\nu}M^{4/3}r.                     \tag{278.14}
\]

Dividing (278.14) by the right side of (278.1) gives

\[
 {\int_0^T\|u\|_4^4dt\over \nu X(T)^{2/3}}
 ={c_4\log2\over Kc_3^{2/3}}
      {rM^{2/3}\over\nu^2}.                         \tag{278.15}
\]

For fixed admissible `r` and `nu`, this tends to infinity as `M` tends to
infinity, while (278.12)--(278.13) hold exactly and the endpoint is a strict
first record. Unlike a Navier--Stokes trajectory, this prescribed path need not
satisfy `partial_t u+(u dot grad)u+grad p=nu Delta u`; the exact energy identity
alone does not enforce that equation. Thus the construction is purely
kinematic: it disproves an implication from the named scalar controls, not an
implication that is additionally allowed to use the full Navier--Stokes equation
or other trajectory information.

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
