# Order-ten exact Gram-template mining

## Recognizer

`rank6_order10_gram_template_miner.py` decodes completed `R10G1` witnesses,
reconstructs each rational branch correlation Gram, and canonicalizes it under
the full equivalence

`G -> D P G P^T D`,

where `P` is any vertex permutation and `D` is any diagonal sign matrix.  All
comparisons use `Fraction`; SHA-256 is only a compact name for the resulting
exact canonical upper triangle.  Switching-invariant vertex and signed-triangle
fingerprints split the permutation search into tied cells.  The remaining cell
permutations are enumerated, so the recognizer is exact rather than heuristic.

Run from the repository root:

```sh
python3 positive-square-energy/experiments/rank6_order10_gram_template_miner.py \
  --census-cache /tmp/opencode/r10-census.xz --require-covered 70000 \
  --output positive-square-energy/experiments/rank6_order10_gram_template_mining.json
```

The unit audit is:

```sh
python3 -m unittest \
  positive-square-energy/experiments/test_rank6_order10_gram_template_miner.py
```

## Exact 70,000-row result

The completed interval `[0,70000)` contains 69,992 shared rational witnesses
and eight pre-existing symbolic K1133 templates.  The shared witnesses produce
69,780 distinct signed-permutation Gram classes.  Only eleven classes recur:
they contain 223 witnesses, and only 212 witnesses occur after the first member
of their class has entered the library.

Thus an online library populated from earlier witnesses recognizes exactly
`212/69992`, about `0.303%`, of later shared witnesses.  The dominant class is
the rank-one balanced Gram and accounts for 190 occurrences; the next class has
only seven.  This is an exact negative answer to the proposed broad shortcut:
raw rationalized branch Grams are overwhelmingly unique, even after quotienting
by every sign switch and vertex relabeling.  A small exact library is useful for
a thin degenerate lane, but it does not certify broad future order-ten
residuals instantly.  Any broad template scheme must canonicalize a coarser
analytic geometry before rational waypoint perturbation, not the completed
rational branch Gram itself.
