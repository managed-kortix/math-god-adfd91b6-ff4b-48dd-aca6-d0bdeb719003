# Cycle 63: complete-tail and boundary certificate

## Durable verifier

`verify_cycle63_complete_tail.py` evaluates the complete restricted Vasyunin
Gram through the existing `certify_complete_gram.RestrictedGram` implementation.
It subtracts the finite `(1,M)` prefix cell by cell, retaining exact integer and
rational coefficients while enclosing logarithms and all linear algebra with
Arb. The four-window output at 192-bit precision is:

| window | `Omega_infinity` | boundary Schur | full `R` |
|---|---:|---:|---:|
| `[98,99)` | `0.030162988363064539935` | `0.045615062017116374369` | `0.075778050380180914304` |
| `[219,231)` | `0.026726387237328858507` | `0.031679021351980235849` | `0.058405408589309094356` |
| `[220,231)` | `0.027337641721077888943` | `0.031062663964177908238` | `0.058400305685255797182` |
| `[222,226)` | `0.028763566006604881443` | `0.033116652858458946834` | `0.061880218865063828278` |

For each row, Arb verifies both

\[
R=\Omega_\infty+\text{boundary Schur}
\]

and an independent direct complete-Gram projection after subtraction of the
optimal below-`M` reserve `W_M`. The unit test compares all twelve displayed
values and checks the two full-`R` identities.

The completed residual pays the lag-two sufficient target on `[219,231)`,
`[220,231)`, and `[222,226)`. It does not pay that stronger sufficient target
on the physically positive singleton `[98,99)`, where endpoint dependence is
essential. Pure tail by itself pays only `[220,231)` among these four windows.

## Cycle 62 correction

Re-evaluation from the exact physical definitions gives

\[
\beta_2+\delta_{220,231}
=0.0186371960000083830592811401588\ldots,
\]

not `0.0186372067026351066091997...`. The Cycle 62 constant and resulting
margin are corrected accordingly. This remains a fixed finite diagnostic. It
is not an asymptotic theorem and makes no claim about the Riemann hypothesis.

## Scale obstruction and explicit weak witness

Normalized dilation copies the even reciprocal subsystem exactly, but the
doubled physical system adds odd rows and an odd Möbius score remainder. Thus
no positive ratio between consecutive dyadic innovations follows from Gram
interlacing or dilation alone. A valid conditional inequality is

\[
\sqrt{I_{[2N,4N]}}\ge
(\sqrt{I_{[N,2N]}}-\mathcal R_N)_+,
\]

where `R_N` explicitly measures score noncovariance and failure of the
constraint kernels to intertwine. Bounding this remainder is another
Möbius--Vasyunin correlation problem.

A separate two-cell spline representer turns jump evaluation into a bounded
dual functional on the affine-cell space. Two well-separated squarefree
composites in `[B,2M)` yield an unconditional asymptotic certificate
`Omega_infinity >> 1/M^2`. This is far below the constant-scale finite values
and cannot pay fixed-strength renewal, but it proves qualitative tail
separation without a complete Gram solve.
