# Low-order rank-six kernel theorem

## Theorem

Let `B` be a finite simple subdivision of a loopless no-cut-vertex multigraph
`K` with minimum degree at least three, cyclomatic rank six, and at most four
vertices. Then

`kappa(B)<=|E(B)|+5`.

Consequently, if `G` is obtained from `B` by attaching arbitrary rooted trees
at arbitrary vertices, then

`s^+(G)>=|V(G)|`.

For the unique two-vertex kernel both inequalities are strict.

## Exact scope

The canonical rank-six fixture contains exactly `1+4+26=31` kernels of orders
two, three, and four. The order-two kernel is the seven-dipole. Its complete
analytic elimination is given in `seven-path-dnn-theorem.md` and has strict DNN
excess below five for every simple length vector.

For order three, the four bundle triples are `(1,2,5)`, `(1,3,4)`, `(2,2,4)`,
and `(2,3,3)`. Their `36+40+45+48=169` physical parity rows form
`36+40+30+30=136` genuine automorphism orbits. Every orbit has an exact
rational correlation-Gram certificate of canonical excess at most five.

For order four, the 26 kernels have 3652 physical parity rows and 2564 genuine
automorphism orbits. A regular-tetrahedron rational Gram sieve certifies every
orbit at budget five; there is no residual frontier.

Fixed-parity path monotonicity extends the canonical length bounds to every
simple subdivision. If the subdivision has `L` edges, it has `L-5` vertices.
After rooted trees with `t` edges are attached, one-vertex-sum additivity gives
`kappa(G)<=L+5+t`, while `|E(G)|=L+t` and `|V(G)|=L-5+t`. Therefore

`s^+(G)=2|E(G)|-s^-(G)>=2|E(G)|-kappa(G)>=|V(G)|`.

## Exact audit

Run both modes:

```text
python3 research/rank-six-low-order-master-verifier.py
python3 -O research/rank-six-low-order-master-verifier.py
```

The verifier digest-locks the canonical kernel fixture and analytic proof,
selects the exact 31 kernels, independently reconstructs every physical row
and automorphism orbit, checks every rational Gram matrix and cost, and rejects
hostile scope and ledger mutations.
