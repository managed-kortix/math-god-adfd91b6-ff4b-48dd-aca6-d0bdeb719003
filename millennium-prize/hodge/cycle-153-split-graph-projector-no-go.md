# Cycle 153: split graph-projector objects do not deform

The rational Weil projector from Cycle 152 has a canonical denominator-cleared
perfect representative in `K_0`, but the obvious split object remains
obstructed. Cancellation occurs only after supertrace and semiregularity.

Write

\[
q(t)=D^{-1}\sum_{k=0}^6c_kt^k,
\qquad D=930187500000000000,
\]

and let `F_k` be the structure sheaf of the transformed graph obtained from
the diagonal by `u^k`, where `u=2+i`. Split positive and negative coefficients
and form

\[
P_D=\bigoplus_{c_k>0}F_k^{\oplus c_k}
\oplus
\bigoplus_{c_k<0}F_k[1]^{\oplus(-c_k)}.
\]

Then

\[
\operatorname{ch}_3(P_D)/D=P_{\rm Weil}[\Gamma].
\]

Thus `P_D` realizes the desired class rationally. However, a shift does not
negate the raw Atiyah obstruction. The obstruction of the split sum is block
diagonal, and vanishing requires each graph block to vanish. The signs appear
only in the supertrace, explaining why the horizontal Chern character does not
imply deformation of the object.

Upper-triangular extensions cannot repair this. For

\[
\alpha=\begin{pmatrix}a&\eta\\0&b\end{pmatrix},
\]

the Maurer--Cartan curvature has diagonal entries `da+a^2` and `db+b^2`,
independent of `eta`. The extension class has its own compatibility equation
but supplies no return path capable of canceling either diagonal obstruction.
The same conclusion holds for a pre-existing filtered cone.

Effective unions of graph components also fail. Distinct scalar graphs
intersect in finitely many transverse points, but the local union of two
three-planes in six-space has no hypersurface-node smoothing parameter. Its
bilinear ideal has syzygies forcing constant first-order smoothing terms to
vanish. The normal obstruction is componentwise:

\[
B\longmapsto(\rho_a(B),\rho_b(B)),
\qquad
\rho_a(B)=Q^{-1}B^t-N(a)B.
\]

For the unit pair `(1,i)`, the kernel remains the original three-dimensional
graph locus. For `(1,1+i)`, the combined map is injective, so the union moves
in no nonzero PEL direction.

For distinct transformed graphs meeting transversely, cross Ext groups are
concentrated in degree three. In particular, unshifted `Ext^1` and `Ext^2`
vanish, so there are no ordinary extension differentials available to kill the
six-dimensional self-obstruction. Shifting moves intersection classes in degree
but does not itself create a differential whose commutator null-homotopes every
graph obstruction.

This closes three natural representatives: the denominator-cleared split
perfect object, every filtration-preserving upper-triangular graph extension,
and the smallest effective graph unions with transverse intersections.

A genuinely bidirectional twisted complex remains logically possible because
return paths can modify diagonal curvature through products of opposite
off-diagonal morphisms. Such a candidate must be explicit and pass the exact
corrected obstruction test

\[
O_E(B)+C_E(u)=0
\]

for a PEL tangent `B` outside the three-dimensional graph kernel, after all
gauge boundaries and hyper-Ext corrections are included. No such differential
is currently known.

This is a bounded no-go for split/filtered graph-projector realizations, not a
no-go for all perfect representatives and not a Hodge-conjecture result.
