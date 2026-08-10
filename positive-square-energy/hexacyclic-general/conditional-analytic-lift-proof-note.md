# Conditional analytic lift: finite frontier to subdivisions and rooted trees

## Scope

This note proves one implication only. Let `K` be a loopless 2-connected
multigraph of cyclomatic rank six and minimum degree at least three. Replace
each physical edge by a positive-length path, with distinct replacement paths
having disjoint interiors and meeting only at their prescribed endpoints. The
resulting core `B` and the final graph must be finite and simple.

Assume an exact finite ledger covers every physical parity orbit. An orbit is
owned either by one coarse certificate that stays within DNN excess five under
all same-parity lengthenings, or by exact certificates for

```text
F(c) = {c} union {c+2e_i : 1 <= i <= p},
```

where `c` is the canonical simple length vector and `p` is the number of
physical kernel edges. Assume the checked owner keys are a disjoint exact cover
of the regenerated target keys. Under precisely this premise, every simple
subdivision of `K`, with arbitrary finite rooted trees attached at branch or
internal subdivision vertices, satisfies `s+(G) >= |V(G)|`.

This is conditional analytic glue. It does not establish the finite premise,
complete any kernel order, cover multiple cyclic blocks, or assert a theorem
about all connected hexacyclic graphs.

## Canonical domination and the finite frontier

In a parallel class of multiplicity `m` with `o` odd paths, order the physical
edges so that the canonical simple lengths are

```text
o = 0: (2,...,2),
o > 0: (1,3,...,3,2,...,2).
```

There are `o` odd entries in the second row. Simplicity permits at most one
length-one path between the same branch vertices. Thus, after permuting
indistinguishable physical edges, every simple realization `l` in the orbit
satisfies `c <= l` coordinatewise and every difference is even.

If `l=c`, use the canonical owner. Otherwise choose an `i` with
`l_i >= c_i+2`; then `c+2e_i <= l`. The corresponding coordinate-frontier
owner is therefore a valid starting witness. This choice is why a residual
canonical target alone is insufficient.

## Fixed-parity path lift

For endpoint correlation `r`, exact elimination of a path of length `j` gives
minimum excess

```text
f_j(r) = j tan^2(acos((-1)^j r)/(2j)).
```

At fixed parity put `beta=acos((-1)^j r)` and `z=beta/(2j)`. Differentiation
with respect to positive real `j` gives a nonnegative prefactor times
`sin(z)cos(z)-2z`. For `0 <= z < pi/2`,
`sin(z)cos(z) <= z <= 2z`, so this derivative is nonpositive. Endpoint cases
follow by one-sided limits. Hence `f_(j+2)(r) <= f_j(r)`.

Retain the branch vectors of the selected frontier witness. On each path that
must be lengthened, discard its internal vectors and install an optimal
equal-angle chain. Different paths use mutually orthogonal auxiliary
subspaces. Every path excess weakly decreases, including when several
coordinates are lengthened. Consequently the finite premise implies

```text
kappa(B) <= |E(B)| + 5
```

for every arbitrary-length simple subdivision in the owned parity orbit.

## Rooted trees and spectral conclusion

Write `L=|E(B)|`. Rank six and connectedness give `|V(B)|=L-5`. For a genuine
one-vertex sum, restriction of correlation matrices gives one inequality for
`kappa` additivity; gluing Gram representations with orthogonal complements
gives the reverse inequality. A tree with `t` edges has `kappa=t`, attained by
opposite vectors on its bipartition classes.

Attach arbitrary finite rooted trees, each meeting the graph already built
only at its root, and let their total edge count be `t`. Roots may be branch
vertices or internal subdivision vertices. Repeated one-vertex additivity gives

```text
kappa(G) <= L + 5 + t,
|E(G)| = L + t,
|V(G)| = L - 5 + t.
```

Using `s-(G) <= kappa(G)` and
`s+(G)+s-(G)=tr(A^2)=2|E(G)|` for a finite simple graph,

```text
s+(G) >= 2(L+t) - (L+5+t) = L-5+t = |V(G)|.
```

No graph contraction, parity-changing subdivision, or spectral subdivision
monotonicity is used. A connector meeting the core twice is not a rooted-tree
attachment and lies outside this implication.

## Machine-readable companion

`research/rank-six-conditional-analytic-lift-manifest.json` records this exact
conditional scope. `research/rank-six-conditional-analytic-lift-verifier.py`
checks its canonical ASCII encoding, pins this note by SHA-256, verifies the
integer and symbolic affine identities above, rejects nearby scope widenings,
and requires byte-identical normal and `python3 -O` output.
