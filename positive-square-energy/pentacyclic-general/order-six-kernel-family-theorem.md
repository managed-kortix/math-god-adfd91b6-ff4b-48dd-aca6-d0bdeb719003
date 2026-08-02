# Complete order-six rank-five kernel-family theorem

## Theorem

Let `K` be any of the 38 order-six kernels in the exact rank-five suppressed
kernel classification. Let `B` be any simple subdivision of `K`, and obtain
`G` by attaching an arbitrary rooted tree at each vertex of `B`. Then

`s^+(G) >= |V(G)|`.

The proof is disjunctive. Most parity families have a DNN certificate with
excess at most four; the remaining kernel-71 targets have an induced-territory
structural proof. No DNN assertion is inferred from the structural cases.

## Exhaustive ledger

The source-locked census reconstructs the following sets rather than trusting
counts copied from the search output.

| set | exact count |
|:---|---:|
| order-six kernels | 38 |
| labeled physical parity rows | 23,208 |
| automorphism orbits | 12,810 |
| regular-tetrahedron certificates | 11,312 |
| residual orbits | 1,498 |
| canonical plus ten coordinate frontiers | 16,478 |

Every order-six rank-five kernel has ten suppressed paths. For each residual
row the finite frontier is its canonical shortest length vector together with
all ten vectors obtained by adding two to one path length. Fixed-parity path
monotonicity then covers every coordinatewise longer length vector.

The frontier has the disjoint certificate partition

| method | exact targets |
|:---|---:|
| strict rational stereographic path vectors | 16,451 |
| symbolic equality, K55 | 9 |
| symbolic equality, K61 | 9 |
| structural triangle plus attached `K4`, K71 | 9 |
| total | 16,478 |

The independent key audit derives the Cartesian target set directly from all
1,498 census residual keys and the frontier set `{canonical,0,...,9}`. It then
requires uniqueness and exact equality with the raw-result keys, so equal
counts cannot hide an omission/extraneous-key swap. Removing the 16,451 keys
having strict witnesses leaves exactly nine keys in each of K55, K61, and K71
and no others.

## Strict rational certificates

The raw result file stores all 16,451 strict witnesses. A witness gives five
rational stereographic parameters for each of six branch vectors and each
internal path vector. The verifier reconstructs every unit vector over
`Fraction`. For each transformed adjacent pair with correlation `r`, it
recomputes the exact step cost

`(1-r)/(1+r)`.

It reconstructs the ten physical paths from the kernel multiplicities, parity
row, and frontier coordinate; checks every internal-vector count and stored
path length; sums all exact step costs; requires equality with the stored
reduced fraction; and requires the result to be strictly less than four. Thus
floating-point `numerical_cost` fields have no proof role.

## K55 and K61 symbolic equalities

The 18 equality keys have the following exact shape.

| kernel | parity rows | frontiers per row | total |
|:---:|:---|:---|---:|
| K55 | three choices for the `03`/`12` zero-cost signs | canonical, 0, 3 | 9 |
| K61 | three choices for the `03`/`12` zero-cost signs | canonical, 0, 3 | 9 |

Each fixture record freezes a rational `6 x 6` endpoint Gram matrix. The
verifier checks symmetry, unit diagonal, and every principal minor, not merely
a claimed factorization. Every physical path is then checked separately:

| transformed endpoint correlation | path length | exact path cost |
|:---:|---:|---:|
| `1` | arbitrary listed zero-cost path | `0` |
| `1/2` | `1` | `1/3` |
| `-1/2` | `2` | `2/3` |

For a length-two path, the verifier also checks the PSD of the exact
three-vector Gram matrix with endpoint correlation `-1/2` and midpoint
correlations `1/2`. The ten verified path costs sum to exactly four in every
record. Lengthening frontier 0 or 3 does not alter the sum because that path's
transformed endpoints coincide. This establishes a genuine equality
certificate, rather than accepting the numerical optimizer's displayed `4.0`.

## K71 structural closures

Use pair order

`01,02,03,04,05,12,13,14,15,23,24,25,34,35,45`.

K71 has multiplicities

`(0,0,1,1,1,2,0,0,1,0,1,0,1,1,1)`.

Its nine structural keys are three parity rows, each at the canonical vector
and frontiers 5 and 6. Paths 5 and 6 are respectively the `15` and `24` paths;
lengthening either remains wholly on the deleted side. In every one of these
keys the six paths `03,04,05,34,35,45` are unit edges and induce the actual
`K4` on branch vertices `{0,3,4,5}`.

Delete branch vertices `1,2`, all internal vertices on paths `12^0,12^1,15,24`,
and every rooted tree owned at one of those vertices. The deleted core is a
triangle subdivision on the two `12` paths, with the `15` and `24` portions
attached as trees after endpoints 5 and 4 remain on the other side. It is an
induced connected favorable unicyclic territory. The complement is the induced
actual `K4` on `{0,3,4,5}`, with all rooted trees owned there attached. The
standard favorable-triangle and attached-`K4` packet inequalities, combined by
induced superadditivity, give the required spectral conclusion.

The graph audit does not accept this description as metadata. It reconstructs
every physical subdivision from the kernel and target key, computes induced
edge sets, checks the actual six-edge `K4`, connectedness and cyclomatic count
of the deleted territory, and reconstructs its triangle. It assigns every
branch/internal owner to exactly one side. It then materializes rooted trees of
varying depths, computes descendants from parent links, and checks that every
descendant stays with its unique owner, the partition is exhaustive and
disjoint, and the two induced core types survive. Since the argument uses only
the rooted-tree parent relation, replacing a materialized tree by any finite
rooted tree preserves the owner-exact proof.

For each of the three K71 rows, the canonical, frontier-5, and frontier-6 keys
are structural. The other eight one-coordinate frontiers are strict rational
certificates. Hence any monotone descendant uses the structural frontier when
only path 5 or 6 grows, and otherwise uses a strict rational coordinate
frontier. This avoids claiming that a subdivision of one of the six retained
edges remains an actual `K4`.

## Fail-closed audit

The frozen inputs are

| artifact | SHA-256 |
|:---|:---|
| rank-five kernel source | `027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884` |
| order-six tetra census | `de4278bd890c99fa6c06e62c1641eb2f0ce3a3d4603427d2b80d24c674bb9089` |
| raw rational experiment results | `6a46d2acebe60015c0071332f1152bb3da5c9b893e7fc22943a38162db37487e` |
| theorem fixture | `69b236b014aef58c037c610ca01fa62ad82601f7bb34153939ec4ddd3b5f364d` |

The raw census and experiment retain `full_theorem=false`; they are evidence
sources, not silently relabeled theorem files. The deterministic theorem
fixture records the exact 27 closures and source hashes. Its verifier freshly
reconstructs the fixture and complete key universe, checks all 16,478 proofs,
and rejects hostile changes to closure presence, uniqueness, counts, Gram
entries, costs, structural frontiers/openings, and source locks.

Run in both interpreter modes so checks cannot depend on `assert`:

```text
python3 pentacyclic/research/order6-kernel-family-theorem-verifier.py
python3 -O pentacyclic/research/order6-kernel-family-theorem-verifier.py
```
