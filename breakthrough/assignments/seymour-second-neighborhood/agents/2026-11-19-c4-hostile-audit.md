# Hostile audit of the `C4` four-hole proof

Scope: conditional isolated-root `n=18,m=9,k=4` normal form only.

An independent hostile referee reconstructed the normal form, checked the
predecessor-source lower bound, exhaustively enumerated the abstract packet
projection, and found the proof mathematically valid.  In particular:

- the common-C-dominator count is five or six and the B-row/hole ledger forces
  at least four distinct A' predecessor sources;
- every such source has exactly two T-inaccessible vertices;
- the four adjacent inaccessible labels are pairwise incompatible through the
  two diagonal orientations, while each of the two opposite labels determines
  a unique closed source set;
- a fixed closed source set supports at most one source, so at most three
  sources coexist, contradicting the lower bound four.

The audit identified only presentation defects.  The durable proof has been
revised to state the normal-form hole ledger, separate the source endpoint in
the inaccessibility orientation argument, give the transparent B-row identity,
and expand the opposite-packet row saturation.  The audit did not rely on the
historical aggregate SAT claim or unavailable pilot LRATs.

This is not an order-18 or SNC claim.
