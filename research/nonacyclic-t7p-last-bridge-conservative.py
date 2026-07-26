#!/usr/bin/env python3
"""Exact marked-entry census for the disconnected rank-nine T^7P | P row."""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from itertools import combinations, permutations


HERE = Path(__file__).resolve().parent


def check(condition, message):
    """Fail closed even when Python is run with optimization enabled."""
    if not condition:
        raise RuntimeError(message)


SPEC = spec_from_file_location(
    "incidence", HERE / "nonacyclic-fully-shared-incidence-census.py"
)
BASE = module_from_spec(SPEC)
check(SPEC.loader is not None, "could not load incidence census module")
SPEC.loader.exec_module(BASE)


NAKED_TREE_OWNER = "naked-tree:entry"


@dataclass(frozen=True)
class Mark:
    kind: str
    vertex: int


REFINEMENT_REGRESSION = (
    "X(P()T()T()T()T(X(T()))T(X(T())))",
    Mark("cut", 8),
)


@dataclass(frozen=True)
class Bound:
    value: Fraction
    strict: bool
    source: str


@dataclass(frozen=True)
class Packet:
    owner: str
    cycles: tuple[int, ...]
    bound: tuple[Fraction, int, bool, str]


@dataclass(frozen=True)
class Interval:
    port: tuple[str, int]
    size: int
    owner: str


@dataclass(frozen=True)
class RouterStep:
    router: int
    active_cycles: tuple[int, ...]
    intervals: tuple[Interval, ...]


@dataclass(frozen=True)
class DeletionCertificate:
    order: tuple[int, ...]
    steps: tuple[RouterStep, ...]
    packets: tuple[Packet, ...]
    cut_owners: tuple[tuple[int, str], ...]
    root_owner: str
    remote_owner: str
    attachment_owners: tuple[tuple[tuple[str, int], str], ...]
    ledger: tuple[Fraction, int]
    strict: bool
    positive: bool
    entry_cost: int
    keep_connector: bool


@dataclass(frozen=True)
class OneRouterCertificate:
    step: RouterStep
    packet_bounds: tuple[Bound, ...]
    cut_owners: tuple[tuple[int, str], ...]
    root_owner: str
    remote_owner: str
    attachment_owners: tuple[tuple[tuple[str, int], str], ...]
    total: Fraction
    strict: bool
    positive: bool
    keep_connector: bool


TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1, 7: 0}


def marked_signature(tree, mark):
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)

    def code(vertex, parent):
        if vertex < cycle_count:
            color = tree.colors[vertex]
            if mark.kind == "private" and mark.vertex == vertex:
                color += "R"
        else:
            color = "R" if mark.kind == "cut" and mark.vertex == vertex else "X"
        children = sorted(
            code(neighbor, vertex) for neighbor in adj[vertex] if neighbor != parent
        )
        return color + "(" + "".join(children) + ")"

    return min(code(center, -1) for center in BASE.tree_centers(adj))


def root_orbits(tree):
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    candidates = [(Mark("cut", cut), 1) for cut in range(cycle_count, len(adj))]
    candidates += [
        (Mark("private", cycle), 3 - len(adj[cycle]))
        for cycle, color in enumerate(tree.colors)
        if color == "T" and len(adj[cycle]) < 3
    ]
    answer = {}
    for mark, positions in candidates:
        code = marked_signature(tree, mark)
        if code in answer:
            representative, old_positions = answer[code]
            answer[code] = representative, old_positions + positions
        else:
            answer[code] = mark, positions
    return tuple((code, *value) for code, value in sorted(answer.items()))


def component_counts(tree, component):
    counts = Counter(tree.colors[cycle] for cycle in component[0])
    return counts["T"], counts["P"]


def root_component(tree, sacrificed, mark, components):
    if mark.kind == "private" and mark.vertex == sacrificed:
        return None
    adj = BASE.adjacency(tree)
    for index, component in enumerate(components):
        vertices = set(component[0]) | set(component[1])
        if mark.vertex in vertices:
            return index
        if mark.kind == "cut" and any(
            mark.vertex in adj[cycle] for cycle in component[0]
        ):
            return index
    raise AssertionError((sacrificed, mark, components))


def profile_bound(tree, component):
    triangles, pentagons = component_counts(tree, component)
    if pentagons == 0:
        return Bound(Fraction(TRIANGLE_MARGIN[triangles]), True, f"A_{triangles}")
    base = BASE.tpp_bound(tree, component)
    return Bound(base.value, base.strict, base.source)


def conservative_split(tree, sacrificed, mark):
    if tree.colors[sacrificed] != "T":
        return None
    components = BASE.components_after_split(tree, sacrificed)
    owner = root_component(tree, sacrificed, mark, components)
    if not 2 <= len(components) + (owner is None) <= 3:
        return None
    bounds = [profile_bound(tree, component) for component in components]
    bounds.append(Bound(Fraction(-1, 4), True, "remote P>-1/4"))
    if owner is None:
        bounds.append(Bound(Fraction(-1), False, "private-entry tree>=-1"))
    total = sum((bound.value for bound in bounds), Fraction())
    strict = any(bound.strict for bound in bounds)
    positive = total > 0 or (total == 0 and strict)
    if not positive:
        return None
    return materialize_one_router(
        tree, sacrificed, mark, components, tuple(bounds), owner, False,
        total, strict, positive,
    )


def private_entry_uncut_split(tree, sacrificed, mark):
    """Keep the remote-P connector and give it to a private router interval."""
    if mark != Mark("private", sacrificed) or tree.colors[sacrificed] != "T":
        return None
    components = BASE.components_after_split(tree, sacrificed)
    if not 2 <= len(components) + 1 <= 3:
        return None
    bounds = [profile_bound(tree, component) for component in components]
    bounds.append(Bound(Fraction(-1, 4), True, "remote P>-1/4"))
    total = sum((bound.value for bound in bounds), Fraction())
    strict = any(bound.strict for bound in bounds)
    positive = total > 0 or (total == 0 and strict)
    if not positive:
        return None
    return materialize_one_router(
        tree, sacrificed, mark, components, tuple(bounds), None, True,
        total, strict, positive,
    )


def materialize_one_router(
    tree, router, mark, components, bounds, root_component_index,
    keep_connector, total, strict, positive,
):
    """Record interval, connector, cut, and attachment owners for one split."""
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    cycle_owner = {}
    component_owner = {}
    for index, component in enumerate(components):
        owner = f"packet:{index}"
        component_owner[index] = owner
        for cycle in component[0]:
            cycle_owner[cycle] = owner

    remote_owner = "remote:P1"
    root_owner = (
        remote_owner
        if keep_connector
        else NAKED_TREE_OWNER
        if root_component_index is None
        else component_owner[root_component_index]
    )
    intervals = []
    for cut in adj[router]:
        owners = {cycle_owner[cycle] for cycle in adj[cut] if cycle in cycle_owner}
        check(len(owners) == 1, ("one-router interval owner", router, cut, owners))
        intervals.append((('cut', cut), owners.pop()))
    if mark == Mark("private", router):
        intervals.append((('private', router), root_owner))
    check(2 <= len(intervals) <= 3, ("one-router interval count", router, intervals))
    check(
        len({owner for _, owner in intervals}) == len(intervals),
        ("duplicate one-router interval owners", router, intervals),
    )
    sizes = (1, 2) if len(intervals) == 2 else (1, 1, 1)
    step = RouterStep(
        router,
        tuple(range(cycle_count)),
        tuple(
            Interval(port, size, owner)
            for (port, owner), size in zip(intervals, sizes)
        ),
    )

    interval_owner = {
        interval.port[1]: interval.owner
        for interval in step.intervals
        if interval.port[0] == "cut"
    }
    cuts = []
    for cut in range(cycle_count, len(adj)):
        owners = {cycle_owner[cycle] for cycle in adj[cut] if cycle in cycle_owner}
        if owners:
            check(len(owners) == 1, ("one-router cut owner", cut, owners))
            cut_owner = owners.pop()
        else:
            cut_owner = interval_owner[cut]
        cuts.append((cut, cut_owner))
    if mark.kind == "cut":
        root_owner = dict(cuts)[mark.vertex]
    elif mark.vertex != router:
        root_owner = cycle_owner[mark.vertex]

    attachments = tuple(
        [(('cut', cut), owner) for cut, owner in cuts]
        + [(('private', cycle), cycle_owner[cycle]) for cycle in cycle_owner]
        + [
            ((f"router-{step.router}-interval", index), interval.owner)
            for index, interval in enumerate(step.intervals)
        ]
        + [(('root', mark.vertex), root_owner), (('remote', 1), remote_owner)]
    )
    check(
        sum(interval.size for interval in step.intervals) == 3,
        ("one-router interval size", step),
    )
    certificate = OneRouterCertificate(
        step, bounds, tuple(cuts), root_owner, remote_owner, attachments,
        total, strict, positive, keep_connector,
    )
    validate_concrete_owners(
        [root_owner, remote_owner]
        + [owner for _, owner in cuts]
        + [interval.owner for interval in step.intervals]
        + [owner for _, owner in attachments],
        "one-router certificate",
    )
    return certificate


def validate_concrete_owners(owners, context):
    allowed = lambda owner: (
        owner.startswith("packet:")
        or owner.startswith("remote:")
        or owner.startswith("naked-tree:")
    )
    check(all(allowed(owner) for owner in owners), (context, owners))
    check(
        all(not owner.startswith("territory:") for owner in owners),
        ("unresolved synthetic territory", context, owners),
    )


def common_cut(tree, cycles):
    adj = BASE.adjacency(tree)
    return any(all(cut in adj[cycle] for cycle in cycles) for cut in adj[cycles[0]])


def packet_bound(tree, cycles):
    triangles = tuple(cycle for cycle in cycles if tree.colors[cycle] == "T")
    pentagons = tuple(cycle for cycle in cycles if tree.colors[cycle] == "P")
    if not pentagons:
        return Fraction(TRIANGLE_MARGIN[len(triangles)]), 0, True, f"A_{len(triangles)}"
    check(len(pentagons) == 1, ("packet pentagon count", cycles, pentagons))
    if common_cut(tree, cycles):
        return Fraction(len(triangles)), 1, True, f"common-cut T^{len(triangles)}P"
    if len(triangles) == 2 and common_cut(tree, triangles):
        return Fraction(2), 1, True, "shared-cut TTP"
    rank = len(cycles)
    if rank in (2, 3):
        return Fraction(), 0, False, f"generic rank-{rank}>=0"
    check(rank >= 4, ("unsupported packet rank", cycles, rank))
    return Fraction(), 0, True, f"generic rank-{rank}>0"


def deleted_components(tree, deleted):
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    blocked = set(deleted)
    seen = set(blocked)
    answer = []
    for start in range(len(adj)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        vertices = set()
        cycles = set()
        while stack:
            vertex = stack.pop()
            vertices.add(vertex)
            if vertex < cycle_count:
                cycles.add(vertex)
            for neighbor in adj[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if cycles:
            answer.append((vertices, tuple(sorted(cycles))))
    return tuple(answer)


def connected_cycles(tree, cycles):
    if len(cycles) <= 1:
        return True
    adj = BASE.adjacency(tree)
    allowed = set(cycles)
    seen = {cycles[0]}
    stack = [cycles[0]]
    while stack:
        cycle = stack.pop()
        for cut in adj[cycle]:
            for neighbor in adj[cut]:
                if neighbor in allowed and neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return seen == allowed


def exact_sign(a, b):
    """Sign of a-b*(sqrt(5)-2), using positive-side squaring only."""
    left = a + 2 * b
    right_square = 5 * b * b
    if left < 0:
        return -1
    if left == 0:
        return 0 if b == 0 else -1
    left_square = left * left
    if left_square == right_square:
        return 0
    return 1 if left_square > right_square else -1


def active_territory(adj, active, start):
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for neighbor in adj[vertex]:
            if neighbor in active and neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    return seen


def materialize_split_order(tree, deleted, mark, cycle_owner, private_owner):
    """Find a sequential refinement and record every proper router interval."""
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    for order in permutations(deleted):
        active = set(range(len(adj)))
        steps = []
        for router in order:
            if router not in active:
                break
            territory = active_territory(adj, active, router)
            active_cycles = tuple(sorted(v for v in territory if v < cycle_count))
            active.remove(router)
            intervals = []
            for cut in adj[router]:
                if cut not in territory:
                    continue
                seen = {cut}
                stack = [cut]
                cycles = set()
                while stack:
                    vertex = stack.pop()
                    if vertex < cycle_count:
                        cycles.add(vertex)
                    for neighbor in adj[vertex]:
                        if neighbor in active and neighbor in territory and neighbor not in seen:
                            seen.add(neighbor)
                            stack.append(neighbor)
                if cycles:
                    owners = {
                        cycle_owner[cycle]
                        for cycle in cycles
                        if cycle in cycle_owner
                    }
                    owner = (
                        owners.pop()
                        if len(owners) == 1
                        else f"territory:{router}:{cut}"
                    )
                    intervals.append((('cut', cut), owner))
            else:
                if mark == Mark("private", router):
                    intervals.append((('private', router), private_owner))
                if not 2 <= len(intervals) <= 3:
                    break
                owners = [owner for _, owner in intervals]
                if len(owners) != len(set(owners)):
                    break
                sizes = (1, 2) if len(intervals) == 2 else (1, 1, 1)
                steps.append(
                    RouterStep(
                        router,
                        active_cycles,
                        tuple(
                            Interval(port, size, owner)
                            for (port, owner), size in zip(intervals, sizes)
                        ),
                    )
                )
                continue
            break
        else:
            resolved = resolve_refined_owners(tree, tuple(steps), cycle_owner)
            if resolved is not None:
                return resolved
    return None


def resolve_refined_owners(tree, steps, cycle_owner):
    """Push provisional territory owners through all later refinements."""
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    candidates = {}
    for cut in range(cycle_count, len(adj)):
        candidates[cut] = {
            cycle_owner[cycle]
            for cycle in adj[cut]
            if cycle in cycle_owner
        }
    for step in steps:
        for interval in step.intervals:
            if interval.port[0] == "cut" and not interval.owner.startswith("territory:"):
                candidates[interval.port[1]].add(interval.owner)

    final_owner = {}
    for cut, owners in candidates.items():
        if len(owners) == 1:
            final_owner[cut] = next(iter(owners))

    answer = []
    for step in steps:
        intervals = []
        for interval in step.intervals:
            owner = interval.owner
            if owner.startswith("territory:"):
                owner = final_owner.get(interval.port[1])
                if owner is None:
                    break
            intervals.append(Interval(interval.port, interval.size, owner))
        else:
            owners = [interval.owner for interval in intervals]
            if len(owners) != len(set(owners)):
                return None
            answer.append(RouterStep(step.router, step.active_cycles, tuple(intervals)))
            continue
        return None
    return tuple(answer)


def cut_ownership(tree, cycle_owner, steps):
    adj = BASE.adjacency(tree)
    cycle_count = len(tree.colors)
    interval_owner = {
        interval.port[1]: interval.owner
        for step in steps
        for interval in step.intervals
        if interval.port[0] == "cut"
    }
    answer = []
    for cut in range(cycle_count, len(adj)):
        owners = {
            cycle_owner[cycle]
            for cycle in adj[cut]
            if cycle in cycle_owner
        }
        if owners:
            if len(owners) != 1:
                break
            owner = owners.pop()
            if cut in interval_owner:
                check(
                    interval_owner[cut] == owner,
                    ("refined interval/cut owner mismatch", cut, interval_owner[cut], owner),
                )
        else:
            owner = interval_owner[cut]
        answer.append((cut, owner))
    else:
        return tuple(answer)
    raise AssertionError((cut, owners))


def deletion_certificate(tree, deleted, mark, keep_connector=False):
    """Materialize a conservative sequential router and packet certificate."""
    adj = BASE.adjacency(tree)
    components = deleted_components(tree, deleted)
    private_deleted = mark.kind == "private" and mark.vertex in deleted
    if keep_connector and not private_deleted:
        return None

    packets = []
    cycle_owner = {}
    for index, (_, cycles) in enumerate(components):
        check(connected_cycles(tree, cycles), ("disconnected packet", deleted, cycles))
        bound = packet_bound(tree, cycles)
        owner = f"packet:{index}"
        packets.append(Packet(owner, cycles, bound))
        for cycle in cycles:
            cycle_owner[cycle] = owner

    remote_owner = "remote:P1"
    remote_bound = (Fraction(), 1, True, "remote P>-delta")
    packets.append(Packet(remote_owner, (), remote_bound))
    entry_owner = None
    if private_deleted and not keep_connector:
        entry_owner = NAKED_TREE_OWNER
        packets.append(
            Packet(entry_owner, (), (Fraction(-1), 0, False, "private-entry tree=-1"))
        )
    private_owner = remote_owner if keep_connector else entry_owner
    steps = materialize_split_order(
        tree, deleted, mark, cycle_owner, private_owner
    )
    if steps is None:
        return None

    cuts = cut_ownership(tree, cycle_owner, steps)
    cut_owner = dict(cuts)
    if mark.kind == "cut":
        root_owner = cut_owner[mark.vertex]
    elif private_deleted:
        root_owner = private_owner
    else:
        root_owner = cycle_owner[mark.vertex]

    bounds = tuple(packet.bound for packet in packets)
    a = sum(bound[0] for bound in bounds)
    b = sum(bound[1] for bound in bounds)
    strict = any(bound[2] for bound in bounds)
    entry_cost = int(private_deleted and not keep_connector)
    sign = exact_sign(a, b)
    positive = sign > 0 or (sign == 0 and strict)
    if not positive:
        return None

    attachments = tuple(
        [(('cut', cut), owner) for cut, owner in cuts]
        + [(('private', cycle), cycle_owner[cycle]) for cycle in cycle_owner]
        + [
            ((f"router-{step.router}-interval", index), interval.owner)
            for step in steps
            for index, interval in enumerate(step.intervals)
        ]
        + [(('root', mark.vertex), root_owner), (('remote', 1), remote_owner)]
    )
    check(
        len(cycle_owner) == len(tree.colors) - len(deleted),
        ("retained cycle ownership", deleted, cycle_owner),
    )
    check(
        sum(len(packet.cycles) for packet in packets) == len(cycle_owner),
        ("packet cycle partition", deleted, packets),
    )
    check(
        all(0 < interval.size < 3 for step in steps for interval in step.intervals),
        ("improper replacement interval", deleted, steps),
    )
    check(
        all(sum(interval.size for interval in step.intervals) == 3 for step in steps),
        ("replacement interval size", deleted, steps),
    )
    certificate = DeletionCertificate(
        tuple(step.router for step in steps), steps, tuple(packets), cuts, root_owner, remote_owner,
        attachments, (a, b), strict, positive, entry_cost, keep_connector,
    )
    validate_deletion_owners(certificate)
    return certificate


def validate_deletion_owners(certificate):
    """Require every replacement territory to name a final packet explicitly."""
    packet_owners = {packet.owner for packet in certificate.packets}
    represented = [certificate.root_owner, certificate.remote_owner]
    represented.extend(owner for _, owner in certificate.cut_owners)
    represented.extend(
        interval.owner
        for step in certificate.steps
        for interval in step.intervals
    )
    represented.extend(owner for _, owner in certificate.attachment_owners)
    check(
        all(owner in packet_owners for owner in represented),
        ("non-packet replacement owner", packet_owners, represented),
    )
    check(
        all(not owner.startswith("territory:") for owner in represented),
        ("unresolved synthetic territory", represented),
    )
    validate_concrete_owners(represented, "replacement certificate")


def best_deletion_certificate(tree, mark):
    triangles = tuple(i for i, color in enumerate(tree.colors) if color == "T")
    for size in range(len(triangles) + 1):
        for deleted in combinations(triangles, size):
            for keep_connector in (False, True):
                certificate = deletion_certificate(
                    tree, deleted, mark, keep_connector=keep_connector
                )
                if certificate is not None:
                    return certificate
    return None


def census():
    classes = BASE.enumerate_colors(("P",) + ("T",) * 7, 5)
    all_counts = Counter(BASE.cut_count(tree) for _, tree in classes)
    leaf_counts = Counter()
    marked = Counter()
    positions = Counter()
    resolved = Counter()
    failures = []
    deletion_resolved = Counter()
    deletion_sizes = Counter()
    replacement_certificates = []
    refinement_regression_seen = False
    for signature, tree in classes:
        adj = BASE.adjacency(tree)
        pentagon = tree.colors.index("P")
        if len(adj[pentagon]) != 1:
            continue
        cuts = BASE.cut_count(tree)
        leaf_counts[cuts] += 1
        for root_code, mark, multiplicity in root_orbits(tree):
            marked[cuts] += 1
            positions[cuts] += multiplicity
            certificates = tuple(
                conservative_split(tree, cycle, mark)
                for cycle, color in enumerate(tree.colors)
                if color == "T"
            )
            certificates += tuple(
                private_entry_uncut_split(tree, cycle, mark)
                for cycle, color in enumerate(tree.colors)
                if color == "T"
            )
            if any(item is not None for item in certificates):
                check(
                    all(
                        item is None or (item.positive and item.strict)
                        for item in certificates
                    ),
                    ("invalid direct certificate", signature, root_code),
                )
                resolved[cuts] += 1
            else:
                replacement = best_deletion_certificate(tree, mark)
                if replacement is not None:
                    check(
                        replacement.positive and replacement.strict,
                        ("nonpositive replacement", signature, root_code, replacement),
                    )
                    check(
                        bool(replacement.root_owner),
                        ("missing replacement root owner", signature, root_code),
                    )
                    check(
                        replacement.remote_owner == "remote:P1",
                        ("wrong remote owner", signature, root_code, replacement.remote_owner),
                    )
                    check(
                        all(connected_cycles(tree, packet.cycles) for packet in replacement.packets),
                        ("disconnected replacement packet", signature, root_code),
                    )
                    validate_deletion_owners(replacement)
                    replacement_certificates.append(replacement)
                    if (signature, mark) == REFINEMENT_REGRESSION:
                        check(
                            replacement.order == (0, 1)
                            and replacement.steps[0].intervals[0].owner == "packet:1"
                            and replacement.cut_owners[0] == (8, "packet:1")
                            and replacement.root_owner == "packet:1",
                            ("sequential-refinement regression", replacement),
                        )
                        refinement_regression_seen = True
                    deletion_resolved[cuts] += 1
                    deletion_sizes[len(replacement.order)] += 1
                else:
                    failures.append(
                        (cuts, signature, root_code, mark, multiplicity, tree.edges)
                    )
    failures.sort(key=lambda item: (item[0], item[2]))
    check(
        sum(marked.values())
        == sum(resolved.values()) + sum(deletion_resolved.values()) + len(failures),
        ("census partition", marked, resolved, deletion_resolved, failures),
    )
    check(all_counts == Counter({1: 1, 2: 9, 3: 49, 4: 145, 5: 245, 6: 205, 7: 69}), ("all counts", all_counts))
    check(leaf_counts == Counter({1: 1, 2: 6, 3: 30, 4: 79, 5: 120, 6: 86, 7: 23}), ("leaf counts", leaf_counts))
    check(marked == Counter({1: 2, 2: 29, 3: 195, 4: 661, 5: 1144, 6: 909, 7: 248}), ("marked counts", marked))
    check(resolved == Counter({2: 24, 3: 186, 4: 649, 5: 1134, 6: 909, 7: 248}), ("direct counts", resolved))
    check(deletion_resolved == Counter({1: 2, 2: 5, 3: 9, 4: 12, 5: 10}), ("replacement counts", deletion_resolved))
    check(deletion_sizes == Counter({0: 2, 1: 9, 2: 22, 3: 5}), ("replacement sizes", deletion_sizes))
    check(len(replacement_certificates) == 38, ("replacement total", len(replacement_certificates)))
    check(
        all(
            not owner.startswith("territory:")
            for certificate in replacement_certificates
            for _, owner in certificate.attachment_owners
        ),
        "synthetic owner remains in one of 38 replacements",
    )
    check(refinement_regression_seen, "sequential-refinement regression class not checked")
    check(not failures, ("unresolved marked rows", failures))
    return (
        all_counts,
        leaf_counts,
        marked,
        positions,
        resolved,
        deletion_resolved,
        deletion_sizes,
        failures,
    )


def main():
    (
        all_counts,
        leaf_counts,
        marked,
        positions,
        resolved,
        deletion_resolved,
        deletion_sizes,
        failures,
    ) = census()
    print("all T^7P incidence trees:", dict(sorted(all_counts.items())))
    print("P-leaf incidence trees:", dict(sorted(leaf_counts.items())))
    print("marked root orbits:", dict(sorted(marked.items())), "total", sum(marked.values()))
    print("labelled root positions:", dict(sorted(positions.items())))
    print("one-router resolved:", dict(sorted(resolved.items())), "total", sum(resolved.values()))
    print("replacement resolved:", dict(sorted(deletion_resolved.items())), "total", sum(deletion_resolved.values()))
    print("replacement deletion sizes:", dict(sorted(deletion_sizes.items())))
    print("failures:", len(failures), dict(sorted(Counter(x[0] for x in failures).items())))
    for index, (cuts, signature, root_code, mark, multiplicity, edges) in enumerate(failures, 1):
        print(f"N{index}: c={cuts} root={mark.kind}:{mark.vertex} positions={multiplicity}")
        print(f"  root-code={root_code}")
        print(f"  incidence={signature}")
        print(f"  edges={edges}")


if __name__ == "__main__":
    main()
