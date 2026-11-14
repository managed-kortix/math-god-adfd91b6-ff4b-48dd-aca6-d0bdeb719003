#!/usr/bin/env python3
"""NONPROMOTIONAL fail-closed R21 literal-cycle typing verifier.

The gate authenticates blocks from materialized adjacency.  It never infers a
physical graph type from D/T/P labels or from the symbolic R21 registry.  Its
only conclusion is the exact strict-DNN classification of a graph whose
positive-rank Tarjan blocks are literally D=Theta(1,2,2), four C3 blocks, and
one simple C_q block.  It proves no packet, bridge dispatch, or theorem.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Hashable


class GateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GateError(message)


REPO = Path(__file__).resolve().parents[1]
SOURCE_PARENT_COMMIT = "e3bb1e8345d8991383cfada94dda4f87a712881a"
SCHEMA = "r21-literal-cycle-typing/v1"


@dataclass(frozen=True)
class SourcePin:
    path: str
    byte_length: int
    sha256: str
    git_blob_sha1: str
    tokens: tuple[str, ...]


SOURCE_PINS = (
    SourcePin(
        "all-tricyclic-graphs/paper.tex",
        47532,
        "4abf3ffa1e09148c060969f4055d878334af9b7358d0764ac42f5e0ffb236b02",
        "cc9d807f36df0d0dc5cdba7e0ba75c6919dfe13c",
        (
            "Rank-one blocks are cycles.  A simple rank-two $2$-connected block is a theta.",
            "For a cycle put $\\epsilon_q=0$ for even $q$ and\n"
            "$\\epsilon_q=q\\tan^2(\\pi/(2q))$ for odd $q$.",
            "\\Delta(1,2,2)=\\frac{\\sqrt{17}-1}{2}.",
            "Finally, the odd-cycle excess is $h_q(\\pi/2)$, so\n"
            "\\eqref{eq:hs-derivative} says that it decreases strictly with odd $q$.",
            " \\epsilon_3=1,\n"
            " \\qquad \\epsilon_5=5-2\\sqrt5<\\frac23,\n"
            " \\qquad \\epsilon_q\\leq\\epsilon_7<\\frac25"
            "\\quad(q\\geq7\\text{ odd}).",
            "Even cycles have zero excess.",
        ),
    ),
    SourcePin(
        "positive-square-energy/heptacyclic-general/"
        "rank-seven-multiblock-debit-ledger.md",
        13093,
        "3f8bb3a397125782dd6c9cae26ce52f9c6bf826e3136dfee62781048e65c18a5",
        "6a53bbfd1796897cf091f1f9900e75772f41cf3e",
        (
            "`sum_i d(B_i)<=k-1`.                                          (2)",
            "Thus `k-1` is the exact multiblock debit allowance.",
            "`epsilon(C3)=1`, `epsilon(C5)=5-2sqrt(5)`, and even cycles have zero\n"
            "debit.",
            "`Residual predicate`\nis exact: it is evaluated using the actual certified excesses, not merely the\n"
            "uniform maxima in the preceding table.",
            "| `2+1^5` | 5 | DNN when `Delta+sum epsilon_i<=6` | "
            "`R21: Theta(1,2,r)+T^5`; and `D+T^4+P` |",
            "Equality in\nevery DNN predicate is closed and is not a packet residual.",
        ),
    ),
    SourcePin(
        "positive-square-energy/hexacyclic-general/"
        "multiblock-items1-7-combined-theorem-audit.md",
        12795,
        "25ab7e6af9629df5054660d15a67d54192a20b511f8a36f932f157922ff472f1",
        "e792bdfa6627c1bd3be64b86054cd9f8c5f9d628",
        (
            "Write `T=C3`, `P=C5`, `D=Theta(1,2,2)`,",
            "`p=epsilon(P)=5-2sqrt(5)`,\n"
            "`d=Delta(D)=(sqrt(17)-1)/2`.",
            "every odd cycle of length at least seven has excess below `2/5`.",
            "The analogous elementary cycle sums give exactly the two rows in\n"
            "partition 2 and the one row in partition 3.",
        ),
    ),
)


def pure_python_sha1(payload: bytes) -> str:
    """Independent SHA-1 implementation used to authenticate Git blob IDs."""
    message = bytearray(payload)
    bit_length = 8 * len(message)
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message.extend(bit_length.to_bytes(8, "big"))
    h0, h1, h2, h3, h4 = (
        0x67452301, 0xEFCDAB89, 0x98BADCFE,
        0x10325476, 0xC3D2E1F0,
    )
    mask = (1 << 32) - 1
    for offset in range(0, len(message), 64):
        words = [int.from_bytes(message[index:index + 4], "big")
                 for index in range(offset, offset + 64, 4)]
        for index in range(16, 80):
            value = words[index - 3] ^ words[index - 8] ^ words[index - 14] ^ words[index - 16]
            words.append(((value << 1) | (value >> 31)) & mask)
        a, b, c, d, e = h0, h1, h2, h3, h4
        for index, word in enumerate(words):
            if index < 20:
                function, constant = (b & c) | ((~b) & d), 0x5A827999
            elif index < 40:
                function, constant = b ^ c ^ d, 0x6ED9EBA1
            elif index < 60:
                function, constant = (b & c) | (b & d) | (c & d), 0x8F1BBCDC
            else:
                function, constant = b ^ c ^ d, 0xCA62C1D6
            rotate_a = ((a << 5) | (a >> 27)) & mask
            temporary = (rotate_a + function + e + constant + word) & mask
            e, d, c, b, a = d, c, ((b << 30) | (b >> 2)) & mask, a, temporary
        h0 = (h0 + a) & mask
        h1 = (h1 + b) & mask
        h2 = (h2 + c) & mask
        h3 = (h3 + d) & mask
        h4 = (h4 + e) & mask
    return "".join(f"{value:08x}" for value in (h0, h1, h2, h3, h4))


def git_blob_sha1(payload: bytes) -> str:
    header = f"blob {len(payload)}\0".encode("ascii")
    blob = header + payload
    stdlib = hashlib.sha1(blob).hexdigest()
    independent = pure_python_sha1(blob)
    require(stdlib == independent, "independent Git-blob SHA-1 implementations disagree")
    return independent


def audit_sources(pins: tuple[SourcePin, ...] = SOURCE_PINS) -> dict[str, dict[str, object]]:
    require(type(pins) is tuple and len(pins) == 3, "source registry cardinality changed")
    expected_paths = tuple(pin.path for pin in SOURCE_PINS)
    require(tuple(pin.path for pin in pins) == expected_paths,
            "source registry paths or order changed")
    report: dict[str, dict[str, object]] = {}
    for pin in pins:
        path = REPO / pin.path
        require(path.is_file(), f"missing pinned source: {pin.path}")
        payload = path.read_bytes()
        require(len(payload) == pin.byte_length, f"source byte length changed: {pin.path}")
        require(hashlib.sha256(payload).hexdigest() == pin.sha256,
                f"source SHA-256 changed: {pin.path}")
        require(git_blob_sha1(payload) == pin.git_blob_sha1,
                f"source Git blob changed: {pin.path}")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as error:
            raise GateError(f"pinned source is not UTF-8: {pin.path}") from error
        require(type(pin.tokens) is tuple and pin.tokens,
                f"empty semantic token registry: {pin.path}")
        for token in pin.tokens:
            require(type(token) is str and token and text.count(token) == 1,
                    f"semantic token missing or nonunique: {pin.path}: {token!r}")
        report[pin.path] = {
            "bytes": len(payload),
            "git_blob_sha1": pin.git_blob_sha1,
            "semantic_tokens_unique": len(pin.tokens),
            "sha256": pin.sha256,
        }
    return report


@dataclass(frozen=True)
class DNNContract:
    rank_partition: tuple[int, ...]
    positive_rank_blocks: int
    debit_allowance: int
    excess_closure_budget: int
    closure_relation: str
    residual_relation: str
    equality_closed: bool
    theta_type: str
    fixed_triangles: int
    closure_expression: str
    open_expression: str


EXACT_CONTRACT = DNNContract(
    rank_partition=(2, 1, 1, 1, 1, 1),
    positive_rank_blocks=6,
    debit_allowance=5,
    excess_closure_budget=6,
    closure_relation="<=",
    residual_relation=">",
    equality_closed=True,
    theta_type="Theta(1,2,2)",
    fixed_triangles=4,
    closure_expression="Delta(1,2,2)+4*epsilon(C3)+epsilon(C_q)<=6",
    open_expression="Delta(1,2,2)+4*epsilon(C3)+epsilon(C_q)>6",
)


def validate_contract(contract: DNNContract) -> None:
    require(type(contract) is DNNContract, "DNN contract is not typed")
    require(contract.rank_partition == (2, 1, 1, 1, 1, 1),
            "rank partition is not R21 2+1^5")
    require(contract.positive_rank_blocks == 6, "positive block count changed")
    require(contract.debit_allowance == 5, "six-block debit allowance is not k-1=5")
    require(contract.excess_closure_budget == 6, "R21 excess budget changed")
    require(contract.closure_relation == "<=", "DNN closure relation is not <=")
    require(contract.residual_relation == ">", "DNN-open relation is not strict >")
    require(contract.equality_closed is True, "DNN equality was made residual")
    require(contract.theta_type == "Theta(1,2,2)", "theta type is not literal D")
    require(contract.fixed_triangles == 4, "fixed literal triangle count changed")
    require(contract.closure_expression ==
            "Delta(1,2,2)+4*epsilon(C3)+epsilon(C_q)<=6",
            "closure expression changed")
    require(contract.open_expression ==
            "Delta(1,2,2)+4*epsilon(C3)+epsilon(C_q)>6",
            "strict DNN-open expression changed")


Vertex = Hashable
Edge = frozenset[Vertex]


@dataclass(frozen=True)
class PhysicalGraph:
    vertices: frozenset[Vertex]
    edges: frozenset[Edge]


def edge(left: Vertex, right: Vertex) -> Edge:
    require(left != right, "simple graph cannot contain a loop")
    return frozenset((left, right))


def adjacency(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> dict[Vertex, set[Vertex]]:
    require(type(vertices) is frozenset and vertices, "vertex set is not a nonempty frozenset")
    require(type(edges) is frozenset, "edge set is not a frozenset")
    graph = {vertex: set() for vertex in vertices}
    for current in edges:
        require(type(current) is frozenset and len(current) == 2, "malformed simple edge")
        left, right = tuple(current)
        require(left in graph and right in graph, "edge endpoint escaped vertex set")
        require(right not in graph[left], "duplicate simple edge")
        graph[left].add(right)
        graph[right].add(left)
    return graph


def connected(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> bool:
    if not vertices:
        return False
    graph = adjacency(vertices, edges)
    root = min(vertices, key=repr)
    seen = {root}
    stack = [root]
    while stack:
        current = stack.pop()
        for neighbor in graph[current] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return seen == set(vertices)


def components(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> tuple[frozenset[Vertex], ...]:
    graph = adjacency(vertices, edges)
    unseen = set(vertices)
    answer = []
    while unseen:
        root = min(unseen, key=repr)
        seen = {root}
        stack = [root]
        while stack:
            current = stack.pop()
            for neighbor in graph[current] - seen:
                seen.add(neighbor)
                stack.append(neighbor)
        unseen -= seen
        answer.append(frozenset(seen))
    return tuple(answer)


def graph_rank(vertices: frozenset[Vertex], edges: frozenset[Edge]) -> int:
    return len(edges) - len(vertices) + len(components(vertices, edges))


def block_vertices(block: frozenset[Edge]) -> frozenset[Vertex]:
    require(type(block) is frozenset and block, "empty or malformed edge block")
    return frozenset().union(*block)


def block_rank(block: frozenset[Edge]) -> int:
    return len(block) - len(block_vertices(block)) + 1


def biconnected_edge_blocks(vertices: frozenset[Vertex],
                            edges: frozenset[Edge]) -> tuple[frozenset[Edge], ...]:
    """Tarjan edge-stack decomposition; a bridge is a singleton edge block."""
    graph = adjacency(vertices, edges)
    discovery: dict[Vertex, int] = {}
    low: dict[Vertex, int] = {}
    parent: dict[Vertex, Vertex] = {}
    stack: list[Edge] = []
    blocks: list[frozenset[Edge]] = []
    clock = 0

    def visit(current: Vertex) -> None:
        nonlocal clock
        clock += 1
        discovery[current] = low[current] = clock
        for neighbor in sorted(graph[current], key=repr):
            current_edge = edge(current, neighbor)
            if neighbor not in discovery:
                parent[neighbor] = current
                stack.append(current_edge)
                visit(neighbor)
                low[current] = min(low[current], low[neighbor])
                if low[neighbor] >= discovery[current]:
                    block: set[Edge] = set()
                    while True:
                        require(stack, "Tarjan edge stack underflow")
                        popped = stack.pop()
                        block.add(popped)
                        if popped == current_edge:
                            break
                    blocks.append(frozenset(block))
            elif parent.get(current) != neighbor and discovery[neighbor] < discovery[current]:
                stack.append(current_edge)
                low[current] = min(low[current], discovery[neighbor])

    for root in sorted(vertices, key=repr):
        if root not in discovery:
            visit(root)
            require(not stack, "Tarjan stack leaked between components")
    union = set().union(*blocks) if blocks else set()
    require(union == set(edges), "Tarjan blocks do not exhaust the physical edges")
    require(sum(map(len, blocks)) == len(edges), "Tarjan blocks duplicate an edge")
    return tuple(blocks)


def block_degrees(block: frozenset[Edge]) -> dict[Vertex, int]:
    vertices = block_vertices(block)
    return {vertex: sum(vertex in current for current in block) for vertex in vertices}


def authenticate_literal_cycle(block: frozenset[Edge]) -> int:
    vertices = block_vertices(block)
    degrees = block_degrees(block)
    require(len(vertices) >= 3, "cycle block has fewer than three vertices")
    require(len(block) == len(vertices), "rank-one block is not a literal cycle")
    require(all(value == 2 for value in degrees.values()),
            "rank-one block is not internally 2-regular")
    return len(vertices)


def authenticate_literal_diamond(block: frozenset[Edge]) -> None:
    vertices = block_vertices(block)
    degrees = block_degrees(block)
    require(len(vertices) == 4 and len(block) == 5,
            "rank-two block is not the four-vertex five-edge D")
    require(sorted(degrees.values()) == [2, 2, 3, 3],
            "rank-two block does not have diamond degrees")
    branches = tuple(vertex for vertex, degree in degrees.items() if degree == 3)
    interiors = tuple(vertex for vertex, degree in degrees.items() if degree == 2)
    require(len(branches) == 2 and len(interiors) == 2,
            "diamond branch/interior cardinality changed")
    require(edge(*branches) in block, "D has no literal unit branch path")
    for interior in interiors:
        require(all(edge(interior, branch) in block for branch in branches),
                "D length-two path is not literal")
    require(edge(*interiors) not in block, "D interiors acquired a chord")


@dataclass(frozen=True)
class Inventory:
    q: int
    cycle_lengths: tuple[int, ...]
    cyclic_block_ranks: tuple[int, ...]
    bridge_blocks: int
    graph_vertices: int
    graph_edges: int


def authenticate_inventory(graph: PhysicalGraph) -> Inventory:
    require(type(graph) is PhysicalGraph, "certificate contains no materialized adjacency")
    adjacency(graph.vertices, graph.edges)
    require(connected(graph.vertices, graph.edges), "physical graph is disconnected")
    blocks = biconnected_edge_blocks(graph.vertices, graph.edges)
    ranks = tuple(block_rank(block) for block in blocks)
    require(all(rank >= 0 for rank in ranks), "Tarjan block has negative rank")
    require(all(len(block) == 1 for block, rank in zip(blocks, ranks) if rank == 0),
            "noncyclic Tarjan block is not a physical bridge")
    cyclic = tuple(block for block, rank in zip(blocks, ranks) if rank > 0)
    cyclic_ranks = tuple(sorted(block_rank(block) for block in cyclic))
    require(cyclic_ranks == (1, 1, 1, 1, 1, 2),
            "positive-rank inventory is not one rank-two plus five rank-one blocks")
    diamond_blocks = tuple(block for block in cyclic if block_rank(block) == 2)
    cycle_blocks = tuple(block for block in cyclic if block_rank(block) == 1)
    require(len(diamond_blocks) == 1 and len(cycle_blocks) == 5,
            "R21 cyclic block cardinality changed")
    authenticate_literal_diamond(diamond_blocks[0])
    lengths = tuple(sorted(authenticate_literal_cycle(block) for block in cycle_blocks))
    if lengths == (3, 3, 3, 3, 3):
        q = 3
    else:
        require(lengths[:4] == (3, 3, 3, 3) and len(lengths) == 5 and lengths[4] >= 4,
                "cycle inventory is not four literal T blocks plus one literal C_q")
        q = lengths[4]
    require(graph_rank(graph.vertices, graph.edges) == 7,
            "authenticated physical graph does not have rank seven")
    return Inventory(
        q=q,
        cycle_lengths=lengths,
        cyclic_block_ranks=cyclic_ranks,
        bridge_blocks=sum(rank == 0 for rank in ranks),
        graph_vertices=len(graph.vertices),
        graph_edges=len(graph.edges),
    )


@dataclass(frozen=True)
class Classification:
    q: int
    dnn_open: bool
    physical_family: str
    proof_case: str
    exact_margin_or_bound: str
    integer_witnesses: tuple[str, ...]


def classify_q(q: int, contract: DNNContract = EXACT_CONTRACT) -> Classification:
    validate_contract(contract)
    require(type(q) is int and not isinstance(q, bool) and q >= 3,
            "simple cycle length q must be an integer at least three")
    if q == 3:
        require(17 > 9, "integer witness d>1 failed")
        return Classification(
            q=3,
            dnn_open=True,
            physical_family="D+T^5",
            proof_case="q=3 is the first R21 family, not P",
            exact_margin_or_bound="d+5-6=(sqrt(17)-3)/2>0",
            integer_witnesses=("17>9",),
        )
    if q == 5:
        # sqrt(17)+5 > 4sqrt(5): after one valid square this is
        # sqrt(17)>19/5; after the second valid square it is 425>361.
        require(425 > 361, "exact q=5 radical witness failed")
        return Classification(
            q=5,
            dnn_open=True,
            physical_family="D+T^4+P(C5)",
            proof_case="unique nontriangle DNN-open cycle",
            exact_margin_or_bound="(sqrt(17)+5-4sqrt(5))/2>0",
            integer_witnesses=("425>361",),
        )
    if q % 2 == 0:
        require(17 < 25, "even-cycle closure witness failed")
        return Classification(
            q=q,
            dnn_open=False,
            physical_family="DNN_CLOSED:D+T^4+C_q",
            proof_case="even q>=4 has epsilon_q=0",
            exact_margin_or_bound="d+4-6=(sqrt(17)-5)/2<0",
            integer_witnesses=("17<25",),
        )
    require(q >= 7, "odd non-3/non-5 cycle did not enter q>=7 class")
    require(425 < 441, "odd-tail d<8/5 witness failed")
    return Classification(
        q=q,
        dnn_open=False,
        physical_family="DNN_CLOSED:D+T^4+C_q",
        proof_case="odd q>=7 has epsilon_q<2/5",
        exact_margin_or_bound="d+4+epsilon_q<8/5+4+2/5=6",
        integer_witnesses=("425<441",),
    )


@dataclass(frozen=True)
class TypingClaim:
    schema: str
    status: str
    contract: DNNContract
    graph: PhysicalGraph
    claimed_q: int
    claimed_family: str
    claimed_dnn_open: bool


def graph_fingerprint(graph: PhysicalGraph) -> str:
    vertices = sorted((repr(vertex) for vertex in graph.vertices))
    edges = sorted(tuple(sorted((repr(vertex) for vertex in current))) for current in graph.edges)
    payload = json.dumps({"edges": edges, "vertices": vertices},
                         sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def verify_claim(claim: TypingClaim) -> dict[str, object]:
    require(type(claim) is TypingClaim, "typing certificate schema object is missing")
    require(claim.schema == SCHEMA, "typing certificate schema changed")
    require(claim.status == "NONPROMOTIONAL", "typing certificate is not NONPROMOTIONAL")
    validate_contract(claim.contract)
    inventory = authenticate_inventory(claim.graph)
    classification = classify_q(inventory.q, claim.contract)
    require(type(claim.claimed_q) is int and not isinstance(claim.claimed_q, bool)
            and claim.claimed_q == inventory.q,
            "claimed q differs from adjacency-authenticated q")
    require(claim.claimed_family == classification.physical_family,
            "claimed family differs from exact physical dispatch")
    require(type(claim.claimed_dnn_open) is bool
            and claim.claimed_dnn_open is classification.dnn_open,
            "claimed DNN-open status differs from the strict predicate")
    return {
        "adjacency_sha256": graph_fingerprint(claim.graph),
        "bridge_blocks": inventory.bridge_blocks,
        "cycle_lengths": list(inventory.cycle_lengths),
        "dnn_open": classification.dnn_open,
        "edges": inventory.graph_edges,
        "family": classification.physical_family,
        "proof_case": classification.proof_case,
        "q": inventory.q,
        "vertices": inventory.graph_vertices,
    }


def build_profile(q: int) -> PhysicalGraph:
    require(type(q) is int and not isinstance(q, bool) and q >= 3,
            "fixture q is not a simple-cycle length")
    root = "cut"
    branch = "D:branch"
    interiors = ("D:left", "D:right")
    vertices: set[Vertex] = {root, branch, *interiors}
    edges: set[Edge] = {
        edge(root, branch),
        edge(root, interiors[0]), edge(interiors[0], branch),
        edge(root, interiors[1]), edge(interiors[1], branch),
    }
    lengths = (3, 3, 3, 3, q)
    for cycle_index, length in enumerate(lengths):
        private = tuple(f"C{cycle_index}:{place}" for place in range(1, length))
        vertices.update(private)
        sequence = (root, *private, root)
        edges.update(edge(left, right) for left, right in zip(sequence, sequence[1:]))
    return PhysicalGraph(frozenset(vertices), frozenset(edges))


def make_claim(q: int) -> TypingClaim:
    classification = classify_q(q)
    return TypingClaim(
        schema=SCHEMA,
        status="NONPROMOTIONAL",
        contract=EXACT_CONTRACT,
        graph=build_profile(q),
        claimed_q=q,
        claimed_family=classification.physical_family,
        claimed_dnn_open=classification.dnn_open,
    )


def subdivide(graph: PhysicalGraph, target: Edge, vertex: Vertex) -> PhysicalGraph:
    require(target in graph.edges and vertex not in graph.vertices,
            "hostile subdivision fixture is malformed")
    left, right = tuple(target)
    edges = set(graph.edges)
    edges.remove(target)
    edges.update((edge(left, vertex), edge(vertex, right)))
    return PhysicalGraph(graph.vertices | frozenset((vertex,)), frozenset(edges))


def with_edge(graph: PhysicalGraph, addition: Edge) -> PhysicalGraph:
    require(addition not in graph.edges and addition <= graph.vertices,
            "hostile chord fixture is malformed")
    return PhysicalGraph(graph.vertices, graph.edges | frozenset((addition,)))


def add_leaf(graph: PhysicalGraph, root: Vertex, leaf: Vertex) -> PhysicalGraph:
    require(root in graph.vertices and leaf not in graph.vertices,
            "tree-payload fixture is malformed")
    return PhysicalGraph(graph.vertices | frozenset((leaf,)),
                         graph.edges | frozenset((edge(root, leaf),)))


def add_bridge_path_triangle(graph: PhysicalGraph, root: Vertex) -> PhysicalGraph:
    """Attach one literal C3 after a positive K2 chain for hostile coverage."""
    route = ("route:0", "route:1")
    private = ("route:T0", "route:T1")
    require(root in graph.vertices and not set((*route, *private)) & set(graph.vertices),
            "bridge-route fixture overlaps the base graph")
    vertices = graph.vertices | frozenset((*route, *private))
    additions = {
        edge(root, route[0]), edge(route[0], route[1]),
        edge(route[1], private[0]), edge(private[0], private[1]),
        edge(private[1], route[1]),
    }
    return PhysicalGraph(vertices, graph.edges | frozenset(additions))


def expect_rejected(action, label: str) -> str:
    try:
        action()
    except (GateError, TypeError, ValueError, KeyError, IndexError):
        return label
    raise GateError(f"hostile mutation accepted: {label}")


def hostile_checks() -> tuple[str, ...]:
    labels = []
    q5 = make_claim(5)

    # Rank-zero bridge blocks and one-root tree payloads are permitted, but
    # their physical adjacency must leave the exact cyclic inventory intact.
    q5_with_tree = add_leaf(q5.graph, "C4:2", "tree:leaf")
    tree_report = verify_claim(replace(q5, graph=q5_with_tree))
    require(tree_report["bridge_blocks"] == 1 and tree_report["q"] == 5
            and tree_report["dnn_open"] is True,
            "permitted one-root tree payload changed the typed row")

    # A required T cannot be a C4 produced by subdividing one T edge.
    subdivided_t = subdivide(q5.graph, edge("cut", "C0:1"), "T:subdivision")
    labels.append(expect_rejected(
        lambda: verify_claim(replace(q5, graph=subdivided_t)),
        "subdivided required T"))

    # A subdivision of D remains a theta but is not literal Theta(1,2,2).
    subdivided_d = subdivide(q5.graph, edge("cut", "D:branch"), "D:subdivision")
    labels.append(expect_rejected(
        lambda: verify_claim(replace(q5, graph=subdivided_d)),
        "subdivided nonliteral D"))

    # A chorded alleged C5 is no longer one literal simple cycle block.
    chorded_q = with_edge(q5.graph, edge("C4:1", "C4:3"))
    labels.append(expect_rejected(
        lambda: verify_claim(replace(q5, graph=chorded_q)),
        "chorded nonliteral cycle"))

    # Labels without materialized adjacency have no authority.
    labels.append(expect_rejected(
        lambda: verify_claim(replace(q5, graph="D+T^4+P")),  # type: ignore[arg-type]
        "symbolic row without adjacency"))

    # q=3 must dispatch to D+T^5, not to the pentagon row.
    q3 = make_claim(3)
    labels.append(expect_rejected(
        lambda: verify_claim(replace(q3, claimed_family="D+T^4+P(C5)")),
        "q=3 mislabeled as P"))

    # A symbolic P label cannot turn an actual C7 into a C5 survivor.
    q7 = make_claim(7)
    labels.append(expect_rejected(
        lambda: verify_claim(replace(q7, claimed_q=5,
                                     claimed_family="D+T^4+P(C5)",
                                     claimed_dnn_open=True)),
        "C7 relabeled P"))

    # An extra positive-rank block hidden behind a physical bridge is not a
    # payload and must not pass as the six-block R21 inventory.
    extra_cycle = add_bridge_path_triangle(q5.graph, "D:left")
    labels.append(expect_rejected(
        lambda: verify_claim(replace(q5, graph=extra_cycle)),
        "extra cyclic block behind bridge"))

    # Exact relation and both equivalent budgets are immutable.
    labels.append(expect_rejected(
        lambda: classify_q(5, replace(EXACT_CONTRACT, residual_relation=">=")),
        "non-strict DNN-open relation"))
    labels.append(expect_rejected(
        lambda: classify_q(5, replace(EXACT_CONTRACT, closure_relation="<")),
        "strict closure mutation"))
    labels.append(expect_rejected(
        lambda: classify_q(5, replace(EXACT_CONTRACT, equality_closed=False)),
        "equality made residual"))
    labels.append(expect_rejected(
        lambda: classify_q(5, replace(EXACT_CONTRACT, excess_closure_budget=5)),
        "excess budget mutation"))
    labels.append(expect_rejected(
        lambda: classify_q(5, replace(EXACT_CONTRACT, debit_allowance=6)),
        "debit allowance mutation"))

    # Exact bytes and exact semantic tokens are both live checks.
    bad_hash_pins = tuple(
        replace(pin, sha256="0" * 64) if index == 0 else pin
        for index, pin in enumerate(SOURCE_PINS)
    )
    labels.append(expect_rejected(lambda: audit_sources(bad_hash_pins),
                                  "source byte hash mutation"))
    bad_token_pins = tuple(
        replace(pin, tokens=pin.tokens + ("NONEXISTENT R21 SOURCE TOKEN",))
        if index == 1 else pin
        for index, pin in enumerate(SOURCE_PINS)
    )
    labels.append(expect_rejected(lambda: audit_sources(bad_token_pins),
                                  "source semantic token mutation"))

    require(len(labels) == len(set(labels)) == 14, "hostile rejection registry changed")
    return tuple(labels)


LIMITATIONS = (
    "NONPROMOTIONAL: this gate types only an adjacency-authenticated D+4T+C_q R21 profile.",
    "The rank-seven ledger is a symbolic residual registry; its token P is not adjacency evidence.",
    "No bridge dispatch, induced-territory ownership, packet inequality, or rank-seven theorem is proved.",
    "The DNN identities and monotonicity bounds are pinned inputs, not rederived spectral results.",
    "No STATE, theorem-master, publication, or lane-control artifact is read as authority or modified.",
)


def run() -> dict[str, object]:
    sources = audit_sources()
    validate_contract(EXACT_CONTRACT)

    # Materialized representatives exercise every universal arithmetic branch;
    # authenticate_inventory/verify_claim remain callable on any finite input.
    fixture_qs = (3, 4, 5, 6, 7, 9, 10)
    fixtures = [verify_claim(make_claim(q)) for q in fixture_qs]
    by_q = {entry["q"]: entry for entry in fixtures}
    require(by_q[3]["dnn_open"] is True and by_q[3]["family"] == "D+T^5",
            "q=3 dispatch changed")
    require(by_q[5]["dnn_open"] is True and by_q[5]["family"] == "D+T^4+P(C5)",
            "q=5 survivor changed")
    require(all(entry["dnn_open"] is False for entry in fixtures
                if entry["q"] >= 4 and entry["q"] != 5),
            "a non-C5 q>=4 fixture survived")

    universal = {
        "dnn_open_predicate": EXACT_CONTRACT.open_expression,
        "equality": "closed",
        "q=3": classify_q(3).__dict__,
        "q=5": classify_q(5).__dict__,
        "even_q>=4": {
            "dnn_open": False,
            "proof": "epsilon_q=0 and 17<25 imply d<2",
        },
        "odd_q>=7": {
            "dnn_open": False,
            "proof": "epsilon_q<2/5 and 425<441 imply d<8/5",
        },
        "q>=4_survivors": [5],
    }
    # Convert tuple fields from dataclass dictionaries to JSON lists.
    universal["q=3"]["integer_witnesses"] = list(universal["q=3"]["integer_witnesses"])
    universal["q=5"]["integer_witnesses"] = list(universal["q=5"]["integer_witnesses"])

    rejected = hostile_checks()
    return {
        "adjacency_authenticated_fixtures": fixtures,
        "contract": {
            "closure": EXACT_CONTRACT.closure_expression,
            "debit_allowance": EXACT_CONTRACT.debit_allowance,
            "equality_closed": EXACT_CONTRACT.equality_closed,
            "open": EXACT_CONTRACT.open_expression,
            "positive_rank_blocks": EXACT_CONTRACT.positive_rank_blocks,
            "rank_partition": list(EXACT_CONTRACT.rank_partition),
        },
        "hostile_mutations_rejected": {
            "count": len(rejected),
            "labels": list(rejected),
        },
        "limitations": list(LIMITATIONS),
        "schema": SCHEMA,
        "source_parent_commit": SOURCE_PARENT_COMMIT,
        "source_registry_role": "symbolic provenance only; physical rows require adjacency",
        "sources": sources,
        "status": "NONPROMOTIONAL_ADJACENCY_AUTHENTICATED_TYPING_CERTIFICATE",
        "universal_classification": universal,
    }


def serialized_report() -> str:
    return json.dumps(run(), sort_keys=True, indent=2) + "\n"


def main() -> int:
    output = serialized_report()
    if not sys.flags.optimize and "--optimized-child" not in sys.argv:
        child = subprocess.run(
            [sys.executable, "-O", str(Path(__file__).resolve()), "--optimized-child"],
            check=False, capture_output=True, text=True,
        )
        require(child.returncode == 0, "optimized typing verifier failed")
        require(child.stderr == "", "optimized typing verifier wrote stderr")
        require(child.stdout == output, "normal and optimized reports differ")
    sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
