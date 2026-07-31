# The doubled-triangle kernel: complete physical parity cover

## Theorem

Let `K` be a simple subdivision of the multigraph obtained from a triangle by
doubling two adjacent sides, and let `G` be obtained from `K` by attaching
arbitrary rooted trees at its vertices. Then

`s^+(G) >= |V(G)|`.

The complete physical-parity census and its exact certificates are recorded
below. No switching operation is used to transport a certificate.

## 1. Exact DNN reduction

Let the branch vertices be `0,1,2`. Write the five internally disjoint branch
paths as

`a,A : 0--1`, `b,B : 0--2`, and `c : 1--2`,

and use the same letters for their positive integer lengths. Put
`L=a+A+b+B+c`. Simplicity says that neither doubled pair can have both lengths
one. The core has `L-2` vertices and `L` edges.

For a correlation matrix `R` on the three branch vertices put

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                         (1)

For any graph `X`, write

`kappa(X)=sup_{M psd, M>=0} 4(sum_{uv in E(X)}sqrt(M_uv))^2/<J,M>`.

The correlation dual is

`kappa(X)=min_{R psd, diag R=1} sum_{uv in E(X)} 2/(1-R_uv)`.

Applying it to `K`, followed by exact path elimination, gives

`kappa(K)-L = min_R [f_a(R01)+f_A(R01)+f_b(R02)
                      +f_B(R02)+f_c(R12)].`                   (2)

Indeed, alternately negate the Gram vectors along a path of length `l`. If its
endpoint correlation is `r`, the transformed endpoint angle is
`acos((-1)^l r)`. The spherical triangle inequality and convexity make the
equal planar subdivision of that angle optimal, proving (1)--(2).

For fixed `r`, `f_l(r)` strictly decreases when `l` is replaced by `l+2`.
Writing `h_s(x)=s tan^2(x/s)` and `z=x/s`, this follows from

`d h_s/ds = tan(z)(tan(z)-2z sec^2(z)) < 0`,

because `sin(z)cos(z)<z<2z` for `0<z<pi/2`.

Thus a fixed parity row is hardest at length one on an odd path and length two
on an even path, except where simplicity excludes that canonical row.
Consequently, any displayed certificate at lengths `1,2` proves every longer
row with the same parities.

Since `s^-(K)<=kappa(K)` and `s^+(K)+s^-(K)=2L`, the core target follows whenever

`kappa(K)-L <= 2`.                                             (3)

If the attached trees contain `t` edges in total, one-vertex additivity of
`kappa` and `kappa(T)=|E(T)|` give `kappa(G)<=L+2+t`. Since
`|E(G)|=L+t` and `|V(G)|=L-2+t`, the same calculation proves the target for
`G`. Thus every DNN certificate below automatically includes arbitrary rooted
trees.

## 2. The 32 physical rows

For one doubled side, pair-member symmetry leaves three physical parity types:

`EE=(2,2)`, `EO=(1,2)`, and `OO=(1,3)`.                     (4)

The last choice is the first simple odd--odd pair; `(1,1)` is excluded. Swapping
the two doubled sides leaves six unordered pairs of types. Crossing these with
the two parities of `c` gives twelve orbits. Their orbit sizes among the 32
labelled parity rows are respectively

`1,4,2,4,4,1` for `EE/EE,EE/EO,EE/OO,EO/EO,EO/OO,OO/OO`,

for each parity of `c`; hence the table below represents all 32 rows.

Here is a wholly rational parametrization of the certificates. For a doubled
side of type `S` and parameter `t`, define its common endpoint correlation and
its total contribution to (2) by

`r_EE(t)=(1-6t^2+t^4)/(1+t^2)^2`,  `e_EE(t)=4t^2`,

`r_EO(t)=(1-6t^2+t^4)/(1+t^2)^2`,
`e_EO(t)=((1-t^2)/(2t))^2+2t^2`,

`q(t)=(3t-t^3)/(1-3t^2)`,
`r_OO(t)=-(1-q(t)^2)/(1+q(t)^2)`,
`e_OO(t)=q(t)^2+3t^2`.                                       (5)

Indeed `-r_OO=cos(6 atan t)`: the length-one contribution is
`tan^2(3 atan t)=q(t)^2`, while the length-three contribution is `3t^2`.

For the connector put

`r_E(t)=(1-6t^2+t^4)/(1+t^2)^2`, `e_E(t)=2t^2`,
`r_O(t)=(t^2-1)/(t^2+1)`,       `e_O(t)=t^2`.                (6)

These identities are just the multiple-angle tangent formulas applied to (1),
so every entry is rational. Given the three displayed correlations, use

`R=[[1,r_1,r_2],[r_1,1,r_c],[r_2,r_c,1]]`.                  (7)

The listed nonnegative determinant proves `R` positive semidefinite (all its
two-by-two principal minors are visibly nonnegative). The excess is the sum of
the three displayed contributions.

| doubled-side types | `c` | `(t_1,t_2,t_c)` | `(r_1,r_2,r_c)` | exact excess `E` | `det R` |
|---|---:|---|---|---:|---:|
| `EE,EE` | even | `(0,0,0)` | `(1,1,1)` | `0` | `0` |
| `EE,EE` | odd | `(1/3,1/3,1/2)` | `(7/25,7/25,-3/5)` | `41/36` | `1216/3125` |
| `EE,EO` | even | `(0,1/2,1/2)` | `(1,-7/25,-7/25)` | `25/16` | `0` |
| `EE,EO` | odd | `(1/4,1/2,1/3)` | `(161/289,-7/25,-4/5)` | `205/144` | `11527191/52200625` |
| `EE,OO` | even | `(1/4,1/4,1/3)` | `(161/289,-495/4913,7/25)` | `2246/1521` | `8593933244/15085980625` |
| `EE,OO` | odd | boundary | `(1,-1,-1)` | `0` | `0` |
| `EO,EO` | even | boundary | `(-1/2,-1/2,1)` | `2` | `0` |
| `EO,EO` | odd | class `111` | -- | structural | -- |
| `EO,OO` | even | `(1/2,1/5,1/5)` | `(-7/25,-828/2197,119/169)` | `83009/48400` | `1304316959/3016755625` |
| `EO,OO` | odd | `(1/2,1/5,1/2)` | `(-7/25,-828/2197,-3/5)` | `91237/48400` | `883705599/3016755625` |
| `OO,OO` | even | boundary | `(-1,-1,1)` | `0` | `0` |
| `OO,OO` | odd | `(1/5,1/5,1/2)` | `(-828/2197,-828/2197,-3/5)` | `16881/12100` | `22382224/120670225` |

In a boundary row, the displayed `R` is used directly; it is the limit of (5)--
(6), and substitution in (1) gives the displayed exact excess. Every numerical
entry in the table is a reduced fraction. Direct cross-multiplication gives

`2246<2(1521)`, `83009<2(48400)`,
`91237<2(48400)`, and `16881<2(12100)`,

while the other nonstructural inequalities are immediate. Thus every row except
the physical class-`111` orbit has excess at most two.

The exceptional orbit is exactly `EO,EO` with odd `c`: each doubled pair has
opposite parity and `c` has parity opposite to either route through their even
members. It is therefore precisely switching class `111`, handled structurally
in Section 3. The orbit has four labelled rows, according to the placements of
the odd member in the two doubled pairs.

For audit purposes, the 32 labelled rows are therefore partitioned as follows:

| pair of types | even `c` rows | odd `c` rows | disposition |
|---|---:|---:|---|
| `EE,EE` | `1` | `1` | DNN |
| `EE,EO` | `4` | `4` | DNN |
| `EE,OO` | `2` | `2` | DNN |
| `EO,EO` | `4` | `4` | DNN / class `111` |
| `EO,OO` | `4` | `4` | DNN |
| `OO,OO` | `1` | `1` | DNN |
| total | `16` | `16` | `28` DNN, `4` structural |

Fixed-parity monotonicity now extends each DNN row to all longer paths.

## 3. Structure of class `111`

The sole physical orbit left by Section 2 has both parallel pairs of type EO
and an odd connector. Thus both parallel pairs have opposite parity and `c` is
odd. Interchanging the members of each parallel pair so that `a,b` are even
gives the actual parity row

`(p_a,p_A,p_b,p_B,p_c)=(0,1,0,1,1)`.                         (7)

There are two cases.

### 3.1 A parallel path is longer than canonical

By symmetry it suffices to lengthen `a` or `A` in (7). Monotonicity then
reduces every such row to one of

`(4,1,2,1,1)` or `(2,3,2,1,1)`.                              (8)

For integers `d,i,j`, let the three branch vectors have planar arguments
`0, pi*i/d, pi*j/d`. Their Gram matrix is automatically positive semidefinite
with unit diagonal. For the first row use `(d;i,j)=(12;16,7)`; direct
substitution in (1) gives

`4 tan^2(pi/12)+tan^2(pi/6)+2 tan^2(7pi/48)
 +tan^2(5pi/24)+tan^2(pi/8) < 2`.                            (9)

For the second use `(d;i,j)=(6;2,8)`, giving

`2 tan^2(pi/12)+3 tan^2(pi/9)+2 tan^2(pi/6)
 +tan^2(pi/6) < 2`.                                         (10)

Both inequalities have exact rational certificates. The elementary bounds

`tan^2(7pi/48)<1/4`, `tan^2(5pi/24)<3/5`,
`tan^2(pi/8)<7/40`, `tan^2(pi/9)<2/15`.

follow from `pi<22/7` together with
`sin x < x-x^3/6+x^5/120` and
`cos x > 1-x^2/2+x^4/24-x^6/720` on the displayed intervals; after replacing
pi by `22/7`, squaring positive sides and clearing denominators leaves integer
comparisons. Also `tan^2(pi/12)<3/40`. Consequently the left side of (9) is
smaller than

`4(3/40)+1/3+2(1/4)+3/5+7/40=229/120<2`,

and the left side of (10) is smaller than

`2(3/40)+3(2/15)+3(1/3)=31/20<2`.
Thus (3) holds whenever any member of a parallel pair is noncanonical.
Relabeling handles all four parallel paths.

### 3.2 Both parallel pairs are canonical

Now `{a,A}={b,B}={1,2}`. The connector `c` is odd.

If `c>=3`, delete an internal vertex of `c`, together with every rooted-tree
branch based there. The induced complement is connected: the opened remnants
of `c` are trees, and the two intact doubled sides meet at branch vertex `0`.
Its cyclic blocks are precisely the two parallel cycles, both of length three.

If `c=1`, choose the even path in one parallel pair and delete its unique
internal vertex, again with every rooted-tree branch based there. The induced
complement is connected and has a theta core between `0` and the opposite
branch vertex. Its three path lengths are the two members `1,2` of the other
parallel pair and the route consisting of the undeleted odd path followed by
`c`, of length `1+1=2`. Thus its core is `Theta(1,2,2)`.

In either case the deleted induced territory `T` is a nonempty tree, so

`s^+(T)-|V(T)|=-1`.                                         (11)

The complement `H` is therefore either an attached two-triangle bicyclic
cactus or an attached `Theta(1,2,2)`. In both graphs every odd cycle is a
triangle. Every singleton odd-cycle term in the normalized Sachs expansion
lies strictly in the lower half-plane, while every even-cycle term and every
possible disjoint pair of odd cycles is real. Hence `s^+(H)>s^-(H)`. Since `H`
is bicyclic,

`s^+(H)-|V(H)|=1+(s^+(H)-s^-(H))/2>1`.                      (13)

Positive square energy is superadditive over induced vertex partitions.
Combining (11)--(13) gives

`s^+(G)-|V(G)| >= [s^+(H)-|V(H)|]+[s^+(T)-|V(T)|] > 0`.

The deletion includes arbitrary rooted trees at the deleted vertex; all other
attachments remain in `H`. Thus it covers every odd connector length and every
attachment pattern.

## 4. Audit status

The class-`111` argument is complete: a noncanonical parallel path has one of
the exact DNN certificates (9)--(10), while canonical parallel pairs admit an
induced deletion leaving either a two-triangle bicyclic cactus or
`Theta(1,2,2)`, plus a nonempty tree. These alternatives exhaust class `111`.

The physical census in Section 2 covers all 32 labelled parity rows without a
switching shortcut: 28 have exact rational DNN certificates and the remaining
four form exactly the class-`111` orbit. Section 3 closes that orbit for every
length, by DNN when a parallel path is noncanonical and by induced deletion
when both doubled pairs are canonical. Consequently the proposed theorem is
proved, including arbitrary rooted-tree attachments.
