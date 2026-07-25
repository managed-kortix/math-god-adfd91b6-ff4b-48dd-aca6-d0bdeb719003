# Notebook

Bounded scout is queued to compute the exact initial derivative of the cubed
`L^3` norm for rational interacting triads and locate pressure-driven growth
candidates before any interval PDE validation.

## Bounded scout tick 2

For smooth divergence-free data,

`d/dt ||u||_3^3 = 3 int p u.grad|u| - 3 nu int |u|(|grad u|^2+|grad|u||^2)`.

Transport cancels exactly. For finite triad data, pressure has finite
frequencies, but `|u|u` generally has infinite Fourier support. Therefore a
Galerkin projection of `|u|u` back to the original triad does not compute the
exact derivative. The next test must rigorously integrate the unprojected
pointwise field at all pressure frequencies.
