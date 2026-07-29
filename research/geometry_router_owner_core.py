#!/usr/bin/env python3
"""Shared fail-closed cyclic geometry and router-owner primitives.

The core deliberately knows nothing about packet theorems.  Endpoint verifiers
provide concrete cyclic positions and final owners; this module checks only the
geometry and exact owner domains on which those theorem ledgers depend.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@dataclass(frozen=True, order=True)
class CyclicVertex:
    cycle: str
    index: int
    role: str
    cut: int | None = None


@dataclass(frozen=True)
class CycleGeometry:
    label: str
    length: int
    vertices: tuple[object, ...]
    edges: tuple[tuple[object, object], ...]


def make_cycle(label, vertices):
    vertices = tuple(vertices)
    require(len(vertices) >= 3, "cyclic geometry has fewer than three vertices")
    require(len(vertices) == len(set(vertices)), "cycle repeats a concrete vertex")
    edges = tuple((vertices[index], vertices[(index + 1) % len(vertices)])
                  for index in range(len(vertices)))
    geometry = CycleGeometry(label, len(vertices), vertices, edges)
    verify_cycle(geometry)
    return geometry


def verify_cycle(geometry):
    require(len(geometry.vertices) == geometry.length and
            len(set(geometry.vertices)) == geometry.length,
            "cycle does not have distinct named vertices")
    require(geometry.edges == tuple(
        (geometry.vertices[index], geometry.vertices[(index + 1) % geometry.length])
        for index in range(geometry.length)),
        "cycle edges are not in named cyclic order")
    require(len({frozenset(edge) for edge in geometry.edges}) == geometry.length,
            "cycle repeats an undirected edge")


def verify_intervals(geometry, intervals, owner_count=None):
    """Verify an ordered, exact partition into proper cyclic intervals."""
    intervals = tuple(tuple(interval) for interval in intervals)
    if owner_count is not None:
        require(len(intervals) == owner_count, "interval/owner count mismatch")
    require(len(intervals) in (2, 3), "router must have two or three owners")
    flat = tuple(vertex for interval in intervals for vertex in interval)
    require(Counter(flat) == Counter(geometry.vertices),
            "cyclic intervals are not an exact vertex partition")
    require(all(0 < len(interval) < geometry.length for interval in intervals),
            "cyclic interval is empty or improper")
    edge_set = {frozenset(edge) for edge in geometry.edges}
    for interval in intervals:
        require(all(frozenset((left, right)) in edge_set
                    for left, right in zip(interval, interval[1:])),
                "interval is not consecutive in the named cycle")
    return tuple(len(interval) for interval in intervals)


def consecutive_intervals(geometry, part_counts=(2, 3)):
    """Enumerate ordered interval partitions with the requested part counts."""
    answer = []
    n = geometry.length
    for start in range(n):
        rotated = geometry.vertices[start:] + geometry.vertices[:start]
        if 2 in part_counts:
            for first in range(1, n):
                answer.append((rotated[:first], rotated[first:]))
        if 3 in part_counts:
            for first in range(1, n - 1):
                for second in range(first + 1, n):
                    answer.append((rotated[:first], rotated[first:second], rotated[second:]))
    for partition in answer:
        verify_intervals(geometry, partition)
    return tuple(answer)


def exact_owner_map(records, expected_domain, label):
    records = tuple(records)
    keys = tuple(key for key, _ in records)
    require(len(keys) == len(set(keys)), f"{label} has duplicate owner keys")
    require(set(keys) == set(expected_domain), f"{label} has an inexact owner domain")
    return dict(records)


def exact_relabel_map(records, expected_source, expected_target, label):
    """Build a bijective relabeling with independently supplied domains."""
    mapping = exact_owner_map(records, expected_source, f"{label} source")
    values = tuple(mapping.values())
    require(len(values) == len(set(values)), f"{label} aliases two source objects")
    require(set(values) == set(expected_target), f"{label} has an inexact target domain")
    return mapping


def verify_router_owner_split(geometry, intervals, owners, expected_sizes=None):
    """Bind ordered owners to concrete proper intervals of one router cycle."""
    require(len(owners) == len(set(owners)), "router has duplicate interval owners")
    sizes = verify_intervals(geometry, intervals, len(owners))
    if expected_sizes is not None:
        require(tuple(expected_sizes) == sizes,
                "ordered interval sizes do not match concrete owner intervals")
    return sizes
