# Independent bridge and certificate audit

A bounded proof-architect audit mapped every assumption of the rooted
`m=8,rho=1,k_T=4` cell to every clause family in `k4_simsrc_cnf.py`.
It verified the degree census, robust-root equality, C-row/hole ledger, six
common C-dominators, exceptional b0 row, exact predecessor union, outsider
saturation (`|P|=6 or 7`), and the two-inaccessible-endpoint argument for every
source in P.  No missing clause or reversed implication was found.

The audit stressed that the projection is one-way and intentionally omits C,
rho, badness, and minimality: those hypotheses derive the encoded necessary
conditions.  UNSAT of the weaker projection therefore excludes exactly the
specified rooted cell.  It does not characterize counterexamples or close all
m=8 cases.

A full fresh source-checker replay accepted all 45 LRAT rows.  The historical
checker ELF is not retained/reproducible bit-for-bit under the current compiler;
this operational caveat is stated in the durable bridge note and does not get
silently weakened in the frozen verifier.
