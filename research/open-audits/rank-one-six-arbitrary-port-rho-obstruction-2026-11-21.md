# Arbitrary-port obstruction to a uniform negative-part bridge-root bound

Date: 2026-11-21. Status: **EXACT ROUTE OBSTRUCTION / NONPROMOTIONAL**.

## Claim boundary

This note refutes the proposed auxiliary assertion

```text
rho_br^2 >= delta_5 := sqrt(5)-2
```

for every marked hostile rank-`(1,6)` bridge. Here `rho_br` is the unique
positive eigenvalue of `E-(A_U)_- direct_sum (A_R)_-`, equivalently the
positive marked-resolvent crossing defined below. It is **not** a surplus
notation and is **not** an interpolation parameter.

This is not a counterexample to `sigma(G)>=0`, to the rank-seven graph theorem,
or even to the joint sufficient condition
`sigma(R)+rho_br^2>=-sigma(U)`. The witness has `sigma(R)=11`, so it has very
large reserve. The obstruction applies because the physical hostile reduction
allows the bridge port to be an arbitrary vertex. The marked vertex below is
not a leaf. A leaf-port-only lower bound is neither proved nor refuted here;
even if true, it would not cover the inherited arbitrary-port residue.

## The exact family and the finite witness

For an integer `t>=1`, let `U_t` be obtained from `C_5` by adjoining exactly
`t` pendant leaves at each cycle vertex. Mark one cycle vertex `y`. Let
`R=K_5` and mark any vertex `x`. Thus

```text
|V(U_t)|=5(t+1),  |E(U_t)|=5(t+1),  beta(U_t)=1,
|V(R)|=5,         |E(R)|=10,        beta(R)=6.
```

The unique cycle of `U_t` has length `5=1 mod 4`, so this is a hostile
unicyclic side. The marked port `y` has degree `t+2`, not degree one. Joining
`x` and `y` by one edge gives a connected rank-seven graph whose new edge is a
physical `1|6` bridge. In particular it is a legitimate outer marked
rank-`(1,6)` schema (the `k=1` unit-star profile); no claim is made that every
extra packet-specific ownership restriction selects it.

The finite witness used below is `t=500`.

## Exact spectral and resolvent formulas

Put

```text
C={2, (sqrt(5)-1)/2, (sqrt(5)-1)/2,
      -(sqrt(5)+1)/2, -(sqrt(5)+1)/2}.
```

Fourier decomposition on the five cycle vertices reduces the nonzero spectrum
of `U_t` to the five symmetric matrices

```text
Q_c = [[c,sqrt(t)],[sqrt(t),0]],       c in C.
```

All other `5(t-1)` eigenvalues are zero. Consequently

```text
chi_Ut(X)=X^(5(t-1))
          (X^2-2X-t)
          (X^4+X^3-(2t+1)X^2-tX+t^2)^2.              (1)
```

For `c in C`, define

```text
m_c=(sqrt(c^2+4t)-c)/2 > 0,
a_c=m_c/(2m_c+c).
```

The negative eigenvalue of `Q_c` is `-m_c`, and the squared cycle-coordinate
of its unit eigenvector is `a_c`. Hence, for every `z>0`, the marked negative-
part resolvent at a cycle vertex is exactly

```text
n_Ut(z)=(1/5) sum_{c in C} ((1-a_c)/z+a_c/(z+m_c)).    (2)
```

Since the negative part of `A(K_5)` is the orthogonal projector onto the
four-dimensional `-1` eigenspace,

```text
n_R(z)=1/(5z)+4/(5(z+1)).                              (3)
```

Let `N_U=(A_Ut)_-`, `N_R=(A_R)_-`, and let `E` be the marked cross-edge
matrix. The matrix

```text
Z=E-(N_U direct_sum N_R)
```

has at most one positive eigenvalue. Its positive eigenvalue `rho_br` is the
unique positive solution of

```text
n_Ut(rho_br)n_R(rho_br)=1.                             (4)
```

Indeed, the matrix determinant lemma gives the crossing equation. Each
resolvent is positive and strictly decreasing on `(0,infinity)`, their product
is strictly decreasing, tends to infinity at zero here (both marks have
nonzero kernel projection), and tends to zero at infinity. Therefore, for
any `s>0`,

```text
n_Ut(s)n_R(s)<1  implies  rho_br<s.                    (5)
```

## Exact finite comparison

Set `t=500` and `s=sqrt(delta_5)`. Substitution into (2)--(3), with exact
real-algebraic arithmetic, gives

```text
n_U500(s)n_R(s)<1.                                     (6)
```

The companion verifier proves (6) by isolating every square root over rational
intervals and evaluating the interval extension using rational arithmetic; no
decimal value participates in acceptance. By (5),

```text
rho_br^2 < s^2 = sqrt(5)-2.                            (7)
```

For orientation only, `rho_br^2` is approximately `0.2356112140`, whereas
`delta_5` is approximately `0.2360679775`.

The same exact verifier checks hostility quantitatively. From the five positive
roots of the blocks `Q_c`,

```text
sigma(U_t)=s+(U_t)-|V(U_t)|
          =(1/2) sum_{c in C} c sqrt(c^2+4t).           (8)
```

At `t=500`, exact algebraic isolation gives `sigma(U_500)<0` (orientation only:
about `-6.98e-6`). Also `sigma(K_5)=4^2-5=11`. Therefore

```text
sigma(R)+rho_br^2 > 11 > -sigma(U_500),                (9)
```

where the verifier also proves `-1<sigma(U_500)<0` exactly. Thus the joint
reserve-plus-root certificate succeeds by a huge margin: (7) is only a
counterexample to the proposed standalone uniform root floor.

## Audit boundary relative to finite scouts

The existing generated common-center unit-star scout marks payloaded selected
arms at a leaf, so it does not test this arbitrary-cycle-port mutation. The
canonical-kernel scout tests cycle hubs, but only up to twenty leaves at one
hub, not the symmetric 500-leaf-per-cycle-vertex family. Therefore its
no-negative finite outputs do not imply (or contradict) the false universal
root floor. This note does not change any finite scout's stated result.

## Reproduction

Run

```bash
python3 research/rank-one-six-arbitrary-port-rho-obstruction-verifier.py
python3 -O research/rank-one-six-arbitrary-port-rho-obstruction-verifier.py
```

The outputs must be byte-identical.
