# K2763 direct frontier closure

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

## Canonical target

Exact permutation expansion gives

```text
det(xI-A)=(x+1)^2 (x^2-3) (x^3-2x^2-7x-2).
```

The quadratic contributes the positive root `sqrt(3)`, with square `3`.  The
cubic is negative at `2` and has positive leading coefficient, so it has a
positive root greater than `2`.  These two positive eigenvalues alone have
square sum greater than `3+4=7=|V|`.  Thus the canonical target satisfies
`s^+(G)>|V(G)|`.

## Frontier 10

Replacing edge `45` (physical path index `10`) by a path of length three gives

```text
det(xI-A)=(x+1)^2 (x^3-4x-1) (x^4-2x^3-8x^2+3x+10).
```

The quartic is negative at `3` and has positive leading coefficient.  It
therefore has a positive root greater than `3`, whose square alone is greater
than `9=|V|`.  Hence this target also satisfies `s^+(G)>|V(G)|`.

`rank7_order7_pack_auditor.py` reconstructs both adjacency matrices from the
authenticated residual row, recomputes their characteristic polynomials over
the integers, checks the displayed factorizations and sign arguments, and
assigns these two keys to a disjoint direct-spectral lane.  The full finite
canonical-plus-coordinate ledger is consequently complete: all 573,496 target
keys have exact owners.

This does **not** close the all-length single-block theorem.  Unlike a retained
Gram, these two finite spectral certificates currently have no proved
same-parity all-length or arbitrary rooted-tree lift.  The auditor therefore
sets `finite_target_gate_eligible=true` but deliberately keeps
`theorem_gate_eligible=false`.
