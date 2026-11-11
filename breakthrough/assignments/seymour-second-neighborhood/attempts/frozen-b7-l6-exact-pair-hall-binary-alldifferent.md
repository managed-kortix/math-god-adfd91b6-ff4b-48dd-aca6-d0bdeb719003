# Frozen B7-l6 Hall binary all-different extension

## Scope and ancestry

This layer applies only to the ordered 33 exact-pair singleton memberships in
the committed Hall campaign. Its ancestry is the committed all33 verifier,
which checks the 29 direct Hall-failure LRATs and the exhaustive seven-way
cardinality splits for the other four memberships. Consequently every graph in
this layer satisfies Hall's condition for the fixed bipartite graph with the
seven vertices `U` on the left, the ordered eight vertices `S=N+(low C)` on the
right, and edge `u--S[i]` exactly when the original arc `S[i]->u` is present.

The new manifest binds the all33 verifier and both Hall certificate ledgers by
byte count and SHA-256. This is certificate-relative: without that ancestry the
extension-existence statement is not available.

## Encoding

For each `u in U`, three variables encode an integer `f(u)` in `0..7`; all eight
three-bit words are valid and value `i` denotes `S[i]`. For every `i`, the
channel clause

```text
f(u) != i OR a_S[i]_u
```

requires the selected value to be an actual bipartite edge. One redundant
eight-literal row-support clause per `u` states that some `S[i]->u` is present;
it follows from Hall's singleton condition but preserves the requested exact
dimension. For every unordered pair `{u,v}` and every bit, an exact four-clause
XOR variable records whether the two bits differ; a three-literal ALO requires
at least one difference.

There are `7*3 + C(7,2)*3 = 84` variables. There are `7*8=56` channel clauses,
seven row-support clauses, and `C(7,2)*(3*4+1)=273` disequality clauses, for
exactly 336 clauses.

## Exact extension theorem

Let `G` be any graph admitted by one of the 33 Hall-synchronized memberships.
The committed Hall ancestry proves `|Gamma(K)|>=|K|` for every `K subset U`.
By Hall's marriage theorem there is a matching saturating `U`; write its matched
right endpoint as `S[f(u)]`. Assign the three bits of `u` to the binary expansion
of `f(u)`. Every channel clause holds because each matched pair is an edge. For
each pair of left vertices, matching injectivity gives distinct three-bit words;
assign each XOR variable to the exact bit inequality, satisfying its four-clause
equivalence and the pair ALO. Row support follows from the matched edge. Thus
every Hall-synchronized graph has a satisfying extension.

Conversely, take any satisfying extension. Three bits decode a unique value
`f(u) in 0..7`. The corresponding channel clause has all three mismatch literals
false, so `a_S[f(u)]_u` is true. The four XOR clauses make each difference
variable exact, and each pair ALO therefore implies `f(u) != f(v)`. Hence `f` is
an injection from `U` into `S`, and every selected pair is an original arc. Every
extension is therefore a valid saturating matching.

The independent checker reconstructs the complete CNF without importing the
producer. Its small-domain audit exhausts 294 incidence graphs and 4,234 value
assignments, directly comparing Hall subsets, maximum matching, extension
existence, and decoded injection validity. A separate Hall graph whose unique
matching uses value 7 proves that forbidding binary word `111` would be unsound.

## Scout result and stopped certificate gate

Pinned CaDiCaL 1.7.3 with `--restart=false --phase=false --seed=3`, eight jobs,
and 30 seconds per membership returned 33 TIMEOUT, zero UNSAT, and zero SAT for
the sound encoding. Therefore the requested expected result of eight UNSAT
memberships `024,028,033,034,064,069,070,075` was not reproduced, and the robust
gate for generating LRATs did not pass. No LRAT or certificate ledger was made.

The source of the expectation was identifiable: the temporary benchmark that
reported eight UNSAT added `-b0 OR -b1 OR -b2` for every `u`, thereby forbidding
value 7 while describing values `0..7`. Removing that invalid restriction and
using the Hall-entailed row-support clauses keeps the exact `+84/+336` dimensions
but changes the scout to 33 TIMEOUT. Retaining the benchmark clause would fail
the extension theorem, as the independent value-7 counterexample demonstrates.

Run from `experiments/`:

```sh
python3 check_m6_b7_l6_exact_pair_hall_binary_alldifferent.py --cover --semantic --excluded-value-counterexample --scout
python3 test_m6_b7_l6_exact_pair_hall_binary_alldifferent.py
```

This layer proves an exact certificate-relative matching-extension encoding. It
does not prove any of the 33 underlying memberships UNSAT and makes no broader
B7, order-18, or Seymour claim.
