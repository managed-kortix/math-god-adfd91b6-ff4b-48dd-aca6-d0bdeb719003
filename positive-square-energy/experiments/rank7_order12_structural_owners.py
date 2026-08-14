#!/usr/bin/env python3
"""Exact payload-free owner scan for rank-seven/order-twelve census chunks.

Rows are assigned, in order, to balanced rank one, signed imbalance, symbolic
simplex/mixed atoms, and two simple-cubic nonlocal candidates.  Compressed JSON
is consumed as a stream: the multi-million-row residual arrays are never held
in memory.  Every decision uses integer or rational arithmetic.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from collections import Counter, deque
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ATOM_RECOGNIZER = HERE / "rank7_order7_symbolic_atom_recognizer.py"
F = Fraction
BUDGET = F(6)
ORDER = 12
RANK = 7
PATH_COUNT = 18
TARGETS_PER_ROW = 19
CHUNK_SCHEMA = "rank-seven-orders9-12-exact-residual-census-chunk-v1"
SCHEMA = "rank-seven-order-twelve-structural-owner-scan-v3"
LANES = ("balanced-rank-one", "signed-imbalance-psd", "simplex-mixed-atom",
         "cubic-cycle-space-candidate")
ATOM_OPTIONAL_COUNTS = {
    0: {10, 12, 15, 18}, 1: {12, 15}, 2: {9, 12}, 3: {6, 9},
    4: {6}, 5: {3}, 6: {0},
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject(value):
        raise RuntimeError(f"nonstandard constant in {label}: {value}")

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                          parse_constant=reject)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def load_atom_recognizer():
    spec = importlib.util.spec_from_file_location("rank7_order12_atom_core",
                                                  ATOM_RECOGNIZER)
    require(spec is not None and spec.loader is not None,
            "cannot load symbolic atom recognizer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ORDER = ORDER
    module.PATH_COUNT = PATH_COUNT
    module.BUDGET = RANK - 1
    return module


def _raw_blocks(path, raw_digest):
    opener = lzma.open if path.suffix == ".xz" else open
    try:
        with opener(path, "rb") as stream:
            while True:
                block = stream.read(1 << 20)
                if not block:
                    break
                raw_digest.update(block)
                yield block
    except lzma.LZMAError as error:
        raise RuntimeError(f"bad XZ chunk: {path.name}") from error


def stream_chunk(path):
    """Yield ``(header, records, finish)`` without retaining the residual list."""
    artifact_digest = file_sha256(path)
    raw_digest = hashlib.sha256()
    blocks = iter(_raw_blocks(path, raw_digest))
    marker = b'"residuals":['
    prefix = bytearray()
    pending = b""
    for block in blocks:
        pending += block
        position = pending.find(marker)
        if position >= 0:
            prefix.extend(pending[:position])
            pending = pending[position + len(marker):]
            break
        keep = len(marker) - 1
        prefix.extend(pending[:-keep])
        pending = pending[-keep:]
    else:
        raise RuntimeError(f"missing residual stream: {path.name}")

    header = strict_json(bytes(prefix) + b'"residuals":[]}', path.name + " header")
    require(list(header) == sorted(header), f"noncanonical key order: {path.name}")
    state = {"suffix": None}

    def records():
        nonlocal pending
        first = True
        while True:
            while not pending:
                try:
                    pending = next(blocks)
                except StopIteration as error:
                    raise RuntimeError(f"truncated residual stream: {path.name}") from error
            if pending.startswith(b"]"):
                pending = pending[1:]
                break
            expected = b"{" if first else b",{"
            while len(pending) < len(expected):
                pending += next(blocks)
            require(pending.startswith(expected), f"bad residual separator: {path.name}")
            if not first:
                pending = pending[1:]
            first = False
            end = pending.find(b"},{")
            array_end = pending.find(b'}],"')
            while end < 0 and array_end < 0:
                try:
                    pending += next(blocks)
                except StopIteration as error:
                    raise RuntimeError(f"truncated residual record: {path.name}") from error
                end = pending.find(b"},{")
                array_end = pending.find(b'}],"')
            if array_end >= 0 and (end < 0 or array_end < end):
                end = array_end + 1
            else:
                end += 1
            encoded, pending = pending[:end], pending[end:]
            record = strict_json(encoded, path.name + " residual")
            require(encoded == canonical_bytes(record)[:-1],
                    f"noncanonical residual record: {path.name}")
            yield record

        suffix = bytearray(pending)
        for block in blocks:
            suffix.extend(block)
        require(suffix.endswith(b"\n"), f"missing canonical newline: {path.name}")
        tail = strict_json(b'{"residuals":[]' + bytes(suffix[:-1]), path.name + " tail")
        tail.pop("residuals")
        require(not set(header).intersection(tail), f"duplicate split key: {path.name}")
        header.update(tail)
        require(list(header) == sorted(header), f"noncanonical key order: {path.name}")
        state["suffix"] = True

    def finish():
        require(state["suffix"], f"residual stream not exhausted: {path.name}")
        require(header.get("schema") == CHUNK_SCHEMA and
                (header.get("rank"), header.get("order"), header.get("path_count")) ==
                (RANK, ORDER, PATH_COUNT), f"wrong chunk scope: {path.name}")
        return raw_digest.hexdigest(), artifact_digest

    return header, records(), finish


def path_ledger(edges, row):
    paths = []
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        require(type(odd) is int and 0 <= odd <= multiplicity, "nonphysical parity row")
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge_index, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "row does not have eighteen paths")
    return tuple(paths)


def balanced_rank_one(edges, row):
    adjacency = [[] for _ in range(ORDER)]
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        if odd not in (0, multiplicity):
            return False
        parity = bool(odd)
        adjacency[u].append((v, parity))
        adjacency[v].append((u, parity))
    signs = [None] * ORDER
    for root in range(ORDER):
        if signs[root] is not None:
            continue
        signs[root] = 0
        queue = [root]
        for vertex in queue:
            for neighbor, parity in adjacency[vertex]:
                expected = signs[vertex] ^ parity
                if signs[neighbor] is None:
                    signs[neighbor] = expected
                    queue.append(neighbor)
                elif signs[neighbor] != expected:
                    return False
    return True


def path_bound(correlation, length):
    transformed = -correlation if length & 1 else correlation
    if transformed <= -1 or transformed > 1:
        return None
    return (1 - transformed) / (length * (1 + transformed))


def signed_imbalance_certificate(edges, row):
    imbalance = {}
    absolute_rows = [0] * ORDER
    weighted_rows = [0] * ORDER
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        value = multiplicity - 2 * odd
        imbalance[u, v] = value
        absolute_rows[u] += abs(value)
        absolute_rows[v] += abs(value)
        weighted_rows[u] += multiplicity
        weighted_rows[v] += multiplicity
    lower = max(absolute_rows)
    if lower == 0:
        return None
    upper = max(lower, 2 * max(weighted_rows))
    paths = path_ledger(edges, row)
    best = None
    for denominator in range(lower, upper + 1):
        total = F()
        for _, _, u, v, length in paths:
            value = imbalance[u, v]
            transformed = -value if length & 1 else value
            if transformed <= -denominator or transformed > denominator:
                break
            total += F(denominator - transformed,
                       length * (denominator + transformed))
            if total > BUDGET:
                break
        else:
            if best is None or total < best[1]:
                best = denominator, total
    return best


def atom_profile_candidate(edges, row):
    """Cheap exact filter for every mixed/simplex profile of total cost six."""
    mixed = optional = 0
    for (_, _, multiplicity), odd in zip(edges, row, strict=True):
        if (multiplicity, odd) == (2, 1):
            mixed += 1
        elif (multiplicity, odd) == (1, 1):
            optional += 1
        elif odd not in (0, multiplicity):
            return False
    return optional in ATOM_OPTIONAL_COUNTS.get(mixed, ())


def simple_cubic(edges):
    degree = [0] * ORDER
    if len(edges) != PATH_COUNT or any(edge[2] != 1 for edge in edges):
        return False
    for u, v, _ in edges:
        degree[u] += 1
        degree[v] += 1
    return degree == [3] * ORDER


def cubic_kernel(edges):
    degree = [0] * ORDER
    if sum(edge[2] for edge in edges) != PATH_COUNT:
        return False
    for u, v, multiplicity in edges:
        if not (0 <= u < v < ORDER and multiplicity > 0):
            return False
        degree[u] += multiplicity
        degree[v] += multiplicity
    return degree == [3] * ORDER


def three_ray_edge_cost(multiplicity, odd, left, right):
    """Return 18 times the path cost, or None for an antipodal path.

    State ``2*c+s`` is the signed copy ``(-1)^s`` of ray ``c``.  The three
    unsigned rays have mutual inner product -1/2.  Scaling by 18 makes every
    possible length-one, -two, and -three cost integral.
    """
    left_color, left_sign = divmod(left, 2)
    right_color, right_sign = divmod(right, 2)
    same_sign = left_sign == right_sign
    if left_color == right_color:
        correlation = 2 if same_sign else -2
    else:
        correlation = -1 if same_sign else 1
    total = 0
    lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
    for length in lengths:
        transformed = -correlation if length & 1 else correlation
        if transformed == -2:
            return None
        total += {2: 0, 1: 6 // length, -1: 54 // length}[transformed]
    return total


def simple_signed_three_ray_witness(edges, row):
    """Return a six-state witness for the simple-cubic zero-cost case."""
    if not simple_cubic(edges) or any(value not in (0, 1) for value in row):
        return None
    adjacency = [[] for _ in range(ORDER)]
    for edge_index, (u, v, _) in enumerate(edges):
        adjacency[u].append((v, row[edge_index]))
        adjacency[v].append((u, row[edge_index]))
    allowed = [[[False] * 6 for _ in range(6)] for _ in range(2)]
    for parity in range(2):
        for left in range(6):
            left_color, left_sign = divmod(left, 2)
            for right in range(6):
                right_color, right_sign = divmod(right, 2)
                allowed[parity][left][right] = parity == (
                    left_sign ^ right_sign ^ (left_color != right_color))
    domains = [0b111111] * ORDER
    domains[0] = 1

    def solve(local):
        queue = deque(range(ORDER))
        while queue:
            vertex = queue.popleft()
            source = local[vertex]
            for neighbor, parity in adjacency[vertex]:
                old = local[neighbor]
                new = sum(1 << target for target in range(6)
                          if old & (1 << target) and any(
                              source & (1 << state) and allowed[parity][state][target]
                              for state in range(6)))
                if not new:
                    return None
                if new != old:
                    local[neighbor] = new
                    queue.append(neighbor)
        choices = [(mask.bit_count(), vertex) for vertex, mask in enumerate(local)
                   if mask & (mask - 1)]
        if not choices:
            return tuple(mask.bit_length() - 1 for mask in local)
        _, vertex = min(choices)
        mask = local[vertex]
        while mask:
            bit = mask & -mask
            mask -= bit
            child = local.copy()
            child[vertex] = bit
            witness = solve(child)
            if witness is not None:
                return witness
        return None

    return solve(domains)


def simple_signed_three_ray_owner(edges, row):
    return simple_signed_three_ray_witness(edges, row) is not None


def three_ray_witness_cost(edges, row, states):
    """Return the exact cost scaled by 18, rejecting malformed witnesses."""
    if (len(states) != ORDER or any(type(state) is not int or not 0 <= state < 6
                                    for state in states)):
        return None
    total = 0
    for (u, v, multiplicity), odd in zip(edges, row, strict=True):
        value = three_ray_edge_cost(multiplicity, odd, states[u], states[v])
        if value is None:
            return None
        total += value
    return total


def _signed_three_ray_witness(edges, row, cubic_only):
    """Find an exact switched three-ray witness, with total cost at most six."""
    if ((cubic_only and not cubic_kernel(edges)) or
            sum(edge[2] for edge in edges) != PATH_COUNT or
            any(not (0 <= edge[0] < edge[1] < ORDER and edge[2] > 0)
                for edge in edges) or
            any(type(value) is not int or value < 0 or value > edge[2]
                for edge, value in zip(edges, row, strict=True))):
        return None
    if cubic_only:
        witness = simple_signed_three_ray_witness(edges, row)
        if witness is not None:
            return witness
    tables = []
    incident = [[] for _ in range(ORDER)]
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row, strict=True)):
        table = tuple(tuple(three_ray_edge_cost(multiplicity, odd, left, right)
                            for right in range(6)) for left in range(6))
        if all(value is None or value > 108 for values in table for value in values):
            return None
        tables.append(table)
        incident[u].append((edge_index, v, False))
        incident[v].append((edge_index, u, True))

    states = [-1] * ORDER
    states[0] = 0

    def lower_bound():
        result = 0
        for edge_index, (u, v, _) in enumerate(edges):
            if states[u] >= 0 and states[v] >= 0:
                continue
            if states[u] >= 0:
                values = tables[edge_index][states[u]]
            elif states[v] >= 0:
                values = tuple(table[states[v]] for table in tables[edge_index])
            else:
                values = tuple(value for values in tables[edge_index] for value in values)
            finite = tuple(value for value in values if value is not None)
            if not finite:
                return 109
            result += min(finite)
        return result

    def solve(assigned, cost):
        if cost + lower_bound() > 108:
            return None
        if assigned == ORDER:
            return tuple(states)
        vertex = max((v for v in range(ORDER) if states[v] < 0),
                     key=lambda v: sum(states[w] >= 0 for _, w, _ in incident[v]))
        choices = []
        for state in range(6):
            added = 0
            for edge_index, neighbor, reversed_edge in incident[vertex]:
                if states[neighbor] < 0:
                    continue
                value = (tables[edge_index][states[neighbor]][state] if reversed_edge else
                         tables[edge_index][state][states[neighbor]])
                if value is None:
                    break
                added += value
            else:
                choices.append((added, state))
        for added, state in sorted(choices):
            if cost + added <= 108:
                states[vertex] = state
                witness = solve(assigned + 1, cost + added)
                if witness is not None:
                    return witness
                states[vertex] = -1
        return None

    return solve(1, 0)


def signed_three_ray_witness(edges, row):
    """Return a cost-at-most-six witness for a loopless cubic multikernel."""
    return _signed_three_ray_witness(edges, row, True)


def signed_three_ray_owner(edges, row):
    """Exact switched three-ray owner for every loopless cubic multikernel."""
    return signed_three_ray_witness(edges, row) is not None


def generalized_three_ray_witness(edges, row):
    """Return a cost-at-most-six witness for an arbitrary loopless multikernel."""
    return _signed_three_ray_witness(edges, row, False)


def generalized_three_ray_owner(edges, row):
    """Exact switched three-ray owner for an arbitrary loopless multikernel."""
    return generalized_three_ray_witness(edges, row) is not None


def signed_adjacency_square_owner(edges, row, radius=8):
    if not simple_cubic(edges) or any(value not in (0, 1) for value in row):
        return None
    signed = [[0] * ORDER for _ in range(ORDER)]
    for (u, v, _), parity in zip(edges, row, strict=True):
        signed[u][v] = signed[v][u] = -1 if parity else 1
    square = [[sum(signed[u][w] * signed[w][v] for w in range(ORDER))
               for v in range(ORDER)] for u in range(ORDER)]
    best = None
    for a in range(1, radius + 1):
        for b in range(-radius, radius + 1):
            if b == 0:
                continue
            denominator = a * a + 3 * b * b
            costs = []
            for (u, v, _), parity in zip(edges, row, strict=True):
                numerator = 2 * a * b * signed[u][v] + b * b * square[u][v]
                cost = path_bound(F(numerator, denominator), 1 if parity else 2)
                if cost is None:
                    break
                costs.append(cost)
            else:
                total = sum(costs, F())
                if total <= BUDGET and (best is None or total < best[2]):
                    best = a, b, total
    return best


def recognize_row(atom, edges, row):
    if balanced_rank_one(edges, row):
        return "balanced-rank-one", None
    imbalance = signed_imbalance_certificate(edges, row)
    if imbalance is not None:
        return "signed-imbalance-psd", [imbalance[0], imbalance[1].numerator,
                                        imbalance[1].denominator]
    owners = (() if not atom_profile_candidate(edges, row) else
              tuple(record for record in atom.recognize(edges, row)
                    if record["status"] == "exact-equality-owner"))
    if owners:
        profiles = sorted({(record["profile"]["mixed"],
                            tuple(record["profile"]["simplex_widths"]))
                           for record in owners})
        return "simplex-mixed-atom", [[mixed, list(widths)] for mixed, widths in profiles]
    if signed_three_ray_owner(edges, row):
        return "cubic-cycle-space-candidate", ["signed-three-ray"]
    square = signed_adjacency_square_owner(edges, row)
    if square is not None:
        return "cubic-cycle-space-candidate", ["signed-adjacency-square", square[0],
                                                square[1], square[2].numerator,
                                                square[2].denominator]
    return None, None


class RemainderWriter:
    def __init__(self, path):
        require(path.parent.is_dir(), "remainder output parent does not exist")
        self.path = path
        self.stream = path.open("wb")
        self.stream.write((b'{"schema":"rank-seven-order-twelve-rational-search-indices-v1",'
                           b'"source_indices":['))
        self.first = True
        self.count = 0
        self.digest = hashlib.sha256()

    def add(self, index):
        encoded = str(index).encode("ascii")
        self.stream.write((b"" if self.first else b",") + encoded)
        self.first = False
        self.count += 1
        self.digest.update(encoded + b"\n")

    def close(self):
        digest = self.digest.hexdigest().encode("ascii")
        self.stream.write(b'],"source_indices_sha256":"' + digest +
                          b'","source_indices_total":' + str(self.count).encode("ascii") + b'}\n')
        self.stream.close()
        return self.count, digest.decode("ascii"), hashlib.sha256(self.path.read_bytes()).hexdigest()


def scan(paths, progress=False, remainder_output=None, limit=None):
    atom = load_atom_recognizer()
    owner_counts = Counter({lane: 0 for lane in LANES})
    cycle_counts = Counter({"signed-three-ray": 0, "signed-adjacency-square": 0})
    profile_counts = Counter()
    chunks = []
    classification_digest = hashlib.sha256()
    remainder_digest = hashlib.sha256()
    writer = RemainderWriter(remainder_output) if remainder_output else None
    scanned = 0
    stop = False
    for path in paths:
        header, records, finish = stream_chunk(path)
        kernels = {item["order_kernel"]: tuple(map(tuple, item["edges"]))
                   for item in header["kernels"]}
        local_counts = Counter()
        local_scanned = 0
        residual_stream_digest = hashlib.sha256()
        for source in records:
            residual_stream_digest.update(canonical_bytes(source))
            if limit is not None and scanned >= limit:
                stop = True
                continue
            edges = kernels[source["order_kernel"]]
            row = tuple(source["row"])
            owner, detail = recognize_row(atom, edges, row)
            source_index = scanned
            scanned += 1
            local_scanned += 1
            if owner is None:
                encoded = str(source_index).encode("ascii")
                remainder_digest.update(encoded + b"\n")
                if writer:
                    writer.add(source_index)
            else:
                owner_counts[owner] += 1
                local_counts[owner] += 1
                if owner == "cubic-cycle-space-candidate":
                    cycle_counts[detail[0]] += 1
                elif owner == "simplex-mixed-atom":
                    profile_counts.update(f"mixed-{mixed}/simplex-{'-'.join(map(str, widths)) or 'none'}"
                                          for mixed, widths in detail)
            classification_digest.update(canonical_bytes(
                [source_index, source["global_kernel"], source["order_kernel"],
                 source["row"], owner, detail]))
        raw_digest, artifact_digest = finish()
        require(residual_stream_digest.hexdigest() == header["residual_stream_sha256"],
                f"residual digest mismatch: {path.name}")
        if not stop:
            require(local_scanned == header["coarse_residual_total"],
                    f"residual count mismatch: {path.name}")
        chunks.append({"artifact_sha256": artifact_digest,
                       "coarse_residual_total": header["coarse_residual_total"],
                       "kernel_range": header["kernel_range"], "path": path.name,
                       "raw_sha256": raw_digest,
                       "scanned_residual_total": local_scanned,
                       "exclusive_owner_row_counts": dict(sorted(local_counts.items()))})
        if progress:
            print(f"chunk={path.name} scanned={scanned} recognized={sum(owner_counts.values())}",
                  flush=True)
        if stop:
            break
    recognized = sum(owner_counts.values())
    remainder = scanned - recognized
    index_record = None
    if writer:
        count, digest, artifact = writer.close()
        require((count, digest) == (remainder, remainder_digest.hexdigest()),
                "remainder output stream changed")
        index_record = {"artifact_sha256": artifact, "path": remainder_output.name,
                        "source_indices_sha256": digest, "source_indices_total": count}
    return {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "exact payload-free sufficient owners over supplied rank-seven order-twelve chunks",
        "chunks": chunks,
        "scanned_residual_total": scanned,
        "scanned_target_total": scanned * TARGETS_PER_ROW,
        "exclusive_owner_row_counts": dict(sorted(owner_counts.items())),
        "cubic_cycle_space_candidate_counts": dict(sorted(cycle_counts.items())),
        "atom_profile_owner_counts": dict(sorted(profile_counts.items())),
        "recognized_residual_total": recognized,
        "recognized_target_total": recognized * TARGETS_PER_ROW,
        "rational_search_residual_total": remainder,
        "rational_search_target_total": remainder * TARGETS_PER_ROW,
        "rational_search_source_indices_sha256": remainder_digest.hexdigest(),
        "rational_search_index_artifact": index_record,
        "classification_stream_sha256": classification_digest.hexdigest(),
    }


def verify_report(payload):
    require(type(payload) is dict and set(payload) == {
        "schema", "full_theorem", "scope", "chunks", "scanned_residual_total",
        "scanned_target_total", "exclusive_owner_row_counts",
        "cubic_cycle_space_candidate_counts", "atom_profile_owner_counts",
        "recognized_residual_total", "recognized_target_total",
        "rational_search_residual_total", "rational_search_target_total",
        "rational_search_source_indices_sha256", "rational_search_index_artifact",
        "classification_stream_sha256",
    }, "coverage report fields changed")
    require(payload["schema"] == SCHEMA and payload["full_theorem"] is False,
            "wrong coverage report schema")
    require(set(payload["exclusive_owner_row_counts"]) == set(LANES),
            "lane ledger changed")
    require(sum(payload["exclusive_owner_row_counts"].values()) ==
            payload["recognized_residual_total"], "exclusive owner sum changed")
    require(payload["scanned_residual_total"] == payload["recognized_residual_total"] +
            payload["rational_search_residual_total"], "row partition changed")
    for prefix in ("scanned", "recognized", "rational_search"):
        require(payload[f"{prefix}_target_total"] ==
                TARGETS_PER_ROW * payload[f"{prefix}_residual_total"],
                f"{prefix} target total changed")


def read_report(path):
    raw = path.read_bytes()
    payload = strict_json(raw, "order-twelve owner coverage report")
    require(raw == canonical_bytes(payload), "coverage report is not canonical JSON")
    verify_report(payload)
    return payload, raw


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    recognize = subparsers.add_parser("recognize")
    recognize.add_argument("chunks", nargs="+", type=Path)
    recognize.add_argument("--output", type=Path)
    recognize.add_argument("--remainder-output", type=Path)
    recognize.add_argument("--limit", type=int, help="test-only global row limit")
    recognize.add_argument("--progress", action="store_true")
    verify = subparsers.add_parser("verify")
    verify.add_argument("report", type=Path)
    verify.add_argument("chunks", nargs="+", type=Path)
    verify.add_argument("--progress", action="store_true")
    verify.add_argument("--limit", type=int, help="test-only global row limit")
    args = parser.parse_args()
    if args.command is None:
        parser.error("a command is required: recognize or verify")
    if args.command == "verify":
        require(args.limit is None or args.limit >= 0, "negative row limit")
        expected, raw = read_report(args.report)
        require(expected["rational_search_index_artifact"] is None,
                "verification of an external remainder artifact is not supported")
        actual = scan(args.chunks, args.progress, limit=args.limit)
        verify_report(actual)
        require(canonical_bytes(actual) == raw, "coverage report differs from exact rescan")
        print(f"audit=passed report_sha256={hashlib.sha256(raw).hexdigest()} "
              f"recognized_targets={actual['recognized_target_total']}")
        return
    require(args.limit is None or args.limit >= 0, "negative row limit")
    report = scan(args.chunks, args.progress, args.remainder_output, args.limit)
    verify_report(report)
    raw = canonical_bytes(report)
    if args.output is not None:
        require(args.output.parent.is_dir(), "output parent does not exist")
        args.output.write_bytes(raw)
    print(raw.decode("ascii"), end="")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
