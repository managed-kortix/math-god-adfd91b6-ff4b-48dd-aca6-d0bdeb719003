# Independent hostile audit: rational packet all-length inference

Date: 2026-11-08. Scope: mathematical contract of the fifth-family wrapper,
its induced-packet engine, and the inherited exact shared verifier. This is
not an order-eight closure claim. The VII--XI uncommitted files were not
available in this isolated sandbox: attempts to copy them from the parent
session failed. Their stated contract was read in the parent session log;
their actual bytes and 19,699 certificates have **not** been audited here.
The checked baseline is origin/main as fetched on this date.

## Verdict

The all-length and rooted-tree inference is valid for a correctly regenerated
physical path ledger and an accepted shared rational packet. In fact, for
this mode the canonical packet alone suffices. The coordinate packets are
redundant for upward feasibility, though they can remain useful as a uniform
frontier interface for other owner types. No counterexample to this inference
was found. Two exposition qualifications and a replay limitation follow below.

## Exact mathematical reconstruction

Let the branch vectors be unit vectors x_v. For a physical path of length q,
alternate signs on its vertex vectors, so its transformed endpoints are
x_u and (-1)^q x_v. If consecutive transformed correlations are t_j, its
DNN excess is sum_j (1-t_j)/(1+t_j). Set beta=acos((-1)^q<x_u,x_v>).
The angular distances theta_j satisfy sum theta_j >= beta. The function
h(theta)=tan²(theta/2) is increasing and convex on [0,pi), so Jensen and
the spherical triangle inequality give

    sum h(theta_j) >= q h(beta/q) = f_q.

An equal-angle great-circle chain attains this bound. For antipodal endpoints
choose an auxiliary unit direction; it exists after enlarging the space.
For q=1, beta=pi the cost is infinite, so no accepted finite packet has that
case. Coincident endpoints have zero optimum. Thus every exact packet is
an upper bound for the optimal path cost at its branch Gram, not necessarily
itself an optimal chain.

For beta fixed and q>=1, put z=beta/(2q). Away from the singular endpoint,
the derivative of q tan²(z) is

    tan²(z) - 2z tan(z) sec²(z).

For z>0 it has the sign of sin(z)cos(z)-2z < 0. Consequently f_(q+2)<=f_q,
with equality exactly when beta=0. Singular cases follow by limits. This is
monotonicity of the **optimized** path cost with fixed endpoints and parity;
it is not monotonicity of arbitrary stored waypoint chains, adjacency
spectra, or a parity-changing subdivision.

For an accepted canonical packet let C_p denote each exact path-chain cost.
Then sum f_(c_p)(r_p)<=sum C_p<=6. Any length vector l>=c with even
coordinate differences has the same transformed endpoints. Hence

    sum f_(l_p)(r_p)<=sum f_(c_p)(r_p)<=6.

Install the optimal chains in a common enlarged Euclidean space. Their
interiors are distinct graph vertices; there is no requirement that their
vectors be distinct. All nonedge correlations are unrestricted. This produces
a PSD correlation matrix on the whole realization simultaneously. The result
is existential for every finite length vector, not one finite matrix serving
infinitely many graphs. Rationality of the new optimal chains is unnecessary:
the exact rational packet plus the analytic inequality is the proof.

Within a parallel class, sort odd paths first and assign the possibly unique
length-one path to the distinguished shortest odd coordinate. Simplicity
ensures that the other odd lengths are >=3; even lengths are >=2. Thus every
physical realization in the parity orbit can be relabeled to dominate the
canonical vector. Alternatively one may start at any stored +2 frontier
that it dominates. Shared endpoints make these frontier certificates valid,
but one must never add all their individual costs together.

## Rooted trees: direct construction, not a citation gap

For each new tree vertex choose the negative of its parent's vector in the
original (untransformed) Gram. Every new edge then has correlation -1 and
DNN contribution 2/(1-(-1))=1, hence zero excess. Repeating from any branch
or internal vertex constructs every finite rooted-tree attachment. More
generally one-vertex additivity follows by orthogonally aligning the shared
unit vector of two feasible Grams, with complementary orthogonal spaces;
the reverse inequality follows by restriction. Here only the constructive
upper bound is needed. With L core edges and t attached edges, rank seven
means n_core=L-6, and kappa<=L+6+t. The cited DNN inequality s^-<=kappa
therefore yields s^+>=2(L+t)-(L+6+t)=L-6+t=n. This audit reconstructs the
attachment argument independently; it does not reprove the underlying DNN
spectral inequality.

## Encoding, dimensions, and numerical search

The inherited verify_shared checks eight branch rows, fourteen canonical
and extended paths, seven parameters per vector, and exact path-specific
internal counts on every frontier. It audits parameters before dot products,
so dot's zip truncation cannot mask a short vector on this acceptance route.
For a parameter tuple a, rational_unit returns

    ((1-S)/(1+S), 2a/(1+S)), S=sum a_i²,

whose norm squared is ((1-S)²+4S)/(1+S)²=1 exactly. With rational parameters
S>=0, so its denominator never vanishes. Exact transformed correlations lie
in [-1,1]; the verifier rejects -1 rather than allowing division by zero.
Thus all accepted path costs are nonnegative. Encoding by a common positive
denominator loses no information: numerator scaling is exactly reversible.
Wrong dimensions cannot hide nonunit vectors when these checks are used.

The included dependency-free test extracts the actual inherited functions,
checks exact unit identities and a feasible synthetic 14-path packet, and
rejects six malformed dimension/width/denominator variants. It passed in
normal and optimized Python. This is not a census replay or an artifact audit.

Floating descent, slerp and stereographic rounding only propose parameters;
acceptance uses Fraction costs. They can cause missed witnesses or execution
failure, never a false accepted inequality through verify_shared. However,
the fifth wrapper's --audit reruns numerical search and rewrites owner and
remainder streams before comparing the report. This is not a pure read-only
replay of stored witnesses; numerical-library/platform variation can impair
reproduction. A separate strict JSON decoder and Fraction-only stored-owner
replay would be preferable. Hash authentication supplies integrity relative
to an upstream report, not independent verification of upstream mathematics.

## Requested wording corrections

1. 'The stored packet owns every same-parity subdivision it induces' should
mean every simple physical realization in its parity orbit after the stated
within-class relabeling. It must not suggest waypoint interpolation or
unrestricted parity-changing subdivisions.
2. The structural theorem's statement that coordinate targets are essential
because a canonical cost-six Gram need not control its descendants is false
if that canonical Gram is a feasible DNN certificate: the proof above retains
it and controls every descendant. Different finite spectral or structural
owner types may require additional frontier/lift hypotheses. This incorrect
motivation does not invalidate the stronger shared-packet inference.
3. Auxiliary spaces may be added to the common branch-vector space; 'mutually
orthogonal auxiliary spaces' does not mean internal vectors themselves must
be orthogonal to branch vectors or to other paths.

No inference here verifies the completeness of VII--XI ownership counts,
their chained remainder identities, or any full kernel-order theorem.

## Follow-up exact artifact audit

The initial isolated review above deliberately did not authenticate the then-
unavailable VII--XI artifacts.  That limitation is now removed by
`experiments/tests/test_rank7_order8_induced_packet_chain.py`.

The strengthened gate is read-only and uses no numerical search.  Its original
VII--XI audit was subsequently extended through the accepted XII lane. It hard-pins
the sixth-stage report and compressed remainder as its trust root, regenerates
the complete 492,812-row rational-search stream from the authenticated census
chunks and index artifact, and compares all six fields of every chained source
row with that regeneration.  For each of the 21,487 VII--XII owners it enforces
strict canonical JSON and exact types, uniqueness, exact target-family
membership, source metadata, and permitted packet dimensions/denominators,
then decodes to `Fraction` and invokes the inherited exact `verify_shared`.
It independently recomputes each physical total and classification digest and
requires each next remainder to be the ordered byte-for-byte source complement.
The five hard-coded partition identities are

```
76085 = 6817 + 69268
69268 = 4219 + 65049
65049 = 3765 + 61284
61284 = 2731 + 58553
58553 = 2167 + 56386
56386 = 1788 + 54598.
```

Hostile review first reproduced two coherent false accepts in the former fast
identity test (a duplicated owner and a zero witness denominator after digest
rewriting), then required this full semantic replay.  A second review found and
repaired two remaining laundering routes by pinning the sixth trust root and
checking the complete hard-coded target-family reports plus authenticated orbit
sums.  The ultimate re-review returned ACCEPT.  Both the exact chain audit and
the dependency-free hostile contract test pass under ordinary and optimized
Python; the latter now uses explicit runtime checks rather than optimization-
removable `assert` statements.
