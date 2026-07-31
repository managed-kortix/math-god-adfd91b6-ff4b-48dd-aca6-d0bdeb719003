# Doubled triangle: exhaustive 32-base-row cover

This note does not modify the main manuscript. It audits all 32 physical parity
rows of the doubled-triangle kernel, including the rows in which a doubled pair
is odd--odd. In such a pair the first simple lengths are `1,3`, not `1,1`.

## 1. Setup and deletion tests

Write the five branch paths as

`a,A : 0--1`, `b,B : 0--2`, and `c : 1--2`.

For a parity bit `0` use base length two and for a parity bit `1` use base
length one, except that an odd--odd doubled pair uses the unordered base pair
`{1,3}`. A physical row is the bit string

`p_a p_A p_b p_B p_c`.

Thus all `2^5=32` rows have simple base realizations. Interchanging the two
members of either doubled pair and interchanging the two doubled sides generate
the kernel automorphisms used below.

Opening an internal vertex of a path means deleting that vertex together with
the entire rooted tree based there. The deleted territory is a nonempty tree
and has credit `-1`. The connected complement has credit at least one in either
of the following cases, and strictly greater than one in the favorable cases.

1. If `c` is opened, the cyclic blocks of the complement are the two cycles of
   lengths `a+A` and `b+B`. The deletion works when both are even, or when each
   odd one is `3 mod 4` and at least one is odd.
2. If `a` is opened, the complement has attached theta core
   `Theta(b,B,A+c)`. The analogous formulas for opening `A,b,B` follow by
   relabeling. The deletion works when the three theta paths have one parity,
   or when its two odd cycles both have length `3 mod 4`.

The first alternative is bipartite. In the second alternative all imaginary
singleton-cycle terms in the normalized Sachs expansion have the favorable
sign. These are exactly the established bipartite/favorable bicyclic credits,
so induced superadditivity pays for the deleted tree.

## 2. Exact orbit table

For a doubled pair use the type

- `E` for parity `00`, with base lengths `(2,2)`;
- `M` for parity `01` or `10`, with base lengths `(2,1)` up to interchange;
- `O` for parity `11`, with first-simple base lengths `(1,3)` up to
  interchange.

The unordered pair of doubled-pair types, together with `p_c`, gives exactly
the twelve automorphism orbits below. The orbit sizes sum to 32.

| orbit | `p_c` | representative row | base lengths `(a,A,b,B,c)` | size | certificate |
|---|---:|---:|---:|---:|---|
| `EE` | 0 | `00000` | `(2,2,2,2,2)` | 1 | open `a`: bipartite `Theta(2,2,4)` |
| `EE` | 1 | `00001` | `(2,2,2,2,1)` | 1 | DNN `R(2,10;6)` |
| `EM` | 0 | `00010` | `(2,2,2,1,2)` | 4 | open `c`: cactus cycles `(4,3)` |
| `EM` | 1 | `00011` | `(2,2,2,1,1)` | 4 | open `b`: bipartite `Theta(2,2,2)` |
| `EO` | 0 | `00110` | `(2,2,1,3,2)` | 2 | open `c`: bipartite cactus cycles `(4,4)` |
| `EO` | 1 | `00111` | `(2,2,1,3,1)` | 2 | open `a`: bipartite `Theta(1,3,3)` |
| `MM` | 0 | `01010` | `(2,1,2,1,2)` | 4 | open `c`: favorable cactus cycles `(3,3)` |
| `MM` | 1 | `01011` | `(2,1,2,1,1)` | 4 | open `a`: favorable `Theta(2,1,2)` |
| `MO` | 0 | `01110` | `(2,1,1,3,2)` | 4 | open `a`: bipartite `Theta(1,3,3)` |
| `MO` | 1 | `01111` | `(2,1,1,3,1)` | 4 | open `B`: favorable `Theta(2,1,2)` |
| `OO` | 0 | `11110` | `(1,3,1,3,2)` | 1 | open `A`: bipartite `Theta(1,3,3)` |
| `OO` | 1 | `11111` | `(1,3,1,3,1)` | 1 | DNN `R(2,4;3)` |

For reference, the physical rows in these orbits are

| orbit and `p_c` | physical rows |
|---|---|
| `EE,0` | `00000` |
| `EE,1` | `00001` |
| `EM,0` | `00010,00100,01000,10000` |
| `EM,1` | `00011,00101,01001,10001` |
| `EO,0` | `00110,11000` |
| `EO,1` | `00111,11001` |
| `MM,0` | `01010,01100,10010,10100` |
| `MM,1` | `01011,01101,10011,10101` |
| `MO,0` | `01110,10110,11010,11100` |
| `MO,1` | `01111,10111,11011,11101` |
| `OO,0` | `11110` |
| `OO,1` | `11111` |

Hence favorable/bipartite deletion closes 30 of the 32 base rows. Only
`00001` and `11111` need DNN.

## 3. The two explicit Gram certificates

For integers `d,i,j`, let

`R(i,j;d) = Gram(u_0,u_1,u_2)`,

where

`u_0=(1,0)`, `u_1=(cos(pi i/d),sin(pi i/d))`, and
`u_2=(cos(pi j/d),sin(pi j/d))`.

This is an exact positive-semidefinite correlation matrix. For

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`,                 (1)

the exact path dual gives

`kappa(K)-L <= f_a(R01)+f_A(R01)+f_b(R02)+f_B(R02)+f_c(R12)`.

### Row `00001`

Take `R(2,10;6)`, so the branch angles are `0,pi/3,5pi/3`. Explicitly,

`R = [[1,1/2,1/2],[1/2,1,-1/2],[1/2,-1/2,1]]`,

and for base lengths `(2,2,2,2,1)` the five terms sum to

`8 tan^2(pi/12)+1/3 = 169/3-32 sqrt(3) < 14/15 < 2`.   (2)

Indeed, `tan^2(pi/12)=7-4sqrt(3)<3/40`; the latter inequality follows by
squaring the positive inequality `sqrt(3)>277/160`, since
`3*160^2=76800>76729=277^2`.

### Row `11111`

Take `R(2,4;3)`, so the branch angles are `0,2pi/3,4pi/3`. Explicitly,

`R = [[1,-1/2,-1/2],[-1/2,1,-1/2],[-1/2,-1/2,1]]`,

and for first-simple base lengths `(1,3,1,3,1)` the five terms sum to

`1+6 tan^2(pi/18) < 1+6 tan^2(pi/12) < 29/20 < 2`.     (3)

The first strict inequality is monotonicity of tangent on `(0,pi/2)`, and the
second uses the exact bound in (2). This is also substantially below the DNN
threshold without any numerical optimization.

Since the core has `L` edges and `L-2` vertices, (2)--(3) give
`kappa(K)<=L+2` and therefore `s^+(K)>=L-2`. One-vertex additivity of `kappa`
and `kappa(T)=|E(T)|` include arbitrary rooted-tree attachments in both DNN
rows.

For each of these two parity rows, fixed-parity path monotonicity extends its
Gram certificate to every longer simple realization. For `11111`, any simple
odd--odd pair has, after interchanging its members, lengths at least `(1,3)`;
the same is true independently for the other doubled pair.

## 4. Exhaustiveness and scope

The orbit sizes are

`1+1+4+4+2+2+4+4+4+4+1+1=32`.

Every orbit has either an explicit legal induced deletion or one of the two
exact Gram matrices above. Thus this is an exhaustive certificate cover of all
32 first-simple base rows, including all fourteen rows omitted if odd--odd
doubled pairs are incorrectly discarded.

The two DNN certificates extend to all lengths in their parity rows. A base-row
deletion, however, does not by itself extend under arbitrary `+2` changes of a
path length, because such a change can reverse a cycle residue modulo four.
Accordingly, the present table is an exhaustive base-row certificate and must
not be cited alone as an all-length closure of the other thirty parity rows.
