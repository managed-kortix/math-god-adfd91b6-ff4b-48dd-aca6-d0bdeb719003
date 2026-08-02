# Cycle 239: infinite Fibonacci rail cancellation obstruction

## Decision

The most direct genuinely infinite continuation of the Cycle 224 Fibonacci rail
is exactly decidable, and it fails. On the full two-sided rail, cancellation of
the leading doubled-rail leakage at every scale forces an exact four-step
amplitude recurrence. That recurrence has two independent fatal consequences:

1. two same-direction upscale transfers two scales apart have opposite signs;
2. every nonzero amplitude subsequence grows by a factor greater than `8` every
   six rails, so the Fourier coefficients do not even tend to zero.

Thus this architecture cannot produce analytic 2D Euler initial data with the
declared cancellation and signed upscale transfer. The obstruction is exact;
no random or floating numerical screen is used. It retires this rail, not the
Cycle 237 genuinely-infinite-tail admission gate in general.

## Infinite rail and Euler convention

Work on `T^2=(R/2pi Z)^2` with normalized Haar measure and

\[
 \omega(x)=\sum_{m\ne0}\omega_m e^{im\cdot x},\qquad
 u_m={i(m_2,-m_1)\over |m|^2}\omega_m,
\]

\[
 \dot\omega_m=\sum_{p+q=m}{-\det(p,q)\over |p|^2}
                  \omega_p\omega_q.                 \tag{239.1}
\]

Let `F_1=F_2=1`, `F_(j+2)=F_(j+1)+F_j`, and

\[
 k_j=(F_{j+1},F_j),\qquad r_j=|k_j|^2=F_{2j+1}.
 \tag{239.2}
\]

Take a real even rail

\[
 \omega_{k_j}=\omega_{-k_j}=a_j\in\mathbb R\setminus\{0\},
 \qquad j\ge1.                                      \tag{239.3}
\]

The rail is lacunary in radius, since `r_(j+2)=3r_(j+1)-r_j` and
`r_(j+1)/r_j` increases from `5/2` to `(3+sqrt(5))/2`.

## Exact leading-leakage recurrence

For every `n>=1`, consider the exterior doubled-rail mode

\[
 h_n=2k_{n+2}=k_n+k_{n+3}=-k_{n+1}+k_{n+4}.         \tag{239.4}
\]

An elementary Fibonacci descent shows that these are the only two unordered
pairs in `{+-k_j:j>=1}` summing to `h_n`. One way to run the descent is to use
the second coordinate to place the largest index, subtract the corresponding
first coordinate, and apply `F_(j+1)-F_j=F_(j-1)`; strict monotonicity leaves
successively `(n,n+3)` and `(-(n+1),n+4)`. Thus (239.4) is an identity for the
full infinite rail, not a truncation statement.

Pairing the two orders in (239.1), and using

\[
 \det(k_n,k_{n+3})=
 \det(-k_{n+1},k_{n+4})=2(-1)^n,
\]

gives

\[
 B_{h_n}=-2(-1)^n\left[
  (r_n^{-1}-r_{n+3}^{-1})a_na_{n+3}
 +(r_{n+1}^{-1}-r_{n+4}^{-1})a_{n+1}a_{n+4}
 \right].                                           \tag{239.5}
\]

Consequently `B_(h_n)=0` is equivalent, with no asymptotic remainder, to

\[
 a_{n+4}=-q_n{a_na_{n+3}\over a_{n+1}},             \tag{239.6}
\]

where

\[
 q_n={r_n^{-1}-r_{n+3}^{-1}\over
           r_{n+1}^{-1}-r_{n+4}^{-1}}>0.             \tag{239.7}
\]

Writing `x_n=r_(n+1)/r_n`, the odd-Fibonacci recurrence gives the exact form

\[
 q_n={x_n(21x_n-8)(2x_n-1)\over
             (8x_n-3)(5x_n-2)}.                     \tag{239.8}
\]

Since `x_n>=5/2`,

\[
 q_n-2={42x_n^3-117x_n^2+70x_n-12\over
              (8x_n-3)(5x_n-2)}>0.                  \tag{239.9}
\]

The numerator is positive at `5/2` and has positive derivative on
`[5/2,infinity)`. This proves the bound without decimal approximation.

## Convergence obstruction

Applying (239.6) three times and cancelling the intermediate amplitudes yields
the exact six-rail recurrence

\[
 a_{n+6}=-q_nq_{n+1}q_{n+2}a_n.                    \tag{239.10}
\]

Equations (239.9)--(239.10) imply

\[
 |a_{n+6}|>8|a_n|.                                  \tag{239.11}
\]

Hence every one of the six residue-class subsequences is unbounded. In
particular `a_j` does not tend to zero, so (239.3) is not an `L^2`, smooth, or
analytic vorticity. (Polynomially growing Fourier coefficients may still define
a distribution, so no stronger claim is made.) Making the first four amplitudes
arbitrarily small cannot repair this: the multiplier in (239.10) is independent
of their common scale.

## Signed-transfer obstruction

The adjacent Fibonacci triad is `k_j+k_(j+1)=k_(j+2)`, with
`D_j=det(k_j,k_(j+1))=(-1)^j`. Its isolated lower-receiver pair-enstrophy rate
is

\[
 R_j=-4D_j(r_{j+1}^{-1}-r_{j+2}^{-1})
              a_ja_{j+1}a_{j+2}.                   \tag{239.12}
\]

Multiplying (239.12) at `j=n` and `j=n+2`, and using (239.6), gives

\[
 R_nR_{n+2}<0.                                      \tag{239.13}
\]

Indeed all radial factors are positive, `D_(n+2)=D_n`, `a_(n+2)^2>0`, and the
remaining sign is that of
`a_na_(n+1)a_(n+3)a_(n+4)=-q_n a_n^2a_(n+3)^2<0`.
Therefore cancellation of even one `h_n` leakage forbids both designated
lower receivers `n` and `n+2` from gaining simultaneously. Cancellation at
all scales cannot support a consistently directed upscale rail.

## Finite rejection gate

A proposed nonzero real-even Fibonacci-rail tail is rejected as soon as one
index `n` supplies the following finite witness:

1. the exact collected coefficient `B_(h_n)` vanishes;
2. both exact directed rates `R_n` and `R_(n+2)` are declared positive.

The witness is terminal because (239.5) implies the strict identity
`R_n R_(n+2)<0`. Independently, three consecutive exact cancellation identities
are enough to expose (239.10); the rational check
`q_n q_(n+1) q_(n+2)>8` rejects convergence of the corresponding nonzero
residue subsequence. These tests involve finitely many integer frequencies and
rational operations and can return the failed signed identity directly.

Reproduce the identities and the first 32 scale instances with

```sh
python3 millennium-prize/navier-stokes/verify_cycle239_infinite_fibonacci_rail.py
```

No Euler `L^3` crossing, Navier--Stokes counterexample, or Millennium solution
is claimed.
