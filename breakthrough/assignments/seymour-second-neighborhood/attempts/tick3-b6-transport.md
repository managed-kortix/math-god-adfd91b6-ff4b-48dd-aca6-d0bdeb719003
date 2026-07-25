# Tick 3: `|B|=6` transport inequalities and sharp barriers

Let `P_b={a in A:a->b}`, put `P=sum_b |P_b|`, and let `e=e(D[A])`.
The root row degrees give `e+P>=64`, hence `P>=36`.

## Proved Hall expansion

For every nonempty `S subseteq B`,

```
|union_{b in S} P_b| >= |S|.                              (1)
```

For `|S|=1`, this is strengthened to 2 by the no-singleton root signature
lemma. For `2<=s=|S|<=5`, if the union has size `u`, then

```
36 <= P <= s*u + 8(6-s),
```

which gives the required bound. For `s=6`, every `a` lies in some `P_b`, since
otherwise its internal outdegree would be at least 8 in an eight-vertex
oriented graph.

Let `m_S` be the number of exterior vertices with exact predecessor signature
`S`, and define

```
E_BR = sum_S |S| m_S,
M    = sum_{a in A} |X_R(a)|.
```

Boundary degree capacity gives

```
E_BR >= P-21,                                           (2)
```

because at most `48-P`, 15, and 6 boundary arcs can point respectively to
`A`, inside `B`, and to `s`. By (1),

```
M = sum_S m_S |union_{b in S}P_b| >= E_BR >= P-21 >=15. (3)
```

If `L` is the total non-exterior exact-second contribution for `A` and each
deficit `mu_a` is 1 or 2, exact badness yields

```
L+M=e+P-sum_a mu_a,
L <= e+21-sum_a mu_a <= e+13.                          (4)
```

## Sharpness / failure compression

The scalar route cannot close without a new structural lower bound on `L-e`.
Strict Hall expansion is false: signatures
`P_1=P_2={a_1,a_2}` and `P_3=...=P_6=A` have `P=36` and equality in (1) for
`S={b_1,b_2}`. This also makes the coefficient in `M>=E_BR` sharp. Boundary
orientation capacity can attain `E_BR=P-21`. An integer ledger satisfying all
aggregate equations is

```
e=28, P=36, sum mu_a=16, E_BR=M=16, L=32.
```

Therefore future human inequalities must exploit overlap/orientation details
inside the exact sets `X_A,X_B`, not only aggregate edge and signature counts.
