#!/usr/bin/env python3
"""Independent raw-coloring and orbit-weight audit of the m=6 placement cover."""

import argparse
import hashlib
from collections import Counter, defaultdict
from pathlib import Path

COLORS = "RABC"
CAPACITIES = {"B6": (1, 8, 6, 3), "B7": (1, 8, 7, 2)}
SUPPORT_BYTES = 934
SUPPORT_SHA256 = "e97de806f6db6c3ac1768cab9259f7f0cd1c91ee26d949c1a3455ef8e471c8be"
EXPECTED_ROWS = 187324
EXPECTED_BYTES = 6659672
EXPECTED_SHA256 = "22d7744f1eecee3ea22527e4beec645ae999c912184f1f23c1a7f701e966ed5e"


def unpack_graph6(text):
    vertex_count = ord(text[0]) - 63
    stream = []
    for char in text[1:]:
        number = ord(char) - 63
        for place in (32, 16, 8, 4, 2, 1):
            stream.append(bool(number & place))
    pairs = [(left, right) for right in range(1, vertex_count) for left in range(right)]
    return vertex_count, frozenset(pair for pair, present in zip(pairs, stream) if present)


def load_supports(filename):
    raw = filename.read_bytes()
    if len(raw) != SUPPORT_BYTES or hashlib.sha256(raw).hexdigest() != SUPPORT_SHA256:
        raise RuntimeError("support census is not the frozen payload")
    result = {}
    for line in raw.decode("ascii").splitlines()[4:]:
        index, stated_order, graph6 = line.split("\t")
        order, edges = unpack_graph6(graph6)
        if order != int(stated_order) or len(edges) != 6:
            raise RuntimeError(f"invalid support {index}")
        result[int(index)] = (order, graph6, edges)
    if set(result) != set(range(68)):
        raise RuntimeError("support index set is not 0..67")
    return result


def full_automorphism_group(order, edges):
    neighbors = [set() for _ in range(order)]
    for left, right in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    degree_classes = defaultdict(list)
    for vertex in range(order):
        degree_classes[len(neighbors[vertex])].append(vertex)
    candidates = [degree_classes[len(neighbors[vertex])] for vertex in range(order)]
    sequence = sorted(range(order), key=lambda vertex: (len(candidates[vertex]), -len(neighbors[vertex]), vertex))
    image = [-1] * order
    occupied = set()
    answer = []

    def search(position):
        if position == order:
            answer.append(tuple(image))
            return
        source = sequence[position]
        for target in candidates[source]:
            if target in occupied:
                continue
            consistent = True
            for prior in sequence[:position]:
                if ((prior in neighbors[source]) != (image[prior] in neighbors[target])):
                    consistent = False
                    break
            if not consistent:
                continue
            image[source] = target
            occupied.add(target)
            search(position + 1)
            occupied.remove(target)
            image[source] = -1

    search(0)
    return answer


def raw_valid_count(order, edges, capacity):
    neighbors = [set() for _ in range(order)]
    for left, right in edges:
        neighbors[left].add(right)
        neighbors[right].add(left)
    sequence = sorted(range(order), key=lambda vertex: (-len(neighbors[vertex]), vertex))
    assigned = [-1] * order
    used = [0, 0, 0, 0]
    total = 0

    def search(position):
        nonlocal total
        if position == order:
            total += 1
            return
        vertex = sequence[position]
        for color in range(4):
            if used[color] == capacity[color]:
                continue
            if color == 0 and any(assigned[other] == 1 for other in neighbors[vertex]):
                continue
            if color == 1 and any(assigned[other] == 0 for other in neighbors[vertex]):
                continue
            assigned[vertex] = color
            used[color] += 1
            search(position + 1)
            used[color] -= 1
            assigned[vertex] = -1

    search(0)
    return total


def load_cover(filename):
    data = filename.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != EXPECTED_BYTES or digest != EXPECTED_SHA256:
        raise RuntimeError(f"frozen cover changed: bytes={len(data)} sha256={digest}")
    lines = data.decode("ascii").splitlines()
    expected_header = [
        "m6-rooted-cell-placement-cover-v1",
        "supports\t68",
        "colors\tR,A,B,C",
        "forbidden\tR-A",
        "capacities\tB6:1,8,6,3;B7:1,8,7,2",
        f"count\t{EXPECTED_ROWS}",
    ]
    if lines[:6] != expected_header or not lines[6].startswith("branch-orders\t"):
        raise RuntimeError("invalid placement-cover header")
    rows = defaultdict(list)
    for expected_index, line in enumerate(lines[7:]):
        fields = line.split("\t")
        if len(fields) != 7 or fields[0] != f"{expected_index:07d}":
            raise RuntimeError(f"malformed cover row {expected_index}")
        _, branch, support, order, graph6, word, weight = fields
        if branch not in CAPACITIES or any(char not in COLORS for char in word):
            raise RuntimeError(f"bad branch/color at row {expected_index}")
        rows[(branch, int(support))].append((int(order), graph6, tuple(COLORS.index(c) for c in word), int(weight)))
    if sum(map(len, rows.values())) != EXPECTED_ROWS:
        raise RuntimeError("wrong cover row count")
    return rows, digest, lines[6]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cover", type=Path)
    parser.add_argument("--supports", type=Path, default=Path(__file__).with_name("m6-support-census.txt"))
    args = parser.parse_args()
    supports = load_supports(args.supports)
    cover, digest, count_header = load_cover(args.cover)
    row_counts = Counter()
    raw_counts = Counter()

    for support in range(68):
        order, graph6, edges = supports[support]
        group = full_automorphism_group(order, edges)
        for branch, capacity in CAPACITIES.items():
            entries = cover[(branch, support)]
            representatives = set()
            orbit_total = 0
            for row_order, row_graph6, coloring, stated_weight in entries:
                if row_order != order or row_graph6 != graph6 or len(coloring) != order:
                    raise RuntimeError(f"support identity mismatch in {branch}/{support:03d}")
                if any(coloring.count(color) > capacity[color] for color in range(4)):
                    raise RuntimeError(f"capacity violation in {branch}/{support:03d}")
                if any({coloring[u], coloring[v]} == {0, 1} for u, v in edges):
                    raise RuntimeError(f"forbidden R-A edge in {branch}/{support:03d}")
                images = {tuple(coloring[permutation[vertex]] for vertex in range(order)) for permutation in group}
                representative = min(images)
                if coloring != representative or representative in representatives:
                    raise RuntimeError(f"noncanonical or duplicate orbit in {branch}/{support:03d}")
                if len(images) != stated_weight:
                    raise RuntimeError(
                        f"orbit weight mismatch in {branch}/{support:03d}: {stated_weight} != {len(images)}"
                    )
                representatives.add(representative)
                orbit_total += stated_weight
            raw_total = raw_valid_count(order, edges, capacity)
            if orbit_total != raw_total:
                raise RuntimeError(
                    f"incomplete orbit partition in {branch}/{support:03d}: {orbit_total} != {raw_total}"
                )
            row_counts[branch, order] += len(entries)
            raw_counts[branch, order] += raw_total

    header = "branch-orders\t" + ";".join(
        branch + ":" + ",".join(f"{order}:{row_counts[branch, order]}" for order in range(4, 13))
        for branch in ("B6", "B7")
    )
    if header != count_header:
        raise RuntimeError("branch/order header does not match audited rows")
    print(f"PASS rows={sum(row_counts.values())} bytes={EXPECTED_BYTES} sha256={digest}")
    for branch in ("B6", "B7"):
        print(branch + " orbits=" + ",".join(str(row_counts[branch, order]) for order in range(4, 13)))
        print(branch + " raw=" + ",".join(str(raw_counts[branch, order]) for order in range(4, 13)))


if __name__ == "__main__":
    main()
