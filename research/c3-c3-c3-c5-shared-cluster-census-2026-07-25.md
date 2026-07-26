# Exact shared-cut `{3,3,3,5}` core census and `Phi` audit

## Outcome

There are exactly **11** connected shared-cut core types with cycle multiset
`{3,3,3,5}`, up to graph isomorphism. This agrees with the independent
shared-only tetracyclic search. For every type, exact sparse integer arithmetic
computes

`Phi=2R-Z5 I`.

Here `R+iI` is the full weighted Sachs sum of the core, with multiplier `-2i`
for each triangle and `+2i` for the pentagon, and `Z5` is the matching
partition of the isolated pentagon in the same five vertex activities. The
identity

`Phi=Im((Z5+2i) conjugate(R+iI))`

is the desired comparison with the pentagon phase.

Only **3 of the 11** types have coefficientwise-positive `Phi` in independent
activities. The other **8** contain negative coefficients. Substituting every
activity as `a_v=t+y_v` does not repair any failed type: exactly the same three
types pass and the same eight fail. Thus coefficient positivity does not give
a uniform `C333q` base at `q=5`, so there is no all-positive base from which to
seek the proposed recurrence extension in `q`.

## Exhaustion and exact computation

The generator starts with one cycle and recursively attaches each remaining
cycle as a leaf block at every existing vertex, over all four distinct orders
of the multiset. It quotients by exact NetworkX graph isomorphism. A second
canonical code independently allows all permutations of the three triangles,
all cycle rotations, and all cycle reflections; both quotients return 11.
Every core has 11 vertices and 14 edges.

For an induced vertex set `S`, matching partitions use

`Z(S)=a_v Z(S-v)+sum_(vw in E[S]) Z(S-{v,w}),  Z(empty)=1`.

Polynomials are sparse maps over `ZZ`. The independent audit treats the 11
activities as separate variables. The shifted audit then expands the exact
same polynomial after `a_v=t+y_v`, retaining `t,y_0,...,y_10` independently.

## Classification

Canonical cycles are ordered `T0,T1,T2,P3`. An incidence string such as
`013+23` records one cut vertex on `T0,T1,P3` and another on `T2,P3`.
Repeated strings distinguish different cyclic distances on the pentagon.
Columns give `(number of nonzero terms, minimum coefficient, number of
negative terms)`.

| type | incidence | independent `a` | after `a=t+y` | result |
|---:|:---|:---|:---|:---|
| 1 | `0123` | `(372, 2, 0)` | `(18159, 2, 0)` | pass |
| 2 | `012+03` | `(380, 2, 0)` | `(15301, 2, 0)` | pass |
| 3 | `013+02` | `(584, -2, 3)` | `(18231, -2, 3)` | fail |
| 4 | `01+02+03` | `(640, 2, 0)` | `(16858, 2, 0)` | pass |
| 5 | `01+02+13` | `(591, -2, 3)` | `(17062, -2, 3)` | fail |
| 6 | `013+23`, distance 1 | `(787, -10, 7)` | `(21103, -10, 7)` | fail |
| 7 | `013+23`, distance 2 | `(677, -10, 4)` | `(20555, -10, 4)` | fail |
| 8 | `01+03+23`, distance 1 | `(852, -10, 8)` | `(19905, -10, 8)` | fail |
| 9 | `01+03+23`, distance 2 | `(789, -10, 6)` | `(19560, -10, 6)` | fail |
| 10 | `03+13+23`, positions `0,1,2` | `(1207, -12, 29)` | `(23011, -86, 32)` | fail |
| 11 | `03+13+23`, positions `0,1,3` | `(1036, -10, 21)` | `(22326, -56, 24)` | fail |

The three passing geometries are: the four-cycle bouquet; three triangles
sharing one vertex with the pentagon attached at a different vertex of one
triangle; and one central triangle whose three distinct vertices carry the
other two triangles and the pentagon. All coefficients in these cases are at
least 2 before and after substitution.

The failures become more numerous when the triangles are spread through the
core. Types 10 and 11 have three vertex-disjoint triangles attached at three
pentagon positions and are the strongest coefficient failures. A negative
coefficient is only a failure of this certificate; it does not imply that
`Phi` is negative anywhere on the positive activity orthant.

## Reproduction

Run

```text
python positive-square-energy/experiments/c3_c3_c3_c5_shared_cluster_certificate.py
```

The script asserts the core count, all 22 exact coefficient profiles, and the
aggregate SHA-256 of the ordered core and polynomial ledger:

`f7f39c81aa13443259ca5a644acfeb639041bc44ff393145a3a031520bac4c03`.
