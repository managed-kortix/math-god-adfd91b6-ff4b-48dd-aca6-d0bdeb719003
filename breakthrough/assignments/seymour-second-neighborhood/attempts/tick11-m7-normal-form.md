# Tick 11: order 18 with seven missing pairs

Exactly two vertices `r,q` have outdegree nine and the other sixteen have
outdegree eight. Every high vertex has a robust deletion witness, and at least
one of these witnesses has degree eight.

Fix a degree-eight robust witness `v->r`. Then

```
A=N+(v), |A|=8; B=N++(v), |B|=7; C has size 2; r in A.
```

Let `epsilon=1[q in C]`, `rho=e(C,B)`, and let `K` count missing pairs in
`C-A`, `C-{v}`, and inside `C`. Exact degree counting gives

```
K=3+rho-epsilon,                                      (1)
h(A)+h(B)+h(A,B)+h(B,C)+h(v,B)+rho=4+epsilon.        (2)
```

The second high vertex lies in one of `A,B,C`, producing three finite location
classes. For each `c in C`, if `a_c` counts missing pairs to `A union {v}` and
`delta_c` is its outgoing internal-C indicator, then

```
e(c,B)=x(c)+a_c-1-delta_c.                            (3)
```

The A-to-B incidence count is exact:

```
e(A,B)=36+x(A)+h(A),                                  (4)
```

and every B-column hit by `r` has a second A-predecessor by robustness. These
identities reduce the case to finite two-row ledgers but do not yet contradict
badness. Simultaneous compatibility of robust witnesses into both high vertices
is the next unexplored constraint.
