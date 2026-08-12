#!/usr/bin/env python3
"""Exact exhaustive census of rank-seven suppressed kernels.

The generator performs one open-ear augmentation of every canonical rank-six
kernel.  Completeness is Theorem 4 of the accompanying removable-ear audit;
this verifier links to the independently regenerated rank-six census.
"""

import argparse
import importlib.util
import json
from collections import Counter
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RANK_SIX_PROGRAM = ROOT / "research" / "rank-six-kernel-census-verifier.py"
RANK_SIX_FIXTURE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
OUTPUT = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
EXPECTED_COUNTS = (1, 6, 47, 233, 914, 2270, 4015, 4495, 3396, 1391, 365)
SCHEMA = "rank-seven-loopless-no-cut-kernels-v2"
STATUS = "complete-proved-removable-ear-exhaustion"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_rank_six_module():
    spec = importlib.util.spec_from_file_location("rank_six_census", RANK_SIX_PROGRAM)
    require(spec is not None and spec.loader is not None, "cannot load rank-six census")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R6 = load_rank_six_module()


def is_rank_seven_kernel(n, code):
    try:
        degree_row = R6.degrees(n, code)
    except (TypeError, ValueError):
        return False
    return (
        2 <= n <= 12
        and sum(code) == n + 6
        and min(degree_row) >= 3
        and all(R6.connected_after_deleting(n, code, vertex) for vertex in range(n))
    )


def edge_list(n, code):
    edges = []
    for multiplicity, edge in zip(code, R6.pairs(n)):
        edges.extend([edge] * multiplicity)
    return edges


def encode(n, edges):
    indices = {edge: index for index, edge in enumerate(R6.pairs(n))}
    code = [0] * len(indices)
    for u, v in edges:
        require(u != v, "augmentation created a loop")
        code[indices[tuple(sorted((u, v)))]] += 1
    return tuple(code)


def augmentations(n, code):
    """Add an ear between vertices or interiors of physical kernel edges."""
    physical_edges = [tuple(edge) + (index,) for index, edge in enumerate(edge_list(n, code))]
    locations = [("v", vertex) for vertex in range(n)]
    locations.extend(("e",) + edge for edge in physical_edges)

    for left_index, left in enumerate(locations):
        for right in locations[left_index:]:
            if left == right and left[0] == "v":
                continue
            edges = edge_list(n, code)
            order = n
            if left == right:
                u, v = left[1:3]
                edges.remove((u, v))
                x, y = order, order + 1
                order += 2
                edges.extend(((u, x), (x, y), (x, y), (y, v)))
            else:
                endpoints = []
                for location in (left, right):
                    if location[0] == "v":
                        endpoints.append(location[1])
                    else:
                        u, v = location[1:3]
                        edges.remove((u, v))
                        x = order
                        order += 1
                        edges.extend(((u, x), (x, v)))
                        endpoints.append(x)
                edges.append(tuple(sorted(endpoints)))
            candidate = encode(order, edges)
            if is_rank_seven_kernel(order, candidate):
                yield order, R6.canonical_code(order, candidate)


def generate():
    require(R6.FIXTURE == RANK_SIX_FIXTURE, "rank-six fixture linkage changed")
    rank_six_rows, _, _, digest = R6.audit()
    require(digest == R6.EXPECTED_DIGEST, "rank-six exact audit digest changed")
    classes = set()
    for n, code in rank_six_rows:
        classes.update(augmentations(n, code))
    return tuple(sorted(classes))


def payload(classes):
    counts = [sum(n == order for n, _ in classes) for order in range(2, 13)]
    degree_counts = Counter(
        ",".join(map(str, sorted(R6.degrees(n, code), reverse=True)))
        for n, code in classes
    )
    support_counts = Counter(
        f"n={n},support={sum(value > 0 for value in code)}" for n, code in classes
    )
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "beta": 7,
        "minimum_degree": 3,
        "orders": [2, 12],
        "encoding": "lexicographic upper-triangle multiplicities",
        "generator": "proved-complete-one-open-ear-augmentation-of-exact-rank-six-census",
        "counts_by_order_n2_to_n12": counts,
        "degree_multiset_counts": dict(sorted(degree_counts.items())),
        "support_edge_counts": dict(sorted(support_counts.items())),
        "kernels": [{"n": n, "code": list(code)} for n, code in classes],
    }


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def audit(value, classes):
    require(set(value) == {
        "schema", "status", "beta", "minimum_degree", "orders", "encoding",
        "generator", "counts_by_order_n2_to_n12", "degree_multiset_counts",
        "support_edge_counts", "kernels",
    }, "payload fields changed")
    require(value["schema"] == SCHEMA, "schema changed")
    require(value["status"] == STATUS, "completeness status changed")
    require(value["beta"] == 7, "rank policy changed")
    require(value["minimum_degree"] == 3, "degree policy changed")
    require(value["orders"] == [2, 12], "order policy changed")
    require(value["counts_by_order_n2_to_n12"] == list(EXPECTED_COUNTS), "counts changed")
    require(len(classes) == sum(EXPECTED_COUNTS), "total changed")
    require(classes == tuple(sorted(set(classes))), "classes are not sorted and unique")
    for n, code in classes:
        require(is_rank_seven_kernel(n, code), "generated row is not a rank-seven kernel")
        require(code == R6.canonical_code(n, code), "generated row is not canonical")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write the canonical exhaustive fixture")
    args = parser.parse_args()
    classes = generate()
    value = payload(classes)
    audit(value, classes)
    raw = canonical_bytes(value)
    if args.write:
        OUTPUT.write_bytes(raw)
    else:
        require(OUTPUT.exists(), "committed exhaustive fixture is missing")
        require(OUTPUT.read_bytes() == raw, "committed exhaustive fixture differs from regeneration")
    print("rank-seven kernel census: exact exhaustive audit passed")
    print(f"status: {value['status']}")
    print("canonical_counts_n2_to_n12: " + ",".join(map(str, EXPECTED_COUNTS)))
    print(f"canonical_total: {len(classes)}")
    print(f"degree_multisets: {len(value['degree_multiset_counts'])}")
    print(f"canonical_payload_sha256: {sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
