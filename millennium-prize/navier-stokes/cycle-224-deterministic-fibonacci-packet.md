# Cycle 224: deterministic finite upscale-biased packet gate

## Decision

Replace random screening by one exact, finite, phase-coherent 2D Euler packet.
The packet below is instantaneous isolated-triad upscale-biased at six
simultaneous designated triads. It is
not admitted as a factor-two candidate: the exact full convolution has a large
off-rail leakage budget. Its value is structural. It fixes a reproducible
packet architecture and a fail-closed finite test that any continuation must
pass before full-PDE integration.

Work on `T^2=(R/2pi Z)^2` with normalized Haar measure and

\[
 \omega(x)=\sum_{m\ne0}\omega_m e^{im\cdot x},\qquad
 m^\perp=(m_2,-m_1),\qquad u_m={i m^\perp\over |m|^2}\omega_m,
 \tag{224.1}
\]

so that

\[
 \dot\omega_m=\sum_{p+q=m}{-\det(p,q)\over |p|^2}\omega_p\omega_q,
 \qquad p\times q=p_1q_2-p_2q_1.                 \tag{224.2}
\]

## Exact packet

Let `F_1=F_2=1`, `F_(j+2)=F_(j+1)+F_j`, and set

\[
 k_j=(F_{j+1},F_j),\qquad 1\leq j\leq8.
 \tag{224.3}
\]

The frequencies and squared radii are

| `j` | `k_j` | `|k_j|^2` |
|---:|---:|---:|
| 1 | `(1,1)` | `2` |
| 2 | `(2,1)` | `5` |
| 3 | `(3,2)` | `13` |
| 4 | `(5,3)` | `34` |
| 5 | `(8,5)` | `89` |
| 6 | `(13,8)` | `233` |
| 7 | `(21,13)` | `610` |
| 8 | `(34,21)` | `1597` |

They obey

\[
 k_j+k_{j+1}=k_{j+2},\qquad k_j\times k_{j+1}=(-1)^j.
 \tag{224.4}
\]

Take a real even vorticity packet supported on `S={+-k_1,...,+-k_8}`:

\[
 \omega_{k_j}=\omega_{-k_j}=a_j,
 \quad
 (a_1,\ldots,a_8)={1\over16}(-1,-1,1,1,1,-1,-16,-16).
 \tag{224.5}
\]

Thus every Fourier phase is exactly `0` or `pi`: positive coefficients have
phase `0`, negative coefficients phase `pi`, and conjugate modes have the same
phase. The signs satisfy

\[
 \operatorname{sgn}(a_{j+2})
  =-(k_j\times k_{j+1})
  \operatorname{sgn}(a_j)\operatorname{sgn}(a_{j+1}).
 \tag{224.6}
\]

This is a deliberately top-loaded packet. The two highest rails have unit
vorticity amplitude; the six lower rails are seeds of magnitude `1/16`.

## Signed triad interactions

For one real triad `p+q=r`, write pair enstrophy
`Z_m=|omega_m|^2+|omega_(-m)|^2=2|omega_m|^2`. If
`D=p cross q` and `R=omega_p omega_q omega_r` are real, its isolated signed
rates are

\[
 \begin{aligned}
 \dot Z_p&=-4D(|q|^{-2}-|r|^{-2})R,\\
 \dot Z_q&=-4D(|r|^{-2}-|p|^{-2})R,\\
 \dot Z_r&=-4D(|p|^{-2}-|q|^{-2})R.
 \end{aligned}                                      \tag{224.7}
\]

Equation (224.6) makes `D R<0` at every stage. Therefore the middle shell loses
vorticity variance while both adjacent shells gain it. More importantly, the
lower receiver always gains. The exact rates `(low,middle,high)` are

| stage | triad | signed pair-enstrophy rates |
|---:|---|---|
| 1 | `k_1+k_2=k_3` | `(1/8320, -11/26624, 3/10240)` |
| 2 | `k_2+k_3=k_4` | `(21/452608, -29/174080, 1/8320)` |
| 3 | `k_3+k_4=k_5` | `(55/3098624, -19/296192, 21/452608)` |
| 4 | `k_4+k_5=k_6` | `(9/1327168, -199/8112128, 55/3098624)` |
| 5 | `k_5+k_6=k_7` | `(377/9096320, -521/3474560, 9/82948)` |
| 6 | `k_6+k_7=k_8` | `(987/3896680, -341/372101, 377/568520)` |

Each row separately satisfies conservation of enstrophy and kinetic energy:

\[
 \sum_m\dot Z_m=0,\qquad \sum_m {|k_m|^{-2}}\dot Z_m=0.
 \tag{224.8}
\]

The ordering is upscale-biased when read from stage 6 to stage 1: a stage deposits into
the lower rail that is the high input of the preceding stage. This is an exact
instantaneous transfer graph, not a proof that the nonlinear orbit executes the
six transfers one after another for positive dwell times. In particular, this
is not a demonstrated cascade.

## Full-convolution leakage budget

Pairing all ordered terms in (224.2), define the complete initial convolution
`B_m` and exterior leakage `L_m=1_(m notin S) B_m`. There are exactly `60`
nonzero signed exterior frequencies (`30` conjugate pairs). Exact rational
bookkeeping gives

\[
 \sum_{m\notin S}|L_m|
 ={78334784061659\over21979083259520}
 \approx3.56406057235,                               \tag{224.9}
\]

\[
 \sum_{m\notin S}|L_m|^2
 ={63086613807192553004774156621\over
    65312429645588943997069230080}
 \approx0.965920486338,                              \tag{224.10}
\]

and, in the velocity-relevant `H^-1` metric,

\[
 \mathcal L^2:=\sum_{m\notin S}{|L_m|^2\over|m|^2}
 ={302948011971805436487777307554270959230223553631407\over
  341276900629764981757462405902609933481946700351078400}
 \approx8.87689765738\,10^{-4}.                     \tag{224.11}
\]

For comparison, the complete on-support velocity forcing is

\[
 \mathcal I^2:=\sum_{m\in S}{|B_m|^2\over|m|^2}
 ={68002292498686558323\over59106271172478682350288896}
 \approx1.15050892485\,10^{-6}.                     \tag{224.12}
\]

Hence

\[
 {\mathcal L^2\over\mathcal I^2}
 ={100982670657268478829259102518090319743407851210469\over
   130880706673510552400767051105667899743556587025}
 \approx771.562694181.                               \tag{224.13}
\]

The packet therefore fails the structural isolation gate by nearly three
orders of magnitude in squared velocity forcing. The principal cause is not a
random phase defect: it is deterministic high-high difference and sum forcing,
including the low difference mode `k_8-k_7=k_6` and many off-rail combinations.

## Finite admission and failure criterion

A proposed deterministic replacement packet is admissible to expensive Euler
integration only if exact rational or directed-ball replay verifies all of the
following finite conditions.

1. `S` is finite, symmetric, zero-free, and all frequencies, phases, and
   amplitudes are explicitly recorded.
2. There is an ordered list of at least six designated triads whose lower
   receiver radii strictly decrease and whose signed lower-receiver rates are
   positive. Every designated rate is nonzero after normalizing
   `sum_(m in S)|omega_m|^2=1`.
3. Full signed convolution is collected by output frequency before absolute
   values. In the normalization of item 2 it satisfies
   `mathcal L^2 <= mathcal I^2/16`.
4. A deterministic converged Galerkin run, with no random starts and with
   doubled cutoff and halved time step, finds a common checkpoint `T<=8` at
   which the endpoint ratio is at least `9/4`; the two ratios differ by at most
   `1/64` and energy and enstrophy drift are each at most `2^-20`.

Items 1--3 are a finite structural admission test. Item 4 is a finite candidate
test, not a PDE certificate. A packet fails immediately at the first violated
item; no tuning, nearby random samples, or post hoc budget extension is allowed.
Passing all four items only promotes the named packet to the Cycle 211
full-Euler enclosure, endpoint `L^3` cubature, and inviscid-limit transfer.

The packet (224.3)--(224.5) passes items 1--2 and fails item 3 because
`mathcal L^2/mathcal I^2>771`, whereas admission requires at most `1/16`.
Accordingly no numerical orbit screen is authorized for it. This is a durable
negative structural result, not an Euler `L^3` crossing, a Navier--Stokes
counterexample, or a Millennium solution.

Reproduce every exact frequency, sign, conservation, and leakage calculation
with

```sh
python3 millennium-prize/navier-stokes/verify_cycle224_fibonacci_inverse_cascade.py
```
