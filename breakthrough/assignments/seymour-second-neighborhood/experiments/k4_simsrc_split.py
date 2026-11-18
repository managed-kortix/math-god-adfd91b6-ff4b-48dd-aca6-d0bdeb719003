#!/usr/bin/env python3
"""Exact symmetry cover for the conditional rooted m=8, k=4 projection.

The graph labels and color classes are fixed by ``k4_simsrc_cnf.py``.  For
p=6, the stabilizer of source 2 is

    S(P-minus-{2}) x S(K),

with 0, 1, the sole outsider 8, and b0=15 fixed.  It has 17 orbits on the
105 selector pairs of source 2.

For p=7, the stabilizer of source 2 is

    S(P-minus-{2}) x S(K),

with 0, 1, and b0 fixed.  It has 12 first-level orbits.  Eleven are discharged
directly.  The remaining orbit, represented by source-2 pair {1,3}, is covered
by fixing that pair and splitting on source 3.  Its stabilizer is

    S(P-minus-{2,3}) x S(K),

with 0, 1, 2, 3, and b0 fixed, and has 17 orbits on source-3 pairs.

The module contains no SAT encoding.  It materializes every finite permutation,
computes every orbit, and rejects overlap or incomplete coverage.  The retained
representative indices name proof artifacts and ledger rows.
"""

from __future__ import annotations

import itertools
from functools import lru_cache

V = tuple(range(16))
ROOT = 0
R = 1
AP = tuple(range(2, 9))
K = tuple(range(9, 15))
B0 = 15
P6 = frozenset(AP[:6])
P7 = frozenset(AP)

P6_REPRESENTATIVE_INDICES = (0, 1, 6, 7, 13, 14, 19, 20, 26, 27, 31, 32, 38, 77, 83, 84, 89)
P7_DIRECT_REPRESENTATIVE_INDICES = (0, 1, 7, 13, 20, 26, 27, 32, 38, 84, 89)
P7_REFINED_PARENT_INDEX = 14
P7_SUBREPRESENTATIVE_INDICES = (0, 1, 2, 7, 13, 14, 15, 20, 26, 27, 32, 38, 39, 43, 49, 84, 89)


def allowed_pairs(source: int) -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations((vertex for vertex in V if vertex != source), 2))


def apply_pair(pair: tuple[int, int], permutation: tuple[int, ...]) -> tuple[int, int]:
    return tuple(sorted((permutation[pair[0]], permutation[pair[1]])))


def direct_product_group(*moved_blocks: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    """Return every permutation acting independently on the listed blocks."""

    if any(set(left) & set(right) for i, left in enumerate(moved_blocks) for right in moved_blocks[i + 1:]):
        raise RuntimeError("group blocks overlap")
    group = []
    for images in itertools.product(*(itertools.permutations(block) for block in moved_blocks)):
        permutation = list(V)
        for block, image in zip(moved_blocks, images):
            for vertex, target in zip(block, image):
                permutation[vertex] = target
        if sorted(permutation) != list(V):
            raise RuntimeError("constructed action is not a permutation")
        group.append(tuple(permutation))
    return tuple(group)


def orbit_partition(source: int, group: tuple[tuple[int, ...], ...]):
    pairs = allowed_pairs(source)
    universe = set(pairs)
    unassigned = set(pairs)
    cells = []
    while unassigned:
        representative = min(unassigned)
        orbit = {apply_pair(representative, permutation) for permutation in group}
        if not orbit <= universe:
            raise RuntimeError("group action moved a pair outside the source-pair universe")
        cells.append((pairs.index(representative), representative, tuple(sorted(orbit))))
        unassigned -= orbit
    covered = [pair for _, _, orbit in cells for pair in orbit]
    if len(covered) != len(set(covered)) or set(covered) != universe:
        raise RuntimeError("orbits are not a disjoint exhaustive partition")
    return tuple(cells)


def require_partition(cells, representatives, sizes, label):
    if tuple(cell[0] for cell in cells) != tuple(representatives):
        raise RuntimeError(f"{label} representative indices changed")
    if tuple(len(cell[2]) for cell in cells) != tuple(sizes):
        raise RuntimeError(f"{label} orbit sizes changed")
    if sum(len(cell[2]) for cell in cells) != len(allowed_pairs(2 if label != "p7 sub" else 3)):
        raise RuntimeError(f"{label} does not cover all selector pairs")


@lru_cache(maxsize=1)
def p6_orbits():
    group = direct_product_group(tuple(sorted(P6 - {2})), K)
    cells = orbit_partition(2, group)
    require_partition(
        cells,
        P6_REPRESENTATIVE_INDICES,
        (1, 5, 1, 6, 1, 5, 1, 6, 1, 10, 5, 30, 5, 6, 1, 15, 6),
        "p6",
    )
    return cells


@lru_cache(maxsize=1)
def p7_first_orbits():
    group = direct_product_group(tuple(sorted(P7 - {2})), K)
    cells = orbit_partition(2, group)
    expected = tuple(sorted(P7_DIRECT_REPRESENTATIVE_INDICES + (P7_REFINED_PARENT_INDEX,)))
    require_partition(cells, expected, (1, 6, 6, 1, 6, 6, 1, 15, 36, 6, 15, 6), "p7 first")
    return cells


@lru_cache(maxsize=1)
def p7_suborbits():
    parent_pair = allowed_pairs(2)[P7_REFINED_PARENT_INDEX]
    if parent_pair != (1, 3):
        raise RuntimeError("refined parent pair changed")
    group = direct_product_group(tuple(sorted(P7 - {2, 3})), K)
    # Every group element fixes source 2, source 3, and the parent pair {1,3}.
    if any(apply_pair(parent_pair, permutation) != parent_pair for permutation in group):
        raise RuntimeError("subgroup does not stabilize the refined parent")
    cells = orbit_partition(3, group)
    require_partition(
        cells,
        P7_SUBREPRESENTATIVE_INDICES,
        (1, 1, 5, 6, 1, 1, 5, 6, 1, 5, 6, 1, 10, 30, 5, 15, 6),
        "p7 sub",
    )
    return cells


def audit() -> None:
    p6 = p6_orbits()
    p7 = p7_first_orbits()
    sub = p7_suborbits()
    first_indices = {cell[0] for cell in p7}
    retained = set(P7_DIRECT_REPRESENTATIVE_INDICES) | {P7_REFINED_PARENT_INDEX}
    if first_indices != retained:
        raise RuntimeError("p7 first-level retained representatives are not exact")
    if sum(len(cell[2]) for cell in p6) != 105 or sum(len(cell[2]) for cell in p7) != 105:
        raise RuntimeError("first-level split is not exhaustive")
    if sum(len(cell[2]) for cell in sub) != 105:
        raise RuntimeError("second-level split is not exhaustive")


if __name__ == "__main__":
    audit()
    print(
        "PASS p6_orbits=17 p6_pairs=105 "
        "p7_first_orbits=12 p7_pairs=105 p7_direct=11 "
        "p7_refined_parent=14 p7_suborbits=17 p7_subpairs=105"
    )
