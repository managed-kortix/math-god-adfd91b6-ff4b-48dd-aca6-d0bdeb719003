# Cycle 243: directed small-N Nyman--Beurling certificate

## Decision

For the Cycle 242 logarithmic coefficients and restricted energy, the proposed
small witness passes strictly:

\[
 \boxed{P_6<{3\over4}P_3.}
\]

This proves only that `N=3` is one finite witness for `NB242`; it says nothing
about a cofinal contraction or RH.

## Complete evaluation

For each `N` in `{3,6}`, the verifier evaluates

\[
 P_N=1+2\sum_a c_a g_a+\sum_a c_a^2G_{a,a}
       +2\sum_{a<b}c_ac_bG_{a,b},
\]

where `c_a=mu(a)(1-log(a)/log(N))`,
`g_a=(log(a)+1-gamma)/a`, and `G` is the complete restricted Vasyunin
cotangent kernel from Cycle 38. Thus the affine term and every off-diagonal
pair are included. The subtraction `-1/(ab)` in `RestrictedGram.entry` keeps
the domain `(0,1)` rather than the full-space norm.

At 256-bit Arb precision, directed evaluation gives approximately

\[
 P_3=1.5452502053206377116,\qquad
 P_6=0.75187564425226997104,
\]

and

\[
 P_6-{3\over4}P_3= -0.407062... <0.
\]

More explicitly, the stored rational endpoints include

\[
 P_3\ge {1868092870976925961530363\over1208925819614629174706176},
 \qquad
 P_6\le {908961879475952824057449\over1208925819614629174706176}.
\]

Cross multiplication gives

\[
 4(908961879475952824057449)
 <3(1868092870976925961530363),
\]

so the requested inequality follows using rational arithmetic alone after the
directed transcendental enclosures have been generated. The sign is therefore
not inferred from the displayed decimals.

## Verification

`cycle243-small-nb-certificate.json` stores outward-rounded dyadic rational
endpoints for all four components, both totals, and the comparison margin.
`verify_cycle243_small_nb.py` recomputes the complete formula with Arb, checks
that every recomputed ball lies in its rational certificate interval, and then
performs the final comparison with `Fraction` arithmetic.

```text
uv run --with python-flint python verify_cycle243_small_nb.py
uv run --with python-flint python -m unittest -v test_cycle243_small_nb.py
```

All transcendental setup is evaluated by Arb with directed rounding. The final
certificate inequality uses exact integers and rational numbers only.
