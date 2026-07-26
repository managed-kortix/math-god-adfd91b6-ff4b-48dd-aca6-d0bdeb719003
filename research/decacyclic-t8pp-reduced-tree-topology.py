#!/usr/bin/env python3
"""Exhaustive reduced-tree topology census for the ten structural T^8PP rows.

Cluster interiors are abstract.  A reduced tree has colored cluster vertices and
uncolored Steiner vertices; Steiner vertices have degree at least three and
every leaf is a cluster.  The generator is finite because a tree with k marked
clusters has at most k-2 Steiner vertices.
"""

from collections import Counter


ROWS = (
    ((0, 1), (0, 1)) + ((1, 0),) * 8,
    ((0, 1), (0, 1), (1, 0), (7, 0)),
    ((0, 1), (0, 1), (8, 0)),
    ((0, 1),) + ((1, 0),) * 6 + ((2, 1),),
    ((0, 1),) + ((1, 0),) * 5 + ((3, 1),),
    ((0, 1),) + ((1, 0),) * 4 + ((4, 1),),
    ((0, 1),) + ((1, 0),) * 3 + ((5, 1),),
    ((0, 1),) + ((1, 0),) * 2 + ((6, 1),),
    ((0, 1), (1, 0), (7, 1)),
    ((0, 1), (8, 1)),
)

EXPECTED_SHAPES = {2: 1, 3: 2, 4: 5, 5: 12, 6: 37, 7: 116, 8: 412, 10: 5995}
EXPECTED_COLORED = (142805, 19, 3, 10727, 2156, 439, 90, 19, 4, 1)
EXPECTED_EXCLUSIVE = (
    Counter({"leaf": 142804, "terminal_tp": 1}),
    Counter({"leaf": 18, "terminal_tp": 1}),
    Counter({"leaf": 2, "p_a8_p": 1}),
    Counter({"leaf": 10726, "terminal_tp": 1}),
    Counter({"leaf": 2155, "terminal_tp": 1}),
    Counter({"leaf": 438, "terminal_tp": 1}),
    Counter({"leaf": 89, "terminal_tp": 1}),
    Counter({"leaf": 18, "terminal_tp": 1}),
    Counter({"leaf": 3, "terminal_tp": 1}),
    Counter({"t8p_p": 1}),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def adjacency(edges, order):
    adj = [set() for _ in range(order)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def centers(edges, order):
    adj = adjacency(edges, order)
    degree = [len(row) for row in adj]
    leaves = [v for v, value in enumerate(degree) if value <= 1]
    remaining = order
    while remaining > 2:
        next_leaves = []
        remaining -= len(leaves)
        for leaf in leaves:
            for neighbor in adj[leaf]:
                degree[neighbor] -= 1
                if degree[neighbor] == 1:
                    next_leaves.append(neighbor)
        leaves = next_leaves
    return tuple(sorted(leaves))


def canonical_code(edges, colors):
    order = len(colors)
    adj = adjacency(edges, order)

    def rooted(vertex, parent):
        children = sorted(rooted(child, vertex) for child in adj[vertex] if child != parent)
        return f"({colors[vertex]}{''.join(children)})"

    return min(rooted(center, -1) for center in centers(edges, order))


def reduced_shapes(cluster_count):
    """Generate uncolored reduced trees by adding a marked leaf.

    Attaching to a vertex or subdividing an edge is inverse to deleting a
    marked leaf and suppressing a resulting degree-two Steiner vertex.  This
    proves generation completeness by induction.
    """
    states = {"(M)": ((), ("M",))}
    for _ in range(1, cluster_count):
        next_states = {}
        for edges, colors in states.values():
            order = len(colors)
            candidates = []
            for vertex in range(order):
                candidates.append((edges + ((min(vertex, order), max(vertex, order)),), colors + ("M",)))
            for edge_index, (u, v) in enumerate(edges):
                steiner = order
                leaf = order + 1
                replaced = edges[:edge_index] + edges[edge_index + 1 :]
                new_edges = replaced + (
                    (min(u, steiner), max(u, steiner)),
                    (min(v, steiner), max(v, steiner)),
                    (steiner, leaf),
                )
                candidates.append((new_edges, colors + ("S", "M")))
            for new_edges, new_colors in candidates:
                new_edges = tuple(sorted(new_edges))
                code = canonical_code(new_edges, new_colors)
                next_states.setdefault(code, (new_edges, new_colors))
        states = next_states
    return tuple(states.values())


def colorings(shape, parts):
    edges, kinds = shape
    marked = tuple(v for v, kind in enumerate(kinds) if kind == "M")
    distinct = sorted(set(parts))
    remaining = Counter(parts)
    colors = ["S" if kind == "S" else None for kind in kinds]
    answer = {}

    def visit(index):
        if index == len(marked):
            code = canonical_code(edges, tuple(colors))
            answer.setdefault(code, (edges, tuple(colors)))
            return
        vertex = marked[index]
        for part in distinct:
            if remaining[part]:
                remaining[part] -= 1
                colors[vertex] = f"C{part[0]},{part[1]}"
                visit(index + 1)
                remaining[part] += 1

    visit(0)
    return answer


def part(color):
    if color == "S":
        return None
    triangles, pentagons = color[1:].split(",")
    return int(triangles), int(pentagons)


def is_path(adj):
    return max(map(len, adj), default=0) <= 2


def certificates(tree):
    edges, colors = tree
    adj = adjacency(edges, len(colors))
    clusters = [v for v, color in enumerate(colors) if color != "S"]
    leaves = [v for v in clusters if len(adj[v]) == 1]
    singleton_rank9 = [v for v in leaves if part(colors[v]) == (1, 0)]
    triangular_leaf = [
        v for v in leaves
        if part(colors[v])[1] == 0 and 10 - part(colors[v])[0] >= 2
    ]

    terminal_tp = []
    for endpoint in leaves:
        if part(colors[endpoint]) != (0, 1):
            continue
        neighbor = next(iter(adj[endpoint]))
        if colors[neighbor] != "S" and part(colors[neighbor]) == (1, 0) and len(adj[neighbor]) == 2:
            terminal_tp.append((endpoint, neighbor))

    no_steiner = all(color != "S" for color in colors)
    cluster_parts = Counter(part(colors[v]) for v in clusters)
    t8p_p = no_steiner and len(colors) == 2 and cluster_parts == Counter({(8, 1): 1, (0, 1): 1})
    p_a8_p = (
        no_steiner and len(colors) == 3 and is_path(adj)
        and cluster_parts == Counter({(0, 1): 2, (8, 0): 1})
        and all(part(colors[v]) == (0, 1) for v in leaves)
    )
    p_leaves = all(part(colors[v])[1] > 0 for v in leaves)
    return {
        "rank9_leaf": bool(singleton_rank9),
        "triangular_leaf": bool(triangular_leaf),
        "terminal_tp": bool(terminal_tp),
        "t8p_p": t8p_p,
        "p_a8_p": p_a8_p,
        "path_p_ends": is_path(adj) and p_leaves,
    }


def row_name(row):
    def name(value):
        triangles, pentagons = value
        return ("T" if triangles == 1 else (f"T^{triangles}" if triangles else "")) + ("P" * pentagons)
    return "|".join(name(value) for value in row)


def validate_tree(tree, expected_parts):
    edges, colors = tree
    adj = adjacency(edges, len(colors))
    require(len(edges) == len(colors) - 1, "wrong tree edge count")
    require(Counter(part(color) for color in colors if color != "S") == Counter(expected_parts), "wrong colors")
    require(all(len(adj[v]) >= 3 for v, color in enumerate(colors) if color == "S"), "unreduced Steiner vertex")
    require(all(colors[v] != "S" for v in range(len(colors)) if len(adj[v]) == 1), "Steiner leaf")
    steiners = sum(color == "S" for color in colors)
    require(steiners <= len(expected_parts) - 2, "Steiner bound violated")


def main():
    shape_cache = {}
    global_counterexample = None
    for index, row in enumerate(ROWS, 1):
        k = len(row)
        shapes = shape_cache.setdefault(k, reduced_shapes(k))
        classes = {}
        for shape in shapes:
            classes.update(colorings(shape, row))
        for tree in classes.values():
            validate_tree(tree, row)

        require(len(shapes) == EXPECTED_SHAPES[k], f"row {index} shape count changed")
        require(len(classes) == EXPECTED_COLORED[index - 1], f"row {index} colored count changed")

        counts = Counter()
        exclusive = Counter()
        failures = []
        narrow_failures = []
        for code, tree in sorted(classes.items()):
            cert = certificates(tree)
            for label, present in cert.items():
                counts[label] += int(present)
            broad = cert["triangular_leaf"] or cert["path_p_ends"]
            closed = cert["triangular_leaf"] or cert["terminal_tp"] or cert["t8p_p"] or cert["p_a8_p"]
            if not broad or not closed:
                failures.append((code, cert))
            narrow = cert["rank9_leaf"] or cert["t8p_p"] or cert["p_a8_p"]
            if not narrow:
                narrow_failures.append((code, cert))
            if cert["triangular_leaf"]:
                exclusive["leaf"] += 1
            elif cert["terminal_tp"]:
                exclusive["terminal_tp"] += 1
            elif cert["t8p_p"]:
                exclusive["t8p_p"] += 1
            elif cert["p_a8_p"]:
                exclusive["p_a8_p"] += 1
            else:
                exclusive["unclassified"] += 1
        require(not failures, f"row {index} has unclassified topology: {failures[:1]}")
        require(exclusive == EXPECTED_EXCLUSIVE[index - 1], f"row {index} outcome counts changed: {exclusive}")
        if global_counterexample is None and narrow_failures:
            global_counterexample = (index, narrow_failures[0])

        print(
            f"R{index:02d} {row_name(row)}: clusters={k} shapes={len(shapes)} colored={len(classes)} "
            f"rank9-leaf={counts['rank9_leaf']} broad-T-leaf={counts['triangular_leaf']} "
            f"terminal-TP={counts['terminal_tp']} T8P|P={counts['t8p_p']} "
            f"P|A8|P={counts['p_a8_p']} exclusive={dict(exclusive)} narrow-fail={len(narrow_failures)}"
        )

    require(global_counterexample is not None, "expected the narrow dichotomy to fail")
    index, (code, cert) = global_counterexample
    print(f"COUNTEREXAMPLE narrow rank9-leaf/kernel claim: row=R{index:02d} code={code} certificates={cert}")
    print("PASS: exhaustive reduced-tree lemma and strict endpoint classification")


if __name__ == "__main__":
    main()
