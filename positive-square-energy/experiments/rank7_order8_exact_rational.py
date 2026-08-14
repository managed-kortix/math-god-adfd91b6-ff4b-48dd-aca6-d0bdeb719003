#!/usr/bin/env python3
"""Compressed exact-rational witnesses for rank-seven/order-eight residuals.

The search stream is the authenticated 492,812-row complement of the three
payload-free owner lanes. Numerics only propose witnesses; decoded witnesses
and symbolic owner tags are replayed with ``fractions.Fraction``. Fragment
checkpoints are canonical, independently auditable, and resumable. This is an
experiment and makes no theorem claim.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import lzma
import math
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from types import SimpleNamespace


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
LANES_PATH = HERE / "rank7_order8_payload_free_lanes.py"
MANIFEST_PATH = HERE / "rank7_order8_exact_residual_census_manifest.json"
INDICES_PATH = HERE / "rank7_order8_rational_search_indices.json"
MAGIC = b"R7O8G1"
ORDER = DIMENSION = 8
PATH_COUNT = 14
BUDGET = __import__("fractions").Fraction(6)
EXPECTED_RESIDUALS = 492812
EXPECTED_MANIFEST_SHA256 = "5d41e78a2f688f4c3064cb88f1d6d475008d36c84f892edc4cba28ade424fe98"
EXPECTED_INDICES_SHA256 = "245cceaab164ba9c2a604d0db8b09a65598fd52084b1df2363911c6d1d4d3a59"
CACHE_MAGIC = b"R7O8C1"
WARM_CACHE_SCHEMA = "rank-seven-order-eight-numerical-gram-cache-v1"
DEFAULT_WARM_SOURCE = HERE / "rank7_order8_chunk_000000_005000.r7o8g.xz"
FRAGMENT_PATTERN = re.compile(r"fragment-(\d+)-(\d+)\.r7o8g\.xz\Z")
_CENSUS = None
_RESIDUALS = None
_LANES = None
_WARM_GRAMS = None
_WARM_HITS = 0


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_module("rank7_order8_r10_base", BASE_PATH)


def lanes_module():
    global _LANES
    if _LANES is None:
        _LANES = load_module("rank7_order8_stream_lanes", LANES_PATH)
    return _LANES


def load_indices(manifest_digest):
    raw = INDICES_PATH.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_INDICES_SHA256,
            "rational-search index artifact changed")
    lanes = lanes_module()
    payload = lanes.strict_json(raw, INDICES_PATH.name)
    require(raw == lanes.canonical_bytes(payload), "noncanonical rational-search indices")
    require(set(payload) == {"schema", "manifest_sha256", "selected_chunks", "source_indices"}
            and payload["schema"] == "rank-seven-order-eight-rational-search-indices-v1"
            and payload["manifest_sha256"] == manifest_digest
            and payload["selected_chunks"] == list(range(8)),
            "wrong rational-search index scope")
    indices = tuple(payload["source_indices"])
    require(len(indices) == EXPECTED_RESIDUALS and
            all(type(value) is int for value in indices) and
            all(left < right for left, right in zip(indices, indices[1:])),
            "rational-search indices changed")
    return indices


def stream_identity():
    return hashlib.sha256(
        (EXPECTED_MANIFEST_SHA256 + ":" + EXPECTED_INDICES_SHA256).encode("ascii")).hexdigest()


def load_census_module():
    global _CENSUS, _RESIDUALS
    if _CENSUS is not None:
        return _CENSUS
    pairs = tuple((u, v) for u in range(ORDER) for v in range(u + 1, ORDER))
    _CENSUS = SimpleNamespace(SOURCE_SHA256=stream_identity(), PAIRS=pairs)
    return _CENSUS


def materialize_residuals(census):
    global _RESIDUALS
    if _RESIDUALS is not None:
        return _RESIDUALS
    lanes = lanes_module()
    manifest, manifest_digest = lanes.load_manifest(MANIFEST_PATH)
    require(manifest_digest == EXPECTED_MANIFEST_SHA256, "residual manifest changed")
    wanted = load_indices(manifest_digest)
    pair_index = {edge: index for index, edge in enumerate(census.PAIRS)}
    residuals = []
    wanted_position = 0
    source_offset = 0
    for chunk_record in manifest["chunks"]:
        chunk = lanes.read_chunk((MANIFEST_PATH.parent / chunk_record["path"]).resolve(),
                                 chunk_record)
        kernels = {item["order_kernel"]: tuple(map(tuple, item["edges"]))
                   for item in chunk["kernels"]}
        for local_index, source in enumerate(chunk["residuals"]):
            source_index = source_offset + local_index
            if wanted_position == len(wanted) or wanted[wanted_position] != source_index:
                continue
            edges = kernels[source["order_kernel"]]
            support = tuple(pair_index[(u, v)] for u, v, _ in edges)
            multiplicities = tuple(value for _, _, value in edges)
            residuals.append((source["global_kernel"], source_index, support,
                              multiplicities, tuple(source["row"]),
                              source["orbit_size"], None, False))
            wanted_position += 1
        source_offset += chunk_record["coarse_residual_total"]
    require(wanted_position == len(wanted) and len(residuals) == EXPECTED_RESIDUALS,
            "rational-search stream materialization changed")
    _RESIDUALS = tuple(residuals)
    return _RESIDUALS


def cache_bytes(census, residuals):
    payload = bytearray()
    base.put_uvarint(payload, len(residuals))
    for global_kernel, source_index, support, multiplicities, row, orbit_size, cost, template in residuals:
        require(cost is None and template is False, "unexpected cached source metadata")
        base.put_uvarint(payload, global_kernel)
        base.put_uvarint(payload, source_index)
        base.put_uvarint(payload, len(support))
        for dense, multiplicity, odd in zip(support, multiplicities, row):
            base.put_uvarint(payload, dense)
            base.put_uvarint(payload, multiplicity)
            base.put_uvarint(payload, odd)
        base.put_uvarint(payload, orbit_size)
    output = bytearray(CACHE_MAGIC)
    output.extend(bytes.fromhex(census.SOURCE_SHA256))
    output.extend(hashlib.sha256(payload).digest())
    output.extend(payload)
    return bytes(output)


def decode_cache(census, raw):
    header = len(CACHE_MAGIC)
    require(raw[:header] == CACHE_MAGIC and raw[header:header + 32] ==
            bytes.fromhex(census.SOURCE_SHA256), "bad census cache header")
    digest_start = header + 32
    payload_start = digest_start + 32
    require(raw[digest_start:payload_start] == hashlib.sha256(raw[payload_start:]).digest(),
            "census cache payload digest changed")
    position = payload_start
    count, position = base.get_uvarint(raw, position)
    require(count == EXPECTED_RESIDUALS, "wrong census cache row count")
    residuals = []
    previous_source = -1
    for _ in range(count):
        global_kernel, position = base.get_uvarint(raw, position)
        source_index, position = base.get_uvarint(raw, position)
        width, position = base.get_uvarint(raw, position)
        support, multiplicities, row = [], [], []
        for _ in range(width):
            dense, position = base.get_uvarint(raw, position)
            multiplicity, position = base.get_uvarint(raw, position)
            odd, position = base.get_uvarint(raw, position)
            require(dense < len(census.PAIRS) and multiplicity > 0 and odd <= multiplicity,
                    "nonphysical census cache row")
            support.append(dense)
            multiplicities.append(multiplicity)
            row.append(odd)
        orbit_size, position = base.get_uvarint(raw, position)
        require(source_index > previous_source and orbit_size > 0 and
                all(left < right for left, right in zip(support, support[1:])),
                "noncanonical census cache stream")
        previous_source = source_index
        residuals.append((global_kernel, source_index, tuple(support), tuple(multiplicities),
                          tuple(row), orbit_size, None, False))
    require(position == len(raw), "trailing census cache bytes")
    return tuple(residuals)


def residual_rows(census, progress=False, cache_path=None):
    require(census is load_census_module(), "foreign census object")
    global _RESIDUALS
    if _RESIDUALS is not None:
        return _RESIDUALS
    if cache_path is not None and cache_path.is_file():
        try:
            raw = lzma.decompress(cache_path.read_bytes(), format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError("census cache is not a valid XZ stream") from error
        _RESIDUALS = decode_cache(census, raw)
        return _RESIDUALS
    started = time.perf_counter()
    _RESIDUALS = materialize_residuals(census)
    if cache_path is not None:
        raw = cache_bytes(census, _RESIDUALS)
        temporary = cache_path.with_name(cache_path.name + ".tmp")
        temporary.write_bytes(lzma.compress(raw, format=lzma.FORMAT_XZ, preset=3))
        temporary.replace(cache_path)
    if progress:
        print(f"census_rows={len(_RESIDUALS)} census_seconds={time.perf_counter() - started:.6f}",
              flush=True)
    return _RESIDUALS


def source_edges(census, source):
    return tuple((*census.PAIRS[dense], multiplicity)
                 for dense, multiplicity in zip(source[2], source[3]))


def lane_result(census, source):
    lanes = lanes_module()
    return lanes.recognize_row(lanes.load_atom_recognizer(), source_edges(census, source), source[4])


def structural_certified(census, source):
    return lanes_module().signed_imbalance_certificate(source_edges(census, source), source[4]) is not None


def atom_source_indices(residuals):
    # The authenticated index stream is defined as the complement of every
    # payload-free owner, so no rational-search row may receive an atom tag.
    return frozenset()


def verify_atom(census, source):
    owner, matches, _ = lane_result(census, source)
    require(owner == "simplex-mixed-atom" and "simplex-mixed-atom" in matches,
            "bad simplex/mixed payload-free owner")


def objective_terms(paths, vectors):
    correlations = {}
    for _, _, u, v, length in paths:
        key = u, v
        if key not in correlations:
            correlations[key] = base.dot(vectors[u], vectors[v])
        yield u, v, base.path_cost_derivative(correlations[key], length)


def objective_gradient(paths, vectors):
    total = 0.0
    gradient = [[0.0] * DIMENSION for _ in range(ORDER)]
    for u, v, (cost, derivative) in objective_terms(paths, vectors):
        total += cost
        for coordinate in range(DIMENSION):
            gradient[u][coordinate] += derivative * vectors[v][coordinate]
            gradient[v][coordinate] += derivative * vectors[u][coordinate]
    for vertex in range(1, ORDER):
        radial = base.dot(gradient[vertex], vectors[vertex])
        gradient[vertex] = [value - radial * coordinate
                            for value, coordinate in zip(gradient[vertex], vectors[vertex])]
    gradient[0] = [0.0] * DIMENSION
    return total, gradient


def objective(paths, vectors):
    return sum(term[2][0] for term in objective_terms(paths, vectors))


def template_key(census, source):
    edges = tuple((*census.PAIRS[dense], multiplicity, odd)
                  for dense, multiplicity, odd in zip(source[2], source[3], source[4]))
    degrees = [0] * ORDER
    signed_degrees = [0] * ORDER
    for u, v, multiplicity, odd in edges:
        degrees[u] += multiplicity
        degrees[v] += multiplicity
        signed = multiplicity - 2 * odd
        signed_degrees[u] += signed
        signed_degrees[v] += signed
    return (tuple(sorted(zip(degrees, signed_degrees))),
            tuple(sorted((multiplicity, odd) for _, _, multiplicity, odd in edges)))


def refined_signature(census, source):
    edges = tuple((*census.PAIRS[dense], multiplicity, odd)
                  for dense, multiplicity, odd in zip(source[2], source[3], source[4]))
    incident = [[] for _ in range(ORDER)]
    for u, v, multiplicity, odd in edges:
        incident[u].append((multiplicity, odd))
        incident[v].append((multiplicity, odd))
    fingerprints = tuple(tuple(sorted(values)) for values in incident)
    signature = (tuple(sorted((multiplicity, odd)
                              for _, _, multiplicity, odd in edges)),
                 tuple(sorted(fingerprints)))
    order = tuple(sorted(range(ORDER), key=lambda vertex: (fingerprints[vertex], vertex)))
    return signature, order


def source_from_paths(census, paths):
    grouped = defaultdict(list)
    for _, _, u, v, length in paths:
        grouped[min(u, v), max(u, v)].append(length)
    pairs = {pair: dense for dense, pair in enumerate(census.PAIRS)}
    edges = sorted(grouped)
    support = tuple(pairs[edge] for edge in edges)
    multiplicities = tuple(len(grouped[edge]) for edge in edges)
    row = tuple(sum(length & 1 for length in grouped[edge]) for edge in edges)
    return (0, 0, support, multiplicities, row, 1, None, False)


def gram_vectors(gram):
    """Return a deterministic numerical factor of a correlation Gram."""
    vectors = [[0.0] * DIMENSION for _ in range(ORDER)]
    for row in range(ORDER):
        for column in range(row + 1):
            value = gram[row][column] - sum(
                vectors[row][k] * vectors[column][k] for k in range(column))
            if row == column:
                vectors[row][column] = math.sqrt(max(0.0, value))
            elif vectors[column][column] > 1e-12:
                vectors[row][column] = value / vectors[column][column]
        norm = math.sqrt(sum(value * value for value in vectors[row]))
        require(norm > 1e-12, "degenerate cached Gram factor")
        vectors[row] = [value / norm for value in vectors[row]]
    return tuple(tuple(row) for row in vectors)


def warm_cache_payload(census, residuals, pack_path):
    stored = pack_path.read_bytes()
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError("warm source pack is not a valid XZ stream") from error
    start, records = base.exact_decode_pack(census, raw, residuals)
    representatives = {}
    for source_index, ((mode, witness), source) in enumerate(
            zip(records, residuals[start:start + len(records)]), start):
        if mode != base.MODE_SHARED:
            continue
        signature, order = refined_signature(census, source)
        if signature in representatives:
            continue
        _, parameters, _, _ = witness
        vectors = tuple(base.rational_unit(row) for row in parameters)
        gram = tuple(tuple(base.dot(vectors[u], vectors[v]) for v in order) for u in order)
        representatives[signature] = (source_index, gram)
    entries = []
    for signature in sorted(representatives):
        source_index, gram = representatives[signature]
        entries.append({
            "signature": signature,
            "source_index": source_index,
            "gram_hex": [[float(value).hex() for value in row] for row in gram],
        })
    return {
        "schema": WARM_CACHE_SCHEMA,
        "source_stream_sha256": census.SOURCE_SHA256,
        "source_pack_sha256": hashlib.sha256(stored).hexdigest(),
        "source_range": [start, start + len(records)],
        "representative_total": len(entries),
        "entries": entries,
    }


def canonical_json_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def write_warm_cache(census, residuals, pack_path, output):
    payload = warm_cache_payload(census, residuals, pack_path)
    temporary = output.with_name(output.name + ".tmp")
    temporary.write_bytes(lzma.compress(canonical_json_bytes(payload), format=lzma.FORMAT_XZ,
                                        preset=6))
    temporary.replace(output)
    return payload


def nested_tuple(value):
    return tuple(nested_tuple(item) for item in value) if isinstance(value, list) else value


def load_warm_cache(census, path):
    try:
        raw = lzma.decompress(path.read_bytes(), format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError("warm-start cache is not a valid XZ stream") from error
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_json_bytes(payload), "noncanonical warm-start cache")
    require(payload.get("schema") == WARM_CACHE_SCHEMA and
            payload.get("source_stream_sha256") == census.SOURCE_SHA256 and
            payload.get("representative_total") == len(payload.get("entries", ())),
            "warm-start cache identity changed")
    result = {}
    for entry in payload["entries"]:
        signature = nested_tuple(entry["signature"])
        require(signature not in result, "duplicate warm-start signature")
        gram = tuple(tuple(float.fromhex(value) for value in row)
                     for row in entry["gram_hex"])
        require(len(gram) == ORDER and all(len(row) == ORDER for row in gram),
                "bad cached Gram dimensions")
        result[signature] = gram_vectors(gram)
    return result


def warm_vectors(census, source):
    if _WARM_GRAMS is None:
        return None
    signature, order = refined_signature(census, source)
    canonical = _WARM_GRAMS.get(signature)
    if canonical is None:
        return None
    position = {vertex: index for index, vertex in enumerate(order)}
    return tuple(canonical[position[vertex]] for vertex in range(ORDER))


def optimize(paths, seed, restarts, iterations, warm=()):
    global _WARM_HITS
    cached = None
    if _WARM_GRAMS is not None:
        cached = warm_vectors(load_census_module(), source_from_paths(load_census_module(), paths))
    if cached is not None:
        _WARM_HITS += 1
        warm = (cached,) + tuple(warm)
        generator = random.Random(seed)
        starts = list(warm) + [base.random_vectors(generator)
                               for _ in range(max(0, restarts - len(warm)))]
        require(starts, "optimizer has no starts")
        return min((base.descend(paths, initial, iterations) for initial in starts),
                   key=lambda row: row[0])
    return base._r10_optimize(paths, seed, restarts, iterations, warm)


def mine_templates(census, residuals, pack_path, output):
    try:
        raw = lzma.decompress(pack_path.read_bytes(), format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError("template source pack is not a valid XZ stream") from error
    start, records = base.exact_decode_pack(census, raw, residuals)
    groups = Counter(template_key(census, source)
                     for source in residuals[start:start + len(records)])
    payload = {
        "schema": "rank-seven-order-eight-template-mining-v1",
        "source_sha256": census.SOURCE_SHA256,
        "pack_sha256": hashlib.sha256(pack_path.read_bytes()).hexdigest(),
        "range": [start, start + len(records)],
        "rows": len(records),
        "unique_templates": len(groups),
        "reused_rows": sum(count for count in groups.values() if count > 1),
        "maximum_reuse": max(groups.values(), default=0),
        "multiplicity_histogram": {str(reuse): count for reuse, count in
                                   sorted(Counter(groups.values()).items())},
    }
    raw_output = (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    output.write_bytes(raw_output)
    return payload


def expand_shard_arguments(arguments):
    options = {name: arguments.index(name) for name in
               ("--shard-index", "--shard-count", "--shard-rows") if name in arguments}
    if not options:
        return arguments
    require(set(options) == {"--shard-index", "--shard-count", "--shard-rows"},
            "sharding requires --shard-index, --shard-count, and --shard-rows")
    values = {}
    result = list(arguments)
    for name in options:
        position = result.index(name)
        require(position + 1 < len(result), f"missing value for {name}")
        values[name] = int(result[position + 1])
        del result[position:position + 2]
    index, count, rows = (values["--shard-index"], values["--shard-count"],
                          values["--shard-rows"])
    require(0 <= index < count and count > 0 and rows > 0, "invalid shard specification")
    require(count == (EXPECTED_RESIDUALS + rows - 1) // rows,
            "shard count does not exactly cover the residual stream")
    start = index * rows
    stop = min(EXPECTED_RESIDUALS, start + rows)
    require(start < stop, "shard starts beyond the residual stream")
    require("--start" not in result and "--count" not in result,
            "do not combine shard selection with --start or --count")
    return result + ["--start", str(start), "--count", str(stop - start)]


def fragment_path(directory, start, stop):
    return directory / f"fragment-{start:06d}-{stop:06d}.r7o8g.xz"


def search(args, census, residuals):
    base._summary_start = args.start
    result = base._r10_search(args, census, residuals)
    if _WARM_GRAMS is not None:
        print(f"warm_cache_signatures={len(_WARM_GRAMS)} warm_start_hits={_WARM_HITS}")
    return result


def configure_base():
    base._r10_search = base.search
    base._r10_optimize = base.optimize
    base._r10_objective = base.objective
    base._r10_objective_gradient = base.objective_gradient
    values = {
        "MAGIC": MAGIC,
        "ORDER": ORDER,
        "DIMENSION": DIMENSION,
        "PATH_COUNT": PATH_COUNT,
        "BUDGET": BUDGET,
        "FRAGMENT_PATTERN": FRAGMENT_PATTERN,
        "load_census_module": load_census_module,
        "residual_rows": residual_rows,
        "atom_source_indices": atom_source_indices,
        "verify_atom": verify_atom,
        "structural_certified": structural_certified,
        "objective_gradient": objective_gradient,
        "objective": objective,
        "optimize": optimize,
        "fragment_path": fragment_path,
        "search": search,
    }
    for name, value in values.items():
        setattr(base, name, value)


configure_base()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build-warm-cache":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--source-pack", type=Path, default=DEFAULT_WARM_SOURCE)
        parser.add_argument("--output", type=Path, required=True)
        parser.add_argument("--census-cache", type=Path)
        cache_args = parser.parse_args(sys.argv[2:])
        require(cache_args.output.parent.is_dir(), "warm-cache output parent missing")
        cache_census = load_census_module()
        cache_residuals = residual_rows(cache_census, cache_path=cache_args.census_cache)
        cache_payload = write_warm_cache(cache_census, cache_residuals,
                                         cache_args.source_pack, cache_args.output)
        print(f"representatives={cache_payload['representative_total']} "
              f"source_rows={cache_payload['source_range'][1] - cache_payload['source_range'][0]}")
        raise SystemExit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "mine-templates":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("pack", type=Path)
        parser.add_argument("--output", type=Path, required=True)
        mining_args = parser.parse_args(sys.argv[2:])
        require(mining_args.output.parent.is_dir(), "template output parent missing")
        mining_census = load_census_module()
        mining_residuals = residual_rows(mining_census)
        mining = mine_templates(mining_census, mining_residuals, mining_args.pack,
                                mining_args.output)
        print(f"rows={mining['rows']} unique_templates={mining['unique_templates']} "
              f"reused_rows={mining['reused_rows']} maximum_reuse={mining['maximum_reuse']}")
        print("full_theorem=false")
        raise SystemExit(0)
    warm_path = None
    if "--warm-start-cache" in sys.argv[1:]:
        position = sys.argv.index("--warm-start-cache")
        require(position + 1 < len(sys.argv), "missing value for --warm-start-cache")
        warm_path = Path(sys.argv[position + 1])
        del sys.argv[position:position + 2]
    sys.argv[1:] = expand_shard_arguments(sys.argv[1:])
    if warm_path is not None:
        require(warm_path.is_file(), "warm-start cache missing")
        _WARM_GRAMS = load_warm_cache(load_census_module(), warm_path)
    base.main()
    print("full_theorem=false")
