# Rank-seven edge opening: marked credit and the finite short-support residue

## Scope

Let `G` have one rank-seven cyclic block, let `K` be its suppressed kernel, and
write its physical paths as `P_e`, of lengths `q_e`.  Thus

```text
|E(K)|=|V(K)|+6,     2<=|V(K)|<=12.
```

This note gives an exact way to use the completed connected rank-six theorem
without importing millions of rank-seven Gram certificates.  It proves a good
edge theorem whenever one marked rank-six owner has enough endpoint credit,
shows that every path of length at least three automatically has enough path
credit, and reduces every possible failure to a finite set of support families or
to a one-ear extension of a typed non-DNN rank-six owner.  It does not prove
that the finite short-support class is empty.

## 1. Marked deletion data

Delete the interior and edges of one physical path `P_e`, retaining its branch
endpoints `a_e,b_e`.  Denote the resulting connected rank-six graph by `H_e`;
degree-two suppression is optional.  Rooted trees formerly attached to the
deleted path are set aside and are reattached after the path is restored.

A **marked DNN owner** for `H_e` consists of a correlation Gram `R^e`, its exact
excess `E_e`, and the marked endpoint correlation

```text
r_e=R^e[a_e,b_e],    E_e<=5.
```

Put

```text
f_q(r)=q tan^2(acos((-1)^q r)/(2q)),
c_e=5-E_e,
d_e=f_(q_e)(r_e)-1.
```

Here `c_e` is rank-six spectral credit and `d_e` is the amount by which the
restored path exceeds its one available rank increment.

## 2. Exact good-edge theorem

**Theorem 1 (marked edge opening).**  If some physical path `P_e` has a marked
DNN owner satisfying

```text
d_e<=c_e,                                      (1)
```

then `G` satisfies `s^+(G)>=|V(G)|`, including arbitrary rooted-tree
attachments at branch and path vertices.

**Proof.**  Condition (1) is exactly

```text
E_e+f_(q_e)(r_e)<=6.                           (2)
```

Keep the branch vectors of `R^e` and insert the optimal equal-angle chain on
`P_e` in a fresh auxiliary space.  Exact path elimination says that its excess
is `f_(q_e)(r_e)`, so (2) gives a DNN certificate of total excess at most six.
If the restored core has `L` edges, rank seven gives `|V|=L-6`; hence the
DNN/trace inequality gives `s^+>=L-6`.  Each rooted-tree edge adds one to
`kappa`, the edge count, and the vertex count, so all set-aside and pre-existing
rooted trees may be attached.  `QED`

At exact rank-six budget `E_e=5`, the endpoint tests are

```text
q_e=1: r_e<=0,
q_e=2: r_e>=-7/9,
q_e>=3: no endpoint restriction.               (3)
```

For the last assertion, `f_q(r)<=1` for every `r in [-1,1]` exactly when

```text
2q atan(1/sqrt(q))>=pi.
```

Equality holds at `q=3`, since `atan(1/sqrt(3))=pi/6`, and the left side is
increasing for real `q>=3`: with `x=1/sqrt(q)`, its derivative has the sign of
`2 atan(x)-x/(1+x^2)>0` (indeed `atan(x)>x/(1+x^2)`).  Thus every
length-at-least-three path carries the full
one unit required to pass from rank six to rank seven.  Positive rank-six
credit only weakens the first two thresholds according to (1).

## 3. Averaging over edges or cycles

The useful averaging statement is elementary but exact; importantly, it
averages marked credit balances, not unmarked theorem conclusions.

**Lemma 2 (weighted good-edge principle).**  Let `D` be any nonempty set of
physical paths having marked DNN owners, and let `lambda_e>0`.  If

```text
sum_(e in D) lambda_e (d_e-c_e)<=0,             (4)
```

then at least one `e in D` satisfies (1).

**Proof.**  If every `d_e-c_e` were positive, the left side of (4) would be
positive.  `QED`

One may take `D` to be all physical edges, one support cycle, one orbit of
edges, or the ears in an ear decomposition.  In particular, for an exact-budget
owner on each edge of a cycle `C`, it suffices to prove

```text
sum_(e in C) f_(q_e)(r_e)<=|C|.                 (5)
```

Equations (4)--(5) identify the precise correlation statement an averaging
argument must establish.  Correlations belonging to different deletion owners
cannot be placed in one PSD matrix without an additional gluing argument, so
PSD cycle inequalities for one Gram do not by themselves prove (5).

## 4. Exact finite exceptional support-family class

Fix the fail-closed owner assignment in the complete rank-six theorem.  Let
`N_6` be its typed non-DNN owner class: these are exactly the rank-six states
whose theorem proof is structural rather than an excess-at-most-five Gram.
This notation includes any multiblock structural owner produced by deletion;
it is not silently restricted to the single-block `K5` and `K223` states.

For a canonical simple realization of a parallel class of multiplicity `m`
with `o` odd paths, the lengths are

```text
o=0: (2,...,2),
o>0: (1,3,...,3,2,...,2).
```

Define `X_short` to be the canonical simple realizations satisfying

```text
o_uv in {0,1} for every support pair uv.         (6)
```

Equivalently, every physical path in the displayed realization has length one
or two.  (Proper same-parity descendants are not in `X_short`.)  Define
`X_ear(N_6)` to consist of realizations having a path of length at least three
whose deletion state belongs to `N_6`.

**Theorem 3 (finite short-support reduction).**  Every rank-seven realization
on kernel orders `8,...,12` outside

```text
X_short union X_ear(N_6)                        (7)
```

satisfies `s^+(G)>=|V(G)|`.  The same statement holds on every kernel order.

**Proof.**  A realization outside `X_short` has a physical path `P_e` of length
at least three.  Indeed, either its canonical row has at least two odd members
in one parallel class, producing a length-three path, or it is a proper
same-parity descendant of a canonical row, in which case some path has been
increased by at least two.  Since the realization is
also outside `X_ear(N_6)`, at least one such long path has a DNN-owned deletion
state.  Its owner has `E_e<=5`; (3) gives `f_(q_e)(r_e)<=1`, independently of
the endpoint correlation.  Theorem 1 applies.  `QED`

The class in (7) is finite at the support-family level (its allowed path lengths
and rooted trees remain arbitrary).  For a fixed kernel, (6) has
at most `2^s` rows, where `s` is the number of support pairs, rather than one
choice for every physical path.  The second class is generated without a
rank-seven Gram search: take the finite typed rank-six non-DNN owner supports
and add one open ear in the endpoint-location cases of the proved removable-ear
recursion.  Canonicalization gives a finite, exact list.

## 5. What remains on the short class

For `X_short`, all candidate paths have length one or two.  No certificate
payload beyond the following marked data is relevant:

```text
(edge key, E_e, r_e),
unit edge failure: E_e+f_1(r_e)>6,
length-two failure: E_e+f_2(r_e)>6.             (8)
```

Thus a support row is closed as soon as one deletion owner has `r_e<=0` on a
unit edge or `r_e>=-7/9` on a length-two edge at exact budget; slack uses (1).
Alternatively, an edge- or cycle-average proving (4) closes the row without
choosing the good edge in advance.

The unmarked rank-six theorem alone cannot supply this conclusion.  It records
neither `r_e` nor `c_e`, and structural owners in `N_6` supply no Gram to which
the restored path can be appended.  Therefore any claimed averaging proof that
uses only `s^+(H_e)>=|V(H_e)|`, or that averages correlations from different
owners as if they belonged to a common Gram, has a genuine logical gap.

The remaining theorem-seeking target is consequently sharp: prove (4) on every
short signed support, preferably cyclewise, or classify the supports on which
it fails and handle only those supports structurally.  Millions of independent
rank-seven certificates are not part of this reduced obligation.
