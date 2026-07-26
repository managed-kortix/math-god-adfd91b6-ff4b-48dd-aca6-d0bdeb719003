#!/usr/bin/env python3
"""Conservative last-bridge audit for the disconnected T^6P | P row."""

from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "marked_census", HERE / "octacyclic-t6p-marked-root-incidence-census.py"
)
CENSUS = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CENSUS)


def conservative_split(tree, sacrificed, mark):
    """Cut before P1, then split one triangle, charging a private root interval."""
    if tree.colors[sacrificed] != "T":
        return None
    components = CENSUS.BASE.components_after_split(tree, sacrificed)
    owner = CENSUS.root_component(tree, sacrificed, mark, components)
    mark_count = len(components) + (owner is None)
    if mark_count < 2 or mark_count > 3:
        return None

    bounds = []
    profiles = []
    for component in components:
        triangles, pentagons = CENSUS.component_counts(tree, component)
        profiles.append((triangles, pentagons))
        bounds.append(CENSUS.profile_bound(triangles, pentagons, (tree, component)))

    # The last bridge is already cut, so P1 is a separate unicyclic packet.
    profiles.append((0, 1))
    bounds.append(CENSUS.profile_bound(0, 1))
    # If the connector enters privately on the sacrificed router, its proper
    # interval has no retained cycle and is an acyclic territory of surplus -1.
    if owner is None:
        profiles.append((0, 0))
        bounds.append(CENSUS.Bound(Fraction(-1), False, "private entry interval=-1"))

    total = sum((bound.value for bound in bounds), Fraction(0))
    strict = any(bound.strict for bound in bounds)
    if total > 0 or (total == 0 and strict):
        return tuple(sorted(profiles)), tuple(bounds), total, strict
    return None


def census():
    classes = CENSUS.BASE.enumerate_colors(("P",) + ("T",) * 6, 5)
    failures = []
    resolved = Counter()
    marked = Counter()
    for signature, tree in classes:
        adj = CENSUS.BASE.adjacency(tree)
        pentagon = tree.colors.index("P")
        if len(adj[pentagon]) != 1:
            continue
        cuts = CENSUS.BASE.cut_count(tree)
        for root_signature, mark, positions in CENSUS.root_orbits(tree):
            marked[cuts] += 1
            certificates = tuple(
                (cycle, conservative_split(tree, cycle, mark))
                for cycle, color in enumerate(tree.colors)
                if color == "T"
            )
            certificates = tuple(item for item in certificates if item[1] is not None)
            if certificates:
                resolved[cuts] += 1
            else:
                failures.append((cuts, signature, root_signature, mark, positions, tree.edges))
    failures.sort(key=lambda item: (item[0], item[2]))
    return marked, resolved, failures


def main():
    marked, resolved, failures = census()
    print("marked:", dict(sorted(marked.items())))
    print("resolved:", dict(sorted(resolved.items())))
    print("failed:", len(failures), dict(sorted(Counter(row[0] for row in failures).items())))
    for index, (cuts, signature, root_signature, mark, positions, edges) in enumerate(failures, 1):
        print(f"L{index}: c={cuts} root={mark.kind}:{mark.vertex} positions={positions}")
        print(f"  root-code={root_signature}")
        print(f"  incidence={signature}")
        print(f"  edges={edges}")


if __name__ == "__main__":
    main()
