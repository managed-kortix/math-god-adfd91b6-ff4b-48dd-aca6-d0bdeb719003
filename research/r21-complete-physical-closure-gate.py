#!/usr/bin/env python3
"""NONPROMOTIONAL fail-closed gate for the corrected complete physical R21 note.

This is an authentication and semantic-composition gate, not a machine proof of
all universal analytic lemmas in the note.  It:

* binds an immutable canonical name -> (resolved path, SHA-256) registry;
* authenticates the corrected complete note itself and its narrow scope;
* replays the adjacency typing/ownership parent, literal typing, DTT selector,
  and exact DTT packet executables;
* derives the retained-C5 owner split and first-bridge away-group typing from
  materialized adjacency, including shared-cut, mixed-C5/triangle, and rooted
  payload fixtures; and
* fails closed in strict executable-promotion mode because four rigorous,
  authenticated prose kernels have no executable universal replay here.

It never reads labels or lane metadata as graph evidence and never promotes or
modifies STATE, a theorem master, publication state, or another lane.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType, ModuleType
from typing import Callable, Mapping


ROOT = Path(__file__).resolve().parents[1]
NOTE_REL = "positive-square-energy/heptacyclic-general/r21-complete-physical-closure.md"
SCHEMA = "r21-complete-physical-closure-gate/v1"
STRICT_FLAG = "--strict-executable-promotion"
OPTIMIZED_FLAG = "--optimized-child"


class GateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


@dataclass(frozen=True)
class SourcePin:
    relative_path: str
    sha256: str
    role: str


# The canonical registry is deliberately module-private, immutable, and keyed
# by semantic role.  check_sources accepts no caller mapping.  Equality below
# is over role, resolved absolute path, and expected digest, so neither a role
# swap nor a self-hash substitution can pass merely by preserving the key set.
_CANONICAL_SOURCE_PINS = MappingProxyType({
    "corrected-complete-note": SourcePin(
        NOTE_REL,
        "c1175db74866fdc03551ffc9081596147acbe14b1d60f6a6e016c8788aa04860",
        "corrected complete R21 proof note",
    ),
    "adjacency-parent-gate": SourcePin(
        "research/r21-adjacency-parent-gate-verifier.py",
        "5cec3e9f35bdbac5ad857e5a82fed49b3f4513a55f4ad2f467ac8e9e156321bc",
        "adjacency/Tarjan typing and owner semantics",
    ),
    "literal-cycle-typing": SourcePin(
        "research/r21-literal-cycle-typing-verifier.py",
        "31c4aa9b30bf0c11e2760350eb7e1262aca8960fade36196e1882a7d3a2f3ef1",
        "literal D+4T+Cq typing and exact DNN survivor arithmetic",
    ),
    "dtt-selector": SourcePin(
        "research/r21-bridge-free-dtt-selector-verifier.py",
        "3da7fa8504b56764bf0d3658f13e15f7c2d568782c11636d108513cc29adaf41",
        "exhaustive bridge-free D+4T DTT selector",
    ),
    "dtt-packet": SourcePin(
        "research/diamond-two-triangle-packet-verifier.py",
        "24da5324c6695de4795fbd7885fbeadf986fabe1b52e2aec2082c92223addc9a",
        "exact executable D+T+T spectral packet",
    ),
    "dnn-ledger": SourcePin(
        "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5",
        "exact R21 DNN residual registry",
    ),
    "triangular-cactus-proof": SourcePin(
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "maximum-cycle-packing Voronoi territories and packing-one Sachs sign",
    ),
    "six-triangle-recurrence-proof": SourcePin(
        "all-heptacyclic-cacti/paper.tex",
        "9323dc212d36b610a66e890df3a267242ae0800efcd445dd911575cc2bd9a4d1",
        "A4 base, A5/A6 incidence-leaf recurrence, and connector territories",
    ),
    "four-five-triangle-kernel": SourcePin(
        "research/five-triangle-shared-cluster-surplus-2026-07-26.md",
        "08e3e9dd69e57de951ff8941d8a31c0a5c3995a661ecfdd103303e11615b4fae",
        "central-triangle/three-petal injection and first leaf opening",
    ),
    "hostile-c5-proof": SourcePin(
        "all-tricyclic-cacti/paper.tex",
        "d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8",
        "tree elimination, weighted-cycle phase domination, and bare C5 spectrum",
    ),
    "nonunicyclic-cactus-theorem": SourcePin(
        "all-nonunicyclic-cacti/paper.tex",
        "26939326e2ad71062617503e106dbd46d99f3d8fe82a98fca858fd3f2f8323f9",
        "strict theorem for every finite simple connected cactus of rank at least two",
    ),
    "historical-partial-note": SourcePin(
        "positive-square-energy/heptacyclic-general/r21-full-physical-first-k2-quotient.md",
        "bff7c46d1af5d718ff5e666adf68b49b98631633c6a0436b7a51fca6eec8a413",
        "historical NONPROMOTIONAL_R21_PARTIAL note; never a closure input",
    ),
    "historical-partial-verifier": SourcePin(
        "research/r21-full-physical-first-k2-verifier.py",
        "6d692e7a1acc5fb1d8487eeac6761154b4556aa535f904596db0edb874f39beb",
        "historical NONPROMOTIONAL_R21_PARTIAL verifier; never a closure input",
    ),
})


def _canonical_registry() -> tuple[tuple[str, str, str, str], ...]:
    return tuple(
        (name, str((ROOT / pin.relative_path).resolve(strict=False)),
         pin.sha256, pin.role)
        for name, pin in _CANONICAL_SOURCE_PINS.items()
    )


_CANONICAL_REGISTRY_LOCK = _canonical_registry()
require(len(_CANONICAL_REGISTRY_LOCK) == len(set(_CANONICAL_REGISTRY_LOCK)),
        "canonical source registry contains duplicate records")
require(len({name for name, unused_path, unused_digest, unused_role
             in _CANONICAL_REGISTRY_LOCK}) == len(_CANONICAL_REGISTRY_LOCK),
        "canonical source registry contains duplicate semantic names")
require(len({path for unused_name, path, unused_digest, unused_role
             in _CANONICAL_REGISTRY_LOCK}) == len(_CANONICAL_REGISTRY_LOCK),
        "canonical source registry aliases two roles to one path")


_SOURCE_TOKENS = MappingProxyType({
    "corrected-complete-note": (
        "Status: **NONPROMOTIONAL_AUTHENTICATED_PROOF_NOTE**",
        "Thus both exact post-DNN residual families are strict.",
        "the whole `R21` block partition is\nclosed",
        "rigorous_prose_authenticated_not_executable_universal_replay",
        "A=R[V(F_c)]",
        "B'=R[union_(w!=c) V(F_w)]",
        "Separate the unique away group containing `P`",
        "connected cactus of rank\n`q+1 in {2,3,4,5}`",
        "no mixed `P`-plus-triangle away group is ever called\ntriangular",
        "expanded incidence\nsubtrees",
        "its **cut closure**",
    ),
    "triangular-cactus-proof": (
        r"\begin{lemma}[Cycle territories]\label{lem:cycle-territories}",
        r"\begin{corollary}[Triangular block graphs]\label{cor:triangular-block}",
        "Here triangular means that every cyclic block is a triangle; bridge blocks",
    ),
    "six-triangle-recurrence-proof": (
        r"\begin{lemma}[Shared-triangle recurrence]\label{lem:triangle-recurrence}",
        r"\sig(A_5)>2", r"\sig(A_6)>1",
    ),
    "four-five-triangle-kernel": (
        "Lemma 3 (four-triangle shared cluster).",
        "Thus `T0` is a central\ntriangle and `T1,T2,T3` are its three pairwise disjoint petals.",
        "Lemma 4 (one leaf opening).",
    ),
    "hostile-c5-proof": (
        r"Q_{u\to p}=\frac{Z_{T_{u\to p}}(t)}{Z_{T_{u\to p}-u}(t)}",
        r"s^+(U_5)\geq u-\delta_5",
        r"\delta_5=\sec(\pi/5)-1=\sqrt5-2",
    ),
    "nonunicyclic-cactus-theorem": (
        r"\begin{theorem}\label{thm:main}",
        "Every finite simple connected cactus $G$ of cyclomatic rank $k\\geq2$ satisfies",
        r"\boxed{\splus(G)>|V(G)|}",
        "Both inputs permit arbitrary shared cuts, bridge connectors, cactus incidence,",
        "and finite tree attachments.",
    ),
    "historical-partial-note": (
        "Status: **NONPROMOTIONAL_R21_PARTIAL**",
        "bridge-free `Theta(1,2,r)+T^5` endpoint as **OPEN**",
    ),
})


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_sources() -> dict[str, dict[str, object]]:
    """Authenticate exactly the immutable canonical registry.

    There is intentionally no ``sources`` parameter.  Reconstructing the
    observed registry from the immutable pins and demanding exact tuple
    equality binds semantic name, resolved path, expected digest, and role.
    """
    observed = _canonical_registry()
    require(observed == _CANONICAL_REGISTRY_LOCK,
            "canonical name/path/digest/role registry changed")
    report: dict[str, dict[str, object]] = {}
    for name, resolved_text, expected, role in observed:
        path = Path(resolved_text)
        require(path.is_absolute() and path == path.resolve(strict=False),
                f"source path is not canonical and resolved: {name}")
        require(path.is_relative_to(ROOT.resolve()),
                f"source escaped repository root: {name}")
        require(path.is_file() and not path.is_symlink(),
                f"missing or symlinked canonical source: {name}")
        actual = sha256(path)
        require(actual == expected,
                f"canonical source digest changed: {name}")
        payload = path.read_bytes()
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise GateError(f"canonical source is not UTF-8: {name}") from error
        for token in _SOURCE_TOKENS.get(name, ()):
            require(text.count(token) == 1,
                    f"semantic token missing or nonunique: {name}: {token!r}")
        report[name] = {
            "resolved_path": resolved_text,
            "sha256": actual,
            "bytes": len(payload),
            "role": role,
            "semantic_tokens_unique": len(_SOURCE_TOKENS.get(name, ())),
        }
    return report


@dataclass(frozen=True)
class AnalyticObligation:
    name: str
    statement: str
    classification: str
    sources: tuple[str, ...]
    proof_kernel: tuple[str, ...]
    strict_executable_replay: bool


PROSE_CLASSIFICATION = "rigorous_prose_authenticated_not_executable_universal_replay"
ANALYTIC_BLOCKERS = (
    AnalyticObligation(
        "uniform-triangular-cactus",
        ("Every connected triangular cactus containing a triangle has sigma>0; "
         "every cyclic block is C3, while bridge blocks/connectors and arbitrary "
         "finite attached trees are allowed."),
        PROSE_CLASSIFICATION,
        ("triangular-cactus-proof",),
        ("maximum vertex-disjoint cycle packing",
         "lexicographic Voronoi territories are connected induced and exhaustive",
         "each territory has cycle-packing number one",
         "packing-one Sachs sign plus induced superadditivity gives strict credit"),
        False,
    ),
    AnalyticObligation(
        "six-triangle-margin",
        ("Every connected six-triangle cactus has sigma>1, including the exact "
         "shared-cluster floors A5>2 and A6>1."),
        PROSE_CLASSIFICATION,
        ("six-triangle-recurrence-proof", "four-five-triangle-kernel",
         "triangular-cactus-proof"),
        ("A4>3 by the central-triangle/three-petal matching injection",
         "one incidence-leaf opening costs exactly one tree credit",
         "therefore A5>2 and A6>1",
         "arbitrary-connector territories or a two-triangle path handle cluster separation"),
        False,
    ),
    AnalyticObligation(
        "hostile-c5-one-root",
        ("A one-root unicyclic C5 territory with arbitrary rooted trees has "
         "sigma>=-(sqrt(5)-2)>-1."),
        PROSE_CLASSIFICATION,
        ("hostile-c5-proof",),
        ("rooted-tree elimination gives activities a_v>=t",
         "weighted-cycle phase is dominated by the bare C5 phase",
         "the bare C5 spectrum gives delta_5=sqrt(5)-2"),
        False,
    ),
    AnalyticObligation(
        "nonunicyclic-cactus-strictness",
        ("Every finite simple connected cactus of cyclomatic rank at least two "
         "has sigma>0, with arbitrary shared cuts, bridge connectors, cactus "
         "incidence, and finite tree attachments."),
        PROSE_CLASSIFICATION,
        ("nonunicyclic-cactus-theorem",),
        ("rank-uniform sharp-DNN frontier is exact",
         "T^(k-1)Q is closed by the hostile/nonhostile one-cycle theorems",
         "T^(k-2)PP is closed including the separate rank-two boundary",
         "the frontier alternatives are exhaustive for every k>=2"),
        False,
    ),
)


EXECUTABLE_CHILDREN = MappingProxyType({
    "adjacency-parent-gate": "adjacency-parent-gate",
    "literal-cycle-typing": "literal-cycle-typing",
    "dtt-selector": "dtt-selector",
    "dtt-packet": "dtt-packet",
})


def run_child(source_name: str) -> dict[str, object]:
    require(source_name in EXECUTABLE_CHILDREN,
            f"unregistered executable child: {source_name}")
    pin = _CANONICAL_SOURCE_PINS[source_name]
    path = (ROOT / pin.relative_path).resolve()
    require(path == Path(dict((name, resolved) for name, resolved,
                              unused_digest, unused_role
                              in _CANONICAL_REGISTRY_LOCK)[source_name]),
            f"executable child path does not match canonical registry: {source_name}")
    normal = subprocess.run([sys.executable, str(path)], check=False,
                            capture_output=True, text=True)
    require(normal.returncode == 0,
            f"executable child failed: {source_name}")
    require(normal.stderr == "",
            f"executable child wrote stderr: {source_name}")
    optimized = subprocess.run([sys.executable, "-O", str(path), OPTIMIZED_FLAG],
                               check=False, capture_output=True, text=True)
    require(optimized.returncode == 0,
            f"optimized executable child failed: {source_name}")
    require(optimized.stderr == "",
            f"optimized executable child wrote stderr: {source_name}")
    require(optimized.stdout == normal.stdout,
            f"normal/-O executable child mismatch: {source_name}")
    parsed_status = None
    if source_name != "dtt-packet":
        try:
            parsed = json.loads(normal.stdout)
        except json.JSONDecodeError as error:
            raise GateError(f"child emitted invalid JSON: {source_name}") from error
        parsed_status = parsed.get("status")
    else:
        require(normal.stdout.startswith(
            "diamond-plus-two-triangles exact packet verifier: PASS\n"),
            "DTT exact packet PASS receipt changed")
        require("uniform packet bound: sigma(D+TT)=3+Delta/2>3" in normal.stdout,
                "DTT exact packet bound receipt changed")
    expected_status = {
        "adjacency-parent-gate": "NONPROMOTIONAL_ADJACENCY_AND_OWNERSHIP_VERIFIED",
        "literal-cycle-typing": "NONPROMOTIONAL_ADJACENCY_AUTHENTICATED_TYPING_CERTIFICATE",
        "dtt-selector": "NONPROMOTIONAL_CANDIDATE_LEMMA",
    }.get(source_name)
    if expected_status is not None:
        require(parsed_status == expected_status,
                f"child status changed: {source_name}")
    return {
        "normal_returncode": normal.returncode,
        "optimized_returncode": optimized.returncode,
        "stdout_bytes": len(normal.stdout.encode("utf-8")),
        "stdout_sha256": hashlib.sha256(normal.stdout.encode("utf-8")).hexdigest(),
        "status": parsed_status or "PASS",
    }


def load_parent_module() -> ModuleType:
    path = (ROOT / _CANONICAL_SOURCE_PINS["adjacency-parent-gate"].relative_path).resolve()
    require(sha256(path) == _CANONICAL_SOURCE_PINS["adjacency-parent-gate"].sha256,
            "parent module changed before import")
    spec = importlib.util.spec_from_file_location("r21_adjacency_parent_gate", path)
    require(spec is not None and spec.loader is not None,
            "cannot create parent-gate module specification")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def add_tree_path(parent: ModuleType, graph: object, root: object,
                  names: tuple[object, ...]) -> object:
    vertices = set(graph.vertices)
    edges = set(graph.edges)
    current = root
    for name in names:
        require(name not in vertices, "tree fixture vertex collision")
        vertices.add(name)
        edges.add(parent.edge(current, name))
        current = name
    return parent.PhysicalGraph(frozenset(vertices), frozenset(edges))


def retained_c5_fixture(parent: ModuleType) -> object:
    """D+4T with P retained behind a shared cut, plus rooted/bridge payloads."""
    vertices, edges, unused_names, unused_path = parent.theta_core(2)
    parent.attach_triangle(vertices, edges, "x", "T0")       # sibling at c
    parent.attach_triangle(vertices, edges, "c1", "T1")      # downstream
    parent.attach_triangle(vertices, edges, "c3", "T2")      # downstream
    parent.attach_triangle(vertices, edges, "y", "T3")       # upstream
    vertices.update(("c1", "c2", "c3", "c4"))
    edges.update((parent.edge("x", "c1"), parent.edge("c1", "c2"),
                  parent.edge("c2", "c3"), parent.edge("c3", "c4"),
                  parent.edge("c4", "x")))
    graph = parent.PhysicalGraph(frozenset(vertices), frozenset(edges))
    graph = add_tree_path(parent, graph, "x", ("up:b1", "up:b2"))
    graph = add_tree_path(parent, graph, "c2", ("down:b1", "down:b2"))
    return graph


def mixed_c5_triangle_away_fixture(parent: ModuleType) -> object:
    """One first bridge has a complete descendant side containing C5 and T."""
    vertices, edges, unused_names, unused_path = parent.theta_core(2)
    for index in range(3):
        parent.attach_triangle(vertices, edges, "x", f"root:T{index}")
    vertices.update(("away:w", "away:c1", "away:c2", "away:c3", "away:c4"))
    edges.update((
        parent.edge("x", "away:w"),
        parent.edge("away:w", "away:c1"),
        parent.edge("away:c1", "away:c2"),
        parent.edge("away:c2", "away:c3"),
        parent.edge("away:c3", "away:c4"),
        parent.edge("away:c4", "away:w"),
    ))
    parent.attach_triangle(vertices, edges, "away:w", "away:T")
    graph = parent.PhysicalGraph(frozenset(vertices), frozenset(edges))
    graph = add_tree_path(parent, graph, "away:c2", ("away:payload1", "away:payload2"))
    return graph


def owner_components(parent: ModuleType, graph: object,
                     cycle_block: frozenset) -> dict[object, frozenset]:
    cycle_vertices = parent.block_vertices(cycle_block)
    remaining_edges = graph.edges - cycle_block
    parts = parent.components(graph.vertices, remaining_edges)
    owners: dict[object, frozenset] = {}
    for part in parts:
        meetings = part & cycle_vertices
        require(len(meetings) == 1,
                "a C5 owner component does not meet the pentagon exactly once")
        owner = next(iter(meetings))
        require(owner not in owners, "duplicate C5 owner class")
        owners[owner] = part
    require(set(owners) == set(cycle_vertices),
            "C5 owner classes do not cover every pentagon vertex")
    flattened = [vertex for part in owners.values() for vertex in part]
    require(len(flattened) == len(set(flattened)) == len(graph.vertices),
            "C5 owner classes are not disjoint and exhaustive")
    return owners


def verify_retained_c5(parent: ModuleType, graph: object) -> dict[str, object]:
    inventory = parent.authenticate_r21(graph)
    require(inventory.family == "D_PLUS_T4_C5",
            "retained-C5 fixture is not the literal D+T^4+C5 residual row")
    c5_blocks = tuple(block for block in inventory.cycles
                      if parent.authenticate_literal_cycle(block) == 5)
    require(len(c5_blocks) == 1, "retained-C5 fixture lacks a unique literal C5")
    c5_block = c5_blocks[0]
    tree = parent.build_block_cut_tree(graph)
    c5_index = tree.block_index[next(iter(c5_block))]
    c5_node = ("B", c5_index)
    d_index = tree.block_index[next(iter(inventory.theta_block))]
    d_node = ("B", d_index)
    path = parent.tree_path(tree, d_node, c5_node)
    c5_neighbors = tree.graph[c5_node]
    require(len(c5_neighbors) == 4,
            "retained-C5 fixture did not exercise all intended pentagon ports")
    parent_cut_nodes = tuple(node for node in path if node[0] == "C"
                             and node in c5_neighbors)
    require(len(parent_cut_nodes) == 1,
            "C5 did not have one adjacency-derived parent cut toward D")
    c = parent_cut_nodes[0][1]
    require(c in parent.block_vertices(c5_block),
            "derived C5 parent cut is not a physical pentagon vertex")

    owners = owner_components(parent, graph, c5_block)
    upstream = owners[c]
    downstream = frozenset().union(*(part for owner, part in owners.items()
                                     if owner != c))
    require(upstream.isdisjoint(downstream) and
            upstream | downstream == graph.vertices,
            "retained-C5 opening is not a vertex partition")
    require(parent.connected(upstream,
            frozenset(edge for edge in graph.edges if edge <= upstream)),
            "retained-C5 upstream owner is disconnected")
    require(parent.connected(downstream,
            frozenset(edge for edge in graph.edges if edge <= downstream)),
            "retained-C5 downstream owner union is disconnected")
    crossing = tuple(edge for edge in graph.edges
                     if bool(edge & upstream) and bool(edge & downstream))
    c5_incident = tuple(edge for edge in c5_block if c in edge)
    require(set(crossing) == set(c5_incident) and len(crossing) == 2,
            "retained-C5 split has crossing edges other than the two at c")

    up_positive = parent.positive_rank_blocks(parent.graph_on(graph, upstream), upstream)
    down_positive = parent.positive_rank_blocks(parent.graph_on(graph, downstream), downstream)
    require(inventory.theta_block in up_positive,
            "upstream class lost the physical diamond")
    require(all(block != c5_block for block in (*up_positive, *down_positive)),
            "opened C5 survived as a cyclic block")
    up_triangles = tuple(block for block in up_positive
                         if parent.block_rank(block) == 1)
    down_triangles = tuple(block for block in down_positive
                           if parent.block_rank(block) == 1)
    require(all(parent.authenticate_literal_cycle(block) == 3
                for block in (*up_triangles, *down_triangles)),
            "opened C5 side created a nontriangle cyclic block")
    require(len(up_triangles) == 2 and len(down_triangles) == 2,
            "retained-C5 fixture did not exercise upstream/downstream triangles")
    require("up:b2" in upstream and "down:b2" in downstream,
            "rooted payload did not follow its adjacency-derived owner")
    return {
        "family": inventory.family,
        "parent_cut": repr(c),
        "pentagon_ports": len(c5_neighbors),
        "owner_classes": len(owners),
        "upstream_vertices": len(upstream),
        "downstream_vertices": len(downstream),
        "upstream_triangles": len(up_triangles),
        "downstream_triangles": len(down_triangles),
        "crossing_edges": len(crossing),
        "payload_ownership": "adjacency-derived and exhaustive",
    }


def verify_mixed_c5_triangle_away(parent: ModuleType, graph: object) -> dict[str, object]:
    """Derive the mixed away side from its physical first bridge, not labels."""
    inventory = parent.authenticate_r21(graph)
    require(inventory.family == "D_PLUS_T4_C5",
            "mixed-away fixture is not the literal D+T^4+C5 residual row")
    c5_blocks = tuple(block for block in inventory.cycles
                      if parent.authenticate_literal_cycle(block) == 5)
    require(len(c5_blocks) == 1, "mixed-away fixture lacks a unique literal C5")
    c5_block = c5_blocks[0]
    bridge = parent.edge("x", "away:w")
    require(frozenset((bridge,)) in inventory.bridge_blocks,
            "mixed-away separator is not an actual Tarjan K2 block")
    parts = parent.components(graph.vertices, graph.edges - frozenset((bridge,)))
    require(len(parts) == 2, "mixed-away first bridge did not give two components")
    d_vertices = parent.block_vertices(inventory.theta_block)
    root_parts = tuple(part for part in parts if part & d_vertices)
    require(len(root_parts) == 1 and d_vertices <= root_parts[0],
            "mixed-away split did not retain the whole diamond on one side")
    root_side = root_parts[0]
    away_side = next(part for part in parts if part != root_side)
    require(root_side.isdisjoint(away_side) and root_side | away_side == graph.vertices,
            "mixed-away bridge split is not disjoint and exhaustive")
    require(parent.connected(away_side,
            frozenset(edge for edge in graph.edges if edge <= away_side)),
            "mixed-away descendant side is disconnected")
    crossing = tuple(edge for edge in graph.edges
                     if bool(edge & root_side) and bool(edge & away_side))
    require(crossing == (bridge,),
            "mixed-away descendant side has a second physical interface")

    away_graph = parent.graph_on(graph, away_side)
    away_positive = parent.positive_rank_blocks(away_graph, away_side)
    ranks = tuple(sorted(parent.block_rank(block) for block in away_positive))
    require(ranks == (1, 1),
            "mixed C5/triangle away side is not adjacency-derived rank two")
    lengths = tuple(sorted(parent.authenticate_literal_cycle(block)
                           for block in away_positive))
    require(lengths == (3, 5),
            "mixed away side is not exactly one literal triangle and one literal C5")
    require(c5_block in away_positive,
            "mixed away side lost the authenticated C5 block")
    triangle_count = lengths.count(3)
    require(triangle_count >= 1 and len(away_positive) == triangle_count + 1,
            "mixed away side does not satisfy rank=q+1 with q>=1")
    require(not all(length == 3 for length in lengths),
            "mixed C5/triangle away side was misclassified all-triangle")
    require("away:payload2" in away_side,
            "mixed-away rooted payload escaped its complete descendant side")
    return {
        "family": inventory.family,
        "first_bridge": tuple(sorted(map(repr, bridge))),
        "away_rank": parent.graph_rank(away_side, away_graph.edges),
        "away_cycle_lengths": list(lengths),
        "away_triangles": triangle_count,
        "classification": "connected nonunicyclic cactus; not triangular and not P-only",
        "analytic_source": "nonunicyclic-cactus-theorem",
        "payload_ownership": "adjacency-derived complete descendant side",
    }


def expect_rejected(action: Callable[[], object], label: str,
                    error_types: tuple[type[RuntimeError], ...] = (GateError,)) -> str:
    """Accept only the explicit narrow error classes for one hostile mutation."""
    try:
        action()
    except error_types:
        return label
    raise GateError(f"hostile mutation accepted: {label}")


def check_supplied_registry_for_hostile_test(
        supplied: tuple[tuple[str, str, str, str], ...]) -> None:
    """Test-only comparator; never used by the promotion path."""
    require(type(supplied) is tuple and supplied == _CANONICAL_REGISTRY_LOCK,
            "supplied source registry differs from the immutable canonical registry")


def hostile_source_checks() -> tuple[str, ...]:
    labels: list[str] = []
    registry = _CANONICAL_REGISTRY_LOCK

    swapped = list(registry)
    first = next(index for index, row in enumerate(swapped)
                 if row[0] == "corrected-complete-note")
    second = next(index for index, row in enumerate(swapped)
                  if row[0] == "triangular-cactus-proof")
    left, right = swapped[first], swapped[second]
    swapped[first] = (left[0], right[1], right[2], left[3])
    swapped[second] = (right[0], left[1], left[2], right[3])
    labels.append(expect_rejected(
        lambda: check_supplied_registry_for_hostile_test(tuple(swapped)),
        "source role/path/digest swap"))

    self_hashed = list(registry)
    index = next(place for place, row in enumerate(self_hashed)
                 if row[0] == "corrected-complete-note")
    name, path, unused_expected, role = self_hashed[index]
    self_hashed[index] = (name, path, sha256(Path(path + ".missing"))
                          if Path(path + ".missing").exists() else "0" * 64, role)
    labels.append(expect_rejected(
        lambda: check_supplied_registry_for_hostile_test(tuple(self_hashed)),
        "self-hash/caller digest substitution"))

    renamed = list(registry)
    index = next(place for place, row in enumerate(renamed)
                 if row[0] == "hostile-c5-proof")
    name, path, digest, role = renamed[index]
    renamed[index] = ("triangular-cactus-proof", path, digest, role)
    labels.append(expect_rejected(
        lambda: check_supplied_registry_for_hostile_test(tuple(renamed)),
        "source semantic-name collision"))

    theorem_removed = tuple(row for row in registry
                            if row[0] != "nonunicyclic-cactus-theorem")
    labels.append(expect_rejected(
        lambda: check_supplied_registry_for_hostile_test(theorem_removed),
        "mixed-away cactus theorem source removed"))

    theorem_substituted = list(registry)
    theorem_index = next(place for place, row in enumerate(theorem_substituted)
                         if row[0] == "nonunicyclic-cactus-theorem")
    theorem_name, unused_path, unused_digest, theorem_role = theorem_substituted[theorem_index]
    triangular = next(row for row in registry if row[0] == "triangular-cactus-proof")
    theorem_substituted[theorem_index] = (
        theorem_name, triangular[1], triangular[2], theorem_role)
    labels.append(expect_rejected(
        lambda: check_supplied_registry_for_hostile_test(tuple(theorem_substituted)),
        "mixed-away theorem replaced by triangular theorem"))

    labels.append(expect_rejected(
        lambda: require(any(item.strict_executable_replay
                            for item in ANALYTIC_BLOCKERS),
                        "prose blocker reclassified executable"),
        "prose kernel reclassified executable"))
    return tuple(labels)


def hostile_adjacency_checks(parent: ModuleType) -> tuple[str, ...]:
    labels: list[str] = []
    parent_gate_error = parent.GateError
    adjacency_rejections = (GateError, parent_gate_error)
    base = retained_c5_fixture(parent)
    inventory = parent.authenticate_r21(base)
    c5 = next(block for block in inventory.cycles
              if parent.authenticate_literal_cycle(block) == 5)

    chord = parent.edge("c1", "c3")
    chorded = parent.PhysicalGraph(base.vertices, base.edges | frozenset((chord,)))
    labels.append(expect_rejected(
        lambda: verify_retained_c5(parent, chorded),
        "chorded retained C5", adjacency_rejections))

    second_join = parent.edge("c2", "y")
    multijoined = parent.PhysicalGraph(base.vertices,
                                      base.edges | frozenset((second_join,)))
    labels.append(expect_rejected(
        lambda: verify_retained_c5(parent, multijoined),
        "second D-to-C5 interface", adjacency_rejections))

    bad_owners = owner_components(parent, base, c5)
    keys = sorted(bad_owners, key=repr)
    duplicated = dict(bad_owners)
    duplicated[keys[1]] = duplicated[keys[1]] | frozenset((keys[0],))
    labels.append(expect_rejected(
        lambda: _validate_owner_map(base.vertices, duplicated),
        "duplicated C5 owner vertex", adjacency_rejections))

    relabelled = parent.d_plus_t4_c5_isolated()
    labels.append(expect_rejected(
        lambda: _require_retained_fixture(parent, relabelled),
        "away C5 relabelled retained", adjacency_rejections))

    mixed = mixed_c5_triangle_away_fixture(parent)
    mixed_inventory = parent.authenticate_r21(mixed)
    mixed_c5 = next(block for block in mixed_inventory.cycles
                    if parent.authenticate_literal_cycle(block) == 5)
    mixed_triangle = next(block for block in mixed_inventory.cycles
                          if parent.authenticate_literal_cycle(block) == 3
                          and "away:w" in parent.block_vertices(block))
    falsely_triangular = parent.graph_on(
        mixed, parent.block_vertices(mixed_c5) | parent.block_vertices(mixed_triangle))
    labels.append(expect_rejected(
        lambda: _require_all_triangle_blocks(parent, falsely_triangular),
        "mixed C5/triangle away side called triangular", adjacency_rejections))

    p_only = parent.d_plus_t4_c5_isolated()
    labels.append(expect_rejected(
        lambda: verify_mixed_c5_triangle_away(parent, p_only),
        "P-only away side called mixed nonunicyclic", adjacency_rejections))

    extra_interface = parent.edge("away:c2", "y")
    multiply_joined = parent.PhysicalGraph(
        mixed.vertices, mixed.edges | frozenset((extra_interface,)))
    labels.append(expect_rejected(
        lambda: verify_mixed_c5_triangle_away(parent, multiply_joined),
        "mixed away side with second interface", adjacency_rejections))
    return tuple(labels)


def _require_all_triangle_blocks(parent: ModuleType, graph: object) -> None:
    for block in parent.positive_rank_blocks(graph, graph.vertices):
        require(parent.block_rank(block) == 1 and
                parent.authenticate_literal_cycle(block) == 3,
                "territory contains a nontriangle cyclic block")


def _validate_owner_map(vertices: frozenset, owners: Mapping[object, frozenset]) -> None:
    flattened = [vertex for part in owners.values() for vertex in part]
    require(len(flattened) == len(set(flattened)) == len(vertices),
            "hostile owner map is not disjoint and exhaustive")


def _require_retained_fixture(parent: ModuleType, graph: object) -> None:
    inventory = parent.authenticate_r21(graph)
    c5 = next(block for block in inventory.cycles
              if parent.authenticate_literal_cycle(block) == 5)
    tree = parent.build_block_cut_tree(graph)
    c5_node = ("B", tree.block_index[next(iter(c5))])
    require(len(tree.graph[c5_node]) >= 2,
            "C5 is not retained in a multi-port root group")


def audit_note_scope() -> dict[str, object]:
    note = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    required_once = (
        "Status: **NONPROMOTIONAL_AUTHENTICATED_PROOF_NOTE**",
        "Thus both exact post-DNN residual families are strict.",
        "the whole `R21` block partition is\nclosed",
        "closed: profiles on the DNN boundary may supply only `sigma>=0`, not a strict\nsurplus.",
        "A=R[V(F_c)]",
        "B'=R[union_(w!=c) V(F_w)]",
        "Separate the unique away group containing `P`",
        "connected cactus of rank\n`q+1 in {2,3,4,5}`",
        "no mixed `P`-plus-triangle away group is ever called\ntriangular",
        "rank-uniform nonunicyclic\ncactus theorem",
        "expanded incidence\nsubtrees",
        "its **cut closure**",
    )
    for token in required_once:
        require(note.count(token) == 1,
                f"corrected note scope token missing or nonunique: {token!r}")
    forbidden = (
        "Thus the full `R21` row is strictly closed.",
        "A=G[V(F_c)]",
        "B'=G[union_(w!=c) V(F_w)]",
        "An away group containing a triangle is a positive\ntriangular cactus.",
        "all triangle-containing away sides add positive credit.",
    )
    for token in forbidden:
        require(token not in note,
                f"superseded note claim survived: {token!r}")
    require("Status: **NONPROMOTIONAL_R21_PARTIAL**" not in note,
            "historical partial status leaked into corrected complete note")
    return {
        "full_row_target": "s^+(G)>=|V(G)| (equivalently sigma>=0)",
        "strict_scope": ["Theta(1,2,r)+T^5, r>=2", "D+T^4+C5"],
        "dnn_boundary_strictness_claimed": False,
        "retained_c5_owner_scope": "components of induced root group R minus E(C5)",
        "away_c5_dispatch": {
            "P_only": "hostile-c5-one-root floor >-(sqrt(5)-2)>-1",
            "P_plus_q_triangles_q_ge_1": (
                "connected rank-(q+1) cactus, q+1 in {2,3,4,5}; "
                "strict by pinned nonunicyclic-cactus theorem"
            ),
            "P_free": "strict all-triangle cactus",
        },
    }


def audit_no_asserts() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            "gate must not rely on Python assertions")


def nonstrict_report() -> dict[str, object]:
    sources = check_sources()
    note_scope = audit_note_scope()
    children = {name: run_child(name) for name in EXECUTABLE_CHILDREN}
    parent = load_parent_module()
    retained = verify_retained_c5(parent, retained_c5_fixture(parent))
    mixed_away = verify_mixed_c5_triangle_away(
        parent, mixed_c5_triangle_away_fixture(parent))
    source_hostiles = hostile_source_checks()
    adjacency_hostiles = hostile_adjacency_checks(parent)
    rejected = (*source_hostiles, *adjacency_hostiles)
    require(len(rejected) == len(set(rejected)),
            "hostile mutation labels are not unique")
    blocker_records = [
        {
            "name": item.name,
            "statement": item.statement,
            "classification": item.classification,
            "authenticated_sources": list(item.sources),
            "proof_kernel": list(item.proof_kernel),
            "executable_universal_replay": item.strict_executable_replay,
        }
        for item in ANALYTIC_BLOCKERS
    ]
    require(all(record["classification"] == PROSE_CLASSIFICATION
                and record["executable_universal_replay"] is False
                for record in blocker_records),
            "analytic blocker classification drifted")
    return {
        "schema": SCHEMA,
        "status": "NONPROMOTIONAL_AUTHENTICATED_STRICT_EXECUTABLE_BLOCKED",
        "promotion_passed": False,
        "mathematical_disproof": False,
        "note_scope": note_scope,
        "source_registry": sources,
        "executable_replays": children,
        "retained_c5_adjacency_fixture": retained,
        "mixed_c5_triangle_away_adjacency_fixture": mixed_away,
        "analytic_blockers": blocker_records,
        "strict_mode_contract": (
            "Promotion requires executable universal replay for every analytic "
            "blocker. Authenticated rigorous prose is mathematical evidence but "
            "does not satisfy this deliberately stronger executable contract."
        ),
        "historical_open_artifacts": {
            "status": "historical_nonpromotional_not_a_closure_input",
            "paths": [
                _CANONICAL_SOURCE_PINS["historical-partial-note"].relative_path,
                _CANONICAL_SOURCE_PINS["historical-partial-verifier"].relative_path,
            ],
        },
        "hostile_mutations_rejected": {
            "count": len(rejected),
            "labels": list(rejected),
        },
        "trust_boundary": (
            "Adjacency/Tarjan typing, owner partition semantics, canonical source "
            "authentication, executable child receipts, and normal/-O equivalence "
            "are checked here. The four named universal analytic kernels are "
            "authenticated as rigorous prose but are not executable universal replays."
        ),
        "state_modified": False,
        "master_promoted": False,
    }


def strict_failure_payload(report: dict[str, object]) -> str:
    names = [item["name"] for item in report["analytic_blockers"]]
    require(names == [item.name for item in ANALYTIC_BLOCKERS],
            "strict blocker registry changed")
    payload = {
        "schema": SCHEMA,
        "status": "STRICT_EXECUTABLE_PROMOTION_BLOCKED",
        "promotion_passed": False,
        "mathematical_disproof": False,
        "blockers": names,
        "reason": (
            "authenticated rigorous prose has no executable universal replay "
            "under this strict promotion contract"
        ),
    }
    return json.dumps(payload, sort_keys=True) + "\n"


def serialized_report() -> str:
    return json.dumps(nonstrict_report(), sort_keys=True, indent=2) + "\n"


def main(argv: list[str]) -> int:
    audit_no_asserts()
    allowed = {STRICT_FLAG, OPTIMIZED_FLAG}
    require(all(argument in allowed for argument in argv),
            "unknown command-line argument")
    require(len(argv) == len(set(argv)), "duplicate command-line argument")
    strict = STRICT_FLAG in argv
    optimized_child = OPTIMIZED_FLAG in argv
    require(bool(sys.flags.optimize) == optimized_child,
            "--optimized-child and Python -O must be used together")
    report = nonstrict_report()
    stdout = "" if strict else json.dumps(report, sort_keys=True, indent=2) + "\n"
    stderr = strict_failure_payload(report) if strict else ""
    returncode = 2 if strict else 0
    if not optimized_child:
        child_argv = [sys.executable, "-O", str(Path(__file__).resolve()),
                      OPTIMIZED_FLAG]
        if strict:
            child_argv.append(STRICT_FLAG)
        child = subprocess.run(child_argv, check=False,
                               capture_output=True, text=True)
        require(child.returncode == returncode,
                "normal/-O closure return codes differ")
        require(child.stdout == stdout,
                "normal/-O closure stdout differs")
        require(child.stderr == stderr,
                "normal/-O closure stderr differs")
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    return returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
