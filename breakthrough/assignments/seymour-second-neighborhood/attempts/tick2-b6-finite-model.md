# Tick 2: exact finite `|B|=6` A-badness projection

Assume a counterexample chosen first with minimum vertices and then minimum
arcs, `delta+=8`, root `s`, `A=N+(s)` of size 8, and `B=N++(s)` of size 6.

For `a in A` define

```
I_a = N+(a) cap A,
Q_a = N+(a) cap B.
```

Every outneighbor of `a` lies in `A union B`, so
`N+(a)=I_a disjoint-union Q_a`. For `b in B` define

```
T_b = N+(b) cap A,
J_b = N+(b) cap B,
epsilon_b = 1[b->s],
R_b = N+(b) \ (A union B union {s}).
```

Then the exact second neighborhood of `a` is the disjoint union of

```
X_A(a) = (union_{c in I_a} I_c union union_{b in Q_a} T_b)
         \ (I_a union {a}),
X_B(a) = (union_{c in I_a} Q_c union union_{b in Q_a} J_b) \ Q_a,
X_s(a) = {s} iff some b in Q_a has epsilon_b=1,
X_R(a) = union_{b in Q_a} R_b.
```

Thus badness of every `a` is exactly

```
|X_A(a)|+|X_B(a)|+1[X_s(a) nonempty]+|X_R(a)|
 <= |I_a|+|Q_a|-1.                                      (1)
```

## Finite exterior signatures

For each nonempty `S subseteq B`, let `m_S` count exterior vertices whose set
of predecessors in `B` is exactly `S`. Then

```
|X_R(a)| = sum_{S: S intersects Q_a} m_S.                (2)
```

There are 63 variables. They are bounded without an assumed completion lemma:
if `b in S`, choose `a->b` (every `b in B` has such a predecessor). Every
vertex counted by `m_S` is an exact second neighbor of `a`, and

```
m_S <= d++(a) <= d+(a)-1 <= (7+6)-1 = 12.               (3)
```

Minimum outdegree for each boundary vertex is exactly represented by

```
|T_b|+|J_b|+epsilon_b+sum_{S containing b} m_S >= 8.    (4)
```

Together with orientation consistency, the tick-1 root constraints, and
(1)--(4), this is a finite forward-sound model for all `A`-badness and boundary
outdegree constraints. Vertices with empty predecessor signature are invisible
to this projection and may remain unbounded; therefore this is not yet a finite
model of the whole counterexample or of badness for `B`.

## Small adversarial partial obstruction

Let `A=Z_8`, orient `i->i+1,i+2`, and put `a->b` for every `a in A,b in B`.
With no outgoing boundary arcs, every `a` has `d+=8` and
`N++(a)={a+3,a+4}`, so all `A` vertices are bad. The 16 arcs in `D[A]` are the
minimum possible under six universal `B` outneighbors. This projection fails
only because boundary vertices have outdegree zero. It demonstrates exactly why
root row constraints alone are far from contradictory.

## Decision

The exterior multiplicities relevant to `A` are bounded; the next computation
should encode (1)--(4) exactly and either produce a complete boundary-feasible
local obstruction or prove this branch infeasible. Any feasible output must
then be extended with exact badness constraints for `B`; local feasibility is
not a counterexample.
