# Three-vertex rank-four kernels: a uniform DNN certificate

## Theorem

Let `K` be a simple subdivision of a loopless multigraph on three vertices
whose three edge multiplicities are either `(1,2,3)` or `(2,2,2)`. Let `G` be
obtained from `K` by attaching arbitrary rooted trees at arbitrary vertices.
Then

`kappa(K) <= |E(K)|+3`

and consequently

`s^+(G) >= |V(G)|`.

The two multiplicity triples in the statement are exactly the rank-four,
minimum-degree-at-least-three triples; the finite tables below are asserted
only for those two triples.

## 1. Exact path reduction

Write the three branch vertices as `0,1,2`. For a branch path `P` of length
`l` between a pair `ij`, and an endpoint correlation `r_ij`, put

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                         (1)

The correlation dual and exact path elimination give

`kappa(K)-L = min_R sum_P f_|P|(r_end(P)),`                    (2)

where `L=|E(K)|` and the minimum is over the three-by-three correlation
matrices

`R=[[1,r_01,r_02],[r_01,1,r_12],[r_02,r_12,1]]`.              (3)

For fixed parity and fixed `r`, `f_l(r)` decreases when `l` is replaced by
`l+2`. Hence an odd path is bounded by its length-one contribution and an even
path by its length-two contribution:

`f_l(r) <= f_1(r)=(1+r)/(1-r)` for odd `l`,

`f_l(r) <= f_2(r)=2 tan^2(acos(r)/4)` for even `l`.             (4)

These canonical bounds may use length one simultaneously on parallel paths.
That does not assert the existence of a nonsimple canonical graph: it only
majorizes the separate path terms of the given simple subdivision. Thus no
special odd--odd physical base row is needed.

## 2. Rational three-correlation certificates

For `0<=t<=1` set

`r(t)=(1-6t^2+t^4)/(1+t^2)^2`.                                (5)

This is `cos(4 atan t)`, and direct multiple-angle identities give

`f_2(r(t))=2t^2`,

`f_1(r(t))=((1-t^2)/(2t))^2` for `t>0`.                       (6)

For a triple `t=(t_01,t_02,t_12)`, let `R(t)` denote (3) with
`r_ij=r(t_ij)`. By (6), if bundle `ij` has multiplicity `m_ij` and contains
`q_ij` physically odd paths, its canonical contribution is exactly

`(m_ij-q_ij)2t_ij^2+q_ij((1-t_ij^2)/(2t_ij))^2`,               (7)

with the second term omitted when `q_ij=0`. Thus all entries and all displayed
excesses below are rational. The nonnegative determinant in the last column,
together with `|r(t_ij)|<=1`, proves that each `R(t)` is a correlation matrix.

Let `q=q_01+q_02+q_12`. All rows with `q>=3` have the one common certificate

`R=[[1,-1/2,-1/2],[-1/2,1,-1/2],[-1/2,-1/2,1]]`.              (8)

This matrix is positive semidefinite, with determinant zero. At correlation
`-1/2`, (4) gives canonical odd cost `1/3` and canonical even cost `2/3`.
Consequently

`kappa(K)-L <= q/3+2(6-q)/3=4-q/3<=3`.                        (9)

It remains only to certify `q=0,1,2`. For multiplicities `(1,2,3)`, in the
displayed bundle order, the complete list is:

| `(q_01,q_02,q_12)` | `(t_01,t_02,t_12)` | exact excess | `det R(t)` |
|---|---|---:|---:|
| `(0,0,0)` | `(0,0,0)` | `0` | `0` |
| `(1,0,0)` | `(1/2,1/4,1/4)` | `19/16` | `6634496/52200625` |
| `(0,1,0)` | `(1/2,1/2,0)` | `25/16` | `0` |
| `(0,0,1)` | `(1/4,1/4,1/2)` | `31/16` | `6634496/52200625` |
| `(1,1,0)` | `(2/3,2/3,0)` | `89/72` | `0` |
| `(1,0,1)` | `(3/4,1/4,1/2)` | `1093/576` | `5328239616/32625390625` |
| `(0,2,0)` | `(1/2,3/4,1/4)` | `301/288` | `5328239616/32625390625` |
| `(0,1,1)` | `(0,1/2,1/2)` | `21/8` | `0` |
| `(0,0,2)` | `(1/3,1/3,2/3)` | `137/72` | `4230144/17850625` |

Every listed excess is strictly below three. These nine rows are exhaustive:
the number of odd paths in the bundles is bounded respectively by `1,2,3`,
and all triples of total at most two appear in the table.

For multiplicities `(2,2,2)`, bundle permutations reduce the rows of total at
most two to the following four types:

| `(q_01,q_02,q_12)` up to permutation | `(t_01,t_02,t_12)` | exact excess | `det R(t)` |
|---|---|---:|---:|
| `(0,0,0)` | `(0,0,0)` | `0` | `0` |
| `(1,0,0)` | `(1/2,1/4,1/4)` | `25/16` | `6634496/52200625` |
| `(2,0,0)` | `(3/4,1/3,1/3)` | `305/288` | `0` |
| `(1,1,0)` | `(1/2,1/2,0)` | `17/8` | `0` |

Permuting the three coordinates of both `q` and `t` supplies the certificate
for every labelled row. Again every excess is strictly below three.

This is a complete physical classification without switching: the physical
type is the bounded integer triple `(q_01,q_02,q_12)`. Equations (8)--(9)
handle every type of total at least three, and the two rational tables handle
all types of smaller total. Fixed-parity monotonicity then extends each row
from its canonical path costs to every actual path length.

## 3. Spectral conclusion and trees

For either multiplicity triple there are six suppressed edges and three branch
vertices, so its cyclomatic rank is `6-3+1=4`. A subdivision with `L` edges
therefore has

`|V(K)|=L-3`.                                                  (10)

The LTZ/DNN inequality `s^-(K)<=kappa(K)`, together with
`s^+(K)+s^-(K)=2L`, now yields

`s^+(K) >= 2L-(L+3)=L-3=|V(K)|`.                              (11)

If rooted trees with `t` total edges are attached at single vertices, the
one-vertex-sum rule for the DNN constant and `kappa(T)=|E(T)|` give

`kappa(G)<=kappa(K)+t <= L+3+t`.                              (12)

Also `|E(G)|=L+t` and `|V(G)|=L-3+t`. Repeating (11) proves
`s^+(G)>=|V(G)|`. Arbitrary subdivisions and arbitrary attached trees are
therefore included.

## 4. Residual status

There is no DNN residual for the three-branch-vertex rank-four kernels with
multiplicities `(1,2,3)` or `(2,2,2)`. The rational certificates above cover
every physical parity row and every path length. The only rows that can attain
the displayed upper bound three are those with exactly three physically odd
paths under the common certificate (8); the low-odd tables are strict. This is
an equality possibility for the certificate, not a claim that the optimized
DNN excess or the spectral inequality is sharp there.
