# Cycle 118: an explicit alpha-visible Hermitian plane and rotation gate

Cycle 117's sparse block plane was useful for a `W_2` obstruction but is
invisible to the exceptional character: its diagonal stabilizer carries a
nontrivial restriction of `alpha`.  We now give an exact visible plane.

Work in

\[
 \mathbf F_{32}=\mathbf F_2[t]/(t^5+t^2+1)
\]

and set

\[
A=\begin{pmatrix}
0&t&t+1\\
t&t^2+1&t^2+t\\
t+1&t^2+t&t^2
\end{pmatrix}.
\]

Exact field arithmetic gives `A^t A=I`.  Its bipartite support graph is
connected, so the graph plane `L_A: y=Ax` has trivial projective diagonal
stabilizer.

For

\[
 \alpha=(7,10,13,19,22,28),
\]

the relevant character coefficient reduces by Lucas/Frobenius support to
sixteen monomials.  Their exact sum is

\[
 P_\alpha(A)=t^3+t^2+t=t^{12}\ne0,
 \qquad P_\alpha(A)^{-1}=t^2+t.
\]

Hence the numerical/cohomological class `e_alpha[L_A]` is nonzero.  This is an
explicit characteristic-two Tate representative of the exceptional character,
not merely an existence consequence of Hermitian-plane spanning.

For a general Hermitian graph plane, the modulo-`4` embedded obstruction has
nine middle coefficients: six of exponent type `(17,16,0)` and three of type
`(16,16,1)`.  This corrects the two-variable formula, which applies only to the
block plane.  Individual Hilbert obstructions live in different summands over
the translated plane orbit; there is no canonical additive Hilbert obstruction
attached to the rational projector cycle.

Most importantly, even cancellation of every first-order character component
would only remove a necessary obstruction.  It would not produce a point of a
relative Chow space, compatible lifts through all `W_n`, or an algebraic cycle
on the characteristic-zero fiber.  Invoking a variational Hodge/Tate theorem at
that step is circular in the required generality.

The Hermitian lifting route is therefore retired as the main funnel.  It is
preserved as a bounded Hodge scout with one meaningful nonlinear test: decide
whether the explicit projector cycle lies in the image of the relative `CH^2`
specialization from the standard `W_2` Fermat lift.  A mere kernel of component
Hilbert obstructions does not pass.

No Hodge or Millennium solution is claimed.
