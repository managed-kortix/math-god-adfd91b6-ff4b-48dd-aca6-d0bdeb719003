# Kernel 16: exact three-color certificate on all physical rows

## Theorem

Let `H` be any simple subdivision of kernel 16 in the rank-four kernel list,
and attach arbitrary rooted trees at arbitrary vertices of `H`. Then

`kappa(H) <= |E(H)|+3`

and consequently `s^+(H)>=|V(H)|`; the same conclusion holds after the tree
attachments.

Kernel 16 has canonical upper triangle

`(0,0,1,1,1,0,1,1,1,1,1,1,0,0,0)`

in the pair order `01,02,03,04,05,12,13,14,15,23,24,25,34,35,45`. Thus it
is the simple cubic graph `K_3,3`, with parts `{0,1,2}` and `{3,4,5}` and edge
order

`03,04,05,13,14,15,23,24,25`.

## Physical rows: exactly `2^9`

Write `l_e>=1` for the length of the subdivided path replacing edge `e`, and
write `q_e=1` when `l_e` is odd and `q_e=0` when it is even. Since every
kernel edge is simple, its physical state is just this parity bit. Therefore
the complete physical state space is

`q in {0,1}^9`,

of cardinality `2^9=512`.

The proposed alphabet `D/O/E` and count `3^9=19683` distinguish an odd direct
path (`D`, length one) from an odd long path (`O`, length at least three). That
distinction is unnecessary for an upper-bound certificate. For endpoint
correlation `r`, exact path elimination gives

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.

For fixed `r` and fixed parity, `f_l(r)` decreases under `l -> l+2`. Hence every
odd path is majorized by canonical length one and every even path by canonical
length two. The canonical odd state does not assert that the physical path is
direct; it is only the worst term for every odd physical length. There is no
structural reason to retain `O` for a simple kernel edge. Thus `512`, not
`19683`, is the exact exhaustive physical-row count for this proof.

## Equilateral three-color construction

Fix three unit vectors at mutual angle `120` degrees. Their Gram matrix has
diagonal `1`, off-diagonal `-1/2`, and is positive semidefinite (its eigenvalues
are `3/2,3/2,0`). Assign one of these vectors, called a color, to each of the
six branch vertices.

For a path whose endpoints have the same color, the correlation is `1`; for
different colors it is `-1/2`. The canonical path costs are

| endpoint colors | odd path | even path |
|:---|---:|---:|
| same | infinite | `0` |
| different | `1/3` | `2/3` |

Consequently a coloring is admissible exactly when every odd edge of `q` is
bichromatic. If `q=sum_e q_e` and `b` is the number of even edges made
bichromatic, the canonical excess is

`q/3+2b/3=(q+2b)/3`.

It is therefore enough to prove, for every one of the 512 rows, that some
three-coloring satisfies all odd-edge constraints and has integer score

`S(q)=q+2b <= 9`.                                             (1)

The odd-edge graph is a subgraph of `K_3,3`, so it is bipartite and always has
an admissible coloring. Inequality (1), including the restriction on the even
edges, is the finite assertion audited exhaustively below.

## Exact exhaustive census

The verifier independently enumerates all `2^9` parity rows and, for each row,
all `3^6=729` maps from branch vertices to the three labeled colors. It rejects
a map if any odd edge is monochromatic, computes `q+2b` with integer arithmetic,
and retains the minimum. The complete minimum-score histogram is

| minimum `S` | rows |
|---:|---:|
| 0 | 1 |
| 3 | 6 |
| 4 | 27 |
| 5 | 63 |
| 6 | 147 |
| 7 | 168 |
| 8 | 81 |
| 9 | 19 |
| total | 512 |

In particular every physical row satisfies (1), and 19 rows attain the
certificate boundary. Quotienting only by genuine automorphisms of `K_3,3`,
namely `(S_3 x S_3) semidirect C_2` of order 72, gives 26 row orbits. This orbit
count is diagnostic only: the proof checks all 512 labeled physical rows and
does not use switching or transport a certificate between distinct rows.

The finer labeled census by `(q,S)` is

`(0,0):1; (1,5):9; (2,4):18; (2,6):18;`

`(3,3):6; (3,5):36; (3,7):42;`

`(4,4):9; (4,6):81; (4,8):36;`

`(5,5):18; (5,7):108; (6,6):48; (6,8):36;`

`(7,7):18; (7,9):18; (8,8):9; (9,9):1`.

These counts total 512 and reproduce the displayed score histogram.

## DNN and spectral conclusion

For the coloring selected for a row, summing the canonical contributions gives

`kappa(H)-|E(H)| <= S(q)/3 <= 3`.

`kappa(H) <= |E(H)|+3`.                                      (2)

Kernel 16 has cyclomatic rank four, so every subdivision satisfies
`|V(H)|=|E(H)|-3`. The LTZ/DNN inequality and the trace identity give

`s^+(H)=2|E(H)|-s^-(H) >= 2|E(H)|-kappa(H)`

`>=|E(H)|-3=|V(H)|`.

For rooted trees attached by one-vertex sums, `kappa(T)=|E(T)|` and DNN
constants add. Adding `t` tree edges to (2) therefore preserves the same
calculation and proves `s^+>=|V|` for all asserted attachments.

## Fail-closed audit

Run

```text
python research/rank-four-kernel16-three-color-verifier.py
python -O research/rank-four-kernel16-three-color-verifier.py
```

The verifier uses only the Python standard library. It regenerates kernel 16
from its canonical code, all 512 rows, all coloring minima, the 26 automorphism
orbits, the score and `(q,S)` ledgers, and a deterministic SHA-256 digest of all
rows with their first minimizing witnesses. It uses explicit `require` checks,
not `assert`, and includes hostile mutations of the row count, score ledger,
digest, and row alphabet. Any missing row, accidental `3^9` policy, changed
cost, malformed state, or altered witness census terminates with an error.

The executable census proves only the finite combinatorial inequality (1).
The path-elimination formula, fixed-parity monotonicity, equilateral Gram
matrix, LTZ/DNN inequality, and one-vertex-sum rule are the mathematical inputs
stated above; they are not replaced by floating-point computation.
