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
The doubled-`C4` audit reconstructs all eight switching classes and separates
`28` canonical DNN rows from the exceptional eight-row automorphism orbit,
which contains four rows in class `110` and four in class `111`.
The canonical digest also commits to every audited doubled-`C4` class count,
first row, failed row, class-`111` long ledger, endpoint definition, and tangent
constant, plus the `K4` endpoints and arithmetic constants. Numeric payload
leaves are integers or rational strings; floats and other non-integral numeric
types are rejected explicitly. The four-path output describes nine
representative symbolic records, including
the one-unit `e=0` endpoint case; it does not claim to reprove the analytic
inequalities that turn those records into all-length coverage. The verifier
rejects 27 deliberately corrupted certificate variants:

```sh
python3 research/tricyclic-finite-rational-certificates-verifier.py
python3 -O research/tricyclic-finite-rational-certificates-verifier.py
```

Both main-audit runs print `tricyclic finite rational certificates: exact audit
passed` and digest
`6d499af761ffa7317a431e5150dac59317618f508896be2c3ed77b250b43c901`.
The all-odd-switching-class audit checks all eight physical parity rows,
including the exact PSD Gram for the four three-edge even cuts and hostile
regressions against the former false simplex estimate:

```sh
python3 positive-square-energy/experiments/k4_all_odd_exact_verify.py
python3 -O positive-square-energy/experiments/k4_all_odd_exact_verify.py
```

Both runs report digest
`b0c4ed64a12ccabe0a8a38cb9fdb85622d8f7c2d07bdf53f75eb1700a684fa39`
and eight rejected hostile mutations.

The audits are corroborative; the paper proves the analytic and structural
reductions separately. A 9 November 2026 hostile re-audit found and repaired
two errors in the earlier `K4` write-up: a false regular-simplex estimate for
the three-even-cut row and an incorrect bipartiteness assertion in the
one-long-path deletion. The replacement physical Gram and
`Theta(1,2,2)` opening are exact and are now regression-tested. See
`HOSTILE_AUDIT.md` for the piece-by-piece review.

The doubled-triangle all-length residue split has a focused finite audit. It
checks the 32-row census, distinguishes long from canonical pairs in the
`(3,3)` residue class, and verifies the two long-path rational bounds:

```sh
python3 research/doubled-triangle-all-length-certificate.py
python3 -O research/doubled-triangle-all-length-certificate.py
python3 research/tricyclic-gram-obstruction-verifier.py
```

The first two runs report digest
`b293eef0d7742da6ecd2c7af35882be14e97811922493121900e65a6705f01e8`
and three rejected hostile mutations. They audit the all-length residue split;
the final command
audits the Gram obstruction used in the finite-certificate analysis. The
residue proof object is
`positive-square-energy/tricyclic-general/doubled-triangle-all-length-residue-cover.md`.

## Build

From the repository root:

```sh
bash scripts/build-paper.sh all-tricyclic-graphs
```

The build produces `all-tricyclic-graphs/paper.pdf`. The paper includes an AI
disclosure, a scoped nonclaim, and no publication step.
