# R21 arbitrary-theta scope audit

Date: 2026-11-14. Status: **OPEN / NONPROMOTIONAL**.

## Verdict

The repository does not currently contain an adjacency-authenticated,
owner-exact proof of the bridge-free family

```text
Theta(1,2,r) + T^5,   r >= 2.
```

The only adjacency gate presently available for this branch is
`research/r21-literal-cycle-typing-verifier.py`. It reconstructs one literal
`D=Theta(1,2,2)=K4-e` and five literal cycle blocks. Its `q=3` output therefore
authenticates only the physical profile `D+T^5` (`r=2`). Its `q=5` output
authenticates the distinct physical profile `D+T^4+C5`. It authenticates no
`Theta(1,2,r)` with `r>=3`, and it proves no territory partition, packet
inequality, bridge dispatch, or rank-seven conclusion.

Accordingly the symbolic row `Theta(1,2,r)+T^5` in the rank-seven debit ledger
must remain open. A symbolic residual registry is not an adjacency receipt.
The separately typed and conditionally dispatched `D+T^4+C5` row does not
close the arbitrary-theta row.

## Exact audit of the proposed opening

Write the theta paths as the edge `xy`, the length-two path `x-a-y`, and an
`x-y` path `Q` of length `r`.

* For `r=2`, `Q` does have one internal vertex. The phrase "choose an internal
  vertex of the long arm" is nevertheless ambiguous because the two
  length-two arms are symmetric and neither is uniquely long. A proof must
  designate one of them and derive its physical owner class. The present
  literal typing gate stops before that operation.
* For `r>=3`, `Q` has an internal vertex, but deleting the complete owner class
  is not the same as deleting that vertex plus a one-root tree. The owner class
  can contain any subset of the five external triangle blocks, including
  nested triangles, unless an adjacency-level owner theorem proves otherwise.
* If the opened owner class contains no external cycle and is proved to be a
  connected tree, its complement does retain the intrinsic triangle `x-a-y-x`
  and the five external triangles. The remnants of `Q-v` are acyclic. Under
  an exact block/owner hypothesis, the complement is therefore an all-triangle
  cactus with six triangular blocks. It need not be one shared-cut cluster,
  but the cited all-triangle cactus packet is topology-uniform and can supply
  the needed `sigma>1` once connectedness, inducedness, and ownership are
  established.
* If the owner class contains one or more external triangles, the sentence
  "it is a strict triangular territory and the rank-at-most-six complement is
  nonnegative" is only a proposed ledger. The repository has not authenticated
  from full adjacency that the owner side and complement are connected induced
  territories, that all boundary cuts and connector remnants have unique
  owners, or that the complement lies in the exact lower-rank theorem scope.

Thus the six-triangle spectral input is not the principal defect. The missing
step is the physical typing and owner lift that makes the two claimed induced
territories legitimate for every `r` and every block-cut incidence.

## Why the historical verifier is not a receipt

`research/rank-seven-nested-induced-piece-verifier.py` reads a manifest whose
`R21` record already says `status: closed`, then determines support from the
manifest integers `anchor_threshold` and `negative_territories`. Its
`synthetic_owner_partition` routine manufactures labelled tuples from the
supplied channel name. It accepts no graph adjacency, reconstructs no theta,
runs no Tarjan/block-cut analysis, derives no owner class, and tests no actual
connectedness or inducedness. Source hashes make this registry stable; they do
not turn it into a semantic proof. Its printed `R21` closure is therefore not
valid provenance for the arbitrary-`r` physical family.

## Minimum fail-closed integration wording

Use the following status until a separate physical theorem exists:

```text
R21 splits into independently authenticated subrows.
The literal adjacency gate types only D=Theta(1,2,2) with five cycle blocks:
q=3 gives D+T^5 and q=5 gives D+T^4+C5. The gate proves classification only,
not ownership or a square-energy packet. The available hostile-C5 dispatch is
conditional and applies only to D+T^4+C5. The family
Theta(1,2,r)+T^5 for arbitrary r (in particular every r>=3 realization)
remains OPEN; no symbolic manifest or synthetic owner channel closes it.
```

A future closure must accept adjacency (or a proved equivalent physical block
contract), authenticate the three theta path lengths and literal external
triangles, derive the opened vertex and its complete owner component, and
verify on original vertices that the resulting territories are connected,
induced, disjoint, exhaustive, and uniquely own every cut, connector remnant,
and rooted payload. Only then may it invoke the tree/triangular and
six-triangle credit inequalities.
