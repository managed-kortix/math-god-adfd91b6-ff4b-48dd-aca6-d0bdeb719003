# Tick 50: exact m=6 parent frontier

## Frozen parent cover

The six-edge support census, rooted placement cover, and exact necessary
placement filter leave 76,361 canonical parent placements: 23,578 in B6 and
52,783 in B7.  `experiments/m6_parent_cnf.py` now maps either an accepted ordinal
or accepted global cover index to one deterministic full order-18 CNF.  It uses
the first labels in each rooted cell, fixes all 153 missing-pair variables (six
positive and 147 negative), and includes the proved robust vertex-deletion and
arc-minimality conditions.

The independent checker reconstructs the selected frozen row and authenticates
the complete ordered base variable map and clause stream before checking the
exact 153-unit suffix.  The frozen base fingerprints are:

```
variables                    23616
variable-map sha256          cff4c18a...db070e
B6 base clauses              142736
B6 base-clause sha256        22b11867...a12c1
B7 base clauses              142729
B7 base-clause sha256        a21d68c9...341ab
```

The two historical duplicate diagonal units in the base are semantically
harmless and deliberately frozen rather than changing `snc_cnf.py` beneath old
certificate campaigns.

## Exact C-layer funnel

Let

```
lambda = H_RC + H_AC + H_CC,
q      = H_CB,
h      = six-hole count wholly outside C,
r      = e(C,B).
```

Thus `lambda+q+h=6`.  In B6, if `t` is the number of degree-nine
vertices in C, summing the C rows gives

```
t = 6-lambda+r.
```

Hence `lambda=3` forces `r=0` and `t=3`.  There are 14,649 canonical
survivors in this regime, partitioned by `(q,h)` as

```
(0,3): 6286,  (1,2): 5541,  (2,1): 2410,  (3,0): 412.
```

The analogous B7 identity is `t=3-lambda+r`.  The large forced row has
`h=5`, `lambda+q=1`, `r=0`, and both C vertices high; it contains 25,766
canonical placements.

## Scout warning

A temporary 48-parent CaDiCaL scout returned UNSAT quickly on 24 B6 and 24 B7
samples, but no proof was retained.  A hostile audit found that the B6 selector
used `h=3`, not the intended `lambda=3`, and therefore sampled only the
unnecessary `q=0` subfamily of 6,286 rows.  The observations have no theorem
status and are not retained as branch evidence.  Any future structural shard
must name all three parameters `(lambda,q,h)` and put added orientation units in
a versioned shard format checked separately from the immutable parent format.

## Next exact attack

Define a versioned `(lambda,r)` child emitter whose checker authenticates the
parent and then an explicit orientation-cardinality suffix.  Start with the two
forced regimes above, retaining LRAT only after the child cover and semantics
are independently audited.  In parallel seek a human contradiction from the
pointwise B6 identities

```
h_R(c)+h_A(c) = d_C^+(c)+e(c,B)       (all c high),
e(C,B)=0                               (lambda=3),
```

coupled to robust witnesses for the high C vertices.
