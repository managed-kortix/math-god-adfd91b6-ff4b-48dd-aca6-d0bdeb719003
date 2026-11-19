# Hostile audits of the remaining four-hole shape proofs

Scope: conditional isolated-root `n=18,m=9,k=4` normal form only.

Two independent hostile Task referees audited ticks 39--44.  Fresh abstract
cut/orientation enumerations confirmed the packet classifications and exact
compatibility maxima for paw (3), triangle plus edge (3), fork (3), P5 (2),
and the two star shapes.  The P5 write-up was tightened with explicit formulas
that reconstruct S in the exceptional P13 packet, and its script is now
correctly described as a truth-table check of the displayed formulas rather
than an independent derivation.

The first audit of tick 43 found a genuine proof-package gap: the original
checker established uniqueness only of `R=S intersect H`, then the prose
incorrectly treated this as uniqueness of the full S.  A further exact census
showed the missing repair is universally available.  In every accepted packet
some inaccessible endpoint t is saturated.  With Q_t its holes into R and W_t
its support outneighbors outside S,

    N+(t) = (S minus Q_t) union W_t,
    S = (N+(t) minus W_t) union Q_t.

The replacement checker verifies this saturation, exact surviving labels,
maximum compatible label families, accepted-state counts, and unique cuts for
all orientations.  It uses explicit exceptions rather than Python assertions
and reports:

    PASS p4_edge orientations=2048 accepted=640 maximum_sources=3
    PASS two_p3 orientations=2048 accepted=640 maximum_sources=2
    PASS p3_two_edges orientations=131072 accepted=8192 maximum_sources=2

The corrected tick-43 proof includes the reconstruction lemma.  This closes
the identified gap; no broader order-18 or SNC claim follows.
