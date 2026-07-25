# Exact shared-cut `{3,3,5,5}` core census and `Phi` audit

## Outcome

The connected shared-cut census has **20**, not 21, quotient-isomorphism
types. Two independent quotients agree: exact NetworkX graph isomorphism and a
canonical cycle-block code that permits both permutations of equal-length
blocks, every cyclic rotation, and every reflection. The older tetracyclic
search independently reports the same count with `--shared-only`.

For each type the script computes, over `ZZ` in 13 independent vertex
activities,

`Phi=2R(p+q)-I(pq-4)`.

Here `R+iI` is the full Sachs sum for all vertex-disjoint subsets of the four
cycles, with triangle multiplier `-2i` and pentagon multiplier `+2i`; `p,q`
are the isolated weighted pentagon matching partitions. Exactly one type is
coefficientwise positive. The other 19 have negative coefficients. Thus this
particular two-pentagon comparison is not a universal coefficient-positive
main proof object for the `{3,3,5,5}` shared cluster.

## Exhaustion and exact arithmetic

The generator starts with one cycle and recursively attaches each remaining
cycle as a leaf block at every existing vertex, over all six permutations of
the multiset. This exhausts connected block-cut trees, including several block
joins coinciding at one cut vertex. Every generated graph has 13 vertices and
16 edges. Graph-isomorphic duplicates are discarded exactly.

For an induced vertex set `S`, the custom sparse recurrence is

`Z(S)=a_v Z(S-v)+sum_(vw in E[S]) Z(S-{v,w}),  Z(empty)=1`,

where `v` is the least remaining vertex. Polynomials are sparse integer maps.
Each exponent occupies a two-bit field, so polynomial multiplication is exact
integer key addition without symbolic parsing or floating point arithmetic.

## Classification

Cycles in the canonical output are ordered `T0,T1,P2,P3`. An incidence string
such as `012+23` says that one cut vertex lies on `T0,T1,P2` and another lies
on `P2,P3`. Repeated incidence strings can represent different cyclic
distances on a middle pentagon.

| type | incidence | terms | min | negative terms | result |
|---:|:---|---:|---:|---:|:---|
| 1 | `0123` | 7506 | -8 | 21 | fail |
| 2 | `012+03` | 7551 | -8 | 21 | fail |
| 3 | `012+23` | 8592 | -4 | 6 | fail |
| 4 | `012+23` | 8543 | -8 | 11 | fail |
| 5 | `023+01` | 9027 | -8 | 21 | fail |
| 6 | `01+02+03` | 7808 | 2 | 0 | **pass** |
| 7 | `01+02+13` | 7776 | -8 | 21 | fail |
| 8 | `01+02+23` | 9777 | -4 | 6 | fail |
| 9 | `01+02+23` | 9749 | -8 | 11 | fail |
| 10 | `023+12` | 12858 | -14 | 155 | fail |
| 11 | `02+03+12` | 12599 | -16 | 141 | fail |
| 12 | `02+12+23` | 14675 | -32 | 172 | fail |
| 13 | `02+12+23` | 14294 | -20 | 178 | fail |
| 14 | `023+12` | 11524 | -14 | 114 | fail |
| 15 | `02+03+12` | 11290 | -16 | 102 | fail |
| 16 | `02+12+23` | 13248 | -32 | 100 | fail |
| 17 | `02+12+23` | 12904 | -20 | 109 | fail |
| 18 | `02+13+23` | 14598 | -16 | 154 | fail |
| 19 | `02+13+23` | 14453 | -16 | 166 | fail |
| 20 | `02+13+23` | 13867 | -16 | 161 | fail |

Type 6 consists of two triangles meeting at one triangle vertex while the two
pentagons meet the other two distinct vertices of that same triangle. It has
7808 nonzero terms, all positive, with coefficient range 2 through 64. Its
canonical core and polynomial hashes are

`core 054f0a3274a40ddc90320b5168b7ea332ad9be7b643d4a18bd3efeed1feb54b6`

`Phi bba25a704998e3d8a77700e9b4ae8d903e919999bcb16b790dc29c07f7733f01`.

The failure classes separate naturally. Types 1--9 have intersecting
triangles and only 6--21 negative terms (minimum -4 or -8). Types 10--20 have
disjoint triangles and 100--178 negative terms (minimum down to -32). The
coefficient failure does not by itself prove that `Phi` takes a negative value
on the positive orthant; it proves that coefficient positivity cannot certify
these 19 cases.

## Reproduction and hashes

Run

```text
python positive-square-energy/experiments/c3_c3_c5_c5_shared_cluster_certificate.py
```

The script validates the expected count, every exact failure profile, and the
aggregate SHA-256 of the ordered `(core hash, Phi hash)` ledger:

`5de126495a983d5014f4339a88830cedc8ec053d89680a23e9663736485d71d5`.

At creation, the script file SHA-256 was

`3743ce87267c27543dcd2bf0ad6792e64ca59d493638a585393711c4ee73fbd5`.

The full per-type canonical cycles and hashes are printed by the driver rather
than duplicated here. `python -m py_compile` also passes.
