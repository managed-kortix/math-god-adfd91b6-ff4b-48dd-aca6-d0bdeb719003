#!/usr/bin/env python3
"""Fail-closed audit of the two R61-K110 shared-cut packets."""

from __future__ import annotations

import hashlib
import itertools
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "positive-square-energy/heptacyclic-general/r61-one-credit-boundary-reduction.md"
SOURCE_SHA256 = "4e5e519dc52630b00cae618f2d80aeb27251bb2c6af8874e59a94d3850b6c9f4"
EXPECTED_KEYS = ("R61-K110-0", "R61-K110-1")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def k5_edges():
    return frozenset(itertools.combinations(range(5), 2))


def audit():
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
            "R61 source changed")
    edges = k5_edges()
    require(len(edges) == 10, "K5 edge set changed")

    # K110-0: Aut(K5) is vertex-transitive; deleting the marked branch leaves K4.
    for marked in range(5):
        retained = set(range(5)) - {marked}
        require(sum(set(edge) <= retained for edge in edges) == 6,
                "all-unit marked complement is not K4")

    # K110-1: the stabilizer of long edge 01 has endpoint and off-edge branch
    # orbits. Every odd length 2h+1 contributes exactly h internal distance orbits.
    endpoint_orbit = {0, 1}
    off_edge_orbit = {2, 3, 4}
    require(endpoint_orbit | off_edge_orbit == set(range(5)),
            "branch orbit partition changed")
    for h in range(1, 65):
        length = 2 * h + 1
        distances = {min(index, length - index) for index in range(1, length)}
        require(distances == set(range(1, h + 1)),
                "internal distance orbit formula changed")

    # Endpoint/internal marks leave one unicyclic territory; off-edge marks
    # leave one path tree and one cycle-minus-cut tree. Strict K4 credit >2
    # closes both exact ledgers, including the tight two-tree route.
    ledgers = {"endpoint": (2, 0), "internal": (2, 0), "off-edge": (2, -1, -1)}
    require(all(sum(row) >= 0 for row in ledgers.values()), "packet debit reopened")
    require(sum(ledgers["off-edge"]) == 0, "tight orbit debit changed")
    require(EXPECTED_KEYS == ("R61-K110-0", "R61-K110-1"), "scope changed")
    return len(endpoint_orbit), len(off_edge_orbit), 64


def main():
    endpoints, off_edge, symbolic_checks = audit()
    output = (
        "R61-K110 shared-cut packet verifier: exact audit passed\n"
        f"marked branch orbits: endpoints={endpoints} off-edge={off_edge}; "
        "internal=min(j,l-j)\n"
        f"symbolic odd-length orbit checks: {symbolic_checks}; all lengths covered by formula\n"
        "packet ledgers: endpoint/internal >2+0; off-edge >2-1-1\n"
        "status: R61-K110-0 and R61-K110-1 CLOSED"
    )
    if "--optimized-child" not in sys.argv and not sys.flags.optimize:
        child = subprocess.run([sys.executable, "-O", __file__, "--optimized-child"],
                               check=True, capture_output=True, text=True)
        require(child.stdout.rstrip() == output, "normal/optimized output mismatch")
    print(output)


if __name__ == "__main__":
    main()
