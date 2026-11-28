# Hostile audit

1. Check the exact Hilbert space and basis normalization against the discrete
   criterion before using the implication to RH.
2. Never continue `1/zeta(s)=sum mu(n)n^-s` to `Re(s)=1/2` without a new
   theorem; doing so is circular.
3. Positive-semidefinite Gram matrices do not provide the needed upper bound;
   all useful smallness is cancellation among Möbius coefficients.
4. The jumps of the fractional-part functions accumulate at zero. Ordinary
   sampled quadrature is not a certificate.
5. No finite table proves a uniform asymptotic bound, and the displayed
   approximants are not nested minimizers or known to be monotone.
6. Existing optimal-rate work is conditional. A proof must identify a new
   unconditional cancellation mechanism and be checked against the cited
   literature.
7. The signed finite-verifier Gram entries already contain the Möbius signs.
   Multiplying a signed divisor entry by another `mu(d)` is a double-signing
   error. De-signing is asserted only on squarefree labels; `diag(mu)` is not
   an orthogonal conjugation on all integer labels.
8. A locally uniform entrywise moving-kernel limit may not be inserted into a
   growing Möbius row sum without a separate discrepancy theorem. Endpoint
   uniformity and uniformity down to fixed old divisors are not part of the
   kernel theorem.
9. Do not conflate the rectangular normal diagonal
   `Delta_a(I)=||M_a||_F^2`, the literal self-pair sum
   `sum_q W_a(q,q)^2`, and the moving-Gram trace. They have different
   normalizations; literal self-pairs are `o(log^-3 a)`.
10. The continuum spectral statement acts on `L^2([1,2],du)`. A squarefree
    mesh carries limiting measure `(6/pi^2)du`, and no finite-mesh spectral
    transfer or unnormalized finite-Gram noncompression has been proved.
11. Positivity, positive entries, spectral tails, and normal-diagonal mass do
    not lower-bound `||M_a x_a||` for the fixed Möbius vector. The open target
    is `D_a(I) >> log^-3 a`. That target is sufficient only for the stated
    trace-based projection lower bound; it is neither necessary for every
    projection argument nor sufficient by itself for the physical budget.
12. The Cycle 45 dispersion census has only six dyadic scales and two
    post-selected row intervals. Its small, nonmonotone values of
    `log(a)D_a/Delta_a` certify finite Möbius cancellation, not convergence or
    failure of a positive liminf. Every use of the artifact must preserve the
    unsigned definition of `W`, the affine `beta` column, all squarefree
    divisor columns, and the outer relation
    `hat_c(q)=mu(q) CompensatedBlock.correlation(q)`; adding another `mu(d)` to
    the already signed legacy Gram rows recreates the double-signing error.
13. Finite-prime grouping preserves the physical vector but changes the normal
    diagonal. The product mesh density is `(6/pi^2) rho_P`; the certified
    finite grouped diagonal is not monotone under adjoining primes, but this
    does not by itself assert nonmonotonicity of the continuum constants.
    Fixed-`P` asymptotics may not be inserted for arbitrary `P=P(a)`. At
    extreme primorial size the grouping is tautological because all
    cancellation sits in one grouped column.
14. The initial non-wrapped interval and its tail are source-orthogonal before
    applying the common row functional, but their scalar row contractions are
    not orthogonal. A physical certified row has a large negative cross term.
    Never retain the initial square, tail square, Chebyshev square, or their
    diagonal sum as a lower bound without controlling every cross term.
15. In the gcd-grouped temporal formula, `U_n` includes the affine `chi`, the
    row is squarefree, the coprime condition is `(r,q)=1`, and the restricted
    correction is `-s_n/q`. Dropping any of these changes the identity.
16. For the Cycle 47 one-generator projection, the intrinsic retention factor
    is `|gamma_a|`, and the resulting constant is `epsilon^2`. The older
    one-sided cross-term condition is sufficient but stronger than necessary.
    Define the quotient as zero when `P_a=0`.
17. The endpoint Möbius-packet expansion is additive, not relative. A PNT
    upper bound, a formal reciprocal-zeta expansion, or a positive logarithmic
    mean does not prove every-scale energy or the target liminf.
18. The Cycle 47 complete-prefix construction has two canonical generators,
    not automatically rank two. Use the Moore--Penrose or variational formula
    unless `det G_a>0` is outward-certified. Trace control and full rank do not
    lower-bound the selected physical vector without a correlation bound.
19. At `theta=2/5`, the six complete-prefix rows are finite diagnostics.
    Their near-total projection capture and positive determinants prove no
    eventual rank, asymptotic lower bound, all-dyadic statement, or
    interscale theorem.
20. A bounded fixed local dual cannot exactly isolate one simple critical zero
    from all other simple critical-line modes, but this does not rule out
    growing or approximate tests, finite cutoffs, ordinary projections, or
    whole-packet inequalities.
21. In Cycle 48 the canonical complete-prefix vector is `B_a=Y_a+V_a`, not a
    new independent generator.  The exact identity is `hat_c=B_a+H_a`, and
    `H_a` retains the affine term, restricted correction, exact coprimality,
    every Mobius sign, and the full tail.  A favorable prime packet inside
    `B_a` cannot be retained without its signed reciprocal-Mobius partner.
22. The Cycle 47 quantities `tr G_a`, `||z_a||`, determinant magnitude, and
    projection coefficients depend on the normalization of `Y_a,V_a`.  The
    basis-invariant objects are the span and `Q_a^(2)`.  Cycle 48's canonical
    line quotient `Q_a^cp` is intrinsic to the actual complete prefix and
    obeys `Q_a^cp<=Q_a^(2)<=D_a`; it still requires a signed correlation bound.
23. High two-generator capture controls only the component of `H_a`
    perpendicular to `span(Y_a,V_a)`.  It does not make `H_a` small and does
    not justify deleting its parallel cross terms.  At `theta=2/5`, the
    reconstructed complete-prefix capture ratios at six starts are
    postprocessed finite diagnostics, not new outward certificates or
    asymptotic evidence.
24. The temporal Abel endpoints `E_(2a)` and `h_(2a)` may be generated by
    telescoping even though the temporal sum ends at `2a-1`.  They are not
    omitted `n=2a` summands.  In the `V_a` Abel formula the terminal
    `h_(2a)` term has a minus sign.
25. The canonical orthogonalization is rank-safe only with explicit zero
    branches: if `B_a=0`, take `R_a=Y_a`; every quotient whose denominator is
    zero is defined as zero.  In particular `B_a=0` with `Y_a=-V_a!=0` is a
    rank-one, not rank-zero, case.
26. In Cycle 49 the exact split `B_a=P_a^++S_a^mu` has
    `alpha_(q,n)>0` and `P_a^+(q)>0` throughout the permitted finite range,
    but positivity is strategically deceptive: uniformly on the physical
    interval, `log(a)^2 P_a^+ -> F` and `log(a)^2 S_a^mu -> -F`.  Never use
    the positive packet as a prefix lower bound without first combining its
    signed partner.
27. The leading-annihilation theorem uses quantitative reciprocal-Mobius
    decay in addition to the PNT.  In particular, justify uniformly
    `log(n)m_n=o(1)` and `ell_n=-1+o(1)`; do not infer them from a formal value
    of `1/zeta` at one without a tail estimate.
28. The common-source coefficient kernels are row-space Gram kernels.  Their
    positive normal diagonal is not a lower bound on the selected affine/Mobius
    vector, and the delta pairing of equal physical rows must not be confused
    with the spatial `H` inner product.  Retain the affine label, `d<=n`
    activation, final complete cell, and restricted `-1/(qd)` correction.
29. The exact residual after leading cancellation is a joint
    Chebyshev-error/reciprocal-Mobius packet.  PNT-sized one-point upper bounds,
    fixed-shift correlation theorems, generic PSD, or a local continuum kernel
    do not prove its every-scale `L^2` lower bound or its prefix-tail retention.
30. The Cycle 50 collapse `1+sum_(d<=n)mu(d)rho_d(t)=m_nt` is prefix-only:
    it holds almost everywhere on `[1,n+1)` by the cumulative identity
    `sum_(d<=k)mu(d)floor(k/d)=sum_(j<=k)sum_(d|j)mu(d)=1`.  Never replace the
    last expression by `sum_(d|k)mu(d)=1`, and never extend the collapse into a
    full Vasyunin integral.
31. In the one-source identity, the affine term is plus inside
    `mathscr K_(q,n)(m)`, the outer Mobius sum has a leading minus, and the
    endpoint `m=n` is nonzero.  The affine integrals `P_(q,n)(0)` and
    `mathfrak a_(q,n)` are different quantities.
32. The collapsed current kernel `K_B` is nonsymmetric.  Only its symmetric
    part on one common square label domain has a PSD order.  The correct fiber
    measure is `ds/s^2`; the collapse correction has a positive cross term;
    label `2` is a zero row; and compact injectivity implies noncoercivity only
    when the underlying `L^2` space is infinite-dimensional.
33. The physical retention matrix is the mixed cross product
    `(W_B)^T W_C^delta`, not the square prefix kernel.  It has a Krein
    difference-of-Grams factorization, and a 256-bit compatible certificate at
    `a=3` gives a strictly negative current-column principal minor.  Prefix PSD
    therefore cannot be transferred to retention.
34. Individual compatible floor-gauge columns have no finite `a log a`
    current-label limit: their redistributed affine prefix contains a leading
    `log(a)/u` term.  The selected Mobius sum may cancel it, but that does not
    justify columnwise convergence.  Use the compatible delta gauge for the
    entrywise full limit.
35. Complete monotonicity of the one-source kernel is false in the physical
    cell `a=4,q=5,n=6,theta=2/5`; a rigorous rational certificate has
    `D^3 mathscr K(2)<0`.  Ordinary monotonicity remains unproved and would not
    by itself provide a Mobius anti-cancellation lower bound.
36. In the Cycle 51 old/current split, the current collapse requires the full
    active range `a<=m<=n<=2a-1<2m`. The endpoints `m=a`, `m=n`, and
    `n=2a-1` remain; there is no `n=2a` term. For nonphysical `q<a`, the
    reordered temporal sum starts at `n=a`.
37. The direct collapsed `d`-column gauge and convolutional one-source
    `m`-column gauge are different. Do not compare their entrywise kernels,
    Hilbert--Schmidt angles, or source labels. Only selected vectors after the
    complete Mobius contraction are gauge-compatible.
38. The raw source ratio `det(G)/tr(G)^2` mixes angular separation with column
    norm balance and changes under independent column rescaling. It is
    redundant for the normalized-moment lower bound. A source Gram, even an
    identity Gram, does not imply retention without selected correlations.
39. The current Volterra limit is entrywise and Riemann-normalized. It may not
    be inserted into the unnormalized growing signed Mobius sum. Standard PNT
    upper bounds for both source blocks are far above the target energy after
    summing the rows and yield no anti-cancellation.
40. Cycle 51 source geometry, the `a=2048` prefix row, and the first seven
    smooth `span{1,q/a,log(q/a)}` captures are binary64 finite screens.  The
    columns are nearly dependent on `[1,3/2]`; high finite capture proves no
    asymptotic low rank, eventual conditioning, remainder bound, projection
    lower bound, or RH consequence.
41. Cycle 52 gives only a rank-safe moment sieve:
    `||B_a||^2 >= ||m_a||^2/(4a)` for the ordered moments against
    `(1,q/a,log(q/a))`.  The tautological orthogonal decomposition is not a
    low-rank theorem, and its continuum Gram positivity supplies no arithmetic
    moment lower bound.  If `G_a=0`, use `m_a=0`; do not divide by a zero
    largest eigenvalue.
42. The Cycle 52 `a=11` determinant is a rigorous Arb interval sign
    certificate, not an elementary closed-form exact value.  It refutes a
    universal exact three-function identity only.  It does not refute eventual
    exact closure, asymptotic rank-three approximation, or a vanishing relative
    remainder.
43. The certified captures `0.769089...` and `0.425849...` at
    `a=8192,16384` are finite counterexamples to universal `>=96%` capture.
    They do not prove asymptotic noncapture, failure of a liminf, a prefix norm
    bound, canonical retention, or RH.  Later binary64 recovery is nonmonotone
    and supplies no contrary theorem either.
44. A smooth row dual has a positive decreasing current-source transform, but
    Abel summation leaves signed block-Mertens values and the old block may
    cancel it.  One-point PNT, Mertens, reciprocal-Mobius, or omega inputs do
    not provide the needed every-scale lower bound.  For
    `y_q=mu(q)f(q/a)`, the self-diagonal is `o(log^-3 a)` after dual
    normalization; success of that particular test requires a weighted
    off-diagonal two-point Mobius estimate for the full moving kernel.
45. Prefix norm and canonical retention remain separate.  In the three-mode
    decomposition the modal and remainder contributions to `<B_a,C_a>` are
    signed and may cancel.  Neither high capture, an absolute norm lower bound,
    nor exact closure implies `Q_a^cp` without an independent relative signed
    retention estimate.
46. Cycle 52 finite differencing does not localize the arithmetic source.
    First, second, and third ordinary differences retain the dense interior and
    moving-boundary packets; `Delta^3 log(q)` is nonzero.  The exact four-point
    annihilator of `(1,q/a,log(q/a))` still leaves `log(q)^2`, reciprocal, and
    cumulative Chebyshev channels.  Poincare transfers a proved differenced
    lower bound but does not supply one.  The no-go concerns these specific
    architectures only, not every longer variable-coefficient test.
