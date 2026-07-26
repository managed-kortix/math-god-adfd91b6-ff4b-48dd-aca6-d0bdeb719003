#!/usr/bin/env python3
"""Independent exact last-bridge marked-root census for G6PP.

This file deliberately imports no project census.  It regenerates the colored
T^6P incidence trees, roots every cyclic position, applies the strict
last-bridge convention (P1 is always a separate packet), and searches packet
decompositions using at most two triangle routers.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations


@dataclass(frozen=True)
class IncidenceTree:
    colors: tuple[str, ...]
    edges: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class Root:
    kind: str
    vertex: int


@dataclass(frozen=True)
class PacketBound:
    constant: int
    delta: int
    strict: bool
    source: str


CAPACITY = {"T": 3, "P": 5}
A_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1}
P1 = "P1"


def adjacency(tree):
    rows = [[] for _ in range(len(tree.edges) + 1)]
    for left, right in tree.edges:
        rows[left].append(right)
        rows[right].append(left)
    return tuple(tuple(sorted(row)) for row in rows)


def centers(adj):
    degree = [len(row) for row in adj]
    leaves = [vertex for vertex, value in enumerate(degree) if value <= 1]
    remaining = len(adj)
    while remaining > 2:
        remaining -= len(leaves)
        next_leaves = []
        for leaf in leaves:
            for neighbor in adj[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    next_leaves.append(neighbor)
        leaves = next_leaves
    return leaves


def rooted_code(tree, vertex, parent, root=None):
    adj = adjacency(tree)
    cycle_count = len(tree.colors)
    if vertex < cycle_count:
        label = tree.colors[vertex]
        if root == Root("private", vertex):
            label += "R"
    else:
        label = "R" if root == Root("cut", vertex) else "X"
    children = sorted(
        rooted_code(tree, child, vertex, root)
        for child in adj[vertex]
        if child != parent
    )
    return label + "(" + "".join(children) + ")"


def canonical_code(tree, root=None):
    adj = adjacency(tree)
    return min(rooted_code(tree, center, -1, root) for center in centers(adj))


def extend(tree, color):
    old_cycles = len(tree.colors)
    colors = tree.colors + (color,)
    shifted = tuple(sorted((cycle, cut + 1) for cycle, cut in tree.edges))
    cut_labels = sorted({cut for _, cut in shifted})
    for cut in cut_labels:
        yield IncidenceTree(colors, tuple(sorted(shifted + ((old_cycles, cut),))))
    new_cut = max(cut_labels, default=old_cycles) + 1
    degrees = Counter(cycle for cycle, _ in shifted)
    for cycle, old_color in enumerate(tree.colors):
        if degrees[cycle] < CAPACITY[old_color]:
            yield IncidenceTree(
                colors,
                tuple(sorted(shifted + ((cycle, new_cut), (old_cycles, new_cut)))),
            )


def enumerate_trees(colors, memo=None):
    colors = tuple(sorted(colors))
    if memo is None:
        memo = {}
    if colors in memo:
        return memo[colors]
    if len(colors) == 2:
        tree = IncidenceTree(colors, ((0, 2), (1, 2)))
        answer = ((canonical_code(tree), tree),)
    else:
        classes = {}
        for color in sorted(set(colors)):
            smaller = list(colors)
            smaller.remove(color)
            for _, old_tree in enumerate_trees(tuple(smaller), memo):
                for tree in extend(old_tree, color):
                    classes.setdefault(canonical_code(tree), tree)
        answer = tuple(sorted(classes.items()))
    memo[colors] = answer
    return answer


def cut_count(tree):
    return len(tree.edges) + 1 - len(tree.colors)


def root_orbits(tree):
    adj = adjacency(tree)
    cycle_count = len(tree.colors)
    candidates = [(Root("cut", cut), 1) for cut in range(cycle_count, len(adj))]
    candidates.extend(
        (Root("private", cycle), 3 - len(adj[cycle]))
        for cycle, color in enumerate(tree.colors)
        if color == "T" and len(adj[cycle]) < 3
    )
    classes = {}
    for root, multiplicity in candidates:
        code = canonical_code(tree, root)
        if code in classes:
            representative, old_multiplicity = classes[code]
            classes[code] = representative, old_multiplicity + multiplicity
        else:
            classes[code] = root, multiplicity
    return tuple((code, root, multiplicity) for code, (root, multiplicity) in sorted(classes.items()))


def retained_components(tree, routers):
    """Cycle sets in components after router cycle nodes are removed."""
    adj = adjacency(tree)
    cycle_count = len(tree.colors)
    deleted = set(routers)
    seen = set(deleted)
    answer = []
    for start in range(len(adj)):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        cycles = []
        while stack:
            vertex = stack.pop()
            if vertex < cycle_count:
                cycles.append(vertex)
            for neighbor in adj[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if cycles:
            answer.append(tuple(sorted(cycles)))
    return tuple(sorted(answer))


def components_after_one_router(tree, router):
    adj = adjacency(tree)
    cycle_count = len(tree.colors)
    seen = {router}
    answer = []
    for start in adj[router]:
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        cycles = []
        cuts = []
        while stack:
            vertex = stack.pop()
            if vertex < cycle_count:
                cycles.append(vertex)
            else:
                cuts.append(vertex)
            for neighbor in adj[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        answer.append((tuple(sorted(cycles)), tuple(sorted(cuts))))
    return tuple(answer)


def root_component(tree, root, routers, components):
    if root.kind == "private":
        if root.vertex in routers:
            return None
        return next(index for index, part in enumerate(components) if root.vertex in part)
    adj = adjacency(tree)
    owners = {
        index
        for index, part in enumerate(components)
        if any(root.vertex in adj[cycle] for cycle in part)
    }
    if len(owners) != 1:
        return None
    return owners.pop()


def common_cut(tree, cycles):
    if not cycles:
        return False
    adj = adjacency(tree)
    return any(all(cut in adj[cycle] for cycle in cycles) for cut in adj[cycles[0]])


def packet_bound(tree, cycles):
    triangles = sum(tree.colors[cycle] == "T" for cycle in cycles)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    if pentagons == 0:
        return PacketBound(A_MARGIN[triangles], 0, True, f"A_{triangles}")
    if triangles == 0:
        assert pentagons == 1
        return PacketBound(0, 1, False, "P")
    if pentagons == 1 and common_cut(tree, cycles):
        return PacketBound(triangles, 1, True, f"common-cut T^{triangles}P")
    if (triangles, pentagons) == (2, 1):
        triangle_cycles = tuple(
            cycle for cycle in cycles if tree.colors[cycle] == "T"
        )
        if common_cut(tree, triangle_cycles):
            return PacketBound(2, 1, True, "shared-cut TTP>2-delta")
    if rank in (2, 3):
        return PacketBound(0, 0, False, f"generic rank-{rank}")
    return PacketBound(0, 0, True, f"generic rank-{rank}")


def conservative_packet_bound(tree, cycles):
    triangles = sum(tree.colors[cycle] == "T" for cycle in cycles)
    pentagons = len(cycles) - triangles
    rank = len(cycles)
    if pentagons == 0:
        return PacketBound(A_MARGIN[triangles], 0, True, f"A_{triangles}")
    if rank == 1:
        return PacketBound(0, 1, True, "P")
    if (triangles, pentagons) == (1, 1):
        return PacketBound(3, 4, True, "TP>3/4")
    if (triangles, pentagons) == (2, 1) and common_cut(tree, cycles):
        return PacketBound(7, 4, True, "common-cut TTP>7/4")
    if (triangles, pentagons) == (3, 1):
        adj = adjacency(tree)
        triangle_set = {cycle for cycle in cycles if tree.colors[cycle] == "T"}
        if any(len(triangle_set & set(adj[cut])) >= 2 for cut in range(len(tree.colors), len(adj))):
            return PacketBound(1, 0, True, "shared-pair TTTP>1")
    if rank in (2, 3):
        return PacketBound(0, 0, False, f"generic rank-{rank}")
    return PacketBound(0, 0, True, f"generic rank-{rank}")


def conservative_one_router(tree, root, router):
    components = components_after_one_router(tree, router)
    owner = None
    if root.kind == "private" and root.vertex == router:
        owner = None
    else:
        for index, (cycles, cuts) in enumerate(components):
            if root.kind == "private" and root.vertex in cycles:
                owner = index
            if root.kind == "cut":
                if root.vertex in cuts or any(root.vertex in adjacency(tree)[cycle] for cycle in cycles):
                    owner = index
                    break
        if owner is None:
            return None
    if not 2 <= len(components) + (owner is None) <= 3:
        return None
    bounds = [conservative_packet_bound(tree, cycles) for cycles, _ in components]
    bounds.append(PacketBound(0, 1, True, "remote P1"))
    if owner is None:
        bounds.append(PacketBound(-1, 0, False, "acyclic root interval"))
    values = {
        "P": Fraction(-1, 4),
        "remote P1": Fraction(-1, 4),
        "TP>3/4": Fraction(3, 4),
        "common-cut TTP>7/4": Fraction(7, 4),
        "acyclic root interval": Fraction(-1),
    }
    total = sum(
        (values.get(bound.source, Fraction(bound.constant)) for bound in bounds),
        Fraction(0),
    )
    strict = any(bound.strict for bound in bounds)
    if total > 0 or (total == 0 and strict):
        return tuple(cycles for cycles, _ in components), tuple(bounds), (total, strict)
    return None


def best_conservative_one_router(tree, root):
    answers = []
    for router, color in enumerate(tree.colors):
        if color == "T":
            certificate = conservative_one_router(tree, root, router)
            if certificate is not None:
                answers.append(((router,), certificate))
    return answers[0] if answers else None


def router_owners(tree, router, routers, components, root):
    adj = adjacency(tree)
    component_of = {
        cycle: index for index, component in enumerate(components) for cycle in component
    }
    owners = []
    for cut in adj[router]:
        side_owners = {
            component_of[cycle]
            for cycle in adj[cut]
            if cycle not in routers and cycle in component_of
        }
        if side_owners:
            assert len(side_owners) == 1
            owners.extend(side_owners)
    if root == Root("private", router):
        owners.append("root-tree")
    return tuple(dict.fromkeys(owners))


def decomposition(tree, root, routers):
    routers = tuple(sorted(routers))
    if any(tree.colors[router] != "T" for router in routers):
        return None
    components = retained_components(tree, routers)
    owner = root_component(tree, root, set(routers), components)
    if root.kind == "cut" and owner is None:
        return None
    for router in routers:
        owners = router_owners(tree, router, set(routers), components, root)
        if not 2 <= len(owners) <= 3:
            return None
    bounds = [packet_bound(tree, component) for component in components]
    bounds.append(PacketBound(0, 1, False, "remote P1"))
    if owner is None:
        bounds.append(PacketBound(-1, 0, False, "acyclic root interval"))
    constant = sum(bound.constant for bound in bounds)
    delta = sum(bound.delta for bound in bounds)
    strict = any(bound.strict for bound in bounds)
    # Exact positivity: a-b*(sqrt(5)-2)>0.  All census ledgers have a,b>=0,
    # and delta<1/4, so 4a>b is a rational certificate.
    safe = constant > 0 and 4 * constant > delta
    if not safe:
        return None
    return components, tuple(bounds), (constant, delta, strict)


def best_decomposition(tree, root, max_routers):
    triangles = tuple(i for i, color in enumerate(tree.colors) if color == "T")
    candidates = []
    for count in range(max_routers + 1):
        for routers in combinations(triangles, count):
            result = decomposition(tree, root, routers)
            if result is not None:
                candidates.append((routers, result))
    if not candidates:
        return None
    return max(candidates, key=lambda item: (item[1][2][0] * 4 - item[1][2][1], -len(item[0])))


def census():
    classes = enumerate_trees(("P",) + ("T",) * 6)
    all_counts = Counter(cut_count(tree) for _, tree in classes)
    leaf_classes = []
    marked = Counter()
    positions = Counter()
    one_router_safe = Counter()
    two_router_safe = Counter()
    stage_one_failures = []
    final_failures = []
    certificates = []
    for signature, tree in classes:
        adj = adjacency(tree)
        pentagon = tree.colors.index("P")
        if len(adj[pentagon]) != 1:
            continue
        leaf_classes.append((signature, tree))
        cuts = cut_count(tree)
        for root_code, root, multiplicity in root_orbits(tree):
            marked[cuts] += 1
            positions[cuts] += multiplicity
            one = best_conservative_one_router(tree, root)
            two = best_decomposition(tree, root, 2)
            row = (cuts, signature, root_code, root, multiplicity, tree.edges)
            if one is None:
                stage_one_failures.append(row)
            else:
                one_router_safe[cuts] += 1
            if two is None:
                final_failures.append(row)
            else:
                two_router_safe[cuts] += 1
            certificates.append((row, one, two))

    assert all_counts == Counter({1: 1, 2: 8, 3: 33, 4: 73, 5: 78, 6: 33})
    assert Counter(cut_count(tree) for _, tree in leaf_classes) == Counter(
        {1: 1, 2: 5, 3: 20, 4: 38, 5: 36, 6: 11}
    )
    assert marked == Counter({1: 2, 2: 24, 3: 126, 4: 303, 5: 316, 6: 106})
    assert positions == Counter({1: 13, 2: 65, 3: 260, 4: 494, 5: 468, 6: 143})
    assert len(stage_one_failures) == 16
    assert Counter(row[0] for row in stage_one_failures) == Counter({1: 2, 2: 5, 3: 5, 4: 4})
    stage_one_failures.sort(key=lambda row: (row[0], row[2]))
    sixteen_codes = {row[2] for row in stage_one_failures}
    final_codes = {row[2] for row in final_failures} & sixteen_codes
    return {
        "all": all_counts,
        "leaf_count": len(leaf_classes),
        "marked": marked,
        "positions": positions,
        "one_safe": one_router_safe,
        "two_safe": two_router_safe,
        "sixteen": tuple(stage_one_failures),
        "final_codes": final_codes,
        "certificates": tuple(certificates),
    }


def format_bound(bound):
    return bound.source


def main():
    result = census()
    print("independent T^6P trees:", sum(result["all"].values()), dict(sorted(result["all"].items())))
    print("P-leaf trees:", result["leaf_count"])
    print("marked roots:", sum(result["marked"].values()), dict(sorted(result["marked"].items())))
    print("labelled positions:", sum(result["positions"].values()))
    print("strict last-bridge, <=1 router: resolved=861 unresolved=16")
    resolved_sixteen = 16 - len(result["final_codes"])
    print(
        "16-class shared-cut/common-cut packet search: "
        f"resolved={resolved_sixteen} unresolved={len(result['final_codes'])}"
    )
    assert resolved_sixteen == 16 and not result["final_codes"]
    by_code = {row[2]: (one, two) for row, one, two in result["certificates"]}
    for index, row in enumerate(result["sixteen"], 1):
        cuts, signature, root_code, root, multiplicity, edges = row
        certificate = by_code[root_code][1]
        status = "UNRESOLVED" if root_code in result["final_codes"] else "RESOLVED"
        print(f"L{index}: {status} c={cuts} root={root.kind}:{root.vertex} positions={multiplicity}")
        print(f"  root-code={root_code}")
        print(f"  incidence={signature}")
        print(f"  edges={edges}")
        if certificate is not None:
            routers, (components, bounds, ledger) = certificate
            sources = " + ".join(format_bound(bound) for bound in bounds)
            print(f"  routers={routers or 'none'} packets={sources}")
            print(f"  ledger={ledger[0]}-{ledger[1]}delta")
        else:
            print("  certificate=no positive established-packet decomposition with <=2 routers")


if __name__ == "__main__":
    main()
