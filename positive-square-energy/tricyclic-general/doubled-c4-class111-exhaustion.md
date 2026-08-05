# Doubled-C4 exceptional orbit: exhaustive all-length closure

This note isolates the eight-row automorphism orbit not closed by the canonical
DNN sieve. The earlier label "switching class 111" was imprecise: under the
fixed switching normalization, four rows lie in class `110` and four in class
`111`. Interchanging parallel-path names joins them into one kernel-automorphism
orbit. The point here is to make explicit that arbitrary connector lengths
introduce no additional case.

## 1. Normal form

Label the branch vertices `A,B,C,D` cyclically. Let the doubled sides be

`a,A' : A--B`, `c,C' : C--D`,

and let `b : B--C` and `d : D--A` be the two single connectors. Write the six
lengths as

`(a,A',b,c,C',d)`.

In the exceptional orbit, each doubled side has one odd and one even path.
Choose the even member of each doubled side as `a` and `c`. The exceptional-row condition says
that the two single connectors have opposite parity. A dihedral automorphism
interchanges the connectors if necessary, so normalize further by making `BC`
odd. Thus, after also interchanging the parallel-path names when needed,

`(p_a,p_A',p_b,p_c,p_C',p_d)=(0,1,1,0,1,0)`.                 (1)

Thus `BC` is odd and `DA` is even. In particular, `DA` is always openable:
its length is at least two. The simple canonical row is

`(a,A',b,c,C',d)=(2,1,1,2,1,2)`.                            (2)

Here and below, canonical means length one for an odd path and length two for
an even path. A path is long if its length is at least two more than its
canonical length.

Put

`X=a+A'` and `Y=c+C'`.                                      (3)

Both `X` and `Y` are odd. Their residues modulo four, together with whether a
parallel path is canonical or long, give the complete classification.

## 2. The open-path deletion

Delete an internal vertex of `DA`, together with the rooted tree attached at
that vertex. The deleted induced graph is a nonempty tree and hence has credit

`sigma(T)=s^+(T)-|V(T)|=-1`.

The complement is connected. The two remnants of `DA` are pendant trees, as
are all original rooted-tree attachments. Its cyclic blocks are exactly the
two cycles formed by the doubled sides, of lengths `X` and `Y`. Consequently
the complement is an attached bicyclic cactus.

If

`X=Y=3 (mod 4)`,                                             (4)

both odd cyclic blocks are favorable. The established attached-cactus packet
then gives `sigma(H)>1`, and induced superadditivity gives

`sigma(G)>=sigma(H)+sigma(T)>1-1=0`.                         (5)

This deletion is available for every value of the odd connector `BC`. If
`BC>=3`, then `BC` is also openable, and deleting an internal vertex of it
leaves the same two cyclic blocks. Thus the distinction `BC=1` versus `BC>=3`
creates no hidden exceptional family.

No bipartite remainder occurs in this normal form because `X` and `Y` are
odd. The useful deletion remainder is precisely the favorable cactus in (4).

## 3. Explicit DNN certificates for every remaining row

For a correlation matrix `R` on `A,B,C,D`, the exact path reduction says

`kappa-L <= sum_P l_P tan^2(acos((-1)^l_P R_uv)/(2l_P))`,     (6)

where `P` runs over the six branch paths, `u,v` are its endpoints, and
`L=a+A'+b+c+C'+d`. The desired DNN bound is `kappa-L<=2`.

For fixed endpoint correlation and fixed parity, each summand in (6) strictly
decreases when its length is increased by two. It therefore suffices to give a
certificate at the first long value while keeping all other paths canonical.

For integers `k_A,k_B,k_C,k_D`, set

`Q(k)_uv=cos(pi(k_u-k_v)/4)`.                                (7)

This is the Gram matrix of four planar unit vectors, so it is exactly positive
semidefinite with unit diagonal.

If the even member of the first doubled pair is long, reduce to

`(4,1,1,2,1,2)`.

The matrix `Q(0,5,2,7)` gives

`4 tan^2(3pi/32)+3 tan^2(pi/8)
 +2 tan^2(pi/16)+2 tan^2(3pi/16)<2`.                         (8)

If the odd member of that pair is long, reduce to

`(2,3,1,2,1,2)`.

The matrix `Q(0,7,3,0)` gives

`2 tan^2(pi/16)+4 tan^2(pi/8)+2 tan^2(3pi/16)<2`.            (9)

For an entirely rational check, use

`tan^2(3pi/32)<93/1000`, `tan^2(pi/8)<172/1000`,

`tan^2(pi/16)<40/1000`, `tan^2(3pi/16)<447/1000`.

The right sides of (8) and (9) are then respectively below `1862/1000` and
`1662/1000`. Each tangent bound follows from repeated half-angle identities
and squaring positive quantities, so these are exact certificates rather than
decimal optimization. Reflection of the kernel supplies the same two
certificates when a member of the second doubled pair is long. Monotonicity in
each path length then proves (6) for arbitrary additional increases, including
arbitrary increases of either connector.

## 4. Exhaustive residue table

There are only four residue cases for the two doubled-side cycle lengths.

| `(X mod 4,Y mod 4)` | consequence | certificate |
|---|---|---|
| `(3,3)` | `DA` deletion leaves a favorable cactus | (5) |
| `(1,3)` | the first doubled pair is not canonical | (8) or (9) |
| `(3,1)` | the second doubled pair is not canonical | reflected (8) or (9) |
| `(1,1)` | both doubled pairs are not canonical | either DNN certificate |

Indeed, a canonical doubled pair has lengths `{1,2}` and hence cycle length
three. Therefore a doubled-side residue of one forces at least one member of
that pair to be long. Conversely, if both doubled pairs are canonical, then
`X=Y=3`, so the deletion case applies.

For clarity, crossing this table with the connector alternatives gives no new
rows:

| odd `BC` length | `(X,Y)=(3,3) mod 4` | at least one of `X,Y=1 mod 4` |
|---|---|---|
| `BC=1` | open `DA`; favorable cactus | explicit parallel-long DNN |
| `BC>=3` | open `DA` or `BC`; favorable cactus | explicit parallel-long DNN |

The even connector `DA` may have any even length at least two. Longer connector
lengths only decrease the DNN objective and do not alter the deletion cycles.

To spell out the DNN conclusion, the core has `m=L` and `n=L-2`. Equations
(8)--(9) give `kappa<=L+2`, and the LTZ/DNN inequality gives

`s^+(G)=2L-s^-(G)>=2L-kappa>=L-2=n`.

If `t` rooted-tree edges are attached, one-vertex additivity gives
`kappa<=L+2+t`, while the graph has `L+t` edges and `L-2+t` vertices, yielding
the same inequality.

Thus every arbitrary-length simple subdivision in the exceptional orbit is
closed: some openable connector deletion leaves a favorable attached cactus,
or a doubled path is long and one of the exact DNN certificates (8)--(9)
applies. One-vertex additivity of `kappa`, together with `kappa(T)=|E(T)|`,
handles arbitrary rooted-tree attachments in the DNN cases as computed above;
the deletion argument already includes them in the favorable-cactus cases.
Hence

`s^+(G)>=|V(G)|`

for the whole class, with strict inequality in the deletion branch.
