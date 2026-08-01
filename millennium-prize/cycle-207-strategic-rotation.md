# Cycle 207: strategic rotation after the HWB all-order gate

## Recommendation

Rotate the main funnel out of P versus NP.  Do not promote another OBDD,
communication, query, or decision-MCSP construction merely by strengthening
its exponent or making it hold for every order.

Cycle 207 closes the selected gate cleanly: `HWB_(8m)` contains a linear INDEX
minor at the midpoint of every variable order and therefore has exponential
deterministic OBDD width in every order.  But HWB is itself computable by
polynomial-size circuits.  Thus the theorem simultaneously demonstrates the
strength of the order-oblivious minor argument and its inability, by itself, to
distinguish easy circuits from hard ones.  More all-order examples would enlarge
the restricted-model theorem without crossing the current P-versus-NP barrier.

The attempted MCSP continuation has three independent missing ingredients.

1. **Entropy:** at the MMW threshold
   `s(n)=2^(n/log^* n)`, packing easy truth tables supplies only
   `O(s log(n+s))=N^o(1)` forced state bits, not a fixed power of `N`.
2. **Equivariance:** an exact relational `search-MCSP^SAT` solver may output any
   valid small circuit.  A canonical circuit, address, or decomposition is not
   available unless a reduction works uniformly for every valid output.
3. **Direct sum:** independent HWB/INDEX restrictions do not automatically add
   space or update-time cost for a shared adaptive solver.  Such additivity
   would require a new relation-level direct-sum theorem, not a disjoint-copy
   construction.

These are obstructions to the proposed transfer, not impossibility theorems for
all MCSP approaches.

## Exact P-versus-NP re-entry criterion

P versus NP returns to the main funnel only with a candidate for one of the
following two statements.  Put `N=2^n` and `s(n)=2^(n/log^* n)`.

\[
 \exists\epsilon>0\ \forall n\gg1:\quad
 \text{no exact one-pass search-MCSP}^{SAT}[s]
 \text{ solver has both space and update time at most }N^\epsilon;
\]

or a reduction from every such solver to a named problem with an unconditional
`N^delta` resource lower bound, where `delta>epsilon` and all reduction overhead
is `N^o(1)`.

The reduction must preserve exactness, the SAT-oracle convention, one-pass
 access, and both space and per-item update time up to `N^{o(1)}` factors.  It
 must handle every valid relational output, not only a minimum, canonical, or
 uniquely decoded circuit.  If the target
lower bound is assembled from many instances, the statement must include a
proved direct-sum inequality at the solver-state level.  If it uses a symmetry
or random relabeling, the decoding must be equivariant and must not insert an
input-readable selector.

This criterion is exact enough to referee line by line: every resource and
quantifier has a named preservation obligation, and one failed obligation
rejects the proposed transfer.  The first alternative is the full MMW-strength
lower-bound gate; the second is a resource-preserving route to it.  The
criterion is not itself a lower bound and does not claim that either statement
is true.

## Rotation rule

Until a candidate meets that re-entry criterion on paper, score every further
all-order easy-function or decision-MCSP gate as
`(barrier crossing, non-equivalence, finite falsifiability, official transfer)
=(0,1,1,0)`.  The main funnel should rotate to portfolio discovery rather than
declare a replacement P-versus-NP gate.  Promote another Millennium lane only
when it supplies a frozen non-equivalent production lemma with an exact
falsifier; none of the presently recorded RH endpoint, Yang--Mills finite-block,
Hodge graph/link, or frozen Navier architectures earns promotion merely by the
failure of this P-versus-NP transfer.

No circuit lower bound, `P != NP`, or Millennium result is claimed.
