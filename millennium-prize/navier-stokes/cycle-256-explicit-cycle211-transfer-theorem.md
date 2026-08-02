# Cycle 256: explicit Cycle 211 transfer for a Cycle 255 certificate

## Decision

The Cycle 211 inviscid-limit step can be made explicit using only the uniform
analytic vorticity bound and the directed endpoint cubature in an eventual
Cycle 255 certificate. No Euler crossing is assumed here. The result is a
conditional transfer theorem and a formula that the validator can evaluate if
and only if a strict directed endpoint margin is present.

All norms and Fourier coefficients below use normalized Haar measure on the
standard square torus. Put

\[
  K\theta=\nabla^\perp\Delta^{-1}\theta,
  \qquad \widehat{K\theta}(k)=-{ik^\perp\over |k|_2^2}\widehat\theta(k).
                                                               \tag{256.1}
\]

## 1. Certificate inputs

Let `v` be the smooth mean-zero Euler velocity certified on an oriented
interval `[0,T]`, with vorticity `omega`. The orientation may be the Cycle 255
forward orbit or its exact Euler time reversal. Suppose the certificate gives

\[
  A_Q(\omega(t))=\sum_{k\ne0}Q^{|k|_1}|\omega_k(t)|\le M
  \quad(0\le t\le T),\qquad Q>1.                       \tag{256.2}
\]

For a forward Cycle 255 orbit one may take exactly

\[
  Q=q_*:=q_0(1-\alpha T).                              \tag{256.3}
\]

Indeed `q(t)>=q_*` and (255.4) imply (256.2). The same constant works after
time reversal, since reversal only changes the sign and order of the
vorticities.

Let the directed endpoint cubature give

\[
  \int|v(0)|^3\le C_{\rm in},\qquad
  \int|v(T)|^3\ge C_{\rm out},                         \tag{256.4}
\]

where `C_in>0`. Define the exact endpoint margin

\[
  d:=C_{\rm out}^{1/3}-2C_{\rm in}^{1/3}.              \tag{256.5}
\]

Thus `d>0` is equivalent to the strict integer/rational test
`C_out>8 C_in`; no approximate cube-root comparison is needed. For the
forward conclusion (255.11), use `C_in=U_0` and `C_out=L_T`. If a reverse
crossing is certified instead, use `C_in=U_T` and `C_out=L_0` and reverse the
enclosed Euler orbit before applying this theorem.

Nothing below asserts `d>0`. If the directed cubature does not prove it, the
transfer gate fails closed and `mu_0` is not positive.

## 2. Exact constants from the Wiener bound

For `j=1,2` define

\[
  \kappa_j(Q):=\max_{n\ge1}{n^j\over Q^n}.             \tag{256.6}
\]

This is a finite exact computation. If `N_j` is the least positive integer
satisfying

\[
  (N_j+1)^j\le QN_j^j,
\]

then `kappa_j(Q)=N_j^j/Q^(N_j)`; equality in the displayed test merely gives
the same value at `N_j+1`. Set

\[
  G:=M\kappa_1(Q),\qquad H:=M\kappa_2(Q),               \tag{256.7}
\]

and

\[
  \Phi(G,T):=
  \begin{cases}
    (e^{GT}-1)/G,&G>0,\\
    T,&G=0.
  \end{cases}                                          \tag{256.8}
\]

The analytic certificate immediately gives

\[
  \|\nabla\omega(t)\|_\infty\le G,
  \qquad \|\Delta\omega(t)\|_2\le H.                  \tag{256.9}
\]

These estimates use `|k|_2<=|k|_1`, Parseval, and
`n^j<=kappa_j(Q)Q^n`; they introduce no unrecorded Sobolev constant.

The only velocity conversion needed below also has a fixed explicit constant:

\[
  \|K\theta\|_3\le4\|\theta\|_2.                      \tag{256.10}
\]

To verify (256.10), scalar Hausdorff--Young and Holder give, for each
component `ell=1,2`,

\[
 \|(K\theta)_\ell\|_3
 \le\left(\sum_{k\ne0}{|\theta_k|^{3/2}\over|k|_2^{3/2}}
       \right)^{2/3}
 \le\|\theta\|_2
       \left(\sum_{k\ne0}|k|_2^{-6}\right)^{1/6}.
\]

The shell `|k|_infinity=n` has `8n` points and `|k|_2>=n`, so the last
lattice sum is at most `8 sum_(n>=1)n^-5<16`. Its sixth root is less than
`2`. Finally `|Ktheta|<=|(Ktheta)_1|+|(Ktheta)_2|` and Minkowski prove the
stated rational constant `4`. A validator may replace `4` by any smaller
rigorously directed vector-valued bound, but must not do so without replaying
that bound.

## 3. Quantitative inviscid limit

Let `w_mu` be the two-dimensional Navier--Stokes solution with viscosity
`mu>0` and the same initial velocity as the oriented Euler orbit. Write

\[
  \xi=\operatorname{curl}w_\mu,
  \qquad \theta=\xi-\omega,
  \qquad z=w_\mu-v=K\theta.
\]

Subtracting the vorticity equations gives

\[
 \partial_t\theta+w_\mu\mathbin\cdot\nabla\theta
 +z\mathbin\cdot\nabla\omega
 =\mu\Delta\theta+\mu\Delta\omega,
 \qquad \theta(0)=0.                                  \tag{256.11}
\]

The normalized `L^2` energy identity, (256.9), and
`||K theta||_2<=||theta||_2` imply, for the upper Dini derivative at zero,

\[
 {d^+\over dt}\|\theta\|_2
 \le G\|\theta\|_2+\mu H.                             \tag{256.12}
\]

Consequently

\[
 \sup_{0\le t\le T}\|w_\mu(t)-v(t)\|_3
 \le 4\mu H\Phi(G,T).                                 \tag{256.13}
\]

No Navier--Stokes norm is bootstrapped in this argument. Global smoothness of
the two-dimensional viscous solution is standard, and all coefficients on the
right side of (256.13) come from the certified Euler orbit.

## 4. Explicit threshold and transfer theorem

If the endpoint gate proves `d>0`, define

\[
 \boxed{\displaystyle
   \mu_0={d\over4H\Phi(G,T)}
   ={C_{\rm out}^{1/3}-2C_{\rm in}^{1/3}
      \over
      4M\kappa_2(Q)\,
      \Phi(M\kappa_1(Q),T)}.}                          \tag{256.14}
\]

For every `0<mu<mu_0`, (256.4), (256.13), and equality of the viscous and
Euler initial data give

\[
\begin{aligned}
 \|w_\mu(T)\|_3
 &\ge \|v(T)\|_3-4\mu H\Phi(G,T)\\
 &>2C_{\rm in}^{1/3}
 \ge2\|w_\mu(0)\|_3.                                  \tag{256.15}
\end{aligned}
\]

This proves the specialized Cycle 211 theorem: a passing directed Cycle 255
Euler certificate transfers to every effective viscosity in the open interval
`(0,mu_0)`. Formula (256.14) supplies no positive threshold when `d<=0`; an
Euler crossing is a checked premise, not an assumption hidden in the theorem.

For exact rational replay without algebraic-number arithmetic, the artifact
may instead include rational numbers `a>0` and `delta>0` satisfying

\[
  a^3\ge C_{\rm in},\qquad (2a+\delta)^3<C_{\rm out}.   \tag{256.16}
\]

Then `0<delta<d`, and the smaller entirely directed threshold

\[
  \mu_0^{\rm rat}:={\delta\over4H\Phi(G,T)}             \tag{256.17}
\]

is valid. The exponential in (256.8) is evaluated by a directed rational upper
bound when certifying a rational lower bound for `mu_0`; a Taylor remainder or
an interval exponential is acceptable only if replayed fail-closed.

## 5. Fixed positive physical viscosity

Fix any physical viscosity `nu>0`. For `lambda>0` define

\[
  u_\lambda(t,x)=\lambda w_{\nu/\lambda}(\lambda t,x),
  \qquad
  p_\lambda(t,x)=\lambda^2p_{\nu/\lambda}(\lambda t,x). \tag{256.18}
\]

This is an exact Navier--Stokes solution with viscosity `nu`. Set

\[
  \boxed{\lambda_0(\nu)={\nu\over\mu_0}}.              \tag{256.19}
\]

Every `lambda>lambda_0(nu)` has effective viscosity
`nu/lambda<mu_0`, initial datum `lambda v(0)`, and physical terminal time
`T/lambda`; hence

\[
  \|u_\lambda(T/\lambda)\|_3
  >2\|u_\lambda(0)\|_3.                                \tag{256.20}
\]

The lift `(u_lambda,1,u_lambda,2,0)`, independent of `x_3`, solves the
three-dimensional periodic equation with the same viscosity. Under normalized
Haar measure its `L^3` ratio is exactly (256.20); under unnormalized product
measure the common third-direction factor also cancels.

Amplitude scaling preserves the ratio and only makes the effective viscosity
smaller. It cannot supply `d>0`. Since no Cycle 255 crossing certificate is
currently present, this cycle proves only the transfer theorem and no
Navier--Stokes counterexample, regularity result, or Millennium result.
