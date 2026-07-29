# Cycle 87: small-Vertex-Cover time--space magnification

Let an `n`-vertex graph be given by its adjacency matrix of bit length
`m=Theta(n^2)`, and fix

\[
k(n)=\left\lfloor2^{\sqrt{\log_2 n}}\right\rfloor=n^{o(1)}.
\]

Oliveira--Santhanam, Theorem 35, proves that for any fixed `epsilon>0`,

\[
k\text{-Vertex-Cover}\notin
\operatorname{DTISP}(m^{1+\epsilon},m^{o(1)})
\quad\Longrightarrow\quad P\ne NP.
\]

Thus excluding simultaneous `m^1.01` time and subpolynomial workspace in the
paper's deterministic random-access model has full official reach.

The contrapositive uses Buss kernelization. A size-`k` instance reduces in
`m^(1+o(1))` time and `m^o(1)` space to at most `2k^2` nonisolated vertices and
`O(k^4)=m^o(1)` adjacency bits. Under `P=NP`, a fixed polynomial-time ordinary
Vertex-Cover solver runs on that kernel in `m^o(1)` additional time and space.

This also supplies the decisive mechanism audit. A generic cell-probe or
communication lower bound cannot cross the magnification threshold: the matrix
can be scanned in `O(m)` probes, after which uncharged computation on the
subpolynomial kernel solves the instance. Any viable proof must charge the
computation on the kernel and be non-localizable.

The correct hard regime is not a dense logarithmic-clique distribution. Since

\[
\tau(G)\le k\iff\alpha(G)\ge n-k,
\]

yes instances have an almost-spanning independent set. All uncertainty lies in
an `O(k^2)` Buss-saturated core hidden among removable isolates. A star-saturated
gadget can preserve such a hard core while keeping every degree at most `k` and
the edge count below `k^2`, but ordinary NP-hardness of the core gives no RAM
time--space lower bound.

The promoted target is therefore the exact computation-sensitive RAM tradeoff,
not a probe surrogate. Promotion of a proof mechanism requires an extraction
lemma converting every fast small-space solver for the original nonpromise
language into a restricted object with a known lower bound, without granting
an arbitrary oracle for the kernel. No such extraction lemma is currently
proved. No circuit lower bound or `P!=NP` result is claimed.
