# Cycle 41: gcd-aggregated Vasyunin packets for the weighted H block

## 1. Aggregate the block before estimating

Fix integers `2<=A<B`, and put

\[
 L_n=\log n,\qquad C_n=L_nL_{n+1},\qquad
 \beta_n={L_{n+1}-L_n\over L_nL_{n+1}^2}>0.
\]

The exact half-strength block residual is

\[
 \mathfrak R(A,B)=\sum_{A\le n<B}\beta_nH_n,
 \qquad H_n=\|D_n\|^2-C_n\|U_n\|^2.                 \tag{41.1}
\]

For `a,b<B`, define

\[
 Q_a=\sum_{\max(A,a)\le n<B}\beta_nC_n,
\]

\[
 R_{a,b}=\sum_{\max(A,a,b)\le n<B}
 \beta_n\bigl(C_n-(\log a)(\log b)\bigr).            \tag{41.2}
\]

Empty sums are zero. If `a,b` occur in (41.2), then `a,b<=n`, and hence

\[
 C_n-(\log a)(\log b)>0.                              \tag{41.3}
\]

Thus every nonempty `R_(a,b)` is strictly positive. Opening the norms only
after summing in `n` gives

\[
\boxed{\begin{aligned}
 \mathfrak R(A,B)={}&-Q_1-2\sum_{a<B}\mu(a)g_aQ_a\\
 &-\sum_{a<B}\mu(a)^2R_{a,a}G_{a,a}
 -2\sum_{1\le a<b<B}\mu(a)\mu(b)R_{a,b}G_{a,b},
\end{aligned}}                                                       \tag{41.4}
\]

where

\[
 g_a={\log a+1-\gamma\over a},\qquad
 G_{a,b}=\langle\rho_a,\rho_b\rangle_{L^2(0,1)}.
\]

Equation (41.4), rather than a termwise estimate of each `H_n`, is the useful
starting point. Notice also that `beta_n C_n=(L_(n+1)-L_n)/L_(n+1)`, which
provides a simple independent check on every `Q_a`.

## 2. Diagonal packet

Put `c_0=log(2 pi)-gamma`. The diagonal kernel is

\[
 G_{a,a}={c_0\over a}-{1\over a^2}>0,
\]

so the complete diagonal packet is

\[
 \boxed{\mathcal D_{A,B}
 =-\sum_{a<B}\mu(a)^2R_{a,a}
 \left({c_0\over a}-{1\over a^2}\right)\le0.}        \tag{41.5}
\]

It is strictly negative whenever the block sees a squarefree index. Therefore
there is no positive diagonal main term to dominate the off-diagonal. Any
successful block must receive compensation from the linear term or from
off-diagonal pairs of opposite Mobius sign.

## 3. Reduced-denominator off-diagonal packets

Write each `a<b` uniquely as

\[
 a=dp,\qquad b=dq,\qquad (p,q)=1,\qquad p<q.
\]

Only squarefree, pairwise-coprime triples contribute: if
`mu(dp)mu(dq)!=0`, then `p,q,d` are squarefree, `(d,pq)=1`, and

\[
 \mu(dp)\mu(dq)=\mu(p)\mu(q).                         \tag{41.6}
\]

For a reduced pair `(p,q)`, let

\[
 \mathcal A(p,q)=(q-p)\log(p/q)+(p+q)c_0
 -\pi\mathcal V(p,q),                                  \tag{41.7}
\]

\[
 \mathcal V(p,q)=V(p,q)+V(q,p),\qquad
 V(p,q)=\sum_{k=1}^{q-1}\{kp/q\}\cot(\pi k/q).
\]

Then

\[
 G_{dp,dq}={\mathcal A(p,q)\over2dpq}-{1\over d^2pq}. \tag{41.8}
\]

Aggregate all common gcds before estimating. With

\[
 M_j(p,q)=\mathop{\sum_{d<B/q}}_{\mu(dp)\mu(dq)\ne0}
 {R_{dp,dq}\over d^j}\qquad(j=1,2),                   \tag{41.9}
\]

the whole reduced-denominator packet is exactly

\[
\boxed{
 \mathcal O_{p,q}
 =-{\mu(p)\mu(q)\over pq}
 \left(\mathcal A(p,q)M_1(p,q)-2M_2(p,q)\right).}     \tag{41.10}
\]

This bracket has an exact sign which is obscured by the cotangent formula:

\[
 \mathcal A(p,q)M_1-2M_2
 =2pq\mathop{\sum_{d<B/q}}_{\mu(dp)\mu(dq)\ne0}
 R_{dp,dq}G_{dp,dq}>0                                  \tag{41.11}
\]

for every nonempty packet, because the fractional-part functions are positive
on a set of positive measure. Consequently

\[
 \boxed{\operatorname{sgn}\mathcal O_{p,q}
 =-\mu(p)\mu(q).}                                      \tag{41.12}
\]

This is the available exact pairing compensation: equal-Mobius-sign packets
are unfavorable, while opposite-Mobius-sign packets are favorable. It is a
positive packet identity, not a square for the full signed block.

Separating elementary and cotangent pieces in (41.10) gives

\[
 \mathcal O_{p,q}^{\rm cot}
 ={\pi\mu(p)\mu(q)\over pq}\mathcal V(p,q)M_1(p,q),   \tag{41.13}
\]

\[
 \mathcal O_{p,q}^{\rm elem}
 =-{\mu(p)\mu(q)\over pq}
 \left(\bigl[(q-p)\log(p/q)+(p+q)c_0\bigr]M_1
 -2M_2\right).                                        \tag{41.14}
\]

Neither piece has a fixed sign. The fixed sign in (41.12) appears only after
they are recombined.

## 4. What can safely be estimated

For a denominator row set

\[
 C(r)=\sum_{k=1}^{r-1}|\cot(\pi k/r)|.
\]

The literal cotangent definition gives the unconditional bound

\[
 |V(p,q)|\le C(q),\qquad
 |\mathcal V(p,q)|\le C(q)+C(p).                       \tag{41.15}
\]

Therefore, after gcd aggregation,

\[
 |\mathcal O_{p,q}^{\rm cot}|
 \le {\pi M_1(p,q)\over pq}\bigl(C(q)+C(p)\bigr).     \tag{41.16}
\]

This is valid but discards both Mobius cancellation across reduced pairs and
the exact elementary compensation in (41.11). A triangle inequality before
(41.9) is strictly weaker and should not be used.

At norm level there is still the exact difference of positive square packets

\[
 \mathfrak R(A,B)=
 \sum_{A\le n<B}\beta_n\|D_n\|^2
 -\sum_{A\le n<B}\beta_nC_n\|U_n\|^2,                \tag{41.17}
\]

but the second packet has the unfavorable sign. No completion of squares
within the Vasyunin cotangent part alone changes that fact. A proof must compare
the favorable opposite-sign packets and the linear term against `Q_1`, the
negative diagonal, and the unfavorable equal-sign packets.

## 5. Hostile sign audit

1. The target is `mathfrak R(A,B)>=0`; reversing this inequality reverses the
   interpretation of every packet.
2. `R_(a,b)>0`, but its coefficient is `-mu(a)mu(b)`, not
   `+mu(a)mu(b)`.
3. The restricted-kernel correction is `-1/(ab)`. It produces the `-2M_2`
   inside (41.10); dropping it destroys (41.11).
4. The reflection identity `V(q-p,q)=-V(p,q)` does not pair the symmetric
   kernel away: the companion term changes from `V(q,p)` to `V(q,q-p)`, and
   the arithmetic weights `M_1` also change.
5. Interchanging `p` and `q` is symmetry of one unordered Gram pair, not a
   second contribution with an opposite sign.
6. The identity (41.6) is false without the nonzero-Mobius restriction. Shared
   primes with `d` give zero terms rather than additional signed terms.
7. Positivity of `G` proves the packet bracket (41.11), but positive
   semidefiniteness does not prove positivity of the signed total (41.4).

Thus gcd aggregation does reveal a clean exact sign rule and prevents unsafe
cotangent estimates, but it does not yield a nonnegative block theorem. The
remaining arithmetic question is whether opposite-Mobius-sign reduced packets,
together with the linear contraction, compensate all unfavorable packets on a
suitable sequence of complete blocks.
