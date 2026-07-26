# Exact finite search for the rooted hostile `C5` guard

## Verdict

No counterexample was found to

`sigma(G)>1-delta_5=3-sqrt(5)`

in the finite classes searched. Every comparison was certified with an integer
characteristic polynomial and multiplicity-aware rational Sturm intervals; no
floating-point spectral decision was used.

The exhaustive bare-core search covers every nonisomorphic triangular cactus
obtained by vertex-coalescing one through six triangles, every root orbit, and
every joining-path length from zero through four. It tests 845 rooted
triangle/`C5` cacti. All 845 have rational lower surplus bounds strictly above
a rational upper bound for `3-sqrt(5)`.

Two attachment searches add:

1. 2,704 tests with bridge lengths zero through three and every rooted tree of
   order at most three attached at the distinguished triangular root, for all
   one- through six-triangle cores; and
2. 1,206 tests through four triangles with a pendant edge attached at every
   vertex of the completed graph, including triangle vertices, joining-path
   vertices, and `C5` vertices.

Again every case is certified strictly above the claimed threshold. These are
finite experiments, not a substitute for the arbitrary-tree theorem, but they
directly attack the configurations most likely to reveal a false rooted or
Voronoi step.

## Exact method

The generator is

`research/rooted_hostile_guard_finite_search.py`.

It imports the audited exact polynomial and Sturm routines from
`research/shared_triangle_rooted_exact.py`. For every graph it computes

`phi_G(x)=det(xI-A(G)) in Z[x]`

by exact Newton identities. It takes squarefree layers of `phi_G`, isolates the
positive roots of each layer by a Sturm sequence over `Fraction`, and restores
the layer multiplicity in

`sum_(lambda>0) lambda^2-|V(G)|`.

Thus a repeated positive eigenvalue contributes once for each algebraic
multiplicity. This explicitly avoids the distinct-root error previously found
in the central-three-petal experiment.

The comparison target is also rationally enclosed. If

`L_5<sqrt(5)<U_5`,

the program compares the surplus interval with

`3-U_5<3-sqrt(5)<3-L_5`.

A case is called certified strict only when its rational surplus lower endpoint
is greater than the rational upper endpoint `3-L_5`. A counterexample would be
reported only when its surplus upper endpoint is at most `3-U_5`. Anything in
between is retained as unresolved rather than guessed. There were no unresolved
cases in the reported runs.

The enumerator constructs all vertex-coalesced triangular cactus cores
recursively and removes isomorphic duplicates. It then keeps one representative
of every root orbit. The resulting unrooted core counts are

| triangles | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| cores | 1 | 1 | 2 | 4 | 8 | 19 |

These agree with the expected tree-like block incidences for this restricted
triangular-cactus model. Rooted trees are generated from all Prüfer codes and
deduplicated as rooted graphs.

## Worst structural types

The global minima in every reported census occur at the smallest triangular
guard, not at a high-rank or Voronoi-splitting core.

* In the bare census, the worst graph is the one-triangle/one-`C5` common-cut
  coalescence. Its exact polynomial is

  `x^7-8x^5-2x^4+16x^3+4x^2-7x`,

  and the certificate gives

  `921023653701551/562949953421312 < sigma`

  `< 1842052502228677/1125899906842624`.

  The lower endpoint is greater than `1.636`, while
  `3-sqrt(5)` is less than `0.764`. Thus this finite minimum has a large
  certified margin.

* With rooted trees through order three, the worst case is still one triangle:
  a bridge of length one and the rooted three-vertex star/path-middle transfer
  at the triangular root. Its certified surplus interval is

  `[199987180505/137438953472,
    400006939635/274877906944]`,

  whose lower endpoint exceeds `1.454`.

* With a pendant edge allowed at every completed-graph vertex through four
  triangles, the worst case is again rank one: common-cut `C3` and `C5`, with
  the edge attached at a private triangle vertex. Its lower endpoint is

  `207411671513/137438953472>1.509`.

At each fixed triangle count from two through six, the smallest sampled surplus
comes from the common-cut bouquet, usually with a one-edge joining path and the
most suppressive rooted tree attached at the common triangular cut. The bare
minimum lower endpoints increase sharply with triangle count: approximately
`3.25, 4.69, 6.06, 7.39, 8.69` for ranks two through six. These decimals are
only orientation; the JSON certificate stores the rational bounds.

The structural conclusion is therefore clear within the searched domain:

1. **Worst:** a single triangular guard, short connector, and a small tree at
   or near the triangular interface.
2. **Next:** common-cut triangle bouquets, especially with bridge length one.
3. **Not worst:** distributed chain/tree incidences.
4. **Far from threshold:** the explicit central-triangle/three-petal Voronoi
   obstruction and its alternate four-triangle block incidence.

## Explicit Voronoi obstruction

The four-triangle census includes the central triangle with one petal at each
central vertex. It also includes the other four-triangle incidence with the
same triangle-vertex membership multiset, so the search does not identify a
core merely by degree data.

For the explicit central-three-petal core, attaching the `C5` at a central
vertex by coalescence gives

`phi=x^13-17x^11-8x^10+99x^9+78x^8-242x^7-256x^6`

`    +219x^5+316x^4-13x^3-104x^2-15x+6`,

with the exact rational enclosure

`1938472089553872953/288230376151711744 < sigma`

`< 1938472828664630453/288230376151711744`.

This lower endpoint exceeds `6.72`. Bridge lengths one through four and every
root orbit were also checked. The alternate four-triangle incidence has a bare
minimum above `6.55`. Small rooted-tree and all-site pendant-edge searches do
not move either type remotely near `3-sqrt(5)`.

This matters because the central-three-petal graph is the exact combinatorial
obstruction to conserving all cyclomatic credits in the Voronoi partition: the
central triangle is split among the three petal territories. The spectral
search shows that this method obstruction is not a finite spectral
counterexample to the guard inequality. Indeed it is one of the safest types
in the census.

## Scope and interpretation

The finite search supports, but cannot prove, the arbitrary-tree statement.
Its exhaustive claim is deliberately limited to triangular cores built only by
vertex coalescence. General cacti may place positive-length bridge paths between
triangular blocks and may carry several simultaneous tree attachments. The
script can sample those operations, but the reported all-core exhaustive run
does not enumerate every combination of them.

The search nevertheless checks the theorem's most delicate advertised points:

* root choice is exhaustive up to automorphism;
* coalescence and positive joining paths are both present;
* the Voronoi split-cycle obstruction is explicit;
* all triangular block-incidence types through six blocks are present in the
  vertex-coalesced model;
* a `C5` is the sharp hostile cycle because `delta_q` decreases with `q`, so
  the largest hostile deficit occurs at `q=5`;
* repeated roots are handled with algebraic multiplicity; and
* every retained extremal graph carries its full characteristic polynomial,
  rational root intervals, and rational surplus interval.

The principal reusable certificate is

`research/rooted-hostile-guard-finite-certificate.json`.

It contains the complete 845-case census counts and the 30 worst full records.
The larger attachment runs can be regenerated rather than stored.

## Reproduction

Run the committed exhaustive bare census with

```text
python research/rooted_hostile_guard_finite_search.py \
  --max-triangles 6 --max-bridge 4 --max-tree-vertices 1 \
  --attachments none --bits 20 --keep 30 \
  --output research/rooted-hostile-guard-finite-certificate.json
```

Run the rooted-tree stress test with

```text
python research/rooted_hostile_guard_finite_search.py \
  --max-triangles 6 --max-bridge 3 --max-tree-vertices 3 \
  --attachments root --bits 16 --keep 40 \
  --output /tmp/rooted-hostile-guard-root-trees.json
```

Run the all-site pendant-edge stress test with

```text
python research/rooted_hostile_guard_finite_search.py \
  --max-triangles 4 --max-bridge 3 --max-tree-vertices 2 \
  --attachments all --bits 14 --keep 40 \
  --output /tmp/rooted-hostile-guard-all-sites.json
```

Only the Python standard library is required.
