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
