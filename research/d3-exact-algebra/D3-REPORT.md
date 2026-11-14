# R31-S:D3 full weighted-core audit (main `72b978271828`)

## Verdict

The exact full real/imaginary weighted-core polynomials have now been regenerated for all 14 one-side incidence records (28 after reflection), independently cross-checked by a subset-DP determinant, rendered in compact explicit R/I form, and exported.  The 9 nonexceptional records have `I<0` coefficientwise after `z_v=t+y_v`.  The five exceptional records reduce to `R=A+By`, `I=P+Qy`, with `P<0` coefficientwise and `Q=6-(positive polynomial)`; however `AQ-BP` is mixed-sign in every record.  Thus the obvious coefficientwise defect elimination is rigorously obstructed.  Random, log-box, and differential-evolution searches found no point with `I>=0,R>=0`, but this is not a proof.

A genuine exact positive result is obtained on the equal-activity one-defect slices: if all nondefect activities are `t` and the defect is `t+y`, then `I>=0 => R<0` in all five records.  The proof uses `u=t^2`, Descartes' rule, and the rational separators `1/3<2/5`; see `defect_line_certificate.py`.  It does not extend to the full activity orthant.

No full semialgebraic certificate and no phase-area certificate was found.  Therefore `sigma(D+T^3)>3` remains **OPEN**.

## Universal exact notation

For the diamond `D` on `{A,B,x,z}` with edges `AB,Ax,Bx,Az,Bz`, let

`D_S = Psi_(D-S)`,  where `Psi_X=i^(-|X|)det(i diag(z)-A_X)`.

For triangle `j` with private vertices `Tja,Tjb`, put

`d_j=z_(Tja) z_(Tjb)+1`, `q_j=z_(Tja)+z_(Tjb)-2i`.

A triangle attached at root `w` acts by

`Psi_(X+T_j)=d_j Psi_X+q_j Psi_(X-w)`.

This identity plus deletion gives the following full complex polynomials; their real and imaginary parts are the requested `R` and `I`.  Substitution `z_v=t+y_v` gives the full activity polynomials exported under `exact-polynomials/`.

## Compact formulas for every incidence shape

### Three direct triangles at roots `r_1,r_2,r_3`

The collision-safe formula is

`Psi = sum_(S subset {1,2,3}, r|_S injective) [prod_(j in S)q_j][prod_(j notin S)d_j] D_{ {r_j:j in S} }`.

The injectivity condition is essential: two triangle Sachs components cannot both occupy the same cut vertex.  This one formula covers the six records `(A,A,x),(A,B,x),(A,x,x),(B,B,x),(B,x,x),(x,x,x)`.

### Chain of two at `u`, plus a direct triangle at `v`

Let `b=z_(T1b)` and

`F_u=d_1d_2D_empty+d_2q_1D_u+q_2(bD_empty+D_u)`.

If `u!=v`, let

`F_{u;v}=d_1d_2D_v+d_2q_1D_{u,v}+q_2(bD_v+D_{u,v})`.

If `u=v`, deletion disconnects the private two-triangle branch `B_12`; hence

`F_{u;u}=D_u Psi_(B_12)`,

where `B_12` has edges `T1a-T1b,T1a-T2a,T1a-T2b,T2a-T2b`.  Then

`Psi=d_3 F_u+q_3 F_{u;v}`.

This covers `(A,x),(B,x),(x,A),(x,B),(x,x)`.

### Fork rooted at `x`

Set `X=d_1D_empty+q_1D_x`,
`X_a=z_(T1b)D_empty+D_x`, and `X_b=z_(T1a)D_empty+D_x`.

For both children at `T1a` (same):

`Psi=d_2d_3X+(q_2d_3+d_2q_3)X_a`.

For children split between `T1a,T1b`:

`Psi=d_2d_3X+d_3q_2X_a+d_2q_3X_b+q_2q_3D_empty`.

### Chain of three rooted at `x`

Set

`X_1=d_1D_empty+q_1D_x`,
`X_1^- = z_(T1b)D_empty+D_x`,
`X_2=d_2X_1+q_2X_1^-`,
`X_2^- = z_(T2b)X_1+X_1^-`.

Then

`Psi=d_3X_2+q_3X_2^-`.

`compact_formula_check.py` compares these formulas exactly against the independently generated full Sachs polynomial in every record.

## Bare-core specializations

With every activity equal to `t`, the exact pairs are listed in `univariate-exact.txt`.  In all 14 cases, `I(t)<0`; for example the split fork is

`R=-12-61t^2+62t^4+60t^6+14t^8+t^10`,
`I=-18t-150t^3-78t^5-10t^7`.

This bare-core fact does not control arbitrary rooted-tree messages.

## Exact obstruction and partial certificate

For each exceptional record, isolate the unique positive activity carrier `+6y`:

`R=A+By`, `I=P+Qy`.

Exact facts:

* `P` is coefficientwise strictly negative;
* `Q` has exactly one positive coefficient, its constant `+6`;
* on `I=0`, `y=-P/Q` (requiring `Q>0`) and `R=(AQ-BP)/Q`;
* `AQ-BP` has both positive and negative coefficients in every record (activity aggregate: 179605 positive, 42651 negative; raw aggregate also mixed).

So neither coefficientwise sign nor naive monomial domination proves the implication.  The first positive terms of `H` already occur in activity degree two, e.g. `+8 y_A y_T1a` (chain/direct) or `+8 y_T1a y_T1b` (split fork), against constant `-72`; see `boundary-lowest-obstruction.txt`.

A second exact obstruction affects the most obvious recursive phase route.  For each leaf triangle, `phase_ratio_cross.py` expands both the host/deleted-host cross product and the full-graph/deleted-host cross product controlling the corresponding phase differences.  Both have both coefficient signs in every leaf deletion except the symmetric direct `(x,x,x)` record.  Thus a uniform coefficientwise leaf-phase comparison also fails, though the underlying semialgebraic inequality may still be true.

The numerical searches consistently maximize boundary `R` only at the closure where activities approach zero, with limiting value `-12`; this is evidence, not a certificate.  Exact checking on all 11,520 one-variable rays through `{0,1}` cube faces gives `H<0` and `B<=0` whenever `Q>0`, hence the full implication `I>=0 => R<0` on those rays; this finite skeleton still does not certify the full orthant.

On the exact equal-activity defect line, write `u=t^2`.  Each `Q(u)` has one positive root (one Descartes variation), and `Q(0)>0>Q(1/3)`.  Each `H(u)=AQ-BP` likewise has one positive root, and `H(0)<0`, `H(2/5)<0<H(4)`.  Hence

`Q(u)>0 => u<rho_Q<1/3<2/5<rho_H => H(u)<0`.

Moreover, `P<0`, while `B(u)` is increasing and `B(1/3)<0`; hence on this region `B<0`.  Therefore `I=P+yQ>=0` implies `y>=-P/Q`, and

`R(y)<=R(-P/Q)=H/Q<0`.

This rigorously proves the full implication `I>=0 => R<0`, but only on those five one-dimensional slices.

## Reproduction

Run from `/workspace/d3-artifacts`:

```sh
python3 r31-s-d3-full-sachs-diagnostic.py       # expected exit 1, fail-closed
python3 check_independent_determinant.py
python3 compact_formula_check.py
python3 export_exact_polynomials.py
python3 univariate_exact.py
python3 defect_line_certificate.py
python3 search_semialgebraic.py 300000           # heuristic
python3 weighted_boundary_search.py 500000       # heuristic
/workspace/.venv/bin/python search_boundary_optimize.py  # heuristic, SciPy
```

The fail-closed diagnostic's nonzero exit is intentional.  No repository, `STATE`, publication, session, commit, push, or external contact was made.

## Final strengthened finite checks

`compact-RI-all-records.txt` now gives the **explicit real and imaginary
parts** (not merely the complex recurrence) for every one of the 14 records,
in terms of the exact diamond deletion states `R_S,I_S` and the triangle
activities.  `check_rendered_compact_RI.py` substitutes the exact diamond
states and verifies these displayed formulas coefficient-for-coefficient
against the independent Sachs generator.  The `u=v` chain formula uses

`Psi(B_12)=a_1a_2b_1b_2+a_1b_1+a_2b_1+a_2b_2+b_1b_2+1-2ib_1`.

A further exact semialgebraic finite check is in
`one-variable-cube-face-certificate.py`: for every exceptional record, every
choice of one free nondefect activity `s>=0`, and every `{0,1}` assignment of
the other eight nondefect activities, it proves

`Q(s)>0 => [H(s)=A(s)Q(s)-B(s)P(s)<0 and B(s)<=0]`.

Since `P<=0` on the closed orthant (and `P<0` in the legal positive interior), this gives `I=P+yQ>=0 => R=A+yB<0` on each ray. Here `Q,B` are affine and `H` is quadratic, so endpoints and (when present) the rational vertex give an exact certificate.  All `5*9*2^8=11520` rays pass.
This strengthens the obstruction search but is **not** a proof on the full
nine-dimensional orthant.

## Exact phase reformulation and obstruction

For arbitrary positive raw activities let `Z=diag(z_v)` and
`B_z=Z^{-1/2}A(G)Z^{-1/2}`.  Since

`Psi_G(z)=det(Z) det(I+i B_z)`,

its continuous phase (normalized to zero as all activities tend to infinity)
is exactly

`theta_G(z)=sum_k arctan(lambda_k(B_z))`.

This spectral identity removes determinant-branch ambiguity, but does not by
itself give the required signed Coulson area.  The natural recursive attempt
would compare the phase of a host `X` with `X-w` while attaching a leaf
triangle.  The exact host cross product

`C_{X,w}=Im(Psi_X conjugate(Psi_{X-w}))`

(and likewise the full-graph/deleted-host cross product) is mixed-sign after activity expansion for every tested leaf deletion except
the symmetric direct record `(x,x,x)`, where it is coefficientwise negative.
The complete counts are in `phase-ratio-cross.txt`.  Thus no uniform
coefficientwise phase-ratio monotonicity certificate exists along this route.
This is an obstruction to that proof mechanism, not a counterexample to the
phase or energy claim.
