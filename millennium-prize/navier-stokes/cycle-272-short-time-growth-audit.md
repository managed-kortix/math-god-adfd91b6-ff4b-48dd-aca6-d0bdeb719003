# Cycle 272: exact short-time growth audit

## Frozen quantities

Put

\[
 C(t)=\int_{\mathbb T^3}|u(t)|^3,\qquad
 L(t)=\log\|u(t)\|_3={1\over3}\log C(t).
\]

Directed evaluation of the existing Arb certificates gives the rational
subintervals

\[
 17089957<C(0)<17090032,
 \qquad 15262<C'(0)<24283,
\]

and the exact second-jet replay gives

\[
 3<L''(0)<4.
\]

Consequently

\[
 {297\over10^6}<L'(0)<{474\over10^6}.                 \tag{272.1}
\]

Indeed the lower inequality follows already from

\[
 {C'(0)\over3C(0)}>{15262\over3\cdot17090032}
 ={7631\over25635048}>{297\over10^6}.
\]

The machine-readable frozen values are in
`cycle272-short-time-manifest.json`.

## Analytic remainder

Retain the admission majorant

\[
 q(t)={33\over32}(1-600t),\quad 0\le t\le T={1\over65536},
 \quad A_{q(t)}(u(t))\le600,
\]

and write `Q=q(T)=267861/262144`. Direct integer comparisons at the
maximizing integers give

\[
 \sup_{n\ge1}{n\over Q^n}<18,
 \quad \sup_{n\ge1}{n^2\over Q^n}<1164,
 \quad \sup_{n\ge1}{n^3\over Q^n}<133868.              \tag{272.2}
\]

For the Euler bilinear map `B(v,w)=-P((v dot grad)w)`, the Euclidean-vector Wiener
norm used in the admission majorant obeys

\[
 \|B(v,w)\|_{W^s}\le
 \sum_{i=0}^s {s\choose i}\|v\|_{W^i}\|w\|_{W^{s-i+1}}.
\]

Equations (272.2) therefore imply, throughout the frozen slab,

\[
 |u|\le600,
 \quad |u_t|\le6480000,
 \quad |u_{tt}|\le391392000000,
 \quad |u_{ttt}|\le46322668800000000.                 \tag{272.3}
\]

Energy conservation and the exact initial Fourier coefficients give

\[
 \|u(t)\|_2^2={1990183\over30}>257^2,
 \qquad C(t)\ge\|u(t)\|_2^3>{511477031\over30}.       \tag{272.4}
\]

Using

\[
 |C'''|\le12|u_t|^3+18|u||u_t||u_{tt}|+3|u|^2|u_{ttt}|
\]

together with the analogous first- and second-derivative bounds, (272.3)--
(272.4), and

\[
 L'''={C'''\over3C}-{C'C''\over C^2}
       +{2(C')^3\over3C^3},
\]

gives the deliberately rounded exact slab estimate

\[
 |L'''(t)|<62000000000000000.                          \tag{272.5}
\]

## Certified lower growth

Taylor's theorem, (272.1), (272.5), and `L''(0)>3` yield

\[
 L(t)-L(0)\ge {297\over10^6}t+{3\over2}t^2
              -{62000000000000000\over6}t^3.          \tag{272.6}
\]

At the frozen short-time witness

\[
 t_*={1\over17179869184},
\]

the right side is exactly

\[
 {110615187084300373\over
  7253554917687775048237056000000}>{1\over10^{14}}.   \tag{272.7}
\]

The differentiated lower Taylor bound is also positive at `t_*`:

\[
 {297\over10^6}+3t_*-{62000000000000000\over2}t_*^2
 ={27017106713235541\over140737488355328000000}>0.    \tag{272.8}
\]

Thus Cycle 272 has rigorous, strictly positive complete-velocity `L^3` growth,
but only on a horizon far smaller than the admission slab. The correct choice
is to retain `T=1/65536` as the existence and generated-tail interval and to
freeze `t_*` separately as the proved growth endpoint.

## Factor-two decision

The pointwise Wiener cap in (272.3) gives a substantially sharper estimate if
it is applied to the `L3` norm before taking the logarithm.  Minkowski's
inequality and the fundamental theorem of calculus imply

\[
 \left|\|u(t)\|_3-\|u(0)\|_3\right|
 \leq\int_0^t\|u_s(s)\|_3\,ds
 \leq6480000t.                                         \tag{272.9}
\]

At the frozen endpoint, (272.4) and (272.9) give

\[
 d:=6480000T={50625\over512},\qquad
 \|u(0)\|_3\geq\|u(0)\|_2>257,
\]

and therefore, with `r=d/257=50625/131584<1`,

\[
 1-r<{\|u(T)\|_3\over\|u(0)\|_3}<1+r.
\]

The decreasing side is the larger logarithmic deviation.  The elementary
inequalities `log(1+r)<r` and `-log(1-r)<r/(1-r)` now yield the exact rational
certificate

\[
 \boxed{\left|L(T)-L(0)\right|
 <{r\over1-r}={50625\over80959}<{2\over3}<\log2.}       \tag{272.10}
\]

Here `50625/80959<2/3` is the integer comparison
`151875<161918`, while `log 2>2/3` follows from
`log x>2(x-1)/(x+1)` for `x>1`.  The same argument with `t<=T` excludes a
factor-two increase everywhere on the frozen slab, without a trajectory
calculation.  Thus the Cycle 273 endpoint promotion threshold `201/100` is
analytically unreachable for this datum and horizon, and its trajectory
manifest is rejected before compute.
