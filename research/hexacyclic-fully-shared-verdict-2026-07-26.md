# Independent verdict on the fully shared hexacyclic censuses

## Verdict

**PASS.** Taken together with the already established consecutive-interval
cycle-splitting construction, the two exact censuses, the common-cut sacrifice
lemma, and the saturated-hub interval arguments cover every fully shared
`TTTTTQ` and `TTTTPP` incidence tree. I found no uncovered canonical incidence
tuple and no acceptance that uses a packet estimate without its stated retained-
incidence hypothesis.

This verdict is only for the fully shared residuals. It does not promote the
disconnected-cluster notes, the sharp-DNN reduction, or a global hexacyclic
theorem beyond their separately stated status.

## Reproduction and independent checks

I ran, unchanged,

```bash
python research/hexacyclic-tttttq-incidence-census.py
python research/hexacyclic-ttttpp-incidence-census.py
```

The first script reproduced the color-preserving `TTTTTQ` totals

```text
q=3:   1, 6, 20, 27, 14 = 68
q=4:   1, 6, 20, 28, 15 = 70
q>=5:  1, 6, 20, 28, 16 = 71
```

by cut count `c=1,...,5`. It resolved respectively `67`, `69`, and `70`
trees by an ordinary one-cycle split and returned only the bouquet in every
capacity regime. I separately compared the center-rooted color code against
the brute-force canonical edge representative under `S5 x S_c`, and rechecked
all branch-count assertions used by the acceptance test.

The second script reproduced

```text
TTTTPP: 1, 9, 40, 62, 38 = 150
SAFE-resolved: 0, 9, 40, 62, 37 = 148.
```

It recorded all `900` cycle choices and `337` accepted splits. I independently
recomputed every accepted numerical sum, its strictness flag, and the retained
internal cuts used by the stronger packet hypotheses. The only two trees with
no SAFE ordinary split were exactly the asserted bouquet and saturated
pentagon hub.

## Acceptance-ledger audit

For `TTTTTQ`, deleting an internal `Q` leaves nonempty connected all-triangle
branches. Deleting an internal triangle leaves one branch containing `Q`.
The four possible cases used by the script are sound:

1. A singleton hostile `Q` has loss less than one, while the other four
   triangles occupy at most two branches and hence one branch contains `TT`,
   with surplus greater than one.
2. A `TQ` branch is positive for every parity of `q`.
3. A generic `TTQ` branch is nonnegative, and another nonempty all-triangle
   branch supplies strictness.
4. Larger `T^kQ` branches and all remaining all-triangle branches are covered
   by the established lower-rank qualitative results.

The regimes `q=3`, `q=4`, and `q>=5` are exhaustive because an incidence tree
has at most five cut nodes. Keeping `Q` distinguished when `q=3` overcounts
uncolored six-triangle shapes but cannot omit one.

For `TTTTPP`, the executable does not infer a strong estimate from colors
alone. In particular, it checks a retained common cut for the two triangles in
`TTP`, checks an intersecting retained triangle pair in `TTTP`, and applies the
`TTT`, `TTTT`, `TPP`, and shared `PP` estimates only to an actual connected
component after the split. Generic tricyclic branches receive only `>=0`, and
generic tetracyclic or pentacyclic positivity is never used to cancel a
negative singleton pentagon. Thus the `148` SAFE resolutions require no
external tree cost and close with a genuinely positive branch sum.

## Exact exceptions and closure

The unique `TTTTTQ` ordinary-split exception, in every capacity regime, is

```text
c=1: ((0,6),(1,6),(2,6),(3,6),(4,6),(5,6)).
```

It is the six-cycle bouquet. The common-cut sacrifice applies: open `Q` and
one designated triangle at private non-cut vertices. Their path remnants keep
the common cut, the other four triangles remain one shared-cut cluster with
surplus `>3`, and the two opened tree territories cost exactly two. Hence the
resulting surplus is `>1`, including the symbolic case `Q=T`.

The two `TTTTPP` ordinary-split exceptions are

```text
c=1: ((0,6),(1,6),(2,6),(3,6),(4,6),(5,6));

c=5: ((0,6),(4,6),(1,7),(4,7),(2,8),(4,8),
      (3,9),(4,9),(4,10),(5,10)).
```

The first is again the bouquet. Opening private vertices on the two pentagons
leaves the four-triangle bouquet, so the same `>3-2>1` sacrifice closes it.

In the second tuple, pentagon `4` is saturated at five distinct degree-two
cuts, with four triangle petals and pentagon `5` as the fifth petal. It cannot
be privately opened. Around the hub, either neighbor of the unique pentagonal
mark is a triangular mark. Merge that adjacent pair into one proper interval
and give the other three marks separate proper intervals. The established
interval construction assigns every marked vertex once and every hanging tree
to its unique attachment, producing induced branch territories

```text
TP + T + T + T.
```

The arbitrary-connector `TP` estimate gives `>1-delta`, where
`delta=sqrt(5)-2<1`, and the three triangle packets are strict positive.
Therefore this split has positive total surplus. No cyclic-order subcase is
missing: with only one pentagonal petal, both cyclic neighbors of its mark are
triangular, including when all five marks occupy all five hub vertices.

## Boundary of the verdict

The census notes correctly describe the hub lemmas as external structural
steps rather than SAFE script acceptances. The proof is complete only when the
general consecutive-interval construction is cited with explicit ownership of
marked vertices and attached trees. That construction is already stated in
`all-pentacyclic-cacti/paper.tex`; under it, the two displayed exception repairs
are valid. Without that construction, the saturated `TTTTPP` hub tuple above
would be the sole gap. With it, there is no fully shared gap.
