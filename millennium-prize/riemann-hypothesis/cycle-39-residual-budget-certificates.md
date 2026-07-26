# Cycle 39: residual-budget recurrence and finite-horizon certificates

## 1. Exact recurrence

Let `P_n>=0`, `c>0`, and

\[
w_n={\log(1+1/n)\over\log(n+1)},\quad
T_a=\sum_{n=a}^\infty w_nP_n,\quad Q_a=P_a-cT_a.
\tag{39.1}
\]

The definitions require `T_a<infinity`. Since `T_a=w_aP_a+T_{a+1}`,

\[
\boxed{Q_a-Q_{a+1}=d_a:=P_a-P_{a+1}-cw_aP_a.}             \tag{39.2}
\]

In the RH normalization `c=2kappa`. Using `P_a-P_{a+1}=2h_aE_a` and
`w_a=h_a log a` gives

\[
\boxed{d_a=h_a(2E_a-c(\log a)P_a).}                       \tag{39.3}
\]

For `a<b`, telescoping yields the exact finite identity

\[
\boxed{Q_a-Q_b=S(a,b):=P_a-P_b-c\sum_{a\le n<b}w_nP_n
=\sum_{n=a}^{b-1}d_n.}                                    \tag{39.4}
\]

Thus renewal from `a` to `b` is exactly `S(a,b)>=0`, equivalently `Q_b<=Q_a`.

## 2. Sign crossings

Fix `a` and write `S_a(b)=S(a,b)`. Then

\[
Q_b=Q_a-S_a(b).                                           \tag{39.5}
\]

Consequently:

1. If `Q_a>=0`, the first negative index is the first `b>a` with
   `S_a(b)>Q_a`; at all earlier `j`, `S_a(j)<=Q_a`.
2. If `Q_a<0`, the first nonnegative index is the first `b>a` with
   `S_a(b)<=Q_a`; at all earlier `j`, `S_a(j)>Q_a`.
3. If `Q_a=0`, return to zero at `b` is equivalent to `S(a,b)=0`.
4. Under the desired global invariant `Q_n>=0`, a zero at `a` implies
   `S(a,b)<=0` for all `b>a`, hence `d_a<=0`. Equality recurrence is a
   nonnegative excursion of `Q` that eventually returns to zero.

In particular, positive one-step surplus is impossible at a zero boundary,
but negative one-step surplus is harmless if later positive surpluses repay it.
Pointwise positivity of `d_a` is therefore neither necessary nor the right
inductive target.

## 3. Finite-horizon certificates

Choose `M>a` and define

\[
\widehat Q_a^{(M)}=P_a-c\sum_{n=a}^{M-1}w_nP_n.
\tag{39.6}
\]

Then `Q_a=widehat Q_a^(M)-cT_M`. If a rigorous common-tail estimate gives
`0<=L_M<=T_M<=U_M`, then simultaneously for every `a<=M`,

\[
\boxed{\widehat Q_a^{(M)}-cU_M\le Q_a
\le\widehat Q_a^{(M)}-cL_M.}                              \tag{39.7}
\]

Comparisons are sharper: for `a<b<=M`, `Q_a-Q_b=S(a,b)` is finite and has no
tail error. Thus one enclosed anchor plus finite surplus sums certifies all
crossings through `M`.

With outward-rounded values `P_n in [p_n^-,p_n^+]`, a direct valid enclosure is

\[
p_a^- -c\sum_{n=a}^{M-1}w_np_n^+-cU_M
\le Q_a\le
p_a^+ -c\sum_{n=a}^{M-1}w_np_n^- -cL_M.                   \tag{39.8}
\]

Positive directed interval enclosures may also replace the exact weights.

### Explicit tail majorants

Any proved `P_n<=B_n` for `n>=M`, with summable `w_nB_n`, gives
`U_M=sum_(n>=M)w_nB_n`. Two concrete forms are:

* If `B_n=C/(log n)^p`, `p>0`, and `r_M=log(M+1)/log M`, then
  \[
  \boxed{U_M\le {Cr_M^p\over p(\log M)^p}.}               \tag{39.9}
  \]
  Write `w_n=Delta_n/log(n+1)`, where
  `Delta_n=log(n+1)-log n`, insert
  `(log(n+1)/log n)^p<=r_M^p`, and use the right-endpoint Riemann sum for
  `int_(log M)^infinity x^(-p-1)dx`.
* If `B_n=Cn^(-alpha)`, `alpha>0`, then
  \[
  \boxed{U_M\le {C\over\log M}
  \left(M^{-\alpha-1}+{M^{-\alpha}\over\alpha}\right).}  \tag{39.10}
  \]
  This follows from `w_n<=1/(n log n)` and the integral test.

For the RH approximants, no unconditional summable majorant for `P_n` is
currently available in this route. Such a majorant would force
`liminf P_n=0` and already contain major RH content. A finite plot alone cannot
certify `Q_a>=0`: it needs a proved tail majorant, a terminal tail-ratio bound,
or an inductive continuation argument.

## 4. Plausible inductive invariant

For `P_a>0`, use the dimensionless tail-load ratio

\[
H_a={cT_a\over P_a}.                                      \tag{39.11}
\]

The target `Q_a>=0` is exactly `H_a<=1`. Its local backward recurrence is

\[
\boxed{H_a=cw_a+{P_{a+1}\over P_a}H_{a+1}.}               \tag{39.12}
\]

Propagating only `H_(a+1)<=1` would require
`P_(a+1)<=(1-cw_a)P_a`, the known overly strong unit decrement. The correct
form is blockwise: for every `b>a`,

\[
\boxed{H_a={c\sum_{a\le n<b}w_nP_n+P_bH_b\over P_a}.}     \tag{39.13}
\]

Let `0<=theta_a<=1` be a barrier. If `H_b<=theta_b`, the finite inequality

\[
\boxed{c\sum_{a\le n<b}w_nP_n+\theta_bP_b
\le\theta_aP_a}                                           \tag{39.14}
\]

propagates `H_a<=theta_a`. This gives a rigorous certificate: establish a
terminal `cT_M<=theta_MP_M`, choose acyclic parents `b(a)>a`, and verify
(39.14) backward. Arbitrarily many negative unit surpluses are allowed inside
each parent block.

The plausible minimal invariant is therefore

\[
\boxed{\mathcal I(a): H_a\le1,
\quad\hbox{propagated along complete favorable blocks by (39.14).}} \tag{39.15}
\]

A stronger computational candidate is `theta_a=1-epsilon_a`, with positive
slack decreasing slowly to zero. The profile `epsilon_a=beta/log a` is a
reasonable diagnostic, not a theorem; it asks for

\[
c\sum_{a\le n<b}w_nP_n+
\left(1-{\beta\over\log b}\right)P_b
\le\left(1-{\beta\over\log a}\right)P_a.                  \tag{39.16}
\]

This stores surplus across bad unit steps and supplies the terminal slack a
finite-horizon proof needs. At the sharp barrier `theta=1`, (39.14) is bare
renewal. If strictness cannot be preserved, the complete invariant must append

\[
Q_a=0\Longrightarrow\exists b>a:\ S(a,b)=0,               \tag{39.17}
\]

which is exactly the equality-set recurrence of Cycle 38.

## 5. Verdict

All sign crossings are finite cumulative-surplus crossings under (39.2). The
promising proof architecture is backward block induction for `H_a`, anchored
by a rigorous terminal tail bound, not pointwise decrement induction. The open
arithmetic task is to prove (39.14) on a complete family of blocks together
with a noncircular terminal enclosure. No RH result is claimed.
