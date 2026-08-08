# Dual stresses beyond the simplex-atom model

## Verdict

The SDP KKT equations do not, by themselves, imply the three known cost-five
profiles. After tight mixed pairs have been removed, the dual stress is a
doubly nonnegative matrix. Simplex-atom proofs implicitly require this stress
to be completely positive. That implication is valid only through quotient
order four and fails already on five quotient vertices.

This note gives the exact KKT reduction and the smallest obstruction: a
non-completely-positive `C5` stress exposing a non-simplex minimizer of an odd
path objective. Its objective value is `5-2 sqrt(5)`, not five, so it is not a
fourth rank-six equality row. It does show rigorously that complementary
slackness alone cannot prove three-profile exhaustion. A cost-five theorem must
add an argument excluding exceptional doubly nonnegative stresses from the
order-nine and order-ten physical ledgers.

## 1. Exact nonlinear SDP duality

Let `E` be a set of unordered pairs and let

`F(R)=sum_(ij in E) g_ij(R_ij)`,

where every `g_ij` is differentiable and convex on an interval containing the
entries under consideration. The feasible set is the elliptope

`R psd, diag(R)=1`.

For a feasible matrix `R*`, put `a_ij=g'_ij(R*_ij)` and let `C` be the symmetric
matrix with `C_ij=C_ji=a_ij/2` on `E` and zero off `E` and on the diagonal.

### Lemma 1 (stress/complementary-slackness criterion)

The matrix `R*` minimizes `F` if there is a diagonal matrix `D` such that

`S=C-D psd` and `S R*=0`.                                      (1)

Conversely, if `R*` is a minimizer and all objective terms are finite and
differentiable there, then such a `D` and `S` exist.

### Proof

Convexity gives

`F(R)-F(R*) >= <C,R-R*>`.                                    (2)

If (1) holds, then `C=S+D`. Since `R` and `R*` have the same diagonal,

`<C,R-R*>=<S,R>-<S,R*> = <S,R> >= 0`;                         (3)

the middle equality uses `S R*=0`, and the last inequality uses `S,R psd`.
Thus `R*` is globally optimal.

For the converse, minimize the linear functional `<C,R>` over the elliptope.
Equation (2) and first-order optimality show that `R*` solves this linear SDP.
The identity matrix is strictly feasible, so SDP strong duality supplies a
diagonal `D` for which `S=C-D psd`; equality of primal and dual values gives
`<S,R*>=0`. Two positive semidefinite matrices with zero trace product satisfy
`S R*=0`. `QED`

Strict convexity gives one further useful conclusion when an optimum exists:
if every `g_ij` is strictly convex, every minimizer has the same entries
`R_ij` on `E`, although unspecified completion entries can still vary.

## 2. What the sign pattern gives

For an odd unit path,

`f(r)=(1+r)/(1-r),    f'(r)=2/(1-r)^2>0`.                    (4)

Consequently the stress in Lemma 1 has nonnegative off-diagonal entries. Its
diagonal entries are nonnegative because it is positive semidefinite. Hence

`S psd` and `S>=0` entrywise: `S` is doubly nonnegative.       (5)

A tight mixed odd/even pair contributes the scalar inequality

`f_1(r)+f_2(r)>=1`,

with equality at `r=-1/2`. Its derivative vanishes there, so a tight mixed
pair contributes no off-diagonal coefficient to the residual matrix stress.
Thus (5) is exactly the matrix object left after extracting individually tight
mixed pairs and signed contractions.

A regular-simplex tangent proof has a stronger property. Its stress is a
positive multiple of `11^T` on the simplex vertices. Sums of such packet
stresses are **completely positive**:

`S=sum_k z_k z_k^T` with every `z_k>=0`.                      (6)

The supports of the `z_k` are cliques in the nonzero graph of `S`, because a
zero entry `S_ij` forces `(z_k)_i (z_k)_j=0` for every `k`. Therefore the
simplex-atom model is naturally a completely-positive factorization model,
not merely a consequence of positive semidefiniteness.

## 3. The five-cycle obstruction

Let `A` be the adjacency matrix of the five-cycle, let

`phi=(1+sqrt(5))/2`,

and define

`S=I+(1/phi) A`.                                              (7)

### Lemma 2

The matrix `S` is doubly nonnegative but not completely positive.

### Proof

The eigenvalues of `A` are `2 cos(2 pi k/5)`, `0<=k<5`. The least is `-phi`,
so every eigenvalue of (7) is nonnegative and two are zero. Entrywise
nonnegativity is immediate.

Suppose (6) held. Since `S_ij=0` on every nonedge of `C5`, each `z_k` would be
supported on a clique of `C5`, hence on one edge or one vertex. For a vector
supported on edge `ij`,

`(z_k)_i^2+(z_k)_j^2 >= 2 (z_k)_i (z_k)_j`.

Summing over all factors (with singleton factors contributing only to the left)
would give

`tr(S) >= 2 sum_(ij in E(C5)) S_ij`.                          (8)

But the two sides are `5` and `10/phi`, and `10/phi>5`. This contradicts
(8). `QED`

The obstruction is not merely an abstract stress. Let `u_0,...,u_4` be unit
vectors in the plane at successive angles `4 pi/5`, and let `R` be their Gram
matrix. Thus

`R_ij=cos(4 pi(i-j)/5)` and `R_(i,i+1)=-phi/2`.               (9)

The columns of `R` lie in the two-dimensional nullspace of `S`, so `S R=0`.
The tangent of (4) at `rho=-phi/2`, together with Lemma 1 (after scaling `S`
by the positive derivative `f'(rho) phi/2`), proves

`sum_(ij in E(C5)) f(R_ij) >= 5 f(-phi/2)=5-2 sqrt(5)`,       (10)

with equality at (9). Strict convexity forces correlation `-phi/2` on every
cycle edge at every minimizer.

For completeness, the scaling is exact: if

`T=(f'(rho) phi/2) S`,

then `T_ij=f'(rho)/2=C_ij` on cycle edges and `T_ij=0=C_ij` on nonedges.
Thus `T=C-D` with the diagonal matrix

`D=-(f'(rho) phi/2) I`,

which is precisely the certificate required in Lemma 1.

Thus (9) is an exact exposed nonlinear-SDP minimizer whose dual stress cannot
be partitioned into nonnegative rank-one clique stresses. It is the smallest
concrete geometry missed by the simplex-atom interpretation of complementary
slackness.

## 4. Consequence for cost-five classification

Equation (10) is irrational and is not a cost-five rank-six ledger. In
particular, adjoining any integer number of tight mixed pairs cannot turn it
into value five. Therefore this note neither proves a fourth cost-five support
row nor refutes three-profile exhaustion for the actual order-nine/order-ten
row universe.

It does isolate a necessary missing lemma. Any proof based only on dual stress
and complementary slackness must establish at least one of the following for
every putative cost-five row:

1. the residual doubly nonnegative stress is completely positive, with factors
   forced to be the regular `K3` and `K4` packet stresses;
2. its nonzero graph is in a class for which doubly nonnegative implies
   completely positive, after the physical contractions and tight mixed pairs;
3. every exceptional non-completely-positive stress has objective value
   different from five or is incompatible with the rank-six degree and path
   multiplicity ledger.

The quotient orders in the three known profiles are already at least five, so
the general identity `DNN=CP` in matrix order at most four cannot close this
gap. The exact five-cycle stress (7) is the hostile test that any proposed
analytic exhaustion argument must defeat.
