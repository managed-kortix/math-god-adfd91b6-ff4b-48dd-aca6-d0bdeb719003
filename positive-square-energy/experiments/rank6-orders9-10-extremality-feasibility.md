# Rank-six orders 9--10 extremality feasibility

The exact artifact is
`rank6_orders9_10_extremality_feasibility.json` (SHA-256
`3fd68dbaa2a250f2bada401f14c79904314333041d7c15fb7fc4ffcc12bb5f05`).
It deterministically audits all 1,419 support/rank pairs induced by the 444
isomorphism classes in the proper odd-support census.

## Result

| rank | feasible | infeasible | unresolved |
|---:|---:|---:|---:|
| 3 | 19 | 209 | 216 |
| 4 | 67 | 0 | 349 |
| 5 | 99 | 0 | 228 |
| 6 | 82 | 0 | 99 |
| 7 | 36 | 0 | 15 |
| **all** | **303** | **209** | **907** |

The sieve rigorously removes 209 candidate pairs. All removals are rank-three
pairs and carry an explicit independent set of four vertices, which forces
four nonzero mutually orthogonal vectors in dimension three. No support class
is removed at every candidate rank, so all 444 supports remain represented in
the narrowed frontier.

The 303 feasible records carry spanning integer orthogonal representations.
For each representation, every nonedge inner product vanishes and the nonedge
symmetric tensors have rank `binom(r+1,2)-1`. The rank computation is certified
by a nonzero minor modulo one of three explicitly checked 31-bit primes; such a
minor is also nonzero over the rationals. Orthogonality supplies the matching
rational upper bound for the tensor rank.

The remaining 907 pairs are unresolved, not infeasible. Likewise, a feasible
record establishes only the displayed rational orthogonal representation and
the extremality tensor-rank condition. It does not establish edge positivity
or path-derivative KKT compatibility, and therefore does not by itself certify
a DNN extreme ray for the original kernel problem.

## Reproduction

Run from the repository root:

```sh
python3 experiments/rank6_orders9_10_extremality_feasibility.py --write
python3 -O experiments/rank6_orders9_10_extremality_feasibility.py \
  --verify experiments/rank6_orders9_10_extremality_feasibility.json
```

The verification recomputes the seeded 64-trial exact search, compares the
complete payload byte-for-byte at the data-model level, checks pair coverage,
and rechecks every stored certificate. It passes under optimized Python, so no
certificate check depends on `assert` statements.
