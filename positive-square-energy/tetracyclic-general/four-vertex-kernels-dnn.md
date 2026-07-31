# Four-vertex rank-four kernels: exact ledger and unresolved residual

## Proposed theorem and current status

Let `B` be a simple subdivision of one of the five four-vertex kernels

`(0,1,2,1,2,1)`, `(0,1,2,2,1,1)`, `(0,1,2,2,2,0)`,
`(0,1,2,3,1,0)`, or `(1,1,1,1,1,2)`,

in edge order `01,02,03,12,13,23`. Attach arbitrary rooted trees at arbitrary
vertices. Then the resulting graph `G` satisfies

`s^+(G)>=|V(G)|`.

The computations below do **not** yet prove this statement. They certify 340
of the 342 physical parity rows. The last two rows reduce exactly to a stronger
all-odd `K4` statement that is not supplied by the existing all-odd `K4`
theorem. Thus the four-branch-vertex part of the rank-four block classification
remains open at these two rows.

## The physical ledger

For kernel multiplicities `m`, let `q_e` be the number of physically odd paths
in bundle `e`. Thus `0<=q_e<=m_e`. Direct Cartesian enumeration gives

| kernel | rows |
|:---|---:|
| `(0,1,2,1,2,1)` | `72` |
| `(0,1,2,2,1,1)` | `72` |
| `(0,1,2,2,2,0)` | `54` |
| `(0,1,2,3,1,0)` | `48` |
| `(1,1,1,1,1,2)` | `96` |
| total | `342` |

The old switching-orbit packet directly certifies 270 physical rows after its
Gram matrices are transported back to the original physical costs. The exact
row patch certifies 70 more rows. It consists of 42 rational planar
automorphism-orbit certificates and one exact boundary matrix; each is checked
against the physical row, never against a switched parity row. The largest
patched excess is at most three.

Exactly two rows remain unresolved:

`(kernel 4, q=(1,1,1,1,1,1))`,

`(kernel 4, q=(1,1,1,1,1,2))`.

They are not outputs of the planar row search and must not be counted as
certified rows.

## Exact structural reduction

Write the last kernel as a `K4` support with a second `23` path. In both
residual rows all five singleton bundles are odd. Choose an odd `23` path for
the `K4` support and let `T` be the internal vertices of the other `23` path,
together with every rooted tree based at those vertices. The other path has an
internal vertex: in row `111111` it is even and hence has length at least two;
in row `111112` both paths are odd, but simplicity permits at most one direct
`23` edge, so one of them has odd length at least three and is chosen as the
deleted path.

The induced graph `T` is a nonempty tree, so `sigma(T)=-1`. Its induced
complement is an all-odd subdivision of `K4`, with all remaining rooted-tree
attachments retained. Induced superadditivity therefore gives exactly

`sigma(G) >= sigma(K4_all_odd_packet) + sigma(T)`

`          = sigma(K4_all_odd_packet) - 1`.

Consequently both residual rows would close if one proved the strengthened
attached all-odd `K4` estimate

`sigma(K4_all_odd_packet) >= 1`.                         (required)

The presently recorded all-odd `K4` result proves only `sigma>=0`, so it cannot
pay for the deleted tree. This reduction is exact, but it is not a discharge.

The standalone verifier also regenerates the full monotone long/unit ledger for
that all-odd support. Of the `2^6=64` subsets of long paths, the exact classes
are

| class | subsets | disposition |
|:---|---:|:---|
| at least three long | `42` | regular-simplex DNN |
| two long, adjacent | `12` | planar DNN |
| two long, opposite | `3` | planar DNN |
| exactly one long | `6` | induced `Theta(1,2,2)` deletion |
| no long path | `1` | actual attached `K4` packet |

For the regular-simplex DNN class it encodes four certificates, according as
the number `q` of long paths is `3,4,5,6`. The simplex has exact off-diagonal
correlation `-1/3`; every unit path costs `1/2`, and the triple-angle identity
gives the strict rational long-path bound `1/6`. Thus the four exact upper
bounds are respectively

`2, 5/3, 4/3, 1`.

The verifier derives these values rather than trusting displayed decimals and
checks all principal Gram minors over `Fraction`. The monotonicity step is only
within a fixed odd parity: every long all-odd path has length at least three,
and increasing its length cannot increase the path cost. The zero-long class
is kept separate because it is the actual `K4`, not another DNN row. Its
required attached-packet margin `sigma>=1` remains an explicit unresolved
proof artifact.

The earlier simplex discharge was invalid. For the quarter-angle convention
used by the verifier,

`r=(1-6t^2+t^4)/(1+t^2)^2`.

Thus regular-simplex correlation `r=-1/3` gives `t^2=2-sqrt(3)`, not `1/3`;
indeed `t^2=1/3` gives `r=-1/2`. The claimed costs `1/3` and `2/3`, and hence
the budgets `8/3` and `7/3`, do not follow from a regular-simplex Gram matrix.

## Fail-closed audit

`research/rank-four-four-vertex-theorem-verifier.py` imports the original base
audit and the exact row patch, independently reconstructs all 342 physical
rows, and checks the disjoint status ledger

`342 = 270 base + 70 patch + 2 unresolved`.

For each unresolved row it checks the parity predicate, the existence of the
nonempty induced deleted tree, the all-odd `K4` complement, and the missing
requirement `sigma>=1`. It also verifies the four rational simplex bounds,
enumerates all 64 monotone classes, identifies the structural actual-`K4`
branch, and rejects the false `t^2=1/3` simplex record. The residual records
must contain no purported Gram matrix or numerical excess. Hostile mutations
of coverage, status, predicates, bounds, or the required margin are rejected.
Run

```text
python research/rank-four-four-vertex-theorem-verifier.py
python -O research/rank-four-four-vertex-theorem-verifier.py
```

Both commands must exit nonzero with the same unresolved blocker. Python
`assert` is not used for any acceptance condition. A zero exit would be a false
theorem acceptance.
