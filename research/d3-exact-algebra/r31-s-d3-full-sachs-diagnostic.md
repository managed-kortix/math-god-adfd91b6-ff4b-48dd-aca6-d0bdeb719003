# `R31-S:D3` full Sachs diagnostic: still open

This note supplements
`r31-s-d3-diamond-territory-packet.md`.  It reconstructs both parts of

```text
Psi(t)=i^(-n)det(itI-A)=R(t,y)+iI(t,y)
```

for all 14 one-side marked incidence records (28 after reflection).  It is a
diagnostic, **not** a proof of

```text
sigma(Theta(1,2,2)+T^3)>3.
```

## Exact formula regenerated

For independent positive core activities `z_v=t+y_v`, the verifier enumerates
all simple cycles and all vertex-disjoint cycle families and applies

```text
Psi_G(z)=sum_C prod_(Q in C)(-2 i^(-|Q|)) Z_(G-V(C))(z),       (1)
```

where `Z` is the positive matching partition.  This constructs the full real
and imaginary sparse integer polynomials without importing the earlier
imaginary-only result.  Depending on the record, the raw real polynomial has
151 through 196 monomials.  After activity expansion the exact audit checks
39,959 real and 11,504 imaginary signed coefficients in total.

## Corrected defect elimination

Exactly five records have the exceptional positive imaginary coefficient
`+6y`:

```text
chain2+direct(A,x),
chain2+direct(B,x),
chain2+direct(x,x),
chain3(x),
fork(x,split).
```

For each, isolate its defect variable and write

```text
R=A+By,             I=P+Qy.                                   (2)
```

The signed-dictionary audit proves that `P` is coefficientwise negative and
that `Q` has exactly one positive coefficient, the constant `+6`, together
with many negative coefficients.  On the boundary `I=0`, the corresponding
numerator of `R` is

```text
AQ-BP.                                                         (3)
```

Equation (3) has coefficients of both signs in every one of the five records.
Aggregated over them, the exact expansion has 179,605 positive and 42,651
negative coefficients.  Therefore neither the imaginary carrier alone nor a
naive coefficientwise defect elimination proves `I>=0 => R<0`.

A technical warning matters here: applying unary `+` to a Python
`collections.Counter` silently deletes zero and negative counts.  Such a
representation falsely makes `P` empty and makes mostly positive pieces look
positive.  The committed diagnostic uses ordinary signed dictionaries for
all elimination steps and explicitly authenticates the mixed sign of (3).

As a second exact guard, the verifier records the full one-variable defect
slice obtained by setting every activity to `t` except the defect activity,
which is `t+y`.  Thus it checks four coefficient tuples `(R_0,R_1,I_0,I_1)`
for `R=R_0+yR_1` and `I=I_0+yI_1` in each of the five exceptional records.
These are diagnostics only: the slice does not certify the full independent-
activity domain and is not promoted to a phase or energy theorem.

## What remains missing

The finite computation does **not** establish any of the following:

1. the semialgebraic implication `I>=0 => R<0` over the legal activity domain;
2. the winding/continuous-argument behavior if the curve crosses an axis;
3. the required signed Coulson phase-area inequality; or
4. `sigma(D+T^3)>3`.

Even a future proof of item 1 would not by itself prove item 3.  The pointwise
half-plane statement and the integrated energy statement must remain
separate.

## Fail-closed diagnostic

Run

```text
python3 research/r31-s-d3-full-sachs-diagnostic.py
python3 -O research/r31-s-d3-full-sachs-diagnostic.py
```

Both commands print the exact finite audit and deliberately exit `1`.  They
require identical normal/optimized output.  A zero exit would be a semantic
failure: this diagnostic preserves the authoritative status `R31-S:D3 OPEN`.
