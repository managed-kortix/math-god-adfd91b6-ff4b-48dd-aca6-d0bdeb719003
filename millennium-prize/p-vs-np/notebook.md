# Notebook

Bounded scout is queued to derive a memorization upper bound for fitting an
arbitrary proposed antichecker and compare its gate exponent with the target.
This is an adversarial test, not evidence from solver failure.

## Bounded scout tick 2

Any arbitrary labels on `h` distinct `N`-bit examples can be memorized by a
binary decision tree with at most `h-1` internal nodes. Multiplexer conversion
uses at most `3(h-1)+min(N,h-1)` De Morgan gates with shared input negations.
Hence an antichecker against size `N^2` circuits must have cardinality greater
than `(N^2-N)/3+1` under this convention. Subquadratic anticheckers are
decisively impossible; the route must target a superquadratic sample and still
needs a separate all-exponents amplification theorem.

## Bounded scout cycle 36

The `122` six-vertex coloring masks have an exact irredundant core of size
`90`.  Distinct masks are unlabeled partitions into at most three nonempty
color classes, and

`S(6,1)+S(6,2)+S(6,3)=1+31+90=122`.

Every proper three-block partition gives a complete tripartite graph whose
only proper three-color partition is that partition, up to color names.  Hence
any cover of all colorable graphs by coloring masks must contain all `S(6,3)=90`
proper three-block masks.  Conversely those masks cover every six-vertex
3-colorable graph, since a coloring using fewer than three colors can split a
color class.  Thus witness-mask deletion stops exactly at `90`; this is a
finite monotone-DNF obstruction and gives no unrestricted circuit lower bound.

## Bounded scout cycle 39

The mask-cover computation has an exact all-`n` form.  For every `n>=3`, any
cover of all labeled `n`-vertex 3-colorable graphs by coloring-partition masks
must contain every partition into exactly three nonempty blocks: the complete
tripartite graph associated with such a partition has no other proper
three-block coloring.  Conversely, every coloring with fewer than three
nonempty classes can be refined by splitting a class, so the three-block masks
cover the whole family.  The exact minimum is therefore

`S(n,3)=(3^n-3*2^n+3)/6`.

This generalizes `S(6,3)=90` and shows that the finite witness-mask DNF itself
has exponential irredundancy, without implying an unrestricted circuit lower
bound.

## Bounded scout cycle 41

The memorization obstruction extends quantitatively to every target size.  A
binary decision tree separating `h` distinct `N`-bit examples has at most
`h-1` internal nodes.  Implementing each node as
`(x and A) or ((not x) and B)` takes three binary De Morgan gates, with at most
`min(N,h-1)` shared input negations.  Hence every labeling is fit by a circuit
of size at most

`3(h-1)+min(N,h-1)`.

An antichecker against size `s` must satisfy
`3(h-1)+min(N,h-1)>s`; when `h>=N+1`, necessarily
`h>(s-N)/3+1`.  In particular, direct anticheckers for size `N^k` require
order-`N^k` samples.  This exact obstruction still gives no mechanism for
amplifying a fixed exponent into a superpolynomial lower bound.

## Bounded scout cycle 42

Integer inversion of the memorization bound is piecewise exact. In the regime
`h<=N+1`, an antichecker must satisfy `4(h-1)>s`, hence
`h>=floor(s/4)+2`. In the regime `h>=N+1`, it must satisfy
`3(h-1)+N>s`, hence `h>=floor((s-N)/3)+2`. For the quadratic target and
`N>=4`, this forces

`h>=floor((N^2-N)/3)+2`.

The threshold remains quadratic, so this exact rounding does not supply
all-exponents amplification.

## Bounded scout cycle 43

Finite-union amplification is blocked by the same exact memorization theorem.
If finitely many same-length anticheckers have a union of `H` distinct examples,
their labels are consistent and one circuit of size at most

`3(H-1)+min(N,H-1)`

memorizes the whole union. Therefore a finite union of polynomial-size
anticheckers reaches only the largest polynomial scale represented in that
union. Defeating every polynomial size by same-length memorization alone would
require a superpolynomial number of distinct examples. This rules out that
finite-union mechanism, not amplification using self-reduction, cross-length
consistency, or other structure.
