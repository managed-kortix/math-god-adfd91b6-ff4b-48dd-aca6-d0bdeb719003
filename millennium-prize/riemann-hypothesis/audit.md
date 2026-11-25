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
