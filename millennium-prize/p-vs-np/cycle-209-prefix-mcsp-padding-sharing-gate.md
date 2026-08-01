# Cycle 209: prefix-constrained MCSP and the padding/tagging sharing gate

Fix the fan-in-two basis `B={AND,XOR,NOT}` with constants. For a set of
truth-table positions `A subseteq {0,1}^n` and an assignment
`rho in {0,1}^A`, define

\[
  \operatorname{PrefixMCSP}_{n,s}(A,rho)=1
  \quad\Longleftrightarrow\quad
  \min_{f:f|_A=rho} C_B(f)\le s.                         \tag{209.1}
\]

This is the exact completion problem hidden by canonical prefix merging. The
question is whether truth-table padding or tagging can turn (209.1) into one
ordinary MCSP instance while preserving the circuit budget up to an explicit
small overhead.

## What an exact reduction would have to preserve

A many-one map would have to compute, from `(A,rho,s)` alone, a complete truth
table `G_(A,rho)` and a threshold `s'` such that

\[
  \exists f\supseteq rho\ [C_B(f)\le s]
  \quad\Longleftrightarrow\quad
  C_B(G_(A,rho))\le s'.                                  \tag{209.2}
\]

Merely padding a chosen completion is not a reduction: choosing that completion
is the search problem in (209.1). Repeating a table on new address variables is
also not resource preserving in an additive sense, since
`F(a,x)=f(x)` ignores `a` and has essentially the same circuit as `f`.

The literal witness-independent alternative is to place possible completions
in tagged slices,

\[
  D(f_1,\ldots,f_t)(a,x)=f_a(x).                           \tag{209.3}
\]

But restriction of `a` proves only

\[
  C_B(D)\ge \max_i C_B(f_i),                              \tag{209.4}
\]

whereas (209.1) is governed by `min_i C_B(f_i)`. Thus the unmodified tagged
table has the wrong Boolean polarity: small tagged complexity requires a joint
small representation of every slice, not one small completion. Complementing
or permuting tags does not change this quantifier mismatch.

## Balanced-prefix circuit-sharing counterexample

The stronger obstruction is present even when all tagged slices are distinct
completions of one balanced prefix. Let the payload variables include
`x_1,...,x_(t+1)`, let

\[
  A=\{x:x_1=0\},\qquad g_i(x)=x_1\mathbin{AND}x_{i+1},
  \qquad f_i(x)=H(x)\mathbin{XOR}g_i(x),                  \tag{209.5}
\]

where `H` is arbitrary. The set `A` contains exactly half of the truth-table
positions, every `f_i` restricts to the same prefix `rho=H|_A`, and the `f_i`
are pairwise distinct. If `c=C_B(H)`, then

\[
  c-2\le C_B(f_i)\le c+2.                                \tag{209.6}
\]

The lower bound follows by recovering `H=f_i XOR g_i` with two more gates.
Nevertheless, with a `q=log_2 t` bit tag (for power-of-two `t`),

\[
  D(a,x)=H(x)\mathbin{XOR}
         \bigl(x_1\mathbin{AND}x_{\operatorname{sel}(a)+1}\bigr), \tag{209.7}
\]

Using `MUX(b,u,v)=v XOR (b AND (u XOR v))`, the selected variable
`x_(sel(a)+1)` costs at most `3(t-1)` gates. Hence

\[
  C_B(D)\le c+3(t-1)+2,                                  \tag{209.8}
\]

while the nominal separate-slice cost is at least `t(c-2)`. Therefore every
additive accounting inequality

\[
  C_B(D)\ge \sum_i C_B(f_i)-\Delta                       \tag{209.9}
\]

must permit

\[
  \Delta\ge (t-1)c-5t+1.                                 \tag{209.10}
\]

Counting supplies finite functions `H` with `c` arbitrarily larger than `t`,
so the loss is essentially the entire repeated hard core. Unique slice tags do
not isolate circuit resources: an unrestricted circuit computes `H` once and
shares it across all completions.

The same example defeats padding by replicated or lightly transformed copies.
If each block is `H XOR g_i XOR tau_i` for an easy public tag `tau_i`, the
circuit computes `H` once and adds the joint selector/tag logic. The cost is
`c+C_B((a,x) mapsto g_a(x) XOR tau_a(x))+1`, not `t c` plus overhead.

## Scope of the no-go

Equations (209.4) and (209.10) refute the ordinary slice-concatenation,
repetition, and easy-tag accounting needed by the proposed truth-table
padding/tagging reduction. They do not prove that no polynomial-time many-one
reduction from PrefixMCSP to MCSP exists by some unrelated construction; such a
claim would require complexity-theoretic assumptions or a new invariant.

An exact resource-preserving reduction would therefore need a gadget whose
minimum circuit complexity implements an existential choice while preventing
arbitrary cross-slice sharing. Proving that anti-sharing property for
unrestricted circuits is precisely a new direct-sum/canonicalization theorem,
not a consequence of truth-table padding. No MCSP lower bound, unrestricted
circuit lower bound, or `P != NP` conclusion follows.
