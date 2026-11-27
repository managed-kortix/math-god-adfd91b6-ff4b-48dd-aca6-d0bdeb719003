#!/usr/bin/env -S python3 -I -S -B
"""Dependency-free exact verifier for the rank-5 / (C5,C5) DNN bundle.

No float conversion, numerical eigensolver, optimizer, assert statement, or
third-party package is used. Invoke externally with ``python3 -I -S -B`` and
with ``python3 -I -S -B -O``; output must be byte-identical. Those interpreter
flags are the trust boundary. This guard runs before any shadowable import.
"""
from __future__ import annotations

import sys

if not (sys.flags.isolated == 1 and sys.flags.no_site == 1 and
        sys.flags.dont_write_bytecode == 1 and sys.flags.ignore_environment == 1 and
        sys.flags.safe_path):
    sys.stderr.write("FAIL: verifier requires external python3 -I -S -B invocation\n")
    raise SystemExit(2)

import gzip
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ATLAS = ROOT / "sources" / "networkx-3.7-atlas.dat.gz"
NETWORKX_LICENSE = ROOT / "THIRD-PARTY-NETWORKX-3.7-LICENSE.txt"
ENUM = ROOT / "data" / "atlas-rank5-enumeration.json"
CERT = ROOT / "data" / "atlas-rank5-rational-gram-certificates.json"
WITNESS = ROOT / "data" / "n8-multiblock-route-witness.json"
MANIFEST = ROOT / "SHA256SUMS"
EXPECTED_ATLAS_SHA256 = "73fc416df0164923607751cb759f4ae81deb5f6550bf25be59c86de3b747e41d"
EXPECTED_NETWORKX_LICENSE_SHA256 = "6025f323ea29dc2f0ee0abd9523bf910186f55b0e148e6ebf646c55566278e2e"
EXPECTED_README_SHA256 = "01c23729438b1fb0a724a152f20819adae4de043a9be7cecf7507d6e3bae9ece"
EXPECTED_CANDIDATE_NOTE_SHA256 = "c78f4b19bbea5f1bde52ce7c225a5a0f084149392e56a97d7051fad62cbf322c"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def reject_duplicate_keys(pairs):
    """Build a JSON object while rejecting duplicate member names."""
    result = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def reject_json_constant(token):
    raise RuntimeError(f"non-finite JSON number is forbidden: {token}")


def load(path: Path):
    """Strict UTF-8 JSON: no duplicate keys, BOM, or non-finite numbers."""
    raw = path.read_bytes()
    require(raw, f"empty JSON file: {path.name}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"invalid UTF-8 JSON in {path.name}: {exc}") from exc
    require(not text.startswith("\ufeff"), f"UTF-8 BOM is forbidden in {path.name}")
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_json_constant,
        )
    except (json.JSONDecodeError, RecursionError) as exc:
        raise RuntimeError(f"malformed JSON in {path.name}: {exc}") from exc


def is_int(value) -> bool:
    """JSON booleans are Python ints; reject that laundering explicitly."""
    return type(value) is int


def integer(value, label: str) -> int:
    require(is_int(value), f"{label} must be a JSON integer (not bool or string)")
    return value


def boolean(value, label: str) -> bool:
    require(type(value) is bool, f"{label} must be a JSON boolean")
    return value


def string(value, label: str) -> str:
    require(type(value) is str, f"{label} must be a JSON string")
    return value


def fraction(text, label="fraction") -> Q:
    string(text, label)
    require(re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", text) is not None,
            f"{label} is not a canonical rational string")
    value = Q(text)
    require(str(value) == text, f"{label} is not reduced canonical rational text")
    return value


def strict_int_list(value, label: str):
    require(isinstance(value, list), f"{label} must be a JSON array")
    return [integer(item, f"{label}[{i}]") for i, item in enumerate(value)]


def strict_edge_list(value, label: str):
    require(isinstance(value, list), f"{label} must be a JSON array")
    edges = []
    for i, item in enumerate(value):
        require(isinstance(item, list) and len(item) == 2,
                f"{label}[{i}] must be a two-element JSON array")
        edges.append(tuple(integer(x, f"{label}[{i}][{j}]") for j, x in enumerate(item)))
    return tuple(edges)


def verify_manifest():
    """Verify a closed, pinned file lock that excludes itself by construction."""
    require(MANIFEST.is_file(), "missing SHA256SUMS")
    raw = MANIFEST.read_bytes()
    require(raw and raw.endswith(b"\n"), "SHA256SUMS must be nonempty and newline-terminated")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"SHA256SUMS is not ASCII: {exc}") from exc
    seen = set()
    expected = {}
    for line_number, line in enumerate(lines, 1):
        match = re.fullmatch(r"([0-9a-f]{64})  (\./)?([^\x00\r\n]+)", line)
        require(match is not None, f"malformed SHA256SUMS line {line_number}")
        digest, _dot, name = match.groups()
        require(name != MANIFEST.name, "SHA256SUMS must not circularly include itself")
        path = Path(name)
        require(not path.is_absolute() and ".." not in path.parts and path.as_posix() == name,
                f"unsafe or noncanonical manifest path: {name!r}")
        require(name not in seen, f"duplicate manifest path: {name}")
        seen.add(name)
        expected[name] = digest

    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path != MANIFEST and "__pycache__" not in path.parts
    }
    require(seen == actual,
            "SHA256SUMS coverage mismatch: "
            f"missing={sorted(actual - seen)!r}, extra={sorted(seen - actual)!r}")
    for name in sorted(seen):
        path = ROOT / name
        require(path.is_file() and not path.is_symlink(), f"manifest member is not a regular file: {name}")
        require(path.stat().st_size > 0, f"manifest member is empty: {name}")
        require(sha256(path) == expected[name], f"manifest hash mismatch: {name}")
    require(NETWORKX_LICENSE.name in seen, "NetworkX redistribution license missing from manifest")
    require(sha256(NETWORKX_LICENSE) == EXPECTED_NETWORKX_LICENSE_SHA256,
            "NetworkX 3.7 redistribution license SHA-256 mismatch")
    require(sha256(ROOT / "README.md") == EXPECTED_README_SHA256,
            "README claim-boundary SHA-256 mismatch")
    require(sha256(ROOT / "CANDIDATE-NOTE.md") == EXPECTED_CANDIDATE_NOTE_SHA256,
            "CANDIDATE-NOTE claim-boundary SHA-256 mismatch")
    return len(seen)


def parse_decimal_integer(text: str, label: str) -> int:
    require(re.fullmatch(r"0|[1-9][0-9]*", text) is not None, f"malformed {label}")
    return int(text)


def parse_atlas(path: Path):
    graphs = []
    try:
        stream = gzip.open(path, "rt", encoding="ascii", errors="strict", newline="")
        with stream as f:
            lines = iter(f)
            pending = None
            while True:
                try:
                    line = pending if pending is not None else next(lines)
                    pending = None
                except StopIteration:
                    break
                match = re.fullmatch(r"GRAPH (0|[1-9][0-9]*)\n", line)
                require(match is not None, "malformed Atlas GRAPH line")
                index = parse_decimal_integer(match.group(1), "Atlas graph index")
                try:
                    node_line = next(lines)
                except StopIteration as exc:
                    raise RuntimeError("truncated Atlas NODES line") from exc
                match = re.fullmatch(r"NODES (0|[1-9][0-9]*)\n", node_line)
                require(match is not None, "malformed Atlas NODES line")
                n = parse_decimal_integer(match.group(1), "Atlas node count")
                edges = []
                for line in lines:
                    if line.startswith("GRAPH "):
                        pending = line
                        break
                    match = re.fullmatch(r"(0|[1-9][0-9]*) (0|[1-9][0-9]*)\n", line)
                    require(match is not None, "malformed Atlas edge line")
                    u = parse_decimal_integer(match.group(1), "Atlas edge endpoint")
                    v = parse_decimal_integer(match.group(2), "Atlas edge endpoint")
                    require(0 <= u < n and 0 <= v < n and u != v,
                            "Atlas edge endpoint out of range or loop")
                    edge = (min(u, v), max(u, v))
                    require(edge not in edges, "duplicate Atlas edge")
                    edges.append(edge)
                graphs.append((index, n, tuple(sorted(edges))))
                if pending is None:
                    break
    except (OSError, EOFError, UnicodeError) as exc:
        raise RuntimeError(f"malformed Atlas gzip/source: {exc}") from exc
    return graphs


def adjacency(n, edges, skip_vertex=None, skip_edge=None):
    adj = [[] for _ in range(n)]
    for k, (u, v) in enumerate(edges):
        if k == skip_edge or u == skip_vertex or v == skip_vertex:
            continue
        adj[u].append(v)
        adj[v].append(u)
    return adj


def connected(n, edges, skip_vertex=None, skip_edge=None):
    vertices = [v for v in range(n) if v != skip_vertex]
    if not vertices:
        return True
    adj = adjacency(n, edges, skip_vertex, skip_edge)
    seen = {vertices[0]}
    stack = [vertices[0]]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == len(vertices)


def bridges(n, edges):
    return [edges[k] for k in range(len(edges)) if not connected(n, edges, skip_edge=k)]


def articulations(n, edges):
    if n <= 2:
        return []
    return [v for v in range(n) if not connected(n, edges, skip_vertex=v)]


def biconnected_edge_blocks(n, edges):
    adj = [[] for _ in range(n)]
    for k, (u, v) in enumerate(edges):
        adj[u].append((v, k))
        adj[v].append((u, k))
    disc = [-1] * n
    low = [0] * n
    parent_edge = [-1] * n
    edge_stack = []
    blocks = []
    clock = 0

    def dfs(u):
        nonlocal clock
        disc[u] = low[u] = clock
        clock += 1
        for v, eid in adj[u]:
            if eid == parent_edge[u]:
                continue
            if disc[v] == -1:
                parent_edge[v] = eid
                edge_stack.append(eid)
                dfs(v)
                low[u] = min(low[u], low[v])
                if low[v] >= disc[u]:
                    block = []
                    while True:
                        z = edge_stack.pop()
                        block.append(z)
                        if z == eid:
                            break
                    blocks.append(tuple(sorted(block)))
            elif disc[v] < disc[u]:
                edge_stack.append(eid)
                low[u] = min(low[u], disc[v])

    for root in range(n):
        if disc[root] == -1:
            dfs(root)
            require(not edge_stack, "Tarjan edge stack not empty")
    return blocks


def scope_data(n, edges):
    blocks = biconnected_edge_blocks(n, edges)
    ranks = []
    for ids in blocks:
        block_edges = [edges[k] for k in ids]
        vertices = {x for edge in block_edges for x in edge}
        ranks.append(len(ids) - len(vertices) + 1)
    positive = sorted((r for r in ranks if r > 0), reverse=True)
    return {
        "bridges": sorted(bridges(n, edges)),
        "articulations": articulations(n, edges),
        "block_rank_profile": sorted(ranks, reverse=True),
        "positive_rank_profile": positive,
        "positive_rank_block_count": len(positive),
        "single_positive_rank_block": len(positive) == 1,
    }


def graph6_encode(n, edges):
    require(0 <= n <= 62, "only short graph6 is supported")
    eset = set(edges)
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append(1 if (i, j) in eset else 0)
    while len(bits) % 6:
        bits.append(0)
    chars = [chr(n + 63)]
    for k in range(0, len(bits), 6):
        value = 0
        for bit in bits[k:k + 6]:
            value = (value << 1) | bit
        chars.append(chr(value + 63))
    return "".join(chars)


def graph6_decode(code):
    require(isinstance(code, str) and code, "bad graph6 code")
    n = ord(code[0]) - 63
    require(0 <= n <= 62, "only short graph6 is supported")
    bits = []
    for ch in code[1:]:
        value = ord(ch) - 63
        require(0 <= value < 64, "bad graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            require(k < len(bits), "truncated graph6 data")
            if bits[k]:
                edges.append((i, j))
            k += 1
    return n, tuple(edges)


def dot(a, b):
    require(len(a) == len(b), "dot product dimension mismatch")
    return sum((x * y for x, y in zip(a, b)), Q(0))


def matrix_equal(A, B):
    return len(A) == len(B) and all(len(a) == len(b) and a == b for a, b in zip(A, B))


def exact_cost(edges, gram):
    terms = []
    total = Q(0)
    for u, v in edges:
        rho = gram[u][v]
        require(rho < 1, "edge correlation is not below one")
        cost = Q(2) / (1 - rho)
        terms.append(((u, v), rho, cost))
        total += cost
    return terms, total


def verify_atlas_and_enumeration():
    require(sha256(ATLAS) == EXPECTED_ATLAS_SHA256, "Atlas source SHA-256 mismatch")
    atlas = parse_atlas(ATLAS)
    require(len(atlas) == 1253, "Atlas must contain 1253 graphs")
    require(max(n for _, n, _ in atlas) == 7, "Atlas maximum order must be 7")
    require([index for index, _, _ in atlas] == list(range(1253)), "Atlas indices are not 0..1252")

    enum = load(ENUM)
    require(isinstance(enum, dict), "enumeration document must be a JSON object")
    require(set(enum) == {
        "counts", "filter", "records", "schema",
        "selected_graph6_source_enumeration", "source",
    }, "enumeration top-level fields changed")
    require(string(enum.get("schema"), "enumeration.schema") ==
            "graph-atlas-rank5-enumeration-v1", "enumeration schema mismatch")
    require(string(enum.get("filter"), "enumeration.filter") ==
            "simple connected beta=5; certificates select bridge-free cores",
            "enumeration filter changed")
    counts = enum.get("counts")
    require(isinstance(counts, dict), "enumeration.counts must be an object")
    expected_counts = {
        "bridge_bearing_rank5": 51,
        "bridge_free_rank5": 102,
        "connected_rank5": 153,
        "selected_multiblock": 7,
        "selected_single_positive_rank_block": 95,
    }
    require(set(counts) == set(expected_counts), "enumeration count fields changed")
    for key, expected in expected_counts.items():
        require(integer(counts.get(key), f"enumeration.counts.{key}") == expected,
                f"enumeration count changed: {key}")

    source = enum.get("source")
    require(isinstance(source, dict), "enumeration.source must be an object")
    require(string(source.get("sha256"), "enumeration.source.sha256") ==
            EXPECTED_ATLAS_SHA256, "enumeration Atlas hash mismatch")
    require(integer(source.get("graph_count"), "enumeration.source.graph_count") == 1253 and
            integer(source.get("maximum_order"), "enumeration.source.maximum_order") == 7,
            "enumeration source counts changed")
    require(string(source.get("relative_path"), "enumeration.source.relative_path") ==
            "../sources/networkx-3.7-atlas.dat.gz", "enumeration source path changed")
    require(string(source.get("name"), "enumeration.source.name") ==
            "NetworkX 3.7 atlas.dat.gz (Read-Wilson Graph Atlas data)",
            "enumeration source name changed")
    require(string(source.get("exhaustiveness_assumption"),
                   "enumeration.source.exhaustiveness_assumption") ==
            "standard Graph Atlas exhaustiveness through order 7",
            "Atlas exhaustiveness must remain explicitly conditional")

    recomputed = []
    for index, n, edges in atlas:
        if n and connected(n, edges) and len(edges) - n + 1 == 5:
            data = scope_data(n, edges)
            recomputed.append((index, n, edges, data))
    require(len(recomputed) == 153, "connected rank-five Atlas count changed")
    require(sum(not data["bridges"] for _, _, _, data in recomputed) == 102,
            "bridge-free rank-five Atlas count changed")
    require(sum(bool(data["bridges"]) for _, _, _, data in recomputed) == 51,
            "bridge-bearing rank-five Atlas count changed")

    records = enum.get("records")
    require(isinstance(records, list) and len(records) == 153, "enumeration record count changed")
    expected_record_keys = {
        "articulation_vertices", "atlas_index", "block_rank_profile",
        "bridge_free_core_graph6", "bridges", "edges", "graph6", "m", "n",
        "positive_rank_block_count", "positive_rank_profile",
        "selected_bridge_free_core", "single_positive_rank_block",
    }
    by_index = {}
    for ordinal, r in enumerate(records):
        require(isinstance(r, dict), f"enumeration.records[{ordinal}] must be an object")
        require(set(r) == expected_record_keys,
                f"enumeration.records[{ordinal}] fields changed")
        index = integer(r.get("atlas_index"), f"enumeration.records[{ordinal}].atlas_index")
        require(index not in by_index, "duplicate enumeration Atlas index")
        by_index[index] = r
    for index, n, edges, data in recomputed:
        require(index in by_index, f"missing Atlas record {index}")
        r = by_index[index]
        label = f"enumeration Atlas {index}"
        require(integer(r.get("n"), label + ".n") == n and
                integer(r.get("m"), label + ".m") == len(edges),
                f"order/size mismatch at Atlas {index}")
        require(strict_edge_list(r.get("edges"), label + ".edges") == edges,
                f"edge mismatch at Atlas {index}")
        require(string(r.get("graph6"), label + ".graph6") == graph6_encode(n, edges),
                f"graph6 mismatch at Atlas {index}")
        require(strict_edge_list(r.get("bridges"), label + ".bridges") ==
                tuple(data["bridges"]), f"bridge mismatch at Atlas {index}")
        require(strict_int_list(r.get("articulation_vertices"), label + ".articulation_vertices") ==
                data["articulations"], f"articulation mismatch at Atlas {index}")
        require(strict_int_list(r.get("block_rank_profile"), label + ".block_rank_profile") ==
                data["block_rank_profile"], f"block rank mismatch at Atlas {index}")
        require(strict_int_list(r.get("positive_rank_profile"), label + ".positive_rank_profile") ==
                data["positive_rank_profile"], f"positive profile mismatch at Atlas {index}")
        require(integer(r.get("positive_rank_block_count"), label + ".positive_rank_block_count") ==
                data["positive_rank_block_count"], f"block count mismatch at Atlas {index}")
        selected = boolean(r.get("selected_bridge_free_core"),
                           label + ".selected_bridge_free_core")
        single = boolean(r.get("single_positive_rank_block"),
                         label + ".single_positive_rank_block")
        require(selected == (not data["bridges"]), f"selection mismatch at Atlas {index}")
        require(single == data["single_positive_rank_block"], f"scope mismatch at Atlas {index}")
        expected_core_graph6 = graph6_encode(n, edges) if not data["bridges"] else None
        core_graph6 = r.get("bridge_free_core_graph6")
        require((core_graph6 is None or type(core_graph6) is str) and
                core_graph6 == expected_core_graph6,
                f"bridge-free core graph6 mismatch at Atlas {index}")

    selected = [r for r in records if
                boolean(r.get("selected_bridge_free_core"),
                        "enumeration selected_bridge_free_core")]
    require(len(selected) == 102, "selected enumeration count changed")
    require(sum(boolean(r.get("single_positive_rank_block"),
                        "enumeration single_positive_rank_block") for r in selected) == 95,
            "single-positive-block enumeration count changed")
    require(sum(not boolean(r.get("single_positive_rank_block"),
                            "enumeration single_positive_rank_block") for r in selected) == 7,
            "multiblock enumeration count changed")
    source_graph6 = enum.get("selected_graph6_source_enumeration")
    require(isinstance(source_graph6, list) and len(source_graph6) == 102,
            "selected graph6/source enumeration must contain 102 records")
    for ordinal, row in enumerate(source_graph6):
        require(isinstance(row, dict), f"selected source row {ordinal} must be an object")
        require(set(row) == {"ordinal", "atlas_index", "graph6"},
                f"selected source row {ordinal} fields changed")
        require(integer(row.get("ordinal"), f"selected source row {ordinal}.ordinal") == ordinal,
                f"selected source ordinal mismatch at {ordinal}")
        require(integer(row.get("atlas_index"), f"selected source row {ordinal}.atlas_index") ==
                integer(selected[ordinal].get("atlas_index"),
                        f"selected record {ordinal}.atlas_index"),
                f"selected source Atlas index mismatch at {ordinal}")
        require(string(row.get("graph6"), f"selected source row {ordinal}.graph6") ==
                string(selected[ordinal].get("graph6"), f"selected record {ordinal}.graph6"),
                f"selected graph6 mismatch at {ordinal}")
    return enum, {
        integer(r.get("atlas_index"), "selected atlas_index"): r for r in selected
    }


def verify_certificates(selected_by_index):
    cert = load(CERT)
    require(isinstance(cert, dict), "certificates document must be a JSON object")
    require(set(cert) == {
        "arithmetic", "claim", "counts", "logic", "records", "schema",
    }, "certificates top-level fields changed")
    require(string(cert.get("schema"), "certificates.schema") ==
            "rank5-c5-c5-rational-elliptope-certificates-v1",
            "certificate schema mismatch")
    require(string(cert.get("claim"), "certificates.claim") ==
            "For each listed bridge-free rank-five core C, kappa(C)-m(C) < 4*sqrt(5)-4.",
            "certificate claim changed")
    require(string(cert.get("logic"), "certificates.logic") ==
            "A listed feasible correlation matrix R gives kappa(C) <= sum_edges 2/(1-R_uv).",
            "certificate logic changed")
    require(string(cert.get("arithmetic"), "certificates.arithmetic") ==
            "All matrices, costs, and radical tests are exact rational/integer data.",
            "certificate arithmetic statement changed")
    counts = cert.get("counts")
    require(isinstance(counts, dict), "certificates.counts must be an object")
    for key, expected in (("total", 102), ("single_positive_rank_block", 95),
                          ("multiblock", 7)):
        require(integer(counts.get(key), f"certificates.counts.{key}") == expected,
                f"certificate count changed: {key}")

    records = cert.get("records")
    require(isinstance(records, list) and len(records) == 102, "certificate count changed")
    expected_record_keys = {
        "atlas_index", "construction", "edge_cost", "edge_cost_minus_m",
        "edge_terms", "edges", "graph6", "m", "n", "ordinal",
        "positive_rank_profile", "psd_certificate", "radical_test",
        "rational_gram_matrix", "rational_unit_vectors",
        "single_positive_rank_block",
    }
    indices = []
    for ordinal, r in enumerate(records):
        require(isinstance(r, dict), f"certificate record {ordinal} must be an object")
        require(set(r) == expected_record_keys, f"certificate record {ordinal} fields changed")
        require(integer(r.get("ordinal"), f"certificate[{ordinal}].ordinal") == ordinal,
                "certificate ordinals changed")
        indices.append(integer(r.get("atlas_index"), f"certificate[{ordinal}].atlas_index"))
    require(len(set(indices)) == 102, "duplicate certificate Atlas index")
    require(set(indices) == set(selected_by_index),
            "certificates do not match selected enumeration")

    total_edges = 0
    single_count = 0
    multi_count = 0
    maximum_by_scope = {}
    minimum_integer_slack = None

    for ordinal, r in enumerate(records):
        index = integer(r.get("atlas_index"), f"certificate[{ordinal}].atlas_index")
        source = selected_by_index[index]
        n = integer(source.get("n"), f"enumeration Atlas {index}.n")
        m = integer(source.get("m"), f"enumeration Atlas {index}.m")
        edges = strict_edge_list(source.get("edges"), f"enumeration Atlas {index}.edges")
        label = f"certificate Atlas {index}"
        require(string(r.get("graph6"), label + ".graph6") ==
                string(source.get("graph6"), f"enumeration Atlas {index}.graph6"),
                f"certificate graph6 mismatch at Atlas {index}")
        require(integer(r.get("n"), label + ".n") == n and
                integer(r.get("m"), label + ".m") == m,
                f"certificate order/size mismatch at Atlas {index}")
        require(strict_edge_list(r.get("edges"), label + ".edges") == edges,
                f"certificate edge mismatch at Atlas {index}")
        single = boolean(r.get("single_positive_rank_block"),
                         label + ".single_positive_rank_block")
        source_single = boolean(source.get("single_positive_rank_block"),
                                f"enumeration Atlas {index}.single_positive_rank_block")
        require(single == source_single, f"certificate scope mismatch at Atlas {index}")
        require(strict_int_list(r.get("positive_rank_profile"), label + ".positive_rank_profile") ==
                strict_int_list(source.get("positive_rank_profile"),
                                f"enumeration Atlas {index}.positive_rank_profile"),
                f"certificate profile mismatch at Atlas {index}")

        construction = r.get("construction")
        require(isinstance(construction, dict), f"construction missing at Atlas {index}")
        require(set(construction) == {
            "integer_stereographic_parameters", "method", "rotation_seed_offset",
            "stereographic_parameter_denominator",
        }, f"construction fields changed at Atlas {index}")
        require(integer(construction.get("rotation_seed_offset"),
                        label + ".construction.rotation_seed_offset") >= 0,
                f"negative rotation seed at Atlas {index}")
        denominator = integer(construction.get("stereographic_parameter_denominator"),
                              label + ".construction.stereographic_parameter_denominator")
        require(denominator > 0, f"bad construction denominator at Atlas {index}")
        parameters = construction.get("integer_stereographic_parameters")
        require(isinstance(parameters, list) and len(parameters) == n,
                f"construction parameter rows mismatch at Atlas {index}")
        for i, row in enumerate(parameters):
            strict_int_list(row, f"{label}.construction.integer_stereographic_parameters[{i}]")
        string(construction.get("method"), label + ".construction.method")
        require(string(r.get("psd_certificate"), label + ".psd_certificate") ==
                "R=U*U^T over Q; each row of U has exact squared norm 1",
                f"PSD certificate description changed at Atlas {index}")

        vector_text = r.get("rational_unit_vectors")
        gram_text = r.get("rational_gram_matrix")
        require(isinstance(vector_text, list) and len(vector_text) == n,
                f"vector row count mismatch at Atlas {index}")
        vectors = []
        for i, row in enumerate(vector_text):
            require(isinstance(row, list) and len(row) == n,
                    f"vector dimension mismatch at Atlas {index}")
            vectors.append([fraction(x, f"{label}.rational_unit_vectors[{i}][{j}]")
                            for j, x in enumerate(row)])
        for row in vectors:
            require(dot(row, row) == 1, f"nonunit rational vector at Atlas {index}")

        require(isinstance(gram_text, list) and len(gram_text) == n,
                f"Gram row count mismatch at Atlas {index}")
        stored_gram = []
        for i, row in enumerate(gram_text):
            require(isinstance(row, list) and len(row) == n,
                    f"Gram dimension mismatch at Atlas {index}")
            stored_gram.append([fraction(x, f"{label}.rational_gram_matrix[{i}][{j}]")
                                for j, x in enumerate(row)])
        computed_gram = [[dot(vectors[i], vectors[j]) for j in range(n)] for i in range(n)]
        require(matrix_equal(stored_gram, computed_gram), f"Gram factor mismatch at Atlas {index}")
        # Exact PSD check: x^T R x = ||U^T x||^2 >= 0 for all rational x.
        require(all(stored_gram[i][i] == 1 for i in range(n)),
                f"Gram diagonal mismatch at Atlas {index}")
        require(all(stored_gram[i][j] == stored_gram[j][i]
                    for i in range(n) for j in range(n)),
                f"Gram asymmetry at Atlas {index}")

        terms, cost = exact_cost(edges, stored_gram)
        stored_terms = r.get("edge_terms")
        require(isinstance(stored_terms, list) and len(stored_terms) == m,
                f"edge-term count mismatch at Atlas {index}")
        for term_index, (stored, (edge, rho, term_cost)) in enumerate(zip(stored_terms, terms)):
            require(isinstance(stored, dict), f"edge term is not an object at Atlas {index}")
            require(set(stored) == {"edge", "correlation", "cost"},
                    f"edge-term fields changed at Atlas {index}")
            require(strict_edge_list([stored.get("edge")],
                                     f"{label}.edge_terms[{term_index}].edge")[0] == edge,
                    f"edge-term edge mismatch at Atlas {index}")
            require(fraction(stored.get("correlation"),
                             f"{label}.edge_terms[{term_index}].correlation") == rho,
                    f"edge-term correlation mismatch at Atlas {index}")
            require(fraction(stored.get("cost"),
                             f"{label}.edge_terms[{term_index}].cost") == term_cost,
                    f"edge-term cost mismatch at Atlas {index}")
        require(fraction(r.get("edge_cost"), label + ".edge_cost") == cost,
                f"edge cost mismatch at Atlas {index}")
        excess = cost - m
        require(fraction(r.get("edge_cost_minus_m"), label + ".edge_cost_minus_m") == excess,
                f"edge excess mismatch at Atlas {index}")

        # Since excess+4>0, excess < 4*sqrt(5)-4 iff (excess+4)^2 < 80.
        require(excess + 4 > 0, f"radical test sign premise fails at Atlas {index}")
        p, q = excess.numerator, excess.denominator
        integer_slack = 80 * q * q - (p + 4 * q) ** 2
        require(integer_slack > 0, f"DNN threshold certificate fails at Atlas {index}")
        radical = r.get("radical_test")
        require(isinstance(radical, dict), f"radical test missing at Atlas {index}")
        require(set(radical) == {"claim", "equivalent_positive_quantity_test", "integer_slack"},
                f"radical-test fields changed at Atlas {index}")
        require(string(radical.get("claim"), label + ".radical_test.claim") ==
                "edge_cost_minus_m < 4*sqrt(5)-4",
                f"radical claim changed at Atlas {index}")
        require(string(radical.get("equivalent_positive_quantity_test"),
                       label + ".radical_test.equivalent_positive_quantity_test") ==
                "(edge_cost_minus_m+4)^2 < 80",
                f"radical equivalence changed at Atlas {index}")
        slack_text = string(radical.get("integer_slack"), label + ".radical_test.integer_slack")
        require(re.fullmatch(r"[1-9][0-9]*", slack_text) is not None,
                f"stored radical slack is not a positive decimal integer at Atlas {index}")
        require(int(slack_text) == integer_slack,
                f"stored radical slack mismatch at Atlas {index}")
        minimum_integer_slack = (integer_slack if minimum_integer_slack is None
                                 else min(minimum_integer_slack, integer_slack))

        scope = "single_positive_rank_block" if source_single else "multiblock"
        if scope == "single_positive_rank_block":
            single_count += 1
        else:
            multi_count += 1
        old = maximum_by_scope.get(scope)
        if old is None or excess > old[0]:
            maximum_by_scope[scope] = (
                excess,
                string(source.get("graph6"), f"enumeration Atlas {index}.graph6"),
                index,
            )
        total_edges += m

    require(single_count == 95 and multi_count == 7, "certificate scope counts changed")
    require(total_edges == sum(integer(r.get("m"), "selected enumeration m")
                               for r in selected_by_index.values()),
            "certificate edge total changed")
    require(minimum_integer_slack is not None and minimum_integer_slack > 0,
            "no positive radical slack")
    return maximum_by_scope


def attach_two_c5(center_n, center_edges, ports):
    require(is_int(center_n) and center_n >= 1, "center order must be a positive integer")
    require(len(ports) == 2 and all(is_int(port) and 0 <= port < center_n for port in ports),
            "attachment ports must be two center vertex integers")
    edges = list(center_edges)
    n = center_n
    bridge_edges = []
    cycles = []
    for port in ports:
        cyc = list(range(n, n + 5))
        n += 5
        bridge = (port, cyc[0])
        edges.append(bridge)
        bridge_edges.append(bridge)
        for i in range(5):
            a, b = cyc[i], cyc[(i + 1) % 5]
            edges.append((min(a, b), max(a, b)))
        cycles.append(cyc)
    return n, tuple(sorted(edges)), bridge_edges, cycles


def verify_local_correlation(matrix_text, expected_order, expected_edge_cost, label):
    require(isinstance(matrix_text, list) and len(matrix_text) == expected_order,
            f"{label} correlation order changed")
    R = []
    for i, row in enumerate(matrix_text):
        require(isinstance(row, list) and len(row) == expected_order,
                f"{label} correlation is not square")
        R.append([fraction(x, f"{label}.dual_correlation[{i}][{j}]")
                  for j, x in enumerate(row)])
    n = len(R)
    require(all(R[i][i] == 1 for i in range(n)), f"{label} correlation diagonal mismatch")
    require(all(R[i][j] == R[j][i] for i in range(n) for j in range(n)),
            f"{label} correlation asymmetry")
    # R has off-diagonal -1/(n-1), so
    # x^T R x = n/(n-1) * sum_i (x_i-mean(x))^2 >= 0 exactly.
    off = Q(-1, n - 1)
    require(all(R[i][j] == (1 if i == j else off) for i in range(n) for j in range(n)),
            f"{label} equicorrelation entries changed")
    edges = tuple((i, j) for j in range(1, n) for i in range(j))
    _, cost = exact_cost(edges, R)
    require(cost == expected_edge_cost, f"{label} exact feasible edge cost changed")
    return cost


def verify_complete_graph_kappa_lower_witness(order, expected_kappa):
    """Execute the M=J plus Cauchy lower witness for kappa(K_order).

    For every feasible correlation R, M=J=11^T is PSD and
    <J,R>=1^T R 1>=0.  Thus sum_edges R_uv>=-order/2 and
    sum_edges(1-R_uv)<=m+order/2.  Cauchy then gives
    sum_edges 2/(1-R_uv)>=2*m^2/(m+order/2)=(order-1)^2.
    Equality is supplied separately by the stored equicorrelation matrix.
    """
    require(is_int(order) and order >= 2, "complete-graph witness order invalid")
    one = [Q(1)] * order
    M = [[one[i] * one[j] for j in range(order)] for i in range(order)]
    require(all(M[i][j] == 1 for i in range(order) for j in range(order)),
            "M=J entries changed")
    # This factorization executes the exact PSD witness J=1*1^T.
    require(all(M[i][j] == one[i] * one[j]
                for i in range(order) for j in range(order)), "M=J factorization changed")
    m = order * (order - 1) // 2
    correlation_sum_lower = Q(-order, 2)
    denominator_sum_upper = Q(m) - correlation_sum_lower
    require(denominator_sum_upper == Q(order * order, 2),
            "M=J denominator-sum bound changed")
    cauchy_lower = Q(2 * m * m) / denominator_sum_upper
    require(cauchy_lower == Q((order - 1) ** 2),
            "complete-graph Cauchy identity changed")
    require(cauchy_lower == expected_kappa,
            "complete-graph lower-witness value changed")
    return cauchy_lower


def verify_one_vertex_sum_additivity(blocks, center_n, center_edges):
    """Execute the exact block sum arithmetic and overlap accounting."""
    require(blocks, "empty block list")
    edge_union = set()
    vertex_union = set()
    running_kappa = Q(0)
    running_m = 0
    running_n = 0
    for block_number, block in enumerate(blocks):
        vertices, block_edges, block_kappa = block
        vertices = set(vertices)
        block_edges = set(block_edges)
        require(block_edges and all(u in vertices and v in vertices for u, v in block_edges),
                f"block {block_number} has an edge outside its vertices")
        require(not (edge_union & block_edges), f"block {block_number} repeats an edge")
        if vertex_union:
            require(len(vertex_union & vertices) == 1,
                    f"block {block_number} is not joined along exactly one vertex")
            running_n += len(vertices) - 1
        else:
            running_n = len(vertices)
        vertex_union |= vertices
        edge_union |= block_edges
        running_m += len(block_edges)
        running_kappa += block_kappa
    require(vertex_union == set(range(center_n)), "block vertices do not cover center")
    require(edge_union == set(center_edges), "block edges do not partition center")
    require(running_n == center_n and running_m == len(center_edges),
            "one-vertex-sum order/size arithmetic changed")
    require(sum(len(vertices) - 1 for vertices, _edges, _kappa in blocks) + 1 == center_n,
            "one-vertex-sum overlap identity changed")
    return running_kappa, running_m


def verify_n8_witness():
    data = load(WITNESS)
    require(isinstance(data, dict), "witness document must be a JSON object")
    require(set(data) == {
        "center", "center_threshold_test", "claim_boundary",
        "local_exact_kappa_certificates", "port_invariance",
        "repeated_port_representative", "schema",
    }, "witness top-level fields changed")
    require(string(data.get("schema"), "witness.schema") ==
            "rank5-c5-c5-n8-route-witness-v1", "witness schema mismatch")
    require(string(data.get("claim_boundary"), "witness.claim_boundary") ==
            "Exact obstruction to the universal all-center DNN threshold only; not a graph counterexample.",
            "witness claim boundary changed")
    require(string(data.get("port_invariance"), "witness.port_invariance") ==
            "For any two center ports, including equal ports, the block multiset is K4,C3,C3,K2,C5,K2,C5; exact kappa block additivity gives the same route gap.",
            "witness port-invariance statement changed")

    center = data.get("center")
    require(isinstance(center, dict), "witness center must be an object")
    center_graph6 = string(center.get("graph6"), "witness.center.graph6")
    n, edges = graph6_decode(center_graph6)
    require(center_graph6 == "GXgrBC", "witness center graph6 changed")
    require(n == 8 and len(edges) == 12 and len(edges) - n + 1 == 5,
            "witness center order/size/rank changed")
    require(integer(center.get("n"), "witness.center.n") == n and
            integer(center.get("m"), "witness.center.m") == len(edges) and
            integer(center.get("beta"), "witness.center.beta") == 5,
            "stored witness center order/size/rank changed")
    require(strict_edge_list(center.get("edges"), "witness.center.edges") == edges,
            "witness center edges changed")
    scope = scope_data(n, edges)
    require(not scope["bridges"], "witness center is not bridge-free")
    require(scope["positive_rank_profile"] == [3, 1, 1],
            "witness positive block profile changed")
    require(not scope["single_positive_rank_block"],
            "witness incorrectly became a one-positive-block graph")
    require(scope["articulations"] == [2], "witness articulation changed")

    blocks = center.get("blocks")
    require(isinstance(blocks, list) and len(blocks) == 3, "witness block count changed")
    expected_block_vertices = [[1, 2, 6, 7], [0, 2, 4], [2, 3, 5]]
    expected_block_edges = [
        [(1, 2), (1, 6), (2, 6), (1, 7), (2, 7), (6, 7)],
        [(0, 2), (0, 4), (2, 4)],
        [(2, 3), (2, 5), (3, 5)],
    ]
    expected_block_ranks = [3, 1, 1]
    parsed_blocks = []
    for i, block in enumerate(blocks):
        require(isinstance(block, dict), f"witness block {i} must be an object")
        vertices = strict_int_list(block.get("vertices"), f"witness.center.blocks[{i}].vertices")
        block_edges = strict_edge_list(block.get("edges"), f"witness.center.blocks[{i}].edges")
        rank = integer(block.get("rank"), f"witness.center.blocks[{i}].rank")
        require(vertices == expected_block_vertices[i], "witness block vertices changed")
        require(list(block_edges) == expected_block_edges[i], "witness block edges changed")
        require(rank == expected_block_ranks[i], "witness block ranks changed")
        require(len(block_edges) - len(vertices) + 1 == rank, "witness block rank arithmetic changed")
        parsed_blocks.append((vertices, block_edges))

    local = data.get("local_exact_kappa_certificates")
    require(isinstance(local, dict), "local kappa certificates must be an object")
    K4 = local.get("K4")
    C3 = local.get("C3")
    require(isinstance(K4, dict) and isinstance(C3, dict), "missing K4/C3 kappa certificate")
    require(string(K4.get("primal"), "witness.local.K4.primal") ==
            "M=J_4 gives objective 9", "K4 lower-witness description changed")
    require(string(C3.get("primal"), "witness.local.C3.primal") ==
            "M=J_3 gives objective 4", "C3 lower-witness description changed")
    require(fraction(K4.get("dual_edge_cost"), "witness.local.K4.dual_edge_cost") == Q(9),
            "stored K4 feasible cost changed")
    require(fraction(C3.get("dual_edge_cost"), "witness.local.C3.dual_edge_cost") == Q(4),
            "stored C3 feasible cost changed")

    k4_upper = verify_local_correlation(K4.get("dual_correlation"), 4, Q(9), "K4")
    c3_upper = verify_local_correlation(C3.get("dual_correlation"), 3, Q(4), "C3")
    k4_lower = verify_complete_graph_kappa_lower_witness(4, Q(9))
    c3_lower = verify_complete_graph_kappa_lower_witness(3, Q(4))
    require(k4_lower == k4_upper == 9 and c3_lower == c3_upper == 4,
            "local K4/C3 lower and upper witnesses do not meet")

    kappa_blocks = center.get("kappa_blocks")
    require(isinstance(kappa_blocks, list) and len(kappa_blocks) == 3,
            "witness kappa block list changed")
    expected_kappa_rows = (("K4", 6, 9, 3), ("C3", 3, 4, 1), ("C3", 3, 4, 1))
    for i, (block_type, block_m, block_kappa, excess) in enumerate(expected_kappa_rows):
        row = kappa_blocks[i]
        require(isinstance(row, dict), f"witness kappa block {i} must be an object")
        require(string(row.get("type"), f"witness.center.kappa_blocks[{i}].type") == block_type and
                integer(row.get("m"), f"witness.center.kappa_blocks[{i}].m") == block_m and
                integer(row.get("kappa"), f"witness.center.kappa_blocks[{i}].kappa") == block_kappa and
                integer(row.get("excess"), f"witness.center.kappa_blocks[{i}].excess") == excess,
                f"witness kappa block {i} changed")
        require(block_kappa - block_m == excess, f"witness kappa block {i} excess changed")

    block_inputs = [
        (parsed_blocks[0][0], parsed_blocks[0][1], k4_upper),
        (parsed_blocks[1][0], parsed_blocks[1][1], c3_upper),
        (parsed_blocks[2][0], parsed_blocks[2][1], c3_upper),
    ]
    center_kappa, center_m = verify_one_vertex_sum_additivity(block_inputs, n, edges)
    require(center_kappa == 9 + 4 + 4 == 17 and center_m == 6 + 3 + 3 == 12,
            "witness exact block-additivity arithmetic changed")
    require(integer(center.get("kappa"), "witness.center.kappa") == center_kappa and
            integer(center.get("kappa_minus_m"), "witness.center.kappa_minus_m") ==
            center_kappa - center_m == 5,
            "witness center kappa data changed")

    threshold = data.get("center_threshold_test")
    require(isinstance(threshold, dict), "center threshold test must be an object")
    require(string(threshold.get("actual"), "witness.center_threshold_test.actual") == "5" and
            string(threshold.get("required"), "witness.center_threshold_test.required") ==
            "kappa(C)-m(C) <= 4*sqrt(5)-4" and
            string(threshold.get("positive_gap"), "witness.center_threshold_test.positive_gap") ==
            "9-4*sqrt(5)" and
            string(threshold.get("integer_sign_test"),
                   "witness.center_threshold_test.integer_sign_test") ==
            "9^2-(4^2*5)=1>0", "witness threshold statement changed")
    require(9 > 0 and 4 > 0 and 9 * 9 - 16 * 5 == 1,
            "witness radical sign certificate changed")

    representative = data.get("repeated_port_representative")
    require(isinstance(representative, dict), "repeated-port representative must be an object")
    ports = strict_int_list(representative.get("ports"), "witness.representative.ports")
    require(ports == [2, 2], "repeated witness ports changed")
    full_n, full_edges, bridge_edges, cycles = attach_two_c5(n, edges, tuple(ports))
    require(full_n == 18 and len(full_edges) == 24 and len(full_edges) - full_n + 1 == 7,
            "attached witness order/size/rank changed")
    require(integer(representative.get("n"), "witness.representative.n") == full_n and
            integer(representative.get("m"), "witness.representative.m") == len(full_edges) and
            integer(representative.get("beta"), "witness.representative.beta") == 7,
            "stored attached witness order/size/rank mismatch")
    require(strict_edge_list(representative.get("edges"), "witness.representative.edges") == full_edges,
            "stored attached witness edges mismatch")
    require(string(representative.get("graph6"), "witness.representative.graph6") ==
            graph6_encode(full_n, full_edges), "stored attached witness graph6 mismatch")
    require(strict_edge_list(representative.get("bridge_edges"),
                             "witness.representative.bridge_edges") == tuple(bridge_edges),
            "stored attached witness bridge mismatch")
    stored_cycles = representative.get("cycle_vertices")
    require(isinstance(stored_cycles, list) and
            [strict_int_list(row, f"witness.representative.cycle_vertices[{i}]")
             for i, row in enumerate(stored_cycles)] == cycles,
            "stored attached witness cycle vertices changed")
    require(sorted(bridges(full_n, full_edges)) == sorted(bridge_edges),
            "attached witness bridge structure changed")
    full_scope = scope_data(full_n, full_edges)
    require(full_scope["positive_rank_profile"] == [3, 1, 1, 1, 1],
            "attached witness block rank profile changed")

    # Exact arithmetic in Q(sqrt(5)): each bridge K2 has kappa 1, and each
    # C5 has kappa 10-2*sqrt(5).  Block addition therefore gives
    # 17 + 2*1 + 2*(10-2*sqrt(5)) = 39-4*sqrt(5).
    def add_radical(*values):
        return (sum((value[0] for value in values), Q(0)),
                sum((value[1] for value in values), Q(0)))

    center_radical = (Q(17), Q(0))
    bridge_radical = (Q(1), Q(0))
    c5_radical = (Q(10), Q(-2))
    exact_kappa = add_radical(center_radical, bridge_radical, bridge_radical,
                              c5_radical, c5_radical)
    require(exact_kappa == (Q(39), Q(-4)),
            "attached exact kappa block sum changed")
    exact_m = center_m + 2 * 1 + 2 * 5
    require(exact_m == 24, "attached block edge-count sum changed")
    cap = exact_m + 6
    route_gap = add_radical(exact_kappa, (Q(-cap), Q(0)))
    require(cap == 30 and route_gap == (Q(9), Q(-4)),
            "attached route-gap arithmetic changed")
    require(string(representative.get("exact_kappa"), "witness.representative.exact_kappa") ==
            "39-4*sqrt(5)" and
            string(representative.get("dnn_target_cap"), "witness.representative.dnn_target_cap") ==
            "m+6=30" and
            string(representative.get("route_gap"), "witness.representative.route_gap") ==
            "9-4*sqrt(5)>0", "stored attached route arithmetic changed")
    require(route_gap[0] > 0 and -route_gap[1] > 0 and
            route_gap[0] ** 2 - route_gap[1] ** 2 * 5 == 1,
            "attached route-gap sign changed")

    # Port invariance is checked over all ordered pairs, including repeats.
    for u in range(n):
        for v in range(n):
            N, E, B, _ = attach_two_c5(n, edges, (u, v))
            require(N == 18 and len(E) == 24 and len(E) - N + 1 == 7,
                    "port-dependent order/size/rank")
            require(sorted(bridges(N, E)) == sorted(B), "port-dependent bridge structure")
            require(scope_data(N, E)["positive_rank_profile"] == [3, 1, 1, 1, 1],
                    "port-dependent block profile")


def report():
    manifest_count = verify_manifest()
    _, selected = verify_atlas_and_enumeration()
    maxima = verify_certificates(selected)
    verify_n8_witness()
    single = maxima["single_positive_rank_block"]
    multi = maxima["multiblock"]
    lines = [
        "PASS exact rank-5 / (C5,C5) DNN candidate-evidence bundle",
        f"strict source lock: {manifest_count} artifacts; SHA256SUMS excluded from itself",
        "NetworkX 3.7 BSD-3-Clause redistribution license: pinned and verified",
        "conditional on standard Graph Atlas exhaustiveness through n=7: 1253 source graphs",
        "connected beta=5 in pinned source: 153",
        "certified bridge-free cores: 102 = 95 single-positive-block + 7 multiblock",
        f"largest stored single-block rational excess: {single[1]} (Atlas {single[2]})",
        f"largest stored multiblock rational excess: {multi[1]} (Atlas {multi[2]})",
        "all 102 exact tests: (edge_cost-m+4)^2 < 80",
        "n=8 witness: GXgrBC = K4 vee C3 vee C3, exact excess 5",
        "exact K4/C3 lower witnesses and one-vertex-sum arithmetic: PASS",
        "exact route gap after two C5 bridge arms: 9-4*sqrt(5) > 0",
        "scope: universal all-center DNN threshold refuted; no graph-theorem closure",
    ]
    return "\n".join(lines) + "\n"


def main():
    output = report()
    if sys.flags.optimize == 0 and "--optimized-child" not in sys.argv:
        child = subprocess.run(
            [sys.executable, "-I", "-S", "-B", "-O", str(Path(__file__).resolve()),
             "--optimized-child"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        require(child.returncode == 0,
                "optimized verifier failed: " + child.stderr.decode("utf-8", errors="replace"))
        require(child.stderr == b"", "optimized verifier wrote to stderr")
        require(child.stdout == output.encode("utf-8"), "normal/-O deterministic output mismatch")
    sys.stdout.write(output)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
