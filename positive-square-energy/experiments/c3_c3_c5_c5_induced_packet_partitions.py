#!/usr/bin/env python3
"""Exhaustive induced-packet certificates for the 20 shared C3355 cores."""

from __future__ import annotations

import importlib.util
import itertools
from dataclasses import dataclass
from decimal import Decimal, getcontext
from pathlib import Path

import networkx as nx


EXPECTED_COUNT = 20
EXPECTED_SCORES = (
    (-1, 0, True),
    (5, -2, True),
    (3, -1, True),
    (3, -1, True),
    (0, 0, True),
    (5, -2, True),
    (5, -2, True),
    (3, -1, True),
    (3, -1, True),
    *((3, -1, True),) * 11,
)


@dataclass(frozen=True)
class Credit:
    """The exact lower-bound credit a + b*sqrt(5), plus strictness."""

    a: int
    b: int = 0
    strict: bool = False

    def __add__(self, other: "Credit") -> "Credit":
        return Credit(self.a + other.a, self.b + other.b, self.strict or other.strict)

    def positive(self) -> bool:
        return compare_radicals(self.a, self.b, 0, 0) > 0 or (
            compare_radicals(self.a, self.b, 0, 0) == 0 and self.strict
        )

    def decimal(self) -> Decimal:
        return Decimal(self.a) + Decimal(self.b) * Decimal(5).sqrt()

    def expression(self) -> str:
        if self.b == 0:
            return str(self.a)
        sign = "+" if self.b > 0 else "-"
        radical = "sqrt(5)" if abs(self.b) == 1 else f"{abs(self.b)}*sqrt(5)"
        return f"{self.a}{sign}{radical}"


@dataclass(frozen=True)
class Packet:
    mask: int
    cycles: tuple[str, ...]
    rule: str
    credit: Credit


def compare_radicals(a1: int, b1: int, a2: int, b2: int) -> int:
    """Compare a1+b1*sqrt(5) and a2+b2*sqrt(5) using integer arithmetic."""

    a = a1 - a2
    b = b1 - b2
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    square_comparison = (a * a > 5 * b * b) - (a * a < 5 * b * b)
    return square_comparison if a > 0 else -square_comparison


def better(left: Credit, right: Credit | None) -> bool:
    if right is None:
        return True
    comparison = compare_radicals(left.a, left.b, right.a, right.b)
    return comparison > 0 or (comparison == 0 and left.strict and not right.strict)


def load_census_module():
    path = Path(__file__).with_name("c3_c3_c5_c5_shared_cluster_certificate.py")
    spec = importlib.util.spec_from_file_location("c3355_census", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load census module at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def packet_for_mask(
    graph: nx.Graph, cycles: tuple[tuple[int, ...], ...], mask: int
) -> Packet | None:
    vertices = tuple(vertex for vertex in graph if mask & (1 << vertex))
    induced = graph.subgraph(vertices)
    if not nx.is_connected(induced):
        return None

    contents = tuple(
        ("T" if len(cycle) == 3 else "P") + str(index)
        for index, cycle in enumerate(cycles)
        if all(mask & (1 << vertex) for vertex in cycle)
    )
    triangles = sum(label.startswith("T") for label in contents)
    pentagons = len(contents) - triangles
    beta = induced.number_of_edges() - induced.number_of_nodes() + 1
    if beta != len(contents):
        raise RuntimeError("induced cactus cycle count disagrees with cyclomatic number")

    if beta == 0:
        return Packet(mask, contents, "tree", Credit(-1))
    if pentagons == 0 and 1 <= triangles <= 2:
        return Packet(
            mask,
            contents,
            f"triangle-packing-{triangles}",
            Credit(triangles - 1, strict=True),
        )
    if triangles == 0 and pentagons == 1:
        return Packet(mask, contents, "C5-unicyclic", Credit(2, -1))
    if triangles == 1 and pentagons == 1:
        return Packet(mask, contents, "C3-C5-bicyclic", Credit(3, -1, strict=True))
    if triangles == 0 and pentagons == 2:
        return Packet(mask, contents, "bicyclic", Credit(0))
    return None


def best_partition(
    graph: nx.Graph, cycles: tuple[tuple[int, ...], ...]
) -> tuple[Credit, tuple[Packet, ...], int]:
    """DP over all connected-part refinements of all vertex set partitions."""

    order = graph.number_of_nodes()
    full = (1 << order) - 1
    packets = {
        mask: packet
        for mask in range(1, full + 1)
        if (packet := packet_for_mask(graph, cycles, mask)) is not None
    }
    best: list[Credit | None] = [None] * (full + 1)
    parts: list[tuple[Packet, ...]] = [()] * (full + 1)
    best[0] = Credit(0)
    transitions = 0
    for mask in range(1, full + 1):
        anchor = mask & -mask
        submask = mask
        while submask:
            if submask & anchor and submask in packets:
                transitions += 1
                remainder = mask ^ submask
                previous = best[remainder]
                if previous is not None:
                    candidate = previous + packets[submask].credit
                    if better(candidate, best[mask]):
                        best[mask] = candidate
                        parts[mask] = parts[remainder] + (packets[submask],)
            submask = (submask - 1) & mask
    if best[full] is None:
        raise RuntimeError("no admissible packet partition")
    return best[full], parts[full], transitions


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(vertex for vertex in range(mask.bit_length()) if mask & (1 << vertex))


def main() -> None:
    getcontext().prec = 30
    census = load_census_module()
    raw = census.enumerate_cores()
    canonical = sorted({census.canonical_cycles(cycles) for cycles in raw})
    if len(raw) != len(canonical) or len(canonical) != EXPECTED_COUNT:
        raise RuntimeError(
            f"census mismatch: graph quotient={len(raw)}, canonical quotient={len(canonical)}"
        )

    print(f"connected_shared_cut_cores={len(canonical)}")
    minimum: Credit | None = None
    observed_scores = []
    for index, cycles in enumerate(canonical, 1):
        graph = census.graph_from_cycles(cycles)
        score, packets, transitions = best_partition(graph, cycles)
        observed_scores.append((score.a, score.b, score.strict))
        if minimum is None or better(minimum, score):
            minimum = score
        print(
            f"type={index:02d} incidence={census.incidence_signature(cycles)} "
            f"score={score.expression()} decimal={score.decimal():.12f} "
            f"strict={str(score.strict).lower()} transitions={transitions} cycles={cycles}"
        )
        for packet_index, packet in enumerate(packets, 1):
            print(
                f"  packet={packet_index} vertices={vertices(packet.mask)} "
                f"cycles={packet.cycles or ('none',)} rule={packet.rule} "
                f"credit={packet.credit.expression()} strict={str(packet.credit.strict).lower()}"
            )
    assert minimum is not None
    if tuple(observed_scores) != EXPECTED_SCORES:
        raise RuntimeError(f"score profile drift: {observed_scores}")
    exact_positive_count = sum(
        compare_radicals(a, b, 0, 0) > 0 for a, b, _ in observed_scores
    )
    strict_target_count = sum(
        Credit(a, b, strict).positive() for a, b, strict in observed_scores
    )
    print(
        f"SUMMARY exact_positive={exact_positive_count}/{len(canonical)} "
        f"strict_target={strict_target_count}/{len(canonical)} "
        f"minimum_score={minimum.expression()} minimum_decimal={minimum.decimal():.12f}"
    )


if __name__ == "__main__":
    main()
