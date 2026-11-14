#!/usr/bin/env python3
"""NONPROMOTIONAL exact census for the abstract R21 D+4T reduction.

This program does not prove any spectral packet bound.  It exhausts the finite
labelled decorated block-cut-tree quotient defined in the accompanying hostile
note and checks the purely combinatorial pruning/ownership lemma.  Channel words are
computed; no graph record supplies one.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
import subprocess
import sys
from collections import Counter, deque
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Callable, Iterable


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


TRIANGLES = ("T0", "T1", "T2", "T3")
ROOT = "D"
REPO = Path(__file__).resolve().parents[1]

# Exact semantic sources.  Each entry below is paired with statement text and
# an explicit use-site check in audit_sources(); these are not inert hash pins.
SOURCE_PINS = {
    "attached-diamond-and-dt": (
        "positive-square-energy/pentacyclic-general/"
        "doubled-c4-111-two-triangles-retained-packet.md",
        "4fec746a4cf479b360e5c8692221bf796b6c260a7f9afc2bad37e404574ca00b"),
    "dtt-note": (
        "positive-square-energy/pentacyclic-general/diamond-two-triangle-exact-packet.md",
        "9107ef2821d441da401079982ae8d0b6c98cee17ae7e52268a9b6ad895b8e11b"),
    "dtt-semantic-child": (
        "research/diamond-two-triangle-packet-verifier.py",
        "24da5324c6695de4795fbd7885fbeadf986fabe1b52e2aec2082c92223addc9a"),
    "triangular-cactus": (
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791"),
    "hostile-unicycle": (
        "all-tricyclic-cacti/paper.tex",
        "d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8"),
    "undecorated-selector": (
        "research/r21-bridge-free-dtt-selector-verifier.py",
        "3da7fa8504b56764bf0d3658f13e15f7c2d568782c11636d108513cc29adaf41"),
    "r21-residual-sieve": (
        "positive-square-energy/heptacyclic-general/"
        "rank-seven-multiblock-debit-ledger.md",
        "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5"),
}
DTT_CHILD_OUTPUT_SHA256 = "a6f61bdafa04dcc1705634ab7b026b7ce5c0cf1b9d7809cf0f5e7b94b7034ff2"
SELECTOR_OUTPUT_SHA256 = "b3d41047454e1e0c087f9591d8d8954a4ea1228357f44555832c424d1acfa168"
EXPECTED_CASES = 606_783
EXPECTED_CASES_BY_K = {0: 15, 1: 240, 2: 3456, 3: 43200, 4: 559872}
EXPECTED_PORT_COLORED_BY_K = {0: 1, 1: 12, 2: 288, 3: 10800, 4: 559872}
EXPECTED_CHANNELS = {"D": 15, "DT": 240, "DTT": 606528}
EXPECTED_CANONICAL_SHA256 = "86bf42d05f7d611607f7e7d4e58e797e717e935473ae2f459c02ae8016076eae"


@dataclass(frozen=True)
class Cut:
    members: frozenset[str]
    ports: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class Cluster:
    root_triangles: tuple[str, ...]
    cuts: tuple[Cut, ...]


@dataclass(frozen=True)
class ReducedCase:
    root_cluster: Cluster
    # Each group is the set of marked triangle blocks in one component cut off
    # by a first actual K2 bridge of the D-rooted CYCLIC HULL.  It is never an
    # arbitrary bridge in a rank-zero rooted payload.
    bridge_groups: tuple[tuple[str, ...], ...]
    chain_lengths: tuple[tuple[tuple[str, ...], int], ...]
    # This flag is part of the reduced-contract witness, not a proof by fiat:
    # the accompanying original-graph argument proves that the simultaneous
    # first/rootmost K2 deletion was made before this quotient is formed.
    rootmost_cyclic_route_k2_deleted: bool
    # payload_mass is only a quotient statistic: total erased vertices over
    # all separately assigned, uniquely rooted acyclic components whose roots
    # land in the named destination territory.  It is not one physical tree.
    payload_mass: tuple[tuple[str, int], ...]
    segment_lengths: tuple[tuple[str, tuple[int, ...]], ...]


@dataclass(frozen=True)
class Certificate:
    channel: str
    selected_anchor: tuple[str, ...]
    opened_groups: tuple[tuple[str, ...], ...]
    owner_partition: tuple[tuple[str, tuple[str, ...]], ...]
    ledger: tuple[tuple[str, int, bool], ...]


def set_partitions(items: tuple[str, ...]) -> Iterable[tuple[frozenset[str], ...]]:
    """Every set partition, canonicalized later by the caller."""
    if not items:
        yield ()
        return
    head = items[0]
    for tail in set_partitions(items[1:]):
        yield (frozenset({head}), *tail)
        for index in range(len(tail)):
            yield (*tail[:index], tail[index] | {head}, *tail[index + 1:])


def canonical_partition(parts: Iterable[Iterable[str]]) -> tuple[tuple[str, ...], ...]:
    return tuple(sorted(tuple(sorted(part)) for part in parts))


def incidence(cluster: Cluster) -> dict[tuple[str, object], set[tuple[str, object]]]:
    blocks = (ROOT, *cluster.root_triangles)
    answer = {("B", block): set() for block in blocks}
    for index, cut in enumerate(cluster.cuts):
        cut_node = ("C", index)
        answer[cut_node] = set()
        for block in cut.members:
            block_node = ("B", block)
            answer[cut_node].add(block_node)
            answer[block_node].add(cut_node)
    return answer


def path(graph: dict[tuple[str, object], set[tuple[str, object]]],
         start: tuple[str, object], finish: tuple[str, object]) -> tuple[tuple[str, object], ...]:
    previous: dict[tuple[str, object], tuple[str, object] | None] = {start: None}
    queue = deque([start])
    while queue and finish not in previous:
        current = queue.popleft()
        for neighbor in sorted(graph[current], key=repr):
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    require(finish in previous, "incidence path is disconnected")
    answer = []
    current: tuple[str, object] | None = finish
    while current is not None:
        answer.append(current)
        current = previous[current]
    return tuple(reversed(answer))


def valid_cluster(cluster: Cluster) -> bool:
    if (tuple(sorted(cluster.root_triangles)) != cluster.root_triangles or
            len(set(cluster.root_triangles)) != len(cluster.root_triangles) or
            not set(cluster.root_triangles) <= set(TRIANGLES)):
        return False
    blocks = (ROOT, *cluster.root_triangles)
    graph = incidence(cluster)
    edge_count = sum(len(neighbors) for neighbors in graph.values()) // 2
    if edge_count != len(graph) - 1:
        return False
    reached = {("B", ROOT)}
    queue = list(reached)
    while queue:
        current = queue.pop()
        for neighbor in graph[current]:
            if neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    if reached != set(graph):
        return False
    for cut in cluster.cuts:
        if len(cut.members) < 2 or not set(cut.members) <= set(blocks):
            return False
        ports = dict(cut.ports)
        if (len(cut.ports) != len(cut.members) or
                len(ports) != len(cut.members) or
                set(ports) != set(cut.members)):
            return False
        # D has four physical vertices; a triangle has three.  Port indices
        # are literal integers, and one block may occur only once at one cut.
        # Reusing a physical port across distinct cuts is forbidden below.
        if not all(type(port) is int and 0 <= port < (4 if block == ROOT else 3)
                   for block, port in cut.ports):
            return False
    used_ports: set[tuple[str, int]] = set()
    for cut in cluster.cuts:
        for item in cut.ports:
            if item in used_ports:
                return False
            used_ports.add(item)
    return True


def generate_uncolored_clusters(root_triangles: tuple[str, ...]) -> tuple[tuple[frozenset[str], ...], ...]:
    blocks = (ROOT, *root_triangles)
    if len(blocks) == 1:
        return ((),)
    candidate_cuts = tuple(frozenset(current)
                           for size in range(2, len(blocks) + 1)
                           for current in itertools.combinations(blocks, size))
    answer = []
    for number in range(1, len(blocks)):
        for chosen in itertools.combinations(candidate_cuts, number):
            # Incidence-tree edge count is a necessary and strong filter.
            if sum(map(len, chosen)) != len(blocks) + number - 1:
                continue
            dummy = Cluster(root_triangles,
                            tuple(Cut(members, tuple((block, 0) for block in sorted(members)))
                                  for members in chosen))
            graph = incidence(dummy)
            reached = {("B", ROOT)}
            queue = list(reached)
            while queue:
                current = queue.pop()
                for neighbor in graph[current]:
                    if neighbor not in reached:
                        reached.add(neighbor)
                        queue.append(neighbor)
            if len(reached) == len(graph):
                answer.append(tuple(chosen))
    return tuple(answer)


def port_colorings(root_triangles: tuple[str, ...],
                   cuts: tuple[frozenset[str], ...]) -> Iterable[Cluster]:
    incidences = tuple((cut_index, block)
                       for cut_index, members in enumerate(cuts)
                       for block in sorted(members))
    domains = tuple(range(4 if block == ROOT else 3) for _, block in incidences)
    for ports in itertools.product(*domains):
        used: set[tuple[str, int]] = set()
        valid = True
        records = [[] for _ in cuts]
        for (cut_index, block), port in zip(incidences, ports):
            item = (block, port)
            if item in used:
                valid = False
                break
            used.add(item)
            records[cut_index].append(item)
        if not valid:
            continue
        cluster = Cluster(root_triangles,
                          tuple(Cut(cuts[index], tuple(sorted(records[index])))
                                for index in range(len(cuts))))
        require(valid_cluster(cluster), "generated physical port coloring is invalid")
        yield cluster


def node_depths(cluster: Cluster) -> dict[tuple[str, object], int]:
    graph = incidence(cluster)
    depths: dict[tuple[str, object], int] = {("B", ROOT): 0}
    queue = deque([("B", ROOT)])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in depths:
                depths[neighbor] = depths[node] + 1
                queue.append(neighbor)
    require(len(depths) == len(graph), "incidence tree is disconnected")
    return depths


def select_anchor_pair(cluster: Cluster) -> tuple[str, str]:
    """Choose the two least-depth retained T block nodes (ties by label)."""
    require(len(cluster.root_triangles) >= 2, "DTT selection needs two root triangles")
    depths = node_depths(cluster)
    pair = tuple(sorted(cluster.root_triangles,
                        key=lambda name: (depths[("B", name)], name))[:2])
    require(len(pair) == 2, "least-depth DTT selector failed")
    graph = incidence(cluster)
    hull = set(path(graph, ("B", ROOT), ("B", pair[0])))
    hull |= set(path(graph, ("B", ROOT), ("B", pair[1])))
    marked = {node[1] for node in hull if node[0] == "B"}
    require(marked == {ROOT, *pair},
            "least-depth DTT hull contains a third marked triangle")
    return pair


def cut_closed_ownership(cluster: Cluster, pair: tuple[str, str]) -> tuple[
        frozenset[tuple[str, object]], tuple[tuple[str, ...], ...],
        tuple[tuple[int, str], ...]]:
    """Return cut-closed S and its separate c->unselected-T territories.

    K0 is the minimal D,T,T incidence hull.  S adjoins *every* cut incident
    with any retained block of K0.  In the original graph the conclusion that
    every cyclic frontier is cut-node -> unselected-triangle uses BOTH this
    cut closure and the prior simultaneous deletion of every first/rootmost
    K2 block on a D-to-T cyclic-hull route.  Closure alone would not exclude a
    retained-block -> cut -> K2 frontier.  Separate siblings at one cut remain
    separate territories.
    """
    graph = incidence(cluster)
    retained_blocks = frozenset({("B", ROOT), *(('B', name) for name in pair)})
    k0 = set(path(graph, ("B", ROOT), ("B", pair[0])))
    k0 |= set(path(graph, ("B", ROOT), ("B", pair[1])))
    require({node for node in k0 if node[0] == "B"} == set(retained_blocks),
            "K0 contains a third marked block")
    closure = set(k0)
    for block_node in retained_blocks:
        closure.update(node for node in graph[block_node] if node[0] == "C")
    require(all(node[0] == "C" or node in retained_blocks for node in closure),
            "cut closure retained an unselected block")

    remaining = frozenset(cluster.root_triangles) - frozenset(pair)
    groups: list[tuple[str, ...]] = []
    frontier: list[tuple[int, str]] = []
    for cut_node in sorted((node for node in closure if node[0] == "C"), key=repr):
        for block_node in sorted(graph[cut_node] - closure, key=repr):
            require(block_node[0] == "B" and block_node[1] in remaining,
                    "cut-closed frontier is not c->unselected-T")
            reached = {block_node}
            queue = [block_node]
            while queue:
                current = queue.pop()
                for neighbor in graph[current]:
                    if {current, neighbor} == {cut_node, block_node}:
                        continue
                    if neighbor not in reached:
                        reached.add(neighbor)
                        queue.append(neighbor)
            group = tuple(sorted(node[1] for node in reached
                                 if node[0] == "B" and node[1] in remaining))
            require(group and block_node[1] in group,
                    "off-closure component has no entering unselected triangle")
            groups.append(group)
            frontier.append((int(cut_node[1]), str(block_node[1])))

    flat = [name for group in groups for name in group]
    require(Counter(flat) == Counter(remaining),
            "cut-closed territories are not disjoint/exhaustive")
    require(len(groups) <= len(remaining), "too many cut-closed territories")
    return frozenset(closure), tuple(groups), tuple(frontier)


def destination_labels(bridge_groups: tuple[tuple[str, ...], ...],
                       opened_groups: tuple[tuple[str, ...], ...]) -> frozenset[str]:
    """Destination territories retained after physical root assignment."""
    labels = {"upstream"}
    labels.update("bridge:" + "+".join(group) for group in bridge_groups)
    labels.update("opened:" + "+".join(group) for group in opened_groups)
    require(len(labels) == 1 + len(bridge_groups) + len(opened_groups),
            "destination territory labels collide")
    return frozenset(labels)


def validate_payload_mass(case: ReducedCase,
                          opened_groups: tuple[tuple[str, ...], ...]) -> dict[str, int]:
    """Validate the quotient mass without inventing one physical payload.

    The original-vertex proof assigns each maximal acyclic off-core component
    separately by its unique physical root.  Only after that assignment may
    this quotient forget root locations and internal shapes and retain the
    sum of their orders in each destination territory.
    """
    items = case.payload_mass
    require(len({label for label, unused_mass in items}) == len(items),
            "payload-mass destination is duplicated")
    expected = destination_labels(case.bridge_groups, opened_groups)
    require({label for label, unused_mass in items} == expected,
            "payload-mass destination labels are not exact")
    require(all(type(mass) is int and mass >= 0 for unused_label, mass in items),
            "payload mass is not a nonnegative integer")
    return dict(items)


def derive(case: ReducedCase) -> Certificate:
    require(valid_cluster(case.root_cluster), "root shared-cut cluster is invalid")
    require(case.rootmost_cyclic_route_k2_deleted is True,
            "rootmost cyclic-route K2 deletion was not established before quotienting")
    root = set(case.root_cluster.root_triangles)
    bridged = {name for group in case.bridge_groups for name in group}
    require(root | bridged == set(TRIANGLES) and not (root & bridged),
            "root and first-bridge groups do not partition four triangles")
    require(sum(map(len, case.bridge_groups)) == len(bridged),
            "first-bridge groups overlap")
    require(all(group and tuple(sorted(group)) == group for group in case.bridge_groups),
            "bridge group is empty or noncanonical")
    require(len(set(case.bridge_groups)) == len(case.bridge_groups),
            "duplicate first-hull-bridge group")
    # Nonempty is semantic: a first K2 block of the cyclic hull lies on a
    # D-to-T route, so its away component contains at least one T.  In
    # particular an acyclic attached-tree component (sigma=-1) cannot enter
    # the nonnegative bridge ledger.
    require(all(set(group) <= set(TRIANGLES) and group for group in case.bridge_groups),
            "first-hull-bridge away component has no marked triangle")
    lengths = dict(case.chain_lengths)
    require(len(case.chain_lengths) == len(lengths) == len(case.bridge_groups),
            "bridge-chain witness is duplicated")
    require(set(lengths) == set(case.bridge_groups) and
            all(type(value) is int and value >= 1 for value in lengths.values()),
            "positive integral bridge-chain witness is missing or zero")
    segments = dict(case.segment_lengths)
    require(len(case.segment_lengths) == len(segments) == len(TRIANGLES),
            "triangle segment witness is duplicated")
    require(set(segments) == set(TRIANGLES), "triangle segment data are incomplete")
    require(all(value == (1, 1, 1) for value in segments.values()),
            "an external T is not the actual three-edge triangle C3")

    owners: list[tuple[str, tuple[str, ...]]] = []
    ledger: list[tuple[str, int, bool]] = []
    opened: tuple[tuple[str, ...], ...] = ()
    for group in case.bridge_groups:
        owners.append(("bridge:" + "+".join(group), group))
        # Every group is a complete connected all-triangle cactus territory.
        # The cited triangular-cluster estimate is strict for every rank >= 1;
        # zero is a deliberately weaker floor used by this ledger.
        ledger.append(("bridge:" + "+".join(group), 0, True))

    k = len(root)
    if k == 0:
        owners.append(("anchor:D", (ROOT,)))
        ledger.append(("anchor:D", 1, True))
        channel = "D"
        selected: tuple[str, ...] = ()
    elif k == 1:
        triangle = min(root)
        owners.append(("anchor:D+T", (ROOT, triangle)))
        ledger.append(("anchor:D+T", 2, True))
        channel = "DT"
        selected = (triangle,)
    else:
        pair = select_anchor_pair(case.root_cluster)
        owners.append(("anchor:D+TT", (ROOT, *pair)))
        ledger.append(("anchor:D+TT", 3, True))
        closure, groups, frontier = cut_closed_ownership(case.root_cluster, pair)
        require(all(("C", cut_index) in closure for cut_index, unused_triangle in frontier),
                "a represented boundary cut did not stay upstream")
        require(len(groups) <= k - 2, "too many cut-closed boundary debits")
        for group in groups:
            label = "opened:" + "+".join(group)
            owners.append((label, group))
            # The conservative ledger charges one non-strict tree unit per
            # complete first-boundary group, even if it retains cycles.
            ledger.append((label, -1, False))
        channel = "DTT"
        selected = tuple(pair)
        opened = tuple(sorted(groups))

    # Token labels are derived from, and must exactly equal, the deterministic
    # territory partition.  Values are only aggregate erased-vertex masses;
    # they never become ledger rows.
    validate_payload_mass(case, opened)
    covered = [block for unused_label, blocks in owners for block in blocks]
    require(Counter(covered) == Counter((ROOT, *TRIANGLES)),
            "owner partition is not induced/disjoint/exhaustive at marked-block level")
    value = sum(bound for unused_label, bound, unused_strict in ledger)
    strict = any(strict for unused_label, unused_bound, strict in ledger)
    require(value > 1 or (value == 1 and strict), "R21 complement ledger is not >1")
    return Certificate(channel, selected, opened, tuple(owners), tuple(ledger))


def normalize(case: ReducedCase) -> ReducedCase:
    """Contract only routing-inert witnesses; retain all semantic cells."""
    return replace(
        case,
        chain_lengths=tuple((group, 1) for group in case.bridge_groups),
        # Erase only aggregate sizes.  The exact destination labels survive;
        # no value denotes a physical component or contributes a ledger row.
        payload_mass=tuple((label, 0) for label, unused_mass in case.payload_mass),
        # External T means an actual C3 block.  Segment lengths are therefore
        # not a legal normalization parameter: all three physical lengths stay 1.
        segment_lengths=tuple((name, (1, 1, 1)) for name in TRIANGLES),
    )


def make_case(cluster: Cluster, groups: tuple[tuple[str, ...], ...], *, chain: int = 1,
              payload: int = 0) -> ReducedCase:
    opened: tuple[tuple[str, ...], ...] = ()
    if len(cluster.root_triangles) >= 2:
        pair = select_anchor_pair(cluster)
        unused_closure, opened, unused_frontier = cut_closed_ownership(cluster, pair)
        opened = tuple(sorted(opened))
    labels = destination_labels(groups, opened)
    return ReducedCase(
        root_cluster=cluster,
        bridge_groups=groups,
        chain_lengths=tuple((group, chain) for group in groups),
        rootmost_cyclic_route_k2_deleted=True,
        payload_mass=tuple((label, payload) for label in sorted(labels)),
        segment_lengths=tuple((name, (1, 1, 1)) for name in TRIANGLES),
    )


def enumerate_cases() -> Iterable[ReducedCase]:
    for k in range(5):
        for root_triangles in itertools.combinations(TRIANGLES, k):
            outside = tuple(name for name in TRIANGLES if name not in root_triangles)
            partitions = sorted({canonical_partition(parts) for parts in set_partitions(outside)})
            for raw_cuts in generate_uncolored_clusters(root_triangles):
                for cluster in port_colorings(root_triangles, raw_cuts):
                    for groups in partitions:
                        yield make_case(cluster, groups)


def sample_repeated_cut_case() -> ReducedCase:
    root_triangles = ("T0", "T1")
    outside = (("T2", "T3"),)
    for raw_cuts in generate_uncolored_clusters(root_triangles):
        if len(raw_cuts) != 2:
            continue
        for cluster in port_colorings(root_triangles, raw_cuts):
            return make_case(cluster, outside)
    raise AuditError("no two-cut hostile sample was generated")


def mutation_checks(sample: ReducedCase) -> int:
    baseline = derive(sample)
    checked = 0

    # A positive chain may be shortened, not deleted.  Length zero would merge
    # a bridge-separated group into a shared-cut cluster and can alter dispatch.
    group = sample.bridge_groups[0]
    expect_rejected(lambda: derive(replace(
        sample, chain_lengths=tuple((current, 0 if current == group else length)
                                    for current, length in sample.chain_lengths))),
        "positive bridge chain collapsed to zero")
    checked += 1

    expect_rejected(lambda: derive(replace(
        sample, chain_lengths=sample.chain_lengths + ((group, 2),))),
        "bridge-chain witness duplicated")
    checked += 1

    # Splitting one first-bridge group duplicates/omits its semantic owner.
    expect_rejected(lambda: derive(replace(sample,
        bridge_groups=sample.bridge_groups + (sample.bridge_groups[0],))),
        "connector payload/group duplicated")
    checked += 1

    # A triangle segment length >1 is not a C3 block and cannot be normalized
    # while claiming the D+4T profile.
    segments = dict(sample.segment_lengths)
    segments[TRIANGLES[0]] = (1, 1, 2)
    expect_rejected(lambda: derive(replace(sample,
        segment_lengths=tuple(sorted(segments.items())))),
        "triangle segment subdivided")
    checked += 1

    expect_rejected(lambda: derive(replace(sample,
        segment_lengths=sample.segment_lengths + ((TRIANGLES[0], (1, 1, 1)),))),
        "triangle segment witness duplicated")
    checked += 1

    # Merging two physical cuts reuses a block port; repeated/nested cut data
    # must be retained rather than quotiented away.
    root_two = sample_repeated_cut_case()
    cuts = root_two.root_cluster.cuts
    changed_second = Cut(cuts[1].members,
                         tuple((block, dict(cuts[0].ports).get(block, port))
                               for block, port in cuts[1].ports))
    expect_rejected(lambda: derive(replace(root_two,
        root_cluster=Cluster(root_two.root_cluster.root_triangles,
                             (cuts[0], changed_second)))),
        "distinct cuts merged through one reused physical port")
    checked += 1

    # A block has one incidence at a represented cut.  A second port for that
    # same block at the same cut is malformed even if both ports are in range.
    target_block = cuts[0].ports[0][0]
    used = {port for cut in cuts for block, port in cut.ports if block == target_block}
    extra_port = next(port for port in range(4 if target_block == ROOT else 3)
                      if port not in used)
    duplicate_incidence = Cut(cuts[0].members,
                              cuts[0].ports + ((target_block, extra_port),))
    expect_rejected(lambda: derive(replace(root_two,
        root_cluster=Cluster(root_two.root_cluster.root_triangles,
                             (duplicate_incidence, *cuts[1:])))),
        "one block represented twice at one cut")
    checked += 1

    # Aggregate mass is routing-inert only after every physical component has
    # been separately assigned.  Changing the mass, but not its exact
    # destination label, cannot change dispatch or the ledger.
    enlarged_mass = tuple((label, 17 if label == "upstream" else mass)
                          for label, mass in sample.payload_mass)
    enlarged = replace(sample, payload_mass=enlarged_mass)
    require(derive(enlarged) == baseline,
            "destination payload mass changed dispatch or ledger")
    checked += 1

    # An empty rank-zero component cannot masquerade as a nonnegative
    # first-hull-bridge group; a nonempty acyclic territory has sigma=-1.
    expect_rejected(lambda: derive(replace(sample, bridge_groups=((), *sample.bridge_groups),
        chain_lengths=(((), 1), *sample.chain_lengths))),
        "acyclic away component booked as a hull group")
    checked += 1

    # The payload-mass label set must be exact.  Duplicate, unknown, and
    # missing destinations would respectively double-book, detach, or omit
    # one class of separately rooted physical branches.
    expect_rejected(lambda: derive(replace(sample,
        payload_mass=sample.payload_mass + (("upstream", 1),))),
        "payload-mass destination duplicated")
    checked += 1
    expect_rejected(lambda: derive(replace(sample,
        payload_mass=sample.payload_mass + (("unowned", 1),))),
        "payload mass detached from a destination territory")
    checked += 1
    expect_rejected(lambda: derive(replace(sample,
        payload_mass=sample.payload_mass[1:])),
        "payload-mass destination omitted")
    checked += 1

    # Cut closure alone is insufficient: the reduced state is legal only
    # after the rootmost actual K2 blocks on cyclic routes were removed.
    expect_rejected(lambda: derive(replace(sample,
        rootmost_cyclic_route_k2_deleted=False)),
        "rootmost cyclic-route K2 deletion omitted")
    checked += 1
    return checked


def expect_rejected(action: Callable[[], object], label: str) -> None:
    try:
        action()
    except (AuditError, KeyError, StopIteration):
        return
    raise AuditError(f"hostile mutation accepted: {label}")


def canonical_case_signature(case: ReducedCase) -> str:
    payload = {
        "root_triangles": list(case.root_cluster.root_triangles),
        "cuts": [
            {"members": sorted(cut.members), "ports": [list(item) for item in cut.ports]}
            for cut in case.root_cluster.cuts
        ],
        "bridge_groups": [list(group) for group in case.bridge_groups],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_sources() -> dict[str, object]:
    require(set(SOURCE_PINS) == {"attached-diamond-and-dt", "dtt-note",
            "dtt-semantic-child", "triangular-cactus", "hostile-unicycle",
            "undecorated-selector", "r21-residual-sieve"},
            "semantic source registry changed")
    texts: dict[str, str] = {}
    for name, (relative, expected) in SOURCE_PINS.items():
        path = REPO / relative
        require(path.is_file() and file_sha256(path) == expected,
                f"semantic source changed: {name}")
        texts[name] = path.read_text(encoding="ascii")

    # Pin exact statement and scope, not just bytes.
    packet = texts["attached-diamond-and-dt"]
    require(all(token in packet for token in (
        "Let `J` be a\ndiamond together with `k<=2` triangular blocks in one bridge-free shared-cut\nincidence tree, with arbitrary one-root tree branches",
        "`sigma(J)>r-1`",
        "The scope excludes an acyclic connector meeting several cyclic cores",
        "respectively `>1`, `>2`, and `>3`")),
        "attached D/DT statement or one-root scope changed")
    dtt = texts["dtt-note"]
    require(all(token in dtt for token in (
        "two triangular blocks are joined to `D` by shared cut vertices",
        "one bridge-free block-cut incidence tree",
        "Arbitrary finite rooted trees may be attached at every vertex",
        "sigma(D+T+T)>3.",
        "positive\nbridge connectors are excluded")),
        "DTT statement or scope changed")
    triangular = texts["triangular-cactus"]
    require(all(token in triangular for token in (
        "Every connected triangular block graph $G$ of order $n$ that contains a",
        "s^+(G)>n",
        "bridge blocks",
        "and arbitrary attached trees are allowed")),
        "triangular-cactus statement or tree/bridge scope changed")
    hostile = texts["hostile-unicycle"]
    require(all(token in hostile for token in (
        r"A unicyclic $C_q$ cactus with $q=1\pmod4$ satisfies",
        r"$s^+\geq h-\delta_q$",
        r"$\delta_q=\sec(\pi/q)-1$",
        "The following hold, with arbitrary tree attachments",
        r"$\delta_5=\sec(\pi/5)-1=\sqrt5-2$",
        r"$s^+(U_5)\geq u-\delta_5$")),
        "hostile C5 inequality, exact delta_5 arithmetic, or tree scope changed")
    residual = texts["r21-residual-sieve"]
    require(all(token in residual for token in (
        "`sigma(C5)=2-sqrt(5)<0`",
        "Here `epsilon(C3)=1`, `epsilon(C5)=5-2sqrt(5)`",
        "`R21: Theta(1,2,r)+T^5`; and `D+T^4+P`")),
        "R21 symbolic residual row or its separate C5 arithmetic changed")
    # Crucial trust boundary: the residual text contains the symbolic P row
    # and separate C5 formulas, but does NOT identify that P occurrence as C5.
    # A prior physical typed-row certificate P=C5 is required externally.
    # Given that certificate, the hostile source supplies
    # delta_5=sec(pi/5)-1=sqrt(5)-2; 0<delta_5<1 follows exactly from
    # 2^2<5<3^2, checked without floating point here.
    require(2 * 2 < 5 < 3 * 3, "exact delta_5 radical bracket failed")

    child_path = REPO / SOURCE_PINS["dtt-semantic-child"][0]
    child_outputs = []
    for optimized in (False, True):
        command = [sys.executable] + (["-O"] if optimized else []) + [str(child_path),
                                                                            "--optimized-child"]
        completed = subprocess.run(command, capture_output=True, check=False)
        require(completed.returncode == 0 and completed.stderr == b"",
                f"DTT semantic child failed/{optimized}")
        require(hashlib.sha256(completed.stdout).hexdigest() == DTT_CHILD_OUTPUT_SHA256,
                f"DTT semantic child output changed/{optimized}")
        child_outputs.append(completed.stdout)
    require(child_outputs[0] == child_outputs[1], "DTT child mode outputs differ")
    child_text = child_outputs[0].decode("ascii")
    require(all(token in child_text for token in (
        "scope exclusions: one-root tree attachments only; no multi-interface acyclic connectors; no positive-rank connector blocks; no D+T^3",
        "uniform packet bound: sigma(D+TT)=3+Delta/2>3")),
        "DTT child semantic receipt changed")

    selector_path = REPO / SOURCE_PINS["undecorated-selector"][0]
    selector_outputs = []
    for optimized in (False, True):
        command = [sys.executable] + (["-O"] if optimized else []) + [str(selector_path),
                                                                            "--optimized-child"]
        completed = subprocess.run(command, capture_output=True, check=False)
        require(completed.returncode == 0 and completed.stderr == b"",
                f"307-state selector failed/{optimized}")
        require(hashlib.sha256(completed.stdout).hexdigest() == SELECTOR_OUTPUT_SHA256,
                f"307-state selector output changed/{optimized}")
        selector_outputs.append(completed.stdout)
    require(selector_outputs[0] == selector_outputs[1], "selector mode outputs differ")
    selector = json.loads(selector_outputs[0])
    require(selector["audit"]["labelled_states"] == 307 and
            selector["audit"]["residual_states"] == 0,
            "undecorated selector census changed")
    return {
        "exact_source_sha256": {name: digest for name, (unused_path, digest) in SOURCE_PINS.items()},
        "semantic_children_replayed_normal_and_O": ["dtt-semantic-child", "undecorated-selector"],
        "statement_text_receipts_only": ["attached-diamond-and-dt", "dtt-note",
                                         "triangular-cactus", "hostile-unicycle",
                                         "r21-residual-sieve"],
        "undecorated_selector_states": 307,
        "hostile_c5_text_receipt": (
            "delta_5=sec(pi/5)-1=sqrt(5)-2 and sigma(P)>=-delta_5; "
            "2^2<5<3^2 proves 0<delta_5<1"),
        "typed_row_scope": (
            "the residual source exposes symbolic D+T^4+P and separate C5 "
            "formulas only; it does not prove that this P is physical C5"),
    }


def audit_no_asserts() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            "verifier must not rely on Python assertions")


def run() -> dict[str, object]:
    audit_no_asserts()
    source_receipt = audit_sources()
    cases = 0
    by_k: Counter[int] = Counter()
    channels: Counter[str] = Counter()
    abstract_incidence_trees_by_k: dict[int, int] = {}
    realizable_uncolored_skeletons_by_k: dict[int, int] = {}
    port_colored_clusters_by_k: dict[int, int] = {}
    for k in range(5):
        root_triangles = TRIANGLES[:k]
        incidence_trees = generate_uncolored_clusters(root_triangles)
        abstract_incidence_trees_by_k[k] = len(incidence_trees)
        realizable = tuple(
            cuts for cuts in incidence_trees
            if next(iter(port_colorings(root_triangles, cuts)), None) is not None)
        realizable_uncolored_skeletons_by_k[k] = len(realizable)
        port_colored_clusters_by_k[k] = sum(
            1 for raw_cuts in realizable
            for unused_cluster in port_colorings(root_triangles, raw_cuts))
    require(abstract_incidence_trees_by_k == {0: 1, 1: 1, 2: 4, 3: 29, 4: 311},
            "abstract shared-cut incidence-tree census changed")
    require(realizable_uncolored_skeletons_by_k ==
            {0: 1, 1: 1, 2: 4, 3: 29, 4: 307},
            "port-realizable uncolored shared-cut skeleton census changed")
    signatures = set()
    sample_with_bridge = None
    for case in enumerate_cases():
        certificate = derive(case)
        normalized = normalize(case)
        require(derive(normalized) == certificate,
                "contractible witness changed derived dispatch or credit ledger")
        cases += 1
        by_k[len(case.root_cluster.root_triangles)] += 1
        channels[certificate.channel] += 1
        signatures.add(canonical_case_signature(case))
        if sample_with_bridge is None and case.bridge_groups:
            sample_with_bridge = case
    require(sample_with_bridge is not None, "census lacks a positive bridge group")
    rejected = mutation_checks(sample_with_bridge)
    digest = hashlib.sha256("\n".join(sorted(signatures)).encode()).hexdigest()
    by_k_dict = dict(sorted(by_k.items()))
    channels_dict = dict(sorted(channels.items()))
    require(cases == EXPECTED_CASES, "decorated quotient census changed")
    require(by_k_dict == EXPECTED_CASES_BY_K,
            "decorated quotient count by root-triangle count changed")
    require(port_colored_clusters_by_k == EXPECTED_PORT_COLORED_BY_K,
            "port-coloured root-cluster census changed")
    require(len(signatures) == cases,
            "canonical signature rows are not one-to-one with decorated states")
    require(digest == EXPECTED_CANONICAL_SHA256,
            "decorated quotient canonical digest changed")
    require(channels_dict == EXPECTED_CHANNELS, "derived channel counts changed")
    return {
        "status": "NONPROMOTIONAL ABSTRACT COMBINATORIAL AUDIT",
        "labelled_decorated_quotient_states": cases,
        "cases_by_root_triangle_count": by_k_dict,
        "abstract_uncolored_incidence_trees_by_k": abstract_incidence_trees_by_k,
        "port_realizable_uncolored_skeletons_by_k": realizable_uncolored_skeletons_by_k,
        "port_colored_root_clusters_by_k": port_colored_clusters_by_k,
        "derived_channels": channels_dict,
        "hostile_mutations_checked": rejected,
        "semantic_source_receipt": source_receipt,
        "bridge_group_semantics": "simultaneous first/rootmost actual K2 bridges of the D-rooted cyclic hull only; every complete away group contains >=1 T",
        "cut_closure_semantics": "least-depth DTT K0; AFTER rootmost cyclic-route K2 deletion, S adjoins every cut incident with retained D/T; each cyclic downstream component is separate c->unselected-T minus c",
        "rank_zero_payload_semantics": "each physical acyclic component is first assigned by its unique root; verifier retains only aggregate payload_mass for exact destination labels upstream/opened/bridge and normalizes sizes to zero",
        "canonical_signature_sha256": digest,
        "decorated_quotient_scope": "labelled triangle choices + labelled root-cluster cut incidences + injective physical block ports + Bell partition of away triangle sets; not physical graphs/isomorphism classes and does not record internal bridge branching",
        "required_prior_physical_typed_row_certificate": (
            "REQUIRED BUT NOT PROVED HERE: an external physical certificate "
            "identifies the isolated R21 row's symbolic P as the actual C5 "
            "unicycle (with its one-root tree attachments)"),
        "trust_boundary": "conditional marked-block combinatorial transport for narrow R21:P D+4T only; this artifact does not prove P=C5 typing; original-vertex induced/disjoint/exhaustive ownership is proved in prose, not adjacency-enumerated here; hashes/token checks authenticate statement text only, and only named executable children are replayed; no generic bridge or rank-seven closure",
        "spectral_dependencies_not_reproved": [
            "attached D with one-root tree branches: sigma>1",
            "bridge-free shared-cut D+T with one-root tree branches: sigma>2",
            "bridge-free shared-cut D+T+T direct/direct or direct/nested with one-root tree branches: sigma>3",
            "connected all-triangle cactus of every positive rank with arbitrary bridge blocks and attached trees: sigma>0",
            "P=C5 with sigma(P)>=-delta_5>-1 (hostile pentagon with arbitrary tree attachments; delta_5=sec(pi/5)-1=sqrt(5)-2 and 0<delta_5<1)"
        ],
    }


def serialized_report() -> str:
    return json.dumps(run(), sort_keys=True, indent=2) + "\n"


def main() -> int:
    output = serialized_report()
    if not sys.flags.optimize and "--optimized-child" not in sys.argv:
        child = subprocess.run([sys.executable, "-O", str(Path(__file__).resolve()),
                                "--optimized-child"], check=False,
                               capture_output=True, text=True)
        require(child.returncode == 0, "optimized audit failed")
        require(child.stderr == "", "optimized audit wrote stderr")
        require(child.stdout == output, "normal and optimized audit outputs differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
