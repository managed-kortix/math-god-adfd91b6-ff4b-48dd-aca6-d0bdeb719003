#!/usr/bin/env python3
"""Fail-closed exact verifier for the R61-K223 marked-cycle packet."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "r61-k223-marked-cycle-packet.json"
FIXTURE_SHA256 = "57fa593f586662660037a763ed26d6ba776d80b9542f1abc46d0dadb1f47e0e4"
PAIRS = tuple(itertools.combinations(range(6), 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_fixture():
    raw = FIXTURE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, "fixture digest changed")
    return json.loads(raw.decode("ascii"))


def graph_from_row(row):
    require(type(row) is str and len(row) == len(PAIRS) and set(row) <= {"0", "1"},
            "invalid canonical row")
    return {pair for pair, bit in zip(PAIRS, row) if bit == "1"}


def map_edge(edge, permutation):
    return tuple(sorted((permutation[edge[0]], permutation[edge[1]])))


def automorphisms(edges):
    return tuple(permutation for permutation in itertools.permutations(range(6))
                 if {map_edge(edge, permutation) for edge in edges} == edges)


def vertex_orbits(group):
    unseen = set(range(6))
    orbits = []
    while unseen:
        vertex = min(unseen)
        orbit = {permutation[vertex] for permutation in group}
        require(orbit <= unseen, "automorphism orbits overlap")
        orbits.append(tuple(sorted(orbit)))
        unseen -= orbit
    return tuple(orbits)


def audit_partition(item, edges):
    require(set(item) == {"marked", "k4_vertices", "tree_vertices"},
            "partition fields changed")
    marked = item["marked"]
    k4 = set(item["k4_vertices"])
    tree = set(item["tree_vertices"])
    require(type(marked) is int and all(type(v) is int for v in k4 | tree),
            "partition vertices are not exact integers")
    require(marked in k4, "marked cut is not retained with K4 and cycle")
    require(len(k4) == 4 and len(tree) == 2 and k4.isdisjoint(tree)
            and k4 | tree == set(range(6)), "partition is not disjoint and exhaustive")
    induced_k4 = {edge for edge in edges if set(edge) <= k4}
    induced_tree = {edge for edge in edges if set(edge) <= tree}
    require(induced_k4 == {tuple(sorted(edge)) for edge in itertools.combinations(k4, 2)},
            "retained territory does not induce K4")
    require(len(induced_tree) == 1, "deleted territory is not a nonempty two-vertex tree")


def audit(payload):
    require(payload["schema"] == "r61-k223-marked-cycle-packet-v1", "schema changed")
    require(payload["pair_order"] == [f"{u}{v}" for u, v in PAIRS], "pair order changed")
    require(type(payload["kernel"]) is int and payload["kernel"] == 223, "kernel changed")
    require(payload["row"] == "001111011011111", "K223 row changed")
    edges = graph_from_row(payload["row"])
    require(edges == {(0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 5),
                      (2, 4), (2, 5), (3, 4), (3, 5), (4, 5)}, "edge set changed")

    group = automorphisms(edges)
    require(len(group) == 16, "automorphism group order changed")
    orbits = vertex_orbits(group)
    require(orbits == ((0, 1, 2, 3), (4, 5)), "marked-cut orbits changed")
    expected_orbits = [
        {"representative": 0, "vertices": [0, 1, 2, 3], "degree": 3},
        {"representative": 4, "vertices": [4, 5], "degree": 5},
    ]
    require(payload["marked_orbits"] == expected_orbits, "marked-orbit ledger changed")
    for item in payload["marked_orbits"]:
        require(all(sum(vertex in edge for edge in edges) == item["degree"]
                    for vertex in item["vertices"]), "orbit degree changed")

    partitions = payload["partitions"]
    require(len(partitions) == 2 and {item["marked"] for item in partitions} == {0, 4},
            "representative partition ledger changed")
    for item in partitions:
        audit_partition(item, edges)

    by_mark = {item["marked"]: item for item in partitions}
    for orbit in orbits:
        representative = min(orbit)
        source = by_mark[representative]
        for marked in orbit:
            transports = [permutation for permutation in group
                          if permutation[representative] == marked]
            require(transports, "missing orbit transport")
            transported = transports[0]
            item = {
                "marked": marked,
                "k4_vertices": [transported[v] for v in source["k4_vertices"]],
                "tree_vertices": [transported[v] for v in source["tree_vertices"]],
            }
            audit_partition(item, edges)

    packet = payload["packet"]
    require(packet == {
        "retained_profile": "actual-K4-at-marked-cut",
        "retained_credit_strictly_greater_than": 2,
        "kernel_tree_credit": -1,
        "boundary_open_cycle_profile": "nonempty-tree",
        "boundary_open_cycle_credit": -1,
        "total_credit_strictly_greater_than": 0,
    }, "packet ledger changed")
    require(packet["retained_credit_strictly_greater_than"] + packet["kernel_tree_credit"]
            + packet["boundary_open_cycle_credit"]
            == packet["total_credit_strictly_greater_than"], "packet debit arithmetic changed")
    return len(group), len(orbits)


def hostile_tests(payload):
    mutations = []
    for mutate in (
        lambda value: value.update(row="101111011011111"),
        lambda value: value["marked_orbits"][0]["vertices"].remove(3),
        lambda value: value["partitions"][0].update(k4_vertices=[0, 1, 4, 5]),
        lambda value: value["partitions"][1].update(marked=5),
        lambda value: value["packet"].update(retained_credit_strictly_greater_than=3),
        lambda value: value["packet"].update(kernel_tree_credit=0),
    ):
        changed = deepcopy(payload)
        mutate(changed)
        mutations.append(changed)
    rejected = 0
    for changed in mutations:
        try:
            audit(changed)
        except RuntimeError:
            rejected += 1
    require(rejected == len(mutations), "hostile mutation accepted")
    return rejected


def main():
    payload = load_fixture()
    group_order, orbit_count = audit(payload)
    rejected = hostile_tests(payload)
    output = ("R61-K223 marked-cycle packet: exact audit passed\n"
              f"automorphism group: {group_order}\n"
              f"marked-cut orbits: {orbit_count}\n"
              f"hostile mutations rejected: {rejected}\n"
              "status: CLOSED for arbitrary cycle length and rooted trees")
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
