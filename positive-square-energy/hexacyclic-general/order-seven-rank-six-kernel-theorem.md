# Complete order-seven rank-six kernel theorem

## Statement

For a graph `X`, let

`s^+(X)=sum_{lambda_i(X)>0} lambda_i(X)^2`

and define the cyclomatic rank of a connected graph to be
`|E(X)|-|V(X)|+1`. A rank-six suppressed kernel is a loopless,
2-connected multigraph of minimum degree at least three and cyclomatic rank
six.

**Theorem (order-seven rank-six kernel theorem).** Let `K` be any rank-six
suppressed kernel on seven vertices. Let `B` be any simple graph obtained by
replacing every edge of `K` by a positive-length path, with the replacement
paths internally vertex-disjoint. Obtain `G` from `B` by identifying the root
of an arbitrary finite rooted tree with each vertex of `B`; trivial trees are
allowed. Then

`s^+(G) >= |V(G)|`.                                           (1)

The rooted trees may have arbitrary shapes and may be attached at branch
vertices or internal subdivision vertices. The conclusion is non-strict.

This theorem concerns only the order-seven, one-nontrivial-block rank-six
class. In particular, it is **not** a theorem for all connected hexacyclic
graphs. The order-eight, order-nine, and order-ten rank-six single-block
kernels require their own closures before such a conclusion can be drawn.

## DNN reduction and path model

Use the DNN constant

`kappa(X)=min {sum_(uv in E(X)) 2/(1-C_uv) : C psd, C_vv=1}`. (2)

The LTZ/DNN estimate and the trace identity give

`s^-(X)<=kappa(X)`,  `s^+(X)+s^-(X)=2|E(X)|`.                 (3)

If a suppressed path has length `l` and its branch endpoint correlation is
`r`, exact path elimination gives the excess contribution

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                        (4)

Equivalently, after alternating the signs of consecutive path vectors, a
rational Gram chain with adjacent correlations `q_j` has exact excess

`sum_j (1-q_j)/(1+q_j)`.                                     (5)

For fixed `r` and fixed parity, `f_l(r)` is nonincreasing under
`l -> l+2`. This is the fixed-parity path monotonicity used below.

An order-seven rank-six kernel has

`|E(K)|=7+6-1=12`.                                           (6)

For each unordered pair of branch vertices, record the multiplicity `m` and
the number `o` of odd replacement paths. This is a physical parity row. Within
a parallel class its canonical simple length multiset is

`(1,3,...,3,2,...,2)` if `o>0`, and `(2,...,2)` if `o=0`,    (7)

with `o` odd entries and `m-o` even entries. Simplicity permits at most one
unit path in a parallel class, so every simple subdivision with that parity
row dominates this canonical vector after permuting equal kernel edges.

For a canonical vector `c`, take the 13-point frontier

`F(c)={c} union {c+2e_i : 0<=i<12}`.                         (8)

This frontier covers every length vector `l` of the same physical parity. If
`l=c`, use the canonical target. Otherwise choose a coordinate with
`l_i>=c_i+2`; then `c+2e_i<=l` coordinatewise, and repeated fixed-parity
monotonicity proves the certificate for `l`. This argument also covers
simultaneous lengthening of any number of other paths.

## Exact coarse census

The canonical rank-six fixture contains exactly 314 order-seven kernels,
K332--K645. The census enumerates every physical parity row, computes the full
kernel automorphism group from all `7!` branch permutations, and retains the
lexicographically least row in each orbit. It gives the exact ledger

| item | exact count |
|:---|---:|
| kernels | 314 |
| physical parity rows | 700,792 |
| automorphism orbits | 519,453 |
| coarse-certified orbits | 494,899 |
| coarse-residual orbits | 24,554 |

The coarse certificate assigns the branch vertices to at most four vectors
forming a regular tetrahedron. Equal colors have correlation one and distinct
colors have correlation `-1/3`. A row with an odd path inside one color class
is inadmissible. Costs are computed in integer units of `1/30`. For paths
joining different color classes, the first canonical odd path costs
15, each further odd path costs 5, and each even path costs 18; an even path
inside one color class costs zero. Thus the acceptance test is the exact
integer inequality

`coarse_cost_scaled <= 150=30*5`.                             (9)

No floating-point comparison enters this partition. Every coarse-certified
canonical target has excess at most five, and (4) covers all same-parity
lengthenings. The remaining 24,554 orbits produce

`24,554*13=319,202`                                          (10)

canonical and one-coordinate frontier keys.

## Complete exact frontier

The 319,202 residual-frontier keys are closed by the following disjoint exact
partition:

| method | exact keys |
|:---|---:|
| rational Gram-chain certificates | 319,163 |
| exact equality-template certificates | 39 |
| total | 319,202 |

The 319,163 rational certificates are stored in six contiguous chunks covering
source indices 0--24,553. For each accepted key the verifier reconstructs
seven rational unit branch vectors and every rational internal path vector,
checks the endpoint and length ledger, and sums (5) with `Fraction`. Acceptance
requires an exact total at most five. Floating-point optimization is used only
to propose vectors; stored numerical costs are ignored by the proof audit.

The six chunk counts are

| source indices | exact keys / all keys |
|:---|---:|
| 0--3,999 | 52,000 / 52,000 |
| 4,000--7,999 | 52,000 / 52,000 |
| 8,000--11,999 | 51,988 / 52,000 |
| 12,000--15,999 | 51,982 / 52,000 |
| 16,000--19,999 | 51,991 / 52,000 |
| 20,000--24,553 | 59,202 / 59,202 |

Their ordered digest-manifest SHA-256 is

`5a3693a15beb0a6c37089c5fe15f78eaf76875dcd3096b98a2fc3dbf0f339324`.

### The 39 exact equality targets

The remaining 39 keys are three frontier targets on each of 13 source rows:

| kernel | source rows | frontier labels | exact geometry | keys |
|:---:|:---|:---|:---|---:|
| K469 | 10370, 10372, 10427, 10429 | canonical, 0, 10 | tetrahedron plus apex | 12 |
| K511 | 14191, 14206, 14225 | canonical, 2, 5 | tetrahedron plus apex | 9 |
| K534 | 15904, 15908, 15927 | canonical, 0, 3 | signed five-cycle quotient | 9 |
| K548 | 16796, 16800, 16819 | canonical, 0, 3 | signed five-cycle quotient | 9 |

Thus “39 equality templates” means 39 target-indexed exact equality
certificates, arising from 13 source-row instances and two geometric template
families.

For K534 and K548, contract the signed singleton paths `03,12`. The five
remaining quotient classes form a signed five-cycle of mixed odd/even doubled
bundles. Put diagonal one and signed cycle-edge correlation `-1/2` on the
quotient Gram matrix. Switching reduces its positive-semidefiniteness to the
balanced or unbalanced five-cycle matrix. Each contraction costs zero, while
each mixed bundle costs

`1/3+2/3=1`;                                               (11)

hence the five bundles have total excess five.

For K469 and K511, use a regular tetrahedron with mutual correlations `-1/3`
and one apex. Two signed singleton contractions cost zero, six odd tetrahedron
edges cost `1/2` each, and two mixed doubled bundles cost one each. Therefore

`6*(1/2)+2*1=5`.                                             (12)

The verifier constructs every resulting rational `7 by 7` Gram matrix and
checks all 127 principal minors exactly. For each of the two distinguished
coordinate frontiers, adding two copies of the first alternating unit vector
adds two adjacent correlations equal to one and therefore zero cost. Repetition
also gives an explicit same-parity lengthening for these equality cases.

## Full-key coverage

The proof audit does not infer completeness from the displayed totals. It
derives the expected key set

`U={(j,a): 0<=j<24554, a in {canonical,0,...,11}}`            (13)

from the digest-locked census. It then checks all of the following:

1. the selected kernels are exactly K332--K645 from the locked rank-six
   fixture;
2. the physical rows, automorphism orbits, coarse partition, and ordered
   residual source rows have the exact counts above;
3. the six chunks cover every source index exactly once and have the locked
   SHA-256 digests and ordered manifest;
4. every rational record reconstructs and verifies over `Fraction`;
5. the null-witness set in the chunks is exactly the 39-key equality fixture;
6. every equality key has the census-derived kernel, physical row, path ledger,
   rational PSD Gram matrix, and exact cost five;
7. the union of the rational and equality key sets equals `U`, with no missing,
   duplicate, or out-of-scope key.

The normal equality-frontier audit reruns itself under `python3 -O` and requires
byte-identical output. Consequently Python assertions are not proof premises.
The census artifact and equality fixture retain `full_theorem=false` as a
fail-closed provenance guard; the theorem status is conferred only by the
separate complete verifier after it proves the full-key equality in item 7.

## Proof of the theorem

Fix `K`, `B`, and `G` as in the theorem. The exact census places the physical
parity row of `B` in one of the 519,453 automorphism orbits.

If the orbit is coarse-certified, its tetrahedral certificate and fixed-parity
monotonicity give

`kappa(B)<=|E(B)|+5`.                                        (14)

If it is coarse-residual, the length vector of `B` dominates one of the 13
frontier vectors in (8). Full-key coverage gives either an exact rational
certificate or one of the exact equality certificates for that frontier.
Monotonicity again yields (14). Thus (14) holds for every permitted `B`.

Write `L=|E(B)|`. Since `B` is connected of cyclomatic rank six,

`|V(B)|=L-5`.                                                (15)

Suppose the attached rooted trees contain `t` edges in total. One-vertex-sum
additivity of `kappa`, together with `kappa(T)=|E(T)|` for every tree, gives

`kappa(G)<=L+5+t`.                                           (16)

Also `|E(G)|=L+t` and `|V(G)|=L-5+t`. Equations (3) and (16) now give

`s^+(G) = 2|E(G)|-s^-(G)`
`         >= 2(L+t)-(L+5+t)`
`         = L-5+t`
`         = |V(G)|`,                                        (17)

which proves (1). `QED`

## Computer-assisted proof model

This is a finite, exact, computer-assisted theorem. Its trusted mathematical
interface consists of:

- exhaustive generation of the canonical rank-six kernel fixture;
- exhaustive finite iteration over physical rows, branch permutations, and
  restricted set-partition colorings;
- canonical ASCII JSON parsing and SHA-256 identity checks;
- integer arithmetic for the coarse sieve;
- rational arithmetic for unit vectors, Gram entries, path costs, and totals;
- exact determinants of rational principal submatrices for the equality Grams;
- deterministic set equality for complete key coverage.

Floating-point optimization and multiprocessing affect witness discovery and
runtime only. A numerical candidate has no theorem status unless exact rational
reconstruction succeeds. The proof does not assume that the optimizer found a
global minimum: it uses only verified feasible Gram chains of cost at most
five. SHA-256 is used to identify the audited finite artifacts, not as a
mathematical substitute for the arithmetic checks performed on their contents.

## Reproduction

From the repository root, run

```sh
python3 positive-square-energy/experiments/rank6_order7_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order7_orbit_frontier_census.json
python3 -O positive-square-energy/experiments/rank6_order7_orbit_frontier_census.py \
  --verify positive-square-energy/experiments/rank6_order7_orbit_frontier_census.json
python3 positive-square-energy/experiments/rank6_order7_batched_exact_gram.py \
  --audit positive-square-energy/experiments/rank6_order7_batched_chunks/*.json.xz
python3 research/rank-six-order-seven-equality-frontier-verifier.py
python3 -O research/rank-six-order-seven-equality-frontier-verifier.py
python3 research/rank-six-order2-7-master-verifier.py
python3 -O research/rank-six-order2-7-master-verifier.py
```

The batched audit must report

```text
chunks=6 records=24554 targets=319202 exact=319163 unresolved=39
complete_frontier=true
```

and the equality audit must report

```text
batched_exact=319163 equality_exact=39 frontier_targets=319202
theorem_status=PROVED
```

The fail-closed master then authenticates the exact rank-six census and the
theorem owners for orders two through seven. It runs every dependency in the
same interpreter mode, rejects omitted or scope-widened dependencies, and in
normal mode reruns its complete audit under `python3 -O`, requiring
byte-identical output. Its conclusion is limited to the 645 selected
single-block kernel families; it explicitly makes no claim for orders eight
through ten or for all connected hexacyclic graphs.

## Dependency map

```text
rank-six-kernels.json
  -> exact order-seven selection K332--K645 (314 kernels)
  -> rank6_order7_orbit_frontier_census.py
       -> physical rows and automorphism orbits
       -> exact tetrahedral coarse sieve
       -> 24,554 ordered residual rows
       -> 319,202-key canonical-plus-coordinate universe U

U + exact path elimination + fixed-parity monotonicity
  -> rank6_order7_batched_exact_gram.py
       -> six digest-locked chunks
       -> 319,163 exact rational keys
       -> exact 39-key null-witness set

39-key null-witness set
  -> rank-six-order-seven-equality-frontier.json
  -> rank-six-order-seven-equality-frontier-verifier.py
       -> K469/K511 tetrahedron-plus-apex Grams
       -> K534/K548 signed-five-cycle Grams
       -> 39 exact cost-five keys

319,163 rational keys + 39 equality keys
  -> exact set equality with U
  -> DNN excess-five bound for every residual parity family

494,899 coarse orbits + all residual parity families
  -> DNN excess-five bound for every simple subdivision of every
     order-seven rank-six kernel

DNN bound + one-vertex-sum tree additivity + trace identity
  -> s^+(G) >= |V(G)| for the theorem class

exact rank-six census + theorem owners for orders 2--7
  -> rank-six-order2-7-master-verifier.py
       -> exact 1+4+26+84+216+314 = 645 kernel partition
       -> fail-closed normal/python -O implication audit
       -> no order-8--10 or all-hexacyclic promotion

NOT INCLUDED
  -> order-eight, order-nine, or order-ten rank-six single-block closure
  -> all connected hexacyclic graphs
```

The principal source files are:

- `research/fixtures/rank-six-kernels.json`;
- `positive-square-energy/experiments/rank6_order7_orbit_frontier_census.py`;
- `positive-square-energy/experiments/rank6_order7_orbit_frontier_census.json`;
- `positive-square-energy/experiments/rank6_order7_batched_exact_gram.py`;
- `positive-square-energy/experiments/rank6_order7_batched_chunks/`;
- `research/fixtures/rank-six-order-seven-equality-frontier.json`;
- `research/rank-six-order-seven-equality-frontier-verifier.py`;
- `research/rank-six-order2-7-master-verifier.py`.
