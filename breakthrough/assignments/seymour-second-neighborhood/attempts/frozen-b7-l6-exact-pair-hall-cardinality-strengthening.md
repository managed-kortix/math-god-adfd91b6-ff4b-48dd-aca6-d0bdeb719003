# Frozen B7-l6 Hall cardinality strengthening

This certificate-relative layer applies exactly to the 33 residual exact-pair
singleton memberships proved Hall-synchronized by the committed all33 verifier.

There are `C(18,2)-6=147` arcs. Every outdegree is 8 or 9, so
`147=sum_v d+(v)=18*8+high(V)` and exactly three vertices are high. For
`S=N+(low C)`, exact-pair semantics says no vertex of `S` sends an arc to the low
C vertex or either inaccessible endpoint. Writing `U` for the other seven
nonoutneighbors, `sum_S d+=64+high(S)` and `e(S,S)=28-H(S)`. Therefore
`e(S,U)=36+H(S)+high(S)`.

Fresh unary counters count all 56 `S->U` arcs, all 28 holes internal to `S` plus
the eight high indicators in `S`, and all 18 global high indicators. They add
2,433 variables and 9,571 clauses. Pinned CaDiCaL scouts all 33 unsplit CNFs
UNSAT. Pinned `lrat-check` accepts all textual LRATs. Raw proofs total 436,397,454
bytes; `xz -3` artifacts total 47,134,964 bytes, below the 250,000,000-byte cap.

Composition does not subtract overlapping model counts. The certified 172-child
union was subtracted from the overlapping 192-pair cover to produce exactly 20
residual pair cells and 101 memberships. The prior 68 and new 33 membership sets
are disjoint and exhaust `0..100`, closing `03,11,23,25,28,47,49,54`.
