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

## Held-out no-optimization test

The reusable content of the dominant class is not its stored rational payload,
but its balanced signed rank-one geometry. A row has this certificate exactly
when every support bundle is uniformly odd or uniformly even and those bundle
parities are a cut: there are vertex signs `s_u` with
`s_u s_v = (-1)^odd` on every support edge. Then `G_uv=s_u s_v` is PSD of rank
one and every canonical or plus-two path has transformed endpoint correlation
one, hence exact cost zero. This is a payload-free certificate and requires no
optimization.

Run the held-out scan with:

```sh
python3 positive-square-energy/experiments/rank6_order10_gram_template_miner.py \
  --census-cache /tmp/opencode/r10-census.xz --require-covered 70000 \
  --future-range 90000 125457
```

On the untouched future residual interval `[90000,125457)`, it recognizes
exactly `218/35457` rows (`0.6148%`) and therefore certifies `3488` frontier
targets. The split is `55/10000` on `[90000,100000)` and `163/25457` on
`[100000,125457)`. None of the 218 rows overlaps the four structural or fourteen
atom rows in the held-out interval, so the net gain is 218 rows and the combined
payload-free coverage there is `236/35457` rows, or 3776 targets. This is
substantial enough to integrate as `MODE_BALANCED`, a payload-free mode verified
directly from the residual parity row. It is checked before the existing
structural and atom lanes, then before numerical optimization. The result
remains a thin fast lane rather than broad template coverage, but unlike literal
stored rational Grams it transfers exactly to the held-out future stream.
