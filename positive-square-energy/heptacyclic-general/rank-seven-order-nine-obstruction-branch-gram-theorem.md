# Order-nine obstruction frontier: exact all-descendant branch-Gram gate

## Scope and verdict

Consider the exact `1,615` order-nine parity rows left after the induced
rank-at-least-two territory transfer and removal of the three named persisted
Gram streams.  They represent `1,945` physical parity rows on `115` kernels.
Every row has fifteen physical paths and hence sixteen canonical-plus-coordinate
targets.

This note proves a **uniform all-descendant owner**, not merely another finite
target scan:

> **Theorem.** Every one of the `1,615` rows has a single positive-semidefinite
> unit-diagonal branch Gram whose exact eliminated-path excess is at most six at
> the canonical simple length vector.  Retaining that same branch Gram owns
> every coordinatewise same-parity length descendant, including all
> `1,615*16=25,840` canonical-plus-coordinate targets.  Arbitrary finite rooted
> trees may be attached at branch or subdivision vertices.

The exact gate has two disjoint modes.  A refined switched-three-ray
construction owns `1,614` rows (`1,944` physical rows).  Its sole residual is
owned by one explicit rational positive-definite `9 x 9` Gram.  Thus the
residual count after this gate is exactly zero.

This is a theorem for the authenticated order-nine obstruction frontier.  By
itself it does not authenticate the mathematical payloads of the three earlier
Gram streams, prove the separate induced-territory theorem, cover other kernel
orders, or close arbitrary multiblock rank-seven graphs beyond the stated
one-root tree attachments.

## Exact path atom and descendant stability

If a physical path has length `L` and its branch endpoint correlation is `r`,
alternating the path vectors changes the endpoint correlation to

```text
t=(-1)^L r.
```

The least DNN excess on that path is

```text
f_L(r)=L tan^2(acos(t)/(2L)).                                  (1)
```

An equal-angle great-circle chain attains (1); interiors of distinct paths may
be installed in mutually orthogonal auxiliary subspaces.  For fixed `t`, put
`beta=acos(t)` and `z=beta/(2L)`.  Differentiating in real `L>0` gives

```text
d/dL [L tan^2(beta/(2L))]
 = tan(z)/cos(z)^2 * (sin(z)cos(z)-2z).
```

This is nonpositive because `sin(z)cos(z)<=z<=2z`, and it is strict unless
`beta=0`.  Hence

```text
f_(L+2)(r) <= f_L(r).                                          (2)
```

Parity is unchanged by adding two, so `t` is unchanged.  Consequently one
branch Gram accepted at the canonical vector owns **all simultaneous**
same-parity coordinate lengthenings.  This is stronger than target-dependent
favorable-cycle partitions and is unaffected by their known simultaneous-
lengthening obstruction.

If the realized core has `M` edges, rank seven gives `|V|=M-6`.  A branch Gram
with total excess at most six gives `kappa<=M+6`.  The standard DNN inequality
`s^-<=kappa` and `s^++s^-=2M` then yield `s^+>=M-6=|V|`.
One-vertex additivity of `kappa` and the zero-excess bipartition Gram of a tree
preserve this conclusion under the stated rooted-tree attachments.

## Refined switched-three-ray owner

Take three equilateral unit rays `a_0,a_1,a_2`, with
`<a_i,a_j>=-1/2` for `i!=j`.  Assign each branch vertex one of the six states

```text
z_v=(-1)^s a_c,    c in {0,1,2}, s in {0,1}.                  (3)
```

The resulting branch matrix is automatically a PSD correlation matrix.  Its
entries belong to `{1,-1,1/2,-1/2}`.  At transformed correlation `1`, a path
has zero cost; transformed correlation `-1` is rejected.  The authenticated
frontier has raw odd total at most one in every bundle, so its canonical paths
have only lengths one and two.  The only remaining costs therefore have
`L in {1,2}` and transformed correlation `t in {1/2,-1/2}`.

The verifier uses integer charges on scale sixty:

| `L` | `t` | exact/upper charge `60 f_L` |
|---:|:---:|---:|
| 1 | `1/2` | `20` (exact) |
| 1 | `-1/2` | `180` (exact) |
| 2 | `1/2` | `<9` |
| 2 | `-1/2` | `40` (exact) |

Here is an exact proof of the sole strict bound.

### The length-two positive bound

Put `y=tan^2(pi/12)`.  Since `tan(pi/12)=2-sqrt(3)`, we have

```text
y=(2-sqrt(3))^2=7-4sqrt(3).
```

Consequently

```text
60 f_2(1/2)=120y<9
```

because `y<3/40`, equivalently `sqrt(3)>277/160`, whose square is the integer
inequality `76800>76729`.

Summing these rigorous per-path upper charges, the six-state weighted CSP
accepts a witness when its rigorous upper-charge total is at most `360`.  The
deterministic branch-and-bound solver fixes vertex zero to state `(0,0)`, uses exact local
lower bounds, returns an actual witness, and independently replays its total.
It owns exactly `1,614` frontier rows.  The accepted scaled charges range from
`218` through `360`.  Since every table entry is an upper bound on its exact
path cost, a total at most `360` proves exact excess at most six.  If a
charge-`360` witness uses the sole strict entry then its exact excess is
strictly below six; if not, its exact excess equals the charged value and is
six.

## Sole switched-three-ray residual and direct Gram

The unique CSP residual is

```text
[source index, global kernel, local kernel, odd-count row, orbit]
[2584311,11564,4078,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],1].
```

Its fifteen simple kernel edges are

```text
03, 07, 08, 12, 17, 18, 26, 28, 35, 38, 45, 46, 47, 56, 78.
```

The verifier embeds an exact rational symmetric matrix `G` with unit diagonal.
Rather than trusting a decimal eigenvalue, it recomputes the fraction-only
factorization

```text
G = L diag(d_1,...,d_9) L^T
```

and requires the following nine positive pivots:

```text
1,
429/529,
114527/247104,
18575533187/104690505024,
16893611/313686669,
22115545080139280247/466834327076602240000,
43723152036881631881605412/941583154002604943566179375,
240810798556848021/4635649647213071861,
177718468252360464231472/3277126971347347357191141.
```

Hence `G` is positive definite.  Every canonical path has length one, for which

```text
f_1(r)=(1+r)/(1-r).
```

Direct fraction arithmetic gives

```text
sum_(uv in E) (1+G_uv)/(1-G_uv)
 = 607593754/122731245 < 6.                                  (4)
```

By (2), the same `G` owns every same-parity descendant of this row.  The matrix
was found numerically and rationalized only as a proposal; the theorem trusts
solely the embedded rational entries, exact LDL replay, and exact inequality
(4).

## Fail-closed finite gate

Run from the repository root:

```text
python3 research/rank-seven-order-nine-obstruction-branch-gram-verifier.py
python3 -O research/rank-seven-order-nine-obstruction-branch-gram-verifier.py
```

The verifier uses only the Python standard library.  It:

1. SHA-256 authenticates the kernel fixture, the `272,520`-row compressed and
   raw source, and all three compressed and raw owner streams;
2. parses canonical JSONL, binds every stream owner to an exact source record,
   checks stream disjointness, reconstructs all order-nine kernels, and
   independently re-enumerates the induced-partition criterion;
3. regenerates exactly `1,615` obstruction rows, `1,945` physical rows, and
   `115` represented kernels rather than trusting a persisted frontier list;
4. runs and replays the exact six-state CSP, pins its complete deterministic
   witness-stream digest and exact cost histogram, and requires the sole
   residual key above;
5. parses the direct matrix as reduced rational pairs, recomputes and
   reconstructs its exact LDL factorization, and recomputes (4).

No `assert` is used, so optimized mode cannot disable a gate.  The verifier's
finite work establishes the authenticated frontier coverage.  The analytic
path formula, the elementary trigonometric inequality, PSD
interpretation of (3), fixed-parity monotonicity, and DNN spectral implication
are proved in this note rather than being silently attributed to the script.
