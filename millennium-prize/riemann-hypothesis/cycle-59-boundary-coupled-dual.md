# Cycle 59: boundary-coupled dual for the missing residual

Work in `H=L^2((1,infinity),dt/t^2)`. Fix `M<B` and put

\[
D=D_{M-1},\quad Z=\operatorname{span}\{U_{M-1},\rho_M,\ldots,\rho_{B-1}\}.
\]

For the optimal Cycle 55 staircase `g_M`, define

\[
E=I-\Pi_{Z\oplus\langle g_M\rangle},\quad r=ED,\quad R=\|r\|^2.
\]

Then

\[
\boxed{\|(I-\Pi_Z)D\|^2=W_M+R.}                  \tag{59.1}
\]

## Exact finite-cell dual

Let `K` be a finite collection of complete cells `I_k=(k,k+1)`. For a function
`h` supported on their union define

\[
A_k=\int_{I_k}h(t)/t\,dt,\quad B_k=\int_{I_k}h(t)/t^2\,dt,\quad A=\sum_kA_k.
\]

Write

\[
m=\sum_{a<M}{\mu(a)\over a},\quad \ell=\sum_{a<M}{\mu(a)\log a\over a},
\]
\[
u_k=1-\sum_{a<M}\mu(a)\lfloor k/a\rfloor,\quad
v_k=-\sum_{a<M}\mu(a)\log a\lfloor k/a\rfloor.
\]

The leading `1` in `u_k` is essential: `U_n` includes `chi`, whose reciprocal
image is the constant one. The exact conditions `h` orthogonal to `Z` and
`g_M` are

\[
\boxed{
\begin{aligned}
mA+\sum_ku_kB_k&=0,\\
A/q-\sum_k\lfloor k/q\rfloor B_k&=0 &&(M\le q<B),\\
\sum_{k<M}(\psi(k)B_k-c_MA_k)&=0.
\end{aligned}}                                                     \tag{59.2}
\]

All new-row equations share the boundary moment `A`; setting it to zero first
discards the remaining below-`M` coupling.

Put `lambda_k=log(1+1/k)`, `tau_k=1/(k(k+1))`, and
`Delta_k=tau_k-lambda_k^2>0`. The unique least-norm function with prescribed
moments is affine on each cell, with

\[
\boxed{\|h\|_{\min}^2=\sum_k
{\tau_kA_k^2-2\lambda_kA_kB_k+B_k^2\over\Delta_k}.}                \tag{59.3}
\]

Moreover `inner(r,h)=ell A+sum_k v_k B_k`. Hence duality gives the explicit
arithmetic certificate

\[
\boxed{R\ge\Omega_K:=\sup_{(A_k,B_k)\ne0,\ (59.2)}
{\left|\ell A+\sum_kv_kB_k\right|^2\over
\displaystyle\sum_k
{\tau_kA_k^2-2\lambda_kA_kB_k+B_k^2\over\Delta_k}}.}              \tag{59.4}
\]

This replaces a complete-Gram projection by a weighted finite projection of an
explicit Möbius divisor-floor vector against explicit floor constraints.

## Corrected matched-shell no-go

Assume `B<=2M` and take `K={M,...,B-1}`. Then the floor equations and old `U`
equation reduce exactly to

\[
\boxed{m_{B-1}A=0,\qquad m_{B-1}=\sum_{a<B}\mu(a)/a.}              \tag{59.5}
\]

If `m_(B-1)!=0`, triangular back-substitution forces `A=0` and every `B_k=0`,
so `Omega_K=0`. Cycle 56's unconditional wording omitted this nondegeneracy.
Moment-null functions remain possible but correlate with no affine old-state
trace. Surplus or remote cells can create feasible directions, but rank alone
does not make the numerator in (59.4) nonzero; remote cells are strongly
penalized because `Delta_k~1/(12k^4)`.

## Exact energy partition

Since `F_M=U_(M-1)-D_(M-1)/log M` and `U_(M-1)` belongs to `Z`,

\[
\boxed{(\log M)^2P_M=W_M+\mathcal K_{M,B}+R,\qquad
\mathcal K_{M,B}=(\log M)^2\|\Pi_ZF_M\|^2.}                       \tag{59.6}
\]

Thus `R>=r_M` is exactly the second-order complete-Gram capture estimate

\[
\mathcal K_{M,B}\le(\log M)^2P_M-W_M-r_M.                         \tag{59.7}
\]

The smallest observed `R` on certified windows through the Cycle 51 frontier
is `R_(220,231)=0.0584003056852557...`. The candidate
`R>=1/(4 log M)` survives that finite range, whereas `1/(3 log M)` fails at
`[219,231)`. These are diagnostics only.

The next target is a feasible vector in (59.4) whose physical Möbius
divisor-floor correlation pays `beta_2+delta_(M,B)`, or the equivalent capture
bound (59.7). Generic geometry cannot supply it. No additive-12 theorem or RH
result is claimed.
