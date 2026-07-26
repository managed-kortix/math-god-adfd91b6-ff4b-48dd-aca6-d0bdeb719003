# Cycle 41: exact sparse-impulse recurrence for the H defect

## 1. Setup

Work in `L^2((0,1),dx)` and put

\[
 L_j=\log j,\qquad C_j=L_jL_{j+1},
\]

\[
 U_j=\chi+\sum_{a\le j}\mu(a)\rho_a,
 \qquad
 D_j=\sum_{a\le j}\mu(a)L_a\rho_a,
\]

\[
 H_j=\|D_j\|^2-C_j\|U_j\|^2.
\]

Write

\[
 g_a=\langle\chi,\rho_a\rangle,
 \qquad G_{a,b}=\langle\rho_a,\rho_b\rangle.
\]

To describe the transition from `n` to `n+1`, set `q=n+1` and

\[
 V_{q-1}=\|U_{q-1}\|^2,
 \qquad u_q=\langle U_{q-1},\rho_q\rangle,
 \qquad d_q=\langle D_{q-1},\rho_q\rangle,
\]

\[
 \Delta C_q=C_q-C_{q-1}
 =L_q(L_{q+1}-L_{q-1}),
 \qquad \delta_q=L_{q+1}-L_q.
\]

The vector updates are

\[
 U_q=U_{q-1}+\mu(q)\rho_q,
 \qquad D_q=D_{q-1}+\mu(q)L_q\rho_q.                 \tag{41.1}
\]

## 2. Exact one-step recurrence

Expanding (41.1), with every inner product taken against the old vectors,
gives

\[
 \|U_q\|^2=V_{q-1}+2\mu(q)u_q+\mu(q)^2G_{q,q},       \tag{41.2}
\]

\[
 \|D_q\|^2=\|D_{q-1}\|^2+2\mu(q)L_qd_q
              +\mu(q)^2L_q^2G_{q,q}.                 \tag{41.3}
\]

Consequently

\[
\boxed{\begin{aligned}
 H_q-H_{q-1}={}&-\Delta C_qV_{q-1}\\
 &+2\mu(q)\big(L_qd_q-C_qu_q\big)\\
 &+\mu(q)^2\big(L_q^2-C_q\big)G_{q,q}.
\end{aligned}}                                                   \tag{41.4}
\]

Since `L_q^2-C_q=-L_q\delta_q`, the last term is nonpositive and is
present exactly when `q` is squarefree.

If `\mu(q)=0`, then the vectors do not move, but the changing radial scale
still produces a drift:

\[
 \boxed{H_q=H_{q-1}-\Delta C_q\|U_{q-1}\|^2.}         \tag{41.5}
\]

If `\mu(q)=\varepsilon\in\{-1,1\}`, then

\[
\boxed{\begin{aligned}
 H_q={}&H_{q-1}-\Delta C_q\|U_{q-1}\|^2\\
 &+2\varepsilon\big(L_q\langle D_{q-1},\rho_q\rangle
                    -C_q\langle U_{q-1},\rho_q\rangle\big)\\
 &-L_q\delta_qG_{q,q}.
\end{aligned}}                                                   \tag{41.6}
\]

Thus `H_q` is not constant across a nonsquarefree index. Only the vector
impulse vanishes there; the coefficient drift remains.

## 3. Full Gram form of the increment

All old-vector quantities in (41.4) are finite Gram contractions:

\[
 u_q=g_q+\sum_{a<q}\mu(a)G_{a,q},
 \qquad
 d_q=\sum_{a<q}\mu(a)L_aG_{a,q},                     \tag{41.7}
\]

and

\[
\begin{aligned}
 V_{q-1}={}&1+2\sum_{a<q}\mu(a)g_a
 +\sum_{a<q}\mu(a)^2G_{a,a}\\
 &+2\sum_{1\le a<b<q}\mu(a)\mu(b)G_{a,b}.           \tag{41.8}
\end{aligned}
\]

Substitution gives the completely opened recurrence

\[
\boxed{\begin{aligned}
H_q-H_{q-1}={}&-\Delta C_q\left(
 1+2\sum_{a<q}\mu(a)g_a
 +\sum_{a<q}\mu(a)^2G_{a,a}
 +2\sum_{a<b<q}\mu(a)\mu(b)G_{a,b}\right)\\
&-2\mu(q)C_qg_q\\
&+2\mu(q)\sum_{a<q}\mu(a)(L_qL_a-C_q)G_{a,q}\\
&+\mu(q)^2(L_q^2-C_q)G_{q,q}.
\end{aligned}}                                                   \tag{41.9}
\]

The first line changes the coefficients of every previously present Gram
entry. The remaining three lines are precisely the new `q`th Gram row and
diagonal. In particular, (41.9) contains the constant--old, old--old,
constant--new, old--new, and new--new inner products; no Gram channel is
omitted.

For the restricted Vasyunin Gram matrix used in Cycle 40,

\[
 g_q={L_q+1-\gamma\over q},
 \qquad
 G_{q,q}={\log(2\pi)-\gamma\over q}-{1\over q^2},     \tag{41.10}
\]

while the off-diagonal `G_{a,q}` is given by the complete Vasyunin formula.

## 4. Sparse impulse and compensated process

Define the norm increments

\[
 \Delta V_q=\|U_q\|^2-\|U_{q-1}\|^2
 =2\mu(q)u_q+\mu(q)^2G_{q,q},                         \tag{41.11}
\]

\[
 \Delta W_q=\|D_q\|^2-\|D_{q-1}\|^2
 =2\mu(q)L_qd_q+\mu(q)^2L_q^2G_{q,q}.                \tag{41.12}
\]

The squarefree-supported impulse is

\[
\boxed{J_q:=\Delta W_q-C_q\Delta V_q
 =2\mu(q)(L_qd_q-C_qu_q)
  -\mu(q)^2L_q\delta_qG_{q,q}.}                       \tag{41.13}
\]

It satisfies `J_q=0` whenever `\mu(q)=0`. Equation (41.4) now has the
drift-plus-sparse-impulse form

\[
 \boxed{H_q-H_{q-1}=-\Delta C_qV_{q-1}+J_q.}          \tag{41.14}
\]

For a fixed starting index `A`, define the drift-compensated defect

\[
 \widehat H_N^{(A)}
 :=H_N+\sum_{q=A+1}^{N}\Delta C_q\|U_{q-1}\|^2.
                                                                    \tag{41.15}
\]

Then

\[
 \widehat H_A^{(A)}=H_A,
 \qquad
 \widehat H_N^{(A)}-\widehat H_{N-1}^{(A)}=J_N.       \tag{41.16}
\]

Hence the compensated process changes only at squarefree indices.

The zero events can also be compressed without compensation. If
`r<q\le s` all satisfy `\mu(q)=0`, then `U_q=U_r` throughout the run and

\[
 \boxed{H_s=H_r-(C_s-C_r)\|U_r\|^2.}                 \tag{41.16a}
\]

More generally, let `s_1<s_2<\cdots` enumerate the squarefree indices. Between
two successive events, (41.14) collapses to the event-time recurrence

\[
 \boxed{H_{s_{k+1}}
 =H_{s_k}-(C_{s_{k+1}}-C_{s_k})\|U_{s_k}\|^2
   +J_{s_{k+1}}.}                                    \tag{41.16b}
\]

Thus one may retain either every deterministic drift step, as in (41.14), or
jump directly between squarefree events, as in (41.16b).

## 5. Cumulative telescope

Summing (41.14) from `q=A+1` through `N` gives the exact sparse cumulative
representation

\[
\boxed{\begin{aligned}
H_N={}&H_A-\sum_{q=A+1}^{N}(C_q-C_{q-1})\|U_{q-1}\|^2\\
&+\sum_{\substack{A<q\le N\\ \mu(q)\ne0}}
 \left[2\mu(q)(L_qd_q-C_qu_q)
       -L_q\delta_qG_{q,q}\right].
\end{aligned}}                                                   \tag{41.17}
\]

Equivalently,

\[
 \boxed{\widehat H_N^{(A)}
 =H_A+\sum_{\substack{A<q\le N\\ \mu(q)\ne0}}J_q.} \tag{41.18}
\]

There is also a useful product-rule check. From (41.11),

\[
 C_qV_q-C_{q-1}V_{q-1}
 =\Delta C_qV_{q-1}+C_q\Delta V_q.                   \tag{41.19}
\]

Using `J_q=\Delta W_q-C_q\Delta V_q` in (41.17), both norm channels
telescope separately:

\[
\begin{aligned}
H_N-H_A
&=\sum_{q=A+1}^{N}\Delta W_q
  -\sum_{q=A+1}^{N}
    \big(\Delta C_qV_{q-1}+C_q\Delta V_q\big)\\
&=\|D_N\|^2-\|D_A\|^2
  -\big(C_N\|U_N\|^2-C_A\|U_A\|^2\big).             \tag{41.20}
\end{aligned}
\]

This recovers `H_N-H_A` and verifies the indexing and all diagonal and cross
terms. The decomposition is exact bookkeeping: it supplies no sign for the
drift, the squarefree impulses, or their cumulative balance.
