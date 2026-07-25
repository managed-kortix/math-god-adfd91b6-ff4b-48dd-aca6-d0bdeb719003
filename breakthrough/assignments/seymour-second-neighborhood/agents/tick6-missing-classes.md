# Tick 6 literature classification by missing graph

Verified blanket coverage:

- missing matching: Fidler--Yuster (2007);
- missing matching plus one star: Dara--Francis--Jacob--Narayanan (2022),
  Theorem 6;
- missing two stars: Daamouch--Ghazal--Al-Mniny (2025), Theorem 3.2;
- generalized stars/threshold missing graphs: Ghazal (2012);
- the paper-specific comb and separately `C4,C5`: Ghazal (2013).

Every graph with at most three edges is a matching plus a star. Every graph
with four edges is likewise covered except possibly `C4`, which has its own
theorem. Therefore all order-18 shards with at most four missing pairs satisfy
SNC, independently of root structure.

No arbitrary-forest theorem was verified. Five missing edges already permit
`P6`, which is not forced into the matching, matching-plus-star, two-star,
threshold, or published-comb classes. Thus the literature blanket stops at
`m=4`; order-18 shards `m=5,...,9` remain genuine targets.
