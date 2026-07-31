# Cycle 197: exact tangent map and the quadratic-jet gate

## Relative pair tangent theorem

Let `k` be a field of characteristic zero, let `S` be locally of finite type
over `k`, and let

\[
 p_+:H_+\longrightarrow S,\qquad p_-:H_-\longrightarrow S
\]

be two relative Hilbert/Chow charts.  At points `h_+`, `h_-` over `s`, put
`H=H_+ \times_S H_-` and `h=(h_+,h_-)`.  Functoriality of Zariski tangent
spaces gives the exact formula

\[
 T_hH=
 \ker\left(T_{h_+}H_+\oplus T_{h_-}H_-
 \xrightarrow{dp_+-dp_-}T_sS\right).                 \tag{197.1}
\]

Consequently the image in the base is

\[
 \boxed{\operatorname {im}(dp_h)=
 \operatorname {im}(dp_+)\cap\operatorname {im}(dp_-).}           \tag{197.2}
\]

This is an intersection, not a sum.  In particular, signs in a signed cycle
cannot cancel between the two effective factors.

Suppose each chart has a relative obstruction presentation

\[
 \rho_\pm:T_sS\longrightarrow O_\pm,
 \qquad \operatorname {im}(dp_\pm)=\ker\rho_\pm.                  \tag{197.3}
\]

For an lci Hilbert chart, (197.3) is the standard embedded obstruction map;
for a Chow chart it is a hypothesis to be checked on the selected local chart.
Then

\[
 \boxed{\operatorname {im}(dp_h)
 =\ker\rho_+\cap\ker\rho_-
 =\ker(\rho_+\oplus\rho_-).}                                     \tag{197.4}
\]

Thus a finite matrix certificate consists of matrices for `rho_+` and
`rho_-`: if `R_+` and `R_-` are written in one basis of `T_sS`, the three base
image dimensions are

\[
 n-\operatorname {rank}R_+,\quad
 n-\operatorname {rank}R_-,\quad
 n-\operatorname {rank}\begin{pmatrix}R_+\\R_-\end{pmatrix}.     \tag{197.5}
\]

## Exact second-order jet

The quadratic gate also has a finite presentation.  Complete at the selected
points and choose base parameters `t=(t_1,...,t_n)` and chart variables `x_+`
and `x_-`.  Write equations through degree two as

\[
 f_\pm(t,x_\pm)=A_\pm x_\pm+B_\pm t+q_\pm(t,x_\pm)+O(3),          \tag{197.6}
\]

where `q_+` and `q_-` are homogeneous quadratic vectors.  A section over the
second infinitesimal neighborhood of `s` has the form

\[
 x_\pm(t)=U_\pm t+W_\pm(t,t)\pmod{(t)^3}.                         \tag{197.7}
\]

It exists exactly when the following finite linear systems hold:

\[
 A_\pm U_\pm+B_\pm=0,                                             \tag{197.8}
\]

and, for every `1 <= a <= b <= n`,

\[
 A_\pm W_{\pm,ab}
 +[t_at_b]q_\pm(t,U_\pm t)=0.                                    \tag{197.9}
\]

The same base variables occur on both sides; there is no independent positive
and negative base acceleration.  Equivalently, for one curvilinear jet

\[
 t=\epsilon v+\epsilon^2z,\qquad
 x_\pm=\epsilon u_\pm+\epsilon^2w_\pm,
 \qquad \epsilon^3=0,
\]

the exact equations are

\[
 A_\pm u_\pm+B_\pm v=0,
\qquad
 A_\pm w_\pm+B_\pm z+q_\pm(v,u_\pm)=0.                           \tag{197.10}
\]

Equations (197.8)--(197.9), over the coefficient field of the equations, are
the requested finite linear algebra certificate.  A verifier input must supply
`A_+`, `B_+`, `q_+`, `A_-`, `B_-`, `q_-`, a rank-`n` first-order solution
`U_+`, `U_-`, and quadratic solutions `W_+`, `W_-`.  Passing the quadratic
systems proves lifting only to order two; it is not an all-order formal
effectivity or finite-determinacy theorem.

## Abelian-sixfold certificate

Take

\[
 A_0=E_i^3\times E_i^3,
 \qquad Q=\operatorname {diag}(1,1,3),
\]

and let `Gamma_k` be the graph of scalar multiplication by
`u^k`, where `u=2+i`.  Every `Gamma_k` is a smooth codimension-three lci:

\[
 \Gamma_k=D_{u^k,1}\cap D_{u^k,2}\cap D_{u^k,3},
 \qquad D_{a,j}=\{z_{j+3}-az_j=0\}.                               \tag{197.11}
\]

On a rational matrix model whose scalar extension is the nine-dimensional PEL
tangent, the exact graph obstruction is

\[
 \rho_k(B)=Q^{-1}B^t-5^kB.                                       \tag{197.12}
\]

In row-major bases its entries are rational.  Direct elimination gives

\[
 \operatorname {rank}(\rho_0)=6,
 \qquad \operatorname {rank}(\rho_k)=9\quad(1\leq k\leq6).       \tag{197.13}
\]

For the explicit lci pair `(Gamma_0,Gamma_1)`, the individual base images have
dimensions `3` and `0`, while the fiber-product pair image is their
intersection and has dimension `0`.  This separates the individual image from
the pair image in the simplest exact example.

For the Cycle 169 effective projector pair, stack the graph maps on each side:

\[
 R_+=(\rho_0,\rho_2,\rho_4,\rho_5),
 \qquad R_-=(\rho_1,\rho_3,\rho_6).                               \tag{197.14}
\]

Both stacked matrices have rank nine, and so does their joint stack.  Hence

\[
 \boxed{\dim\operatorname {im}(dp_+)=
 \dim\operatorname {im}(dp_-)=
 \dim\operatorname {im}(dp_h)=0.}                                \tag{197.15}
\]

The required rank-nine first-order section therefore does not exist for this
pair.  Its second-order rank-nine test is not failed by a computed Hessian; it
is **not reached**, because (197.8) already has no rank-nine solution.  This is
an exact negative certificate for the displayed pair, not an obstruction to a
different rationally equivalent pair in another finite-type incidence chart.

The machine-readable theorem data are in
`cycle197_tangent_jet_input.json`.  Verify all Gaussian powers, obstruction
matrix ranks, and base-image intersections with

```sh
python3 millennium-prize/hodge/verify_cycle197_relative_chow_jet.py
```

For a future positive pair, extend `second_order_template` by the coefficient
arrays in (197.6) and witnesses in (197.8)--(197.9); those are the complete
verifier inputs through order two.
