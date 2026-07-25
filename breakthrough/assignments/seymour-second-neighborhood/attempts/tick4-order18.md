# Tick 4: exact order-18 compression

For an 18-vertex oriented graph of minimum outdegree 8, let `m` be the number
of missing unordered pairs and `x(v)=d+(v)-8`, `X=sum_v x(v)`. Arc counting
gives

```
X+m=9.                                                   (1)
```

Thus at least `9+m` vertices have outdegree exactly 8. Fix one such root `v`,
put `A=N+(v)`, `B=N++(v)`, and let `C` be the remaining vertices. Since `v` is
bad, `|C|>=2`. Counting outgoing arcs of `C`, with `m0` the missing pairs in
`C-A`, `C-{v}`, and inside `C`, gives the exact budget

```
9 = |C| + binom(|C|,2) + e(C,B) + X_outsideC + m_outside0. (2)
```

Therefore `|C| in {2,3}`, recovering root deficits one or two directly.

For `|C|=3` (`|B|=6`),

```
e(C,B)+X_outsideC+m_outside0=3,
e(B,C)>=15,
36 <= e(A,B) <= 39-e(C,B).
```

This tiny exact budget should replace broad local-layer variables in the
order-18 branch. The analogous `|C|=2` budget has seven units of slack and is
the harder branch.

The direct SMT model now branches on the exact number of missing pairs and
includes degree upper bounds and root signature implications. It returned
`unsat` for both root branches at `m=0`, and for `|B|=6` at `m=1,2`; the
`|B|=7,m=1,2` runs timed out. These solver statuses are experimental only and
are not proof certificates.
