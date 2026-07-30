# Cycle 123: exhaustive no-go for adjacent Hermitian-plane unions

The minimal interacting-plane ansatz is now closed exhaustively.

Let `A` be the explicit alpha-visible orthogonal matrix from Cycle 118.  Every
Hermitian graph plane meeting `L_A` in a projective line is uniquely
parameterized by a nonzero isotropic vector

\[
 z=(a,b,a+b)\in\mathbf F_{32}^3,
\]

through

\[
 B_z=A(I+zz^t).
\]

There are exactly `32^2-1=1023` such neighbors.  For each one, the reduced
union `L_A union L_(B_z)` is a `(1,1,2)` complete intersection in its spanning
projective three-space.  Its full embedded first-order normal map is

\[
 H^0(O_Z(1))^{\oplus2}\oplus H^0(O_Z(2))
 \longrightarrow H^0(O_Z(33)),
\]

with `17` columns in a `1156`-dimensional target.

The dependency-free verifier enumerates all neighbors using genuine
`W_2(F_32)` arithmetic, constructs the divided standard-Fermat remainder, and
tests exact membership in the complete normal image.  For every one of the
`1023` pairs,

\[
 \operatorname{rank}M_z=17,
 \qquad
 \operatorname{rank}[M_z\mid h_z]=18.
\]

Thus no adjacent reduced two-plane union in this complete graph-plane family
admits an embedded flat lift to the standard degree-33 Fermat hypersurface over
`W_2(F_32)`.

The deterministic certificate stream consists of records

```text
a,b,a^b:17,18
```

ordered lexicographically in `a,b`, excluding `(0,0)`.  Its SHA-256 is

```text
c893f4112547e53d50f762167923aa67e17008f7c24cb11bfdaa0f179e9633fe
```

This includes the three pairs whose nine componentwise middle obstruction
coordinates cancel while the alpha coefficient remains nonzero.  Their full
union obstruction still has rank jump `17 -> 18`, proving again that
componentwise cancellation is not the nonlinear lifting criterion.

The conclusion is narrow.  It excludes adjacent reduced pairs containing the
fixed `L_A`; it does not exclude triples, nonreduced structures, different
Hermitian-plane orbits, rational equivalence, relative Chow lifts, or the
exceptional Hodge class itself.  Automatically escalating to an unstructured
triple census would not pass the main-funnel production gate.  The Hodge route
returns to bounded-scout status pending a distinguished collective cycle with a
reason for all-order deformation.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle123_all_adjacent_unions.py
```

No Hodge or Millennium solution is claimed.
