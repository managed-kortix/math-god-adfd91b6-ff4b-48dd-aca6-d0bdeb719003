# Low-order rank-five kernel theorem

## Theorem

Let `B` be a finite simple subdivision of a loopless no-cut-vertex
multigraph `K` with minimum degree at least three, cyclomatic rank five, and
at most four vertices. Then

`kappa(B) <= |E(B)|+4`.

Consequently, if `G` is obtained from `B` by attaching arbitrary rooted trees
at arbitrary vertices, then

`s^+(G) >= |V(G)|`.

If `K` has two vertices, the first inequality is strict, and hence so is the
spectral conclusion.

## Exact kernel selection

The frozen rank-five classification fixture contains exactly

`1 + 3 + 13 = 17`

kernels of orders two, three, and four. In its canonical order these are
fixture row 1, fixture rows 2--4, and fixture rows 5--17 (called kernels 4--16
by the local numbering in the four-vertex artifacts). Their upper
triangle multiplicity codes are selected directly from
`research/fixtures/rank-five-kernels.json` and compared with an independently
frozen exact low-order selection in the master verifier.

## Proof synthesis

For two vertices, `K` is the six-dipole. The six-path theorem eliminates all
six paths exactly and proves that their DNN excess is strictly less than four
for every positive length vector allowed by simplicity. This covers the sole
order-two kernel.

For three vertices, the exact physical-orbit theorem treats bundle
multiplicities `(1,2,4)`, `(1,3,3)`, and `(2,2,3)`. It reconstructs 98
physical parity rows, quotients them into 74 genuine automorphism orbits, and
supplies an exact rational correlation Gram certificate of excess at most four
on every orbit. Fixed-parity path monotonicity gives every simple subdivision.

For four vertices, the tetrahedral sieve reconstructs all 1281 physical rows
of all 13 kernels and their 821 genuine automorphism orbits. It certifies 808
orbits and leaves exactly 13 residual orbits. The residual-frontier theorem
checks the selected 117-element frontier covering set: for each residual it
selects the canonical vector and all eight one-coordinate-plus-two vectors.
The selected targets carry 116 strict rational path-vector certificates and
one exact symbolic equality certificate. Fixed-parity path
monotonicity closes every residual. Thus the sieve and frontier compose to
cover all 821 orbits, rather than either artifact being promoted beyond its
stated scope.

These cases exhaust the exact `1+3+13` low-order fixture selection and prove
the DNN bound. A rank-five subdivision with `L` edges has `L-4` vertices.
After attaching rooted trees with `t` total edges, one-vertex-sum additivity
gives `kappa(G)<=L+4+t`, while `|E(G)|=L+t` and `|V(G)|=L-4+t`. Therefore

`s^+(G)=2|E(G)|-s^-(G) >= 2|E(G)|-kappa(G) >= |V(G)|`.

## Master audit

Run both modes:

```text
python3 research/rank-five-low-order-master-verifier.py
python3 -O research/rank-five-low-order-master-verifier.py
```

The master digest-locks and selects the exact 17 fixture rows, checks the
six-path analytic proof ledger, invokes the three-vertex verifier and both
four-vertex verifiers, enforces the sieve/frontier composition, rejects
hostile registry, scope, fixture-selection, and analytic-ledger mutations, and
requires byte-identical normal and optimized output. The executable analytic
ledger audits the finite case split and exact arithmetic quoted by the
six-path proof; it does not replace its convexity, path-elimination, or DNN
duality arguments.
