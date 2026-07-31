# Positive square energy of every tricyclic graph

`paper.tex` proves that every finite simple connected graph `G` with `n`
vertices and `n + 2` edges satisfies

```text
s+(G) >= n.
```

The manuscript does not claim strict inequality globally because the DNN
certificates can meet their auxiliary boundary and not every resulting
spectral equality case has been classified.

## Proof map

- Cyclic block ranks are classified exhaustively as `1+1+1`, `2+1`, or `3`.
- Rank `1+1+1` is the established tricyclic cactus theorem.
- Rank `2+1` is one theta block plus one cycle block. An exact DNN sieve leaves
  only `Theta(1,2,r)+C3` and `Theta(1,2,2)+C5`; induced territories close both.
- A rank-three block suppresses to exactly four kernels: four-path theta,
  doubled triangle, `K4`, or doubled `C4`.
- The paper includes the DNN correlation dual, exact path-elimination lemma,
  parity monotonicity, finite certificate ledgers, and structural deletion
  repairs. These arguments cover arbitrary subdivisions and rooted trees, not
  merely graphs through a fixed order.

The detailed proof objects synthesized by the paper are in
`positive-square-energy/tricyclic-general/`.

## Verify

The exact finite-certificate audit uses integer and rational arithmetic. It
directly reconstructs all 56 physical non-all-odd `K4` rows from their seven
switching invariants, checks sign transport without transporting path lengths,
and explicitly enumerates all 64 all-odd long/unit subsets. Of those subsets,
57 are DNN-audited (`42` with at least three long paths, `12` adjacent and `3`
opposite two-long placements); `6` one-long subsets use structural deletion and
the no-long subset uses the attached-`K4` packet. The doubled-triangle audit
separates its `28` DNN physical rows from its `4` structural class-`111` rows
and checks the two noncanonical class-`111` long-path tangent certificates.
The four-path output describes nine representative symbolic records, including
the one-unit `e=0` endpoint case; it does not claim to reprove the analytic
inequalities that turn those records into all-length coverage. The verifier
rejects thirteen deliberately corrupted certificate variants:

```sh
python3 research/tricyclic-finite-rational-certificates-verifier.py
python3 -O research/tricyclic-finite-rational-certificates-verifier.py
```

Both runs should print `tricyclic finite rational certificates: exact audit
passed` and digest
`a34ed2d3898c1a244e861ce11ffb51d84d65eb4409066f0745829de5a8ca58b8`.
This value is the expected canonical payload digest embedded in the verifier
and mirrored here as the human-readable manifest.
The audit is corroborative; the paper proves the analytic and structural
reductions separately.

## Build

From the repository root:

```sh
bash scripts/build-paper.sh all-tricyclic-graphs
```

The build produces `all-tricyclic-graphs/paper.pdf`. The paper includes an AI
disclosure, a scoped nonclaim, and no publication step.
