# Order-seven cost-six symbolic atom geometries

Every order-seven rank-seven kernel has thirteen physical paths.  After signed
zero-cost contractions, a positive atom is either a mixed pair of cost one or a
regular simplex `K_k` of cost `(k-1)(k-2)/2`.  Thus the positive costs of
`K3`, `K4`, and `K5` are respectively `1`, `3`, and `6`.

## Complete atomic profiles

Writing `M` for a mixed pair, every cost-six multiset of these atoms is one of

```text
K5
K4+K4
K4+3K3
6K3
M+5K3
M+K4+2K3
2M+4K3
2M+K4+K3
3M+K4
3M+3K3
4M+2K3
5M+K3
6M.
```

This list is arithmetic, not a claim that every profile embeds in a physical
row or has a common PSD completion.  Contractions may identify and switch
vertices.  Consequently distinct physical supports can become repeated or
overlapping quotient supports, producing coupled assemblies.

## Exact support recognizer

`rank7_order7_symbolic_atom_recognizer.py` reads either a generic sparse row or
the emerging exact census.  It:

1. accepts only pure-parity contraction bundles, mixed `(2,1)` bundles, and
   singleton odd paths available to simplex atoms;
2. enumerates every signed contraction quotient and every indexed clique
   partition realizing one of the thirteen profiles;
3. rejects conflicting prescribed correlations exactly over `Fraction`;
4. proves PSD completion when the atom scopes have a running-intersection join
   tree, by the Gram-gluing theorem, and for pure mixed path/cycle quotients by
   the exact spectral bound for signed paths and cycles; and
5. retains cyclic coupled scope systems as `coupled-psd-open`, rather than
   silently promoting a merely plausible support to an equality owner.

The owner template is the canonical target together with precisely the
one-coordinate frontiers carried by zero-cost contraction paths.  Every path in
a mixed or simplex atom is noncontracting, so lengthening it makes the retained
Gram strictly cheaper and does not remain an equality target.

The `exact-equality-owner` label covers disjoint assemblies, one-sums, nested
compatible atoms (including a mixed pair repeated on a `K3` edge), and all other
atom hypergraphs admitting a join tree.  A `coupled-psd-open` record identifies
an exact support candidate but is not ownership: it still requires an exact PSD
completion or a separate coupled equality argument.

## Completed census snapshot

On the completed 40,964-row coarse residual artifact, the recognizer finds 20
candidate rows.  Eleven rows have exact atomic owners: nine admit a switched
regular `K5` quotient and two admit a signed six-cycle mixed-pair quotient.
These give 12 decompositions because one row has two `K5` contraction choices.
The remaining nine candidate rows give 11 `K4+3M` decompositions whose scope
systems are not join-tree assemblies; they remain deliberately typed
`coupled-psd-open`.  This is an owner-template census, not yet a disjoint owner
assignment against rational certificates.

Run a bounded early scan with

```text
python3 positive-square-energy/experiments/rank7_order7_symbolic_atom_recognizer.py --limit 1000
```

Omit `--limit` for the complete 40,964-row residual artifact.  The report keeps
`full_theorem=false`; symbolic atom ownership is only one lane of the full
canonical-plus-thirteen frontier.

For a generic row, pass literal sparse edges and odd counts:

```text
python3 positive-square-energy/experiments/rank7_order7_symbolic_atom_recognizer.py \
  --generic '{"edges":[[0,1,2],[1,2,2],[2,3,2],[3,4,2],[4,5,2],[0,5,2],[0,6,1]],"row":[1,1,1,1,1,1,0]}'
```
