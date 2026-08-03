# Cycle 280: multiscale SAT merge hostile audit

## Target and verdict

Consider the frozen lemma in
`cycle-280-multiscale-sat-merge-admission.md`. It extracts SAT-active first
merges from restrictions of one unrestricted circuit for canonical padded
`3SAT`, then demands `cN` physical gates at each of `eta log N` pairwise
disjoint scales. That disjointness does not follow from the definition of
firstness. A gate is first only relative to a restriction and a chosen pair
`(A,B)`. Changing either can reuse the same gate.

There is a direct dichotomy.

1. If first merge is defined syntactically in the original DAG, each gate has
   one fixed location and one fixed original support scale. Disjoint scale
   buckets can then be imposed by definition, but restrictions provide no new
   additive demand at those buckets.
2. If constants are propagated and firstness is recomputed after each
   restriction, one physical gate can be first at arbitrarily many surviving
   support scales. Disjointness is false without a separate ownership theorem.
3. Under the actual semantic definition, scale is the cardinality of the
   externally selected active sets `A,B`, not a physical invariant of `g`.
   The same gate can therefore carry many scale labels. If scale is changed to
   the number of source components at the first binary join, every first merge
   has intrinsic scale two and the multiscale assertion becomes empty.

The obstruction is finite and occurs inside a literal restriction of the
frozen padded `3SAT`; it does not rely on a circuit lower bound. It refutes any
proof step deriving cross-scale disjointness from `FM_N` alone. It is not by
itself a counterexample to the full existential lemma, which could attempt to
choose sufficiently many other gates.

## A four-scale reusable gate

Let

\[
 L=\bigwedge_{i=1}^8 b_i,\qquad
 R=\bigwedge_{i=9}^{16}b_i,\qquad
 r=L\wedge R,                                                     \tag{280.1}
\]

where `L` and `R` are computed by fixed balanced fan-in-two trees. For
`k=1,2,3,4`, define `rho_k` by leaving exactly `2^(k-1)` designated variables
live in each half and setting every other `b_i` to one. Then the same physical
root gate `r` has, after restriction, two nonconstant children, each depending
on exactly `2^(k-1)` live variables. No gate below `r` meets both halves.
Consequently `r` is the first left--right merge under every `rho_k`, at live
block cardinalities `(1,1),(2,2),(4,4),(8,8)`, hence frozen dyadic scales
`0,1,2,3`; the corresponding total live supports are

\[
 2,4,8,16.                                                       \tag{280.2}
\]

Thus four scale demands can all select the singleton `{r}`. Any assertion that
first-merge witnesses produced independently at different scales are
automatically disjoint is false for this DAG. The family with `2^h` leaves
gives `h` scales for every finite `h`.

There is also an explicit many-gate version. For arbitrary finite `q,h>=1`,
take `q` disjoint balanced AND trees `T_j`, each on `2^(h+1)` leaves, and AND
their roots to form the output. For each scale `k=0,...,h` and each `j`, fix all
leaves outside `T_j` to one, leave `2^k` leaves live on each side of its root,
and fix its remaining leaves to one. With `A` and `B` the two live sides, the
root `r_j` is SAT-active and is their first merge. Hence the independently
valid witness sets may be

\[
 G_0=G_1=\cdots=G_h=\{r_1,\ldots,r_q\}.                         \tag{280.2a}
\]

They contain `q` distinct gates within every scale but only `q`, not
`q(h+1)`, physical gates in their union. Taking `(q,h)=(2,3)` gives a concrete
eight-tree-root demand represented by only two reusable gates. This defeats
both singleton-dismissal and within-scale-distinctness repairs.

Internal gates do not repair the claim. They merge variables within one half,
whereas the asserted firstness of `r` concerns the two designated components.
If those internal gates are instead declared earlier merges of the same kind,
then the definition has abandoned component-scale firstness and collapses to
the scale-two case in item 3 above.

## Realization as a padded `3SAT` restriction

Referee correction: the earlier notation `ell_i(1)=z_i` silently chose a sign
convention that the frozen parser did not state, and it did not exhibit fixed
values of `v,m` compatible with the input length. The construction is valid,
but only after making those details explicit as follows.

This tree is not an unrelated toy function. Here is a convention-independent
coordinate realization in the exact parser frozen by the admission note. For
every `N>=626`, fix `v=16` and `m=32`. Then `ell=5`, the two unary headers use
`17+33` bits, the `96` literals use `96(1+5)=576` bits, and all `N-626`
padding coordinates are fixed to zero.

Use the sixteen private SAT variables `z_i`. Let `P_i` be the literal on `z_i`
encoded when its sign coordinate is `1`, and let `Q_i` be the literal encoded
when it is `0`; thus `\{P_i,Q_i\}=\{z_i,\neg z_i\}`, independently of which sign
convention the parser uses. Let `a_i` be the unique value of `z_i` that makes
`P_i` true, let `A_i` be the literal forcing `z_i=a_i`, and write `\bar A_i`
for its opposite. For each `i`, use the two clauses

\[
 (A_i\vee A_i\vee A_i),\qquad
 (\bar A_i\vee\bar A_i\vee \ell_i(b_i)),                       \tag{280.3}
\]

where all six index fields are fixed to `i`, the first five sign fields are
fixed as displayed, and the final sign field is the actual free encoding
coordinate `b_i`, so `ell_i(1)=P_i` and `ell_i(0)=Q_i`. The first clause forces
`z_i=a_i`. Under that value, both copies of `bar A_i` and `Q_i` are false while
`P_i` is true. The package is therefore satisfiable exactly when the coordinate
bit itself satisfies `b_i=1`; `b_i` is not a renamed complemented coordinate
and no equality promise ties it to another field.

There are exactly `32` displayed clauses, so no filler is needed for `m=32`.
If the same construction is placed in an encoding with a larger fixed `m`,
every extra clause can be fixed, for example, to
`(z_1\vee\neg z_1\vee z_1)`. This is a tautology because repeated literals are
expressly allowed; it introduces no free coordinate and no constraint. Hence
on this explicit sixteen-bit encoding subcube,

\[
 \operatorname{PAD3SAT}\upharpoonright R
   =\bigwedge_{i=1}^{16}b_i.                                    \tag{280.4}
\]

Now let `F` be the padded `3SAT` truth-table function and let `I_R` be the
equality indicator for every coordinate outside
`{b_1,...,b_16}` against its fixed value defining the subcube `R`. Thus `I_R`
does not inspect any `b_i`. Since the domain is finite, choose any unrestricted
circuit `C_F` for `F`, for example its full DNF, and form

\[
 C=(I_R\wedge H)\vee(\neg I_R\wedge C_F),                       \tag{280.5}
\]

where `H` is the fixed tree (280.1), wired directly to the sixteen sign
coordinates. On `R`, `I_R=1` and equation (280.4) gives `C=H=F`; off `R`,
`I_R=0` and `C=C_F=F`. This includes malformed strings and strings whose
altered unary header changes where the parser would place later fields, so `C`
computes the total canonical padded-`3SAT` function on every `N`-bit input.

Under `R` and then `rho_k`, ordinary constant propagation reduces the wrapper
to `H`, collapses the fixed-one portions of its two subtrees, and retains the
same physical root gate `r`, whose two inputs remain nonconstant. If the frozen
definition instead keeps the original restricted DAG without syntactic
propagation, the conclusion is unchanged: `r` is in the output cone, its strict
predecessors lie wholly in one half, and the restricted output equals `H` and
is separately active in both live blocks. Thus `r` satisfies the semantic
first-merge predicate in either reading at all four scales.

Equation (280.5) is intentionally an unrestricted, nonminimal circuit because
the proposed lemma quantifies over every unrestricted circuit. If a proof
silently assumes minimum, reduced, read-once, or restriction-stable circuits,
that is a material model restriction and must be stated and proved preserved.

## Disjoint restrictions do not help

Nestedness of the `rho_k` is not the source of reuse. Use two additional free
sign bits as selectors, assign one selector value to each of four disjoint
cylinders, and fix the unwanted leaves within each cylinder. A multiplexer can
feed the selected leaves into the same `H`; its physical root remains `r` in
every cylinder. A wrapper analogous to (280.5) embeds these cylinders in the
total padded-SAT function. Semantic disjointness of restricted input sets does
not imply physical disjointness of circuit gates.

Nor can disjointness be recovered by choosing one witness gate from each
first-merge set: in the displayed circuit each relevant set is the same
singleton. Fractional charging also fails at the local interface, since four
unit demands are being assigned to one physical gate. This is the same sharing
defect exhibited quantitatively by the address-component breakers in Cycles
264 and 269, now applied to restriction scales rather than addresses.

## What a repair would have to add

A nontrivial merge lemma needs an ingredient not contained in the definition
of first merge:

- a restriction-independent owner assigned to each physical gate, together
  with a proof that every scale has enough differently owned gates;
- a syntactic circuit model forbidding cross-scale sharing;
- an anti-sharing transformation that converts any unrestricted SAT circuit
  to that model with a proved small overhead; or
- a nonadditive potential that explicitly quotients the common core instead of
  counting it once per restriction.

Choosing a canonical formula encoding, canonical restrictions, or a canonical
first gate does none of these. Canonical choice can make the repeated witness
deterministic; it cannot make repeated physical gates disjoint.

`P280-MULTISCALE-MERGE STRUCTURAL BREAKER: the frozen FM predicate permits the
same physical gate to be a SAT-active first A/B merge at every selected scale.
Therefore FM supplies no cross-scale ownership, and no derivation may sum
independently produced scale witnesses without an additional anti-sharing
theorem. Freezing a physical scale instead makes disjoint buckets definitional
and supplies no per-scale abundance.`

This retires the stated proof interface only. It proves no unrestricted circuit
lower bound and no `P != NP` result.
