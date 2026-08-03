# Positive square energy of every pentacyclic graph

`paper.tex` proves that every finite simple connected graph `G` with `n`
vertices and `n + 4` edges satisfies

```text
s+(G) >= n.
```

## Proof map

- Positive cyclic-block ranks split exhaustively as `1^5`, `2+1^3`, `2+2+1`,
  `3+1+1`, `3+2`, `4+1`, or `5`.
- The exact multiblock DNN sieve leaves four hard incidence families. The
  repaired owner-exact closure handles positive routes, repeated owners,
  direct/nested shared cuts, the doubled-C4 interior-owner orbit, all connector
  remnants, and arbitrary rooted branches.
- A single rank-five block suppresses to exactly 118 loopless no-cut-vertex
  multigraph kernels, with order counts `1,3,13,24,38,23,16` on 2 through 8
  branch vertices.
- The paper proves the DNN correlation dual and exact path elimination.
  Fixed-parity monotonicity promotes canonical and one-coordinate frontiers to
  every physical path length.
- The single-block master tables reproduce the physical-row, orbit, coarse
  sieve, rational frontier, symbolic equality, and structural packet counts
  for all seven kernel orders.
- The all-odd `K5-e` family is treated by a disjunction, not by the false
  universal excess-four claim; its optimized DNN excess is `2sqrt(7)-1 > 4`.

The multiblock owner proof is in
`positive-square-energy/pentacyclic-general/four-residual-owner-exact-closure.md`.
The 118-kernel master theorem and detailed order packages are in
`positive-square-energy/pentacyclic-general/`.

## Verify

The finite part is a computer-assisted proof, not a numerical search. Its
proof objects are the committed JSON fixtures in `research/fixtures/` and
`pentacyclic/research/`; the verifiers check them with integer and rational
arithmetic only. In outline:

```text
generate every degree partition and incidence solution -> canonical 118 kernels
generate every physical parity row -> quotient by exact kernel automorphisms
generate canonical + every one-coordinate (+2) frontier for each residual row
require generated key set == certificate key set, with no duplicates or extras
verify each rational, symbolic-equality, or structural certificate exactly
```

For rational records, stereographic unit vectors and every path step cost
`(1-u.v)/(1+u.v)` are reconstructed as `Fraction`s and the final predicate is
`numerator < 4*denominator`. Symbolic records are accepted only after all
principal Gram minors and the exact cost identity are checked. Structural
records are rebuilt as physical subdivisions and their induced territories are
validated; they are not mislabeled as DNN witnesses. Fixed-parity path
monotonicity in the paper proves that the finite canonical/frontier key set
covers arbitrary path lengths.

The verifiers fail closed on missing, duplicate, extra, malformed, reordered,
or out-of-scope records and on changed costs, Gram entries, owner registries, or
hashes. They run hostile mutation suites and compare normal with `python3 -O`
execution, so correctness does not depend on removable `assert` statements.

Run from the repository root with Python 3.10 or newer; the proof verifiers use
only the standard library:

```sh
python3 research/rank-five-kernel-census-verifier.py
python3 -O research/rank-five-kernel-census-verifier.py

python3 research/rank-five-order2-8-master-verifier.py
python3 -O research/rank-five-order2-8-master-verifier.py
```

The implication master invokes all single-block theorem owners. Individual
packages can also be audited directly:

```sh
python3 research/rank-five-low-order-master-verifier.py
python3 pentacyclic/research/order5-kernel-family-theorem-verifier.py
python3 pentacyclic/research/all-odd-k5e-theorem-verifier.py
python3 pentacyclic/research/order6-kernel-family-theorem-verifier.py
python3 pentacyclic/research/order7-kernel-family-theorem-verifier.py
python3 pentacyclic/research/order8-kernel-family-theorem-verifier.py
```

Repeat those commands with `python3 -O`. The canonical 118-kernel fixture hash
is
`027c84d6dd777a29b3dc93389ab30b5d43f6507eddceb4ea286f1240da95b884`.
The principal theorem-appendix hashes are:

```text
three-vertex orbits   e3ec57422ba2d9ca0c25ad2ba7d85b8bc74a5d656ebfe20fdb072a0688d01fa9
four-vertex sieve     0b8ded3f4dbe0b8de916c085393c5f470bbaf8961deddf4305396e15f1d45588
four-vertex frontier  09a7b38b1e9f5e18aaddc1f9e0114b8490151f2062d3f51100c52eb314eb56d2
all-odd K5-e          35523cc3be872181e2f343a7e21936f82b14e4a6968896fc2dcfd5f545da1ee1
order 5 theorem       4d8b826b397dc269c7853b8bd386d00bf469282b52720b8dac96d850e9e616d8
order 6 theorem       69b236b014aef58c037c610ca01fa62ad82601f7bb34153939ec4ddd3b5f364d
order 7 theorem       1de37116d406f72abba33f85678be9f2eba38e71347a79c67bad5f159e2f1c16
order 8 theorem       f1c08641de224194d871197454d7056eb0884c8972c535dd8daa5abd08a37a6f
```

These committed machine-readable certificates are the unabridged theorem
appendices. The paper gives the supplemental count tables and certificate
schemas instead of printing more than 100,000 repetitive rows, records the
larger source/chunk hashes, and separates executable obligations from the
analytic and graph-theoretic arguments.

## Build

```sh
bash scripts/build-paper.sh all-pentacyclic-graphs
```

This creates `all-pentacyclic-graphs/paper.pdf`. The manuscript includes a
scoped nonclaim and AI disclosure. It makes no strict global claim, no edge
monotonicity claim, and no universal DNN excess-four claim.
