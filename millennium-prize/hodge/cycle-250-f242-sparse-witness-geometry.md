# Cycle 250: exact geometry of the F242 sparse witness

## Result

The Cycle 249 norm-one witness with `S=-i` is everywhere tangent-injective,
but it is not geometrically injective. Hence it is not a closed immersion and
is rejected before any deformation calculation. This tests only that one
witness and does not enumerate the `5^54` matrix triples.

## Tangent calculation

Put `c=zeta Z`, so the Fermat quartic is

\[
 a^4+b^4+c^4=0.
\]

By Cycle 248, the canonical-coordinate vector of `dphi`, up to a nonzero local
tangent scalar, is `(a,-b,-c)`. For points `p_r=[a_r:b_r:c_r]`, multiplying
this vector by the three Cycle 249 matrices gives the columns

\[
 v_1=(0,-ia_1,-ic_1,ia_1,0,ic_1)^t,
\]

\[
 v_2=(c_2,0,-ia_2-c_2,-b_2,a_2,-ic_2)^t,
\]

\[
 v_3=(b_3,-a_3,-b_3+c_3,a_3,-b_3+c_3,0)^t.
\]

Tangent injectivity is equivalent to rank three of `[v_1 v_2 v_3]` at every
point of `C^3`. Adjoin its twenty `3 x 3` minors to the three Fermat equations.
On each of the 27 standard projective patches, obtained by setting one of
`a_r,b_r,c_r` equal to one for each `r`, exact Groebner reduction over
`Q(i)` gives the unit ideal. The patches cover `C^3`, so the tangent map is
everywhere injective.

## Cheap exact rejection

The middle column of `L_1` is zero. Therefore `L_1 phi` depends only on the two
quotient maps `q_X` and `q_Z`. Take

\[
 P=[1:0:1],\qquad Q=[-1:0:1].
\]

These are distinct points of `C`. Moreover

\[
 Q=\sigma_X(P)=\sigma_Z(P)
\]

projectively. Since `q_X` is the quotient by `sigma_X` and `q_Z` is the
quotient by `sigma_Z`, both quotient values agree at `P,Q`. Consequently
`L_1 phi(P)=L_1 phi(Q)`. Fixing arbitrary points `R_2,R_3` in the other two
source factors gives

\[
 f_L(P,R_2,R_3)=f_L(Q,R_2,R_3).
\]

Thus this witness passes the rank, exceptional-Weil, and tangent tests but
fails geometric injectivity. It is exactly `REJECT_NONINJECTIVE`, not an F242
pass and not a rejection of the full finite category.

Reproduce both checks with

```sh
python3 millennium-prize/hodge/verify_cycle250_f242_sparse_witness_geometry.py
```
