# The seven non-all-odd switching classes of subdivided `K4`

This note gives a complete all-length DNN certificate for the seven switching
classes other than the all-odd class. The important point is that switching is
used only to name a class and to design a Gram matrix. The certificate is then
transported back to the **same physical parity row**, and fixed-parity path
monotonicity is applied there. No path of length one is ever replaced by a path
of length two merely because a parity switch toggles its bit.

## 1. Exact path reduction and the target

Let the branch vertices be `1,2,3,4`, and put the six branch paths in the order

`12,13,14,23,24,34`.

Write `p_ij=1` when the physical length `l_ij` is odd and `p_ij=0` when it is
even. Let `L=sum l_ij`. The subdivision has `L` edges and `L-2` vertices.

For unit branch vectors with correlation `r_ij`, exact path elimination gives
the excess over the `l_ij`-edge baseline as

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                       (1)

Hence any branch correlation matrix `R` with

`sum_(ij) f_(l_ij)(R_ij) <= 2`                              (2)

proves `kappa<=L+2`. The DNN spectral inequality then gives

`s^+ = 2L-s^- >= 2L-kappa >= L-2`.

For fixed endpoint correlation and fixed parity,

`f_(l+2)(r) <= f_l(r)`,                                     (3)

with equality only at the degenerate zero-angle boundary. Thus it is enough,
for each physical parity row, to check its physical canonical lengths

`lambda_ij = 1 if p_ij=1, and 2 if p_ij=0`.                 (4)

There are no parallel kernel edges in `K4`, so every one of the `2^6=64`
canonical rows is a simple subdivision.

Arbitrary rooted trees are included at the end by one-vertex additivity of
`kappa` and `kappa(T)=|E(T)|`.

## 2. Normalization, invariants, and the length warning

Choose switching bits `s_4=0` and

`s_i = 1-p_i4` for i=1,2,3.                                (5)

The normalized parity is

`p'_ij = p_ij xor s_i xor s_j`.                             (6)

Equation (5) makes all three normalized paths to vertex `4` odd. For the
remaining triangle define

`epsilon_ij = 1-p'_ij`, for ij in {12,13,23}.                (7)

Thus `epsilon_ij=1` means that the normalized triangle path `ij` is even.
The three epsilon bits are complete switching invariants: switching has four
bits modulo the global switch, so each of the eight epsilon words has exactly
`2^3=8` physical rows. The word `000` is the all-odd class. The other seven
words are the classes proved here.

The vectors below are first specified in the normalized signs. If `q_i` is a
normalized planar angle, define the physical vector angle by

`theta_i = q_i + pi s_i`.                                   (8)

Then

`cos(theta_i-theta_j)=(-1)^(s_i+s_j) cos(q_i-q_j)`.          (9)

This is the valid sign-switch transport of a correlation matrix. In (1), the
transformed endpoint correlation for the **physical** path is

`(-1)^p_ij cos(theta_i-theta_j)
 = (-1)^p'_ij cos(q_i-q_j)`.                                (10)

So its transformed endpoint angle is the normalized one. However, its
coefficient and denominator in (1) remain the physical `lambda_ij` from (4),
not the normalized canonical length. This distinction is exactly what prevents
false switching transport of path lengths.

## 3. The three planar templates

Angles are given modulo `2pi`, always with `q_4=0`. Permuting vertices
`1,2,3` permutes the epsilon bits and gives every word of the same weight.

### One normalized even triangle edge: weight one

For `epsilon=001`, so `23` is normalized even, take

`(q_1,q_2,q_3,q_4)=(2pi/3,4pi/3,4pi/3,0)`.                 (11)

At the normalized canonical lengths (odd paths of length one and the one even
path of length two), the six costs are five copies of `1/3` and one zero:

`C_norm(001)=5/3`.                                          (12)

Indeed, every nonzero transformed angle is `pi/3`; a canonical odd path costs
`tan^2(pi/6)=1/3`, while the even edge `23` has transformed angle zero.

### Two normalized even triangle edges: weight two

For `epsilon=011`, so `13,23` are normalized even, take

`(q_1,q_2,q_3,q_4)=(2pi/3,4pi/3,pi,0)`.                    (13)

The normalized canonical costs are three copies of `1/3`, two copies of

`2 tan^2(pi/12)=14-8sqrt(3)`,

and one zero. Therefore

`C_norm(011)=1+2(14-8sqrt(3))
            =29-16sqrt(3)<5/3<2`.                           (14)

The inequality `29-16sqrt(3)<5/3` is equivalent to
`sqrt(3)>41/24`, true after squaring because `1728>1681`.

### All three normalized triangle edges even: weight three

For `epsilon=111`, take

`(q_1,q_2,q_3,q_4)=(pi,pi,pi,0)`.                           (15)

Every normalized transformed endpoint angle is zero, so

`C_norm(111)=0`.                                            (16)

Equations (11)--(16), together with permutations of `1,2,3`, are the requested
normalized planar table. The next section proves that these templates certify
all 56 physical rows without pretending that their normalized lengths are
physical lengths.

## 4. Direct physical-row theorem

Put

`a = 2 tan^2(pi/12)=14-8sqrt(3)`, and `b=1/3`.              (17)

For either template (11) or (13), and for any switching bits in (5), direct
use of (8)--(10) shows that every physical canonical path has one of only four
types:

| physical parity | transformed angle | physical canonical cost |
|---|---:|---:|
| even | `0` | `0` |
| even | `pi/3` | `a` |
| odd | `0` | `0` |
| odd | `pi/3` | `b` |

This table is a substitution into (1) with physical length two or one. It is
not a switched-length calculation.

For each nonzero epsilon word there are eight physical rows, indexed by the
actual switch triple `(s_1,s_2,s_3)`. A direct count in either the weight-one
or weight-two template gives exactly the following multiset of total physical
canonical costs:

| number of rows | number of `a` terms | number of `b` terms | total cost |
|---:|---:|---:|---:|
| 1 | 0 | 5 | `5/3` |
| 2 | 2 | 3 | `2a+1` |
| 4 | 3 | 2 | `3a+2/3` |
| 1 | 4 | 1 | `4a+1/3` |

Here is the complete eight-switch audit for each representative template. An
entry such as `2a+3b` records the six physical path costs, including the one
zero-cost path.

| `(s_1,s_2,s_3)` | cost for `001` | cost for `011` |
|---:|---:|---:|
| `000` | `5b` | `2a+3b` |
| `001` | `2a+3b` | `5b` |
| `010` | `2a+3b` | `3a+2b` |
| `011` | `4a+b` | `3a+2b` |
| `100` | `3a+2b` | `3a+2b` |
| `101` | `3a+2b` | `3a+2b` |
| `110` | `3a+2b` | `2a+3b` |
| `111` | `3a+2b` | `4a+b` |

This table follows by six substitutions per row in the four-type physical
table above. Equivalently, on each of the five nonzero-angle edges, the XOR in
(6) decides whether its physical canonical cost is `a` or `b`; the sixth edge
costs zero for either physical parity. Permuting vertices `1,2,3` merely
permutes the switch columns, so this audits all three weight-one and all three
weight-two epsilon words. In either case the number of `a` terms has
distribution `0,2,3,4` with multiplicities `1,2,4,1`, proving the preceding
census.

All four totals are at most `5/3`. First,

`a=14-8sqrt(3)<1/6`,                                        (18)

because `sqrt(3)>83/48`, and `3*48^2=6912>6889=83^2`.
Consequently

`2a+1<4/3`, `3a+2/3<7/6`, and `4a+1/3<1`,                  (19)

while the first row is exactly `5/3`. Thus every physical row in any epsilon
class of weight one or two has canonical physical excess at most `5/3<2`.

For epsilon `111`, (15) and (8)--(10) make every transformed endpoint angle
zero for every one of its eight physical rows. Their physical canonical costs
are all zero. We have therefore proved directly:

> **Physical-row certificate theorem.** For each of the 56 parity rows with
> `epsilon != 000`, the physical canonical lengths (4) admit a planar Gram
> matrix whose exact path excess is at most `5/3`.

This is also a complete physical census: seven epsilon classes, eight actual
switch triples per class, with all eight costs accounted for by the table. It
uses switching only through the physical vector sign changes (8), which do not
alter any path length.

## 5. All lengths and rooted-tree attachments

Fix any physical parity row with `epsilon != 000` and use its physical vectors
from (8). By (3), replacing any canonical physical length `lambda_ij` by an
arbitrary longer length of the same physical parity cannot increase its path
cost. Hence for every realization of that row,

`kappa-L <= sum_(ij) f_(l_ij)(R_ij)
          <= sum_(ij) f_(lambda_ij)(R_ij)
          <= 5/3 < 2`.                                      (20)

Therefore `kappa<L+2` and `s^+>L-2` for the bare subdivision.

Now attach arbitrary rooted trees at arbitrary core vertices. One-vertex
additivity adds exactly one to `kappa` for each tree edge. Adding a rooted tree
with `t` edges also adds `t` vertices, so (20) retains the same strict margin
from the threshold. Thus every such attached subdivision in the seven
non-all-odd switching classes satisfies

`s^+(G)>|V(G)|`.

The omitted epsilon word `000` is precisely the all-odd switching class and is
not claimed here.
