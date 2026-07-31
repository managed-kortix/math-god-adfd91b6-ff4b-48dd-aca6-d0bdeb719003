# Five-vertex rank-four kernels: exact coarse three-color sieve

## Scope and result

For kernels 9--12, use pair order

`01,02,03,04,12,13,14,23,24,34`

and write `m_uv` for the physical bundle multiplicity and `q_uv` for its
number of odd paths. Thus `0<=q_uv<=m_uv`; a doubled bundle with `q_uv=2`
contains two distinct odd paths.

The exact equilateral three-color DNN sieve certifies 370 of the 378 genuine
vertex-automorphism orbits and leaves exactly eight:

| kernel | canonical physical row |
|---:|:---|
| 9 | `(0,0,0,1,1,0,1,1,0,0)` |
| 9 | `(0,0,1,1,1,0,1,1,0,0)` |
| 9 | `(0,0,1,1,1,0,1,2,0,0)` |
| 9 | `(0,0,1,1,1,0,2,1,0,0)` |
| 10 | `(0,0,0,1,1,1,1,1,1,0)` |
| 10 | `(0,0,1,0,1,1,1,1,1,0)` |
| 11 | `(0,0,1,1,0,0,1,1,0,0)` |
| 11 | `(0,0,1,1,1,1,1,1,0,0)` |

This artifact itself is a sieve statement. The separate exact frontier theorem
`five-vertex-residual-closure-theorem.md` closes all eight residual orbits.

## Exact canonical physical costs

Take three unit vectors at mutual angle `2*pi/3`. Equal colors have endpoint
correlation `1`; unequal colors have correlation `-1/2`. Exact elimination of
a path of length `l` gives

`f_l(r)=l tan^2(acos((-1)^l r)/(2l))`.                 (1)

For a fixed parity and endpoint correlation, this decreases when the length is
increased by two. A monochromatic odd path has infinite cost and is therefore
forbidden. A monochromatic even path has cost zero. For a bichromatic bundle,
the exact worst physical cost is:

| `(m,q)` | canonical physical lengths | cost |
|:---:|:---:|:---:|
| `(1,0)` | `(2)` | `2/3` |
| `(1,1)` | `(1)` | `1/3` |
| `(2,0)` | `(2,2)` | `4/3` |
| `(2,1)` | `(1,2)` | `1` |
| `(2,2)` | `(1,3)` | `1/3+a` |

Here

`a=3 tan^2(pi/18)`                                           (2)

is the length-three odd cost. The last row is essential: in a simple
subdivision, two paths in one doubled bundle cannot both have length one.
Hence the physical odd--odd canonical lengths are `(1,3)`, not the fictitious
multigraph lengths `(1,1)`. Longer same-parity paths only lower these costs.

The parameter `a` is treated algebraically. It is the unique root in
`(93/1000,94/1000)` of

`a^3-27a^2+99a-9=0`.                                        (3)

Equation (3) follows from `tan(3*pi/18)=tan(pi/6)=1/sqrt(3)` and the triple
angle formula after putting `a=3 tan^2(pi/18)`. The derivative of the left
side is positive on the isolating interval, so the root is unique there.

## Genuine exhaustive enumeration

The four kernel multiplicity vectors and independently regenerated ledgers are

| kernel | physical rows | automorphisms | genuine orbits |
|---:|---:|---:|---:|
| 9 | 108 | 2 | 63 |
| 10 | 192 | 2 | 120 |
| 11 | 144 | 1 | 144 |
| 12 | 256 | 8 | 51 |
| total | 700 | | 378 |

For every canonical orbit representative, the verifier enumerates all
`3^5=243` labeled colorings. It rejects a coloring if any odd physical path is
monochromatic, sums the bundle costs above as an exact pair `p+q*a`, and keeps
the exact minimum. Algebraic comparisons use rational bisection of the isolated
root (3); no decimal or floating-point acceptance test occurs. An orbit is
certified exactly when its minimum is at most the tetracyclic excess budget
three. This gives the disjoint partition

`378 = 370 certified + 8 residual`.                          (4)

The construction is DNN-valid: the branch matrix is explicitly the Gram
matrix of the three equilateral unit vectors, and path elimination supplies
internal vectors with total cost (1). Thus every row certified in (4) has
`kappa(H)-|E(H)|<=3`. The usual LTZ/DNN and trace calculation then gives
`s^+(H)>=|V(H)|`, including arbitrary rooted-tree attachments by additivity.

## Intersection with the existing 96 fixture

The verifier digest-locks and loads
`research/fixtures/rank-four-five-vertex-orbits.json`. Its exact residual-key
set has 96 members. Intersecting that set with the independently computed
eight-row sieve residual gives exactly two rows:

| kernel | canonical physical row |
|---:|:---|
| 11 | `(0,0,1,1,0,0,1,1,0,0)` |
| 11 | `(0,0,1,1,1,1,1,1,0,0)` |

Therefore the coarse sieve certifies 94 of the old 96 residual targets. The
other six members of the eight-row sieve residual were in the old 282-member
incidence section. That section explicitly made no analytic claim, so there is
no contradiction: the new fixture extends it with genuine exact cost and
coloring data rather than promoting its historical labels.

## Fail-closed artifacts

Run

```text
python research/rank-four-five-vertex-three-color-verifier.py
python -O research/rank-four-five-vertex-three-color-verifier.py
```

The verifier rebuilds all 700 physical rows, all four exact automorphism
groups, all 378 orbit representatives, all coloring minima, the eight residual
keys, and the two-key intersection with the old 96 fixture. The extended
fixture is

`research/fixtures/rank-four-five-vertex-three-color-sieve.json`.

Each of its 378 records stores the kernel, canonical row, exact minimum
`[numerator,denominator,a_coefficient]`, first labeled minimizing coloring,
sieve status, and old-96 membership. The verifier rejects nine hostile changes,
uses explicit exceptions instead of `assert`, digest-locks both fixtures, and
requires byte-identical normal and optimized output.

The audit is valid for the stated 370-orbit DNN sieve. Its eight displayed
residuals are closed by `five-vertex-residual-closure-theorem.md` and
`research/rank-four-five-vertex-residual-closure-verifier.py`; they are retained
here as the exact output of this coarse equilateral-coloring stage.
