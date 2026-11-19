# Frozen B7-l6 two-high profile root cardinality

## Exact scope

This layer applies only to early C-profile cells
`12-17,36-43,55-59`. They are exactly the 19 census TIMEOUT cells with high-C
mask `11`, after removing the eight one-high cells already closed by the exact
inaccessible-pair/Hall composition. It imports no witness or later refinement
units.

## Authoritative identity

Six holes leave `C(18,2)-6=147` arcs. Every vertex has outdegree eight or nine,
so `147=18*8+high(V)` and exactly three vertices are high. Let
`A={1,...,8}` and `B={9,...,15}`. The root normalization forbids arcs from `A`
to the root or either C vertex. Thus

`sum_(a in A) d+(a)=64+high(A)`, `e(A,A)=28-H(A)`, and therefore

`e(A,B)=36+H(A)+high(A)`.

Fresh, separately named unary counters enforce exactly three global highs and
every threshold consequence of this root identity. The extension adds exactly
2,433 variables and 9,571 clauses to each profile CNF. The checker reconstructs
the frozen base, all profile and selector clauses, and all counters without
importing the campaign producer. Its semantic audit checks 262,144 degree
vectors and all 116 `(H(A),high(A))` arithmetic cases.

## Certificates and implication

Pinned CaDiCaL 1.7.3 produced 19 textual LRATs, and pinned `lrat-check` accepted
all 19. The raw proofs total 217,996,726 bytes; retained `xz -3` artifacts total
20,979,196 bytes, strictly below the exclusive 250,000,000-byte cap. Fresh
replay regenerates and independently checks every CNF, authenticates every raw
and compressed proof, and reruns `lrat-check`.

The composition verifier combines the original 33 certified profile cells, the
eight one-high profile closure, and these 19 cells. These scopes are disjoint
and exhaust `0..59`. It independently reconstructs 42 parents, 30 states, 60
`S7(B)` orbits, 544 parent/orbit incidences, and checks each parent-support
family under all 5,040 permutations. Consequently the entire frozen clean
`B7-l6` parent campaign is closed. This does not close any other residual B7
group, all residual B7 generally, order 18 generally, or Seymour's conjecture.
