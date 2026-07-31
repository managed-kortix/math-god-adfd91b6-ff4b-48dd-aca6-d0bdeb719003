# The doubled-C4 kernel: exact switching sieve

## 1. Kernel and exact dual

Let the branch vertices be `0,1,2,3`, in cyclic order.  Write the six
internally disjoint branch paths as

`a,A : 0--1`, `b : 1--2`, `c,C : 2--3`, `d : 3--0`,

and let their lengths, in that order, be `l=(a,A,b,c,C,d)`.  Simplicity says
that the two entries in neither doubled pair may both be one.  Put `L=sum l`.
The core has `L-2` vertices and `L` edges, so the DNN bound proves the desired
inequality as soon as `kappa<=L+2`.

For a correlation matrix `R` on the four branch vertices, define

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                         (1)

The exact path reduction gives

`kappa-L = min_R [f_a(R01)+f_A(R01)+f_b(R12)
                  +f_c(R23)+f_C(R23)+f_d(R30)]`.              (2)

The minimum is over all real positive-semidefinite `R` with unit diagonal.
Thus every matrix displayed below is an exact DNN certificate.

For fixed `r`, `f_l(r)` strictly decreases when `l` is increased by two.  This
is the derivative calculation for `h_s(x)=s tan^2(x/s)`.  Consequently, within
any fixed parity row, (2) is largest at the canonical lengths

`l_i=1` for odd `l_i`, and `l_i=2` for even `l_i`.             (3)

This is the all-length parity theorem: a certificate for the simple canonical
row proves every simple length row having the same six parities.  Notice that
switching changes the canonical lengths, not merely the Gram matrix.  It is
therefore invalid to verify only one representative of a switching class; all
simple representatives must be checked.

## 2. Exactly eight switching classes

Record a canonical parity row by a bit string `p_a p_A p_b p_c p_C p_d`, with
one meaning odd.  Switching at branch vertex `i` toggles every incident bit.
After fixing the spanning-tree bits `p_a=p_b=p_c=0`, the three remaining bits

`(x,y,z)=(p_A,p_C,p_d)`

are complete switching invariants.  Hence there are exactly eight switching
classes.  Intersecting each class with the simplicity constraints
`not(p_a=p_A=1)` and `not(p_c=p_C=1)` gives the following exact census.

| `(x,y,z)` | lexicographically first simple row | number of simple rows |
|---|---:|---:|
| `000` | `000000` | 2 |
| `001` | `000001` | 2 |
| `010` | `000010` | 4 |
| `011` | `000011` | 4 |
| `100` | `010000` | 4 |
| `101` | `010001` | 4 |
| `110` | `010010` | 8 |
| `111` | `010011` | 8 |

The counts sum to all 36 simple canonical parity rows.

## 3. Exact Gram certificates

For integers `k=(0,k_1,k_2,k_3)`, let

`R(k)_ij = cos(pi(k_i-k_j)/6)`.                               (4)

This is the Gram matrix of the planar unit vectors
`(cos(pi k_i/6),sin(pi k_i/6))`; in particular it is exactly PSD and has
unit diagonal.  The following table gives a certificate for every row outside
the last switching class.  Rows on the same line use the same `k`.  Every
entry is exact: substitution in (1) uses only standard angles.

| parity rows | `(k_1,k_2,k_3)` | certified excess |
|---|---:|---:|
| `000000` | `(0,0,0)` | `0` |
| `001001` | `(0,6,6)` | `0` |
| `000001` | `(11,8,7)` | `<3/5` |
| `001000` | `(1,8,9)` | `<3/5` |
| `000010`, `000100` | `(1,3,11)` | `<5/4` |
| `010000`, `100000` | `(8,9,10)` | `<5/4` |
| `000011`, `000101` | `(1,2,6)` | `<9/8` |
| `001010`, `001100` | `(11,5,1)` | `<9/8` |
| `010001`, `100001` | `(8,7,6)` | `<9/8` |
| `011000`, `101000` | `(8,2,1)` | `<9/8` |
| `001011`, `001101` | `(2,9,5)` | `<3/2` |
| `011001`, `101001` | `(4,9,7)` | `<3/2` |
| `010010`, `010100`, `100010`, `100100` | `(8,8,0)` | `2` |
| `011011`, `011101`, `101011`, `101101` | `(4,10,6)` | `2` |

For a formal check, replace each displayed bound by the left side of (2), use
(4), and reduce with

`tan^2(pi/12)=7-4 sqrt(3)`, `tan^2(pi/8)=3-2 sqrt(2)`,

together with angle addition.  The two boundary lines are especially simple:
their six contributions are respectively `2/3,1/3,0,2/3,1/3,0`, in a suitable
order.  Thus their sum is exactly two.  The other lines have strict slack.

It follows, by the monotonicity preceding (3), that every doubled-C4
subdivision in the first seven switching classes, with arbitrary lengths and
subject to simplicity, satisfies `kappa<=L+2`.  One-vertex additivity of
`kappa`, and `kappa(T)=|E(T)|`, then gives `s^+(G)>=|V(G)|` after arbitrary
rooted trees are attached.

## 4. The failed canonical class

The eight simple rows in class `111` are

`010011, 010101, 011010, 011100,`

`100011, 100101, 101010, 101100`.                             (5)

The matrices above do not certify these rows.  Direct minimization of (2)
suggests the common canonical value `2.0796037466...`, but that decimal is not
used as a theorem here: an exact lower-bound certificate for the elliptope
minimum has not been supplied.  Accordingly, (5) is the precise failed class
of this Gram-certificate sieve, not a claimed list of counterexamples.

There is, however, a rigorous induced-deletion closure for the canonical rows.
Each row in (5) has exactly one even connector among `b,d`; its canonical
length is two.  Delete its internal vertex together with the rooted tree at
that vertex.  The deleted territory is a nonempty tree and has credit `-1`.
The complement is connected and bicyclic: its cyclic blocks are the two
doubled-path cycles.  Both have canonical length `1+2=3`.  Hence it is an
attached favorable bicyclic cactus with two `3 mod 4` odd cycles and has credit
strictly greater than one.  Induced superadditivity therefore gives

`sigma(G) > 1 + (-1) = 0`.                                   (6)

This closes all eight canonical failures, including arbitrary rooted-tree
attachments.

## 5. Closing the failed class at all lengths

There is a stronger all-length dichotomy.  Up to the automorphisms of the
kernel and interchange of parallel paths, take the failed parity row to be

`(p_a,p_A,p_b,p_c,p_C,p_d)=(0,1,0,0,1,1)`.                   (7)

Its canonical lengths are `(2,1,2,2,1,1)`.  If any member of either doubled
pair is longer than canonical, monotonicity reduces to one of two rows.  Define

`Q(k)_ij=cos(pi(k_i-k_j)/4)`.

For `(4,1,2,2,1,1)`, the exact Gram matrix `Q(0,3,2,5)` gives excess

`4 tan^2(3pi/32)+3 tan^2(pi/8)
 +2 tan^2(pi/16)+2 tan^2(3pi/16) < 2`.                       (8)

For `(2,3,2,2,1,1)`, the exact Gram matrix `Q(0,1,1,4)` gives excess

`2 tan^2(pi/16)+3 tan^2(pi/8)
 +2 tan^2(3pi/16)+tan^2(pi/8) < 2`.                          (9)

For a short rational verification of (8)--(9), repeated half-angle identities
and squaring give

`tan^2(3pi/32)<93/1000`, `tan^2(pi/8)<172/1000`,

`tan^2(pi/16)<40/1000`, `tan^2(3pi/16)<447/1000`.

The right sides of (8) and (9) are therefore below `1862/1000` and
`1662/1000`, respectively.  These are exact rational bounds; each displayed
tangent inequality reduces, after at most three squarings of positive sides,
to an integer inequality.  Relabeling gives the same two certificates for
either doubled pair, and increasing any length further only decreases its
term.

It remains that both doubled pairs have exactly the canonical lengths `{1,2}`.
The connector parities in class `111` are opposite.  Delete an internal vertex
of the even connector; it exists because that connector has length at least
two.  The complement is an attached bicyclic cactus whose two cyclic blocks
have lengths

`a+A=c+C=3`,                                                  (10)

regardless of both connector lengths.  It is therefore favorable and has
credit strictly greater than one, while the deleted territory is a tree of
credit `-1`.  This proves (6) for every remaining length row.

Combining Sections 3 and 5 proves the rigorous all-length parity theorem:
every simple subdivision of the doubled-C4 kernel, with arbitrary rooted-tree
attachments, satisfies `s^+(G)>=|V(G)|`.  The first seven switching classes
are closed uniformly by DNN.  In the eighth class, DNN closes the row as soon
as a doubled path is longer than canonical; otherwise induced deletion leaves
a favorable `C3`--`C3` bicyclic remainder plus a tree.
