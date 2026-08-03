# Cycle 272: ND270 Kida-tail admission audit

## Verdict: `ND270-DUPLICATE`

The proposed rational Gaussian tail is a genuine infinite-support analytic
perturbation of the retired `C267-KP1` datum. Nevertheless, under the Cycle 272
mechanism-deletion rule it is an exact architectural duplicate: deleting the
tail along `u_(epsilon,s)=u^*+s epsilon H` leaves the Kida core as the sole
claimed source of favorable complete-`L^3` production, while the tail supplies
only infinite support, nonplanarity, and a continuity error. No indispensable
signed core--tail or tail--tail mechanism is printed.

There is a second, downstream defect: the retained record contains no
certified positive interval for the production of `K-F(K)/32`. Continuity
cannot preserve a sign observed only by non-directed floating cubature. The
duplicate rule stops the architecture before that item 3 wall is reached.

No trajectory computation is authorized.

## Exact candidate

Use normalized Haar measure on `T^3=(R/2 pi Z)^3` and retain

\[
 u^*=K-{1\over32}{\cal F}(K),\qquad
 {\cal F}(v)=-\mathbb P((v\mathbin\cdot\nabla)v),
 \tag{272.1}
\]

with `K` exactly as in (265.26). For `n>=20`, set

\[
 k_n=(n,n^2,1),\qquad a_n=(n,-1,0),\qquad
 m_n=|k_n|_1=n^2+n+1                                      \tag{272.2}
\]

and define

\[
 H(x)=\sum_{n=20}^{\infty}2^{-2m_n}a_n\sin(k_n\cdot x),
 \qquad u_\varepsilon=u^*+\varepsilon H.                 \tag{272.3}
\]

Freeze the compact rational parameter box and its rational witness as

\[
 \boxed{P=[2^{-65},2^{-64}],\qquad
        \varepsilon_*=3\,2^{-66}\in P.}                  \tag{272.4}
\]

Equivalently, the datum to be tested is the compact singleton
`{u_(3/2^66)}` inside the printed box. Every Fourier coefficient is rational
(hence Gaussian rational), and `k_n dot a_n=n^2-n^2=0`; therefore (272.3) is
real, mean zero, and divergence free term by term.

## Closed Wiener majorant

For a vector field use the componentwise analytic Wiener norm

\[
 \|f\|_{A_2}=\sum_{k\in\mathbb Z^3}2^{|k|_1}
                   \sum_{j=1}^3|\widehat f_j(k)|.         \tag{272.5}
\]

The two coefficients of each sine have total componentwise mass
`2^(-2m_n)(n+1)`. Hence

\[
 \|H\|_{A_2}=\sum_{n=20}^{\infty}(n+1)2^{-m_n}
 \le R_H:={21\,2^{-421}\over1-2^{-41}}.                 \tag{272.6}
\]

Indeed, consecutive summands have ratio

\[
 {n+2\over n+1}2^{-(2n+2)}\le2^{-41}\qquad(n\ge20).
\]

Thus the series converges absolutely on the complex strip
`|Im x_j|<log 2`, and, writing the finite exactly computable algebraic
sum `W_*=||u^*||_(A_2)`, every member of (272.4) obeys the closed bound

\[
 \boxed{\|u_\varepsilon\|_{A_2}
        \le W_*+2^{-64}R_H.}                              \tag{272.7}
\]

The same geometric estimate after replacing `2` by any rational
`lambda` with `1<lambda<2` gives a positive residual strip and bounds every
spatial derivative. This is an initial-data majorant, not the item 4
full-Euler continuation majorant on a declared time interval.

## Infinite support and nonplanarity

The finite polynomial `u^*` has no frequencies above its fixed support, while
every coefficient at `+/-k_n` in the tail is nonzero for every
`epsilon in P`. Consequently every member has genuinely infinite Fourier
support; no cancellation with (272.1) is possible for `n>=20`.

Moreover,

\[
 \det\begin{pmatrix}
 20&400&1\\21&441&1\\22&484&1
 \end{pmatrix}=2\ne0.                                   \tag{272.8}
\]

The three nonzero tail frequencies `k_20,k_21,k_22` therefore span `R^3`.
This is a full-support nonplanarity certificate independent of the Kida
frequencies.

Projection onto the frequencies `{k_n:n>=20}` does recover a nonzero infinite
tail, so the perturbed field is not literally equal to a retired finite
profile. That support distinction does not pass the Cycle 272 duplicate rule.
The exact deletion homotopy

\[
 u_{\varepsilon,s}=u^*+s\varepsilon H,\qquad0\le s\le1, \tag{272.9}
\]

removes the tail while preserving the claimed logical source of production.
The proposal attributes no favorable signed term to a core--tail or tail--tail
interaction and gives no lemma whose strict margin disappears at `s=0`.
Therefore the tail is mechanism-removable even though support cardinality and
the three-frequency nonplanarity certificate change at the endpoint.

## First failed certificate

Let

\[
 \mathcal P_3(v)=3\int_{\mathbb T^3}|v|v\cdot\mathcal F(v)
                 =3\int_{\mathbb T^3}p_v\,v\cdot\nabla|v|. \tag{272.10}
\]

The map `epsilon -> mathcal P_3(u_epsilon)` is continuous (indeed locally
Lipschitz in the displayed analytic Wiener topology). Therefore a directed
base enclosure

\[
 \mathcal P_3(u^*)\in[q_0,Q_0],\qquad q_0>0,              \tag{272.11}
\]

together with a certified Lipschitz constant `L` would yield the exact
robustness margin

\[
 |\varepsilon|\le\delta:=q_0/(2LR_H)
 \quad\Longrightarrow\quad
 \mathcal P_3(u_\varepsilon)\ge q_0/2.                  \tag{272.12}
\]

But (272.11) does not exist in the retained dossier. Cycle 266 reports only
the converged floating value `0.0356418`; its own hostile audit records that
the available rectangle-rule radius is about `219.60`, uses no directed
interval arithmetic, and is too wide even to certify the sign. Thus the
requested interval robustness margin is

\[
 \boxed{\delta_{\rm certified}=\text{UNAVAILABLE}.}       \tag{272.13}
\]

Qualitative continuity, arbitrarily small rational coefficients, and the
strictly positive floating midpoint do not imply a rational `q>0`. Item 3
also requires a same-majorant pressure/tail enclosure and an exact exclusion
of stationarity modulo every Galilean translation. Positive certified
production would exclude such translation-stationarity because translations
preserve `L^3`, but the missing sign certificate cannot be used to do so.

Under the fail-closed order, mechanism deletion precedes the six admission
items. The exact terminal output is

`ND270-DUPLICATE: THE TAIL IS MECHANISM-REMOVABLE.`

The unavailable sign margin is a hostile secondary check, not the terminal
classification. This retires only the printed tail architecture. It does not
reopen `C267-KP1`, establish an Euler endpoint crossing, or make a
Navier--Stokes or Millennium claim.
