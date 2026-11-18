# Checked certificate package for the rooted `m=8`, `k=4` simultaneous-source projection

## Scope and verdict

This package proves one **conditional finite lemma** only:

> Under the frozen rooted order-18 `m=8`, `k=4` normal-form consequences
> encoded below, the common 16-vertex `T` projection is infeasible for the
> only possible exact predecessor-union sizes `|P|=6` and `|P|=7`.

It does **not** prove the upstream normal-form reduction, all `m=8` cases,
order 18 in general, or Seymour's second-neighborhood conjecture.

The retained package consists of 45 independently checked LRAT leaves:

| logical package | split | leaves | compressed bytes |
|---|---|---:|---:|
| `P=6` | source-2 inaccessible-pair orbits | 17 | 58,140,108 |
| `P=7` | 11 source-2 orbits directly; the hard `{1,3}` orbit split on source 3 | 28 | 230,672,140 |

Each logical package is strictly below the repository convention of
250,000,000 compressed bytes. Together they contain 288,812,248 bytes.

## Mathematical projection

The labels are

```text
v=0, r=1, A'={2,...,8}, K={9,...,14}, b0=15.
```

The encoding requires:

1. exact trichotomy (forward arc, reverse arc, or hole) on every pair;
2. exactly four holes;
3. exact `T`-outdegrees `8,9,8^7,6^6,7`;
4. `N_T^+(v)={r} union A'`;
5. every `K union {b0}` column has an `A'` predecessor;
6. `P` is exactly the predecessor union of the six `K` columns;
7. for every source in `P`, one pair of vertices is selected which is outside
   its closed outrow and is not reachable from it by a two-walk in `T`.

A short outsider-saturation argument leaves only `|P|=6,7`: if
`x in A'\P`, then `x` has no outarc to `K` and cannot point to `v`; its only
possible eight `T`-outneighbors are `r`, the other six members of `A'`, and
`b0`. Its exact outdegree is eight, so it dominates all eight. Two outsiders
would therefore form a digon. Hence `|A'\P|<=1`.

The clauses are a necessary projection of a frozen-cell counterexample, not a
biconditional characterization of one. Checked UNSAT therefore eliminates only
that conditional cell.

## Exact exhaustive split

For `P=6`, the stabilizer of source 2 is

```text
S(P\{2}) x S(K), with 0,1,8,15 fixed.
```

Its 17 pair orbits have sizes

```text
1,5,1,6,1,5,1,6,1,10,5,30,5,6,1,15,6
```

and sum to all `C(15,2)=105` possible source-2 selector pairs.

For `P=7`, the source-2 stabilizer is

```text
S(P\{2}) x S(K), with 0,1,15 fixed.
```

It has 12 orbits, of sizes

```text
1,6,6,1,6,6,1,15,36,6,15,6.
```

Eleven orbit representatives have direct checked proofs. The remaining orbit
has representative pair `{1,3}` (selector index 14). Fixing it, its stabilizer
on source 3 is

```text
S(P\{2,3}) x S(K), with 0,1,2,3,15 fixed.
```

The resulting 17 source-3 pair orbits have sizes

```text
1,1,5,6,1,1,5,6,1,5,6,1,10,30,5,15,6
```

and again sum to all 105 pairs. `k4_simsrc_split.py` materializes every finite
permutation, every orbit, and rejects overlap, omissions, or changed
representatives. The symmetry is semantic: all fixed clauses and variable
families are invariant under the stated color-class permutations.

## Files

```text
experiments/k4_simsrc_cnf.py
    deterministic producer; no repository SAT helper or historical generator

experiments/check_k4_simsrc_cnf.py
    producer-independent reconstruction of the entire variable order and
    clause sequence; explicit selector-guard audit; exhaustive small-width
    counter-semantics audit

experiments/k4_simsrc_split.py
    exact finite permutation/orbit cover checker

experiments/k4-simsrc-certificates.tsv
    frozen tool metadata and all 45 CNF/raw-LRAT/compressed-artifact identities

experiments/verify_k4_simsrc_certificates.py
    fail-closed identity, cover, regeneration, structural, decompression, and
    LRAT replay verifier

experiments/test_k4_simsrc_package.py
    nine deterministic hostile mutations, each required to be rejected

certificates/k4-simsrc-*.lrat.xz
    45 retained compressed LRAT proofs
```

The generator, structural checker, and split checker SHA-256 identities are
frozen in the ledger and enforced by the verifier. Every CNF, raw LRAT, and
compressed artifact has a row-specific byte count and SHA-256 there.

## Pinned tools and proof boundary

Proof producer:

```text
CaDiCaL 1.7.3
source commit 38e073b389a877b0a0d3c91136d2443ab95fdeba
command: cadical --lrat --no-binary -q CNF LRAT
required exit: 20
```

Solver status is not an acceptance boundary. Every proof must pass:

```text
lrat-check from drat-trim commit 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
lrat-check.c SHA-256 bf07c2ac96b9035da1ebcc578cb95e956a2b795629d613154cdb307f8a8f4a95
binary bytes 22064
binary SHA-256 e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8
required exit: 0
required output: exactly one literal line `c VERIFIED`
```

## Clean replay

Build the pinned checker, then run from `experiments/`:

```sh
git clone https://github.com/marijnheule/drat-trim.git /tmp/drat-trim
git -C /tmp/drat-trim checkout 2e3b2dc0ecf938addbd779d42877b6ed69d9a985
cc -O2 -o /tmp/drat-trim/lrat-check /tmp/drat-trim/lrat-check.c
sha256sum /tmp/drat-trim/lrat-check /tmp/drat-trim/lrat-check.c

python3 k4_simsrc_split.py
python3 verify_k4_simsrc_certificates.py \
  --checker /tmp/drat-trim/lrat-check --identity-only
python3 test_k4_simsrc_package.py /tmp/drat-trim/lrat-check
python3 verify_k4_simsrc_certificates.py \
  --checker /tmp/drat-trim/lrat-check
```

The full verifier deterministically regenerates every leaf CNF and variable
map, runs the independent structural checker, checks the generated CNF
identity, checks both compressed and streaming-decompressed LRAT identities,
and invokes `lrat-check` on all 45 leaves.

## Hostile checks

`test_k4_simsrc_package.py` requires rejection of all nine mutations:

1. remove an endpoint-outside-source-row literal;
2. remove an endpoint-to-source guard literal;
3. remove a two-walk exclusion guard literal;
4. remove an exact-`P` negative literal;
5. remove one split representative;
6. remove one ledger row;
7. mutate one artifact hash;
8. mutate the checker binary;
9. bind a valid proof to the wrong deterministic branch CNF.

## Checked development replay

In the producing environment, the final run reported:

```text
PASS hostile-mutations=9
PASS full-replay rows=45 p6_xz_bytes=58140108 p7_xz_bytes=230672140
```

The full 45-leaf replay took 95 seconds. This timing is informational; the
identities and independently checked LRATs are the evidence.
