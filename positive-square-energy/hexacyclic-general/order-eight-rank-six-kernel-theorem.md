# Complete order-eight rank-six kernel theorem

## Statement and boundary

For a graph `X`, put

`s^+(X)=sum_{lambda_i(X)>0} lambda_i(X)^2`.

**Theorem.** Let `K` be any loopless 2-connected rank-six multigraph on eight
vertices with minimum degree at least three. Replace its thirteen edges by
positive-length, internally disjoint paths so that the resulting graph `B` is
simple. At every branch or subdivision vertex, identify the root of an
arbitrary finite rooted tree; call the resulting graph `G`. Then

`s^+(G) >= |V(G)|`.

This is exactly the order-eight, one-nontrivial-block rank-six theorem. It makes
no assertion about order-nine or order-ten kernels, multiblock rank-six graphs,
or all connected hexacyclic graphs.

## DNN reduction

Use

`kappa(X)=min {sum_(uv in E(X)) 2/(1-C_uv): C psd, C_vv=1}`.

The LTZ/DNN inequality and the trace identity give

`s^-(X)<=kappa(X)`,  `s^+(X)+s^-(X)=2|E(X)|`.                 (1)

After alternating signs along a path, a rational unit-vector chain with
successive correlations `q_j` has exact excess

`sum_j (1-q_j)/(1+q_j)`.                                     (2)

Equivalently, eliminating a length-`l` path with branch correlation `r` gives

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                        (3)

For fixed `r` and parity, `f_l(r)` is nonincreasing under `l -> l+2`. The
finite certificate below proves

`kappa(B) <= |E(B)|+5`                                       (4)

for every permitted subdivision `B`.

## Exact census

The digest-locked rank-six fixture contains exactly 325 order-eight kernels,
K646--K970. Since each has thirteen edges,
`sum_v(deg(v)-3)=2`; the degree types and counts are

| degree multiset | kernels | simple kernels |
|:--|--:|--:|
| `5,3,3,3,3,3,3,3` | 55 | 6 |
| `4,4,3,3,3,3,3,3` | 270 | 27 |
| total | 325 | 33 |

For each support of multiplicity `m`, record the number `o` of odd physical
paths. The exhaustive census enumerates all `0<=o<=m`, computes the full kernel
automorphism group, and retains one canonical physical row per orbit. Its exact
ledger is

| item | exact count |
|:--|--:|
| physical parity rows | 1,598,512 |
| automorphism orbits | 1,045,292 |
| tetrahedrally certified orbits | 942,304 |
| residual orbits | 102,988 |

The tetrahedral sieve is integer-only, in units of `1/30`, and accepts exactly
when its cost is at most `150=30*5`. No floating-point decision enters this
partition.

The canonical census JSON has SHA-256

`724fdb337b7bb9225b1a8691c28e131ae1c8de7dc38bb13a5adbb98c1f92218e`.

Its ordered stream digests are

```text
kernel                 37646f53c89bd904c7e04c687ce90e52be3aea414810499e749ce95493aab0ea
orbit manifest         40ce2900c0e2f9887d46f9bf1dfe4eb21ad8b0cc1c4e71179a56d49b34220b3e
residual               b451837e04a30e5b71eba5fe631841eee73bbb8f3722a0b6bd25b666ad4fe900
frontier keys          52439257eaa2b5a6bc2976f5c4199a5a06e3e3b6ab8afc61b2ad7c734876e97d
```

## Complete v2 manifest and finite target universe

For a physical parity row, simplicity gives the canonical lengths

```text
(1,3,...,3,2,...,2) if at least one path is odd,
(2,...,2)           if every path is even,
```

with at most one unit path in each parallel class. If `c` is the resulting
thirteen-coordinate vector, define

`F(c)={c} union {c+2e_i: 0<=i<13}`.                          (5)

The 102,988 residual rows therefore have exactly

`102,988*14=1,441,832`                                       (6)

canonical-plus-coordinate targets. The complete v2 manifest consists of 17
ordered, contiguous XZ chunks covering the half-open source range
`[0,102988)`. It pins compressed and raw byte counts and SHA-256 digests,
transitive source digests, and the covered key stream. Its SHA-256 is

`dd97ff3059cd637177171cb5d335cc17889a3714459522232e8110c5d79da469`.

The manifest's covered-key-stream digest is

`bf608536f7645ca5ad4eef586fb72cbddf90a4f243a00b954635eb6f5ec27794`.

The exact auditor rejects gaps, overlaps, path escapes, malformed XZ, changed
compressed or raw bytes, trailing binary data, source-range disagreement,
malformed rational vectors, incomplete path ledgers, nonunit vectors, endpoint
disagreement, nonpositive step denominators, costs above five, duplicate keys,
and any unresolved key outside the independently derived symbolic set. A stored
JSON result digest authenticates bytes only: because there is no signature from
an independently trusted verifier, anyone can fabricate a matching result and
hash. It is a reproducibility receipt, not independent exact proof.

It reconstructs all arithmetic with `Fraction`. The exact ownership partition
is

| owner | targets |
|:--|--:|
| rational Gram-chain records | 1,441,808 |
| symbolic exact-cost-five records | 24 |
| total | 1,441,832 |

The 24 symbolic targets are not inferred from a numerical null count. The
symbolic recognizer independently derives its signed-five-cycle and
tetrahedron-plus-apex rows from the kernel fixture, constructs rational Gram
matrices, checks every principal minor, verifies every physical path and
contraction, and computes exact cost five. Its larger dictionary has 256
cost-five target keys; 232 happen also to receive rational records. The theorem
partition uses only the 24 keys left unresolved by the rational chunks, and the
auditor proves exact set equality with no unexpected null.

The symbolic fixture SHA-256 is

`2f457374d9627bd27339a0988aa47149db825dd0cba050c71ac9accfa3f72b95`.

Both the census and symbolic fixtures retain `full_theorem=false`. They are
fail-closed ingredients; only the master verifier promotes their exact union
with the rational chunks after checking complete target ownership.

## Arbitrary same-parity lengthening

Let `l` be any simple subdivision length vector in the parity orbit represented
by `c`. After permuting equal kernel edges, `c<=l` coordinatewise and every
difference is even. If `l=c`, use the canonical target. Otherwise choose any
coordinate `i` with `l_i>=c_i+2`; then

`c+2e_i <= l` coordinatewise.                                (7)

The target `c+2e_i` is among the 14 audited targets. Repeated fixed-parity
monotonicity in every coordinate carries that certificate to `l`. Thus (5)
covers arbitrary simultaneous lengthening of any subset of paths, not merely
one-coordinate subdivisions. Coarse-owned rows use their canonical
tetrahedral Gram directly, since the same monotonicity applies in every
coordinate.

This implication needs no assertion that an equality Gram remains an equality
Gram after every lengthening. A noncanonical vector chooses one audited
coordinate frontier, and monotonicity handles all remaining increases.

## Rooted-tree lift and proof

Fix a permitted `B` and write `L=|E(B)|`. The census places its parity row in
exactly one orbit. A coarse orbit has an exact tetrahedral certificate. For a
residual orbit, complete target ownership and the preceding all-length argument
give an exact rational or symbolic certificate. Hence (4) holds in all cases.

Because `B` is connected of cyclomatic rank six,

`|V(B)|=L-5`.                                                 (8)

Suppose the attached rooted trees contain `t` edges in total. One-vertex-sum
additivity of `kappa` and `kappa(T)=|E(T)|` for every tree give

`kappa(G)<=kappa(B)+t<=L+5+t`.                               (9)

Also `|E(G)|=L+t` and `|V(G)|=L-5+t`. Applying (1),

```text
s^+(G) >= 2(L+t)-(L+5+t)
       = L-5+t
       = |V(G)|.
```

This includes arbitrary tree shapes rooted at branch vertices or internal
subdivision vertices. It proves the stated theorem. `QED`

## Trusted base and reproduction

The proof trusts deterministic finite enumeration, canonical ASCII JSON and
binary parsing, SHA-256 for artifact identity, XZ decompression, integer and
exact rational arithmetic, exact determinant tests, and the mathematical DNN,
path-monotonicity, and one-vertex-sum lemmas. Floating-point optimization is
only a witness-discovery mechanism; stored decimal scores are not read by the
theorem verifier.

From the repository root, the exact reproduction commands are

```sh
python3 positive-square-energy/experiments/rank6_order8_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order8_orbit_frontier_census.json
python3 -O positive-square-energy/experiments/rank6_order8_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order8_orbit_frontier_census.json
python3 positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py
python3 -O positive-square-energy/experiments/rank6_order8_symbolic_recognizers.py
python3 positive-square-energy/experiments/rank6_order8_pack_auditor.py
python3 -O positive-square-energy/experiments/rank6_order8_pack_auditor.py
python3 research/rank-six-order-eight-kernel-theorem-verifier.py --full
python3 -O research/rank-six-order-eight-kernel-theorem-verifier.py --full
```

The master accepts only `--full` and performs the complete pack audit itself; it
does not promote a stored transcript to proof. All proof premises use exceptions
rather than `assert`. The normal and optimized commands are separate complete
replays. The master also rejects hostile registry mutations: each omitted
dependency, an altered manifest digest, a widened scope, and a weakened
conclusion.

For practical independent checking, replay the 17 chunks separately. Each
command regenerates the complete residual census and symbolic fixture, verifies
the global manifest and key-stream commitment, decodes one pinned chunk, and
recomputes every exact rational cost in that chunk:

```sh
mkdir -p /tmp/order8-audit
python3 positive-square-energy/experiments/rank6_order8_pack_auditor.py \
  --chunk-index 0 --write-chunk-transcript /tmp/order8-audit/chunk-00.json
# Repeat indices 1 through 16, independently and in any order.
python3 positive-square-energy/experiments/rank6_order8_pack_auditor.py \
  --aggregate-transcripts /tmp/order8-audit/chunk-*.json \
  --write-aggregate /tmp/order8-audit/aggregate.json
```

The aggregate is fail-closed bookkeeping: it requires exactly one transcript
for every manifest chunk and exact global coverage, but it cannot prove that an
untrusted party actually ran those replays. A stranger obtains independent
exact proof only by running all 17 chunk commands (possibly across machines),
or by running the master with `--full`. No theorem claim is made from merely
authenticating the aggregate or the legacy whole-run transcript.

The principal pinned leaf digests are

```text
rank-six-kernels.json                    5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476
rank6_order8_orbit_frontier_census.json 724fdb337b7bb9225b1a8691c28e131ae1c8de7dc38bb13a5adbb98c1f92218e
rank6_order8_search_manifest.json        dd97ff3059cd637177171cb5d335cc17889a3714459522232e8110c5d79da469
rank6_order8_symbolic_templates.json     2f457374d9627bd27339a0988aa47149db825dd0cba050c71ac9accfa3f72b95
```

The master prints the canonical exact-dependency-manifest SHA-256 after the
audit. That root authenticates this order-eight theorem only; it is not a root
for a broader hexacyclic theorem.
