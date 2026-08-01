# Cycle 214: finite majorant components

The selected datum is

\[
 \psi_0=\cos x+\cos y+\cos(x+y),\qquad \mu=1,
 \qquad 0\leq t\leq 1/64,
\]

with the normalized Fourier-vorticity convention of Cycle 212. The rational
artifact `cycle214-components-certificate.json` replays to `PASS COMPONENTS`.
It is not a full-PDE enclosure and makes no amplification claim.

## What is replayed

* The retained square has `0<|k|_infinity<=2` (24 complex coefficients), and
  the first entry is checked coefficient-by-coefficient against the datum.
* The finite interval calculation has 64 slabs of width `1/4096`, with exact
  rational entry, Picard tube, endpoint, and low-mode remainder boxes.
* Shells 3 through 31 have slab-specific conditional head bounds. Shells
  `n>=32` use the formal Cycle 213 cap
  `z_n<=(1/1024)(33/32)^(-n)`.
* The checker recomputes retained shell domination, conditional cap-face
  margins, low-mode majorants, and every finite Picard inclusion. It also
  replays a separate retained-plus-geometric-cap norm/cubature calculation.

The formal endpoint cubature calculation is deliberately coarse. It omits the
explicit shells 3 through 31 and therefore is not a norm enclosure for the
conditional shell tube, much less for a Navier--Stokes solution. It is retained
only as an arithmetic replay component; no analytic or PDE conclusion is drawn
from its stored interval.

## Why this is not `PASS FULL`

The artifact does not prove a cutoff-uniform Galerkin existence theorem and
passage to a strong enough infinite limit, nor an infinite-dimensional
first-exit argument identifying the conditional shell tube with the full PDE.
It also does not independently bind the slab head hypotheses and geometric cap
inheritance to such a limit. Finally, the three stored ray coefficients only
replay the Cycle 213 polynomial-majorant formula; the artifact does not supply
an independent proof object establishing that formula for every infinite shell.

These are theorem-level obligations, not numerical tolerances. Until they are
proved and made fail-closed validator inputs, the strongest sound result is a
finite Fourier calculation plus conditional shell-majorant components.

## Replay

Run

```text
python validate_cycle214.py cycle214-components-certificate.json
```

A successful replay prints `PASS COMPONENTS Cycle 214` and
`NO FULL-PDE OR AMPLIFICATION CLAIM`.
