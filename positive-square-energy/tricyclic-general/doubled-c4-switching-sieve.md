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
is the derivative calculation for `h_s(x)=s tan^2(x/s)`.  For a single path
the first lengths are one when odd and two when even.  There is one essential
simplicity correction: if both paths in a doubled pair are odd, their first
simple unordered lengths are `{1,3}`, not `{1,1}`.  Thus the three
first-simple states of a doubled pair are

`EE=(2,2),  EO=(1,2),  OO=(1,3)`,                            (3)

up to interchanging its members.  A certificate at these componentwise first
simple lengths proves every longer realization of the same *physical* parity
row.  Notice that switching changes physical first lengths, not merely the
Gram matrix.  It is therefore invalid to verify only one representative of a
switching class; all physical representatives must be checked.

There is a second bookkeeping caution. Interchanging the names of two parallel
paths is a genuine kernel automorphism, not switching. It can change the
displayed switching word because the normalized outer cycle uses the named
paths `a` and `c`. Thus an automorphism orbit need not be one switching class.

## 2. Exactly eight switching classes

Record a parity word by `p_a p_A p_b p_c p_C p_d`, with one meaning odd.
Switching at branch vertex `i` toggles every incident bit.  After fixing the
spanning-tree bits `p_a=p_b=p_c=0`, the three remaining bits

`(x,y,z)=(p_A,p_C,p_d)`

are complete switching invariants.  Hence there are exactly eight switching
classes, each with eight labelled parity words.  The former 36-row census was
not a census of simple subdivisions: it deleted every word with an `OO`
doubled pair.  Simplicity deletes only the simultaneous length choice `(1,1)`;
the parity word is realizable at `{1,3}`.  Therefore all `2^6=64` parity words
are realizable.  The old restricted slice, retained below because its 28 DNN
certificates and eight structural rows remain valid, has the following counts.

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

The counts sum to 36 only in the restricted no-`OO` slice.  The omitted
realizable words are the other 28 labelled parity words.  At the coarser
first-simple type level, the two doubled sides independently have type
`EE,EO,OO` and the connectors independently have parity `E,O`, giving
`3*3*2*2=36` type states.  Exactly 20 of these have at least one `OO` side;
Section 4 supplies their complete all-length cover.

## 3. Exact Gram certificates on the old no-`OO` slice

For integers `k=(0,k_1,k_2,k_3)`, let

`R(k)_ij = cos(pi(k_i-k_j)/6)`.                               (4)

This is the Gram matrix of the planar unit vectors
`(cos(pi k_i/6),sin(pi k_i/6))`; in particular it is exactly PSD and has
unit diagonal. The following table gives a certificate for 28 of the 36 rows.
Rows on the same line use the same `k`. Every
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
subdivision represented by these 28 no-`OO` rows, with arbitrary lengths,
satisfies `kappa<=L+2`.  One-vertex additivity of `kappa`, and
`kappa(T)=|E(T)|`, then gives `s^+(G)>=|V(G)|` after arbitrary rooted trees are
attached.

## 4. The omitted odd--odd rows: complete exact DNN cover

It remains to repair every realizable parity word having an `OO` doubled
side.  Reflect the four-cycle if necessary so that the first doubled side is
`OO`, and interchange its two members so that its first-simple lengths are
`(a,A)=(1,3)`.  The other doubled side has type `S in {EE,EO,OO}`, while the
connectors `b,d` independently have parity `E` or `O`.  These are exactly
`3*2*2=12` normalized states.  They cover all 20 of the 36 first-simple type
states, equivalently all 28 labelled parity words, having at least one `OO`
side (states with two `OO` sides admit the two normalizations).

For integers `k=(k_0,k_1,k_2,k_3)`, put

`P(k)_ij=cos(pi(k_i-k_j)/3)`.                                 (5)

This is the Gram matrix of four planar unit vectors, hence is exactly positive
semidefinite with unit diagonal.  The following table gives a certificate for
all twelve states.  The path order is `(a,A,b,c,C,d)`.  In the last column,

`alpha=2 tan^2(pi/12)=14-8 sqrt(3)`,

`beta=tan^2(pi/6)=1/3`, and `gamma=3 tan^2(pi/18)`.

Every unlisted path contribution is zero.  The displayed identities follow
directly from (1), including the length-three `OO` member; no decimal
optimization is involved.

| second side `S` | `(p_b,p_d)` | first-simple lengths | `k` | exact excess |
|---|---:|---:|---:|---:|
| `EE` | `OO` | `(1,3,1,2,2,1)` | `(0,3,5,4)` | `2 beta+2 alpha` |
| `EE` | `OE` | `(1,3,1,2,2,2)` | `(0,3,0,0)` | `0` |
| `EE` | `EO` | `(1,3,2,2,2,1)` | `(0,3,3,3)` | `0` |
| `EE` | `EE` | `(1,3,2,2,2,2)` | `(0,3,2,1)` | `4 alpha` |
| `EO` | `OO` | `(1,3,1,1,2,1)` | `(0,3,0,4)` | `4 beta` |
| `EO` | `OE` | `(1,3,1,1,2,2)` | `(0,3,1,5)` | `4 beta+alpha` |
| `EO` | `EO` | `(1,3,2,1,2,1)` | `(0,3,2,4)` | `4 beta+alpha` |
| `EO` | `EE` | `(1,3,2,1,2,2)` | `(0,3,3,1)` | `3 beta+alpha` |
| `OO` | `OO` | `(1,3,1,1,3,1)` | `(0,3,0,3)` | `0` |
| `OO` | `OE` | `(1,3,1,1,3,2)` | `(0,3,1,5)` | `2 beta+alpha+gamma` |
| `OO` | `EO` | `(1,3,2,1,3,1)` | `(0,3,2,4)` | `2 beta+alpha+gamma` |
| `OO` | `EE` | `(1,3,2,1,3,2)` | `(0,3,3,0)` | `0` |

For a short wholly exact strict comparison,

`alpha < 1/6`, `beta < 17/50`, `gamma < 1/10`.                (6)

Here `beta=1/3`; `alpha<1/6` is equivalent to
`48^2*3>83^2`.  Also the squared triple-angle map
`y(3-y)^2/(1-3y)^2` is increasing for `0<=y<=1/3`; if
`x=tan(pi/18)` had `x^2>=1/30`, it would give

`tan^2(pi/6) >= ((1/30)(3-1/30)^2)/(1-3/30)^2`

`              = 7921/21870 > 1/3`,

a contradiction.  The verifier also reconstructs every term independently
with alternating Taylor enclosures and `333/106<pi<355/113`.  The deliberately
loose `beta<17/50` makes the largest resulting upper bound

`4(17/50)+1/6 = 229/150 < 2`.

Thus every first-simple state containing `OO` has `kappa-L<2`.  Fixed-physical-
parity monotonicity now permits arbitrary independent additions of two to all
six path lengths.  In particular it covers both odd paths becoming long,
simultaneously lengthened doubled sides, and arbitrary connector lengths.
One-vertex additivity then covers arbitrary rooted-tree attachments exactly as
in Section 3.

## 5. The exceptional canonical orbit in the no-`OO` slice

The eight simple rows not certified above are

`010011, 010101, 011010, 011100,`

`100011, 100101, 101010, 101100`.                             (5)

They form one orbit under dihedral kernel automorphisms and interchange of
parallel-path names. They are not one switching class: the normalization of
Section 2 puts four in class `110` and four in class `111`. The matrices above
do not certify these rows. Direct minimization of (2)
suggests the common canonical value `2.0796037466...`, but that decimal is not
used as a theorem here: an exact lower-bound certificate for the elliptope
minimum has not been supplied. Accordingly, (5) is the precise exceptional
orbit of this Gram-certificate sieve, not a claimed list of counterexamples.

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

## 6. Closing the exceptional orbit at all lengths

There is a stronger all-length dichotomy.  Up to the automorphisms of the
kernel and interchange of parallel paths, take the exceptional parity row to be

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
In this normal form the connector parities are opposite. Delete an internal
vertex of the even connector; it exists because that connector has length at
least two. The complement is an attached bicyclic cactus whose two cyclic blocks
have lengths

`a+A=c+C=3`,                                                  (10)

regardless of both connector lengths.  It is therefore favorable and has
credit strictly greater than one, while the deleted territory is a tree of
credit `-1`.  This proves (6) for every remaining length row.

Combining Sections 3, 4, and 6 proves the rigorous all-length theorem: every
simple subdivision of the doubled-C4 kernel, with arbitrary rooted-tree
attachments, satisfies `s^+(G)>=|V(G)|`.  Section 4 closes all 28 parity words
formerly omitted merely because a doubled pair was odd--odd.  On the old
36-word no-`OO` slice, DNN closes 28 rows.  The remaining eight rows (four each
in switching classes `110` and `111`) are closed by DNN as soon as a doubled
path is longer than first-simple; otherwise induced deletion leaves a
favorable `C3`--`C3` bicyclic remainder plus a nonempty tree.
