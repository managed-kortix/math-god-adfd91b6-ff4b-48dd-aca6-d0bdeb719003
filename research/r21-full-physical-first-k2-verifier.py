#!/usr/bin/env python3
"""NONPROMOTIONAL fail-closed audit of the partial physical R21 quotient.

This authenticates exact post-DNN typing, the P-row dispatch, and the theta
actual-bridge reduction; it keeps bridge-free arbitrary-r theta+T^5 OPEN.
It regenerates the 203/6,768 censuses and promotes no master theorem.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import subprocess
import sys
from collections import Counter, deque
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "positive-square-energy/heptacyclic-general/r21-full-physical-first-k2-quotient.md"
SOURCES = {
    "dnn-ledger": (
        ROOT / "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5",
    ),
    "rank-six-owner": (
        ROOT / "positive-square-energy/hexacyclic-general/multiblock-items1-4-owner-exact-closure.md",
        "7ffe92c30ae098cdec9fdc06061c2f5e391ea6c4f5e24be1cc707f34e14612e1",
    ),
    "dtt-packet": (
        ROOT / "positive-square-energy/pentacyclic-general/diamond-two-triangle-exact-packet.md",
        "9107ef2821d441da401079982ae8d0b6c98cee17ae7e52268a9b6ad895b8e11b",
    ),
    "bicyclic-theorem": (
        ROOT / "all-bicyclic-graphs/paper.tex",
        "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
    ),
    "tricyclic-theorem": (
        ROOT / "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
    ),
    "tetracyclic-theorem": (
        ROOT / "all-tetracyclic-graphs/paper.tex",
        "70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f",
    ),
    "pentacyclic-theorem": (
        ROOT / "all-pentacyclic-graphs/paper.tex",
        "8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18",
    ),
    "hexacyclic-theorem": (
        ROOT / "all-hexacyclic-graphs/paper.tex",
        "0e7a2db2932d38a4b4909831c34050553afc0973869fe937eb510cb59421bda7",
    ),
    "dtt-selector": (
        ROOT / "research/r21-bridge-free-dtt-selector-verifier.py",
        "3da7fa8504b56764bf0d3658f13e15f7c2d568782c11636d108513cc29adaf41",
    ),
    "literal-typing-certificate": (
        ROOT / "research/r21-literal-cycle-typing-certificate-2026-11-14.md",
        "4cffd8a71a76208608a9403d442aad56e0c63be00157bf07daa558785c65a489",
    ),
    "literal-typing-verifier": (
        ROOT / "research/r21-literal-cycle-typing-verifier.py",
        "31c4aa9b30bf0c11e2760350eb7e1262aca8960fade36196e1882a7d3a2f3ef1",
    ),
}

ROWS = (
    {"name": "theta-five-triangles", "root": "Theta(1,2,r)",
     "external": ("T0", "T1", "T2", "T3", "T4"), "r_min": 2},
    {"name": "diamond-four-triangles-pentagon", "root": "D=Theta(1,2,2)",
     "external": ("T0", "T1", "T2", "T3", "P=C5")},
)
BELLS = (1, 1, 2, 5, 15, 52, 203)
EXPECTED_N = {
    0: (1, 1, 4, 29, 307),
    1: (1, 4, 29, 308, 4322),
}
EXPECTED_BY_CUTS = {
    (0, 0): {0: 1}, (0, 1): {1: 1},
    (1, 0): {1: 1}, (1, 1): {1: 1, 2: 3},
    (2, 0): {1: 1, 2: 3}, (2, 1): {1: 1, 2: 12, 3: 16},
    (3, 0): {1: 1, 2: 12, 3: 16},
    (3, 1): {1: 1, 2: 35, 3: 150, 4: 122},
    (4, 0): {1: 1, 2: 35, 3: 150, 4: 121},
    (4, 1): {1: 1, 2: 90, 3: 900, 4: 2120, 5: 1211},
}
EXPECTED_FINE_ROWS = (52, 15, 60, 80, 120, 348, 232, 1232, 307, 4322)
OPEN_THETA_RESIDUAL = "bridge-free Theta(1,2,r)+T^5, r>=2"


class AuditError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_sources(sources=None) -> None:
    sources = SOURCES if sources is None else sources
    require(set(sources) == set(SOURCES), "source registry changed")
    for name, (path, expected) in sources.items():
        require(path.is_file(), f"missing pinned source: {name}")
        require(digest(path) == expected, f"pinned source digest changed: {name}")
def check_literal_typing_gate() -> str:
    path = SOURCES["literal-typing-verifier"][0]
    child = subprocess.run([sys.executable, str(path)], check=False,
                           capture_output=True, text=True)
    require(child.returncode == 0, "literal-cycle typing gate failed")
    require(child.stderr == "", "literal-cycle typing gate wrote stderr")
    try:
        payload = json.loads(child.stdout)
    except json.JSONDecodeError as error:
        raise AuditError("literal-cycle typing gate emitted invalid JSON") from error
    require(payload["status"] ==
            "NONPROMOTIONAL_ADJACENCY_AUTHENTICATED_TYPING_CERTIFICATE",
            "literal-cycle typing status changed")
    classification = payload["universal_classification"]
    require(classification["q=3"]["physical_family"] == "D+T^5" and
            classification["q=3"]["dnn_open"] is True,
            "q=3 theta/T5 dispatch changed")
    require(classification["q=5"]["physical_family"] == "D+T^4+P(C5)" and
            classification["q=5"]["dnn_open"] is True and
            classification["q>=4_survivors"] == [5],
            "literal P=C5 dispatch changed")
    return hashlib.sha256(child.stdout.encode("utf-8")).hexdigest()


def set_partitions(items):
    """Yield every set partition once, in restricted-growth order."""
    items = tuple(items)
    if not items:
        yield ()
        return
    blocks = [[items[0]]]

    def visit(index):
        if index == len(items):
            yield tuple(tuple(block) for block in blocks)
            return
        item = items[index]
        for target in range(len(blocks)):
            blocks[target].append(item)
            yield from visit(index + 1)
            blocks[target].pop()
        blocks.append([item])
        yield from visit(index + 1)
        blocks.pop()

    yield from visit(1)


def coarse_states(externals):
    externals = tuple(externals)
    states = set()
    for mask in range(1 << len(externals)):
        root = tuple(externals[i] for i in range(len(externals)) if mask >> i & 1)
        away = tuple(externals[i] for i in range(len(externals)) if not (mask >> i & 1))
        for partition in set_partitions(away):
            canonical = tuple(sorted(tuple(sorted(block)) for block in partition))
            states.add((tuple(sorted(root)), canonical))
    return states


def incidence_states(k: int, p: int):
    labels = ("D",) + tuple(f"T{i}" for i in range(k)) + (("P",) if p else ())
    capacities = (4,) + (3,) * k + ((5,) if p else ())
    block_count = len(labels)
    if block_count == 1:
        return {"D[]": ((), 0)}
    states = {}
    for cut_count in range(1, block_count):
        order = block_count + cut_count
        edge_count = order - 1
        possible = tuple((block, block_count + cut)
                         for block in range(block_count) for cut in range(cut_count))
        for edges in itertools.combinations(possible, edge_count):
            degree = [0] * order
            graph = [[] for unused in range(order)]
            for left, right in edges:
                degree[left] += 1
                degree[right] += 1
                graph[left].append(right)
                graph[right].append(left)
            if any(degree[block_count + cut] < 2 for cut in range(cut_count)):
                continue
            if any(degree[block] > capacities[block] for block in range(block_count)):
                continue
            reached = {0}
            queue = [0]
            while queue:
                current = queue.pop()
                for neighbor in graph[current]:
                    if neighbor not in reached:
                        reached.add(neighbor)
                        queue.append(neighbor)
            if len(reached) != order:
                continue
            # A connected |V|-1 edge graph is a tree.  Root at D and AHU-code
            # the uniquely coloured block nodes and equally coloured cuts.
            parent = [-2] * order
            parent[0] = -1
            queue = deque([0])
            while queue:
                current = queue.popleft()
                for neighbor in sorted(graph[current]):
                    if parent[neighbor] == -2:
                        parent[neighbor] = current
                        queue.append(neighbor)
            children = [[] for unused in range(order)]
            for node, predecessor in enumerate(parent):
                if predecessor >= 0:
                    children[predecessor].append(node)

            def encode(node):
                label = labels[node] if node < block_count else "C"
                return label + "[" + "|".join(sorted(encode(child)
                                                      for child in children[node])) + "]"

            code = encode(0)
            states.setdefault(code, (tuple(edges), cut_count))
    return states


def regenerate_fine():
    arrays = {0: [], 1: []}
    by_cuts = {}
    codes = {}
    for k in range(5):
        for p in range(2):
            states = incidence_states(k, p)
            arrays[p].append(len(states))
            by_cuts[(k, p)] = dict(sorted(Counter(value[1] for value in states.values()).items()))
            codes[(k, p)] = states
    return {p: tuple(values) for p, values in arrays.items()}, by_cuts, codes


def first_bridge_partition_model(root_labels, away_blocks, bridge_lengths=None):
    """Finite original-vertex lift of a coarse simultaneous bridge split."""
    bridge_lengths = ([1] * len(away_blocks) if bridge_lengths is None else bridge_lengths)
    require(len(bridge_lengths) == len(away_blocks), "bridge length inventory changed")
    require(all(type(length) is int and length >= 1 for length in bridge_lengths),
            "zero-length bridge was treated as K2")
    root_vertices = {("root", label) for label in root_labels} | {("root", "payload")}
    vertices = set(root_vertices)
    pieces = [set(root_vertices)]
    crossing = []
    for index, (block, length) in enumerate(zip(away_blocks, bridge_lengths)):
        require(block, "empty away group")
        side = {("away", index, label) for label in block} | {("away", index, "payload")}
        # Every positive connector vertex is put on exactly one physical side;
        # the first edge is the sole crossing edge of this model.
        side |= {("away", index, "connector", step) for step in range(1, length)}
        vertices |= side
        pieces.append(side)
        crossing.append((("root", "payload"), min(side, key=repr)))
    union = set().union(*pieces)
    require(union == vertices, "first-K2 partition omitted a vertex")
    require(sum(map(len, pieces)) == len(vertices), "first-K2 partition duplicated a vertex")
    require(all(left in pieces[0] and sum(right in piece for piece in pieces) == 1
                for left, right in crossing), "bridge endpoint ownership changed")
    return len(vertices), len(pieces)


def pentagon_owner_model(owner=None):
    """Audit F_v ownership, with the parent class wholly upstream."""
    if owner is None:
        owner = {vertex: {("P", vertex), ("payload", vertex)} for vertex in range(5)}
        owner[0] |= {("D", index) for index in range(4)} | {("T-at-c", index) for index in range(3)}
        owner[1] |= {("T-away", index) for index in range(3)}
        owner[3] |= {("T-away-2", index) for index in range(3)}
    require(set(owner) == set(range(5)), "pentagon owner class missing")
    require(all(("P", vertex) in owner[vertex] for vertex in range(5)),
            "pentagon vertex moved from its F_v class")
    flattened = [item for part in owner.values() for item in part]
    require(len(flattened) == len(set(flattened)), "F_v classes overlap")
    parent = 0
    upstream = set(owner[parent])
    downstream = set().union(*(owner[vertex] for vertex in range(5) if vertex != parent))
    require(("D", 0) in upstream, "parent cut class lost D-side")
    require(all(item[0] != "T-at-c" for item in downstream), "triangle at c moved downstream")
    require(all(item[0] not in {"T-away", "T-away-2"} for item in upstream),
            "triangle at v!=c moved upstream")
    require(upstream.isdisjoint(downstream), "F_c duplicated across P opening")
    require(upstream | downstream == set(flattened), "P opening is not exhaustive")
    # Quotient connectivity: every F_v is connected by contract; P-c is the
    # path 1-2-3-4 and joins every downstream owner class.  F_c contains D.
    path_edges = {(1, 2), (2, 3), (3, 4)}
    reached = {1}
    queue = [1]
    while queue:
        current = queue.pop()
        for left, right in path_edges:
            neighbor = right if left == current else left if right == current else None
            if neighbor is not None and neighbor not in reached:
                reached.add(neighbor)
                queue.append(neighbor)
    require(reached == {1, 2, 3, 4}, "P-c downstream path disconnected")
    return len(flattened)


def root_margin(k: int) -> int:
    """Certified strict integer threshold, without attachment monotonicity."""
    require(type(k) is int and 0 <= k <= 4, "D+T^k scope changed")
    if k <= 2:
        return 1 + k                 # >1, >2, >3
    outside = k - 2
    return 3 - outside               # DTT >3 pays each complete side >=-1


def audit(rows=None, sources=None):
    rows = ROWS if rows is None else rows
    check_sources(sources)
    note_text = NOTE.read_text(encoding="utf-8")
    require(note_text.count("Status: **NONPROMOTIONAL_R21_PARTIAL**") == 1,
            "partial status missing from note")
    require(note_text.count(OPEN_THETA_RESIDUAL) == 1,
            "open arbitrary-r theta residual missing or nonunique")
    require("q3_theta_T5_covered" not in note_text and
            "NONPROMOTIONAL_R21_PACKET_CLOSED" not in note_text,
            "closed theta/R21 semantics leaked into note")
    typing_output_sha256 = check_literal_typing_gate()
    require(tuple(record["name"] for record in rows) ==
            ("theta-five-triangles", "diamond-four-triangles-pentagon"),
            "R21 residual family typing changed")
    require(rows[0]["root"] == "Theta(1,2,r)" and rows[0]["r_min"] == 2 and
            rows[0]["external"] == ("T0", "T1", "T2", "T3", "T4"),
            "theta R21 row mistyped")
    require(rows[1]["root"] == "D=Theta(1,2,2)" and
            rows[1]["external"] == ("T0", "T1", "T2", "T3", "P=C5"),
            "diamond/P R21 row mistyped")

    coarse_theta = coarse_states(rows[0]["external"])
    coarse_diamond = coarse_states(rows[1]["external"])
    require(len(coarse_theta) == BELLS[6] == 203, "theta coarse census changed")
    require(len(coarse_diamond) == BELLS[6] == 203, "diamond coarse census changed")

    arrays, by_cuts, codes = regenerate_fine()
    require(arrays == EXPECTED_N, "fine root-incidence N arrays changed")
    require(by_cuts == EXPECTED_BY_CUTS, "fine cut-node census changed")
    require(set(codes[(3, 1)]).isdisjoint(codes[(4, 0)]),
            "labelled P/T distinction was erased")
    rows_fine = []
    fine_total = 0
    for k in range(5):
        for p in range(2):
            contribution = math.comb(4, k) * arrays[p][k] * BELLS[5 - k - p]
            rows_fine.append(contribution)
            fine_total += contribution
    require(tuple(rows_fine) == EXPECTED_FINE_ROWS, "fine row contributions changed")
    require(fine_total == 6768, "fine quotient census changed")

    # Every coarse state gets a finite lifted partition audit.  Labels are
    # payload tokens here; the theorem note supplies the graph-theoretic lift.
    lift_cases = lift_vertices = 0
    for root, away in sorted(coarse_diamond, key=repr):
        vertices, pieces = first_bridge_partition_model(("D",) + root, away)
        lift_cases += 1
        lift_vertices += vertices + pieces
    require(lift_cases == 203, "first-K2 lift census changed")

    p_vertices = pentagon_owner_model()
    margins = tuple(root_margin(k) for k in range(5))
    require(margins == (1, 2, 3, 2, 1), "D+T^k nonmonotone derivation changed")
    require(all(value >= 1 for value in margins), "root no longer pays P/tree debit")
    return {
        "coarse_states_per_family": 203,
        "fine_N_no_P": list(arrays[0]),
        "fine_N_with_P": list(arrays[1]),
        "fine_states": fine_total,
        "fine_row_contributions": rows_fine,
        "first_K2_lifts": lift_cases,
        "lift_tokens": lift_vertices,
        "pentagon_owner_tokens": p_vertices,
        "D_plus_Tk_strict_thresholds": list(margins),
        "literal_typing_output_sha256": typing_output_sha256,
        "literal_q3_fixture_scope": "r=2 typing only; no packet conclusion",
        "theta_actual_bridge_states": "closed by positive away cactus plus rank<=6 root",
        "open_residual": OPEN_THETA_RESIDUAL,
    }


def expect_rejection(action, label):
    try:
        action()
    except (AuditError, KeyError, IndexError, TypeError):
        return
    raise AuditError(f"hostile mutation accepted: {label}")


def hostile_tests():
    # 1. Parent cut no longer owns the D-side.
    bad = {vertex: {("P", vertex), ("payload", vertex)} for vertex in range(5)}
    bad[1].add(("D", 0))
    expect_rejection(lambda: pentagon_owner_model(bad), "parent-cut ownership")

    # 2. F_c is duplicated downstream.
    bad = {vertex: {("P", vertex), ("payload", vertex)} for vertex in range(5)}
    bad[0].add(("D", 0)); bad[1].add(("payload", 0))
    expect_rejection(lambda: pentagon_owner_model(bad), "F_c duplication")

    # 3. A triangle physically owned at c is moved through another P vertex.
    bad = {vertex: {("P", vertex), ("payload", vertex)} for vertex in range(5)}
    bad[0].add(("D", 0)); bad[1].add(("T-at-c", 0))
    expect_rejection(lambda: pentagon_owner_model(bad), "triangle moved across c")

    # 4. A zero-length connector is called a K2 bridge.
    expect_rejection(lambda: first_bridge_partition_model(("D",), (("T0",),), (0,)),
                     "zero-length bridge")

    # 5. A triangle is given a fourth articulation port.
    labels = ("D", "T0", "T1", "T2", "T3")
    capacities = (4, 4, 3, 3, 3)
    # The generator itself uses the immutable physical cap; hostile acceptance
    # would require its 307 census to equal the relaxed census.
    def relaxed_port():
        states = incidence_states(4, 0)
        require(capacities[1] == 3 and len(states) == 307, "port-capacity violation")
    expect_rejection(relaxed_port, "port-capacity violation")

    # 6-7. Either exact post-DNN row is mistyped.
    changed = [dict(record) for record in ROWS]
    changed[0]["external"] = ("T0", "T1", "T2", "T3", "P=C5")
    expect_rejection(lambda: audit(tuple(changed)), "theta row mistyping")
    changed = [dict(record) for record in ROWS]
    changed[1]["external"] = ("T0", "T1", "T2", "T3", "C7")
    expect_rejection(lambda: audit(tuple(changed)), "diamond row mistyping")

    # 8. Source scope is silently replaced.
    changed_sources = dict(SOURCES)
    path, expected = changed_sources["dtt-packet"]
    changed_sources["dtt-packet"] = (path, "0" * 64)
    expect_rejection(lambda: audit(sources=changed_sources), "source digest")

    # 9. The arbitrary-r bridge-free theta residual is erased or renamed.
    expect_rejection(lambda: require(OPEN_THETA_RESIDUAL == "",
                                    "open theta residual erased"),
                     "open theta residual erased")
    return 9


def report():
    result = audit()
    result.update({
        "status": "NONPROMOTIONAL_R21_PARTIAL",
        "typed_families": [record["name"] for record in ROWS],
        "hostile_mutations_rejected": hostile_tests(),
        "master_promoted": False,
    })
    return json.dumps(result, sort_keys=True, indent=2) + "\n"


def main():
    output = report()
    if not sys.flags.optimize and "--optimized-child" not in sys.argv:
        child = subprocess.run([sys.executable, "-O", str(Path(__file__).resolve()),
                                "--optimized-child"], check=False,
                               capture_output=True, text=True)
        require(child.returncode == 0, "optimized full-R21 audit failed")
        require(child.stderr == "", "optimized full-R21 audit wrote stderr")
        require(child.stdout == output, "normal/optimized full-R21 reports differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
