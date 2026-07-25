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
