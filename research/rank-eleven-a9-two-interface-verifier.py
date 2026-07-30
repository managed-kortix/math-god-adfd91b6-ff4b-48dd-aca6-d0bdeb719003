#!/usr/bin/env python3
"""Fail-closed theorem-aware verifier for the rank-eleven P | A_9 | P endpoint.

The program independently enumerates the marked incidence rows, searches only
realized triangle-router refinements, resolves every mark through the complete
refinement tree, and derives each ledger from the theorem whitelist below.  An
unknown packet profile is an error, never a retained triangular credit.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank_nine_two_interface_base", HERE / "nonacyclic-t7-two-interface-census.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("two-interface dependency has no import loader")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)

CORE_SPEC = spec_from_file_location(
    "geometry_router_owner_core", HERE / "geometry_router_owner_core.py"
)
CORE = module_from_spec(CORE_SPEC)
if CORE_SPEC.loader is None:
    raise RuntimeError("router-owner core has no import loader")
sys.modules[CORE_SPEC.name] = CORE
CORE_SPEC.loader.exec_module(CORE)

TRIANGLES = frozenset(range(9))
PENTAGONS = ("PA", "PB")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(records):
    return sha256(("\n".join(records) + "\n").encode("ascii")).hexdigest()


def enumerate_rows():
    """Generate all rows without importing another rank-nine row census."""
    classes = BASE.BASE.enumerate_colors(("T",) * 9, 0)
    signatures = tuple(signature for signature, _ in classes)
    require(signatures == tuple(sorted(signatures)), "incidence classes are not sorted")
    require(len(signatures) == len(set(signatures)), "duplicate incidence class")
    rows = {}
    placements = 0
    for incidence_signature, tree in classes:
        require(incidence_signature == BASE.BASE.signature(tree), "noncanonical incidence tree")
        positions = BASE.position_universe(tree)
        placements += len(positions) ** 2
        local = {}
        for first in positions:
            for second in positions:
                pair = (first, second)
                signature = BASE.marked_signature(tree, pair)
                if signature not in local:
                    local[signature] = (pair, 0)
                representative, multiplicity = local[signature]
                local[signature] = (representative, multiplicity + 1)
        for signature, (positions, multiplicity) in local.items():
            require(signature not in rows, "marked signature crosses incidence classes")
            rows[signature] = BASE.Row(
                signature, incidence_signature, tree, positions, multiplicity
            )
    return tuple(rows[key] for key in sorted(rows)), classes, placements


@dataclass(frozen=True)
class Bound:
    credit: Fraction
    deficits: int
    strict: bool

    def __add__(self, other):
        return Bound(
            self.credit + other.credit,
            self.deficits + other.deficits,
            self.strict or other.strict,
        )

    def positive(self):
        """Check credit-deficits*(sqrt(5)-2)>0 without floating point."""
        shifted = self.credit + 2 * self.deficits
        if shifted < 0:
            return False
        square = shifted * shifted - 5 * self.deficits * self.deficits
        return square > 0 or square == 0 and self.strict


ZERO = Bound(Fraction(0), 0, False)


@dataclass(frozen=True)
class Packet:
    name: str
    cycles: tuple[int, ...]
    demands: tuple[str, ...]
    theorem: str
    hypothesis: str
    bound: Bound


@dataclass(frozen=True)
class Split:
    router: int
    active: tuple[int, ...]
    interval_sizes: tuple[int, ...]
    owners: tuple[tuple[object, tuple[int, ...]], ...]


@dataclass(frozen=True)
class Plan:
    packets: tuple[Packet, ...]
    routers: tuple[int, ...]
    splits: tuple[Split, ...]

    @property
    def bound(self):
        answer = ZERO
        for packet in self.packets:
            answer += packet.bound
        return answer


@dataclass(frozen=True)
class Repair:
    code: str
    operation: str
    router: int | None
    interval_sizes: tuple[int, ...]
    interval_positions: tuple[tuple[object, ...], ...]
    interval_owners: tuple[str, ...]
    packets: tuple[Packet, ...]
    connector_owners: tuple[str, str]
    cut_owners: tuple[tuple[int, str], ...]
    opening: object | None
    bound: Bound


@dataclass(frozen=True)
class PentagonOpening:
    label: str
    vertices: tuple[str, ...]
    cyclic_edges: tuple[tuple[str, str], ...]
    connector_vertex: str
    vertex_owners: tuple[tuple[str, str], ...]
    attachment_owners: tuple[tuple[str, str], ...]
    retained_owner: str
    opening_owner: str
    cost: int


def pairwise_intersecting(tree, cycles):
    adjacency = BASE.BASE.adjacency(tree)
    return all(
        set(adjacency[first]) & set(adjacency[second])
        for index, first in enumerate(cycles)
        for second in cycles[index + 1 :]
    )


def common_cut(tree, cycles):
    adjacency = BASE.BASE.adjacency(tree)
    common = set(adjacency[cycles[0]])
    for cycle in cycles[1:]:
        common &= set(adjacency[cycle])
    return min(common) if common else None


def connected_cycles(tree, cycles):
    cycles = set(cycles)
    if not cycles:
        return True
    adjacency = BASE.BASE.adjacency(tree)
    seen = {min(cycles)}
    stack = list(seen)
    while stack:
        cycle = stack.pop()
        for cut in adjacency[cycle]:
            for neighbor in adjacency[cut]:
                if neighbor in cycles and neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return seen == cycles


def local_triangle_positions(tree, router):
    adjacency = BASE.BASE.adjacency(tree)
    positions = [BASE.Position("cut", cut) for cut in adjacency[router]]
    positions.extend(
        BASE.Position("private", router, slot)
        for slot in range(3 - len(adjacency[router]))
    )
    require(len(positions) == 3, "router does not have three concrete triangle vertices")
    return tuple(positions)


def local_triangle_geometry(tree, router):
    return CORE.make_cycle(f"T{router}", local_triangle_positions(tree, router))


def concrete_split(tree, router, active, owner_anchors):
    """Bind each owner to actual vertices of the router triangle."""
    local = local_triangle_positions(tree, router)
    anchors = []
    for anchor, cycles in owner_anchors:
        positions = anchor if isinstance(anchor, tuple) else (anchor,)
        anchors.append((tuple(positions), tuple(cycles)))
    require(len(anchors) in (2, 3), "split must have two or three owners")
    used = {position for positions, _ in anchors for position in positions}
    require(len(used) == sum(len(positions) for positions, _ in anchors),
            "split anchor belongs to two owners")
    require(used <= set(local), "split anchor is not a concrete router vertex")
    missing = tuple(position for position in local if position not in used)
    if len(anchors) == 2:
        require(sum(map(len, (positions for positions, _ in anchors))) in (2, 3),
                "binary split has invalid concrete anchor count")
        if missing:
            first_positions, first_cycles = anchors[0]
            anchors[0] = (first_positions + missing, first_cycles)
    else:
        require(not missing, "three-way split omits a router vertex")
    sizes = tuple(len(positions) for positions, _ in anchors)
    return Split(router, tuple(sorted(active)), sizes, tuple(anchors))


def terminal_packet(tree, cycles, demands, name="K"):
    """Apply exactly one proved theorem, selected from a closed whitelist."""
    cycles = tuple(sorted(cycles))
    demands = tuple(sorted(demands))
    require(cycles or demands, "empty terminal packet")
    require(connected_cycles(tree, cycles), "terminal triangular carrier is disconnected")
    require(set(demands) <= set(PENTAGONS), "unknown hostile demand")
    require(len(demands) == len(set(demands)), "demand appears twice in one packet")
    t, p = len(cycles), len(demands)
    rank = t + p
    if p == 0:
        require(t > 0, "empty pure packet")
        return Packet(name, cycles, demands, "pure-triangular-strict",
                      "nonempty connected triangular cactus", Bound(Fraction(0), 0, True))
    if t == 0 and p == 1:
        return Packet(name, cycles, demands, "P-deficit",
                      "one complete pentagon packet", Bound(Fraction(0), 1, False))
    if t == 0 and p == 2:
        return Packet(name, cycles, demands, "PP-nonnegative",
                      "complete connected two-pentagon profile", ZERO)
    if t == 1 and p == 1:
        return Packet(name, cycles, demands, "TP-quantitative",
                      "complete connected TP profile", Bound(Fraction(1), 1, True))
    if t == 1 and p == 2:
        return Packet(name, cycles, demands, "TPP-strict",
                      "complete connected TPP profile", Bound(Fraction(3, 2), 0, True))
    if p == 1 and pairwise_intersecting(tree, cycles):
        hub = common_cut(tree, cycles)
        theorem = "one-hostile-common-cut" if hub is not None else "one-hostile-packing-one"
        hypothesis = (f"all retained triangles contain cut {hub}" if hub is not None
                      else "every pair of retained triangles intersects")
        return Packet(name, cycles, demands, theorem, hypothesis,
                      Bound(Fraction(t), 1, True))
    if 2 <= rank <= 3:
        return Packet(name, cycles, demands, "connected-rank-2/3-nonnegative",
                      f"complete connected cyclic rank {rank}", ZERO)
    if 4 <= rank <= 10:
        return Packet(name, cycles, demands, "connected-rank-4..10-strict",
                      f"complete connected cyclic rank {rank}", Bound(Fraction(0), 0, True))
    raise RuntimeError(f"unproved terminal profile T^{t}P^{p}")


def labels_at(row, positions):
    answer = {}
    for label, position in zip(PENTAGONS, row.positions):
        if position in positions:
            answer.setdefault(position, []).append(label)
    return answer


def standard_plans(row):
    """Enumerate standard recursive router plans and proved terminal packets."""
    tree = row.tree
    adjacency = BASE.BASE.adjacency(tree)

    @lru_cache(maxsize=None)
    def solve(active, active_positions):
        active = frozenset(active)
        active_positions = tuple(active_positions)
        demands = tuple(
            label for label, position in zip(PENTAGONS, row.positions)
            if position in active_positions
        )
        candidates = []
        try:
            candidates.append(Plan((terminal_packet(tree, active, demands),), (), ()))
        except RuntimeError:
            pass

        marks = labels_at(row, active_positions)
        for router in sorted(active):
            branches = BASE.component_cycle_sets(tree, active, router)
            owners = []
            child_arguments = []
            loose_packets = []
            for cut, branch in branches:
                position = BASE.Position("cut", cut)
                branch_positions = tuple(
                    site for site in active_positions
                    if (site.kind == "private" and site.vertex in branch)
                    or (site.kind == "cut" and set(adjacency[site.vertex]) & set(branch))
                )
                if branch:
                    owners.append((position, tuple(sorted(branch))))
                    child_arguments.append((branch, branch_positions))
                elif position in marks:
                    owners.append((position, ()))
                    loose_packets.append((position, tuple(marks[position])))
            for position in sorted(marks):
                if position.kind == "private" and position.vertex == router:
                    owners.append((position, ()))
                    loose_packets.append((position, tuple(marks[position])))
            if not 2 <= len(owners) <= 3 or not child_arguments:
                continue
            split = concrete_split(tree, router, active, owners)
            children_by_branch = [solve(frozenset(branch), positions)
                                  for branch, positions in child_arguments]
            if any(not children for children in children_by_branch):
                continue
            products_so_far = [Plan((), (), ())]
            for child_options in children_by_branch:
                products_so_far = [
                    Plan(left.packets + right.packets,
                         left.routers + right.routers,
                         left.splits + right.splits)
                    for left in products_so_far for right in child_options
                ]
            for _, labels in loose_packets:
                packet = terminal_packet(tree, (), labels, f"P{router}")
                products_so_far = [
                    Plan(item.packets + (packet,), item.routers, item.splits)
                    for item in products_so_far
                ]
            for child_product in products_so_far:
                candidates.append(Plan(
                    child_product.packets,
                    (router,) + child_product.routers,
                    (split,) + child_product.splits,
                ))

        # A complete-profile two-port coalescence owns both hostile branches as
        # PP and sends every triangular branch through the third router port.
        for router in sorted(active):
            branch_records = BASE.component_cycle_sets(tree, active, router)
            hostile_ports = []
            triangular = set()
            triangular_positions = []
            triangular_anchors = []
            valid = True
            for cut, branch in branch_records:
                position = BASE.Position("cut", cut)
                port_labels = list(marks.get(position, ()))
                branch_positions = [
                    site for site in active_positions
                    if (site.kind == "private" and site.vertex in branch)
                    or (site.kind == "cut" and set(adjacency[site.vertex]) & set(branch))
                ]
                branch_labels = [label for label, site in zip(PENTAGONS, row.positions)
                                 if site in branch_positions]
                port_labels.extend(branch_labels)
                if port_labels:
                    if branch or len(port_labels) != 1:
                        valid = False
                    hostile_ports.append((position, tuple(port_labels)))
                else:
                    triangular.update(branch)
                    triangular_positions.extend(branch_positions)
                    if branch:
                        triangular_anchors.append(position)
            for position in sorted(marks):
                if position.kind == "private" and position.vertex == router:
                    labels = tuple(marks[position])
                    if len(labels) != 1:
                        valid = False
                    hostile_ports.append((position, labels))
            if not valid or len(hostile_ports) != 2 or set().union(
                    *(set(labels) for _, labels in hostile_ports)) != set(PENTAGONS):
                continue
            if not triangular or len(triangular_anchors) != 1:
                continue
            child_options = solve(frozenset(triangular), tuple(dict.fromkeys(triangular_positions)))
            for child in child_options:
                pp = terminal_packet(tree, (), PENTAGONS, f"PP{router}")
                owners = (
                    (tuple(position for position, _ in hostile_ports), ()),
                    (triangular_anchors[0], tuple(sorted(triangular))),
                )
                split = concrete_split(tree, router, active, owners)
                candidates.append(Plan((pp,) + child.packets, (router,) + child.routers,
                                       (split,) + child.splits))

        # Keep one deterministic representative per theorem ledger and packet
        # profile. This bounds the exhaustive dynamic program without deciding
        # acceptance heuristically.
        unique = {}
        for candidate in candidates:
            key = (
                candidate.bound,
                tuple((packet.cycles, packet.demands, packet.theorem)
                      for packet in candidate.packets),
            )
            old = unique.get(key)
            if old is None or (len(candidate.routers), repr(candidate)) < (
                    len(old.routers), repr(old)):
                unique[key] = candidate
        return tuple(unique.values())

    return solve(TRIANGLES, row.positions)


def choose_plan(row):
    if expected_residual(row):
        return None
    plans = standard_plans(row)
    proved = [plan for plan in plans if plan.bound.positive()]
    if proved:
        return min(proved, key=lambda plan: (len(plan.routers), repr(plan)))
    return two_arm_common_hub_plan(row)


def two_arm_common_hub_plan(row):
    """Materialize the fifteen nested two-arm plans omitted by standard search.

    At each marked router, its private connector port and outer cut are the
    consecutive size-two interval. The hub port is the singleton interval.
    Thus the first split retains the second router in the hub child, and the
    second split is a genuine recursive refinement of that current child.
    """
    adjacency = BASE.BASE.adjacency(row.tree)
    cuts = tuple(range(9, len(adjacency)))
    if len(cuts) != 3 or any(position.kind != "private" for position in row.positions):
        return None
    marked_routers = tuple(position.vertex for position in row.positions)
    if len(set(marked_routers)) != 2 or any(len(adjacency[router]) != 2 for router in marked_routers):
        return None
    common = set(adjacency[marked_routers[0]]) & set(adjacency[marked_routers[1]])
    if len(common) != 1:
        return None
    hub = next(iter(common))
    if len(adjacency[hub]) < 2:
        return None
    outer_cuts = tuple(
        next(cut for cut in adjacency[router] if cut != hub)
        for router in marked_routers
    )
    if any(not (set(adjacency[cut]) - set(marked_routers)) for cut in outer_cuts):
        return None
    first_outer_cycles = set(adjacency[outer_cuts[0]]) - {marked_routers[0]}
    second_outer_cycles = set(adjacency[outer_cuts[1]]) - {marked_routers[1]}
    if marked_routers[1] in first_outer_cycles or marked_routers[0] in second_outer_cycles:
        return None

    active = set(TRIANGLES)
    splits = []
    packets = []
    for label, position in zip(PENTAGONS, row.positions):
        router = position.vertex
        require(router in active, "two-arm router was removed before its recursive split")
        outer_cut = next(cut for cut in adjacency[router] if cut != hub)
        branches = dict(BASE.component_cycle_sets(row.tree, frozenset(active), router))
        arm = set(branches[outer_cut])
        hub_child = set(branches[hub])
        require(arm and hub_child, "two-arm split has an empty cyclic side")
        require(arm | hub_child == active - {router} and arm.isdisjoint(hub_child),
                "two-arm split branches are not exact")
        splits.append(concrete_split(
            row.tree, router, active,
            (((position, BASE.Position("cut", outer_cut)), tuple(sorted(arm))),
             (BASE.Position("cut", hub), tuple(sorted(hub_child)))),
        ))
        packets.append(terminal_packet(row.tree, arm, (label,), f"arm-{label}"))
        active = hub_child

    require(active, "two-arm plan has no retained common-hub core")
    packets.append(terminal_packet(row.tree, active, (), "hub-core"))
    plan = Plan(tuple(packets), marked_routers, tuple(splits))
    require(plan.bound.positive(), "two-arm theorem ledger is not positive")
    return plan


def verify_plan(row, plan, submitted_position_owners=None):
    adjacency = BASE.BASE.adjacency(row.tree)
    for packet in plan.packets:
        derived = terminal_packet(row.tree, packet.cycles, packet.demands, packet.name)
        require(packet == derived,
                "terminal packet theorem/hypothesis/bound was not independently derived")
    removed = set(plan.routers)
    require(len(removed) == len(plan.routers), "router repeated")
    retained = [cycle for packet in plan.packets for cycle in packet.cycles]
    require(Counter(retained) == Counter(TRIANGLES - removed),
            "final packets do not own exactly the retained triangles")
    demands = [demand for packet in plan.packets for demand in packet.demands]
    require(Counter(demands) == Counter(PENTAGONS), "pentagon demands not assigned exactly once")
    for split in plan.splits:
        require(split.router in split.active, "inactive router")
        require(len(split.interval_sizes) == len(split.owners), "interval/owner count mismatch")
        require(split.interval_sizes == tuple(len(positions) for positions, _ in split.owners),
                "ordered interval sizes do not match concrete vertex owners")
        require(sum(split.interval_sizes) == 3, "router intervals do not cover triangle")
        require(sorted(split.interval_sizes) in ([1, 2], [1, 1, 1]), "improper intervals")
        geometry = local_triangle_geometry(row.tree, split.router)
        local = geometry.vertices
        CORE.verify_router_owner_split(
            geometry,
            tuple(positions for positions, _ in split.owners),
            tuple(range(len(split.owners))),
            split.interval_sizes,
        )
        branches = [set(cycles) for _, cycles in split.owners]
        require(sum(map(len, branches)) == len(set().union(*branches)), "split branches overlap")
        require(set().union(*branches) == set(split.active) - {split.router},
                "split branches do not exhaust active non-router cycles")
        for positions, _ in split.owners:
            require(positions, "owner has no concrete interval marks")
            for position in positions:
                if position.kind == "cut":
                    require(position.vertex in adjacency[split.router], "nonincident cut owner")
                else:
                    require(position.vertex == split.router, "private owner on another router")
    split_by_active = {frozenset(split.active): split for split in plan.splits}
    require(len(split_by_active) == len(plan.splits), "two splits refine the same active territory")
    root = frozenset(TRIANGLES)
    child_active_sets = [
        frozenset(cycles)
        for split in plan.splits
        for _, cycles in split.owners
        if cycles
    ]
    for active in split_by_active:
        if active == root:
            continue
        require(child_active_sets.count(active) == 1,
                "recursive split is not the unique active child of its parent")
    terminals = {frozenset(packet.cycles): index for index, packet in enumerate(plan.packets)
                 if packet.cycles}

    def child_adhesion(positions, child):
        candidates = [
            position for position in positions
            if position.kind == "cut" and set(adjacency[position.vertex]) & set(child)
        ]
        require(len(candidates) == 1,
                "router child does not have one concrete adhesion position")
        return candidates[0]

    def resolve(active, site):
        if active in terminals:
            return terminals[active]
        require(active in split_by_active, "recursive owner reaches no final packet")
        split = split_by_active[active]
        matches = []
        for positions, cycles in split.owners:
            if site in positions:
                matches.append((positions, frozenset(cycles), True))
            elif site.kind == "private" and site.vertex in cycles:
                matches.append((positions, frozenset(cycles), False))
            elif site.kind == "cut" and set(adjacency[site.vertex]) & set(cycles):
                matches.append((positions, frozenset(cycles), False))
        require(len(matches) == 1, "recursive adhesion does not select one child")
        positions, child, explicit = matches[0]
        if not child:
            labels = [label for label, position in zip(PENTAGONS, row.positions)
                      if position in positions]
            owners = [index for index, packet in enumerate(plan.packets)
                      if set(labels) & set(packet.demands) and not packet.cycles]
            require(len(set(owners)) == 1, "hostile-only interval has no unique final owner")
            return owners[0]
        # Preserve a site while it merely lies inside an ancestral branch. Once
        # it is an explicit vertex of the current router interval, continue
        # through that child's unique cut adhesion. This binds private
        # parent-router positions without pretending they are descendant sites.
        next_site = child_adhesion(positions, child) if explicit else site
        return resolve(child, next_site)

    interval_owner_records = []
    for split in plan.splits:
        for positions, cycles in split.owners:
            root_owners = {resolve(root, position) for position in positions}
            require(len(root_owners) == 1,
                    "concrete router interval positions have different root owners")
            root_owner = next(iter(root_owners))
            if cycles:
                child_owner = resolve(
                    frozenset(cycles), child_adhesion(positions, frozenset(cycles))
                )
                require(root_owner == child_owner,
                        "router interval child owner disagrees with root owner: "
                        f"router={split.router} active={split.active} positions={positions} "
                        f"cycles={cycles} root={root_owner} child={child_owner}")
            for position in positions:
                interval_owner_records.append((position, root_owner))
    cycle_owner = {
        cycle: index for index, packet in enumerate(plan.packets) for cycle in packet.cycles
    }
    cut_owner_records = []
    for cut in range(9, len(adjacency)):
        position = BASE.Position("cut", cut)
        resolved_owner = resolve(root, position)
        cut_owner_records.append((position, resolved_owner))
        owners = {cycle_owner[cycle] for cycle in adjacency[cut] if cycle in cycle_owner}
        require(len(owners) <= 1, "retained cut has competing final owners")
        if owners:
            require(resolved_owner in owners,
                    "recursive cut owner disagrees with final packet")
    for label, position in zip(PENTAGONS, row.positions):
        packet = next(index for index, item in enumerate(plan.packets) if label in item.demands)
        require(resolve(root, position) == packet,
                "connector mark does not recursively reach its declared packet")
    expected_positions = tuple(
        [BASE.Position("cut", cut) for cut in range(9, len(adjacency))]
        + [position for router in plan.routers
           for position in local_triangle_positions(row.tree, router)
           if position.kind == "private"]
    )
    require(len(expected_positions) == len(set(expected_positions)),
            "independently derived final-position domain has duplicate keys")
    derived_records = tuple(cut_owner_records + interval_owner_records)
    derived_map = {}
    for position, owner in derived_records:
        old = derived_map.setdefault(position, owner)
        require(old == owner, "final position receives competing terminal owners")
    require(set(derived_map) == set(expected_positions),
            "final position/cut owner map has an inexact domain")
    canonical_records = tuple((position, derived_map[position])
                              for position in sorted(expected_positions))
    if submitted_position_owners is not None:
        submitted = CORE.exact_owner_map(
            submitted_position_owners, expected_positions,
            "submitted final position/cut owners",
        )
        require(submitted == derived_map,
                "submitted final position/cut owners differ from recursive resolution")
    require(plan.bound.positive(), "theorem ledger is not positive")
    return canonical_records


def plan_text(row, plan, position_owners):
    packets = ";".join(
        f"{packet.cycles}:{','.join(packet.demands)}:{packet.theorem}:"
        f"{packet.bound.credit},{packet.bound.deficits},{int(packet.bound.strict)}"
        for packet in plan.packets
    )
    splits = ";".join(
        f"T{step.router}@{step.active}:{step.interval_sizes}:{step.owners}"
        for step in plan.splits
    )
    owners = ";".join(
        f"{position.text()}={owner}" for position, owner in position_owners
    )
    return f"{row.signature}|{packets}|{splits}|final-positions={owners}"


def repair_text(row, repair):
    packets = ";".join(
        f"{packet.name}:{packet.cycles}:{packet.demands}:{packet.theorem}:"
        f"{packet.hypothesis}:{packet.bound.credit},{packet.bound.deficits},"
        f"{int(packet.bound.strict)}"
        for packet in repair.packets
    )
    return "|".join((
        row.signature, repair.code, repair.operation, f"router={repair.router}",
        f"intervals={repair.interval_sizes}", f"interval-owners={repair.interval_owners}",
        f"packets={packets}", f"connectors={repair.connector_owners}",
        f"cuts={repair.cut_owners}", f"opening={repair.opening}",
        f"bound={repair.bound.credit},{repair.bound.deficits},{int(repair.bound.strict)}",
    ))


def expect_rejected(action, label):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError(f"mutation self-test was accepted: {label}")


def mutation_self_tests(plan_rows, repairs, repair_rows):
    tests = 0
    row, plan = next((row, plan) for row, plan, _ in plan_rows if plan.packets)
    bad_packet = replace(plan.packets[0], bound=Bound(Fraction(999), 0, True))
    expect_rejected(
        lambda: verify_plan(row, replace(plan, packets=(bad_packet,) + plan.packets[1:])),
        "ordinary packet bound",
    )
    tests += 1

    row, plan, owners = next((row, plan, owners) for row, plan, owners in plan_rows
                             if owners)
    position, owner = owners[0]
    bad_owners = ((position, owner), (position, owner)) + owners[1:]
    expect_rejected(lambda: verify_plan(row, plan, bad_owners),
                    "duplicate final position owner key")
    tests += 1

    packet_count = len(plan.packets)
    forged = (owner + 1) % packet_count if packet_count > 1 else owner + 1
    bad_owners = ((position, forged),) + owners[1:]
    expect_rejected(lambda: verify_plan(row, plan, bad_owners),
                    "forged final position owner")
    tests += 1

    ambiguity_fixture = next(
        ((row, plan, index, owner_index, position)
         for row, plan, _ in plan_rows
         for index, split in enumerate(plan.splits)
         for owner_index, (positions, cycles) in enumerate(split.owners)
         if cycles
         for position in positions
         if position.kind == "cut"),
        None,
    )
    require(ambiguity_fixture is not None, "shared-cut interval ambiguity fixture is absent")
    row, plan, split_index, owner_index, position = ambiguity_fixture
    split = plan.splits[split_index]
    target_index = next(index for index in range(len(split.owners)) if index != owner_index)
    target_positions, target_cycles = split.owners[target_index]
    bad_target = (target_positions + (position,), target_cycles)
    bad_owners = split.owners[:target_index] + (bad_target,) + split.owners[target_index + 1:]
    bad_split = replace(split, owners=bad_owners,
                        interval_sizes=tuple(len(items) for items, _ in bad_owners))
    bad_splits = plan.splits[:split_index] + (bad_split,) + plan.splits[split_index + 1:]
    expect_rejected(lambda: verify_plan(row, replace(plan, splits=bad_splits)),
                    "shared-cut interval ambiguity")
    tests += 1

    row, plan = next((row, plan) for row, plan, _ in plan_rows
                     if any(split.interval_sizes == (2, 1) for split in plan.splits))
    index = next(index for index, split in enumerate(plan.splits)
                 if split.interval_sizes == (2, 1))
    split = plan.splits[index]
    bad_split = replace(split, interval_sizes=(1, 2))
    bad_splits = plan.splits[:index] + (bad_split,) + plan.splits[index + 1:]
    expect_rejected(lambda: verify_plan(row, replace(plan, splits=bad_splits)),
                    "swapped ordered triangle intervals")
    tests += 1

    row, plan = next((row, plan) for row, plan, _ in plan_rows if len(plan.splits) >= 2)
    bad_child = replace(plan.splits[1], active=plan.splits[0].active)
    bad_splits = (plan.splits[0], bad_child) + plan.splits[2:]
    expect_rejected(lambda: verify_plan(row, replace(plan, splits=bad_splits)),
                    "recursive adhesion active set")
    tests += 1

    repair, row = repairs[0], repair_rows[0]
    bad_packet = replace(repair.packets[0], theorem="forged-theorem")
    expect_rejected(
        lambda: verify_safe_repair(
            row, replace(repair, packets=(bad_packet,) + repair.packets[1:])),
        "repair packet theorem",
    )
    tests += 1
    expect_rejected(lambda: verify_safe_repair(row, replace(repair, interval_sizes=(1, 2))),
                    "repair swapped router intervals")
    tests += 1

    repair, row = repairs[-1], repair_rows[-1]
    opening = repair.opening
    require(isinstance(opening, PentagonOpening), "opening mutation fixture is absent")
    owners = dict(opening.vertex_owners)
    owners[opening.vertices[1]] = opening.retained_owner
    bad_opening = replace(opening, vertex_owners=tuple(owners.items()))
    expect_rejected(lambda: verify_safe_repair(row, replace(repair, opening=bad_opening)),
                    "pentagon four-path vertex owner")
    tests += 1
    expect_rejected(
        lambda: verify_safe_repair(row, replace(repair, connector_owners=("opened-PA", "A9P"))),
        "pentagon connector reachability",
    )
    tests += 1
    return tests


def expected_residual(row):
    """Recognize the independently specified six-signature frontier."""
    adjacency = BASE.BASE.adjacency(row.tree)
    cuts = tuple(range(9, len(adjacency)))
    first, second = row.positions
    if len(cuts) == 1:
        return (
            first.kind == second.kind == "cut"
            or {first.kind, second.kind} == {"cut", "private"}
            or first.kind == second.kind == "private" and first.vertex != second.vertex
        )
    if len(cuts) != 2:
        return False
    routers = [cycle for cycle in range(9) if len(adjacency[cycle]) == 2]
    hubs = [cut for cut in cuts if len(adjacency[cut]) == 8]
    if len(routers) != 1 or len(hubs) != 1:
        return False
    private = BASE.Position("private", routers[0], 0)
    locked = BASE.Position("cut", hubs[0])
    return {first, second} == {private, locked}


def make_safe_repair(row, code):
    adjacency = BASE.BASE.adjacency(row.tree)
    cuts = tuple(range(9, len(adjacency)))
    if len(cuts) == 2:
        router = next(cycle for cycle in range(9) if len(adjacency[cycle]) == 2)
        hub = next(cut for cut in cuts if len(adjacency[cut]) == 8)
        leaf_cut = next(cut for cut in cuts if cut != hub)
        leaf = next(cycle for cycle in adjacency[leaf_cut] if cycle != router)
        fan = tuple(sorted(TRIANGLES - {router, leaf}))
        private_label = next(
            label for label, position in zip(PENTAGONS, row.positions)
            if position.kind == "private" and position.vertex == router
        )
        hub_label = next(label for label in PENTAGONS if label != private_label)
        tp = terminal_packet(row.tree, (leaf,), (private_label,), "TP")
        a7p = terminal_packet(row.tree, fan, (hub_label,), "A7P")
        bound = tp.bound + a7p.bound
        return Repair(
            code, "split-router: TP + packing-one A7P", router, (2, 1),
            ((BASE.Position("private", router, 0), BASE.Position("cut", leaf_cut)),
             (BASE.Position("cut", hub),)),
            ("TP", "A7P"), (tp, a7p),
            tuple("TP" if label == private_label else "A7P" for label in PENTAGONS),
            ((hub, "A7P"), (leaf_cut, "TP")), None, bound,
        )

    require(len(cuts) == 1, f"{code}: safe opening repair is not a bouquet")
    hub = cuts[0]
    packet = terminal_packet(row.tree, TRIANGLES, ("PB",), "A9P")
    bound = Bound(packet.bound.credit - 1, packet.bound.deficits, packet.bound.strict)
    vertices = tuple(f"PA.v{index}" for index in range(5))
    edges = tuple((vertices[index], vertices[(index + 1) % 5]) for index in range(5))
    opening = PentagonOpening(
        "PA", vertices, edges, vertices[0],
        tuple((vertex, "A9P" if index == 0 else "opened-PA")
              for index, vertex in enumerate(vertices)),
        tuple((vertex, "A9P" if index == 0 else "opened-PA")
              for index, vertex in enumerate(vertices)),
        "A9P", "opened-PA", -1,
    )
    return Repair(
        code, "open PA; retain packing-one A9P", None, (), (), (), (packet,),
        ("A9P", "A9P"), ((hub, "A9P"),),
        opening, bound,
    )


def verify_safe_repair(row, repair):
    adjacency = BASE.BASE.adjacency(row.tree)
    cuts = set(range(9, len(adjacency)))
    require(expected_residual(row), f"{repair.code}: repair applied outside six-signature set")
    packet_by_name = {packet.name: packet for packet in repair.packets}
    require(len(packet_by_name) == len(repair.packets), f"{repair.code}: duplicate packet name")
    for packet in repair.packets:
        require(packet == terminal_packet(row.tree, packet.cycles, packet.demands, packet.name),
                f"{repair.code}: packet theorem/hypothesis/bound was not rederived")
    cycles = [cycle for packet in repair.packets for cycle in packet.cycles]
    demands = [demand for packet in repair.packets for demand in packet.demands]
    cut_owners = dict(repair.cut_owners)
    require(len(cut_owners) == len(repair.cut_owners) and cut_owners.keys() == cuts,
            f"{repair.code}: cut-owner domain mismatch")
    valid_owner_names = set(packet_by_name) | {"opened-PA"}
    require(set(cut_owners.values()) <= valid_owner_names,
            f"{repair.code}: cut owner has no materialized packet/opening")
    require(len(repair.connector_owners) == 2 and
            set(repair.connector_owners) <= valid_owner_names,
            f"{repair.code}: connector owners are not materialized")
    cycle_owner = {cycle: packet.name for packet in repair.packets for cycle in packet.cycles}
    require(len(cycle_owner) == len(cycles), f"{repair.code}: cycle has two packet owners")
    for cut in cuts:
        incident = {cycle_owner[cycle] for cycle in adjacency[cut] if cycle in cycle_owner}
        require(len(incident) <= 1, f"{repair.code}: cut meets competing retained packets")
        if incident:
            require(incident == {cut_owners[cut]},
                    f"{repair.code}: cut owner disagrees with retained cycles")
    if repair.opening is None:
        require(repair.router is not None, f"{repair.code}: split repair has no router")
        require(repair.interval_sizes == tuple(map(len, repair.interval_positions)),
                f"{repair.code}: interval sizes are not bound to concrete positions")
        require(repair.interval_sizes == (2, 1) and sum(repair.interval_sizes) == 3,
                f"{repair.code}: router intervals are not concrete proper intervals")
        require(repair.interval_owners == ("TP", "A7P"),
                f"{repair.code}: split interval owners changed")
        local = local_triangle_positions(row.tree, repair.router)
        require(Counter(position for interval in repair.interval_positions for position in interval)
                == Counter(local), f"{repair.code}: intervals do not partition router vertices")
        require(repair.interval_positions[0] ==
                (BASE.Position("private", repair.router, 0),
                 next(BASE.Position("cut", cut) for cut in adjacency[repair.router]
                      if cut_owners[cut] == "TP")),
                f"{repair.code}: ordered size-two interval is not private+leaf-cut")
        require(repair.interval_positions[1] ==
                (next(BASE.Position("cut", cut) for cut in adjacency[repair.router]
                      if cut_owners[cut] == "A7P"),),
                f"{repair.code}: singleton interval is not the hub cut")
        require(Counter(demands) == Counter(PENTAGONS),
                f"{repair.code}: split demands are not exact")
        require(Counter(cycles) == Counter(TRIANGLES - {repair.router}),
                f"{repair.code}: split cycles are not distinct/exhaustive")
        require(repair.bound == Bound(Fraction(8), 2, True),
                f"{repair.code}: TP+A7P radical ledger changed")
        require(repair.bound == sum((packet.bound for packet in repair.packets), ZERO),
                f"{repair.code}: split bound is not the exact packet sum")
        a7p = next(packet for packet in repair.packets if packet.name == "A7P")
        require(len(a7p.cycles) == 7 and pairwise_intersecting(row.tree, a7p.cycles),
                f"{repair.code}: A7P packing-one hypothesis is not materialized")
        hub = common_cut(row.tree, a7p.cycles)
        require(hub is not None and dict(repair.cut_owners)[hub] == "A7P",
                f"{repair.code}: A7P hub has no final cut owner")
        tp = next(packet for packet in repair.packets if packet.name == "TP")
        require(len(tp.cycles) == 1 and tp.theorem == "TP-quantitative",
                f"{repair.code}: TP theorem was not derived from its exact profile")
        for label, position, owner in zip(PENTAGONS, row.positions, repair.connector_owners):
            require(label in packet_by_name[owner].demands,
                    f"{repair.code}: connector owner omits its demand")
            if position.kind == "private" and position.vertex == repair.router:
                require(position in repair.interval_positions[repair.interval_owners.index(owner)],
                        f"{repair.code}: private connector does not reach its interval owner")
            elif position.kind == "cut":
                require(cut_owners[position.vertex] == owner,
                        f"{repair.code}: cut connector does not reach its cut owner")
    else:
        opening = repair.opening
        require(isinstance(opening, PentagonOpening), f"{repair.code}: opening is not materialized")
        require(repair.router is None and not repair.interval_sizes and
                not repair.interval_positions and not repair.interval_owners,
                f"{repair.code}: pentagon opening carries triangle-router data")
        require(opening.label == "PA" and opening.cost == -1,
                f"{repair.code}: opening label/cost changed")
        require(opening.vertices == tuple(f"PA.v{index}" for index in range(5)) and
                len(set(opening.vertices)) == 5,
                f"{repair.code}: opening lacks five distinct cyclic vertices")
        require(opening.cyclic_edges == tuple(
                    (opening.vertices[index], opening.vertices[(index + 1) % 5])
                    for index in range(5)),
                f"{repair.code}: opening vertices are not in one five-cycle")
        require(opening.connector_vertex == opening.vertices[0],
                f"{repair.code}: connector root is not the named singleton")
        expected_vertex_owners = {
            vertex: opening.retained_owner if vertex == opening.connector_vertex
            else opening.opening_owner for vertex in opening.vertices
        }
        require(len(opening.vertex_owners) == len(expected_vertex_owners) and
                len({vertex for vertex, _ in opening.vertex_owners}) == len(opening.vertex_owners) and
                dict(opening.vertex_owners) == expected_vertex_owners,
                f"{repair.code}: pentagon vertex ownership is not singleton+four-path")
        require(len(opening.attachment_owners) == len(expected_vertex_owners) and
                len({vertex for vertex, _ in opening.attachment_owners}) == len(opening.attachment_owners) and
                dict(opening.attachment_owners) == expected_vertex_owners,
                f"{repair.code}: attachments do not follow pentagon vertex owners")
        opening_edges = {frozenset(edge) for edge in opening.cyclic_edges}
        path_vertices = set(opening.vertices) - {opening.connector_vertex}
        require(sum(edge <= path_vertices for edge in opening_edges) == 3,
                f"{repair.code}: complementary four vertices do not induce a path")
        require(opening.retained_owner == "A9P" and opening.opening_owner == "opened-PA",
                f"{repair.code}: opening owner names changed")
        require(Counter(demands + [opening.label]) == Counter(PENTAGONS),
                f"{repair.code}: opening demands are not exact")
        require(Counter(cycles) == Counter(TRIANGLES),
                f"{repair.code}: retained A9 cycles are not distinct/exhaustive")
        require(repair.bound == Bound(Fraction(8), 1, True),
                f"{repair.code}: opened A9P radical ledger changed")
        packet = repair.packets[0]
        require(repair.bound == Bound(packet.bound.credit + opening.cost,
                                      packet.bound.deficits, packet.bound.strict),
                f"{repair.code}: opening bound is not packet bound plus exact cost")
        require(len(packet.cycles) == 9 and pairwise_intersecting(row.tree, packet.cycles),
                f"{repair.code}: A9P packing-one hypothesis is not materialized")
        hub = common_cut(row.tree, packet.cycles)
        require(hub is not None and dict(repair.cut_owners)[hub] == "A9P",
                f"{repair.code}: A9P hub has no final cut owner")
        require(repair.connector_owners == ("A9P", "A9P") and
                dict(opening.vertex_owners)[opening.connector_vertex] ==
                repair.connector_owners[0] and
                "PB" in packet_by_name["A9P"].demands,
                f"{repair.code}: opening connector owners are not reachable")
    require(repair.bound.positive(), f"{repair.code}: exact radical ledger is not positive")


def main():
    rows, classes, placements = enumerate_rows()
    accepted = []
    residuals = []
    theorem_counts = Counter()
    records = []
    two_arm_records = []
    accepted_plans = []
    for index, row in enumerate(rows, 1):
        plan = choose_plan(row)
        if plan is None:
            residuals.append(row)
            continue
        position_owners = verify_plan(row, plan)
        accepted.append(row)
        accepted_plans.append((row, plan, position_owners))
        theorem_counts.update(packet.theorem for packet in plan.packets)
        records.append(plan_text(row, plan, position_owners))
        exceptional = (
            len(plan.splits) == 2
            and plan.routers == tuple(position.vertex for position in row.positions)
            and all(position.kind == "private" for position in row.positions)
            and all(len(split.interval_sizes) == 2 for split in plan.splits)
        )
        if exceptional:
            two_arm_records.append(plan_text(row, plan, position_owners))
        if index % 5000 == 0:
            print(f"checked {index}/{len(rows)}", flush=True)

    row_digest = digest(row.signature for row in rows)
    residual_digest = digest(row.signature for row in residuals)
    proof_digest = digest(records)
    accepted_digest = digest(row.signature for row in accepted)
    two_arm_digest = digest(two_arm_records)
    specified_residuals = tuple(row for row in rows if expected_residual(row))
    specified_digest = digest(row.signature for row in specified_residuals)
    repairs = tuple(make_safe_repair(row, f"R{index}")
                    for index, row in enumerate(specified_residuals, 1))
    for row, repair in zip(specified_residuals, repairs):
        verify_safe_repair(row, repair)
    mutation_count = mutation_self_tests(accepted_plans, repairs, specified_residuals)
    repair_digest = digest(repair_text(row, repair)
                           for row, repair in zip(specified_residuals, repairs))
    print("nine-triangle incidence trees:", len(classes))
    print("ordered labelled placements before automorphisms:", placements)
    print("canonical marked rows:", len(rows))
    print("ordinary theorem-aware accepted:", len(accepted))
    print("residual signatures:", len(residuals))
    print("theorem uses:", dict(sorted(theorem_counts.items())))
    print("canonical-row sha256:", row_digest)
    print("residual sha256:", residual_digest)
    print("ordinary-proof sha256:", proof_digest)
    print("ordinary-signature sha256:", accepted_digest)
    print("two-arm plan count:", len(two_arm_records))
    print("two-arm plan sha256:", two_arm_digest)
    print("specified-six sha256:", specified_digest)
    print("safe repair profiles:", dict(sorted(Counter(repair.operation for repair in repairs).items())))
    print("safe repair sha256:", repair_digest)
    print("rejected mutation self-tests:", mutation_count)
    for index, row in enumerate(residuals, 1):
        print(f"R{index}: {row.signature}")

    require(len(classes) == 355, "incidence count changed")
    require(placements == 128155, "ordered placement count changed")
    require(len(rows) == 43151, "canonical marked row count changed")
    require(row_digest == "0bf53914ae760002386b4b94e4de2d0cccbe61725063b4a46435bcd49c70403b",
            "canonical row digest changed")
    require(len(specified_residuals) == 6, "specified residual count is not six")
    require(specified_digest ==
            "248a595dfebef2cdb2caaa0c0f9d0d729ff0e1be71d3345bfc4cb2869072b26d",
            "specified residual signature digest changed")
    require(len(accepted) == 43145, "fail-closed: theorem-aware 43145 count not reproduced")
    require(tuple(residuals) == specified_residuals,
            "fail-closed: search residuals differ from specified six signatures")
    require(accepted_digest == "8d170ef9af714c6288214e5933826fcbfe2d006dc0e70c7277a393fc2d18239c",
            "ordinary accepted-signature digest changed")
    require(proof_digest == "58f9951b620fa9f4830724a8bbc5b426a6125437b11c84b125d4ee63488dd3ec",
            "ordinary proof digest changed")
    require(len(two_arm_records) == 15, "explicit two-arm plan count changed")
    require(two_arm_digest == "1512256af2a6e1294ca6f21d176877829ad1fd1aabb7555345e5486cb8b3b98d",
            "explicit two-arm plan digest changed")
    require(repair_digest == "9b8631b8d1b92970584156e2e444fedf78c2394e0867d43c1204aa09c4f49e0e",
            "safe repair digest changed")
    require(mutation_count == 10, "mutation self-test count changed")


if __name__ == "__main__":
    main()
