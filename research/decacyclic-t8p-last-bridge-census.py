#!/usr/bin/env python3
"""Exact marked-entry census for the decacyclic T^8P | P endpoint."""

from collections import Counter
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


spec = spec_from_file_location("rank9_last_bridge", HERE / "nonacyclic-t7p-last-bridge-conservative.py")
base = module_from_spec(spec)
require(spec.loader is not None, "cannot load last-bridge dependency")
sys.modules[spec.name] = base
spec.loader.exec_module(base)

base.TRIANGLE_MARGIN[8] = 0


def census():
    classes = base.BASE.enumerate_colors(("P",) + ("T",) * 8, 5)
    all_counts = Counter(base.BASE.cut_count(tree) for _, tree in classes)
    leaf_counts = Counter()
    marked = Counter()
    direct = Counter()
    replacements = Counter()
    replacement_sizes = Counter()
    failures = []
    for signature, tree in classes:
        adj = base.BASE.adjacency(tree)
        pentagon = tree.colors.index("P")
        if len(adj[pentagon]) != 1:
            continue
        cuts = base.BASE.cut_count(tree)
        leaf_counts[cuts] += 1
        for root_code, mark, multiplicity in base.root_orbits(tree):
            marked[cuts] += 1
            certificates = tuple(
                base.conservative_split(tree, cycle, mark)
                for cycle, color in enumerate(tree.colors) if color == "T"
            ) + tuple(
                base.private_entry_uncut_split(tree, cycle, mark)
                for cycle, color in enumerate(tree.colors) if color == "T"
            )
            if any(item is not None for item in certificates):
                direct[cuts] += 1
                continue
            replacement = base.best_deletion_certificate(tree, mark)
            if replacement is not None:
                base.validate_deletion_owners(replacement)
                replacements[cuts] += 1
                replacement_sizes[len(replacement.order)] += 1
            else:
                failures.append((cuts, signature, root_code, mark, multiplicity, tree))
    return all_counts, leaf_counts, marked, direct, replacements, replacement_sizes, failures


def close_failures(failures):
    require(len(failures) == 3, failures)
    common_signature = "T(X(P())X(T()T()T()T()T()T()T()))"
    require({item[1] for item in failures} == {common_signature}, "failures do not share the expected kernel")
    repairs = []
    for _, _, _, mark, _, tree in failures:
        adj = base.BASE.adjacency(tree)
        router = next(c for c, color in enumerate(tree.colors) if color == "T" and len(adj[c]) == 2)
        hub_cut = next(cut for cut in adj[router] if len(adj[cut]) == 8)
        pentagon_cut = next(cut for cut in adj[router] if cut != hub_cut)
        if mark.kind == "cut" and mark.vertex == pentagon_cut:
            repairs.append(("split router: A_7 + PP", "strict >0"))
        elif mark.kind == "cut" and mark.vertex == hub_cut:
            require(base.exact_sign(7, 2) > 0, "7-2delta is not positive")
            repairs.append(("split router: P + packing-one A_7P", ">7-2delta"))
        else:
            require(mark.kind == "private" and mark.vertex == router, "unexpected failed mark")
            require(base.exact_sign(7, 1) > 0, "7-delta is not positive")
            repairs.append(("open remote P; retain packing-one T^8P", ">7-delta"))
    return repairs


def main():
    all_counts, leaf_counts, marked, direct, replacements, replacement_sizes, failures = census()
    repairs = close_failures(failures)
    require(all_counts == Counter({1: 1, 2: 11, 3: 68, 4: 258, 5: 589, 6: 781, 7: 536, 8: 148}), all_counts)
    require(leaf_counts == Counter({1: 1, 2: 7, 3: 42, 4: 142, 5: 301, 6: 354, 7: 212, 8: 46}), leaf_counts)
    require(sum(marked.values()) == 11689, marked)
    require(sum(direct.values()) == 11586, direct)
    require(sum(replacements.values()) == 100, replacements)
    require(replacement_sizes == Counter({0: 2, 1: 9, 2: 73, 3: 16}), replacement_sizes)
    require(sum(direct.values()) + sum(replacements.values()) + len(repairs) == sum(marked.values()), "census does not close")
    print("all T^8P incidence trees:", dict(sorted(all_counts.items())), "total", sum(all_counts.values()))
    print("P-leaf incidence trees:", dict(sorted(leaf_counts.items())), "total", sum(leaf_counts.values()))
    print("marked entry classes:", dict(sorted(marked.items())), "total", sum(marked.values()))
    print("direct one-router:", sum(direct.values()))
    print("finite replacements:", sum(replacements.values()), dict(sorted(replacement_sizes.items())))
    print("explicit openings/repairs:", len(repairs))
    for index, repair in enumerate(repairs, 1):
        print(f"F{index}: {repair[0]}; {repair[1]}")
    print("closed marked classes:", sum(marked.values()), "of", sum(marked.values()))


if __name__ == "__main__":
    main()
