# Cycle 212: fail-closed validated integration design

## Selected datum and normalization

Work on `T^2=(R/2pi Z)^2` with normalized Haar measure.  The selected
nondegenerate member of the Cycle 210 family is

\[
 \psi_0(x,y)=\cos x+\cos y+\cos(x+y),\qquad
 \omega_0=\Delta\psi_0=-\cos x-\cos y-2\cos(x+y).
 \tag{212.1}
\]

It uses the first three frozen frequencies and has nonzero vorticity
interaction.  For `k=(k_1,k_2) != 0`, put `k^perp=(k_2,-k_1)` and use

\[
 \omega=\sum_k\omega_k e^{ik\cdot x},\qquad
 u_k={i k^\perp\over |k|_2^2}\omega_k,
\]

so the full vorticity equation is

\[
 \dot\omega_k=-\mu|k|_2^2\omega_k+
 \sum_{p+q=k}{p^\perp\cdot q\over |p|_2^2}\omega_p\omega_q.
 \tag{212.2}
\]

The zero mode is fixed to zero and Fourier reality is
`omega_(-k)=conj(omega_k)`.  Every certificate must state this normalization;
changing torus measure, Fourier signs, or the Biot--Savart multiplier invalidates
it.

## Exact certificate theorem

The following is the intended theorem interface.  It separates the mathematical
lemmas from finite interval replay and makes every trust boundary explicit.

**Theorem 212.A (validated Fourier-vorticity integration).**  Fix rational
`mu>0`, `T>0`, a symmetric retained set `S_N={k:0<|k|_infinity<=N}`, and the
datum (212.1).  Suppose a certificate contains:

1. **Directed arithmetic.** Rational outward intervals only.  Every elementary
   transcendental enclosure carries its reduction range, Taylor degree, and a
   rational remainder bound.  NaN, infinity, a reversed interval, an unknown
   key, or an omitted mode rejects the certificate.
2. **Slab chain.** A rational partition `0=t_0<...<t_m=T`.  On each slab `I_j`
   there are complex boxes `W_(j,k)`, an entry box `A_(j,k)`, a derivative box,
   and an endpoint box `B_(j,k)`.  Fourier reality and zero mean hold boxwise.
3. **Full-PDE tail majorant.** Nonnegative shell masses
   `z_(j,n)>=sum_(|k|_infinity=n)|omega_k|` for `n>N`, represented by a finite
   head and a geometric analytic cap
   `z_n<=C_j rho_j^-n`, satisfy a published comparison lemma for (212.2).
   Its interval replay proves: initial domination, inward pointing inequalities
   on every shell face, preservation of the geometric cap, and the declared
   low-mode remainder intervals `R_(j,k)`.  The comparison lemma and all
   constants are part of the certificate, not an appeal to a Galerkin limit.
4. **Interval ODE inclusion.** With `F_N` the exact retained convolution,
   interval evaluation proves

   \[
   A_j+[0,h_j](F_N(W_j)+R_j)\subseteq W_j,
   \quad
   A_j+h_j(F_N(W_j)+R_j)\subseteq B_j.             \tag{212.3}
   \]

   The first inclusion is the Picard enclosure; the second propagates the
   endpoint.  `B_j subseteq A_(j+1)` and the first entry contains the exact
   coefficients of (212.1).
5. **Analytic velocity bounds.** The same shell majorant proves rational
   `U_j>=sup |u|` and `G_j>=sup ||grad u||_op`.  A separate unbound Galerkin
   norm is not accepted.  A simple admissible conversion is

   \[
   U_j\le\sum_{k\ne0}{|\omega_k|\over|k|_2},\qquad
   G_j\le\sum_{k\ne0}|\omega_k|,
   \tag{212.4}
   \]

   with the retained sums and infinite tail both rounded upward.
6. **`L^3` cubature.** On an `M x M` grid, directed Fourier evaluation gives
   center boxes for both velocity components, including an interval contribution
   from the unresolved velocity tail.  If `d_M>=sqrt(2)pi/M`, then
   `| |u(x)|^3-|u(c)|^3 |<=3U_j^2G_j d_M` on a cell.  Consequently

   \[
   {1\over M^2}\sum_c |u(c)|^3-3U_j^2G_jd_M
   \le ||u||_3^3 \le
   {1\over M^2}\sum_c |u(c)|^3+3U_j^2G_jd_M.       \tag{212.5}
   \]

   The point boxes must be recomputed from the endpoint Fourier and tail boxes;
   certificate-supplied point values are not trusted.

Then a unique smooth 2D Navier--Stokes solution exists on `[0,T]`, its Fourier
coefficients lie in the certified boxes, and (212.5) encloses its endpoint
`L^3` norm.  If the final lower cube bound is strictly greater than eight times
the initial upper cube bound, then
`||u(T)||_3>2||u(0)||_3`; embedding it independently of `x_3` is a strict
falsifier of (210.1).

**Proof structure.**  Item 3 and the comparison principle control every
unresolved Fourier coefficient and justify the full convolution.  Item 4 and
the interval Picard theorem enclose the retained equations with that tail
remainder.  Slab induction gives existence through `T`; standard 2D uniqueness
identifies the enclosure with the Navier--Stokes solution.  Equations (212.4)
and the mean-value theorem give (212.5).  Cubing avoids an interval division or
an incorrectly rounded cube root.  The final strict rational inequality gives
the claim.

## Certificate object

The production JSON object is versioned and has these required top-level keys:

```text
format, normalization, selected_datum, parameters, modes, slabs,
tail_majorant, analytic_norm, cubature, conclusion, digests
```

`tail_majorant` records the exact comparison-lemma identifier, shell cutoff,
geometric-cap parameters, shell inequalities, and low-mode remainder boxes.
`analytic_norm` records independently recomputed retained and tail contributions
to (212.4).  `cubature` records only grid size and Taylor policy; point boxes and
the final integral are verifier outputs.  `conclusion` is accepted only when it
equals a conclusion derived by the checker.  Input file hashes bind any split
binary slab data to the manifest.

The validator has three outcomes only:

* `PASS FULL`: every item of Theorem 212.A replayed and the stated strict
  conclusion derived;
* `PASS COMPONENTS`: reusable arithmetic, ODE, tail-conversion, or cubature
  components passed, but no PDE or amplification claim is made;
* nonzero exit with the first failed invariant.

There is deliberately no `UNKNOWN -> PASS` path.  In particular, absent shell
comparison data, a sampled trajectory, or a tiny numerical residual fails
closed rather than becoming an assumed tail bound.

## Reusable skeleton and present scope

`validate_cycle212.py` implements exact rational interval arithmetic, complex
Fourier convolution, Picard-box checks, analytic-tail conversion, directed
Taylor trigonometric enclosures, and Lipschitz `L^3` cubature.  Its self-test
uses exact manufactured boxes and returns `PASS COMPONENTS`.  The production
manifest loader rejects `mode="full"` because the shell comparison replay is
not implemented yet.

Thus Cycle 212 fixes the exact theorem and certificate architecture and supplies
reusable audited primitives.  It does **not** certify the selected trajectory,
does not report an amplification ratio, and does not close either outcome of
the Cycle 210 finite campaign.  The next mathematical implementation gate is
item 3: an explicit dissipative shell comparison theorem whose constants are
strong enough to survive interval replay.
