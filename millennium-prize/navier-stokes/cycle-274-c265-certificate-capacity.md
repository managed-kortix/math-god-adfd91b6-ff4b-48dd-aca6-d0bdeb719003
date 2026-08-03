# Cycle 274: dimensionless capacity of the C265 certificate

## Verdict

`ND274-C265-CERTIFICATE-CAPACITY` returns `WALL` under the instruction to use
the bounded grid imported from the frozen C266 manifest but no datum. The C265
interface itself does not freeze these ranges. The complete framework has
an exact dimensionless feasibility region, but its Picard and cubature gates
remain functions of the Fourier coefficients. The scalar region is nonempty,
so it is not a `NOGO`; without a datum it cannot produce a `WITNESS`.

## 1. Frozen grid and scaling variables

Import the following bounded grid from the frozen `C266-3DDE1` manifest:

\[
 q_0\in\left\{{5\over4},{3\over2},2,3\right\},\qquad
 T\in\{1,2,3,4\},\qquad M=A_{q_0}(u_0),\qquad \alpha=M,
 \tag{274.1}
\]

and the strict numerical promotion ratio `gamma=11/5`. These are manifest
choices, not ranges intrinsic to the general C265 interface. The C266 profile
family is not reopened: no coefficient, profile, or new continuous range is
introduced, and the analysis below is conditional on a nonzero datum having
the displayed exact norm.

To expose amplitude scaling, write `u_0=lambda v_0`, and put

\[
 A=A_{q_0}(v_0),\qquad L=\|v_0\|_3,\qquad
 m=\lambda AT,\qquad \ell={L\over A}.
 \tag{274.2}
\]

Both `m` and `ell` are dimensionless. Under the exact Euler scaling
`u_lambda(t)=lambda v(lambda t)`, changing amplitude and inversely changing
time leaves `m` unchanged. Thus amplitude cannot buy analytic capacity while
preserving the same dimensionless Euler endpoint.

The definitions also impose the datum-independent normalization bound

\[
 0<\ell\le {1\over q_0},
 \tag{274.2a}
\]

because `A_{q0}(v0)>=q0 A_1(v0)>=q0||v0||_3` for every nonzero mean-zero
datum (with normalized Haar measure). This bound must be retained in the
scalar feasibility region; it is not a sufficient datum condition.

## 2. Shrinking-Wiener and tail capacity

With the frozen choice `M=alpha=lambda A`, the endpoint weight is

\[
 Q=q_0(1-MT)=q_0(1-m).
 \tag{274.3}
\]

The complete shrinking-Wiener feasibility gate is exactly

\[
 0<m<1-{1\over q_0}.
 \tag{274.4}
\]

For the four imported frozen weights, the upper margins are respectively

\[
 {1\over5},\quad {1\over3},\quad {1\over2},\quad {2\over3}.
 \tag{274.5}
\]

Equivalently, at an imported frozen physical horizon `T`, amplitude must satisfy

\[
 0<\lambda A<{1-q_0^{-1}\over T}.
 \tag{274.6}
\]

When (274.4) holds, every generated shell has the exact capacity bound

\[
 \sum_{|k|_\infty=n}|\widehat u_k(t)|_2
 \le \lambda A\,[q_0(1-\lambda At)]^{-n}.
 \tag{274.7}
\]

This controls the complete retained--tail and tail--tail sums, with shell count
`24n^2+2`, but it does not determine their signed component boxes without the
retained Fourier coefficients.

## 3. Picard and cubature gates

After setting dimensionless time `s=lambda A t` and normalizing the field,
reference path, and every retained box by `lambda A`, the Euler equation and
the C265 Picard conditions retain exactly their form:

\[
 \widetilde E_j^{in}+[0,\Delta s_j]\widetilde D_j
 \subset\operatorname{int}\widetilde E_j,
 \qquad
 \widetilde E_j^{in}+\Delta s_j\widetilde D_j
 \subset\widetilde E_j^{out}.
 \tag{274.8}
\]

Here `widetilde D_j` still contains the datum-dependent ordered convolution,
Leray projections, and componentwise omitted-convolution boxes. No scalar
inequality in `(q0,m,ell)` is equivalent to (274.8).

For endpoint cubic bounds `C_0<=U_0` and `C_T>=L_T`, the exact cubature gate is

\[
 L_T>\gamma^3U_0.
 \tag{274.9}
\]

At the frozen numerical lead `gamma=11/5`, this is

\[
 125L_T>1331U_0.
 \tag{274.10}
\]

For the theorem-level factor two gate it is `L_T>8U_0`. Cubic quantities scale
by `lambda^3`, so amplitude cancels from both tests.

## 4. Necessary L3 displacement

Every strict endpoint ratio `||u(T)||_3>gamma||u(0)||_3` necessarily satisfies

\[
 \|u(T)-u(0)\|_3>(\gamma-1)\|u(0)\|_3.
 \tag{274.11}
\]

The Wiener cap also gives

\[
 \|\partial_tu\|_3\le A_1(F(u))
 \le M^2\kappa_1(Q),\qquad
 \kappa_1(Q)=\max_{n\ge1}{n\over Q^n}.
 \tag{274.12}
\]

Consequently a necessary dimensionless capacity inequality is

\[
 (\gamma-1)\ell<m\kappa_1\!\left(q_0(1-m)\right).
 \tag{274.13}
\]

For the imported frozen lead this reads

\[
 {6\over5}\ell<m\kappa_1\!\left(q_0(1-m)\right).
 \tag{274.14}
\]

This gate is necessary, not sufficient. In particular, lowering amplitude at
fixed `T` lowers `m` and therefore reduces accessible displacement; scaling
time inversely restores exactly the same `m` and creates no new capacity.

## 5. Inviscid-transfer capacity

Write the transfer slack and shrink rate as

\[
 e={\epsilon\over\lambda A}>0,
 \qquad b={\beta\over\lambda A}.
 \tag{274.15}
\]

The C265 radius gates become

\[
 1<\rho_0<Q,
 \qquad b\ge1+e,
 \qquad \rho_0(1-bm)>1.
 \tag{274.16}
\]

For prescribed `e`, such `rho0,b` exist exactly when

\[
 (1+e)m<1-{1\over Q},
 \qquad Q=q_0(1-m).
 \tag{274.17}
\]

For some positive slack `e`, the exact reduced condition is

\[
 m<1-{1\over Q}
 \quad\Longleftrightarrow\quad
 q_0(1-m)^2>1.
 \tag{274.18}
\]

Thus (274.18), not merely (274.4), is the scalar capacity gate for a positive
shrinking-Wiener inviscid transfer.

For `r=rho0/Q`, define exactly

\[
 k_j(r)=\max_{n\ge1}n^jr^n,
 \qquad x=mk_1(r),
 \qquad
 B=mk_2(r){e^x-1\over x},
 \tag{274.19}
\]

with the quotient equal to one at `x=0`. A certificate must replace `B` by a
positive rational outward upper bound `B_up`. If rational endpoint witnesses
`a,delta>0` satisfy

\[
 a^3\ge U_0,\qquad (2a+\delta)^3<L_T,
 \tag{274.20}
\]

then the effective-viscosity gate is

\[
 0<\nu<{\min(\epsilon,\delta)\over B_{up}}.
 \tag{274.21}
\]

Here `epsilon` and `delta` belong to the already fixed certificate at amplitude
`lambda`; they are not the normalized slack `e`. If that completed certificate
is subsequently rescaled by a new factor `mu`, then at fixed physical
viscosity the exact amplitude condition and terminal time are

\[
 \mu>{\nu_{phys}B_{up}\over\min(\epsilon,\delta)},
 \qquad t_{phys}={T\over\mu}.
 \tag{274.22}
\]

Using `lambda` again in (274.22) would conflate the candidate-amplitude
parameter in (274.2) with this later C265 physical-viscosity rescaling. The
later scaling preserves a crossing already proved by (274.8)--(274.10); it
cannot prove the crossing or repair failure of (274.13) or (274.18).

## 6. Classification

The scalar region, including (274.2a), is nonempty: for every imported `q0`,
sufficiently small positive `m` satisfies (274.18), and sufficiently small
positive `ell` is not excluded by (274.13). Hence the framework has no
datum-free contradiction.
But `ell`, all signed omitted convolutions, every strict Picard inclusion, and
both endpoint cubature bounds require an actual datum and enclosed orbit.
Under the frozen instruction `no datum`, exact replay therefore stops at a
missing-input wall.

`ND274-C265-CERTIFICATE-CAPACITY: WALL`
