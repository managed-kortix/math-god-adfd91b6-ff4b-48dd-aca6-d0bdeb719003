# Cycles 214--215: finite majorant artifact upgraded to a full 2D enclosure

The selected datum is

\[
 \psi_0=\cos x+\cos y+\cos(x+y),\qquad \mu=1,
 \qquad 0\leq t\leq 1/64.
\]

Cycle 214 first published the rational slab data as reusable components. Cycle
215 supplies the missing exact enclosure theorem and upgrades the artifact to
`cycle215-full-2d-enclosure-certificate.json`. It encloses the full smooth 2D
Navier--Stokes solution through `T=1/64`; it makes no amplification claim.

## What is replayed

* The retained square is `0<|k|_infinity<=2`, and its first entry equals the
  datum coefficient by coefficient.
* There are 64 slabs of width `1/4096`, with exact rational entry, Picard tube,
  endpoint, and low-mode remainder boxes.
* Shells 3 through 31 have slab-specific entry, tube, and endpoint bounds.
  Shells `n>=32` obey `(1/1024)(33/32)^(-n)`.
* The checker recomputes every finite cap margin, the complete quadratic ray,
  all low-mode remainders, and both inclusions in (215.2).
* Endpoint velocity and gradient bounds include the retained modes, every
  explicit shell 3 through 31, and the infinite geometric cap. Cubature thus
  encloses the full 2D PDE endpoint rather than a truncated arithmetic object.

The theorem-level justification, including simultaneous first contact,
non-strict cap faces, the joint retained/shell bootstrap, and Picard inclusion,
is `cycle-215-exact-2d-enclosure-theorem.md`.

## Replay

```text
python validate_cycle214.py cycle215-full-2d-enclosure-certificate.json
```

A successful replay prints `PASS FULL 2D PDE ENCLOSURE Cycle 215` and
`NO AMPLIFICATION CLAIM`. The old `PASS COMPONENTS` interpretation is retired.
