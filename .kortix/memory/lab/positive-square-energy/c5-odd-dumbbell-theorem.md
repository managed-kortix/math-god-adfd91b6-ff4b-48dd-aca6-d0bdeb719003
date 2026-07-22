# The C5--odd-cycle dumbbell theorem

Let `G_q` be obtained from disjoint cycles C5 and Cq by adding one edge between
distinguished vertices, where q is odd and q>=3. Then

`s^+(G_q)>q+5`.

## Exact factorization

With `p_n=chi(C_n)` and `m_n=chi(P_{n-1})`,

`chi(G_q)=p_5p_q-m_5m_q`.

The factor `x^2+x-1` divides both p5 and m5 and hence persists. The standard
odd-cycle retained factor also divides the quotient. The remaining symmetric
factor S_q has the nine-term Chebyshev form certified by
`c5_moment_formulas.py`.

## Finite range

The same script proves its first 16 power sums symbolically for all stable q.
The exact polynomial minorant in `c5_moment_minorant.py` proves the required
defect inequality for every odd q<=725; q=3..23 are separately exact-isolated.

## Tail

The band phase satisfies the derivative bounds certified by
`c5_phase_bounds.py`. Its limiting phase integral is positive by the exact
polynomial majorant in `c5_phase_integral.py`. The positive outlier has
`r>5/3`, so the limiting defect exceeds `2+(34/15)^2`, with margin >2/5 over
the target.

For q>=727, counting coordinates put the positive band roots at consecutive
integers. The composite trapezoid error and both fractional endpoint cells are
bounded in `c5_euler_tail.md`; exact constants in `c5_tail_constants.py` give
total error <1/25. Thus the finite defect remains above target.

## Verification status

All algebraic identities, Sturm sign checks, moment inequalities, and rational
constants have standalone SymPy certificates. Independent PARI reproduced
every odd q=3..23 finite exception with exact integer characteristic
polynomials and positive 80-digit slacks. A line-by-line adversarial review
remains before any novelty/public result claim.
