#!/usr/bin/env python3
"""Candidate adjacency-only semantic verifier for the complete physical R221 lane.

Production API
--------------
``verify(vertices, edges)`` accepts only immutable physical adjacency.  It does
not accept a profile, block inventory, owner map, root, route, rank, threshold,
partition, or analytic charge.  It reconstructs all such data from adjacency,
replays the physical proof once from each of the two literal diamonds, and
returns only recursively immutable records.

Scope and proof boundary
------------------------
The accepted lane is exactly two literal, unsubdivided diamonds and three
literal triangles, with arbitrary physical K2 connectors, block-cut nesting,
shared cuts, and finite tree payloads.  This executable is a semantic gate and
finite corroborator.  Source-byte authentication proves byte identity, not the
truth of the cited mathematics or the correctness of this program on every
future input.  In particular, no finite fixture suite is represented as the
universal proof.

This file never writes repository state.  It deliberately uses no ``assert``
statement: every production and audit predicate is an explicit fail-closed
``require``.
"""
from __future__ import annotations

import ast
import hashlib
import itertools
import json
import shutil
import sys
import tempfile
from collections import Counter, deque
from dataclasses import dataclass, fields, is_dataclass, replace
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[1]
PROFILE = "literal-D+D+T3"
SCHEMA = "r221-adjacency-semantic-certificate-v1"


class VerifyError(RuntimeError):
    """A semantic or provenance predicate rejected the input."""


def require(condition, message):
    if not condition:
        raise VerifyError(message)


def expect_rejection(action, label, expected_message):
    """Accept only the intended VerifyError; never mask implementation crashes."""
    require(type(label) is str and label, "hostile test has no label")
    require(type(expected_message) is str and expected_message,
            f"hostile test has no expected reason: {label}")
    try:
        action()
    except VerifyError as error:
        require(expected_message in str(error),
                f"hostile rejection had wrong reason: {label}: {error}")
        return label
    raise VerifyError(f"hostile mutation accepted: {label}")


def sha256_bytes(data):
    require(type(data) is bytes, "SHA-256 input is not bytes")
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    return sha256_bytes(path.read_bytes())


# ---------------------------------------------------------------------------
# Canonical immutable atoms and canonical encodings.
# ---------------------------------------------------------------------------


def atom_encoding(value):
    """Injective JSON-compatible encoding for accepted physical vertex atoms."""
    if type(value) is int:
        return ["int", str(value)]
    if type(value) is str:
        return ["str", value]
    if type(value) is bytes:
        return ["bytes", value.hex()]
    if type(value) is tuple:
        return ["tuple", [atom_encoding(item) for item in value]]
    raise VerifyError("vertex atom is outside the immutable canonical type grammar")


def atom_bytes(value):
    return json.dumps(atom_encoding(value), ensure_ascii=True,
                      separators=(",", ":")).encode("utf-8")


def vertex_key(value):
    return atom_bytes(value)


def ordered_vertices(vertices):
    return tuple(sorted(vertices, key=vertex_key))


def edge(left, right):
    require(left != right, "loop in simple adjacency")
    return frozenset((left, right))


def edge_key(current):
    require(type(current) is frozenset and len(current) == 2,
            "malformed unordered edge")
    ends = sorted((atom_bytes(item) for item in current))
    return (ends[0], ends[1])


def edge_set_key(edges):
    return tuple(sorted((edge_key(current) for current in edges)))


def vertex_set_key(vertices):
    return tuple(sorted((vertex_key(current) for current in vertices)))


def canonical_value(value):
    """Canonical encoding for immutable certificates and audit summaries."""
    if value is None:
        return ["none"]
    if type(value) is bool:
        return ["bool", value]
    if type(value) is int:
        return ["int", str(value)]
    if type(value) is str:
        return ["str", value]
    if type(value) is bytes:
        return ["bytes", value.hex()]
    if type(value) is tuple:
        return ["tuple", [canonical_value(item) for item in value]]
    if type(value) is frozenset:
        encoded = [canonical_value(item) for item in value]
        encoded.sort(key=lambda item: json.dumps(
            item, ensure_ascii=True, separators=(",", ":")))
        return ["frozenset", encoded]
    if is_dataclass(value) and not isinstance(value, type):
        return ["record", type(value).__name__, [
            [field.name, canonical_value(getattr(value, field.name))]
            for field in fields(value)
        ]]
    raise VerifyError(f"noncanonical certificate value: {type(value).__name__}")


def canonical_bytes(value):
    return json.dumps(canonical_value(value), ensure_ascii=True,
                      separators=(",", ":")).encode("utf-8")


def certificate_digest(certificate):
    return sha256_bytes(canonical_bytes(certificate))


def require_recursively_immutable(value, path="certificate"):
    if value is None or type(value) in (bool, int, str, bytes):
        return True
    if type(value) is tuple:
        for index, item in enumerate(value):
            require_recursively_immutable(item, f"{path}[{index}]")
        return True
    if type(value) is frozenset:
        for item in value:
            require_recursively_immutable(item, f"{path}{{item}}")
        return True
    if is_dataclass(value) and not isinstance(value, type):
        parameters = getattr(type(value), "__dataclass_params__", None)
        require(parameters is not None and parameters.frozen,
                f"{path} record is not frozen")
        for field in fields(value):
            require_recursively_immutable(getattr(value, field.name),
                                          f"{path}.{field.name}")
        return True
    raise VerifyError(f"{path} contains mutable or unsupported state")


# ---------------------------------------------------------------------------
# Immutable semantic contract manifest.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ContractRecord:
    contract_id: str
    source_path: str
    source_sha256: str
    locator: str
    claim: str
    applicability: str
    floor: int | None
    strict: bool
    depends_on: tuple[str, ...]


CONTRACT_SPECS = (
    ContractRecord(
        "R221-THETA-CYCLE-CLASSIFICATION-v1",
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "Theta-cycle DNN sieve, lines 289-417",
        "Delta>1 exactly for Theta(1,2,r); the unique maximum is Delta(1,2,2)=(sqrt(17)-1)/2, every nonmaximum exceptional Delta is below 4/3, and cycle excesses obey epsilon3=1, epsilon5<2/3, epsilon_q<2/5 for odd q>=7",
        "exact excess classification used only with the rank-seven 2+2+1^3 DNN threshold",
        None,
        False,
        (),
    ),
    ContractRecord(
        "R221-RESIDUAL-SIEVE-v1",
        "positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
        "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5",
        "rank partition table row 2+2+1^3 and its exact-classification premise",
        "the exact R221 post-DNN residual is two literal diamonds plus three literal triangles",
        "adjacency must independently authenticate literal D+D+T3 and total rank seven",
        None,
        False,
        ("R221-THETA-CYCLE-CLASSIFICATION-v1",),
    ),
    ContractRecord(
        "R221-INDUCED-SUPERADD-v1",
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "induced square-energy superadditivity lemma",
        "sigma(G) is at least the sum of sigma on an original-vertex induced partition",
        "finite vertex partitions; crossing edges are allowed but every part is evaluated as an induced subgraph",
        None,
        False,
        (),
    ),
    ContractRecord(
        "R221-TREE-EXACT-v1",
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "tree base case",
        "every nonempty tree has sigma=-1",
        "connected nonempty rank-zero induced piece",
        -1,
        False,
        (),
    ),
    ContractRecord(
        "R221-CONNECTED-FLOOR-v1",
        "tree-equality-square-energy/paper.tex",
        "66370f3cb81546325f0e9a4e19919aa2572f0d147cff6d8baa3f9425e7d82889",
        "connected n-1 lower bound and equality theorem",
        "every nonempty connected graph has sigma>=-1",
        "generic nonempty connected induced piece",
        -1,
        False,
        (),
    ),
    ContractRecord(
        "R221-TRIANGULAR-BLOCK-v1",
        "packing-two-square-energy/paper.tex",
        "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "triangular block-graph territory theorem",
        "a connected graph whose positive blocks are literal triangles and which contains a triangle has sigma>0",
        "arbitrary bridge-tree attachments, including several or nested triangle blocks",
        0,
        True,
        (),
    ),
    ContractRecord(
        "R221-DIAMOND-EXACT-v1",
        "all-pentacyclic-graphs/paper.tex",
        "8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18",
        "packet ledger and weighted diamond phase, lines 239-290",
        "a literal diamond with arbitrary one-root tree branches has sigma>1",
        "bridge-free shared-cut D packet; no additional positive block or positive K2 connector",
        1,
        True,
        (),
    ),
    ContractRecord(
        "R221-DIAMOND-T1-EXACT-v1",
        "all-pentacyclic-graphs/paper.tex",
        "8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18",
        "packet ledger and exact D+T one-sum phase, lines 239-290",
        "a bridge-free shared-cut literal D+T packet with arbitrary one-root tree branches has sigma>2",
        "one literal diamond and one literal triangle in one bridge-free shared-cut incidence tree",
        2,
        True,
        (),
    ),
    ContractRecord(
        "R221-DTT-EXACT-v1",
        "positive-square-energy/pentacyclic-general/diamond-two-triangle-exact-packet.md",
        "9107ef2821d441da401079982ae8d0b6c98cee17ae7e52268a9b6ad895b8e11b",
        "Theorem and Sections 1-5",
        "a bridge-free shared-cut literal D+T+T packet with arbitrary one-root trees has sigma>3",
        "direct/direct or direct/nested triangle incidence; no positive K2 connector on the cyclic hull",
        3,
        True,
        (),
    ),
    ContractRecord(
        "R221-DIAMOND-T0T3-ROOT-v1",
        "positive-square-energy/heptacyclic-general/r21-complete-physical-closure.md",
        "c1175db74866fdc03551ffc9081596147acbe14b1d60f6a6e016c8788aa04860",
        "Section 4, Narrow root packets",
        "every bridge-free shared-cut root cluster D+T^k for 0<=k<=3, with arbitrary one-root tree branches, has sigma>1",
        "one literal diamond, k literal triangles, no physical K2 on a route between positive blocks",
        1,
        True,
        ("R221-DIAMOND-EXACT-v1", "R221-DIAMOND-T1-EXACT-v1",
         "R221-DTT-EXACT-v1", "R221-CONNECTED-FLOOR-v1"),
    ),
    ContractRecord(
        "R221-CONNECTED-RANK2-v1",
        "all-bicyclic-graphs/paper.tex",
        "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
        "main connected bicyclic theorem",
        "every finite simple connected rank-two graph has sigma>0",
        "complete first-K2 away component with recomputed rank two",
        0,
        True,
        (),
    ),
    ContractRecord(
        "R221-CONNECTED-RANK3-v1",
        "all-tricyclic-graphs/paper.tex",
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "main connected tricyclic theorem",
        "every finite simple connected rank-three graph has sigma>=0",
        "complete first-K2 away component with recomputed rank three",
        0,
        False,
        (),
    ),
    ContractRecord(
        "R221-CONNECTED-RANK4-v1",
        "all-tetracyclic-graphs/paper.tex",
        "70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f",
        "main connected tetracyclic theorem",
        "every finite simple connected rank-four graph has sigma>=0",
        "complete first-K2 away component with recomputed rank four",
        0,
        False,
        (),
    ),
    ContractRecord(
        "R221-CONNECTED-RANK5-v1",
        "all-pentacyclic-graphs/paper.tex",
        "8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18",
        "Theorem 1, connected pentacyclic result",
        "every finite simple connected rank-five graph has sigma>=0",
        "complete first-K2 away component with recomputed rank five",
        0,
        False,
        (),
    ),
)

CONTRACTS = {item.contract_id: item for item in CONTRACT_SPECS}

EXPECTED_CONTRACT_IDS = frozenset({
    "R221-THETA-CYCLE-CLASSIFICATION-v1",
    "R221-RESIDUAL-SIEVE-v1",
    "R221-INDUCED-SUPERADD-v1",
    "R221-TREE-EXACT-v1",
    "R221-CONNECTED-FLOOR-v1",
    "R221-TRIANGULAR-BLOCK-v1",
    "R221-DIAMOND-EXACT-v1",
    "R221-DIAMOND-T1-EXACT-v1",
    "R221-DTT-EXACT-v1",
    "R221-DIAMOND-T0T3-ROOT-v1",
    "R221-CONNECTED-RANK2-v1",
    "R221-CONNECTED-RANK3-v1",
    "R221-CONNECTED-RANK4-v1",
    "R221-CONNECTED-RANK5-v1",
})

EXPECTED_SOURCE_ROWS = frozenset({
    ("positive-square-energy/heptacyclic-general/rank-seven-multiblock-debit-ledger.md",
     "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5"),
    ("all-tricyclic-graphs/paper.tex",
     "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02"),
    ("tree-equality-square-energy/paper.tex",
     "66370f3cb81546325f0e9a4e19919aa2572f0d147cff6d8baa3f9425e7d82889"),
    ("packing-two-square-energy/paper.tex",
     "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791"),
    ("positive-square-energy/pentacyclic-general/diamond-two-triangle-exact-packet.md",
     "9107ef2821d441da401079982ae8d0b6c98cee17ae7e52268a9b6ad895b8e11b"),
    ("positive-square-energy/heptacyclic-general/r21-complete-physical-closure.md",
     "c1175db74866fdc03551ffc9081596147acbe14b1d60f6a6e016c8788aa04860"),
    ("all-bicyclic-graphs/paper.tex",
     "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da"),
    ("all-tetracyclic-graphs/paper.tex",
     "70a931c28c8a8817e2c02818200885f73c532d9afe2c065831f2b3884d61160f"),
    ("all-pentacyclic-graphs/paper.tex",
     "8ce140b07dc1428656b4ffd914305f2b14b49a0555cd13a6fc87be0fd4246a18"),
})

# Filled below with independently generated literal values after the canonical
# schema was fixed.  They are not recomputed from mutated runtime globals.
EXPECTED_FULL_CONTRACT_MANIFEST_SHA256 = "686aa99b3f07223ed8f241be2480490b0afe3f1ad83d937f8dfced3dc2031b67"
EXPECTED_SOURCE_MANIFEST_SHA256 = "18383070b4eb253b634e3fb9be8dbd716d9ceedfa618e6c1ed5e4ab15c404679"


def contract_manifest_payload(specs=None):
    specs = CONTRACT_SPECS if specs is None else specs
    records = []
    for item in specs:
        floor = ({"kind": "null"} if item.floor is None else
                 {"kind": "integer", "value": item.floor})
        records.append({
            "id": item.contract_id,
            "path": item.source_path,
            "sha256": item.source_sha256,
            "locator": item.locator,
            "claim": item.claim,
            "applicability": item.applicability,
            "floor": floor,
            "strict": item.strict,
            "depends_on": list(item.depends_on),
        })
    return {"schema": "r221-semantic-contract-manifest-v1",
            "records": records}


def full_contract_manifest_bytes(specs=None):
    return json.dumps(contract_manifest_payload(specs), ensure_ascii=True,
                      separators=(",", ":")).encode("utf-8")


def full_contract_manifest_digest(specs=None):
    return sha256_bytes(full_contract_manifest_bytes(specs))


def source_manifest_digest(specs=None):
    specs = CONTRACT_SPECS if specs is None else specs
    rows = sorted({f"{item.source_path}\t{item.source_sha256}"
                   for item in specs})
    return sha256_bytes(("\n".join(rows) + "\n").encode("utf-8"))


def audit_contract_table():
    require(type(CONTRACT_SPECS) is tuple,
            "analytic contract specification container changed")
    require(all(type(item) is ContractRecord for item in CONTRACT_SPECS),
            "analytic contract specification record changed")
    ids = tuple(item.contract_id for item in CONTRACT_SPECS)
    require(len(ids) == len(set(ids)) and frozenset(ids) == EXPECTED_CONTRACT_IDS,
            "analytic contract ID set changed")
    require(type(CONTRACTS) is dict and frozenset(CONTRACTS) == EXPECTED_CONTRACT_IDS,
            "analytic contract lookup changed")
    require(CONTRACTS == {item.contract_id: item for item in CONTRACT_SPECS},
            "analytic contract tuple/lookup disagree")
    for item in CONTRACT_SPECS:
        require(type(item.contract_id) is str and item.contract_id,
                "malformed contract ID")
        require(type(item.source_path) is str and item.source_path and
                not Path(item.source_path).is_absolute() and
                ".." not in Path(item.source_path).parts,
                f"malformed source path: {item.contract_id}")
        require(type(item.source_sha256) is str and
                len(item.source_sha256) == 64 and
                all(character in "0123456789abcdef"
                    for character in item.source_sha256),
                f"malformed source digest: {item.contract_id}")
        require(type(item.locator) is str and item.locator,
                f"malformed source locator: {item.contract_id}")
        require(type(item.claim) is str and item.claim,
                f"malformed contract claim: {item.contract_id}")
        require(type(item.applicability) is str and item.applicability,
                f"malformed contract applicability: {item.contract_id}")
        require(item.floor is None or type(item.floor) is int,
                f"contract floor malformed: {item.contract_id}")
        require(type(item.strict) is bool,
                f"contract strictness malformed: {item.contract_id}")
        require(type(item.depends_on) is tuple and
                all(type(name) is str and name for name in item.depends_on),
                f"contract dependencies malformed: {item.contract_id}")
        require(len(item.depends_on) == len(set(item.depends_on)) and
                set(item.depends_on) <= EXPECTED_CONTRACT_IDS and
                item.contract_id not in item.depends_on,
                f"contract dependencies invalid: {item.contract_id}")
    require(full_contract_manifest_digest() ==
            EXPECTED_FULL_CONTRACT_MANIFEST_SHA256,
            "analytic full contract manifest changed")
    rows = frozenset((item.source_path, item.source_sha256)
                     for item in CONTRACT_SPECS)
    require(rows == EXPECTED_SOURCE_ROWS,
            "analytic source path/digest manifest changed")
    require(source_manifest_digest() == EXPECTED_SOURCE_MANIFEST_SHA256,
            "analytic source manifest digest changed")
    return True


def authenticate_source_blob(blob, expected, label):
    require(type(blob) is bytes, "analytic source blob is not bytes")
    require(sha256_bytes(blob) == expected,
            f"analytic source changed: {label}")


def audit_sources():
    audit_contract_table()
    root = SOURCE_ROOT
    require(isinstance(root, Path) and root.is_dir(),
            "analytic source authentication failed: repository absent")
    checked = set()
    for item in CONTRACT_SPECS:
        key = (item.source_path, item.source_sha256)
        if key in checked:
            continue
        path = root / item.source_path
        require(path.is_file(),
                f"analytic source authentication failed: missing {item.contract_id}")
        try:
            blob = path.read_bytes()
        except OSError as error:
            raise VerifyError(
                f"analytic source authentication failed: unreadable {item.contract_id}") from error
        authenticate_source_blob(blob, item.source_sha256, item.contract_id)
        checked.add(key)
    require(checked == set(EXPECTED_SOURCE_ROWS),
            "authenticated source set differs from immutable manifest")
    return len(checked)


def dependency_closure(contract_ids):
    pending = [(current, ()) for current in contract_ids]
    result = set()
    while pending:
        current, ancestors = pending.pop()
        require(current in CONTRACTS, f"unknown analytic contract: {current}")
        require(current not in ancestors,
                "analytic contract dependency graph contains a cycle")
        if current in result:
            continue
        result.add(current)
        lineage = (*ancestors, current)
        pending.extend((dependency, lineage)
                       for dependency in CONTRACTS[current].depends_on)
    return tuple(sorted(result))


# ---------------------------------------------------------------------------
# Physical graph, iterative Tarjan reconstruction, and rooted block-cut tree.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PhysicalGraph:
    vertices: frozenset
    edges: frozenset


@dataclass(frozen=True, slots=True)
class Block:
    index: int
    edges: frozenset
    vertices: frozenset
    rank: int
    kind: str


@dataclass(slots=True)
class Inventory:
    graph: PhysicalGraph
    blocks: tuple[Block, ...]
    cuts: frozenset
    tree: dict
    diamonds: tuple[int, int]
    triangles: tuple[int, int, int]
    bridges: tuple[int, ...]


@dataclass(slots=True)
class Rooting:
    root_block: int
    parent: dict
    depth: dict
    order: tuple


@dataclass(frozen=True, slots=True)
class LocalAnalysis:
    vertices: frozenset
    edges: frozenset
    blocks: tuple[Block, ...]
    rank: int
    positive_blocks: tuple[Block, ...]


def normalize_graph(vertices, edges):
    require(type(vertices) is frozenset and vertices,
            "vertices must be a nonempty frozenset")
    for vertex in vertices:
        atom_encoding(vertex)
    require(type(edges) is frozenset,
            "edges must be a frozenset")
    normalized = set()
    for current in edges:
        require(type(current) is frozenset and len(current) == 2,
                "malformed unordered edge")
        require(current <= vertices, "edge endpoint outside vertex set")
        left, right = ordered_vertices(current)
        require(left != right, "loop in simple adjacency")
        normalized.add(frozenset((left, right)))
    require(len(normalized) == len(edges),
            "duplicate physical edge representation")
    return PhysicalGraph(vertices, frozenset(normalized))


def adjacency(vertices, edges):
    graph = {vertex: set() for vertex in vertices}
    for current in edges:
        left, right = ordered_vertices(current)
        graph[left].add(right)
        graph[right].add(left)
    return graph


def induced_edges(edges, vertices):
    vertices = frozenset(vertices)
    return frozenset(current for current in edges if current <= vertices)


def components(vertices, edges):
    vertices = frozenset(vertices)
    require(all(current <= vertices for current in edges),
            "component edge escapes supplied vertices")
    graph = adjacency(vertices, edges)
    unseen = set(vertices)
    answer = []
    while unseen:
        start = min(unseen, key=vertex_key)
        seen = {start}
        stack = [start]
        while stack:
            current = stack.pop()
            for neighbor in sorted(graph[current], key=vertex_key, reverse=True):
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        unseen.difference_update(seen)
        answer.append(frozenset(seen))
    answer.sort(key=vertex_set_key)
    return tuple(answer)


def connected(vertices, edges):
    return bool(vertices) and len(components(vertices, edges)) == 1


def graph_rank(vertices, edges):
    return len(edges) - len(vertices) + len(components(vertices, edges))


def biconnected_edge_blocks(vertices, edges):
    """Iterative edge-stack Tarjan; every physical bridge is a K2 block."""
    graph_sets = adjacency(vertices, edges)
    graph = {vertex: tuple(sorted(neighbors, key=vertex_key))
             for vertex, neighbors in graph_sets.items()}
    discovery = {}
    low = {}
    parent = {}
    parent_edge = {}
    edge_stack = []
    raw_blocks = []
    clock = 0

    for root in ordered_vertices(vertices):
        if root in discovery:
            continue
        clock += 1
        discovery[root] = low[root] = clock
        frames = [[root, 0]]
        while frames:
            current, offset = frames[-1]
            if offset >= len(graph[current]):
                frames.pop()
                if current in parent:
                    upstream = parent[current]
                    low[upstream] = min(low[upstream], low[current])
                    if low[current] >= discovery[upstream]:
                        boundary = parent_edge[current]
                        current_block = set()
                        while True:
                            require(edge_stack, "Tarjan edge stack underflow")
                            popped = edge_stack.pop()
                            current_block.add(popped)
                            if popped == boundary:
                                break
                        raw_blocks.append(frozenset(current_block))
                else:
                    require(not edge_stack,
                            "Tarjan edge stack leaked at DFS root")
                continue

            neighbor = graph[current][offset]
            frames[-1][1] += 1
            current_edge = edge(current, neighbor)
            if neighbor not in discovery:
                parent[neighbor] = current
                parent_edge[neighbor] = current_edge
                edge_stack.append(current_edge)
                clock += 1
                discovery[neighbor] = low[neighbor] = clock
                frames.append([neighbor, 0])
            elif (parent.get(current) != neighbor and
                  discovery[neighbor] < discovery[current]):
                edge_stack.append(current_edge)
                low[current] = min(low[current], discovery[neighbor])

    union = set().union(*raw_blocks) if raw_blocks else set()
    require(union == set(edges),
            "Tarjan blocks do not exhaust physical edges")
    require(sum(len(current) for current in raw_blocks) == len(edges),
            "Tarjan blocks duplicate physical edges")
    raw_blocks.sort(key=edge_set_key)
    return tuple(raw_blocks)


def classify_block(index, edges):
    require(type(edges) is frozenset and edges, "empty edge block")
    vertices = frozenset().union(*edges)
    rank = len(edges) - len(vertices) + 1
    degrees = {vertex: sum(vertex in current for current in edges)
               for vertex in vertices}
    if len(edges) == 1:
        require(rank == 0 and len(vertices) == 2,
                "malformed physical bridge")
        return Block(index, edges, vertices, rank, "bridge")
    if (len(vertices) == 4 and len(edges) == 5 and rank == 2 and
            sorted(degrees.values()) == [2, 2, 3, 3]):
        return Block(index, edges, vertices, rank, "diamond")
    if (len(vertices) == 3 and len(edges) == 3 and rank == 1 and
            all(value == 2 for value in degrees.values())):
        return Block(index, edges, vertices, rank, "triangle")
    raise VerifyError("unsupported positive-rank block type in physical R221 lane")


def block(inventory, index):
    require(type(index) is int and 0 <= index < len(inventory.blocks),
            "block index outside reconstructed inventory")
    return inventory.blocks[index]


def positive_ids(inventory):
    return (*inventory.diamonds, *inventory.triangles)


def reconstruct(vertices, edges):
    graph = normalize_graph(vertices, edges)
    require(connected(graph.vertices, graph.edges), "input graph disconnected")
    require(graph_rank(graph.vertices, graph.edges) == 7,
            "input graph does not have cyclomatic rank seven")

    raw = biconnected_edge_blocks(graph.vertices, graph.edges)
    blocks = tuple(classify_block(index, current)
                   for index, current in enumerate(raw))
    positive = tuple(current for current in blocks if current.rank)
    diamonds = tuple(current.index for current in positive
                     if current.kind == "diamond")
    triangles = tuple(current.index for current in positive
                      if current.kind == "triangle")
    require(len(diamonds) == 2 and len(triangles) == 3 and
            len(positive) == 5,
            "positive blocks are not exactly two literal diamonds and three literal triangles")
    require(tuple(sorted(current.rank for current in positive)) ==
            (1, 1, 1, 2, 2),
            "positive block ranks are not exactly 2+2+1+1+1")
    require(sum(current.rank for current in positive) == 7,
            "positive block ranks do not sum to seven")

    membership = {
        vertex: tuple(current.index for current in blocks
                      if vertex in current.vertices)
        for vertex in graph.vertices
    }
    cuts = frozenset(vertex for vertex, owners in membership.items()
                     if len(owners) >= 2)
    tree = {("B", current.index): set() for current in blocks}
    for cut in cuts:
        cut_node = ("C", cut)
        tree[cut_node] = set()
        for owner in membership[cut]:
            block_node = ("B", owner)
            tree[cut_node].add(block_node)
            tree[block_node].add(cut_node)
    require(tree, "empty block-cut incidence")
    incidence_edges = sum(len(neighbors) for neighbors in tree.values()) // 2
    require(incidence_edges == len(tree) - 1,
            "block-cut incidence is not a tree")
    # Connectivity is checked independently rather than inferred only from E=V-1.
    incidence_seen = set()
    incidence_stack = [min(tree, key=node_key)]
    while incidence_stack:
        current = incidence_stack.pop()
        if current in incidence_seen:
            continue
        incidence_seen.add(current)
        incidence_stack.extend(tree[current] - incidence_seen)
    require(incidence_seen == set(tree),
            "block-cut incidence is disconnected")
    for left, right in itertools.combinations(blocks, 2):
        overlap = left.vertices & right.vertices
        require(len(overlap) <= 1,
                "distinct Tarjan blocks overlap in more than one vertex")
        if overlap:
            only = next(iter(overlap))
            require(only in cuts,
                    "intersecting blocks do not meet at a reconstructed cut")
    bridges = tuple(current.index for current in blocks
                    if current.kind == "bridge")
    return Inventory(graph, blocks, cuts, tree, diamonds, triangles, bridges)


def node_key(node):
    if node[0] == "B":
        return (b"B", str(node[1]).encode("ascii"))
    return (b"C", vertex_key(node[1]))


def root_block_cut_tree(inventory, root_index):
    root = ("B", root_index)
    require(root in inventory.tree, "block-cut root absent")
    parent = {root: None}
    depth = {root: 0}
    order = [root]
    queue = deque([root])
    while queue:
        current = queue.popleft()
        for neighbor in sorted(inventory.tree[current], key=node_key):
            if neighbor == parent[current]:
                continue
            require(neighbor not in parent,
                    "block-cut incidence contains a cycle")
            parent[neighbor] = current
            depth[neighbor] = depth[current] + 1
            order.append(neighbor)
            queue.append(neighbor)
    require(set(parent) == set(inventory.tree),
            "rooted block-cut topology disconnected")
    return Rooting(root_index, parent, depth, tuple(order))


def path_from_root(rooting, node):
    require(node in rooting.parent, "block-cut path target absent")
    result = []
    current = node
    while current is not None:
        result.append(current)
        current = rooting.parent[current]
    result.reverse()
    return tuple(result)


def is_ancestor(rooting, ancestor, descendant, strict=False):
    require(ancestor in rooting.depth and descendant in rooting.depth,
            "ancestry node absent")
    if strict and ancestor == descendant:
        return False
    current = descendant
    while current is not None and rooting.depth[current] >= rooting.depth[ancestor]:
        if current == ancestor:
            return True
        current = rooting.parent[current]
    return False


def upstream_cut(inventory, rooting, block_index):
    node = ("B", block_index)
    require(block_index != rooting.root_block,
            "root diamond has no upstream articulation")
    parent = rooting.parent.get(node)
    require(parent is not None and parent[0] == "C",
            "positive block lacks immediate upstream articulation")
    cut = parent[1]
    require(cut in block(inventory, block_index).vertices,
            "upstream articulation lies outside boundary block")
    return cut


def analyze_piece(inventory, vertices):
    require(type(vertices) is frozenset and vertices,
            "piece is empty or not a frozenset")
    require(vertices <= inventory.graph.vertices,
            "piece contains a foreign vertex")
    edges = induced_edges(inventory.graph.edges, vertices)
    require(connected(vertices, edges), "piece is disconnected")
    raw = biconnected_edge_blocks(vertices, edges)
    local_blocks = tuple(classify_block(index, current)
                         for index, current in enumerate(raw))
    rank = graph_rank(vertices, edges)
    require(rank == sum(current.rank for current in local_blocks),
            "piece rank is not additive over local blocks")
    positive = tuple(current for current in local_blocks if current.rank)
    return LocalAnalysis(vertices, edges, local_blocks, rank, positive)


def local_positive_edge_sets(analysis):
    return frozenset(current.edges for current in analysis.positive_blocks)


# ---------------------------------------------------------------------------
# Recursively immutable production certificate records.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BlockRef:
    kind: str
    vertices: frozenset
    edges: frozenset
    rank: int


@dataclass(frozen=True, slots=True)
class PieceReceipt:
    phase: str
    category: str
    vertices: frozenset
    rank: int
    floor: int
    strict: bool
    contract_id: str
    owned_blocks: tuple[frozenset, ...]


@dataclass(frozen=True, slots=True)
class FirstK2Side:
    bridge_edge: frozenset
    vertices: frozenset
    diamond_blocks: tuple[frozenset, ...]
    triangle_blocks: tuple[frozenset, ...]
    rank: int
    receipt: PieceReceipt


@dataclass(frozen=True, slots=True)
class OwnerComponent:
    owner_vertex: object
    vertices: frozenset


@dataclass(frozen=True, slots=True)
class DiamondOpening:
    boundary_block: frozenset
    upstream_cut: object
    owner_components: tuple[OwnerComponent, ...]
    downstream_vertices: frozenset
    anchor_vertices: frozenset
    residual_edges: frozenset
    delta: int
    eta: int
    rank: int
    receipt: PieceReceipt


@dataclass(frozen=True, slots=True)
class AnchorPacket:
    root_diamond: frozenset
    triangle_blocks: tuple[frozenset, ...]
    vertices: frozenset
    triangle_count: int
    rank: int
    receipt: PieceReceipt


@dataclass(frozen=True, slots=True)
class RootCertificate:
    root_diamond: frozenset
    other_diamond: frozenset
    first_k2_sides: tuple[FirstK2Side, ...]
    root_vertices: frozenset
    opening: DiamondOpening | None
    anchor: AnchorPacket
    final_parts: tuple[frozenset, ...]
    lower_integer: int
    tree_debit: int
    strict: bool
    contracts: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class R221Certificate:
    schema: str
    profile: str
    graph_vertices: frozenset
    graph_edges: frozenset
    diamonds: tuple[BlockRef, BlockRef]
    triangles: tuple[BlockRef, BlockRef, BlockRef]
    roots: tuple[RootCertificate, RootCertificate]
    contract_manifest_sha256: str
    source_manifest_sha256: str


def block_ref(current):
    return BlockRef(current.kind, current.vertices, current.edges, current.rank)


def block_sort_key(index, inventory):
    return edge_set_key(block(inventory, index).edges)


def verify_partition(inventory, target, pieces, label):
    require(type(target) is frozenset and target,
            f"{label} target is malformed")
    require(type(pieces) is tuple and pieces and
            all(type(side) is frozenset and side for side in pieces),
            f"{label} contains an empty or malformed piece")
    union = set().union(*pieces)
    require(union == set(target), f"{label} is not exhaustive")
    require(sum(len(side) for side in pieces) == len(union),
            f"{label} pieces overlap")
    for side in pieces:
        require(side <= target, f"{label} piece escapes target")
        current_edges = induced_edges(inventory.graph.edges, side)
        require(connected(side, current_edges),
                f"{label} piece is disconnected")
        require(current_edges == frozenset(
            current for current in inventory.graph.edges if current <= side),
            f"{label} piece is not induced")
    return True


# ---------------------------------------------------------------------------
# First physical K2 split and exact complete-away receipts.
# ---------------------------------------------------------------------------


def first_external_bridges(inventory, rooting, root_index):
    external = tuple(index for index in positive_ids(inventory)
                     if index != root_index)
    selected = set()
    for index in external:
        route = path_from_root(rooting, ("B", index))
        bridge_nodes = tuple(node for node in route
                             if node[0] == "B" and
                             block(inventory, node[1]).kind == "bridge")
        if bridge_nodes:
            selected.add(bridge_nodes[0][1])
    result = tuple(sorted(selected, key=lambda index: block_sort_key(index, inventory)))
    nodes = tuple(("B", index) for index in result)
    for left, right in itertools.permutations(nodes, 2):
        require(not is_ancestor(rooting, left, right, strict=True),
                "deduplicated first physical K2 blocks are not an antichain")
    return result


def bridge_away_component(inventory, root_index, bridge_index):
    current = block(inventory, bridge_index)
    require(current.kind == "bridge" and len(current.edges) == 1,
            "away split requested on a non-K2 block")
    physical_edge = next(iter(current.edges))
    remaining = frozenset(inventory.graph.edges - {physical_edge})
    sides = components(inventory.graph.vertices, remaining)
    require(len(sides) == 2,
            "Tarjan K2 block did not split physical adjacency")
    root_vertices = block(inventory, root_index).vertices
    roots = tuple(side for side in sides if root_vertices <= side)
    require(len(roots) == 1,
            "physical K2 orientation from root diamond is ambiguous")
    away = tuple(side for side in sides if side != roots[0])
    require(len(away) == 1, "physical K2 has no unique away component")
    return away[0]


def intact_original_ids(inventory, vertices):
    local_edges = induced_edges(inventory.graph.edges, vertices)
    return tuple(index for index in positive_ids(inventory)
                 if block(inventory, index).edges <= local_edges)


def away_receipt(inventory, vertices):
    analysis = analyze_piece(inventory, vertices)
    intact = intact_original_ids(inventory, vertices)
    expected = frozenset(block(inventory, index).edges for index in intact)
    require(local_positive_edge_sets(analysis) == expected and
            len(analysis.positive_blocks) == len(intact),
            "first-K2 away side has a split, merged, or manufactured positive block")
    diamonds = tuple(sorted((index for index in intact
                             if block(inventory, index).kind == "diamond"),
                            key=lambda index: block_sort_key(index, inventory)))
    triangles = tuple(sorted((index for index in intact
                              if block(inventory, index).kind == "triangle"),
                             key=lambda index: block_sort_key(index, inventory)))
    expected_rank = 2 * len(diamonds) + len(triangles)
    require((diamonds or triangles) and analysis.rank == expected_rank and
            1 <= analysis.rank <= 5,
            "first-K2 away side lacks exact positive rank in 1..5")
    owned = tuple(sorted((block(inventory, index).edges for index in intact),
                         key=edge_set_key))
    if analysis.rank == 1:
        require(not diamonds and len(triangles) == 1,
                "rank-one away side is not exactly one literal triangle")
        contract_id = "R221-TRIANGULAR-BLOCK-v1"
        category = "triangle-away-positive"
    else:
        contract_id = f"R221-CONNECTED-RANK{analysis.rank}-v1"
        require(contract_id in CONTRACTS,
                "complete-away rank has no authenticated contract")
        category = f"rank{analysis.rank}-away-nonnegative"
    contract = CONTRACTS[contract_id]
    require(contract.floor == 0,
            "complete-away contract does not have zero floor")
    receipt = PieceReceipt("first-K2", category, vertices, analysis.rank,
                           0, contract.strict, contract_id, owned)
    return receipt, diamonds, triangles


def construct_first_k2(inventory, rooting, root_index):
    selected = first_external_bridges(inventory, rooting, root_index)
    preliminary = tuple((index,
                         next(iter(block(inventory, index).edges)),
                         bridge_away_component(inventory, root_index, index))
                        for index in selected)
    away_sets = tuple(row[2] for row in preliminary)
    removed_edges = frozenset(row[1] for row in preliminary)
    require(len(removed_edges) == len(preliminary),
            "first-K2 deletion contains a duplicate physical edge")
    simultaneous = components(
        inventory.graph.vertices,
        frozenset(inventory.graph.edges - removed_edges))
    root_block_vertices = block(inventory, root_index).vertices
    roots = tuple(side for side in simultaneous
                  if root_block_vertices <= side)
    require(len(roots) == 1,
            "simultaneous first-K2 root component is ambiguous")
    root_vertices = roots[0]
    require(frozenset(simultaneous) ==
            frozenset((root_vertices, *away_sets)),
            "individual and simultaneous first-K2 splits disagree")
    verify_partition(inventory, inventory.graph.vertices,
                     (root_vertices, *away_sets),
                     "simultaneous first-K2 partition")

    sides = []
    for bridge_index, physical_edge, vertices in preliminary:
        receipt, diamonds, triangles = away_receipt(inventory, vertices)
        sides.append(FirstK2Side(
            physical_edge,
            vertices,
            tuple(block(inventory, index).edges for index in diamonds),
            tuple(block(inventory, index).edges for index in triangles),
            receipt.rank,
            receipt,
        ))
    sides.sort(key=lambda side: edge_key(side.bridge_edge))

    for index in positive_ids(inventory):
        if block(inventory, index).edges <= induced_edges(
                inventory.graph.edges, root_vertices):
            route = path_from_root(rooting, ("B", index))
            require(not any(node[0] == "B" and
                            block(inventory, node[1]).kind == "bridge"
                            for node in route),
                    "retained positive block still has a K2 on its root route")
    return tuple(sides), root_vertices


# ---------------------------------------------------------------------------
# Exact second-diamond owner split, manufactured entry triangle, and anchor.
# ---------------------------------------------------------------------------


def diamond_internal_degree(inventory, diamond_index, vertex):
    current = block(inventory, diamond_index)
    require(current.kind == "diamond" and vertex in current.vertices,
            "diamond degree requested outside literal diamond")
    return sum(vertex in physical_edge for physical_edge in current.edges)


def owner_components_at_boundary(inventory, root_vertices, boundary_index):
    boundary = block(inventory, boundary_index)
    require(boundary.kind == "diamond",
            "R221 boundary opening requires a literal diamond")
    current_edges = induced_edges(inventory.graph.edges, root_vertices)
    require(boundary.edges <= current_edges,
            "boundary diamond is not intact in root territory")
    owner_sides = components(root_vertices,
                             frozenset(current_edges - boundary.edges))
    by_vertex = {}
    for side in owner_sides:
        hits = side & boundary.vertices
        require(len(hits) == 1,
                "outside component meets maximal diamond at multiple vertices")
        owner = next(iter(hits))
        require(owner not in by_vertex,
                "diamond vertex has duplicate outside owner component")
        by_vertex[owner] = side
    require(set(by_vertex) == set(boundary.vertices) and
            len(owner_sides) == 4,
            "diamond boundary decomposition omitted or duplicated an owner")
    return by_vertex


def construct_opening(inventory, rooting, root_vertices, boundary_index):
    boundary = block(inventory, boundary_index)
    cut = upstream_cut(inventory, rooting, boundary_index)
    require(cut in root_vertices,
            "boundary upstream cut escaped root territory")
    by_vertex = owner_components_at_boundary(
        inventory, root_vertices, boundary_index)
    downstream = frozenset().union(
        *(side for owner, side in by_vertex.items() if owner != cut))
    anchor_vertices = by_vertex[cut]
    require(downstream and cut not in downstream,
            "opened diamond side is empty or copied its upstream cut")
    require(boundary.vertices - {cut} <= downstream,
            "opened diamond side omitted a non-cut diamond vertex")
    verify_partition(inventory, root_vertices,
                     (anchor_vertices, downstream),
                     "second-diamond owner partition")

    degree = diamond_internal_degree(inventory, boundary_index, cut)
    require(degree in (2, 3),
            "literal diamond entry has impossible internal degree")
    delta = 1 if degree == 2 else 0
    residual_vertices = boundary.vertices - {cut}
    residual_edges = induced_edges(boundary.edges, residual_vertices)
    residual_degrees = {
        vertex: sum(vertex in current for current in residual_edges)
        for vertex in residual_vertices
    }
    if delta:
        require(len(residual_edges) == 3 and len(residual_vertices) == 3 and
                all(value == 2 for value in residual_degrees.values()),
                "degree-two diamond entry did not manufacture a literal triangle")
    else:
        require(len(residual_edges) == 2 and len(residual_vertices) == 3 and
                sorted(residual_degrees.values()) == [1, 1, 2],
                "degree-three diamond entry did not leave a three-vertex path")

    analysis = analyze_piece(inventory, downstream)
    captured_triangles = tuple(sorted(
        (index for index in inventory.triangles
         if block(inventory, index).edges <= analysis.edges),
        key=lambda index: block_sort_key(index, inventory)))
    eta = len(captured_triangles)
    expected_positive = {block(inventory, index).edges
                         for index in captured_triangles}
    if delta:
        expected_positive.add(residual_edges)
    require(local_positive_edge_sets(analysis) == frozenset(expected_positive),
            "opened diamond side positive blocks disagree with delta/eta inventory")
    require(all(current.kind == "triangle"
                for current in analysis.positive_blocks),
            "opened diamond side is not triangular after the exact opening")
    require(analysis.rank == delta + eta,
            "opened diamond side rank is not delta+eta")

    owned = tuple(sorted((block(inventory, index).edges
                          for index in captured_triangles), key=edge_set_key))
    if analysis.rank == 0:
        require(delta == 0 and eta == 0 and
                len(analysis.edges) == len(analysis.vertices) - 1 and
                not analysis.positive_blocks,
                "tree-debit opening is not a nonempty tree")
        receipt = PieceReceipt(
            "second-diamond", "tree-debit", downstream, 0, -1, False,
            "R221-TREE-EXACT-v1", owned)
    else:
        require(analysis.positive_blocks,
                "positive opened side has no triangular block")
        receipt = PieceReceipt(
            "second-diamond", "triangular-open-side-positive", downstream,
            analysis.rank, 0, True, "R221-TRIANGULAR-BLOCK-v1", owned)

    owners = tuple(OwnerComponent(owner, by_vertex[owner])
                   for owner in sorted(by_vertex, key=vertex_key))
    return DiamondOpening(
        boundary.edges,
        cut,
        owners,
        downstream,
        anchor_vertices,
        residual_edges,
        delta,
        eta,
        analysis.rank,
        receipt,
    )


def construct_anchor(inventory, rooting, root_index, anchor_vertices,
                     excluded_diamond_index):
    analysis = analyze_piece(inventory, anchor_vertices)
    root = block(inventory, root_index)
    require(root.edges <= analysis.edges,
            "anchor omitted its root literal diamond")
    require(block(inventory, excluded_diamond_index).edges not in
            local_positive_edge_sets(analysis),
            "anchor retained the second diamond after opening/away split")
    triangle_ids = tuple(sorted(
        (index for index in inventory.triangles
         if block(inventory, index).edges <= analysis.edges),
        key=lambda index: block_sort_key(index, inventory)))
    expected = frozenset({root.edges,
                          *(block(inventory, index).edges
                            for index in triangle_ids)})
    require(local_positive_edge_sets(analysis) == expected and
            len(analysis.positive_blocks) == 1 + len(triangle_ids),
            "anchor positive inventory is not exactly D+T^k")
    k = len(triangle_ids)
    require(0 <= k <= 3 and analysis.rank == 2 + k,
            "anchor does not have exact rank 2+k for 0<=k<=3")
    for index in triangle_ids:
        route = path_from_root(rooting, ("B", index))
        require(not any(node[0] == "B" and
                        block(inventory, node[1]).kind == "bridge"
                        for node in route),
                "anchor triangle has a physical K2 on its root route")
    owned = (root.edges, *(block(inventory, index).edges
                           for index in triangle_ids))
    owned = tuple(sorted(owned, key=edge_set_key))
    receipt = PieceReceipt(
        "anchor", f"strict-D+T{k}-root", anchor_vertices, analysis.rank,
        1, True, "R221-DIAMOND-T0T3-ROOT-v1", owned)
    return AnchorPacket(
        root.edges,
        tuple(block(inventory, index).edges for index in triangle_ids),
        anchor_vertices,
        k,
        analysis.rank,
        receipt,
    )


def audit_original_ownership(inventory, root_index, other_index,
                             sides, opening, anchor, final_parts):
    verify_partition(inventory, inventory.graph.vertices, final_parts,
                     "final original-vertex partition")
    for cut in inventory.cuts:
        require(sum(cut in side for side in final_parts) == 1,
                "physical articulation has nonunique final owner")
    piece_edges = tuple(induced_edges(inventory.graph.edges, side)
                        for side in final_parts)
    root_edges = block(inventory, root_index).edges
    require(sum(root_edges <= current for current in piece_edges) == 1 and
            root_edges <= induced_edges(inventory.graph.edges, anchor.vertices),
            "root diamond lacks unique intact final owner")
    for triangle_index in inventory.triangles:
        triangle_edges = block(inventory, triangle_index).edges
        require(sum(triangle_edges <= current for current in piece_edges) == 1,
                "literal triangle lacks unique intact final owner")
    other_edges = block(inventory, other_index).edges
    if opening is None:
        require(sum(other_edges <= current for current in piece_edges) == 1,
                "away second diamond lacks unique intact owner")
    else:
        require(sum(other_edges <= current for current in piece_edges) == 0,
                "opened second diamond was incorrectly retained intact")
        require(opening.residual_edges <= induced_edges(
                    inventory.graph.edges, opening.downstream_vertices),
                "opened second-diamond residual edges escaped downstream")
        cross = frozenset(current for current in other_edges
                          if not current <= opening.downstream_vertices and
                          not current <= opening.anchor_vertices)
        require(cross == other_edges - opening.residual_edges,
                "second-diamond crossing/residual edge split changed")
    # Every away-side stored inventory is physical and complete.
    for side in sides:
        require(side.receipt.vertices == side.vertices and
                side.rank == side.receipt.rank,
                "first-K2 side and receipt disagree")
    return True


def construct_root_certificate(inventory, root_index):
    require(root_index in inventory.diamonds,
            "R221 replay root is not a literal diamond")
    other_index = next(index for index in inventory.diamonds
                       if index != root_index)
    rooting = root_block_cut_tree(inventory, root_index)
    sides, root_vertices = construct_first_k2(
        inventory, rooting, root_index)
    root_edges = induced_edges(inventory.graph.edges, root_vertices)
    other_retained = block(inventory, other_index).edges <= root_edges
    opening = (construct_opening(inventory, rooting, root_vertices, other_index)
               if other_retained else None)
    anchor_vertices = (opening.anchor_vertices if opening is not None
                       else root_vertices)
    anchor = construct_anchor(inventory, rooting, root_index,
                              anchor_vertices, other_index)
    final_parts = (anchor.vertices,
                   *((opening.downstream_vertices,) if opening is not None else ()),
                   *(side.vertices for side in sides))
    audit_original_ownership(inventory, root_index, other_index,
                             sides, opening, anchor, final_parts)

    receipts = (anchor.receipt,
                *((opening.receipt,) if opening is not None else ()),
                *(side.receipt for side in sides))
    for receipt in receipts:
        require(receipt.contract_id in CONTRACTS,
                "piece receipt cites an unknown analytic contract")
        contract = CONTRACTS[receipt.contract_id]
        require(receipt.floor == contract.floor and
                receipt.strict == contract.strict,
                "piece receipt floor/strictness disagrees with pinned contract")
    tree_debit = int(opening is not None and opening.receipt.floor == -1)
    require(tree_debit in (0, 1),
            "R221 root has more than one tree debit")
    lower = sum(receipt.floor for receipt in receipts)
    require(lower == 1 - tree_debit and lower in (0, 1),
            "strict R221 ledger is not 1-tree_debit in {0,1}")
    require(anchor.receipt.strict,
            "R221 ledger lacks its strict D+T^k anchor")
    used = dependency_closure({
        "R221-RESIDUAL-SIEVE-v1",
        "R221-INDUCED-SUPERADD-v1",
        *(receipt.contract_id for receipt in receipts),
    })
    return RootCertificate(
        block(inventory, root_index).edges,
        block(inventory, other_index).edges,
        sides,
        root_vertices,
        opening,
        anchor,
        final_parts,
        lower,
        tree_debit,
        True,
        used,
    )


def construct_certificate(inventory):
    diamond_ids = tuple(sorted(inventory.diamonds,
                               key=lambda index: block_sort_key(index, inventory)))
    triangle_ids = tuple(sorted(inventory.triangles,
                                key=lambda index: block_sort_key(index, inventory)))
    require(len(diamond_ids) == 2 and len(triangle_ids) == 3,
            "R221 canonical inventory count changed")
    roots = tuple(construct_root_certificate(inventory, index)
                  for index in diamond_ids)
    require(len(roots) == 2 and
            {item.root_diamond for item in roots} ==
            {block(inventory, index).edges for index in diamond_ids},
            "both physical root diamonds were not replayed exactly once")
    return R221Certificate(
        SCHEMA,
        PROFILE,
        inventory.graph.vertices,
        inventory.graph.edges,
        tuple(block_ref(block(inventory, index)) for index in diamond_ids),
        tuple(block_ref(block(inventory, index)) for index in triangle_ids),
        roots,
        EXPECTED_FULL_CONTRACT_MANIFEST_SHA256,
        EXPECTED_SOURCE_MANIFEST_SHA256,
    )


def audit_certificate(vertices, edges, certificate):
    audit_sources()
    require(type(certificate) is R221Certificate,
            "supplied certificate has wrong record type")
    require_recursively_immutable(certificate)
    fresh_inventory = reconstruct(vertices, edges)
    fresh = construct_certificate(fresh_inventory)
    require(certificate == fresh,
            "independent adjacency certificate replay disagrees")
    require(certificate.contract_manifest_sha256 ==
            EXPECTED_FULL_CONTRACT_MANIFEST_SHA256 and
            certificate.source_manifest_sha256 ==
            EXPECTED_SOURCE_MANIFEST_SHA256,
            "certificate manifest anchors changed")
    return True


def verify(vertices: frozenset, edges: frozenset):
    """Production adjacency-only R221 gate; no semantic metadata is accepted."""
    audit_sources()
    inventory = reconstruct(vertices, edges)
    certificate = construct_certificate(inventory)
    # Reconstruct and replay rather than trusting freshly stored plan fields.
    audit_certificate(vertices, edges, certificate)
    require_recursively_immutable(certificate)
    return certificate


# ---------------------------------------------------------------------------
# Independent physical fixture builder and semantic signatures.
# ---------------------------------------------------------------------------


def add_cycle(edges, vertices):
    require(len(vertices) >= 3 and len(set(vertices)) == len(vertices),
            "bad generated cycle")
    edges.update(edge(vertices[index], vertices[(index + 1) % len(vertices)])
                 for index in range(len(vertices)))


class Builder:
    def __init__(self):
        self.vertices = set()
        self.edges = set()
        self.serial = 0
        self.routing = []
        self.positive = []

    def fresh(self, prefix):
        require(type(prefix) is str and prefix,
                "fixture vertex prefix malformed")
        vertex = (prefix, self.serial)
        self.serial += 1
        self.vertices.add(vertex)
        return vertex

    def diamond(self, port=None, entry_orbit="degree3"):
        require(entry_orbit in ("degree2", "degree3"),
                "unknown diamond entry orbit")
        if port is not None:
            self.vertices.add(port)
        if entry_orbit == "degree3":
            x = port if port is not None else self.fresh("DX")
            y = self.fresh("DY")
            a = self.fresh("DA")
            b = self.fresh("DB")
        else:
            a = port if port is not None else self.fresh("DA")
            x = self.fresh("DX")
            y = self.fresh("DY")
            b = self.fresh("DB")
        self.vertices.update((x, y, a, b))
        self.edges.update({edge(x, y), edge(x, a), edge(a, y),
                           edge(x, b), edge(b, y)})
        result = (x, y, a, b)
        self.positive.append(("D", result))
        return result

    def triangle(self, port=None):
        if port is None:
            root = self.fresh("TX")
        else:
            root = port
            self.vertices.add(port)
        left = self.fresh("TA")
        right = self.fresh("TB")
        result = (root, left, right)
        add_cycle(self.edges, result)
        self.positive.append(("T", result))
        return result

    def cycle(self, length, port=None):
        require(type(length) is int and length >= 3,
                "fixture cycle length malformed")
        vertices = ([port] if port is not None else [])
        if port is not None:
            self.vertices.add(port)
        vertices.extend(self.fresh(f"C{length}")
                        for _ in range(length - len(vertices)))
        add_cycle(self.edges, vertices)
        self.positive.append((f"C{length}", tuple(vertices)))
        return tuple(vertices)

    def theta_122_plus(self, r, port=None):
        """Unsupported Theta(1,2,r) fixture for hostile profile tests."""
        require(type(r) is int and r >= 2, "hostile theta r malformed")
        x = port if port is not None else self.fresh("UX")
        if port is not None:
            self.vertices.add(port)
        y = self.fresh("UY")
        short = self.fresh("US")
        long = [self.fresh("UL") for _ in range(r - 1)]
        self.edges.update({edge(x, y), edge(x, short), edge(short, y)})
        sequence = (x, *long, y)
        self.edges.update(edge(left, right)
                          for left, right in zip(sequence, sequence[1:]))
        self.positive.append((f"Theta{r}", (x, y, short, *long)))
        return (x, y, short, *long)

    def bridge_path(self, left, right, length):
        require(type(length) is int and length >= 1,
                "fixture bridge length must be a positive integer")
        self.vertices.update((left, right))
        internal = [self.fresh("R") for _ in range(length - 1)]
        sequence = (left, *internal, right)
        self.edges.update(edge(a, b) for a, b in zip(sequence, sequence[1:]))
        self.routing.extend(internal)
        return sequence

    def tree_payload(self, root, count, style=0):
        require(root in self.vertices and type(count) is int and count >= 0,
                "fixture payload request malformed")
        made = []
        for index in range(count):
            if style % 4 == 0:
                parent = root if index == 0 or index % 5 == 0 else made[index - 1]
            elif style % 4 == 1:
                parent = root if index < 3 or index % 4 == 0 else made[(index - 1) // 2]
            elif style % 4 == 2:
                parent = root if index == 0 else made[max(0, index // 3)]
            else:
                parent = root if index % 2 == 0 else made[-1]
            vertex = self.fresh("P")
            self.edges.add(edge(parent, vertex))
            made.append(vertex)
        return tuple(made)

    def graph(self):
        return frozenset(self.vertices), frozenset(self.edges)


@dataclass(frozen=True, slots=True)
class FixtureCase:
    name: str
    graph: tuple[frozenset, frozenset]
    tags: tuple[str, ...]


def add_standard_payloads(builder, roots, scale=5):
    roots = tuple(roots)
    for index, root in enumerate(roots[:6]):
        builder.tree_payload(root, max(1, min(scale, index + 2)), index)
    for index, route_vertex in enumerate(builder.routing[:4]):
        builder.tree_payload(route_vertex, max(1, min(scale, index + 1)), index + 7)


def entry_fixture(entry_orbit, eta, mode="separate", payload=0):
    require(entry_orbit in ("degree2", "degree3") and
            type(eta) is int and 0 <= eta <= 3,
            "entry fixture request malformed")
    require(mode in ("separate", "repeated", "nested"),
            "entry fixture mode malformed")
    builder = Builder()
    root = builder.diamond()
    second = builder.diamond(root[0], entry_orbit)
    private = tuple(vertex for vertex in second if vertex != root[0])
    triangles = []
    downstream = []
    for index in range(eta):
        if mode == "nested" and downstream:
            port = downstream[-1][1]
        elif mode == "repeated":
            port = private[0]
        else:
            port = private[index % len(private)]
        current = builder.triangle(port)
        triangles.append(current)
        downstream.append(current)
    for index in range(3 - eta):
        port = root[1] if mode == "repeated" else root[1 + (index % 3)]
        triangles.append(builder.triangle(port))
    if payload:
        roots = [root[-1], second[-1], *(item[-1] for item in triangles)]
        add_standard_payloads(builder, roots, payload)
    tags = (f"entry-{entry_orbit}", f"eta-{eta}", mode)
    return FixtureCase(f"entry-{entry_orbit}-eta{eta}-{mode}",
                       builder.graph(), tags)


def away_rank_fixture(rank, length=3, payload=0, variant="diamond"):
    require(type(rank) is int and 1 <= rank <= 5,
            "away-rank fixture request malformed")
    builder = Builder()
    root = builder.diamond()
    hub = builder.fresh("HUB")
    builder.bridge_path(root[0], hub, length)
    group_diamond = rank >= 2 and variant == "diamond"
    group_triangles = rank - (2 if group_diamond else 0)
    if not group_diamond:
        require(rank <= 3, "triangle-only away fixture rank exceeds inventory")
    require(0 <= group_triangles <= 3,
            "away fixture triangle count impossible")
    if group_diamond:
        second = builder.diamond(hub, "degree3")
    else:
        second = builder.diamond(root[1], "degree2")
    triangles = []
    for _ in range(group_triangles):
        triangles.append(builder.triangle(hub))
    for index in range(3 - group_triangles):
        triangles.append(builder.triangle(root[1 + (index % 3)]))
    if payload:
        roots = [root[-1], second[-1], hub,
                 *(item[-1] for item in triangles)]
        add_standard_payloads(builder, roots, payload)
    return FixtureCase(
        f"away-rank{rank}-{variant}-L{length}-P{payload}",
        builder.graph(),
        (f"away-rank-{rank}", "physical-K2", variant),
    )


def common_cut_fixture(payload=0):
    builder = Builder()
    root = builder.diamond()
    cut = root[0]
    second = builder.diamond(cut, "degree2")
    triangles = [builder.triangle(cut) for _ in range(3)]
    if payload:
        add_standard_payloads(builder,
                              [root[-1], second[-1],
                               *(item[-1] for item in triangles)], payload)
    return FixtureCase("all-five-common-cut", builder.graph(),
                       ("repeated-cut", "common-cut", "entry-degree2"))


def nested_chain_fixture(with_bridge=False, payload=0):
    builder = Builder()
    root = builder.diamond()
    first = builder.triangle(root[0])
    if with_bridge:
        second = builder.diamond()
        builder.bridge_path(first[1], second[0], 5)
    else:
        second = builder.diamond(first[1], "degree3")
    middle = builder.triangle(second[2])
    last = builder.triangle(middle[1])
    if payload:
        add_standard_payloads(builder,
                              [root[-1], first[-1], second[-1],
                               middle[-1], last[-1]], payload)
    return FixtureCase(
        "nested-chain-bridge" if with_bridge else "nested-chain-shared",
        builder.graph(),
        ("nested", "triangle-between-diamonds",
         "physical-K2" if with_bridge else "shared-cut"),
    )


def separate_arms_fixture(payload=0):
    builder = Builder()
    root = builder.diamond()
    blocks = []
    second = builder.diamond()
    builder.bridge_path(root[0], second[0], 2)
    blocks.append(second)
    for index, length in enumerate((3, 5, 7)):
        triangle = builder.triangle()
        builder.bridge_path(root[1 + index], triangle[0], length)
        blocks.append(triangle)
    if payload:
        add_standard_payloads(builder,
                              [root[-1], *(item[-1] for item in blocks)], payload)
    return FixtureCase("four-separate-K2-arms", builder.graph(),
                       ("separate-arms", "physical-K2"))


def shared_prefix_fixture(length=5, payload=0, later_bridge=True):
    builder = Builder()
    root = builder.diamond()
    hub = builder.fresh("HUB")
    route = builder.bridge_path(root[0], hub, length)
    second = builder.diamond(hub, "degree3")
    first = builder.triangle(hub)
    if later_bridge:
        subhub = builder.fresh("SUB")
        builder.bridge_path(hub, subhub, 3)
        second_triangle = builder.triangle(subhub)
        third_triangle = builder.triangle(second_triangle[1])
    else:
        second_triangle = builder.triangle(hub)
        third_triangle = builder.triangle(hub)
    if payload:
        roots = [root[-1], second[-1], first[-1], second_triangle[-1],
                 third_triangle[-1], hub, *route[1:-1]]
        add_standard_payloads(builder, roots, payload)
    return FixtureCase(
        f"shared-prefix-L{length}-P{payload}-later{int(later_bridge)}",
        builder.graph(),
        ("shared-prefix", "away-rank-5", "later-K2" if later_bridge else "common-away-cut"),
    )


def mixed_prefix_fixture(payload=0):
    builder = Builder()
    root = builder.diamond()
    hub = builder.fresh("MH")
    builder.bridge_path(root[0], hub, 4)
    second = builder.diamond(hub, "degree2")
    t1 = builder.triangle(hub)
    t2 = builder.triangle(root[1])
    t3 = builder.triangle(t2[1])
    if payload:
        add_standard_payloads(builder,
                              [root[-1], second[-1], t1[-1], t2[-1], t3[-1], hub],
                              payload)
    return FixtureCase("mixed-shared-prefix-and-root-nesting", builder.graph(),
                       ("shared-prefix", "nested", "mixed"))


def fixture_universe():
    cases = []
    cases.append(common_cut_fixture(payload=6))
    for orbit in ("degree2", "degree3"):
        for eta in range(4):
            mode = "separate"
            cases.append(entry_fixture(orbit, eta, mode, payload=4))
        cases.append(entry_fixture(orbit, 3, "repeated", payload=3))
        cases.append(entry_fixture(orbit, 3, "nested", payload=3))
    for rank in range(1, 6):
        cases.append(away_rank_fixture(rank, length=rank + 1, payload=4))
    cases.append(away_rank_fixture(2, length=6, payload=2,
                                   variant="triangles"))
    cases.append(away_rank_fixture(3, length=4, payload=2,
                                   variant="triangles"))
    cases.append(separate_arms_fixture(payload=5))
    cases.append(shared_prefix_fixture(length=5, payload=7, later_bridge=True))
    cases.append(shared_prefix_fixture(length=1, payload=2, later_bridge=False))
    cases.append(mixed_prefix_fixture(payload=6))
    cases.append(nested_chain_fixture(with_bridge=False, payload=5))
    cases.append(nested_chain_fixture(with_bridge=True, payload=5))
    for length in (1, 2, 7, 257):
        cases.append(away_rank_fixture(5, length=length, payload=2))
    cases.append(shared_prefix_fixture(length=2049, payload=12,
                                       later_bridge=True))
    names = tuple(item.name for item in cases)
    require(len(names) == len(set(names)),
            "fixture universe contains a duplicate name")
    return tuple(cases)


def opaque_relabel(vertices, edges, salt):
    require(type(salt) is int, "opaque relabel salt malformed")
    ordered = sorted(vertices,
                     key=lambda vertex: sha256_bytes(
                         str(salt).encode("ascii") + b"\0" + atom_bytes(vertex)))
    mapping = {vertex: ("opaque", salt, 1009 * index + 17)
               for index, vertex in enumerate(ordered)}
    new_vertices = frozenset(mapping[vertex] for vertex in vertices)
    new_edges = frozenset(frozenset(mapping[vertex] for vertex in current)
                          for current in edges)
    return new_vertices, new_edges


def semantic_signature(certificate):
    roots = []
    for root in certificate.roots:
        away = tuple(sorted((
            side.rank,
            len(side.diamond_blocks),
            len(side.triangle_blocks),
            len(side.vertices),
            side.receipt.contract_id,
        ) for side in root.first_k2_sides))
        opening = (None if root.opening is None else (
            root.opening.delta,
            root.opening.eta,
            root.opening.rank,
            len(root.opening.downstream_vertices),
            root.opening.receipt.category,
        ))
        roots.append((
            away,
            opening,
            root.anchor.triangle_count,
            root.anchor.rank,
            len(root.anchor.vertices),
            root.tree_debit,
            root.lower_integer,
            root.contracts,
        ))
    roots.sort(key=lambda item: json.dumps(canonical_value(item),
                                           ensure_ascii=True,
                                           separators=(",", ":")))
    return (certificate.profile, tuple(roots))


# ---------------------------------------------------------------------------
# Fixture audit, hostile mutations, static audit, and deterministic report.
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class AuditResult:
    fixture_count: int
    relabel_count: int
    root_replays: int
    away_ranks: tuple[int, ...]
    entry_deltas: tuple[int, ...]
    entry_etas: tuple[int, ...]
    anchor_triangle_counts: tuple[int, ...]
    tree_debits: tuple[int, ...]
    max_connector_length: int
    semantic_suite_sha256: str
    hostile_rejections: tuple[str, ...]
    source_files: int
    static_checks: int


def audit_fixtures():
    signatures = []
    away_ranks = set()
    deltas = set()
    etas = set()
    anchor_counts = set()
    tree_debits = set()
    relabels = 0
    roots = 0
    max_connector = 0
    tag_counts = Counter()
    cases = fixture_universe()
    for index, case in enumerate(cases):
        vertices, edges = case.graph
        certificate = verify(vertices, edges)
        require(len(certificate.roots) == 2,
                "fixture did not replay both root diamonds")
        roots += len(certificate.roots)
        for tag in case.tags:
            tag_counts[tag] += 1
        for root in certificate.roots:
            away_ranks.update(side.rank for side in root.first_k2_sides)
            anchor_counts.add(root.anchor.triangle_count)
            tree_debits.add(root.tree_debit)
            if root.opening is not None:
                deltas.add(root.opening.delta)
                etas.add(root.opening.eta)
        signatures.append((case.name, semantic_signature(certificate)))
        relabeled_graph = opaque_relabel(vertices, edges, 101 + 37 * index)
        relabeled = verify(*relabeled_graph)
        require(semantic_signature(certificate) == semantic_signature(relabeled),
                f"opaque relabeling changed semantic certificate: {case.name}")
        relabels += 1
        if "L2049" in case.name:
            max_connector = max(max_connector, 2049)
        elif "L257" in case.name:
            max_connector = max(max_connector, 257)
    require(away_ranks == {1, 2, 3, 4, 5},
            "fixture universe did not cover complete-away ranks 1..5")
    require(deltas == {0, 1},
            "fixture universe did not cover both diamond entry orbits")
    require(etas == {0, 1, 2, 3},
            "fixture universe did not cover opened-side eta 0..3")
    require(anchor_counts == {0, 1, 2, 3},
            "fixture universe did not cover anchor D+T^k for k=0..3")
    require(tree_debits == {0, 1},
            "fixture universe did not cover both tree-debit states")
    for mandatory in ("shared-prefix", "nested", "repeated-cut",
                      "separate-arms", "later-K2"):
        require(tag_counts[mandatory] > 0,
                f"fixture universe omitted mandatory topology: {mandatory}")
    require(max_connector >= 2049,
            "fixture universe omitted a recursion-hostile long K2 chain")
    suite_digest = sha256_bytes(json.dumps(
        canonical_value(tuple(signatures)), ensure_ascii=True,
        separators=(",", ":")).encode("utf-8"))
    return (len(cases), relabels, roots, tuple(sorted(away_ranks)),
            tuple(sorted(deltas)), tuple(sorted(etas)),
            tuple(sorted(anchor_counts)), tuple(sorted(tree_debits)),
            max_connector, suite_digest)


def replace_root(certificate, index, new_root):
    roots = list(certificate.roots)
    roots[index] = new_root
    return replace(certificate, roots=tuple(roots))


def hostile_tests():
    rejected = []
    base_case = entry_fixture("degree2", 2, "nested", payload=8)
    base_vertices, base_edges = base_case.graph
    base_certificate = verify(base_vertices, base_edges)
    inventory = reconstruct(base_vertices, base_edges)
    root_block = block(inventory, inventory.diamonds[0])
    triangle_block = block(inventory, inventory.triangles[0])

    rejected.append(expect_rejection(
        lambda: verify(set(base_vertices), base_edges),
        "mutable vertex-set API injection",
        "vertices must be a nonempty frozenset"))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, set(base_edges)),
        "mutable edge-set API injection",
        "edges must be a frozenset"))
    only_vertex = next(iter(base_vertices))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) | {frozenset({only_vertex})})),
        "malformed singleton edge",
        "malformed unordered edge"))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) |
                                 {frozenset({only_vertex, ("foreign", 999)})})),
        "foreign edge endpoint",
        "edge endpoint outside vertex set"))
    rejected.append(expect_rejection(
        lambda: verify(frozenset(set(base_vertices) | {True}), base_edges),
        "boolean vertex atom",
        "vertex atom is outside the immutable canonical type grammar"))

    payload_edge = next(current for current in base_edges
                        if any(type(vertex) is tuple and vertex[0] == "P"
                               for vertex in current))
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) - {payload_edge})),
        "disconnected payload mutation",
        "input graph disconnected"))

    # Subdivide a literal diamond edge: rank is preserved but literal typing is not.
    diamond_edge = next(iter(root_block.edges))
    left, right = ordered_vertices(diamond_edge)
    new_vertex = ("hostile-subdivide-D", 1)
    subdivided_vertices = frozenset(set(base_vertices) | {new_vertex})
    subdivided_edges = set(base_edges) - {diamond_edge}
    subdivided_edges |= {edge(left, new_vertex), edge(new_vertex, right)}
    rejected.append(expect_rejection(
        lambda: verify(subdivided_vertices, frozenset(subdivided_edges)),
        "subdivided literal diamond",
        "unsupported positive-rank block type"))

    triangle_edge = next(iter(triangle_block.edges))
    left, right = ordered_vertices(triangle_edge)
    new_vertex = ("hostile-subdivide-T", 2)
    subdivided_vertices = frozenset(set(base_vertices) | {new_vertex})
    subdivided_edges = set(base_edges) - {triangle_edge}
    subdivided_edges |= {edge(left, new_vertex), edge(new_vertex, right)}
    rejected.append(expect_rejection(
        lambda: verify(subdivided_vertices, frozenset(subdivided_edges)),
        "subdivided literal triangle",
        "unsupported positive-rank block type"))

    missing_diamond_edge = next(
        edge(left, right)
        for left, right in itertools.combinations(root_block.vertices, 2)
        if edge(left, right) not in root_block.edges)
    rejected.append(expect_rejection(
        lambda: verify(base_vertices,
                       frozenset(set(base_edges) | {missing_diamond_edge})),
        "completed diamond to K4",
        "input graph does not have cyclomatic rank seven"))

    # Same total rank, wrong positive rank-one block: C4 replaces one triangle.
    builder = Builder()
    d0 = builder.diamond()
    builder.diamond(d0[0], "degree3")
    builder.triangle(d0[1])
    builder.triangle(d0[2])
    builder.cycle(4, d0[3])
    rejected.append(expect_rejection(
        lambda: verify(*builder.graph()),
        "C4 substituted for literal triangle",
        "unsupported positive-rank block type"))

    # Same total rank, unsupported rank-two theta replaces the second diamond.
    builder = Builder()
    d0 = builder.diamond()
    builder.theta_122_plus(3, d0[0])
    builder.triangle(d0[1])
    builder.triangle(d0[2])
    builder.triangle(d0[3])
    rejected.append(expect_rejection(
        lambda: verify(*builder.graph()),
        "non-diamond rank-two theta",
        "unsupported positive-rank block type"))

    # Cross-ear merger changes the physical block inventory and must close.
    diamonds = [block(inventory, index) for index in inventory.diamonds]
    left = next(iter(diamonds[0].vertices - diamonds[1].vertices))
    right = next(iter(diamonds[1].vertices - diamonds[0].vertices))
    cross = edge(left, right)
    rejected.append(expect_rejection(
        lambda: verify(base_vertices, frozenset(set(base_edges) | {cross})),
        "cross-block ear merger",
        "input graph does not have cyclomatic rank seven"))

    # Immutable plan/certificate mutations: independent replay must reject all.
    forged_root = replace(base_certificate.roots[0], lower_integer=99)
    rejected.append(expect_rejection(
        lambda: audit_certificate(base_vertices, base_edges,
                                  replace_root(base_certificate, 0, forged_root)),
        "forged root ledger",
        "independent adjacency certificate replay disagrees"))
    root_with_opening = next((item for item in base_certificate.roots
                              if item.opening is not None), None)
    require(root_with_opening is not None,
            "hostile base lacks retained-diamond opening")
    forged_opening = replace(root_with_opening.opening,
                             delta=1 - root_with_opening.opening.delta)
    forged_root = replace(root_with_opening, opening=forged_opening)
    root_index = base_certificate.roots.index(root_with_opening)
    rejected.append(expect_rejection(
        lambda: audit_certificate(base_vertices, base_edges,
                                  replace_root(base_certificate, root_index,
                                               forged_root)),
        "forged diamond entry orbit",
        "independent adjacency certificate replay disagrees"))
    forged_anchor = replace(base_certificate.roots[0].anchor,
                            triangle_count=99)
    forged_root = replace(base_certificate.roots[0], anchor=forged_anchor)
    rejected.append(expect_rejection(
        lambda: audit_certificate(base_vertices, base_edges,
                                  replace_root(base_certificate, 0, forged_root)),
        "forged anchor triangle count",
        "independent adjacency certificate replay disagrees"))
    rejected.append(expect_rejection(
        lambda: audit_certificate(base_vertices, base_edges,
                                  replace(base_certificate, roots=(
                                      base_certificate.roots[0],
                                      base_certificate.roots[0]))),
        "duplicated root replay",
        "independent adjacency certificate replay disagrees"))
    rejected.append(expect_rejection(
        lambda: audit_certificate(base_vertices, base_edges,
                                  replace(base_certificate,
                                          contract_manifest_sha256="0" * 64)),
        "forged certificate manifest digest",
        "independent adjacency certificate replay disagrees"))

    bridge_case = shared_prefix_fixture(length=8, payload=3,
                                        later_bridge=True)
    bridge_vertices, bridge_edges = bridge_case.graph
    bridge_certificate = verify(bridge_vertices, bridge_edges)
    bridge_root_index = next(index for index, item in
                             enumerate(bridge_certificate.roots)
                             if item.first_k2_sides)
    bridge_root = bridge_certificate.roots[bridge_root_index]
    genuine_side = bridge_root.first_k2_sides[0]
    fake_edge = next(current for current in bridge_edges
                     if current != genuine_side.bridge_edge)
    forged_side = replace(genuine_side, bridge_edge=fake_edge)
    forged_root = replace(bridge_root,
                          first_k2_sides=(forged_side,
                                          *bridge_root.first_k2_sides[1:]))
    rejected.append(expect_rejection(
        lambda: audit_certificate(
            bridge_vertices, bridge_edges,
            replace_root(bridge_certificate, bridge_root_index, forged_root)),
        "forged first physical K2 edge",
        "independent adjacency certificate replay disagrees"))
    forged_vertices = frozenset(set(genuine_side.vertices) -
                                 {next(iter(genuine_side.vertices))})
    forged_side = replace(genuine_side, vertices=forged_vertices)
    forged_root = replace(bridge_root,
                          first_k2_sides=(forged_side,
                                          *bridge_root.first_k2_sides[1:]))
    rejected.append(expect_rejection(
        lambda: audit_certificate(
            bridge_vertices, bridge_edges,
            replace_root(bridge_certificate, bridge_root_index, forged_root)),
        "incomplete complete-away owner set",
        "independent adjacency certificate replay disagrees"))

    # In-memory contract-table mutations, including simultaneous rebinds.
    lookup_original = globals()["CONTRACTS"]
    specs_original = globals()["CONTRACT_SPECS"]
    rank5_id = "R221-CONNECTED-RANK5-v1"
    rank5_original = lookup_original[rank5_id]
    lookup_original[rank5_id] = replace(rank5_original, floor=99)
    try:
        rejected.append(expect_rejection(
            audit_contract_table,
            "analytic lookup floor mutation",
            "analytic contract tuple/lookup disagree"))
    finally:
        lookup_original[rank5_id] = rank5_original

    def rebound_specs(replacement):
        return tuple(replacement if item.contract_id == rank5_id else item
                     for item in specs_original)

    mutations = (
        ("simultaneous unused floor rebind",
         replace(rank5_original, floor=99),
         "analytic full contract manifest changed"),
        ("simultaneous unused claim rebind",
         replace(rank5_original, claim="HOSTILE changed rank-five claim"),
         "analytic full contract manifest changed"),
        ("simultaneous unused strictness rebind",
         replace(rank5_original, strict=True),
         "analytic full contract manifest changed"),
        ("simultaneous dependency rebind",
         replace(rank5_original,
                 depends_on=("R221-TREE-EXACT-v1",)),
         "analytic full contract manifest changed"),
        ("simultaneous Boolean floor rebind",
         replace(rank5_original, floor=True),
         "contract floor malformed"),
        ("simultaneous source path rebind",
         replace(rank5_original, source_path="all-tetracyclic-graphs/paper.tex"),
         "analytic full contract manifest changed"),
        ("simultaneous source digest rebind",
         replace(rank5_original, source_sha256="0" * 64),
         "analytic full contract manifest changed"),
    )
    for label, replacement, expected in mutations:
        mutated_specs = rebound_specs(replacement)
        globals()["CONTRACT_SPECS"] = mutated_specs
        globals()["CONTRACTS"] = {item.contract_id: item
                                  for item in mutated_specs}
        try:
            rejected.append(expect_rejection(
                lambda: verify(base_vertices, base_edges),
                label, expected))
        finally:
            globals()["CONTRACT_SPECS"] = specs_original
            globals()["CONTRACTS"] = lookup_original

    source_contract = lookup_original["R221-RESIDUAL-SIEVE-v1"]
    blob = (SOURCE_ROOT / source_contract.source_path).read_bytes()
    rejected.append(expect_rejection(
        lambda: authenticate_source_blob(blob + b"\nHOSTILE\n",
                                         source_contract.source_sha256,
                                         "synthetic source mutation"),
        "analytic source-byte mutation",
        "analytic source changed"))

    source_root_original = globals()["SOURCE_ROOT"]
    globals()["SOURCE_ROOT"] = source_root_original / "definitely-absent-r221"
    try:
        rejected.append(expect_rejection(
            lambda: verify(base_vertices, base_edges),
            "public API missing source root",
            "analytic source authentication failed: repository absent"))
    finally:
        globals()["SOURCE_ROOT"] = source_root_original

    # Unexpected implementation errors must propagate, not count as rejection.
    reconstruct_original = globals()["reconstruct"]
    def unrelated_crash(*_args, **_kwargs):
        raise KeyError("unrelated implementation crash")
    globals()["reconstruct"] = unrelated_crash
    try:
        try:
            expect_rejection(lambda: verify(base_vertices, base_edges),
                             "unrelated implementation crash",
                             "unrelated implementation crash")
        except KeyError as error:
            require(str(error) == "'unrelated implementation crash'",
                    "unrelated implementation error changed")
        else:
            raise VerifyError("hostile harness masked an unrelated KeyError")
    finally:
        globals()["reconstruct"] = reconstruct_original

    require(len(rejected) == len(set(rejected)),
            "hostile rejection labels are not unique")
    return tuple(rejected)


def static_audit():
    source_path = Path(__file__)
    require(source_path.is_file(), "candidate source file is absent")
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))
    assert_nodes = tuple(node for node in ast.walk(tree)
                         if isinstance(node, ast.Assert))
    require(not assert_nodes, "candidate source contains an assert statement")
    verify_defs = tuple(node for node in tree.body
                        if isinstance(node, ast.FunctionDef) and
                        node.name == "verify")
    require(len(verify_defs) == 1, "production verify definition is not unique")
    definition = verify_defs[0]
    require(tuple(argument.arg for argument in definition.args.args) ==
            ("vertices", "edges") and
            not definition.args.vararg and not definition.args.kwarg and
            not definition.args.defaults and
            not definition.args.kwonlyargs,
            "production API accepts semantic metadata or optional bypasses")
    debug_names = tuple(node for node in ast.walk(tree)
                        if isinstance(node, ast.Name) and node.id == "__debug__")
    require(not debug_names, "candidate source branches on optimization mode")
    return 3


def audit():
    source_files = audit_sources()
    static_checks = static_audit()
    (fixture_count, relabel_count, root_replays, away_ranks,
     entry_deltas, entry_etas, anchor_counts, tree_debits,
     max_connector, suite_digest) = audit_fixtures()
    hostiles = hostile_tests()
    return AuditResult(
        fixture_count,
        relabel_count,
        root_replays,
        away_ranks,
        entry_deltas,
        entry_etas,
        anchor_counts,
        tree_debits,
        max_connector,
        suite_digest,
        hostiles,
        source_files,
        static_checks,
    )


def render_report(result):
    require(type(result) is AuditResult, "report input is not an AuditResult")
    lines = (
        "R221 ADJACENCY-ONLY SEMANTIC VERIFIER CANDIDATE",
        "status: FINITE CANDIDATE AUDIT PASS; UNIVERSAL/PUBLICATION CLAIM WITHHELD",
        "scope: physical rank-seven R221 only; exactly two literal diamonds plus three literal triangles",
        "input: immutable canonical adjacency only; no caller profile, root, block, route, owner, rank, threshold, partition, or charge",
        f"contract records: {len(CONTRACT_SPECS)}; authenticated source files: {result.source_files}",
        f"full contract manifest SHA-256: {EXPECTED_FULL_CONTRACT_MANIFEST_SHA256}",
        f"source manifest SHA-256: {EXPECTED_SOURCE_MANIFEST_SHA256}",
        f"generated physical fixtures: {result.fixture_count}; opaque relabel replays: {result.relabel_count}; root-diamond replays: {result.root_replays}",
        f"complete-away ranks covered: {','.join(map(str, result.away_ranks))}",
        f"diamond entry deltas covered: {','.join(map(str, result.entry_deltas))}; opened eta covered: {','.join(map(str, result.entry_etas))}",
        f"anchor triangle counts covered: {','.join(map(str, result.anchor_triangle_counts))}; tree debits covered: {','.join(map(str, result.tree_debits))}",
        f"longest explicit K2 connector: {result.max_connector_length}",
        f"semantic fixture-suite SHA-256: {result.semantic_suite_sha256}",
        f"hostile mutations rejected: {len(result.hostile_rejections)}",
        f"static fail-closed checks: {result.static_checks}; Python assert statements: 0",
        "ledger: every root replay conditionally derives sigma(G) > 1-tree_debit >= 0 from pinned contracts",
        "proof boundary: source hashes authenticate bytes, not mathematical truth; finite fixtures do not exhaust arbitrary block-cut trees or payload sizes",
        "normal/-O policy: this deterministic report must be compared byte-for-byte by the external release command",
    )
    return "\n".join(lines) + "\n"


def main():
    result = audit()
    sys.stdout.write(render_report(result))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerifyError as error:
        sys.stderr.write(f"R221 VERIFY ERROR: {error}\n")
        raise SystemExit(1)
