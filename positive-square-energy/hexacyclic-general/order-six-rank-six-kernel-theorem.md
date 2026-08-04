# Complete order-six rank-six kernel theorem

## Theorem

Let `K` be any of the 216 order-six kernels in the exact rank-six suppressed
kernel classification. Let `B` be any simple subdivision of `K`, and obtain
`G` by attaching an arbitrary finite rooted tree at every vertex of `B`. Then

`s^+(G) >= |V(G)|`.

The proof combines 31,235 exact rational DNN targets, twelve exact equality
targets on K253, K300, and K302, and one owner-exact structural opening on
K223. The structural target is not asserted to have DNN excess at most five.

## Exact census and frontier

The digest-locked census selects exactly K116--K331 from the canonical
rank-six kernel fixture. These are the 216 order-six kernels, each with eleven
suppressed paths. Exhausting all physical parity rows and quotienting by the
exact automorphism group gives the following ledger.

| item | exact count |
|:---|---:|
| physical parity rows | 207,358 |
| automorphism orbits | 150,734 |
| regular-tetrahedron coarse certificates | 148,130 |
| coarse residual orbits | 2,604 |

For every residual orbit, take its canonical shortest physical length vector
and the eleven vectors obtained by adding two to one path length. This gives

`2604 * 12 = 31,248`

frontier targets. Their disjoint exact closure is

| method | targets |
|:---|---:|
| rational stereographic Gram witnesses of cost at most five | 31,235 |
| K253 equality templates | 4 |
| K300 equality templates | 4 |
| K302 equality templates | 4 |
| K223 structural opening | 1 |
| total | 31,248 |

The verifier reconstructs the complete Cartesian key set, rather than trusting
the totals. It also checks that the three source chunks cover residual indices
0--2603 exactly once and that every stored source index agrees with its census
kernel and physical row.

## Equality templates

The twelve nonrational DNN targets are the canonical and one distinguished
frontier for each of the following six physical rows:

| kernel | row | frontiers |
|:---:|:---|:---|
| K253 | `001001011011011` | `c,2` |
| K253 | `001101011011011` | `c,2` |
| K300 | `000010010111111` | `c,0` |
| K300 | `100010010111111` | `c,0` |
| K302 | `000010010101100` | `c,0` |
| K302 | `100010010101100` | `c,0` |

For each row the verifier contains a rational positive-semidefinite unit-diagonal
Gram matrix. It checks every principal minor over `Fraction` and realizes every
path exactly. Unit odd paths at endpoint correlation `-1/3` cost `1/2`;
odd/even doubled bundles at correlation `-1/2` cost `1/3+2/3=1`;
and the distinguished path has transformed endpoint correlation one and hence
cost zero. Every template totals exactly five.

This zero-cost property is why one template closes both listed targets and all
further same-parity lengthenings of the distinguished path. For any other
noncanonical length vector, choose a different coordinate that was lengthened.
Its one-coordinate rational frontier is at most five, and fixed-parity path
monotonicity covers the actual vector, including simultaneous lengthening of
the distinguished coordinate. Thus no unsupported assertion that a general
equality Gram remains valid under arbitrary coordinate changes is used.

## K223 structural target

The sole remaining target is the canonical all-unit row

`K223: 001111011011111`.

Its eleven edges are

`03,04,05,12,14,15,24,25,34,35,45`.

The vertices `{0,3,4,5}` induce an actual `K4`. Put vertices `{1,2}`, their
edge, and every rooted tree owned there into the other induced part. This is a
nonempty tree territory; all attachments follow their unique owner. The two
parts are disjoint and exhaustive, while the four crossing edges are harmless
for induced square-energy superadditivity. The attached actual `K4` has credit
strictly greater than two and the nonempty tree has credit `-1`, so the total
credit is strictly positive.

If any K223 path is longer than its canonical unit length, choose one such
coordinate. All eleven one-coordinate frontiers have exact rational DNN cost at
most five, and monotonicity closes every coordinatewise same-parity descendant.
Consequently the structural argument is needed only for the actual all-unit
core, but it remains uniform over arbitrary rooted-tree attachments.

## All lengths and attachments

The census covers every physical parity orbit. For ordinary rational targets,
the canonical vector or a one-coordinate frontier is coordinatewise below the
given same-parity length vector. The equality and K223 exceptions are handled
as described above. Hence every simple subdivision of every one of the 216
kernels is covered.

If the subdivision has `L` edges, then it has `L-5` vertices. A DNN excess-five
certificate gives `kappa(B)<=L+5`. Attaching rooted trees with `t` total edges
adds exactly `t` to the DNN bound by one-vertex-sum additivity, and

`2(L+t)-(L+5+t)=L-5+t=|V(G)|`.

The K223 opening instead proves positive credit directly. Both routes are
uniform in the number, shape, and placement of the rooted trees.

## Exact audit

Run either mode; the normal invocation also launches `python -O` and requires
byte-identical output:

```text
python3 research/rank-six-order-six-kernel-theorem-verifier.py
python3 -O research/rank-six-order-six-kernel-theorem-verifier.py
```

The verifier digest-locks the theorem fixture, canonical kernel source, coarse
census, and all three rational-result chunks. It audits all 31,235 rational
witnesses independently with exact `Fraction` arithmetic; checks the exact
13-key nonrational residual; verifies every equality Gram, midpoint, path cost,
and total; verifies the K223 induced partition; checks the complete key set,
frontiers, lengths, and source coverage; and rejects hostile mutations of the
scope, counts, source ranges and digests, equality rows, and structural data.

This promotes the former experimental frontier to a complete order-six theorem.
No broader master theorem is changed by this note.
