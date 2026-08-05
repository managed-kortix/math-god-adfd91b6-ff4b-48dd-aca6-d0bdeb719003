# Doubled triangle: residue-mod-4 and long-path closure

## Theorem

Let `K` be any simple subdivision of the triangle with two adjacent sides
doubled, and attach arbitrary rooted trees at arbitrary vertices of `K`. Then

`s^+(G) >= |V(G)|`.

This note supplies the all-length step that the 32-base-row deletion ledger
does not supply. It uses that ledger only as a physical-parity census. The
actual all-length certificates are the eleven orbitwise DNN Gram records in
`doubled-triangle-dnn-cover.md`, together with the residue and long-path
argument below for the remaining orbit.

## 1. Path dual and the all-length rule

Label the branch paths

`a,A : 0--1`, `b,B : 0--2`, and `c : 1--2`,

and put `L=a+A+b+B+c`. Exact path elimination assigns to a path of length `l`
and endpoint correlation `r` the excess

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                       (1)

For fixed `r` and fixed parity,

`f_(l+2)(r) <= f_l(r)`,                                     (2)

with strict inequality away from a zero endpoint angle. Thus one correlation
matrix certified at a componentwise smaller length vector certifies every
vector obtained by adding nonnegative even integers to its coordinates.

For one doubled side, the first simple representatives are

- `EE=(2,2)`;
- `EO=(2,1)`, up to interchanging its members;
- `OO=(1,3)`, up to interchanging its members.

The twelve type/connector-parity orbits have labelled sizes

`1,4,2,4,4,1` for each connector parity, hence total 32. The exact rational
Gram ledger in `doubled-triangle-dnn-cover.md` certifies eleven of these twelve
orbits, comprising 28 labelled physical rows, with excess at most two. By (2),
those are already all-length certificates; none of the base-row deletions is
needed for those rows.

The only orbit not covered by those Gram records is

`EO,EO` with `c` odd.                                        (3)

It has four labelled rows. Interchanging members independently in the two
parallel pairs normalizes its parities to

`(p_a,p_A,p_b,p_B,p_c)=(0,1,0,1,1)`.                        (4)

## 2. Exact long-path DNN records

Call an even path canonical at length two and an odd path canonical at length
one. A parallel member is long if it is noncanonical, so its first long length
is four when even and three when odd.

For integers `d,i,j`, assign the branch vertices planar angles

`0, pi*i/d, pi*j/d`.

Their Gram matrix is positive semidefinite with diagonal one.

If an even parallel member is long, symmetry and (2) reduce all such length
vectors to

`(a,A,b,B,c)=(4,1,2,1,1)`.                                  (5)

Use `(d;i,j)=(12;16,7)`. Direct substitution in (1) gives

`E_even = 4 tan^2(pi/12)+tan^2(pi/6)`
`       + 2 tan^2(7pi/48)+tan^2(5pi/24)+tan^2(pi/8)`
`       < 4(3/40)+1/3+2(1/4)+3/5+7/40`
`       = 229/120 < 2`.                                     (6)

If an odd parallel member is long, reduce instead to

`(a,A,b,B,c)=(2,3,2,1,1)`.                                  (7)

Use `(d;i,j)=(6;2,8)`. The zero path term is omitted below, and (1) gives

`E_odd = 2 tan^2(pi/12)+3 tan^2(pi/9)`
`      + 2 tan^2(pi/6)+tan^2(pi/6)`
`      < 2(3/40)+3(2/15)+3(1/3)`
`      = 31/20 < 2`.                                        (8)

The rational tangent comparisons in (6)--(8) are audited using alternating
Taylor enclosures and `333/106 < pi < 355/113` by

`research/doubled-triangle-all-length-certificate.py`.

Reflection through the two doubled sides and interchange within either pair
move any long parallel member to (5) or (7) without changing its physical
parity or length. Equation (2) then allows arbitrary further `+2` increases in
all five paths. In particular, the same certificate allows an arbitrarily long
odd connector and simultaneous lengthening of several parallel members.

## 3. Complete residue-mod-4 split

Put

`X=a+A` and `Y=b+B`.                                        (9)

In (4), both `X` and `Y` are odd. A canonical doubled pair is exactly `{1,2}`
and has sum three. Therefore:

- a sum congruent to one modulo four forces that pair to contain a long member;
- a sum congruent to three modulo four is either canonical or contains a long
  member.

This gives the exhaustive table.

| `(X mod 4,Y mod 4)` | complete subcase | certificate |
|---|---|---|
| `(1,1)` | each pair is noncanonical | (6) or (8) |
| `(1,3)` | the first pair is noncanonical | (6) or (8) |
| `(3,1)` | the second pair is noncanonical | reflected (6) or (8) |
| `(3,3)` | at least one pair is noncanonical | (6) or (8) |
| `(3,3)` | both pairs are canonical | induced deletion below |

There is no assertion that residue three implies canonicality. The final two
rows explicitly retain both possibilities, which is the point missed by a
base-length-only deletion argument.

For the final row, `{a,A}={b,B}={1,2}` and `c` is any odd positive integer.

- If `c>=3`, delete an internal vertex of `c` and the entire rooted tree based
  there. The deleted territory is a nonempty tree. The connected complement
  has exactly the two doubled-side cycles, each a triangle, as its cyclic
  blocks.
- If `c=1`, delete the unique internal vertex of an even member of one doubled
  pair and its entire rooted tree. The connected complement has core
  `Theta(1,2,2)`.

In either case the deleted territory has

`s^+(T)-|V(T)|=-1`,

while the attached bicyclic complement has

`s^+(H)-|V(H)|>1`.

The latter is the established two-triangle/`Theta(1,2,2)` lower-half-plane
credit, including arbitrary rooted trees. Induced superadditivity therefore
gives `s^+(G)>|V(G)|` in this final structural row.

## 4. DNN balance and attachment ownership

For every DNN row above, `K` has `L` edges and `L-2` vertices. Excess at most
two gives

`kappa(K)<=L+2`, hence `s^+(K)>=L-2`.

If the rooted attachments have `t` edges in total, one-vertex additivity and
`kappa(T)=|E(T)|` give

`kappa(G)<=L+2+t`, `|E(G)|=L+t`, `|V(G)|=L-2+t`,

so the same DNN calculation proves `s^+(G)>=|V(G)|`. In the structural row,
the deletion assigns the complete rooted tree at the opened vertex to the
deleted territory and leaves every other attachment in the complement. Thus
every vertex and attachment is owned exactly once.

The eleven monotone DNN orbits and the five residue subcases above exhaust all
32 physical parity rows and every allowed path length. This proves the stated
theorem. The finite checker audits the census, residue decision table, and the
two long-path inequalities; it does not claim to machine-prove DNN duality,
path monotonicity, induced superadditivity, or the attached bicyclic credit.
