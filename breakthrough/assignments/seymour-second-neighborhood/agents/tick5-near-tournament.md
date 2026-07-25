# Tick 5 near-tournament literature route

Known theorem (Fidler--Yuster, JGT 55 (2007), with a later good-digraph
treatment by Ghazal, arXiv:1509.03282): every tournament missing a matching
satisfies SNC. Consequently an oriented graph obtained from a tournament by
deleting at most two arcs satisfies SNC; when the missing pairs share an
endpoint, the missing graph is a star and the convenient-orientation/feed-
vertex argument applies.

A hostile audit found that a tempting shortcut proof was incomplete: missing
edges need not each have a convenient orientation; two disjoint missing edges
can form a dependency 2-cycle; reversing a restored feed-incident edge is safe
only toward the feed vertex; and dependency paths/cycles require separate
accounting. We therefore invoke the cited matching/star result, not that
shortcut. It independently eliminates order-18 shards with zero, one, or two
missing pairs in both root branches.
