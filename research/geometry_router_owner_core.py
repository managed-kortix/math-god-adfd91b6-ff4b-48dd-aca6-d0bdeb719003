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


@dataclass(frozen=True, order=True)
class CutSite:
    """One canonical physical vertex shared by every incidence at a cut."""

    cut: int


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


def undirected_edge(edge):
    require(len(edge) == 2 and edge[0] != edge[1], "physical edge is a loop")
    return frozenset(edge)


def verify_physical_owner_certificate(expected_vertices, expected_edges,
                                      expected_attachment_domain, vertices, edges,
                                      owner_records, attachment_owner_records, owners):
    """Check an exhaustive physical graph and connected induced owner territories.

    Expected graph and attachment domains are independently reconstructed by the
    caller. Submitted vertices, edges, and owner ledgers must match those domains
    exactly. Cross-owner edges are boundary edges and are not available when a
    terminal's connectivity is checked.
    """
    expected_vertices = tuple(expected_vertices)
    expected_edges = tuple(tuple(edge) for edge in expected_edges)
    expected_attachment_domain = tuple(expected_attachment_domain)
    vertices = tuple(vertices)
    edges = tuple(tuple(edge) for edge in edges)
    owners = tuple(owners)
    require(len(expected_vertices) == len(set(expected_vertices)),
            "expected physical vertex domain has aliases")
    expected_edge_keys = tuple(undirected_edge(edge) for edge in expected_edges)
    require(len(expected_edge_keys) == len(set(expected_edge_keys)),
            "expected physical edge domain has duplicates")
    require(all(endpoint in set(expected_vertices) for edge in expected_edges
                for endpoint in edge),
            "expected physical edge has an endpoint outside its vertex domain")
    require(len(expected_attachment_domain) == len(set(expected_attachment_domain)) and
            set(expected_attachment_domain) <= set(expected_vertices),
            "expected physical attachment domain is invalid")
    require(len(vertices) == len(set(vertices)), "physical vertex domain has aliases")
    require(set(vertices) == set(expected_vertices),
            "submitted physical vertex domain differs from reconstructed domain")
    require(len(owners) == len(set(owners)), "physical certificate repeats an owner")
    edge_keys = tuple(undirected_edge(edge) for edge in edges)
    require(len(edge_keys) == len(set(edge_keys)), "physical edge domain has duplicates")
    require(set(edge_keys) == set(expected_edge_keys),
            "submitted physical edge domain differs from reconstructed domain")
    require(all(endpoint in set(vertices) for edge in edges for endpoint in edge),
            "physical edge has an endpoint outside the vertex domain")
    owner_map = exact_owner_map(
        owner_records, expected_vertices, "physical vertex owners"
    )
    attachment_map = exact_owner_map(
        attachment_owner_records, expected_attachment_domain,
        "physical attachment owners"
    )
    require(set(owner_map.values()) == set(owners),
            "physical certificate has an inexact final-owner range")
    require(all(owner in set(owners) for owner in attachment_map.values()),
            "physical attachment has an unknown owner")
    require(all(attachment_map[vertex] == owner_map[vertex]
                for vertex in expected_attachment_domain),
            "physical attachment does not follow its vertex owner")

    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        if owner_map[left] == owner_map[right]:
            adjacency[left].add(right)
            adjacency[right].add(left)
    owned_vertices = {}
    for owner in owners:
        domain = {vertex for vertex in vertices if owner_map[vertex] == owner}
        require(domain, "physical terminal owner has an empty domain")
        seen = {next(iter(domain))}
        stack = list(seen)
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor in domain and neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        require(seen == domain, "owned physical terminal graph is disconnected")
        owned_vertices[owner] = frozenset(domain)
    return owner_map, tuple(edge_keys), owned_vertices
