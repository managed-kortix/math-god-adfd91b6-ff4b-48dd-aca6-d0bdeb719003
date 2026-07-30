# Cycle 133: all reduced dependent-pencil triples are obstructed

After the hyperbolic triple of Cycle 132, every remaining pair of distinct
isotropic directions is dependent.  The resulting three planes lie in a common
pencil and are classified by a cross-ratio parameter.  Every reduced,
pairwise-distinct member of this entire finite stratum fails the genuine
`W_2(F_32)` embedded lifting gate.

Fix a nonzero isotropic vector `z` and write `w=lambda z`.  In a common
`P^3`, with coordinates

\[
y=Ax+(Az)s,\qquad U=z^tx,
\]

the three graph planes are

\[
s=0,\qquad s+U=0,\qquad s+\lambda^2U=0.
\]

For `lambda` different from `0,1`, their reduced union is the complete
intersection

\[
I_\lambda=(H_1,H_2,s(s+U)(s+\lambda^2U))
\]

of type `(1,1,3)` in `P^5`.  Its degree-33 quotient has dimension `1684`, and
its complete embedded normal space has dimension

\[
2h^0(O_T(1))+h^0(O_T(3))=8+19=27.
\]

The 30 field values `lambda in F_32 minus {0,1}` form five fully unordered
cross-ratio classes.  Exact computation for all 30 values, using genuine
Teichmüller-coordinate Witt arithmetic, gives uniformly

\[
\boxed{\operatorname{rank}M_\lambda=27},\qquad
\boxed{\operatorname{rank}[M_\lambda\mid h_\lambda]=28}.
\]

Thus no reduced, pairwise-distinct dependent-pencil triple containing the fixed
alpha-visible plane lifts as an embedded flat subscheme to the standard Fermat
model modulo four.

There is also a symbolic explanation.  A fixed left-kernel functional applied
to the divided remainder is, up to a nonzero field unit,

\[
p(\lambda)
=1+\lambda+\lambda^8+\lambda^9
 +\lambda^{15}+\lambda^{16}+\lambda^{23}+\lambda^{24}
\]

\[
=(1+\lambda)(1+\lambda^8)(1+\lambda^{15}).
\]

Over `F_32`, its only zero is the collision `lambda=1`; hence it is nonzero on
all 30 distinct-plane parameters.  This proves the obstruction uniformly on
the finite field-valued pencil stratum rather than merely sampling five
representatives.

Twenty-eight parameters retain nonzero alpha projection in the anchored
coordinate presentation.  The two alpha-zero parameters are `9` and `24`; they
are also obstructed.  Visibility therefore supplies no hidden survivor.

The deterministic aggregate certificate hash is

```text
81903632919c44c3164507ec8ecb2c3af7cc0459b3fe7bf23ef9c7d12e196525
```

Together with Cycle 132, this closes both reduced incidence strata arising
from pairs of distinct isotropic directions: hyperbolic pairs and dependent
pencils.  It does not cover repeated-plane collisions, nonreduced structures,
other collective cycles, rational equivalence, relative Chow classes, or the
Hodge conjecture.

Reproduce with

```sh
python3 millennium-prize/hodge/verify_cycle133_dependent_pencils.py
```

No Hodge or Millennium solution is claimed.
