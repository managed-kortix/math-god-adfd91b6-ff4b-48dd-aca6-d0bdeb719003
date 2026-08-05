# Exact symbolic templates for the last tricyclic kernel rows

This note independently optimizes the correlation-Gram obstruction in the two
rows where the finite parity ledger does not itself give a uniform DNN proof:
the doubled-triangle class `111` and the all-odd switching class of a subdivided
`K4`. It records both finite all-length templates and exact counterexamples to
a universal Gram-only closure.

Throughout,

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.

For fixed `r` and fixed parity, `f_l(r)` decreases under `l -> l+2`. Thus every
strict certificate below extends coordinatewise to all longer paths with the
same parity.

## 1. Doubled triangle

Write the paths as `a,A:01`, `b,B:02`, and `c:12`. Up to relabeling, the only
parity row not covered by the rational 32-row ledger is

`(p_a,p_A,p_b,p_B,p_c)=(0,1,0,1,1)`.

Its canonical length vector is `(2,1,2,1,1)`.

### Exact Gram counterexample at the canonical row

There is no correlation-Gram certificate of excess at most two at this row.
The exact minimum is already greater than two.

Indeed, for planar branch angles `(0,theta,2pi-theta)`, put

`u=tan(theta/4)` and `x=tan(theta/2)=2u/(1-u^2)`.

The excess becomes

`F(u)=2(2u^2+x^(-2))+(1-x^2)^2/(4x^2)`

`    =(73u^8-172u^6+150u^4-44u^2+9)/(16u^2(1-u^2)^2)`.

The stationary equation in `y=u^2` is

`73y^5-219y^4+194y^3-62y^2-27y+9=0`.                 (DT1)

It has a unique root `y_0` in `(1/4,1/3)`. Substitution gives

`F(sqrt(y_0)) = 2.1967859496... > 2`.

The strict inequality is especially transparent before optimization:

`F(u)-2 = Q(u^2)/(16u^2(1-u^2)^2)`,

where

`Q(y)=73y^4-204y^3+214y^2-76y+9`.

The quartic `Q` has no real root and `Q(0)>0`, so `Q(y)>0` for every real
`y`. To pass from this slice to the full elliptope, average a feasible matrix
under the automorphism interchanging branch vertices `1,2`. Convexity of every
path cost leaves `R01=R02=s` without increasing the objective. The `3x3`
determinant condition gives `R12>=2s^2-1`; since the unit odd-path cost
increases with its correlation, equality holds at an optimum. Writing
`s=cos(theta)` recovers the planar family above, and its Lagrange equation is
exactly (DT1). Hence the canonical class-`111` row is an exact counterexample
to any proposed all-length DNN template with threshold two. A structural
certificate is necessary there.

### Two finite noncanonical templates

If an even parallel path is long, monotonicity reduces to
`(a,A,b,B,c)=(4,1,2,1,1)`. Use planar angles

`(theta_0,theta_1,theta_2)=(0,4pi/3,7pi/12)`.

The Gram matrix is

```text
[[1, -1/2,                 (sqrt(2)-sqrt(6))/4],
 [-1/2, 1,                -sqrt(2)/2],
 [(sqrt(2)-sqrt(6))/4, -sqrt(2)/2, 1]].
```

It has determinant zero and its exact excess is

`4tan^2(pi/12)+tan^2(pi/6)+2tan^2(7pi/48)`
` +tan^2(5pi/24)+tan^2(pi/8) < 229/120 < 2`.          (DT2)

If an odd parallel path is long, reduce to `(2,3,2,1,1)` and use angles

`(theta_0,theta_1,theta_2)=(0,pi/3,4pi/3)`.

Its Gram matrix is

```text
[[1, 1/2, -1/2],
 [1/2, 1, -1],
 [-1/2, -1, 1]].
```

Again the determinant is zero, and the exact excess is

`2tan^2(pi/12)+3tan^2(pi/9)+3tan^2(pi/6) < 31/20 < 2`. (DT3)

Thus (DT2)--(DT3), relabeled over the four parallel paths, cover every
noncanonical realization. When both doubled pairs are canonical, the exact
counterexample above explains why one must use the known induced deletion:
open a long connector, or for a unit connector open one even parallel path.

## 2. All-odd `K4`

Call an odd path unit at length one and long at length at least three. The
automorphism group has one orbit with no long edge, one with one long edge, two
with two long edges (adjacent or opposite), and one coarse class with at least
three long edges.

### Exact counterexample for zero long edges

For six unit paths the optimization is

`min_R sum_(ij) (1+R_ij)/(1-R_ij)`.

By convexity and `S_4` averaging, an optimum is equicorrelated. Positive
semidefiniteness requires `r>=-1/3`, and the objective increases with `r`.
Thus the exact minimum is attained by the regular simplex at `r=-1/3` and is

`6(1/2)=3>2`.                                             (K1)

The no-long state therefore uses the attached-`K4` packet. With exactly one
long edge, the finite cover uses induced deletion to `Theta(1,2,2)`; no
Gram-only impossibility is claimed for that state here.

### Three finite DNN templates

If at least three edges are long, use the regular-simplex Gram matrix

`R_ii=1`, `R_ij=-1/3`.

A unit edge costs `1/2`; a long edge costs at most

`3tan^2(acos(1/3)/6)<1/6`.

For `q>=3` long edges, the total is strictly below

`(6-q)/2+q/6 = 3-q/3 <= 2`.                              (K3)

For exactly two opposite long edges, assign planar angles

`(0,pi/4,pi,5pi/4)`

so that the long edges are the two `pi/4` pairs. The excess is exactly

`8tan^2(pi/8)=24-16sqrt(2)<2`.                            (K4)

For exactly two adjacent long edges, put their common endpoint at zero, their
other endpoints at `3pi/8` and `13pi/8`, and the fourth vertex at `pi`. At
length three the excess is

`6tan^2(5pi/48)+tan^2(pi/8)+2tan^2(3pi/16)`
` < 6(7/60)+7/40+2(9/20)=71/40<2`.                       (K5)

The PSD property in (K3)--(K5) is exact because the matrices are explicit Gram
matrices. Fixed-parity monotonicity extends (K3)--(K5) to every longer state in
their respective long-edge classes.

## 3. Final finite cover

- Doubled triangle: the 28 ordinary physical rows use the rational parity
  ledger; class `111` uses four relabelings each of (DT2) and (DT3) whenever a
  parallel path is noncanonical, and structural deletion at the canonical
  obstruction.
- All-odd `K4`: (K3) covers all 42 subsets with at least three long edges;
  (K4) covers the three opposite two-edge subsets; (K5) covers the twelve
  adjacent two-edge subsets; six one-long subsets use deletion and the no-long
  subset is necessarily structural by the exact obstruction (K1).

These are finite templates extending to all lengths. In both kernels the
canonical doubled-triangle and unit-`K4` structural cases are forced by exact
failures of the correlation-Gram threshold. The one-long `K4` state is closed
only by its independent structural proof.
