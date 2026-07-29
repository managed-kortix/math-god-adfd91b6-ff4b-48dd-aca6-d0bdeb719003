# Cycle 84: bounded Hodge and BSD calibration review

For a correctly rooted plane on the Fermat degree-`d` fourfold, `d>=3`, the
normal sequence identifies

\[
H^1(N_{P/X_d})\simeq
\mathbf C[u_0,u_1,u_2]_d/
\sum_i u_i^{d-1}\mathbf C[u_0,u_1,u_2]_1,
\]

of dimension `binom(d+2,2)-9`. Multiplication by the Jacobian representative of
the primitive plane class is injective. A private output monomial for every
source monomial gives an all-degree proof, audited by
`verify_cycle84_unique_pivots.py`.

This yields the expected first-order equality of the plane-incidence and marked
Hodge tangent spaces. Primary-source review shows that the theorem is already
known in substance through complete-intersection and Fermat linear-cycle work
of Dan, Movasati--Villaflor, Kloosterman, and Villaflor. The private-pivot proof
is an explicit calibration, not a new Hodge-conjecture case or a publication
claim.

A second clean propagation statement was formalized: bounded denominators and
finitely many Hilbert/Chow data on a Zariski-dense set of fibers force one proper
relative cycle component to dominate the base. This is a standard finite-union
properness argument. The hard input remains a uniform complexity bound; the
lemma does not create a generic algebraic seed.

The BSD scout likewise identified the exact published certificate

\[
\widetilde\delta^{(1)}_{41\cdot61}(389\mathrm a1)\ne0\pmod5.
\]

Chan-Ho Kim already computed this and derived its Selmer consequences. It may be
independently replicated as software, but it is not a new arithmetic theorem
and does not bridge cyclotomic data to complex BSD.

No Hodge or BSD solution, new case, or publication-level novelty is claimed.
