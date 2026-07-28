# Tick 46: exact k=6 frontier and rejected sourcewise bound

In the final row `(rho,k)=(0,6)`, every B vertex dominates both C vertices. Let
`P=union_{b in B}(N-(b) intersect A')`.
Every `a in A'` must have a B-outneighbor: `w->a`, no A vertex points to C,
and only seven other A vertices are available, while `d+(a)=8`. Hence the
common-dominator predecessor union is exactly

```
P=A', |P|=7.                                         (1)
```

Exact A' degree sums and the z row give

```
e(A',B)=29+h(A')+Q,                                 (2)
```

where `h(A')` counts holes internal to A' and `Q=|{b in B:b->z}|`. Thus at
least 29 A'-to-B arcs are required.

For every source a, put `S_a={a} union N_T+(a)`, let `J_a` be the full set of
vertices in `T\S_a` inaccessible by a T-two-walk, let
`R_a=T\(S_a union J_a)`, and let `q_a(t)` count T-holes from t into S_a.
Badness gives `|J_a|>=2`. Exact degree
and the fact that an inaccessible B vertex already dominates both C vertices
yield

```
sum_{t in J_a} q_a(t)+e_h(J_a)
 = |J_a|+C(|J_a|,2)+e+(J_a,R_a)+2|J_a intersect B|.
```

Since only six holes exist, `|J_a|` is two or three; a triple avoids B and uses
all six holes, while a pair contains at most one B vertex and uses at least
three holes (at least five if it contains B).

An attractive claimed shortcut, `d_B+(a)<=4` for each bad A' source, failed in
temporary tests: a one-source relaxed model reportedly had five B-outneighbors
and `d++=7`, with an inaccessible A' pair sharply supported by three holes. No
reproducible witness artifact was retained, so this remains an unverified
breaker observation. If reproduced, it refutes that uniform cap and its direct
summation proof, not every possible sourcewise route. Temporary runs also
reportedly found every six-row badness subset satisfiable, but no durable
certificate supports a conclusion about the full seven-row obstruction.

The durable next lemma must therefore be genuinely multi-source:

> **Target lemma.** Seven simultaneously realized closed source rows, all bad and sharing one
> six-hole graph, are incompatible with the exact rooted A'/B row equations.

Packet loads cannot simply be summed because one physical hole may support
several sources. A tentative arc-minimal charging route also appears vulnerable
to gain cycles, but this has not been preserved as a reproducible theorem or
breaker. Any proof must control shared packet compatibility. This note records
a structural frontier, not an elimination of k=6.
