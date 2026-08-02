# Cycle 253: fixed-orbit energy-level variational audit

## Verdict: CONNECTED-LEVEL MEMBERSHIP IS NOT PROVED

Let `s>2`, let `omega_* in H^s(T^2)` be smooth and mean zero, and use the
right pullback convention

\[
 \mathcal O^s(\omega_*)=
 \{\omega_*\circ\eta^{-1}:\eta\in\operatorname{Ham}^{s+1}(\mathbb T^2)\}.
\]

Write

\[
 E(\omega)={1\over2}\|K\omega\|_2^2,
 \qquad J(\omega)=\|K\omega\|_3^3,
 \qquad K=\nabla^\perp\Delta^{-1}.
\]

Cycle 251 supplies `omega_0,omega_1 in O^s(omega_0)` with equal positive
energy and `J(omega_0)^(1/3)>2J(omega_1)^(1/3)`. This does not imply that they
belong to one connected component of
`O^s(omega_0) cap E^-1(E(omega_0))`.

The Hamiltonian orbit is path connected, but a level set of a continuous
function on a path-connected space need not be path connected. The available
Hamiltonian isotopy need not remain on the energy shell.

## Why scalar energy normalization does not answer the question

Let `h_tau`, `0<=tau<=1`, be a smooth Hamiltonian isotopy from the identity to
the Cycle 251 endpoint map `h`, and set

\[
 \rho_\tau=\omega_0\circ h_\tau.
\]

Every `rho_tau` is smooth, mean zero, and equimeasurable with `omega_0`.
Continuity of composition in `H^s` and boundedness of `K:H^s_0 -> H^{s+1}`
show that

\[
 e(\tau):=E(\rho_\tau)>0
\]

is continuous. Since Cycle 251 gives `e(0)=e(1)=E_0`, one might define

\[
 a(\tau)=\sqrt{E_0/e(\tau)},
 \qquad \Omega_\tau=a(\tau)\rho_\tau.                 \tag{253.1}
\]

Then `E(Omega_tau)=E_0` and the endpoints are unchanged. But

\[
 \Omega_\tau=(a(\tau)\omega_0)\circ h_\tau,            \tag{253.2}
\]

so this path lies in the union of orbits of the scalar multiples
`a(tau) omega_0`, not generally in the one fixed orbit `O^s(omega_0)`.
Vorticity Casimirs change whenever `a(tau) != 1`. Thus

\[
 \boxed{\text{Cycle 251 does not prove that its endpoints lie in one connected
 component of }\mathcal O^s(\omega_0)\cap E^{-1}(E_0).} \tag{253.3}
\]

## What a connecting path would imply

If a continuous path `gamma:[0,1] -> O^s(omega_*) cap E^-1(E_0)` joins the
Cycle 251 endpoints, then `J o gamma` is continuous and

\[
 J(\gamma(0))^{1/3}>2J(\gamma(1))^{1/3}.               \tag{253.4}
\]

The same connected energy-level component would therefore contain the full
intermediate interval of velocity `L^3` values between the endpoint values.
No local extremum is needed to obtain the gap. If the component were compact
in a topology in which `J` is continuous, it would have a maximum and minimum
whose ratio is already greater than two. Such compactness is not available for
a smooth infinite-dimensional coadjoint orbit.

For a fixed smooth orbit the vorticity distribution fixes every `L^p` norm.
In particular, with normalized Haar measure and mean zero,

\[
 \|K\omega\|_3\le C_3\|K\omega\|_{W^{1,2}}
 \le C_3'\|\omega\|_2,                                \tag{253.5}
\]

uniformly on the orbit. At positive fixed energy,

\[
 \|K\omega\|_3\ge\|K\omega\|_2=\sqrt{2E_0}.          \tag{253.6}
\]

Therefore `J` is bounded above and bounded away from zero on every fixed
`L^2` coadjoint orbit intersected with a positive energy shell. Velocity `L^3`
is not unbounded there. The bounds do not imply attainment: the orbit or its
energy slice is noncompact and need not be closed in the relevant weak or
strong topology, so maximizing and minimizing sequences may escape by mixing.

Across different orbits, fixed energy alone does not bound velocity `L^3`:
two-dimensional concentration can keep velocity `L^2` fixed while making its
`L^3` norm arbitrarily large. That is different from unboundedness on one
coadjoint orbit.

## First variations and constrained critical points

Let `psi=Delta^-1 omega`, `u=K omega=grad^perp psi`, and let `chi` be a smooth
mean-zero Hamiltonian generator. The tangent induced by pullback is, up to one
convention-dependent global sign,

\[
 \delta_\chi\omega=\{\chi,\omega\}.                    \tag{253.7}
\]

The energy derivative is

\[
 dE_\omega(\delta\omega)=-\int_{T^2}\psi\,\delta\omega,
 \qquad
 dE_\omega(\delta_\chi\omega)
   =-\int_{T^2}\chi\,\{\omega,\psi\}.                 \tag{253.8}
\]

Thus, at a regular point, the realized tangent space to the energy slice is the
kernel of the last linear functional. It is a codimension-one hyperplane in the
orbit tangent space unless `{omega,psi}=0`; at a steady Euler vorticity, energy
is critical on the entire coadjoint orbit and the level set can be singular.
This statement is local: it uses a Sobolev chart for the Hamiltonian
diffeomorphism group and the implicit-function theorem. It does not assert that
the global orbit is embedded or closed in `H^s`.

The cubed `L^3` functional is Frechet differentiable because
`z -> |z|^3` is `C^1`. If

\[
 q=|u|u,
 \qquad A_\omega=-\Delta^{-1}\operatorname{curl}q,
\]

then, with `curl q=partial_1 q_2-partial_2 q_1`,

\[
 dJ_\omega(\delta\omega)=3\int_{T^2}A_\omega\,\delta\omega,
 \qquad
 dJ_\omega(\delta_\chi\omega)
   =3\int_{T^2}\chi\,\{\omega,A_\omega\}.             \tag{253.9}
\]

At a regular point of the energy restriction, a constrained critical point of
`J` therefore satisfies the exact multiplier equation

\[
 \boxed{\{\omega,\,3A_\omega+\lambda\psi\}=0}          \tag{253.10}
\]

for some real `lambda`, in the distributional sense. On each connected regular
vorticity contour, (253.10) says that `3A_omega+lambda psi` is constant. For
Morse vorticity this constant must be compatible across the measured Reeb
graph. At a steady point where (253.8) vanishes identically, the ordinary
one-constraint multiplier theorem is not applicable; criticality requires
`{omega,A_omega}=0` directly, followed by second variation for an extremum
claim. Equation (253.10) characterizes candidates only; it proves neither
existence nor attainment of global extrema.

## Accessibility: two Hamiltonian vector fields

An arbitrary Hamiltonian path in the coadjoint orbit has

\[
 \partial_t\omega=\{\chi_t,\omega\},                  \tag{253.11}
\]

where `chi_t` is freely prescribed. Tangency to the fixed energy shell imposes
only the scalar condition

\[
 \int_{T^2}\chi_t\{\omega,\psi\}=0.                   \tag{253.12}
\]

Modulo generators in the stabilizer `{chi,omega}=0`, this leaves an
infinite-dimensional family of directions.

Euler is much narrower. Its Lie--Poisson Hamiltonian is `E`, and its vector
field is

\[
 X_E(\omega)=\{\psi,\omega\},
 \qquad \chi_t=\psi_t=\Delta^{-1}\omega_t             \tag{253.13}
\]

up to the same global sign convention. There is no control choice. Through
each smooth initial vorticity there is one global smooth two-dimensional Euler
trajectory, plus time reversal. Condition (253.12) is automatic by
antisymmetry, but almost every tangent direction allowed by (253.12) is not
`X_E`.

Accordingly:

- membership in one Hamiltonian coadjoint orbit is only rearrangement
  accessibility;
- membership in one connected fixed-energy level, if proved, is only
  energy-preserving Hamiltonian-path accessibility;
- Kelvin circulation on matched material contours and harmonic impulse are
  additional necessary endpoint data;
- even all those conditions do not imply Euler accessibility;
- the final requirement is the pointwise self-induced constraint (253.13), or
  equivalently equality with the unique Euler solution at the proposed time.

Cycle 251 proves the static Hamiltonian pair but not connected-level
membership, and a fortiori not Euler accessibility. The fixed-orbit
connected-level question remains a genuine topological/variational problem;
the self-induced vector-field gate remains the decisive dynamical obstruction.
