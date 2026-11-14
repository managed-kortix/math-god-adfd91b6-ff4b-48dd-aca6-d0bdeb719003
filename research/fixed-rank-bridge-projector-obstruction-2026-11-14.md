# Fixed-rank bridge projector correction: exact theorem and obstruction

## Scope

For a real symmetric matrix `A`, write

`A_+=sum_(lambda>0) lambda uu^T`,

`Pi_+(A)=sum_(lambda>0) uu^T`, and

`s^+(A)=tr(A_+^2)`.

This note proves an exact lower bound for restoring one omitted bridge and
shows that fixed total cyclomatic rank seven gives no positive lower bound on
that particular correction.  It does **not** assert that the full bridge gain
has no lower bound, and it does not prove or refute the heptacyclic theorem.

## 1. Exact positive-projector bridge correction

Let `H,K` be vertex-disjoint graphs, let `u in V(H)`, `v in V(K)`, and let `G`
be obtained by adding the bridge `uv`.  Put

`Pi_H=Pi_+(A(H))`, `Pi_K=Pi_+(A(K))`.

Then

`s^+(G) >= s^+(H)+s^+(K)+(Pi_H)_(uu)(Pi_K)_(vv)`.             (1)

More generally, if the cross-adjacency between the two parts is `E`, then

`s^+([[A(H),E],[E^T,A(K)]])`
` >=s^+(H)+s^+(K)+||Pi_H E Pi_K||_F^2`.                       (2)

### Proof

Put `A_0=A(H) direct_sum A(K)`, `R=A(H)_+ direct_sum A(K)_+`,
`C=[[0,E],[E^T,0]]`, and `Pi=Pi_H direct_sum Pi_K`.  The variational identity

`s^+(M)=max_(X>=0) {2 tr(MX)-tr(X^2)}`                         (3)

follows by diagonalizing `M` and completing squares.  For every `Z>=0` with
`Z=Pi Z Pi`, the matrix `R+Z` is positive semidefinite.  Since `A_0 R=R^2`
and `A_0 Z=RZ` under the trace on `range(Pi)`, (3) gives

`2tr((A_0+C)(R+Z))-tr((R+Z)^2)`
` =s^+(H)+s^+(K)+2tr(CZ)-tr(Z^2)`.                             (4)

Maximizing the last two terms over positive semidefinite `Z` supported on
`range(Pi)` gives

`s^+(Pi C Pi)=||Pi_H E Pi_K||_F^2`,                            (5)

because `Pi C Pi`, restricted to the positive subspaces, has block form
`[[0,D],[D^T,0]]` with `D=Pi_H E Pi_K`; its positive eigenvalues are the
singular values of `D`.  This proves (2).  For one bridge,
`E=e_u e_v^T`, so

`||Pi_H e_u e_v^T Pi_K||_F^2`
` =||Pi_H e_u||^2 ||Pi_K e_v||^2`
` =(Pi_H)_(uu)(Pi_K)_(vv)`,                                   (6)

which proves (1).

For connected nontrivial `H,K`, both factors in (6) are positive: the Perron
unit eigenvector belongs to the positive subspace and has a nonzero coordinate
at every vertex.  This gives strictness graph by graph, but not a uniform
margin.

## 2. Exact fixed-rank obstruction family

For an integer `t>=1`, define:

* `H_t`: take `C5`, choose a vertex `a`, and attach `t` new leaves directly
  to `a`; choose one leaf as `u_t`.
* `K_t`: take `K5`, choose a vertex `b`, and attach `t` new leaves directly
  to `b`; choose one leaf as `v_t`.

These are connected simple graphs.  Tree attachment does not change
cyclomatic rank, so

`beta(H_t)=1`, `beta(K_t)=6`.                                  (7)

Consequently, adding the bridge `u_t v_t` produces a connected simple graph of
rank seven whose bridge deletion has positive-rank sides one and six.

### Equitable quotients and characteristic polynomials

For `H_t`, use the equitable cells

`{a}`, `{the two neighbors of a on C5}`,
`{the two remaining C5 vertices}`, `{the t leaves}`.

The divisor and its symmetric conjugate are

`D_H(t)=[[0,2,0,t],[1,0,1,0],[0,1,1,0],[1,0,0,0]]`,

`Q_H(t)=[[0,sqrt(2),0,sqrt(t)],`
`        [sqrt(2),0,1,0],`
`        [0,1,1,0],`
`        [sqrt(t),0,0,0]]`.

They have the same polynomial

`p_t(x)=x^4-x^3-(t+3)x^2+(t+2)x+t`.                            (8)

The orthogonal complement of the cell-constant space contributes one positive
root `(sqrt(5)-1)/2`, one negative root `-(sqrt(5)+1)/2`, and `t-1` zeros.
Thus

`chi_(H_t)(x)=x^(t-1)(x^2+x-1)p_t(x)`.                         (9)

For `K_t`, with cells `{b}`, `{the other four K5 vertices}`, `{the t leaves}`,

`D_K(t)=[[0,4,t],[1,3,0],[1,0,0]]`,

`Q_K(t)=[[0,2,sqrt(t)],[2,3,0],[sqrt(t),0,0]]`,

and

`q_t(x)=x^3-3x^2-(t+4)x+3t`.                                  (10)

The remaining directions contribute three eigenvalues `-1` and `t-1` zeros:

`chi_(K_t)(x)=x^(t-1)(x+1)^3 q_t(x)`.                          (11)

### Exact inertia

The coefficient signs of `p_t(x)` in descending order are

`+,-,-,+,+`,

so Descartes' rule gives exactly two or zero positive roots.  But

`p_t(0)=t>0`, `p_t(2)=-t<0`,

and `p_t(x)->+infinity` as `x->+infinity`; hence `p_t` has at least two
positive roots and therefore exactly two.  Applying the same argument to

`p_t(-x)=x^4+x^3-(t+3)x^2-(t+2)x+t`,

whose signs are `+,+,-,-,+`, and observing

`p_t(-1)=-(t+3)<0`, while `p_t(-(t+4))>0`,

shows that `p_t` has exactly two negative roots.  The last positivity is
immediate after expansion (all remaining terms are positive), or from the
explicit polynomial identity checked by the verifier.  It has no zero root because
`p_t(0)=t`.  Together with (9),

`inertia(H_t)=(n_+,n_-,n_0)=(3,3,t-1)`.                       (12)

For `q_t`, the signs are `+,-,-,+`, so it has two or zero positive roots.
Since

`q_t(0)=3t>0`, `q_t(4)=-t<0`, and `q_t(x)->+infinity`,

it has exactly two positive roots.  Also

`q_t(-x)=-x^3-3x^2+(t+4)x+3t`

has signs `-,-,+,+`, hence exactly one positive root by Descartes' rule.  Thus
`q_t` has exactly one negative root.  Equation (11) gives

`inertia(K_t)=(2,4,t-1)`.                                     (13)

### Leaf projector leverage

All `t` leaves in each graph are permuted transitively by automorphisms fixing
the core.  A spectral projector is a function of the adjacency matrix and
commutes with every automorphism.  Hence its diagonal is constant on the leaf
orbit.  Since the trace of an orthogonal projector is its rank, (12)--(13)
give the exact bounds

`(Pi_+(H_t))_(u_t u_t) <= 3/t`,

`(Pi_+(K_t))_(v_t v_t) <= 2/t`.                               (14)

Equivalently, in the symmetric quotient, if `e_L` denotes the normalized
leaf-orbit vector, then

`(Pi_+(H_t))_(u_tu_t)=<e_L,Pi_+(Q_H(t))e_L>/t`,

`(Pi_+(K_t))_(v_tv_t)=<e_L,Pi_+(Q_K(t))e_L>/t`;               (15)

the dark leaf subspace is the zero eigenspace.  Since a projector diagonal is
at most one, (15) also gives the sharper individual bounds `<=1/t` on both
sides.  In either form,

`0<(Pi_+(H_t))_(u_tu_t)(Pi_+(K_t))_(v_tv_t)<=1/t^2 ->0`.       (16)

Positivity in (16) follows from Perron--Frobenius, as noted after (6).

## 3. Consequence and stopping point

Equations (7) and (16) prove:

> There is no constant `c_7>0` such that the positive-positive projector
> correction in (1) is at least `c_7` for every bridge whose deletion gives
> connected positive-rank sides summing to cyclomatic rank seven.  This remains
> false in the specific split `(1,6)`, with cores `C5` and `K5` and only rooted
> tree attachments.

This is an obstruction to a **projector-correction-only** replacement for the
false both-sides-nonnegative sentence.  It says nothing adverse about the full
bridge restoration gain

`s^+(G)-s^+(H)-s^+(K)`,

which can be much larger than the lower bound (1).  A successful rank-seven
bridge proof must therefore use packet-specific surplus, fuller rooted
characteristic-polynomial/phase data, or a stronger variational witness that
also mixes positive and nonpositive spectral directions.
