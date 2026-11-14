# D3 exact algebra packet — OPEN partial evidence

This directory preserves reproducible exact algebra for the open obligation

`R31-S:D3: sigma(Theta(1,2,2)+T^3)>3`.

**Status: OPEN. This is partial evidence and proof-route diagnostics only.** It is not a theorem receipt, does not change any owner/master state, and must not be cited as closing D3. In particular, neither the full nonnegative-orthant implication `I>=0 => R<0` nor the continuous signed Coulson phase-area inequality is proved here.

The packet contains:

* complete raw and activity-expanded real/imaginary determinant polynomials for all 14 one-side incidence records (28 after reflection);
* collision-safe compact formulas and independent coefficient checks;
* exact obstruction data for naive coefficientwise defect elimination and leaf-phase comparison;
* exact partial certificates on five equal-activity defect lines and 11,520 one-variable `{0,1}`-face rays.

## Normalization

`Psi_G(z)=i^{-|V(G)|} det(i diag(z)-A_G)=R_G(z)+i I_G(z)`, with rooted-tree substitution `z_v=t+y_v`, `t>0`, `y_v>=0`.

## Reproduce

From this directory:

```sh
python3 export_exact_polynomials.py
python3 check_independent_determinant.py       # 14 PASS
python3 compact_formula_check.py               # 14 PASS
python3 check_rendered_compact_RI.py           # 14 PASS
python3 defect_line_certificate.py             # five exact slice certificates
python3 one-variable-cube-face-certificate.py  # 11,520 exact rays
python3 phase_ratio_cross.py

# Intentionally exits 1 because D3 remains open:
python3 r31-s-d3-full-sachs-diagnostic.py

sha256sum -c SHA256SUMS
```

`D3-REPORT.md` gives the formulas, exact findings, and explicit limitations. `exact-polynomials/manifest.json` records per-record term counts and hashes. The large but text-only exact-polynomial files are retained because they are the independently inspectable evidence; generated caches and the redundant archive are deliberately excluded.
