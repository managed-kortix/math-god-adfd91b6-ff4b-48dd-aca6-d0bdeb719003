#!/usr/bin/env python3
"""Exact supporting checks for the favorable-theta plus triangle packet."""

from itertools import combinations

from arbitrary_attached_theta_phase_verifier import ONE, ZERO, matching_partition, variables


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def path_edges(path):
    return list(zip(path, path[1:]))


def theta(lengths):
    paths = []
    next_vertex = 2
    for length in lengths:
        interior = list(range(next_vertex, next_vertex + length - 1))
        next_vertex += length - 1
        paths.append([0] + interior + [1])
    vertices = list(range(next_vertex))
    edges = sum((path_edges(path) for path in paths), [])
    cycles = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        cycle_vertices = frozenset(paths[i] + paths[j])
        cycles.append((cycle_vertices, len(paths[i]) + len(paths[j]) - 2))
    return paths, vertices, edges, cycles


def phase_add(left, right):
    return left[0] + right[0], left[1] + right[1]


def phase_mul(left, right):
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def cycle_factor(length):
    residue = length % 4
    if residue == 0:
        return -2, 0
    if residue == 1:
        return 0, 2
    if residue == 2:
        return 2, 0
    return 0, -2


def psi(vertices, edges, cycles, activities):
    total = (matching_partition(vertices, edges, activities), ZERO)
    for size in range(1, len(cycles) + 1):
        for selected in combinations(cycles, size):
            used = set()
            valid = True
            for cycle_vertices, _ in selected:
                if used.intersection(cycle_vertices):
                    valid = False
                    break
                used.update(cycle_vertices)
            if not valid:
                continue
            retained = [vertex for vertex in vertices if vertex not in used]
            retained_edges = [(u, v) for u, v in edges if u not in used and v not in used]
            term = (matching_partition(retained, retained_edges, activities), ZERO)
            for _, length in selected:
                term = phase_mul(term, cycle_factor(length))
            total = phase_add(total, term)
    return total


def delete_vertex(vertices, edges, cycles, vertex):
    return ([v for v in vertices if v != vertex],
            [(u, v) for u, v in edges if u != vertex and v != vertex],
            [(cycle, length) for cycle, length in cycles if vertex not in cycle])


def check_root(lengths, root, mutation=None):
    paths, h_vertices, h_edges, h_cycles = theta(lengths)
    private = [max(h_vertices) + 1, max(h_vertices) + 2]
    vertices = h_vertices + private
    activities = variables(vertices)
    triangle_edges = [(root, private[0]), (private[0], private[1]), (private[1], root)]
    triangle_cycle = (frozenset((root, private[0], private[1])), 3)
    full = psi(vertices, h_edges + triangle_edges, h_cycles + [triangle_cycle], activities)
    theta_phase = psi(h_vertices, h_edges, h_cycles, activities)
    hm_vertices, hm_edges, hm_cycles = delete_vertex(h_vertices, h_edges, h_cycles, root)
    deleted_phase = psi(hm_vertices, hm_edges, hm_cycles, activities)
    b, c = activities[private[0]], activities[private[1]]
    d = b * c + ONE
    e = b + c
    subtraction = -1 if mutation == "triangle-sign" else -2
    rhs = phase_add(phase_mul((d, ZERO), theta_phase),
                    phase_mul((e, subtraction * ONE), deleted_phase))
    if mutation == "root-duplication":
        rhs = phase_add(rhs, (activities[root] * deleted_phase[0],
                              activities[root] * deleted_phase[1]))
    identity = full == rhs
    signs = (deleted_phase[0].nonnegative() and deleted_phase[0] != ZERO
             and (-deleted_phase[1]).nonnegative()
             and (-full[1]).nonnegative() and full[1] != ZERO)
    return identity and signs


def run(mutation=None):
    for lengths in ((3, 4, 4), (4, 3, 3)):
        paths, _, _, _ = theta(lengths)
        roots = (0, paths[0][1], paths[1][1], paths[2][1])
        if not all(check_root(lengths, root, mutation) for root in roots):
            return False
    return True


def main():
    require(run(), "canonical favorable-theta triangle packet failed")
    mutations = ("triangle-sign", "root-duplication")
    rejected = sum(not run(mutation) for mutation in mutations)
    require(rejected == len(mutations), "a hostile packet mutation survived")
    print(
        "favorable theta plus triangle shared-cut verifier: PASS "
        f"(root-cases=8, mutations={rejected}/{len(mutations)})"
    )


if __name__ == "__main__":
    main()
