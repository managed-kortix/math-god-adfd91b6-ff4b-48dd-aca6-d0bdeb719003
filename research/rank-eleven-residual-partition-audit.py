#!/usr/bin/env python3
"""Exact rank-eleven colored-partition audit under proven rank <= 10 bounds.

This is a finite ledger and structural-endpoint audit, not a rank-eleven
theorem checker.  It does not verify graph realizability or endpoint closure.
"""

from __future__ import annotations

from fractions import Fraction


TRIANGLE_MARGIN = {
    1: 0,
    2: 1,
    3: 2,
    4: 3,
    5: 2,
    6: 1,
    7: 0,
    8: 0,
    9: 0,
    10: 0,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def partitions(triangles, distinguished, minimum=(0, 0)):
    rows = []
    for triangle_count in range(triangles + 1):
        for distinguished_count in range(distinguished + 1):
            part = (triangle_count, distinguished_count)
            if part == (0, 0) or part < minimum:
                continue
            if part == (triangles, distinguished):
                rows.append((part,))
                continue
            for rest in partitions(
                triangles - triangle_count,
                distinguished - distinguished_count,
                part,
            ):
                rows.append((part,) + rest)
    return tuple(rows)


def triangle_bound(triangles):
    require(triangles in TRIANGLE_MARGIN, f"missing proven A_{triangles} bound")
    return Fraction(TRIANGLE_MARGIN[triangles]), True


def tq_bound(part):
    triangles, q_count = part
    require(q_count in (0, 1), f"invalid TQ part {part}")
    rank = triangles + q_count
    require(rank <= 10, f"direct ledger retained rank-{rank} TQ part")
    if q_count == 0:
        return triangle_bound(triangles)
    if triangles == 0:
        return Fraction(-1), False
    if triangles == 1:
        return Fraction(0), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def tpp_bound(part):
    triangles, pentagons = part
    require(pentagons in (0, 1, 2), f"invalid TPP part {part}")
    rank = triangles + pentagons
    require(rank <= 10, f"direct ledger retained rank-{rank} TPP part")
    if pentagons == 0:
        return triangle_bound(triangles)
    if part == (0, 1):
        return Fraction(-1, 4), False
    if part == (1, 1):
        return Fraction(3, 4), True
    if part == (0, 2):
        return Fraction(0), True
    if part == (1, 2):
        return Fraction(3, 2), True
    if rank in (2, 3):
        return Fraction(0), False
    return Fraction(0), True


def audit(triangles, distinguished, bound):
    all_rows = partitions(triangles, distinguished)
    require(len(all_rows) == len(set(all_rows)), "duplicate colored partition")
    proper_rows = tuple(row for row in all_rows if len(row) > 1)
    direct_rows = []
    structural_rows = []
    for row in proper_rows:
        entries = tuple(bound(part) for part in row)
        total = sum((value for value, _ in entries), Fraction())
        strict = any(strict for _, strict in entries)
        target = direct_rows if total > 0 or (total == 0 and strict) else structural_rows
        target.append(row)
    require(len(direct_rows) + len(structural_rows) == len(proper_rows), "lost row")
    return all_rows, proper_rows, tuple(direct_rows), tuple(structural_rows)


EXPECTED_T10Q = (
    ((0, 1),) + ((1, 0),) * 10,
    ((0, 1),) + ((1, 0),) * 3 + ((7, 0),),
    ((0, 1), (1, 0), (1, 0), (8, 0)),
    ((0, 1), (1, 0), (9, 0)),
    ((0, 1), (10, 0)),
)

EXPECTED_T9PP = (
    ((0, 1), (0, 1)) + ((1, 0),) * 9,
    ((0, 1), (0, 1), (1, 0), (1, 0), (7, 0)),
    ((0, 1), (0, 1), (1, 0), (8, 0)),
    ((0, 1), (0, 1), (9, 0)),
    ((0, 1),) + ((1, 0),) * 7 + ((2, 1),),
    ((0, 1),) + ((1, 0),) * 6 + ((3, 1),),
    ((0, 1),) + ((1, 0),) * 5 + ((4, 1),),
    ((0, 1),) + ((1, 0),) * 4 + ((5, 1),),
    ((0, 1),) + ((1, 0),) * 3 + ((6, 1),),
    ((0, 1),) + ((1, 0),) * 2 + ((7, 1),),
    ((0, 1), (1, 0), (8, 1)),
    ((0, 1), (2, 1), (7, 0)),
    ((0, 1), (9, 1)),
)

# These are candidate minimal forms identified by the structural rows and the
# elementary leaf/path tests. Vertical order records the required reduced-tree
# order; this table does not assert topology exhaustion, realizability, or
# positivity of an endpoint.
ENDPOINTS = {
    "T^10Q": ("A_10|Q",),
    "T^9PP": ("T^9P_0|P_1", "P_0|A_9|P_1", "P_0|A_7|T^2P_1"),
}

ENDPOINT_SOURCES = {
    "A_10|Q": ("T^10Q", ((0, 1), (10, 0)), Fraction(-1)),
    "T^9P_0|P_1": ("T^9PP", ((0, 1), (9, 1)), Fraction(-1, 4)),
    "P_0|A_9|P_1": ("T^9PP", ((0, 1), (0, 1), (9, 0)), Fraction(-1, 2)),
    "P_0|A_7|T^2P_1": ("T^9PP", ((0, 1), (2, 1), (7, 0)), Fraction(-1, 4)),
}


def check_endpoints(results):
    profiles = {
        "A_10|Q": (10, 1),
        "T^9P_0|P_1": (10, 1),
        "P_0|A_9|P_1": (1, 9, 1),
        "P_0|A_7|T^2P_1": (1, 7, 3),
    }
    require(set(profiles) == set(sum(ENDPOINTS.values(), ())), "endpoint table mismatch")
    require(set(profiles) == set(ENDPOINT_SOURCES), "endpoint source table mismatch")
    for name, ranks in profiles.items():
        require(sum(ranks) == 11, f"{name} has wrong total rank")
        require(all(rank <= 10 for rank in ranks), f"{name} exceeds lower-rank input")
        residual, row, expected_total = ENDPOINT_SOURCES[name]
        require(row in results[residual][3], f"{name} source is not structural")
        bound = tq_bound if residual == "T^10Q" else tpp_bound
        total = sum((bound(part)[0] for part in row), Fraction())
        require(total == expected_total, f"{name} endpoint ledger changed")


def display(name, result):
    all_rows, proper_rows, direct_rows, structural_rows = result
    print(
        f"{name}: total={len(all_rows)} proper={len(proper_rows)} "
        f"direct={len(direct_rows)} structural={len(structural_rows)}"
    )
    for row in structural_rows:
        print("  structural", row)
    for endpoint in ENDPOINTS[name]:
        print("  candidate minimal endpoint", endpoint)


def main():
    print("BOUNDARY: exact conditional audit using proven connected ranks <= 10")
    print("NO CLAIM: no rank-eleven theorem or endpoint closure is asserted")
    results = {
        "T^10Q": audit(10, 1, tq_bound),
        "T^9PP": audit(9, 2, tpp_bound),
    }
    expected = {
        "T^10Q": ((139, 138, 133, 5), EXPECTED_T10Q),
        "T^9PP": ((267, 266, 253, 13), EXPECTED_T9PP),
    }
    for name, result in results.items():
        counts = tuple(len(rows) for rows in result)
        require(counts == expected[name][0], f"{name} counts changed: {counts}")
        require(result[3] == expected[name][1], f"{name} structural rows changed")
        for row in result[1]:
            expected_triangles = 10 if name == "T^10Q" else 9
            expected_distinguished = 1 if name == "T^10Q" else 2
            require(sum(part[0] for part in row) == expected_triangles, "triangle mass changed")
            require(
                sum(part[1] for part in row) == expected_distinguished,
                "distinguished mass changed",
            )
        display(name, result)
    check_endpoints(results)
    print("PASS: frozen counts, rows, exact ledgers, masses, and endpoint ranks")


if __name__ == "__main__":
    main()
