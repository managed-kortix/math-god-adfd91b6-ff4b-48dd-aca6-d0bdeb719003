# Exact averaged positive-part witness for hostile unit stars

Date: 2026-11-21. Status: **proved variational certificate; not a closure of the hostile unit-star remainder**.

For a real symmetric matrix `M`, write

```text
Phi(M)=tr(M_+^2),
q_M(X)=2 tr(MX)-tr(X^2)       (X positive semidefinite).
```

The positive part `M_+` is the unique maximizer in

```text
Phi(M)=max_{X positive semidefinite} q_M(X).                 (1)
```

## 1. Weighted barycentre identity

### Theorem 1

Let `X_1,...,X_k` be positive semidefinite matrices of the same size, and let
`w_i>=0`, `sum_i w_i=1`. Put

```text
Xbar=sum_i w_i X_i,
V_w=sum_i w_i ||X_i-Xbar||_F^2.
```

Then `Xbar` is positive semidefinite and

```text
q_M(Xbar)=sum_i w_i q_M(X_i)+V_w,                            (2)
V_w=sum_{i<j} w_i w_j ||X_i-X_j||_F^2.                      (3)
```

Consequently

```text
Phi(M)>=sum_i w_i q_M(X_i)+V_w.                             (4)
```

**Proof.** The variance identity gives

```text
sum_i w_i tr(X_i^2)=tr(Xbar^2)+V_w.
```

The linear terms average exactly, so substitution in `q_M` proves (2).
Expanding the pairwise squares proves (3). Equation (4) follows from (1).
`QED`

No disjoint-support hypothesis occurs in this theorem. In particular, shared
central vertices cause no algebraic problem: they occur once in the common
ambient matrix and are averaged, not duplicated.

## 2. Exact graph-cut specialization

Let `G` be any finite graph, `M=A(G)`, and let `U_i` be vertex sets such that
there is no edge between `U_i` and `R_i=V(G)\U_i` after deleting a specified
set of crossing edges. In the physical unit-star application, `U_i` is the
whole original-vertex territory of arm `i` (including whichever bridge-chain
vertices are assigned to that side), and the crossing set is its one physical
bridge. Thus `U_i,R_i` are disjoint, exhaustive sets of original vertices;
central vertices belong only to `R_i` for that cut.

Put

```text
D_i=A(G[U_i]) direct_sum A(G[R_i]),
X_i=(D_i)_+,
sigma(H)=Phi(A(H))-|V(H)|.
```

Embed each `X_i` in the common original-vertex order of `G`. Since `M-D_i`
is supported only on crossing blocks while `X_i` is block diagonal,
`tr((M-D_i)X_i)=0`. Hence

```text
q_M(X_i)=q_{D_i}(X_i)=Phi(D_i)
        =|V(G)|+sigma(G[U_i])+sigma(G[R_i]).                 (5)
```

Combining (4) and (5) proves the exact weighted certificate

```text
sigma(G)>=sum_i w_i [sigma(U_i)+sigma(R_i)] + V_w.           (6)
```

Equivalently, if

```text
Gamma_i=Phi(M)-Phi(D_i),
```

then

```text
sum_i w_i Gamma_i >= V_w.                                   (7)
```

The instance is certified whenever the right side of (6) is nonnegative.
For hostile unicyclic arms, writing `d_i=-sigma(U_i)>0`, and using only the
known rank-six floors `sigma(R_i)>=0`, the remaining sufficient condition is

```text
V_w >= sum_i w_i d_i.                                       (8)
```

With uniform weights,

```text
V=(1/k)sum_i ||X_i-Xbar||_F^2
 =(1/k^2)sum_{i<j} ||X_i-X_j||_F^2.                         (9)
```

The certificate is sound for overlapping complements because all matrices
are embedded on the same original vertices. It does not license summing
several owners that duplicate a center.

### Exact optimal weights for a fixed finite instance

Let `b_i=sigma(U_i)+sigma(R_i)` and
`d_ij=||X_i-X_j||_F^2`. The strongest certificate obtainable from these
specific cut optimizers is

```text
max { sum_i w_i b_i + sum_{i<j} w_i w_j d_ij :
      w_i>=0, sum_i w_i=1 }.                                (10)
```

This is an exact finite concave quadratic program because squared Euclidean
distance matrices are conditionally negative semidefinite. Formula (10) is
an instance certificate, not a rank-only theorem.

## 3. Sharp obstruction to closure by this identity alone

There is no arm choice and hence no averaging when `k=1`. Then `V_w=0`, and
(6) reduces exactly to the already known single-cut bound

```text
sigma(G)>=sigma(U_1)+sigma(R_1).                            (11)
```

The inherited unit-star residue explicitly permits `k=1`: one hostile
rank-one component joined by a bridge chain to a bridge-free rank-six
component. Therefore Theorem 1, without an additional quantified theorem for
`sigma(R_1)` or the actual bridge gain, cannot close the full hostile
unit-star remainder. This is an exact structural obstruction, not a numerical
counterexample to the target graph inequality.

Even for `k>=2`, (8) is an additional analytic obligation; (2) supplies the
variance term exactly but gives no universal lower bound on it. A finite exact
interval verifier in `verify_obstruction.py` records a small graph (two `C5`
arms attached to the center of a `K_{1,3}` zero-rank tree) for which the
**uniform** two-cut certificate is strictly negative. This graph is a
rank-two analogue rather than a rank-seven inherited state, so it only
refutes a structure-free claim that multiple hostile arms automatically make
the barycentre certificate nonnegative. It is not a counterexample to the
positive-square-energy conjecture and is not used in the `k=1` obstruction.

## 4. Exact scope

The theorem closes every concrete unit-star instance for which (6), or the
optimized form (10), is certified nonnegative. It proves no rank-only
subfamily closure beyond that check. In particular, it does not prove (8)
from hostility, arm count, bridge-chain ownership, or the rank-six theorem.
A global closure still needs a quantitative lower bound tying `V_w`, the
rank-six reserves `sigma(R_i)`, and the hostile deficits, or a separate
single-arm marked bridge theorem for the allowed `k=1` state.
