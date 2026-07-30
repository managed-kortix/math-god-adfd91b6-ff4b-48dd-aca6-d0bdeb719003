# Prompt - all cyclomatic-rank-thirteen cacti

## Exact target

Prove that every connected cactus `G` of cyclomatic rank `13` satisfies

```text
s+(G) > |V(G)|.
```

The exact sharp-DNN frontier consists precisely of

```text
T^12Q,
T^11PP,
```

where `T=C3`, `P=C5`, and `Q=C_q`, `q>=3`.

## Victory

Victory requires an exhaustive synthesis of the DNN-positive region and both
residual families. Invoke the existing all-rank hostile and nonhostile one-cycle
theorems for `T^12Q`, with complementary parity scopes and arbitrary shared
cuts, bridges, and trees. Invoke the existing all-rank two-pentagon theorem for
`T^11PP`, again with its full topology and attachment scope. Check that no
finite-rank or hidden incidence hypothesis is introduced.

The proof object must include the exact frontier note and fail-closed verifier,
matching normal and `python3 -O` output, frozen certificate and file digests,
hostile mutation rejection, a concise manuscript, and a rebuilt PDF.

## Non-victory

None of the following is victory:

- deriving only the DNN frontier;
- citing only one parity of `Q` or omitting `q=3`;
- treating only a special `T^11PP` incidence topology;
- replacing either all-rank theorem by a finite census or floating evidence;
- claiming a theorem for all cactus ranks or all graphs.

## Proof route

Use the rank-twelve synthesis verbatim with indices shifted by one. Sharp DNN
gives `sigma>=12-sum epsilon_l`; exact triangle counting leaves `T^12Q` and
`T^11PP`; the two already proved rank-uniform results close those families.
The only new mathematics is the exact rank-thirteen frontier arithmetic.
