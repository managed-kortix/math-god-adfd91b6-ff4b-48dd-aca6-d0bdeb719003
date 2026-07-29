# Reduced k=6 exact-pressure certificate campaign

The archive `../certificates/k6-exact-campaign.tar.xz` contains 1,110 leaf
metadata records and 651 content-addressed compressed LRAT objects.  Every leaf
of the complete source-cut/witness orbit cover is `UNSAT_VERIFIED`.

- Cover: 1,110 semantic orbits, labelled multiplicity 3,171,168.
- Cover payload SHA-256:
  `3979f9dca4f134055b87b3485b95e9601f3263c50031471fbf0659902abbb970`.
- Archive SHA-256:
  `e44f8ff81d272a9f9e4b060d37aa51cdbd560552fd3ced2a1d5f98d94bb80402`.
- Archive bytes: 103,486,540.
- Uncompressed LRAT bytes represented: 602,210,046.
- CaDiCaL source: 1.7.3, commit
  `38e073b389a877b0a0d3c91136d2443ab95fdeba`.
- `lrat-check` source commit:
  `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.

The exact-pressure clauses are redundant consequences of the base reduced
model.  For source `a`, selected inaccessible pair `{t,u}`, eight outneighbors
`O`, five remaining vertices `R`, source-hole count `h`, indicators
`i_v=[v->a]`, and `b_v=[v in B]`, they encode

```
e+({t,u},R) + h_other = 5-h-i_t-i_u-2b_t-2b_u.
```

Here `h_other` counts holes outside the source and witness support.  Explicit
hole variables are equivalent to absence of both orientations, and their total
is constrained to six, which already follows from the exact degree sequence.

Fresh verification:

```sh
mkdir -p /tmp/k6-exact
tar -xJf ../certificates/k6-exact-campaign.tar.xz -C /tmp/k6-exact \
  --strip-components=1
python3 k6_exact_verify.py \
  --root /tmp/k6-exact \
  --checker /path/to/pinned/lrat-check
```

Expected final line:

```
PASS leaves=1110 labelled=3171168
```

This campaign closes the reduced all-seven `rho=0,k=6` model only.  Its use in
the original order-18 problem additionally depends on the written reduction.
