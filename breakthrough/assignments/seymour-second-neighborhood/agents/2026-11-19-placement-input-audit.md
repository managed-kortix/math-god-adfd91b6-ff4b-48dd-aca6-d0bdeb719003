# Bounded hostile audit: placement lambda splits

Assignment: Seymour second neighborhood; LANE=breakthrough.
This is a bounded audit, not a lane-state update or a solved-result claim.
The runtime session ID differs from the registered Breakthrough root; no
registry, trigger, or active frontier was changed.

## Exact coverage lemma

Let B have seven elements, D be the marked hole-degree-at-least-two
vertices in B, and K be the common C-dominators. For |D|=beta and
|K|=kappa, lambda=|D intersect K| satisfies

    max(0,beta+kappa-7) <= lambda <= min(beta,kappa).

Proof: the upper bound is inclusion; the lower bound follows from
|D union K|=beta+kappa-lambda <= 7 and nonnegativity. Conversely any
integer in the interval is realized by choosing lambda elements of K
and beta-lambda elements of B minus K. This converse is only a subset
statement, not a graph-completion assertion.

Splitting over every integer in this interval is disjoint and exhaustive.
In particular lambda=0 cannot be dropped when beta+kappa<=7 without
an additional proved constraint.

## Independent Task audit findings

The conjunction LK_b iff (K_b and ge2_b) is correctly bidirectional.
The following input/provenance defects remain in m9_k4_placements.py:

1. lam with no kappa/eta is silently ignored because it is only processed
   in the kappa branch.
2. exact() does not validate negative counts. On seven threshold outputs,
   lam=-1 selects count 6, lam=-2 selects count 5, through lam=-6 selecting
   count 1, through Python negative indexing. These are not valid shards.
3. Counts outside the conditional intersection interval can generate empty
   shards. They cannot establish coverage of omitted valid counts.
4. Programmatic emit validation is weaker than argparse validation; expensive
   build() precedes some validation.
5. Printed summary omits kappa, eta, lambda, weakening provenance.

These findings do not invalidate a previously checked UNSAT formula. They do
require auditing actual invocation parameters before using a shard ledger as
an exhaustive parent cover. No inference about missing certificates is made.

Recommended owner action: validate all split arguments before build(), reject
lam without kappa/eta, enforce the displayed interval, include all split
parameters in logs, and regression-test invalid values without solver calls.

No publication or conjecture-resolution claim is warranted.
