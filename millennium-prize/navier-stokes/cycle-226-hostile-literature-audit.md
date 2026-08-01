# Cycle 226 hostile literature audit

## Verdict

The real, mean-zero, fixed-support use of Elgindi--Hu--Sverak Theorem 5.1 is
sound and rules out every real coefficient-dependent finite-mode orbit in
Cycle 226. Three qualifications are necessary:

1. "Supported on finitely many modes" means support in one common finite set
   throughout a time interval, not merely finite support separately at each
   time.
2. Literal time-independence requires removal of the constant velocity mode.
   With nonzero mean, the classified fields travel by Galilean translation.
3. The paper says the statement remains true for complex solutions, but its
   displayed proof uses the `k -> -k` symmetry of real Fourier support and
   supplies no replacement complex argument. The arbitrary-complex-variety
   version and complex equilibrium decomposition therefore rest on an author
   assertion, not the proof printed there.

There is no regularity gap in the coefficient-variety application: finite
Fourier support turns Euler into a polynomial ODE, so the local orbit is
analytic in time and smooth in space. The serious overreach was presenting the
complex algebraic conclusion as proved without recording the source's omitted
complex argument.

## Exact source statement

Theorem 5.1 of T. Elgindi, W. Hu, and V. Sverak, *On 2d Incompressible Euler
Equations with Partial Damping*, Communications in Mathematical Physics 355
(2017), 145--159, doi:`10.1007/s00220-017-2877-y`, says:

> If `u(x,t)` is a solution of 2d incompressible Euler's equation on `T^2`
> which is supported on finitely many Fourier modes, then `u` is independent
> of time. Moreover, its "Fourier support" is either a subset of a circle
> centered at the origin, or a line passing through the origin.

The proof works with real-valued solutions, invokes
`hat f(-k)=conj(hat f(k))`, and says that "the statement remains true for
complex solutions." It then chooses a minimal common finite set `S` containing
the vorticity support for every time in an interval. Analyticity of the finite
polynomial ODE shows that each mode in minimal `S` is nonzero away from a
discrete set. The key combinatorial lemma is proved for symmetric `S`, using
the symmetry inherited from reality.

Thus Cycle 226's mean-zero formulation is not an exact quotation; it is a
necessary repaired interpretation. Likewise, the complex result is stated in
the prose of the proof, but the proof on the page establishes the real
symmetric-support case.

## Applicability audit

### Complex solutions

Cycle 226 takes `A_S=C^S`, starts the polynomial ODE at every complex point,
and invokes Theorem 5.1 on that orbit. This is valid only if one accepts the
paper's one-sentence complex extension or supplies its missing argument. The
real theorem cannot by itself prove vanishing at all complex points: vanishing
on the Fourier-real locus of an arbitrary complex variety need not control
complex components having no real points.

What is unconditional is the real version. On the real coefficient space
defined by `z_-k=conj(z_k)`, every invariant trajectory is stationary, giving
a real-radical conclusion. This does not automatically imply the ordinary
complex-radical identity.

### Time-varying support

The source fixes a finite `S` with `supp hat(omega(t)) subset S` for every time
in an interval. Coefficients may vanish at isolated times, so support drops and
reappearances inside `S` are covered. Cycle 226's invariant variety also has a
fixed ambient `S`, so its application is exact on this point.

The theorem does not cover a hypothetical solution for which each individual
time has finite support but the union over an interval is infinite. The
paper's following remark discusses stronger bounded-support-at-selected-times
statements and leaves related two-time questions open. "Every individual
finite-support orbit" must therefore mean a uniformly finite-support orbit.

### Mean mode

Vorticity has no zero Fourier mode, but velocity can have a conserved mean
`U`. If `v` is a mean-zero stationary line/circle field, then

\[
 u(x,t)=U+v(x-Ut)
\]

is a finite-mode Euler solution and is generally time dependent in fixed
coordinates. Hence Theorem 5.1, read literally with the velocity zero mode
allowed, has an omitted normalization. Cycle 226 correctly removes the mean
and identifies Galilean traveling waves afterward. This exhausts real
uniformly finite-mode behavior by applying the theorem in the moving frame.

### Regularity and tangency

No extra Sobolev or Yudovich hypothesis is needed for Cycle 226's constructed
orbits. A finite Fourier polynomial is smooth in space. Its Fourier equations
are a finite polynomial ODE, giving a unique local analytic coefficient curve.
The exterior equations make its zero extension an exact classical Euler
solution, and a local interval suffices for Theorem 5.1.

For a reduced algebraic variety, `D_F I(X) subset I(X)` implies local flow
invariance: for finite ideal generators, their derivatives are an
ideal-linear system along the flow. This remains valid at singular points.
The criterion is therefore adequate in the fixed-support algebraic setting.

## Equilibrium variety

The easy inclusion is algebraic. If active modes lie on one origin-line, every
wedge vanishes; if they lie on one origin-circle, every reciprocal-length
difference vanishes. Hence every coordinate subspace `L_T` indexed by a
degenerate `T` lies in the zero set of all Euler quadrics over `R` or `C`.

The converse regards a point of the equilibrium zero set as a constant
finite-mode Euler solution and invokes support classification. It is therefore
proved for Fourier-real points by the printed proof, but valid for all complex
points only through the asserted complex extension or a new proof.

Subject to that extension, the decomposition is correct. Maximal degenerate
supports give maximal coordinate subspaces, and

\[
 \sqrt{I_{eq}(S)}=
 \bigcap_{T\in M(S)}(z_k:k\in S\setminus T)
\]

follows from the complex Nullstellensatz. Without the extension, only the
Fourier-real set-theoretic classification and corresponding real-radical
conclusion are justified; the complex coordinate-subspace decomposition is
not a consequence of the cited real proof.

## Correction

Cycle 226 now distinguishes the proved real result from the asserted complex
extension, narrows the claim to fixed support, makes the zero-mean
normalization explicit, and makes the complex equilibrium decomposition
conditional. The route remains closed for real Euler candidates, which are
the ones relevant to the Navier--Stokes program.
