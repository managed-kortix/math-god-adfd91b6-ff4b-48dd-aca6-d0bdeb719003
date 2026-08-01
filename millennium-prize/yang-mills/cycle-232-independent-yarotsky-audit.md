# Cycle 232: rooted configuration count with coincident centers

## Verdict

Cycle 231's count uses the assertion that a configuration with support size
`n` has at most `n` events. That assertion is not robust if an `I` event and a
`J` event may have the same space-time center. The following count deliberately
allows that coincidence and gives the explicit bulk-polymer constant

\[
 c'=2\,191^4=2\,661\,726\,722.                    \tag{232.1}
\]

With

\[
 q'=6c'=15\,970\,360\,332,
\]

the exact-support activity comparison and the bulk Kotecky--Preiss test close
at the rational endpoint

\[
 |\lambda|\le \lambda_{\rm bulk}:=\frac1{8(q')^{416}}.    \tag{232.2}
\]

This is only a bulk-polymer convergence certificate. It is not a gap theorem.
Yarotsky's boundary-vector insertion introduces different polymers, and the
uniform constants needed there are not extracted below. Equation (232.2) is
also only a sufficient endpoint, not an exact maximal coupling.

## 1. Gauge normalization and event geometry

Put one tensor site at each vertex and assign to it the two positively oriented
links leaving that vertex. For

\[
 A=\{0,e_1,e_2\},\qquad C_2(1/2)=\frac34,
\]

define

\[
 h_x=\frac43\sum_{e:\operatorname{cell}(e)\in A+x}C_e.
\]

Every cell occurs in three translates of `A`, so `sum_x h_x=4T`, and the least
nonzero eigenvalue of each `h_x` is one. If

\[
 K_\lambda=T+\lambda\sum_p(1-w_p),\qquad
 w_p=\frac12\operatorname{Re}\operatorname{Tr}U_p,
\]

then, after deleting the scalar `4 lambda |P|`,

\[
 4K_\lambda=\sum_xh_x+\sum_x\phi_x+\text{scalar},\qquad
 \phi_x=-4\lambda w_{p_x},\qquad \|\phi_x\|\le b=4|\lambda|.
                                                               \tag{232.3}
\]

Consequently Yarotsky's form bound holds with any positive `alpha` and
`beta=b`; the final conversion is `|lambda|<=alpha/4`.

Write

\[
 D=A-A,\qquad B=A+D.
\]

An `I` event has spatial support `B+x`, a `J` event has support `D+x`, and each
event occupies two adjacent time layers. Direct lattice arithmetic gives

\[
 |D|=7,\quad |B|=12,
\]

and

\[
 |B-B|=37,\quad |B-D|=|D-B|=27,\quad |D-D|=19.             \tag{232.4}
\]

There are three relative time positions at which two two-layer events can
overlap. Hence the labelled event-overlap degrees are bounded by

\[
 \Delta_I=3(37+27)-1=191,
 \qquad
 \Delta_J=3(27+19)-1=137.                                 \tag{232.5}
\]

A fixed space-time point belongs to at most

\[
 R=2(|B|+|D|)=38                                           \tag{232.6}
\]

labelled events.

## 2. Exact rooted count allowing coincident `I/J` centers

An event is labelled by `(type,k,x)`, with `type` equal to `I` or `J`. Fix an
ordering of every event's neighbors. A connected set of `m` labelled events
containing a fixed root injects into event-graph depth-first walks of length
`2(m-1)`: recover the visited vertex set from the walk. By (232.5), there are at
most

\[
 191^{2(m-1)}                                               \tag{232.7}
\]

such rooted sets. This is an upper bound; not every walk is a canonical DFS
walk.

The multiplicity issue is resolved as follows. Choose from every event support
the canonical point `(k,x)` on one of its two time layers. After forgetting the
event type, at most two labelled events map to a canonical point. This remains
true when the `I` and `J` centers coincide. Therefore every configuration `C`
with `m` labelled events satisfies

\[
 m\le2|\operatorname{supp}C|.                              \tag{232.8}
\]

This deliberately does not use Yarotsky's additional exclusion
`J_k subset Lambda setminus Lambda_(I_k)`, which can forbid some same-layer
coincidences. It therefore bounds the larger hostile configuration class.

Let a connected configuration of support cardinality `n` contain a prescribed
space-time point. Choose as root one of the at most 38 events over that point.
Equations (232.7)--(232.8) give

\[
 \begin{aligned}
 N_n
 &\le38\sum_{m=1}^{2n}191^{2(m-1)}\\
 &\le76n\,191^{4n-2}\\
 &\le(2\,191^4)^n=(c')^n.
 \end{aligned}                                             \tag{232.9}
\]

For the last line, use `n<=2^(n-1)` and `38<191^2`:

\[
 76n\,191^{4n-2}
 \le\frac{38}{191^2}(2\,191^4)^n
 <(2\,191^4)^n.
\]

Thus (232.1) is a proved rooted connected configuration bound, equivalently a
bound for center multisets of multiplicity at most two after forgetting type.

It is not a bound for cluster multisets with arbitrary positive polymer
multiplicity. No constant-to-union-support bound can hold there: repeating one
fixed polymer `r` times leaves its union support unchanged. Standard cluster
estimates instead charge multiplicity, for example by
`sum_i n_i |supp chi_i|`, and use the factorials in the cluster weight.

## 3. Bulk Kotecky--Preiss criterion

Set `eta'=(q')^-1`. For bulk polymer activities satisfying
`|w(chi)|<=(eta')^|supp chi|`, (232.9) gives

\[
 \begin{aligned}
 \sum_{\chi'\not\sim\chi}|w(\chi')|e^{|\supp\chi'|}
 &\le |\supp\chi|\sum_{n\ge1}(c'e\eta')^n\\
 &< |\supp\chi|\sum_{n\ge1}(3c'\eta')^n\\
 &=|\supp\chi|.
 \end{aligned}                                             \tag{232.10}
\]

Only the strict inequality `e<3` is used. There is also a positive bulk tilt:
for every

\[
 0<\theta<\log(3/e),                                       \tag{232.11}
\]

replace each activity by `|w(chi)| exp(theta |supp chi|)`. Then
`c' eta' e exp(theta)<1/2`, so the tilted geometric sum in (232.10) remains
strictly less than `|supp chi|`. This controls ordinary bulk clusters and their
time span. It does not automatically control a new boundary-inserted species.

## 4. Activity comparison and explicit bulk endpoint

Yarotsky's Lemma 3, specialized to `|A|=3`, gives

\[
 |w(C)|\le
 \left(2\alpha e^{t_0(\beta/\alpha+27)}\right)^{N_I}
 \left(e^{-t_0}\right)^{N_J}.                              \tag{232.12}
\]

The number `27=|A|^3` is the energy-loss constant in that lemma, not a support
cardinality. The actual event supports imply

\[
 |\supp C|\le2|B|N_I+2|D|N_J=24N_I+14N_J.                 \tag{232.13}
\]

Take

\[
 t_0=14\log q',\qquad
 \alpha=\frac1{2(q')^{416}},\qquad
 \beta=b\le\alpha.                                        \tag{232.14}
\]

Then

\[
 e^{-t_0}=(\eta')^{14},
\]

and

\[
 2\alpha e^{t_0(\beta/\alpha+27)}
 \le(q')^{-416}(q')^{14(28)}
 =(q')^{-24}=(\eta')^{24},                                 \tag{232.15}
\]

where `416=24+14(27+1)`. Therefore

\[
 |w(C)|\le(\eta')^{24N_I+14N_J}
 \le(\eta')^{|\supp C|}.                                  \tag{232.16}
\]

Factorization gives the same estimate for every bulk polymer. Equations
(232.9)--(232.10) prove bulk KP convergence. Finally, (232.3) and
`b<=alpha` give exactly (232.2).

No claim is made that `c'`, exponent 416, or (232.2) is optimal. Enforcing all
configuration exclusions may improve the count. The point of (232.9) is that
it remains correct without silently excluding coincident `I/J` labels.

## 5. Why this is not an explicit gap theorem

The constants proved above belong to the vacuum-to-vacuum bulk partition
function. Three logically separate quantities must not be conflated:

1. **Bulk constant.** Equations (232.9)--(232.11) give an explicit rooted count,
   KP norm, and temporal tilt for ordinary bulk polymers.
2. **Boundary-insertion constant.** To prove the finite-volume full-space gap,
   Yarotsky replaces the reference vector by `Omega_0+v`. This creates polymers
   touching `{0} x Lambda`, `{N} x Lambda`, or both. The paper states that for
   `v` small their activity estimate persists, but does not print their rooted
   count, admissible radius in `v`, or a tilted KP bound uniform in the direction
   of `v` and in `Lambda`.
3. **Gap constant.** A numerical lower bound for the gap requires converting
   the uniform boundary-inserted time tail into a bound on every vector in the
   orthogonal complement. No such number follows from the bulk tilt alone. Any
   normalized gap for `4K_lambda` would moreover be divided by four for
   `K_lambda`.

Periodic volumes large enough to realize the fixed interaction geometry are
the setting of this count. Small tori with wraparound and arbitrary open
spatial boundaries require separate geometry and boundary-term checks. Gauss
restriction also requires the commuting-projector and gauge-invariant ambient
ground-state argument, though it does not change the coupling endpoint once an
ambient gap is actually proved.

Accordingly, (232.2) is a correct, deliberately hostile bulk-polymer
certificate allowing coincident `I/J` centers. It does not establish a
finite-volume full-space gap, does not supply a boundary-insertion constant,
and has no continuum Yang--Mills consequence.
