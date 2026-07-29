# Cycle 117: Hermitian-plane lifting gate

The exceptional degree-33 Fermat character has abundant algebraic
representatives after reduction modulo `2`.  This does not supply a
characteristic-zero cycle, and an explicit noncoordinate Hermitian plane is
already obstructed modulo `4`.

Over `F_(2^10)`, the reduction

\[
 X:\sum_{i=0}^5x_i^{33}=0
\]

is a Hermitian fourfold because `33=2^5+1`.  Shimada's theorem says that its
maximal planes span middle etale cohomology over `Q_l`, so after cyclotomic
scalar extension at least one plane has nonzero projection to

\[
 \alpha=(7,10,13,19,22,28).
\]

This is an exact finite-field Tate statement, not a lift.

For a concrete plane, take `a in F_32 \ F_2`, `b=1+a`, and in coordinates
`(x_0,x_1,x_2,y_0,y_1,y_2)` put

\[
 y=Ax,\qquad
 A=\begin{pmatrix}a&b&0\\b&a&0\\0&0&1\end{pmatrix}.
\]

Since `A^t A=I` in characteristic two, this is a maximal Hermitian plane.  Its
normal map into degree-33 hypersurface equations is

\[
 \Phi(B)=x^{[32]t}A^tBx,
\]

with image exactly the nine-dimensional span of `x_r^32 x_s`.  The target has
dimension `binom(35,2)=595`, so the cokernel has dimension `586`.

Use Teichmuller lifts of `a,b` to the standard Fermat model over `W_2(F_32)`.
After dividing the restricted equation by `2` and reducing modulo `2`, all
interior binomial terms vanish except exponents `16,17`: these are exactly the
interior `m` for which

\[
 v_2\binom{33}{m}=1.
\]

Modulo `im Phi`, the obstruction is

\[
 (ab)^{16}
 [x_0^{16}x_1^{17}+x_0^{17}x_1^{16}]\ne0.
\]

Neither monomial has the form `x_r^32 x_s`; changing the lift of the plane
adds an element of `im Phi`.  Therefore this noncoordinate Hermitian plane
does not lift as a linear plane even to the standard Fermat hypersurface modulo
`4`.

This does not prove that a projector-weighted combination of Hermitian planes
cannot lift as a cycle.  Individual obstruction classes can cancel.  At the
cohomological level, only balanced character combinations can lie in the
characteristic-zero Hodge filtration; the exceptional `alpha` is balanced and
therefore survives that necessary test.  Producing a characteristic-zero cycle
still requires a genuinely new variational-Hodge or explicit correspondence
argument.

The Artin--Tate appearance of the normalized Jacobi eigenvalue likewise does
not close the gap: a nonzero morphism `L^2 -> M_alpha` in Chow or numerical
motives is equivalent here to the desired algebraicity statement.

No Hodge or Millennium solution is claimed.
