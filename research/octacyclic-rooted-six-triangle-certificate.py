#!/usr/bin/env python3
"""Exact marked-root census for a rooted six-triangle shared cluster.

This is a structural certificate, not a spectral numerical experiment.  It
enumerates color-preserving cycle-cut incidence trees, every possible cyclic
root orbit, and finite packet decompositions used by the accompanying proof.
All packet margins are integers and all assertions are exact.
"""

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations


@dataclass(frozen=True)
class Tree:
    edges: tuple[tuple[int, int], ...]


def adjacency(tree):
    answer = [[] for _ in range(len(tree.edges) + 1)]
    for left, right in tree.edges:
        answer[left].append(right)
        answer[right].append(left)
    return answer


def centers(adj):
    degree = [len(row) for row in adj]
    leaves = [vertex for vertex, value in enumerate(degree) if value <= 1]
    remaining = len(adj)
    while remaining > 2:
        remaining -= len(leaves)
        new_leaves = []
        for leaf in leaves:
            for neighbor in adj[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    new_leaves.append(neighbor)
        leaves = new_leaves
    return leaves


def rooted_code(adj, vertex, parent, cycle_count, marked_root=None):
    if vertex < cycle_count:
        color = "R" if marked_root == ("private", vertex) else "T"
    else:
        color = "Y" if marked_root == ("cut", vertex) else "X"
    children = sorted(
        rooted_code(adj, neighbor, vertex, cycle_count, marked_root)
        for neighbor in adj[vertex]
        if neighbor != parent
    )
    return color + "(" + "".join(children) + ")"


def signature(tree, cycle_count, marked_root=None):
    adj = adjacency(tree)
    return min(
        rooted_code(adj, center, -1, cycle_count, marked_root)
        for center in centers(adj)
    )


def lift(tree, cycle_count):
    base = tuple(sorted((cycle, cut + 1) for cycle, cut in tree.edges))
    cut_labels = sorted({cut for _, cut in base})
    for cut in cut_labels:
        yield Tree(tuple(sorted(base + ((cycle_count, cut),))))
    new_cut = max(cut_labels, default=cycle_count) + 1
    degrees = Counter(cycle for cycle, _ in base)
    for cycle in range(cycle_count):
        if degrees[cycle] < 3:
            yield Tree(
                tuple(sorted(base + ((cycle_count, new_cut), (cycle, new_cut))))
            )


@lru_cache(maxsize=None)
def enumerate_trees(cycle_count):
    if cycle_count == 1:
        tree = Tree(())
        return ((signature(tree, cycle_count), tree),)
    if cycle_count == 2:
        tree = Tree(((0, 2), (1, 2)))
        return ((signature(tree, cycle_count), tree),)
    classes = {}
    for _, old_tree in enumerate_trees(cycle_count - 1):
        for tree in lift(old_tree, cycle_count - 1):
            classes.setdefault(signature(tree, cycle_count), tree)
    return tuple(sorted(classes.items()))


def root_orbits(tree, cycle_count):
    adj = adjacency(tree)
    roots = [("cut", cut) for cut in range(cycle_count, len(adj))]
    roots.extend(
        ("private", cycle)
        for cycle in range(cycle_count)
        if len(adj[cycle]) < 3
    )
    classes = {}
    for root in roots:
        classes.setdefault(signature(tree, cycle_count, root), root)
    return tuple(sorted(classes.items()))


def labelled_root_positions(tree, cycle_count):
    adj = adjacency(tree)
    cut_positions = len(adj) - cycle_count
    private_positions = sum(3 - len(adj[cycle]) for cycle in range(cycle_count))
    return cut_positions + private_positions


def triangles_meet(adj, cycle_count, left, right):
    return any(
        left in adj[cut] and right in adj[cut]
        for cut in range(cycle_count, len(adj))
    )


def components(adj, cycle_count, vertices):
    todo = set(vertices)
    answer = []
    while todo:
        stack = [todo.pop()]
        component = set(stack)
        while stack:
            cycle = stack.pop()
            for cut in adj[cycle]:
                for neighbor in adj[cut]:
                    if neighbor in todo:
                        todo.remove(neighbor)
                        component.add(neighbor)
                        stack.append(neighbor)
        answer.append(frozenset(component))
    return tuple(answer)


TRIANGLE_MARGIN = {1: 0, 2: 1, 3: 2, 4: 3, 5: 2, 6: 1}


SECOND_STAGE = {
    (
        ((0, 6), (0, 7), (1, 6), (2, 7), (3, 6), (4, 6), (5, 7)),
        ("private", 0),
    ): ("private-root split", ((1, 3, 4), (2, 5)), 3),
    (
        ((0, 6), (0, 7), (1, 6), (1, 8), (2, 7), (3, 6), (4, 7), (5, 8)),
        ("private", 0),
    ): ("private-root split", ((1, 3, 5), (2, 4)), 3),
    (
        ((0, 6), (0, 7), (1, 6), (1, 8), (2, 7), (3, 6), (3, 9), (4, 8), (5, 9)),
        ("private", 0),
    ): ("private-root split", ((1, 3, 4, 5), (2,)), 3),
    (
        ((0, 6), (0, 7), (1, 6), (1, 8), (2, 7), (3, 6), (3, 9), (4, 8), (5, 9)),
        ("cut", 6),
    ): ("one-arm hostile packet", ((0, 2), (1, 4), (3, 5)), 2),
}


def certificate(tree, cycle_count, root):
    adj = adjacency(tree)
    all_triangles = set(range(cycle_count))
    candidates = []
    for size in range(1, cycle_count + 1):
        for packet_tuple in combinations(range(cycle_count), size):
            packet = frozenset(packet_tuple)
            if not all(
                triangles_meet(adj, cycle_count, left, right)
                for left, right in combinations(packet, 2)
            ):
                continue
            if root[0] == "private" and root[1] not in packet:
                continue
            if root[0] == "cut" and not packet.intersection(adj[root[1]]):
                continue

            packet_cuts = {cut for cycle in packet for cut in adj[cycle]}
            sacrificed = {
                cycle
                for cut in packet_cuts
                for cycle in adj[cut]
                if cycle < cycle_count and cycle not in packet
            }
            retained = all_triangles - packet - sacrificed
            retained_components = components(adj, cycle_count, retained)

            component_owner = {
                cycle: index
                for index, component in enumerate(retained_components)
                for cycle in component
            }
            valid = True
            terminal_sacrifices = 0
            for cycle in sacrificed:
                inward_cuts = []
                outward_owners = []
                for cut in adj[cycle]:
                    other_triangles = {
                        neighbor
                        for neighbor in adj[cut]
                        if neighbor < cycle_count and neighbor != cycle
                    }
                    if other_triangles.intersection(packet):
                        inward_cuts.append(cut)
                    if other_triangles.intersection(sacrificed):
                        valid = False
                    outward_owners.extend(
                        {
                            component_owner[neighbor]
                            for neighbor in other_triangles
                            if neighbor in component_owner
                        }
                    )
                if len(inward_cuts) != 1:
                    valid = False
                if len(outward_owners) != len(set(outward_owners)):
                    valid = False
                if not outward_owners:
                    terminal_sacrifices += 1
            if not valid:
                continue

            margin = len(packet) - terminal_sacrifices + sum(
                TRIANGLE_MARGIN[len(component)]
                for component in retained_components
            )
            candidates.append(
                (margin, packet, frozenset(sacrificed), retained_components)
            )
    if not candidates:
        return None
    return max(candidates, key=lambda item: (item[0], -len(item[1]), item[1]))


def packing_number(adj, cycle_count, cycles):
    return max(
        len(selected)
        for size in range(len(cycles) + 1)
        for selected in combinations(cycles, size)
        if all(
            not triangles_meet(adj, cycle_count, left, right)
            for left, right in combinations(selected, 2)
        )
    )


def verify_second_stage(tree, root):
    method, groups, margin = SECOND_STAGE[(tree.edges, root)]
    adj = adjacency(tree)
    if method == "private-root split":
        assert root == ("private", 0)
        assert set().union(*(set(group) for group in groups)) == set(range(1, 6))
        owners = {cycle: owner for owner, group in enumerate(groups) for cycle in group}
        for cut in range(6, len(adj)):
            remaining = [cycle for cycle in adj[cut] if cycle != 0]
            assert len({owners[cycle] for cycle in remaining}) <= 1
        assert all(packing_number(adj, 6, group) <= 2 for group in groups)
        assert sum(len(group) - 1 for group in groups) == margin
    else:
        assert root == ("cut", 6)
        assert groups == ((0, 2), (1, 4), (3, 5))
        assert triangles_meet(adj, 6, 0, 2)
        assert triangles_meet(adj, 6, 1, 4)
        assert triangles_meet(adj, 6, 3, 5)
        assert margin == 2
    return method, groups, margin


def main():
    cycle_count = 6
    trees = enumerate_trees(cycle_count)
    marked = []
    positions = 0
    margins = Counter()
    residual = []
    for tree_code, tree in trees:
        positions += labelled_root_positions(tree, cycle_count)
        for root_code, root in root_orbits(tree, cycle_count):
            cert = certificate(tree, cycle_count, root)
            marked.append((tree_code, root_code, root, cert))
            if cert is None or cert[0] < 1:
                residual.append((tree_code, root_code, tree.edges, root, cert))
            else:
                margins[cert[0]] += 1

    assert len(trees) == 19
    assert len(marked) == 111
    assert positions == 247
    assert len(residual) == 4
    assert {(edges, root) for _, _, edges, root, _ in residual} == set(SECOND_STAGE)
    assert sum(margins.values()) == 107
    assert margins == Counter({4: 58, 3: 28, 2: 14, 1: 5, 6: 2})
    print("unmarked incidence trees:", len(trees))
    print("marked cyclic-root orbits:", len(marked))
    print("labelled cyclic-root positions:", positions)
    print("certified marked orbits:", sum(margins.values()))
    print("certificate margins:", dict(sorted(margins.items())))
    print("exact residual marked orbits:", len(residual))
    for tree_code, root_code, edges, root, cert in residual:
        best = None if cert is None else cert[0]
        print(f"  {root_code} root={root} best={best} edges={edges}")
        method, groups, margin = verify_second_stage(Tree(edges), root)
        print(f"    second-stage={method} groups={groups} integer-margin={margin}")


if __name__ == "__main__":
    main()
