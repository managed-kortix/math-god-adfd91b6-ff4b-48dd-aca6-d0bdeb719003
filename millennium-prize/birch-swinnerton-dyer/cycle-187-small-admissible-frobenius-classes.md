# Cycle 187: small admissible Frobenius classes at ell=29

## Frozen packet and exact search

Fix

\[
 E=433\mathrm a1:y^2+xy=x^3+1,
 \quad p=7,\quad P=(0,1),\quad Q=(-1,1),\quad \ell=29.
\]

For every prime `3 <= q < 200000`, excluding `7,29,433`, this cycle checks
the following packet exactly:

1. `(q/29)=1`, equivalently the Cycle 182 auxiliary condition at `ell=29`;
2. `w(E^(D_q))=-1`, using `w(E^(D))=w(E)*(D/-433)` and `w(E)=+1`;
3. `q=1 mod 7`, `a_q(E)=2 mod 7`, and `v_7(#E(F_q))=1`.

The last line makes residual Frobenius a nonidentity unipotent in
`GL_2(F_7)`. The order and trace are computed by the exact character sum on

\[
 W^2=X^3+X^2+64.
\]

Multiplying `P,Q` by `#E(F_q)/7` then computes their ordered localization row.
Cycle 184 and the maximality theorem of Cycle 185 identify the full conjugacy
class in

\[
 \operatorname{Gal}(L_0/\mathbf Q)
 =E[7]^2\rtimes\operatorname{GL}_2(\mathbf F_7)
\]

by the `GL_2` type together with the zero/projective row.

Run

```sh
python3 millennium-prize/birch-swinnerton-dyer/verify_cycle187_small_frobenius_classes.py --bound 200000
```

The dependency-free script uses an integer sieve, Euler's criterion, exact
finite-field group operations, and no floating-point arithmetic in any
arithmetic decision.

## Repeated full `L_0` classes

There are 91 packet members in nine full classes; eight classes repeat. The
smallest useful members of each repeated class are:

| residual `GL_2` type | projective row | count below 200000 | first members |
|---|---:|---:|---|
| nonidentity unipotent | `[0:1]` | 15 | `8191, 10949, 19559, 31963` |
| nonidentity unipotent | `[1:0]` | 6 | `65647, 82657, 86353, 144593` |
| nonidentity unipotent | `[1:1]` | 8 | `1289, 37493, 60901, 80221` |
| nonidentity unipotent | `[1:2]` | 13 | `3823, 8317, 9521, 11131` |
| nonidentity unipotent | `[1:3]` | 15 | `11831, 14897, 48889, 69427` |
| nonidentity unipotent | `[1:4]` | 11 | `35099, 53047, 73361, 80263` |
| nonidentity unipotent | `[1:5]` | 10 | `1499, 6287, 7589, 14071` |
| nonidentity unipotent | `[1:6]` | 12 | `5419, 26153, 26251, 37003` |

The shortest same-class pairs, and hence the first candidates for exact
modular-symbol comparison, are

\[
 (1499,6287)_{[1:5]},\quad
 (3823,8317)_{[1:2]},\quad
 (8191,10949)_{[0:1]},\quad
 (11831,14897)_{[1:3]}.
\]

The pair `(1289,37493)` in class `[1:1]` is also small. For a zero/nonzero
search, compute `c(q,29)` first for these pairs, then continue within the same
row bucket. Matching these labels is an exact conjugacy classification under
the proved maximal semidirect-product model, but a final Cycle 182 certificate
must still provide the explicit comparison maps and exact modular-symbol
replay.

## Correction to Cycle 186

Cycle 186 states that `(1289/29)=-1`. This is an arithmetic error:

\[
 1289\equiv13\pmod {29},\qquad 10^2\equiv13\pmod {29},
\]

so `(1289/29)=1`. Thus `1289` is admissible at `ell=29`; it also lies in the
frozen root-number `-1` packet and has full class
`(nonidentity unipotent,[1:1])`. The old full-modulus progression remains a
needlessly sparse search, but it is not excluded by the `ell=29` condition.

No value of `c(q,29)`, modular-symbol collision, BSD case, or governing-field
theorem is claimed here.
