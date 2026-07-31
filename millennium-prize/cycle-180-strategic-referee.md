# Cycle 180: strategic referee checkpoint

## Decision

Yang--Mills has reached an equivalence wall for the present finite-lattice
low/tail architecture. This is a strategic, not a formal logical, equivalence
claim. Cycles 174, 178, and 179 show that qualitative Wilson density, a fixed
bare representation cutoff, and a global product of local Casimir cutoffs
cannot promote local estimates to contraction on the whole vacuum complement.
The surviving statement would have to construct an interacting-ground-state-
adapted connected decomposition and prove

\[
 \sup_{a,V}\|e^{-t(H_{a,V}-E_{0,a,V})}Q_{a,V}\|<1
\]

at a fixed physical time, while also supplying reflection-positive continuum
tightness, nontriviality, and OS reconstruction. The first conclusion is the
uniform lattice mass gap in semigroup form; the second group of conclusions is
the existence half of the Clay problem. No independently checkable
intermediate estimate currently separates the proposed connected-tail lemma
from those conclusions. Yang--Mills therefore rotates. This does not prove
that every connected/polymer or RG approach is circular; it records that none
with a weaker, separately testable production lemma is presently specified.

## Random-order MCSP comparison

A random-order MCSP theorem remains a legitimate bounded target, but its
quantifiers must not be confused with the McKay--Murray--Williams implication.
There are three distinct levels.

1. An exact random-order decision/query theorem for the Boolean decision
   problem `MCSP[s]` can strengthen Cycle 159 by showing that a random
   permutation does not permit early stopping on a specified distribution of
   truth tables. Its ceiling is still `N` inspected input bits. It is an
   unconditional restricted-model theorem and can be worthwhile.
2. A random-order streaming lower bound for decision MCSP, a promise version,
   or a canonical minimum-circuit output does not automatically lower-bound
   relational `search-MCSP^SAT[s]`. Cycle 77 already shows that canonical
   output can be harder than the relation, and average-order success is not the
   same resource model until the success and order quantifiers are transferred.
3. The Millennium implication requires the exact MMW relation at
   `s(n)=2^(n/log^* n)` and exclusion of a one-pass solver with both
   `N^epsilon` space and `N^epsilon` update time for one fixed `epsilon>0`.
   A random-order theorem has full reach only if it proves this statement for
   every valid relational solver (or is accompanied by a theorem reducing an
   MMW solver to the random-order model without changing exactness, oracle
   access, space, or update time). Near-linear query complexity alone cannot
   cross this gate.

Accordingly the bounded prospect should be phrased as an exact theorem about a
named random-order model, with no `P != NP` claim. It remains a P-versus-NP
scout, not the next main funnel. Before promotion it must state the relation,
input-order distribution, success probability, oracle model, space accounting,
per-item update time, and a resource-preserving implication to the MMW
hypothesis.

## Next main funnel

Rotate the main funnel to Birch--Swinnerton--Dyer, specifically the decorated
prime-twist certificate gate for `433a1` at `p=7`. This is selected because it
has a concrete finite falsification before any asymptotic claim: define the
local Selmer functional `lambda_q` and the derived modular-symbol coordinate
`c(q,ell)` in common determinant lines, then test whether `c` can be Frobenian
in one finite extension jointly with `lambda_q`.

The first main checkpoint is not equidistribution and not BSD. It is the exact
finite-governing-extension dichotomy:

- construct a finite Galois extension and prove that both coordinates factor
  through its Frobenius classes, with the twist-local comparison and all
  primitivity hypotheses uniform; or
- exhibit two admissible pairs with identical proposed finite Frobenius data
  but different derived coordinate, thereby falsifying this route.

If the factorization survives, Chebotarev and explicit reciprocity become
separate later gates toward a certificate-density theorem. Even that theorem
would be a bounded arithmetic advance, not the full BSD conjecture; promotion
beyond it requires an explicit bridge to the official all-curves rank and
leading-term statement. The choice is therefore based on a non-equivalent,
falsifiable production lemma, not on a claim that the current route already has
Millennium reach.

No Millennium problem is claimed solved.
