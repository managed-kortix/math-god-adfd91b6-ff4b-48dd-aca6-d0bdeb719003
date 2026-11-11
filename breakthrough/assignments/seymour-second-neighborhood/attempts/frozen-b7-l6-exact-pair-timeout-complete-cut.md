# Frozen B7-l6 exact-pair TIMEOUT complete cuts

## Scope

This campaign is relative only to the 33 `TIMEOUT` singleton memberships in the
committed five-second exact-pair scout. It preserves each selected singleton
parent, exact inaccessible pair, and all two negative plus seven positive `q`
units. It creates no certificate and does not alter an ancestor CNF.

## Forced orientation

For a membership let `l` be its low C vertex and put `S=N+(l)`. Each endpoint
`x` of the exact inaccessible pair has `q(l,x)=false`. For every `s in S`, the
two-walk `l->s->x` is therefore impossible, so `s->x` is false. If `{s,x}` is
not one of the six holes, exact hole equivalence and arc exclusivity then force
`x->s`. Thus the complete endpoint-to-`S` orientation is already implied by the
existing CNF. Adding its unit clauses would create only propagation redundancy,
not a genuine split, so this layer emits no CNFs.

For each parent the checker reconstructs the six holes and validates

`6 = h(l) + h({x,y},S) + 1[{x,y} is a hole] + h_other`.

It also checks the endpoint-by-endpoint identity: exactly
`16-h({x,y},S)` of the 16 endpoint/`S` pairs are forced present arcs directed
from the inaccessible endpoint into `S`.

## Semantic classes

Membership `000`, pair `{0,3}`, is exceptional. The other 32 packets have one
endpoint in the root/A side `{0,...,8}` and one in C. Their root/A endpoint has
zero holes into `S`. Define `epsilon` as the pair-hole bit, `b=|S intersect B|`,
and `chi` as the C-endpoint hole load into `S`. The exact 15 packet classes are:

```text
(0,0,4): 062                 (0,0,5): 023
(0,1,2): 070                 (0,1,3): 034,075
(0,1,4): 024                 (0,2,1): 003,044,080,082,091
(0,2,2): 005,006,011,054,059,084,093
(0,2,3): 039,047             (1,0,3): 061
(1,0,4): 022                 (1,1,1): 064
(1,1,2): 028,069             (1,1,3): 033
(1,2,1): 010,014,015,051,097 (1,2,2): 019
```

Together with `exceptional-membership000`, the census has 16 classes. The
canonical semantic manifest is
`experiments/m6-b7-l6-exact-pair-timeout-complete-cut.tsv`.

## Scout and verification

Pinned CaDiCaL 1.7.3 was run for ten seconds on each unchanged singleton CNF,
with two jobs. All 33 runs timed out; there were no SAT or UNSAT results. These
are timing observations only. The independent checker reconstructs the scope,
parents, holes, cuts, classes, identities, existing singleton CNF hashes, solver
provenance, timings, and exact status sequence.

Run from `experiments/`:

```sh
python3 check_m6_b7_l6_exact_pair_timeout_complete_cut.py --scout
python3 test_m6_b7_l6_exact_pair_timeout_complete_cut.py
```

No LRAT, certificate, CNF, or commit is produced by this campaign.
