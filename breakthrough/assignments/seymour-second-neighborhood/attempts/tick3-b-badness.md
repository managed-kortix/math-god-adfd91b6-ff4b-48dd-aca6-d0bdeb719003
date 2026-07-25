# Tick 3: exact extension through `B`-badness

Let `C` be the third layer, represented by its nonempty predecessor signatures
in `B`. The row bounds from `A`-badness imply `|N_C^+(b)|<=12` for every
`b in B`, hence `|C|<=72`. The complete first neighborhood of `b` is finite:

```
F_b = T_b disjoint-union J_b disjoint-union ({s} if epsilon_b)
      disjoint-union R_b,
8 <= |F_b| <= 26.
```

Represent fourth-layer vertices by nonempty predecessor signatures `U subseteq
C`, with multiplicities `q_U`. If `x in U` and `b->x`, every such vertex is an
exact second neighbor of `b`, so `q_U<=d++(b)<=25`.

For each `b`, form the raw two-walk endpoint union over the first neighbors in
`F_b`, and subtract `F_b union {b}`. The exact constraint is

```
|raw2(b) \ (F_b union {b})| = |F_b|-mu_b,  mu_b in {1,2}. (1)
```

This is finite for badness through `B`. Iterating layers is finite at every
fixed depth but does not locally bound the number of layers. The precise missing
global lemma is a bound on root eccentricity.

Seacrest's cited reduction bypasses that obstruction: a counterexample with
minimum outdegree 8 implies one on at most `binom(9,2)=36` vertices. Since our
counterexample is globally vertex-minimal, it has at most 36 vertices even if
the graph produced by the reduction does not preserve minimum degree exactly.
Thus a complete finite direct adjacency model exists for orders 17 through 36;
order at least 17 follows already from `C(n,2)>=8n`.
