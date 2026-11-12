#!/usr/bin/env python3
"""Exact standalone blocker for adaptive favorable-cycle all-length promotion.

Source key in the pinned order-nine obstruction stream:
  [78714, 7662, 176, [1,1,1,1,0,1,0,1,1,0,1,1,1], 1]

No third-party packages, floating point, or repository files are used.
"""
from collections import defaultdict, deque

NBRANCH = 9
SOURCE_RECORD = (
    78714, 7662, 176,
    (1,1,1,1,0,1,0,1,1,0,1,1,1),
    1,
)
# (u,v,multiplicity), in canonical support order.  Together with the source
# odd-count row, this deterministically expands to the physical ledger below.
KERNEL_SUPPORTS = (
    (0,7,1), (0,8,2), (1,6,1), (1,7,1), (1,8,1),
    (2,4,1), (2,7,1), (2,8,1), (3,4,1), (3,5,1),
    (3,8,1), (4,8,1), (5,6,2),
)
# Physical occurrence endpoints, in canonical occurrence order 0,...,14.
ENDPOINTS = (
    (0,7), (0,8), (0,8), (1,6), (1,7),
    (1,8), (2,4), (2,7), (2,8), (3,4),
    (3,5), (3,8), (4,8), (5,6), (5,6),
)
CANONICAL = (1,1,2,1,1,2,1,2,1,1,2,1,1,1,2)
# Add two to occurrences 1 and 13.
DESCENDANT = (1,3,2,1,1,2,1,2,1,1,2,1,1,3,2)
EXPECTED = (
    (96,5,(13,14)), (98,4,(13,14)), (104,4,(13,14)),
    (106,3,(13,14)), (120,3,(13,14)), (122,2,(13,14)),
    (124,2,(13,14)), (226,3,(13,14)), (227,2,(13,14)),
    (230,2,(13,14)), (234,2,(13,14)), (257,2,(1,2)),
)

def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)

def reconstruct_canonical_ledger():
    odd_row = SOURCE_RECORD[3]
    require(len(KERNEL_SUPPORTS) == len(odd_row), "source row width changed")
    endpoints = []
    lengths = []
    for (u,v,multiplicity), odd_total in zip(KERNEL_SUPPORTS, odd_row):
        require(type(odd_total) is int and 0 <= odd_total <= multiplicity,
                "invalid source odd-count entry")
        support_lengths = (([1] + [3] * (odd_total - 1)) if odd_total else [])
        support_lengths += [2] * (multiplicity - odd_total)
        require(len(support_lengths) == multiplicity,
                "physical occurrence expansion changed")
        endpoints.extend([(u,v)] * multiplicity)
        lengths.extend(support_lengths)
    return tuple(endpoints), tuple(lengths)

def connected_rank(mask):
    vertices = {v for v in range(NBRANCH) if mask >> v & 1}
    require(vertices, "empty side")
    adj = {v:set() for v in vertices}
    m = 0
    for u,v in ENDPOINTS:
        if u in vertices and v in vertices:
            adj[u].add(v); adj[v].add(u); m += 1
    seen = {min(vertices)}; todo = list(seen)
    while todo:
        u = todo.pop()
        for v in adj[u] - seen:
            seen.add(v); todo.append(v)
    return seen == vertices, m - len(vertices) + 1

def expanded_edges(lengths, mask=(1 << NBRANCH)-1):
    """Return (number of vertices, [(a,b,physical_occurrence),...])."""
    require(len(lengths) == len(ENDPOINTS) == 15, "physical ledger width changed")
    require(all(type(length) is int and length >= 1 for length in lengths),
            "invalid physical path length")
    edges = []
    nxt = NBRANCH
    for occurrence, ((u,v), length) in enumerate(zip(ENDPOINTS, lengths)):
        if not (mask >> u & 1 and mask >> v & 1):
            continue
        chain = [u] + list(range(nxt, nxt + length - 1)) + [v]
        nxt += length - 1
        edges.extend((a,b,occurrence) for a,b in zip(chain,chain[1:]))
    return nxt, edges

def unique_cycle(lengths, low_mask):
    """Leaf-prune the expanded beta-one side, preserving parallel edge IDs."""
    nxt, edges = expanded_edges(lengths, low_mask)
    vertices = {v for v in range(NBRANCH) if low_mask >> v & 1}
    incidence = defaultdict(list)
    for eid,(u,v,unused_occurrence) in enumerate(edges):
        vertices.update((u,v))
        incidence[u].append((eid,v)); incidence[v].append((eid,u))
    alive_v = set(vertices); alive_e = set(range(len(edges)))
    degree = {v:len(incidence[v]) for v in vertices}
    leaves = deque(v for v in vertices if degree[v] <= 1)
    while leaves:
        v = leaves.popleft()
        if v not in alive_v:
            continue
        alive_v.remove(v)
        for eid,w in incidence[v]:
            if eid not in alive_e:
                continue
            alive_e.remove(eid)
            if w in alive_v:
                degree[w] -= 1
                if degree[w] <= 1:
                    leaves.append(w)
    require(len(alive_e) == len(alive_v) > 0, "not one surviving cycle")
    occurrences = tuple(sorted({edges[eid][2] for eid in alive_e}))
    return len(alive_e), occurrences

def eligible_partitions(lengths):
    out = []
    # Masks 1,...,255 omit vertex 8 and enumerate each unordered partition once.
    for representative in range(1, 1 << 8):
        other = 511 ^ representative
        lc,lr = connected_rank(representative)
        rc,rr = connected_rank(other)
        if not (lc and rc):
            continue
        if lr == 1 and 2 <= rr <= 5:
            length, occurrences = unique_cycle(lengths, representative)
            out.append((representative,rr,occurrences,length))
        if rr == 1 and 2 <= lr <= 5:
            length, occurrences = unique_cycle(lengths, other)
            out.append((other,lr,occurrences,length))
    return sorted(out)

def full_simple_audit():
    n, edges = expanded_edges(DESCENDANT)
    pairs = [tuple(sorted((u,v))) for u,v,unused in edges]
    require(len(pairs) == len(set(pairs)), "descendant realization is not simple")
    adj = {v:set() for v in range(n)}
    for u,v in pairs:
        adj[u].add(v); adj[v].add(u)
    seen={0}; todo=[0]
    while todo:
        u=todo.pop()
        for v in adj[u]-seen:
            seen.add(v);todo.append(v)
    require(len(seen)==n, "descendant disconnected")
    require((n,len(edges),len(edges)-n+1)==(18,24,7), "wrong full graph counts")
    return n,len(edges)

def main():
    endpoints, canonical_lengths = reconstruct_canonical_ledger()
    require(endpoints == ENDPOINTS, "source endpoint ledger changed")
    require(canonical_lengths == CANONICAL, "source canonical lengths changed")
    require(tuple(b-a for a,b in zip(CANONICAL,DESCENDANT)) ==
            (0,2,0,0,0,0,0,0,0,0,0,0,0,2,0),
            "descendant is not exactly z={1,13}")

    canonical = eligible_partitions(CANONICAL)
    projected = tuple((mask,high,occ) for mask,high,occ,length in canonical)
    require(projected == EXPECTED, "eligible partition table changed")
    require(all(length == 3 for *unused,length in canonical), "canonical cycle not C3")

    descendant = eligible_partitions(DESCENDANT)
    require(tuple((m,h,o) for m,h,o,L in descendant) == EXPECTED,
            "descendant eligible partition table changed")
    require(all(length == 5 for *unused,length in descendant),
            "not every descendant low cycle is C5")
    require(not any(length % 2 == 0 or length % 4 == 3
                    for *unused,length in descendant),
            "a favorable descendant partition survived")
    n,m = full_simple_audit()

    print("source_record=" + repr(SOURCE_RECORD))
    print("source_key=78714/global7662/local176")
    print("canonical_lengths=" + repr(CANONICAL))
    print("descendant_lengths=" + repr(DESCENDANT))
    print("eligible_low_mask/high_rank/cycle_occurrences=" + repr(EXPECTED))
    print("canonical_cycle_lengths=" + repr(tuple(x[3] for x in canonical)))
    print("descendant_cycle_lengths=" + repr(tuple(x[3] for x in descendant)))
    print(f"simple_connected_rank7_descendant: n={n}, m={m}, beta={m-n+1}")
    print("favorable_cycle_adaptive_blocker_verifier: PASS")

if __name__ == '__main__':
    main()
