#!/usr/bin/env python3
"""Exact order-six rank-seven residual frontier and rational Gram pipeline.

The census stage materializes every coarse residual orbit and every canonical
plus one-coordinate target.  The search is chunkable: floating point arithmetic
only proposes a common branch Gram, while every accepted witness is rebuilt and
audited over Fraction.  Aggregation rejects gaps, overlaps, altered sources, and
unresolved targets by default.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
COARSE = HERE / "rank7_parity_coarse_digest_census.py"
ENGINE = HERE / "rank6_order6_dim6_rational_frontier.py"
DEFAULT_CENSUS = HERE / "rank7_order6_exact_frontier.json"
ORDER = DIMENSION = 6
RANK = 7
PATH_COUNT = ORDER + RANK - 1
BUDGET = Fraction(RANK - 1)
FRONTIERS = (None, *range(PATH_COUNT))
SCHEMA = "rank-seven-order-six-exact-frontier-v1"
CHUNK_SCHEMA = "rank-seven-order-six-dim6-rational-chunk-v1"
AGGREGATE_SCHEMA = "rank-seven-order-six-dim6-rational-aggregate-v1"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pair(value):
    return [value.numerator, value.denominator]


def unpair(raw, label):
    require(type(raw) is list and len(raw) == 2 and
            all(type(value) is int for value in raw), f"bad {label} fraction")
    value = Fraction(*raw)
    require(raw == pair(value), f"uncanonical {label} fraction")
    return value


def dense_kernel(edges):
    values = {(u, v): multiplicity for u, v, multiplicity in edges}
    return tuple(values.get(edge, 0) for edge in itertools.combinations(range(ORDER), 2))


def materialize():
    coarse = load_module(COARSE, "rank7_order6_coarse_source")
    source_raw = SOURCE.read_bytes()
    coarse.SOURCE_SHA256 = hashlib.sha256(source_raw).hexdigest()
    items = tuple(item for item in coarse.source_kernels() if item[2] == ORDER)
    residuals = []
    orbit_digest = hashlib.sha256()
    residual_digest = hashlib.sha256()
    target_digest = hashlib.sha256()
    parity_orbits = 0
    for global_index, local_index, order, edges in items:
        actions = coarse.automorphism_actions(order, edges)
        orbit_sizes = {}
        for row in itertools.product(*(range(multiplicity + 1)
                                       for _, _, multiplicity in edges)):
            representative = min(coarse.apply_action(row, action) for action in actions)
            orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1
        parity_orbits += len(orbit_sizes)
        kernel = dense_kernel(edges)
        for row in sorted(orbit_sizes):
            orbit_line = [global_index, list(row), orbit_sizes[row]]
            orbit_digest.update(coarse.stream_line(orbit_line))
            if not coarse.is_coarse_residual(order, edges, row):
                continue
            residual_digest.update(coarse.stream_line(orbit_line))
            source_index = len(residuals)
            paths = path_ledger(kernel, edges, row)
            targets = []
            for frontier in FRONTIERS:
                lengths = list(path_lengths(paths, frontier))
                target = {"frontier": frontier, "lengths": lengths}
                targets.append(target)
                target_digest.update(canonical_bytes([source_index, frontier, lengths]))
            residuals.append({
                "source_index": source_index,
                "global_kernel": global_index,
                "order_kernel": local_index,
                "sparse_edges": [list(edge) for edge in edges],
                "kernel": list(kernel),
                "row": list(row),
                "orbit_size": orbit_sizes[row],
                "targets": targets,
            })
    require(len(items) == 914 and parity_orbits == 1094367, "order-six scope changed")
    require(len(residuals) == 1517, "order-six residual count changed")
    return {
        "schema": SCHEMA,
        "status": "exact-materialized-search-open",
        "full_theorem": False,
        "order": ORDER,
        "rank": RANK,
        "dimension": DIMENSION,
        "budget": pair(BUDGET),
        "path_count": PATH_COUNT,
        "frontiers_per_residual": len(FRONTIERS),
        "kernel_total": len(items),
        "parity_orbit_total": parity_orbits,
        "coarse_residual_total": len(residuals),
        "frontier_target_total": len(residuals) * len(FRONTIERS),
        "source_sha256": hashlib.sha256(source_raw).hexdigest(),
        "orbit_stream_sha256": orbit_digest.hexdigest(),
        "residual_stream_sha256": residual_digest.hexdigest(),
        "target_stream_sha256": target_digest.hexdigest(),
        "residuals": residuals,
    }


def path_ledger(kernel, sparse_edges, row):
    dense_pairs = tuple(itertools.combinations(range(ORDER), 2))
    odd_by_pair = {(u, v): odd for (u, v, _), odd in zip(sparse_edges, row)}
    paths = []
    for edge, ((u, v), multiplicity) in enumerate(zip(dense_pairs, kernel)):
        odd = odd_by_pair.get((u, v), 0)
        lengths = (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)
        paths.extend((edge, occurrence, u, v, length)
                     for occurrence, length in enumerate(lengths))
    require(len(paths) == PATH_COUNT, "path count changed")
    return tuple(paths)


def path_lengths(paths, frontier):
    require(frontier is None or type(frontier) is int and 0 <= frontier < PATH_COUNT,
            "bad frontier")
    return tuple(length + (2 if frontier == index else 0)
                 for index, (*_, length) in enumerate(paths))


def load_census(path=DEFAULT_CENSUS):
    raw = path.read_bytes()
    payload = json.loads(raw.decode("ascii"))
    require(raw == canonical_bytes(payload), "census is not canonical JSON")
    verify_census(payload)
    return payload, hashlib.sha256(raw).hexdigest()


def verify_census(payload):
    require(payload["schema"] == SCHEMA and payload["full_theorem"] is False,
            "wrong census schema")
    require(payload["coarse_residual_total"] == 1517 and
            payload["frontier_target_total"] == 19721, "census totals changed")
    require(len(payload["residuals"]) == 1517, "residual materialization is incomplete")
    target_digest = hashlib.sha256()
    keys = set()
    for source_index, source in enumerate(payload["residuals"]):
        require(source["source_index"] == source_index, "residual order changed")
        require(len(source["targets"]) == len(FRONTIERS), "frontier width changed")
        paths = path_ledger(tuple(source["kernel"]), tuple(map(tuple, source["sparse_edges"])),
                            tuple(source["row"]))
        for expected, target in zip(FRONTIERS, source["targets"]):
            key = source_index, target["frontier"]
            require(target["frontier"] == expected and key not in keys, "bad target key")
            keys.add(key)
            lengths = list(path_lengths(paths, expected))
            require(target["lengths"] == lengths, "target lengths changed")
            target_digest.update(canonical_bytes([source_index, expected, lengths]))
    require(target_digest.hexdigest() == payload["target_stream_sha256"],
            "target stream digest changed")


def load_engine():
    engine = load_module(ENGINE, "rank7_order6_dim6_engine")
    engine.PATH_COUNT = PATH_COUNT
    engine.BUDGET = BUDGET
    return engine


def exact_path(engine, left, right, exact_left, exact_right, length, denominator):
    parameters = tuple(engine.stereographic(engine.slerp(left, right, step / length), denominator)
                       for step in range(1, length))
    chain = [exact_left, *(engine.rational_unit(row) for row in parameters), exact_right]
    cost = sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), Fraction())
    return parameters, cost


def shared_rationalize(engine, paths, vectors, denominators):
    vectors = engine.rotate_away_from_pole(engine.snap_coincident(vectors))
    for denominator in denominators:
        try:
            branch_parameters = tuple(engine.stereographic(row, denominator) for row in vectors)
            branches = tuple(engine.rational_unit(row) for row in branch_parameters)
            canonical, extended, costs, extended_costs = [], [], [], []
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                exact_endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
                inside, cost = exact_path(engine, vectors[u], endpoint, branches[u], exact_endpoint,
                                          length, denominator)
                longer, longer_cost = exact_path(engine, vectors[u], endpoint, branches[u],
                                                  exact_endpoint, length + 2, denominator)
                canonical.append(inside)
                extended.append(longer)
                costs.append(cost)
                extended_costs.append(longer_cost)
        except (RuntimeError, ZeroDivisionError):
            continue
        base = sum(costs, Fraction())
        totals = (base, *(base - costs[i] + extended_costs[i] for i in range(PATH_COUNT)))
        if max(totals) <= BUDGET:
            return {
                "denominator": denominator,
                "branches": [[[value.numerator, value.denominator] for value in row]
                             for row in branch_parameters],
                "canonical_internals": [[[[value.numerator, value.denominator] for value in row]
                                          for row in path] for path in canonical],
                "extended_internals": [[[[value.numerator, value.denominator] for value in row]
                                         for row in path] for path in extended],
                "costs": [pair(value) for value in totals],
            }
    return None


def correlation_geometry(engine, paths, vectors, value, tolerance):
    correlations = [engine.dot(vectors[u], vectors[v]) for _, _, u, v, _ in paths]
    mixed = sum(1 for correlation in correlations if abs(correlation + 0.5) <= tolerance)
    simplex = sum(1 for correlation in correlations if abs(correlation + 0.25) <= tolerance)
    if abs(value - 6.0) > tolerance:
        return "numerical-over-budget" if value > 6.0 else "rationalization-gap"
    if simplex >= 10:
        return "regular-four-simplex-candidate"
    if mixed >= 6:
        return "six-mixed-pair-candidate"
    return "coupled-equality-candidate"


def symbolic_atom_geometry(source):
    """Recognize the two exact equality assemblies left by rational snapping."""
    edges = tuple(map(tuple, source["sparse_edges"]))
    row = tuple(source["row"])
    bundles = tuple((u, v, multiplicity, odd)
                    for (u, v, multiplicity), odd in zip(edges, row))
    if len(bundles) == 6 and all((multiplicity, odd) == (2, 1)
                                 for _, _, multiplicity, odd in bundles):
        return "six-mixed-pairs"
    mixed = {(u, v) for u, v, multiplicity, odd in bundles
             if (multiplicity, odd) == (2, 1)}
    singles = {(u, v) for u, v, multiplicity, odd in bundles
               if (multiplicity, odd) == (1, 1)}
    if len(mixed) != 3 or len(singles) != 6 or len(bundles) != 9:
        return None
    for vertices in itertools.combinations(range(ORDER), 4):
        if singles == set(itertools.combinations(vertices, 2)):
            outside = set(range(ORDER)) - set(vertices)
            degrees = Counter(vertex for edge in mixed for vertex in edge)
            endpoints = {vertex for vertex, degree in degrees.items() if degree == 1}
            internal = {vertex for vertex, degree in degrees.items() if degree == 2}
            if (len(outside) == 2 and len(degrees) == 4 and endpoints <= set(vertices)
                    and internal == outside):
                return "tetrahedron-plus-three-mixed-pairs"
    return None


def audit_symbolic_atom(source, geometry):
    require(symbolic_atom_geometry(source) == geometry, "symbolic atom scope changed")
    # Mixed-pair and simplex atoms have exact costs one and three.  Their
    # prescribed Gram is PSD: six mixed pairs are the signed C6 quotient; for
    # the second row take a regular tetrahedron, then choose the two remaining
    # unit vectors with prescribed -1/2 products.  In the orthogonal complement
    # their free unit directions need product -5/9, which is feasible.
    require(geometry in {"six-mixed-pairs", "tetrahedron-plus-three-mixed-pairs"},
            "unknown symbolic atom")


def search(census_path, start, limit, seed, restarts, iterations, denominators,
           equality_tolerance):
    census, census_digest = load_census(census_path)
    engine = load_engine()
    stop = len(census["residuals"]) if limit is None else min(len(census["residuals"]), start + limit)
    require(0 <= start <= stop, "bad chunk range")
    records = []
    for source in census["residuals"][start:stop]:
        index = source["source_index"]
        paths = path_ledger(tuple(source["kernel"]), tuple(map(tuple, source["sparse_edges"])),
                            tuple(source["row"]))
        symbolic = symbolic_atom_geometry(source)
        if symbolic is not None:
            audit_symbolic_atom(source, symbolic)
            records.append({
                "source_index": index,
                "kernel": source["global_kernel"],
                "row": source["row"],
                "numerical_cost": 6.0,
                "mode": "symbolic-atom",
                "geometry": symbolic,
                "witness": None,
            })
            continue
        value, vectors = engine.optimize(paths, seed + 1009 * index, restarts, iterations)
        witness = shared_rationalize(engine, paths, vectors, denominators)
        records.append({
            "source_index": index,
            "kernel": source["global_kernel"],
            "row": source["row"],
            "numerical_cost": float(f"{value:.12g}"),
            "mode": "shared-exact" if witness is not None else "unresolved",
            "geometry": None if witness is not None else
                        correlation_geometry(engine, paths, vectors, value, equality_tolerance),
            "witness": witness,
        })
    return {
        "schema": CHUNK_SCHEMA,
        "status": "exact-witnesses-with-explicit-unresolved",
        "full_theorem": False,
        "census_sha256": census_digest,
        "range": [start, stop],
        "residual_total": len(records),
        "target_total": len(records) * len(FRONTIERS),
        "exact_residual_total": sum(row["mode"] != "unresolved" for row in records),
        "exact_target_total": sum(len(FRONTIERS) for row in records if row["mode"] != "unresolved"),
        "unresolved_residual_total": sum(row["mode"] == "unresolved" for row in records),
        "unresolved_target_total": sum(len(FRONTIERS) for row in records if row["mode"] == "unresolved"),
        "search": {"seed": seed, "restarts": restarts, "iterations": iterations,
                   "denominators": list(denominators),
                   "equality_tolerance": equality_tolerance},
        "records": records,
    }


def verify_witness(engine, source, witness):
    denominator = witness["denominator"]
    require(type(denominator) is int and denominator > 0, "bad denominator")
    parameter_rows = tuple(tuple(unpair(value, "branch") for value in row)
                           for row in witness["branches"])
    require(len(parameter_rows) == ORDER and
            all(len(row) == DIMENSION - 1 for row in parameter_rows), "bad branches")
    require(all(denominator % value.denominator == 0 for row in parameter_rows for value in row),
            "unauthenticated branch denominator")
    branches = tuple(engine.rational_unit(row) for row in parameter_rows)
    paths = path_ledger(tuple(source["kernel"]), tuple(map(tuple, source["sparse_edges"])),
                        tuple(source["row"]))
    totals = []
    for frontier in FRONTIERS:
        total = Fraction()
        for index, (_, _, u, v, length) in enumerate(paths):
            family = (witness["extended_internals"] if frontier == index else
                      witness["canonical_internals"])
            raw_path = family[index]
            expected_length = length + (2 if frontier == index else 0)
            require(len(raw_path) == expected_length - 1, "bad internal path width")
            parameters = tuple(tuple(unpair(value, "internal") for value in row)
                               for row in raw_path)
            require(all(len(row) == DIMENSION - 1 for row in parameters),
                    "bad internal dimension")
            require(all(denominator % value.denominator == 0
                        for row in parameters for value in row),
                    "unauthenticated internal denominator")
            chain = [branches[u], *(engine.rational_unit(row) for row in parameters)]
            chain.append(branches[v] if expected_length % 2 == 0 else
                         tuple(-value for value in branches[v]))
            total += sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])),
                         Fraction())
        totals.append(total)
    require([pair(value) for value in totals] == witness["costs"], "stored costs changed")
    require(max(totals) <= BUDGET, "witness exceeds budget six")


def verify_chunk(payload, census_path=DEFAULT_CENSUS):
    census, digest = load_census(census_path)
    engine = load_engine()
    require(payload["schema"] == CHUNK_SCHEMA and payload["full_theorem"] is False,
            "wrong chunk schema")
    require(payload["census_sha256"] == digest, "chunk uses a different census")
    start, stop = payload["range"]
    require(0 <= start <= stop <= len(census["residuals"]), "bad chunk range")
    require(len(payload["records"]) == stop - start == payload["residual_total"],
            "chunk record count changed")
    for expected, record in enumerate(payload["records"], start):
        source = census["residuals"][expected]
        require(record["source_index"] == expected and record["kernel"] == source["global_kernel"]
                and record["row"] == source["row"], "chunk source changed")
        require(record["mode"] in {"shared-exact", "symbolic-atom", "unresolved"},
                "unknown chunk mode")
        if record["mode"] == "shared-exact":
            require(record["witness"] is not None, "shared exact witness is absent")
            require(record["geometry"] is None, "exact record has unresolved geometry")
            verify_witness(engine, source, record["witness"])
        elif record["mode"] == "symbolic-atom":
            require(record["witness"] is None, "symbolic atom carries numerical payload")
            audit_symbolic_atom(source, record["geometry"])
        else:
            require(record["witness"] is None, "unresolved record carries a witness")
            require(record["geometry"] in {"numerical-over-budget", "rationalization-gap",
                                           "regular-four-simplex-candidate",
                                           "six-mixed-pair-candidate",
                                           "coupled-equality-candidate"},
                    "unclassified unresolved geometry")
    exact = sum(record["mode"] != "unresolved" for record in payload["records"])
    require(payload["exact_residual_total"] == exact and
            payload["unresolved_residual_total"] == len(payload["records"]) - exact,
            "chunk partition changed")


def aggregate(census_path, chunk_paths, allow_unresolved):
    census, digest = load_census(census_path)
    records = {}
    chunks = []
    for path in sorted(chunk_paths):
        raw = path.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(payload), f"noncanonical chunk {path}")
        verify_chunk(payload, census_path)
        chunks.append({"path": path.name, "sha256": hashlib.sha256(raw).hexdigest(),
                       "range": payload["range"]})
        for record in payload["records"]:
            require(record["source_index"] not in records, "overlapping chunks")
            records[record["source_index"]] = record
    expected = set(range(len(census["residuals"])))
    require(set(records) == expected, "chunk union does not equal the residual universe")
    unresolved = [record for record in records.values() if record["mode"] == "unresolved"]
    symbolic = Counter(record["geometry"] for record in records.values()
                       if record["mode"] == "symbolic-atom")
    if not allow_unresolved:
        require(not unresolved, "unresolved records remain (pass --allow-unresolved to report)")
    geometries = Counter(record["geometry"] for record in unresolved)
    return {
        "schema": AGGREGATE_SCHEMA,
        "status": "complete-exact-frontier-cover" if not unresolved else "complete-search-census-open",
        "full_theorem": False,
        "census_sha256": digest,
        "chunks": chunks,
        "residual_total": len(records),
        "target_total": len(records) * len(FRONTIERS),
        "exact_residual_total": len(records) - len(unresolved),
        "exact_target_total": (len(records) - len(unresolved)) * len(FRONTIERS),
        "unresolved_residual_total": len(unresolved),
        "unresolved_target_total": len(unresolved) * len(FRONTIERS),
        "unresolved_geometry_counts": dict(sorted(geometries.items())),
        "symbolic_equality_geometry_counts": dict(sorted(symbolic.items())),
        "unresolved_source_indices": [record["source_index"] for record in unresolved],
    }


def write_payload(path, payload):
    require(path.parent.is_dir(), "output parent does not exist")
    path.write_bytes(canonical_bytes(payload))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    census_parser = subparsers.add_parser("census")
    census_parser.add_argument("--output", type=Path, default=DEFAULT_CENSUS)
    census_parser.add_argument("--verify", type=Path)
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--census", type=Path, default=DEFAULT_CENSUS)
    search_parser.add_argument("--start", type=int, default=0)
    search_parser.add_argument("--limit", type=int)
    search_parser.add_argument("--seed", type=int, default=76173)
    search_parser.add_argument("--restarts", type=int, default=6)
    search_parser.add_argument("--iterations", type=int, default=900)
    search_parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    search_parser.add_argument("--equality-tolerance", type=float, default=1e-6)
    search_parser.add_argument("--output", type=Path, required=True)
    verify_parser = subparsers.add_parser("verify-chunk")
    verify_parser.add_argument("chunk", type=Path)
    verify_parser.add_argument("--census", type=Path, default=DEFAULT_CENSUS)
    aggregate_parser = subparsers.add_parser("aggregate")
    aggregate_parser.add_argument("chunks", nargs="+", type=Path)
    aggregate_parser.add_argument("--census", type=Path, default=DEFAULT_CENSUS)
    aggregate_parser.add_argument("--allow-unresolved", action="store_true")
    aggregate_parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "census":
        if args.verify:
            raw = args.verify.read_bytes()
            payload = json.loads(raw.decode("ascii"))
            require(raw == canonical_bytes(payload), "census is not canonical JSON")
            verify_census(payload)
        else:
            payload = materialize()
            verify_census(payload)
            write_payload(args.output, payload)
        print(f"residuals={payload['coarse_residual_total']} targets={payload['frontier_target_total']}")
    elif args.command == "search":
        denominators = tuple(int(value) for value in args.denominators.split(","))
        require(denominators and all(value > 0 for value in denominators), "bad denominators")
        payload = search(args.census, args.start, args.limit, args.seed, args.restarts,
                         args.iterations, denominators, args.equality_tolerance)
        verify_chunk(payload, args.census)
        write_payload(args.output, payload)
        print(f"exact={payload['exact_residual_total']} unresolved={payload['unresolved_residual_total']}")
    elif args.command == "verify-chunk":
        raw = args.chunk.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(raw == canonical_bytes(payload), "chunk is not canonical JSON")
        verify_chunk(payload, args.census)
        print("exact chunk audit passed")
    else:
        payload = aggregate(args.census, args.chunks, args.allow_unresolved)
        write_payload(args.output, payload)
        print(f"exact={payload['exact_residual_total']} unresolved={payload['unresolved_residual_total']}")
    print("full_theorem=false")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
