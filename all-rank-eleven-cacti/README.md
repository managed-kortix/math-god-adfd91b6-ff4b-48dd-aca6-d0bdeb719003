# All cyclomatic-rank-eleven cacti

This manuscript proves that every connected cactus `G` of cyclomatic rank 11
on `n` vertices satisfies

```text
s+(G) > n.
```

The result is scoped to rank-eleven cacti. It does not claim a universal
resolution of the Akbari--Kumar--Mohar--Pragada--Zhang conjecture.

## Proof structure

- The sharp cactus DNN theorem and exact frontier verifier leave precisely
  `T^10Q` and `T^9PP`.
- `T^10Q` is parity-complete: the all-rank hostile-cycle paper covers
  `q=1 mod 4`, and the new all-rank nonhostile note covers even `q` and
  `q=3 mod 4`.
- The exact `T^9PP` proper colored audit is `266=253+13`.
- Corrected actual-bridge pruning uses only certified leaf/complement pairs; it
  does not state the false blanket leaf lemma. Its only endpoints are
  `T^9P|P` and `P|A_9|P`.
- The geometry-aware `T^9P|P` certificate closes `50399/50399` rows. The
  standalone `P|A_9|P` verifier closes `43151/43151` complete central
  position/cut-owner and theorem rows, and the proved connector-lifting lemma
  realizes them in the original cactus.
- The fully shared certificate closes `115512=115502+10` incidence classes.

## Physical certificates

The verifiers have different integrity boundaries. The standalone `P|A_9|P`
verifier checks concrete `C3` positions and intervals, ordered abstract marks,
complete pentagon demands, and post-ownership theorem records. Its exhaustive
final-owner domain contains every shared cut (including an all-router cut if
one occurred), and
every private position of every sacrificed router. Root and child resolution
must agree for every interval position; active-child nesting is unique; owner
records are duplicate-free and have the exact independently derived domain. It
does not itself materialize arbitrary-length external connectors. The lifting
lemma in `paper.tex` and `physical-lifting-note.md`
assigns each complete external pentagon and its entire ordered connector chain
to its mark owner, including coincident-mark consistency, and assigns every
off-hull tree to its unique anchor owner. It proves connected, induced,
disjoint, exhaustive territories with unchanged cycles and ranks.

The `T^9P|P` and fully shared verifiers additionally materialize named
`C3`/`C5` vertices, cyclic edges, canonical shared cuts, connector paths and
remnants, consecutive router intervals, arbitrary-forest attachment
obligations, and final owner domains. Expected graph and attachment domains are
reconstructed independently of submitted certificates. Owner-induced graphs
must be connected cacti with the rederived complete-cycle profile; only then is
a packet theorem selected from a closed whitelist. The exact `T^9P|P`
projection and 43145 rebound plans independently corroborate both ordered
external-role orientations after exchanging `P_0,P_1`; the lifting lemma, not
that executable, supplies uniformity in two arbitrary connector lengths.

All theorem gates use explicit `RuntimeError` checks and run under both normal
Python and `python -O`. Unknown profiles, missing domains, malformed intervals,
split cycles, unreachable connectors, forged theorem records, or changed
digests fail closed. Hostile mutation suites reject 10 mutations for
`P|A_9|P`, 31 for `T^9P|P`, and 25 for fully shared `T^9PP`.

Principal SHA-256 gates:

```text
P|A9|P canonical rows:
  0bf53914ae760002386b4b94e4de2d0cccbe61725063b4a46435bcd49c70403b
P|A9|P complete position/cut-owner and theorem records:
  58f9951b620fa9f4830724a8bbc5b426a6125437b11c84b125d4ee63488dd3ec
P|A9|P repairs:
  9b8631b8d1b92970584156e2e444fedf78c2394e0867d43c1204aa09c4f49e0e
T9P|P combined geometry:
  3da4ebec400a236a10ffb242603b485c7b549a2503fa5c4ee061dcc7afa70b7b
T9P|P ordinary physical owners:
  63305ff27b19d07bd705eec8f489dcfcfd12cc8cc129dbe93cf914d1c29c4a1a
T9P|P private certificates:
  815040d4da58efb5edb5660de47d14d4012eb6245afcabb5b77c98e2a8a8e43d
T9P|P six repairs:
  740a1385503bdf58761be38057ca9d548f85289183ef4a4c515fbc6038398da3
fully shared canonical rows:
  65f4d845ff0ef17ce7880992810de149fd2108927e2ef03b8fac57032ac72ce2
fully shared ordinary physical proofs:
  5d134b875d7ff369c74f361f4fd58a2ee7262c8bfdaba0453987f46f3391b70e
all 517923 safe physical choices:
  071df2e10153eb21a8153cc3e45de6768e350a2257a692b0b03979227bc37a0f
fully shared repairs:
  eedc3bebd64e4711849115b3846db2eee2a93cd7ffee628e49f7a3133f73c324
```

## Exact reproduction

Python 3.10 or newer is required. The certificate programs use the standard
library and repository-local modules; no network service, secret, numerical
eigensolver, or environment file is needed.

Run from the repository root:

```bash
python3 research/rank-eleven-cactus-dnn-residual-frontier-verifier.py
python3 -O research/rank-eleven-cactus-dnn-residual-frontier-verifier.py
python3 research/rank-eleven-residual-partition-audit.py
python3 -O research/rank-eleven-residual-partition-audit.py
python3 research/rank-eleven-a9-two-interface-verifier.py
python3 -O research/rank-eleven-a9-two-interface-verifier.py
python3 research/rank-eleven-t9p-p-endpoint-frontier-verifier.py
python3 -O research/rank-eleven-t9p-p-endpoint-frontier-verifier.py
python3 research/rank-eleven-t9pp-fully-shared-first-phase-verifier.py
python3 -O research/rank-eleven-t9pp-fully-shared-first-phase-verifier.py
```

Expected headline results:

```text
sharp-DNN residuals: T^10Q, T^9PP
colored T^9PP: total 267, proper 266, direct 253, structural 13
P|A9|P: 43151 = 43145 + 6 closed
T9P|P: theorem-certified endpoint rows 50399 / 50399
fully shared T^9PP: 115512 = 115502 ordinary + 10 repairs
```

The fully shared verifier is computationally substantial because it checks all
517923 safe physical candidate certificates, in addition to the ten repairs.

The rank-ten input is exactly Theorem 6.1 of
`all-decacyclic-cacti/paper.tex`: every connected cyclomatic-rank-ten cactus is
strict. Consequently it applies literally to a connected rank-ten territory
with connector remnants and attached trees; no unproved rooted strengthening
is being used.

## Build

```bash
bash scripts/build-paper.sh all-rank-eleven-cacti
```

The resulting PDF is `all-rank-eleven-cacti/paper.pdf`.

## Exclusions and disclosure

The proof does not use the provisional `43151=43116+35` score, the withdrawn
symbolic `50382/50399` closure, its historical 17-row blueprint, the conditional
frontier as an endpoint theorem, any open two-pivot winding claim, or historical
router-reachability assertion R11. In particular, it does not claim an all-rank
`T^rPP` theorem.

The manuscript is AI-generated and claims no human authorship, review, or
verification. Its mathematical authority is the written proof and the cited,
reproducible fail-closed certificates.
