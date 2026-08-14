# K2763 all-length structural/spectral packet

The complete `R7G1` replay leaves exactly two keys outside its rational and
cost-six atom lanes: residual source `28385`, global kernel `2763`, at the
canonical target and physical-path frontier `10`.  The row consists of the 13
odd singleton edges

```text
03 05 06 12 14 16 24 26 35 36 45 46 56.
```

Numerical Gram minimization is not a certificate here.  Its stable objective
values are about `6.086730975` and `6.034354813`, respectively, so these are
genuine non-DNN targets rather than rationalization failures.

## Canonical target and rooted trees

Exact permutation expansion gives

```text
det(xI-A)=(x+1)^2 (x^2-3) (x^3-2x^2-7x-2).
```

The quadratic contributes the positive root `sqrt(3)`, with square `3`.  The
cubic is negative at `2` and has positive leading coefficient, so it has a
positive root greater than `2`.  These two positive eigenvalues alone have
square sum greater than `3+4=7=|V|`.  Thus the canonical target satisfies
`s^+(G)>|V(G)|`.  There is also an attachment-uniform structural proof.  The
vertices `{0,3,5,6}` induce an actual `K4`, while `{1,2,4}` induce an actual
triangle.  Assign every rooted tree to the part containing its root.  The
established rooted `K4` packet has credit `sigma=s^+-|V|>2`, and an attached
triangle has positive credit.  Induced square-energy superadditivity therefore
proves the claim, strictly, with arbitrary rooted trees.  Edges crossing the
two induced parts are simply unused.

## Frontier 10

Replacing edge `45` (physical path index `10`) by a path of length three gives

```text
det(xI-A)=(x+1)^2 (x^3-4x-1) (x^4-2x^3-8x^2+3x+10).
```

The quartic is negative at `3` and has positive leading coefficient.  It
therefore has a positive root greater than `3`, whose square alone is greater
than `9=|V|`.  Hence this target also satisfies `s^+(G)>|V(G)|`.

## The all-length packet

Write

```text
A={03,05,06,35,36,56},   B={12,14,16,24,26,46}.
```

These are two physical `K4` supports meeting only at branch vertex `6`; the
remaining physical path is `45`.  Every path in this parity row is odd.

First consider the one-vertex union `U` of the two actual `K4` supports,
including arbitrary rooted trees assigned to their roots, but not the `45`
path.  Then

`sigma(U)>=1`.                                                (1)

Indeed, put the first attachment-uniform actual-`K4` packet, including the
common vertex `6`, in one induced territory.  It has credit greater than two.
The vertices `{1,2,4}` of the other support, with all rooted branches and the
three remnants ending toward deleted vertex `6`, form an attached odd
unicyclic territory.  Every attached odd unicyclic graph has credit strictly
greater than `-1`.  Induced square-energy superadditivity proves (1), strictly.

Now let the `45` path have any odd length at least three.  Delete one internal
vertex together with the rooted tree based there.  This is a nonempty induced
tree of credit `-1`.  Its induced complement is `U` with the two remnants of
the opened path as rooted trees, so (1) gives

`sigma(G)>=1-1=0`.                                           (2)

This proves the descendants in which only coordinate `10` grows.  For a
descendant in which some coordinate `i!=10` also grows, use the checked exact
rational owner at `c+2e_i`; its length vector is dominated by the descendant,
so retaining its branch Gram and applying fixed-parity path monotonicity closes
all further simultaneous lengthening and arbitrary rooted-tree attachments.
Thus every same-parity descendant of frontier `10` is covered.

For a descendant of the canonical target, there are three exhaustive cases.
If no path grows, use the canonical attachment packet above.  If only `45`
grows, use (2).  Otherwise choose a grown coordinate `i!=10`; its length vector
dominates the checked coordinate target `c+2e_i`.  The exact rational owner at
that target retains its branch Gram, and fixed-parity path monotonicity covers
all further coordinate lengthening and rooted trees.  Thus the canonical key
also has an explicit all-length lift; no spectral subdivision monotonicity is
asserted or used.

`rank7_order7_pack_auditor.py` reconstructs both adjacency matrices from the
authenticated residual row, recomputes their characteristic polynomials over
the integers, checks the displayed factorizations and sign arguments, and
assigns these two keys to a disjoint structural/spectral packet lane.  The full finite
canonical-plus-coordinate ledger is consequently complete: all 573,496 target
keys have exact owners.

The packet above supplies the previously missing same-parity all-length and
arbitrary rooted-tree lifts.  A full exact replay therefore sets both
`finite_target_gate_eligible=true` and `theorem_gate_eligible=true`.  A partial
or digest-only replay remains ineligible.
