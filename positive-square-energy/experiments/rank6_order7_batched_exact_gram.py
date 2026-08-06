#!/usr/bin/env python3
"""Parallel, compact exact rational Gram certificates for the 319202 frontier.

One branch Gram realization is tested against the canonical path ledger and all
twelve one-coordinate lengthenings.  Shared branch parameters and unchanged
path interiors are stored once.  A slower per-frontier fallback preserves exact
coverage when the shared realization does not close every target.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import math
import multiprocessing
import os
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ENGINE_PATH = HERE / "rank6_order7_dim7_rational_frontier.py"
OUTPUT_DIR = HERE / "rank6_order7_batched_chunks"
SCHEMA = "rank-six-order-seven-batched-exact-gram-v1"
FRONTIERS = (None, *range(12))
BUDGET = Fraction(5)
CHUNKS = (
    ("chunk-00000-04000.json.xz", "7973e5e36baf73814b542301cd2da4674bf1bc66bc4cacd796dfcf18c05415e8", "3731079c31db0dd8613836ca69e4e21bcd6533f876964492d38d4d773ec7ecf0"),
    ("chunk-04000-08000.json.xz", "7af9efd2a8fe37e787540ad25dcab19ecea2f0a1b917b860eb1d0dc3401f493e", "4f1746f60bb1d6e32daf77371f0790d0f711e3c98c79dc04f079f094aee7a75c"),
    ("chunk-08000-12000.json.xz", "c66e94e4443bff1aa67d6576c42a8338703e1d1d23d1b70d25d23e4cc056da8d", "0d9425d33fe780d305ab3c0ff22873285861b4196157cbd080c843f6dd8d02a3"),
    ("chunk-12000-16000.json.xz", "1ea2e870017d62c8b53a00d9264182aca0a2081c85396f629abc5777d033a51a", "e4b1a2cc5e235a3eed356090703525a986548af2ba26c2f62a1d972269f955bd"),
    ("chunk-16000-20000.json.xz", "714efdc1d5a4105c4034e587b8dabcce235323987f69590edd90d88d9e91160c", "b2e8d70e14ac7fb8f8430c6af7c949e1cb7a0c6a11c3f18f44c8813257a059d4"),
    ("chunk-20000-24554.json.xz", "c15c4488106b036f2a846df4df3bd2804785e2054670323cd711470990019469", "491afa09d32f772e74bafc8b498544b3894411cdd74097b7229830602f03c318"),
)
MANIFEST_SHA256 = "5a3693a15beb0a6c37089c5fe15f78eaf76875dcd3096b98a2fc3dbf0f339324"
ARTIFACT_MANIFEST_SHA256 = "836ce3a25de9a3f3dd2f83bc5cdfe340b022bc72a73bf7a169a4d7cdd872cca7"
PAYLOAD_FIELDS = {
    "schema", "status", "full_theorem", "source_census_sha256", "source_residual_total",
    "source_frontier_total", "selected_residual_start", "record_total", "target_total",
    "exact_target_total", "unresolved_target_total", "elapsed_seconds", "workers", "search",
    "records",
}
RECORD_FIELDS = {
    "source_index", "kernel", "row", "canonical_lengths", "numerical_costs",
    "shared_witness", "individual_witnesses", "exact_target_total",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_engine():
    spec = importlib.util.spec_from_file_location("rank6_order7_batched_engine", ENGINE_PATH)
    require(spec is not None and spec.loader is not None, "cannot load frontier engine")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant: {value}")


def load_json(raw):
    return json.loads(raw.decode("ascii"), parse_constant=reject_constant)


def artifact_bytes(path, compressed_digest=None):
    stored = path.read_bytes()
    if path.suffix == ".xz":
        if compressed_digest is not None:
            require(hashlib.sha256(stored).hexdigest() == compressed_digest,
                    f"compressed artifact digest changed: {path.name}")
        try:
            return lzma.decompress(stored, format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"invalid xz artifact: {path.name}") from error
    require(compressed_digest is None, f"expected compressed artifact: {path.name}")
    return stored


def pair(value):
    return [value.numerator, value.denominator]


def exact_path(engine, left, right, exact_left, exact_right, length, denominator):
    parameters = tuple(engine.stereographic(
        engine.slerp(left, right, step / length), denominator)
        for step in range(1, length))
    chain = [exact_left]
    chain.extend(engine.rational_unit(row) for row in parameters)
    chain.append(exact_right)
    cost = sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), Fraction())
    return parameters, cost


def shared_rationalize(engine, paths, vectors, denominators):
    vectors = engine.rotate_away_from_pole(engine.snap_coincident(vectors))
    for denominator in denominators:
        try:
            branch_parameters = tuple(engine.stereographic(row, denominator) for row in vectors)
            branches = tuple(engine.rational_unit(row) for row in branch_parameters)
            canonical, extended = [], []
            base_costs, extended_costs = [], []
            for _, _, u, v, length in paths:
                endpoint = vectors[v] if length % 2 == 0 else tuple(-x for x in vectors[v])
                exact_endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
                parameters, cost = exact_path(
                    engine, vectors[u], endpoint, branches[u], exact_endpoint, length, denominator)
                longer_parameters, longer_cost = exact_path(
                    engine, vectors[u], endpoint, branches[u], exact_endpoint,
                    length + 2, denominator)
                canonical.append(parameters)
                extended.append(longer_parameters)
                base_costs.append(cost)
                extended_costs.append(longer_cost)
        except (RuntimeError, ZeroDivisionError):
            continue
        base = sum(base_costs, Fraction())
        costs = [base] + [base - base_costs[index] + extended_costs[index]
                          for index in range(len(paths))]
        if all(cost <= BUDGET for cost in costs):
            return {
                "denominator": denominator,
                "costs": [pair(cost) for cost in costs],
                "branches": [[pair(value) for value in row] for row in branch_parameters],
                "canonical_internals": [
                    [[pair(value) for value in row] for row in path] for path in canonical],
                "extended_internals": [
                    [[pair(value) for value in row] for row in path] for path in extended],
            }
    return None


WORKER = {}


def initialize_worker(denominators, seed, restarts, iterations, fallback_restarts,
                      fallback_iterations):
    frontier = load_engine()
    engine = frontier.load_engine()
    census = frontier.load_census()
    WORKER.update({
        "engine": engine,
        "frontier": frontier,
        "residuals": census["residuals"],
        "kernels": {row["kernel"]: tuple(row["code"]) for row in census["kernels"]},
        "denominators": denominators,
        "seed": seed,
        "restarts": restarts,
        "iterations": iterations,
        "fallback_restarts": fallback_restarts,
        "fallback_iterations": fallback_iterations,
    })


def generate_record(source_index):
    engine = WORKER["engine"]
    frontier_engine = WORKER["frontier"]
    source = WORKER["residuals"][source_index]
    kernel = WORKER["kernels"][source["kernel"]]
    row = tuple(source["row"])
    paths = engine.path_ledger(kernel, row)
    tetra = frontier_engine.tetrahedral_start(kernel, row)
    canonical_value, vectors = engine.optimize(
        paths, WORKER["seed"] + 1009 * source_index, WORKER["restarts"],
        WORKER["iterations"], warm=(tetra,))
    numerical = [canonical_value]
    numerical.extend(engine.objective(engine.path_ledger(kernel, row, frontier), vectors)
                     for frontier in range(12))
    shared = shared_rationalize(engine, paths, vectors, WORKER["denominators"])
    individual = [None] * 13
    if shared is None:
        for position, frontier in enumerate(FRONTIERS):
            frontier_paths = paths if frontier is None else engine.path_ledger(kernel, row, frontier)
            value, candidate = numerical[position], vectors
            witness = engine.rationalize(frontier_paths, candidate, WORKER["denominators"])
            if witness is None:
                value, candidate = engine.optimize(
                    frontier_paths, WORKER["seed"] + 1009 * source_index + position,
                    WORKER["fallback_restarts"], WORKER["fallback_iterations"], warm=(vectors,))
                witness = engine.rationalize(frontier_paths, candidate, WORKER["denominators"])
            numerical[position] = value
            individual[position] = witness
    return {
        "source_index": source_index,
        "kernel": source["kernel"],
        "row": source["row"],
        "canonical_lengths": [path[4] for path in paths],
        "numerical_costs": [float(f"{value:.12g}") for value in numerical],
        "shared_witness": shared,
        "individual_witnesses": individual if shared is None else None,
        "exact_target_total": 13 if shared is not None else sum(x is not None for x in individual),
    }


def fraction(raw, label):
    require(type(raw) is list and len(raw) == 2 and all(type(x) is int for x in raw),
            f"bad {label} fraction")
    value = Fraction(*raw)
    require(raw == pair(value), f"uncanonical {label} fraction")
    return value


def audit_witness(engine, paths, witness, frontier):
    require(type(witness) is dict, "bad witness envelope")
    shared = "canonical_internals" in witness
    expected = ({"denominator", "costs", "branches", "canonical_internals",
                 "extended_internals"} if shared else
                {"denominator", "cost", "branches", "internals"})
    require(set(witness) == expected, "witness envelope changed")
    denominator = witness["denominator"]
    require(type(denominator) is int and denominator > 0, "bad witness denominator")

    def parameter(raw, label):
        value = fraction(raw, label)
        require(denominator % value.denominator == 0,
                f"{label} denominator is not authenticated by witness denominator")
        return value

    branches = tuple(engine.rational_unit(tuple(parameter(x, "branch") for x in row))
                     for row in witness["branches"])
    if shared:
        raw_paths = list(witness["canonical_internals"])
        if frontier is not None:
            raw_paths[frontier] = witness["extended_internals"][frontier]
        claimed = witness["costs"][0 if frontier is None else frontier + 1]
    else:
        raw_paths = witness["internals"]
        claimed = witness["cost"]
    require(len(branches) == 7 and all(len(row) == 7 for row in branches),
            "branch dimensions changed")
    require(len(raw_paths) == len(paths), "internal path count changed")
    total = Fraction()
    for (_, _, u, v, length), raw_path in zip(paths, raw_paths):
        require(len(raw_path) == length - 1, "internal path width changed")
        parameters = tuple(tuple(parameter(x, "internal") for x in row) for row in raw_path)
        require(all(len(row) == 6 for row in parameters), "internal dimension changed")
        chain = [branches[u], *(engine.rational_unit(row) for row in parameters)]
        chain.append(branches[v] if length % 2 == 0 else tuple(-x for x in branches[v]))
        total += sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])), Fraction())
    require(total == fraction(claimed, "cost") and total <= BUDGET, "exact cost changed")


def verify(payload):
    frontier_engine = load_engine()
    engine = frontier_engine.load_engine()
    census = frontier_engine.load_census()
    kernels = {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}
    require(type(payload) is dict and set(payload) == PAYLOAD_FIELDS, "chunk envelope changed")
    require(payload["schema"] == SCHEMA and payload["full_theorem"] is False, "schema changed")
    require(payload["source_census_sha256"] == frontier_engine.EXPECTED_CENSUS_SHA256,
            "wrong census")
    residual_total = len(census["residuals"])
    frontier_total = residual_total * len(FRONTIERS)
    require(census["frontier_target_total"] == frontier_total, "authenticated census is inconsistent")
    require(payload["source_residual_total"] == residual_total and
            payload["source_frontier_total"] == frontier_total, "source totals changed")
    require(type(payload["elapsed_seconds"]) in (int, float) and
            math.isfinite(payload["elapsed_seconds"]) and payload["elapsed_seconds"] >= 0,
            "bad elapsed time")
    require(type(payload["records"]) is list and
            payload["record_total"] == len(payload["records"]), "record total changed")
    require(payload["target_total"] == 13 * len(payload["records"]), "target total changed")
    start = payload["selected_residual_start"]
    require(type(start) is int and 0 <= start <= len(census["residuals"]), "bad chunk start")
    exact = 0
    seen = set()
    for record in payload["records"]:
        require(type(record) is dict and set(record) == RECORD_FIELDS, "record envelope changed")
        index = record["source_index"]
        require(type(index) is int and 0 <= index < len(census["residuals"]) and index not in seen,
                "duplicate or invalid source index")
        seen.add(index)
        source = census["residuals"][index]
        require((record["kernel"], record["row"]) == (source["kernel"], source["row"]),
                "source changed")
        kernel = kernels[record["kernel"]]
        canonical = engine.path_ledger(kernel, tuple(record["row"]))
        require(record["canonical_lengths"] == [path[4] for path in canonical], "lengths changed")
        require(type(record["numerical_costs"]) is list and
                len(record["numerical_costs"]) == len(FRONTIERS) and
                all(type(value) in (int, float) and math.isfinite(value)
                    for value in record["numerical_costs"]), "bad numerical-cost envelope")
        shared = record["shared_witness"]
        if shared is not None:
            require(record["individual_witnesses"] is None, "mixed witness modes")
            for frontier in FRONTIERS:
                paths = canonical if frontier is None else engine.path_ledger(
                    kernel, tuple(record["row"]), frontier)
                audit_witness(engine, paths, shared, frontier)
            local_exact = 13
        else:
            require(len(record["individual_witnesses"]) == 13, "fallback width changed")
            local_exact = 0
            for frontier, witness in zip(FRONTIERS, record["individual_witnesses"]):
                if witness is not None:
                    paths = canonical if frontier is None else engine.path_ledger(
                        kernel, tuple(record["row"]), frontier)
                    audit_witness(engine, paths, witness, frontier)
                    local_exact += 1
        require(record["exact_target_total"] == local_exact, "exact subtotal changed")
        exact += local_exact
    require(payload["exact_target_total"] == exact, "exact total changed")
    require(payload["unresolved_target_total"] == payload["target_total"] - exact,
            "unresolved total changed")
    require(seen == set(range(start, start + len(payload["records"]))), "chunk range is not contiguous")


def audit_chunks(paths):
    expected_files = {name: (stored, raw) for name, stored, raw in CHUNKS}
    require(len(paths) == len(CHUNKS) and {path.name for path in paths} == set(expected_files),
            "full audit requires the complete pinned six-chunk universe")
    paths = sorted(paths, key=lambda path: tuple(expected_files).index(path.name))
    census = load_engine().load_census()
    residual_total = len(census["residuals"])
    frontier_total = residual_total * len(FRONTIERS)
    require(census["frontier_target_total"] == frontier_total, "authenticated census is inconsistent")
    seen = set()
    targets = exact = 0
    raw_digests = []
    stored_digests = []
    for path in paths:
        stored_digest, expected_raw_digest = expected_files[path.name]
        raw = artifact_bytes(path, stored_digest)
        digest = hashlib.sha256(raw).hexdigest()
        require(digest == expected_raw_digest, f"decompressed chunk digest changed: {path.name}")
        payload = load_json(raw)
        require(raw == canonical_bytes(payload), f"chunk is not canonical JSON: {path}")
        verify(payload)
        local = {record["source_index"] for record in payload["records"]}
        require(seen.isdisjoint(local), "overlapping chunks")
        seen.update(local)
        targets += payload["target_total"]
        exact += payload["exact_target_total"]
        raw_digests.append(digest)
        stored_digests.append(stored_digest)
    complete = seen == set(range(residual_total)) and targets == frontier_total
    manifest = hashlib.sha256(("\n".join(raw_digests) + "\n").encode("ascii")).hexdigest()
    require(manifest == MANIFEST_SHA256, "ordered manifest digest changed")
    artifact_manifest = hashlib.sha256(
        ("\n".join(stored_digests) + "\n").encode("ascii")).hexdigest()
    require(artifact_manifest == ARTIFACT_MANIFEST_SHA256,
            "ordered compressed-artifact manifest digest changed")
    require(complete, "full audit did not cover the authenticated key universe")
    print(f"chunks={len(paths)} records={len(seen)} targets={targets} exact={exact} "
          f"unresolved={targets - exact}")
    print(f"complete_frontier={str(complete).lower()} manifest_sha256={manifest}")
    print(f"artifact_manifest_sha256={artifact_manifest}")


def run(args):
    engine = load_engine()
    census = engine.load_census()
    stop = min(len(census["residuals"]), args.start + args.count)
    indices = range(args.start, stop)
    denominators = tuple(int(value) for value in args.denominators.split(","))
    require(denominators and all(value > 0 for value in denominators), "bad denominators")
    started = time.perf_counter()
    initargs = (denominators, args.seed, args.restarts, args.iterations,
                args.fallback_restarts, args.fallback_iterations)
    if args.workers == 1:
        initialize_worker(*initargs)
        records = [generate_record(index) for index in indices]
    else:
        context = multiprocessing.get_context("fork")
        with context.Pool(args.workers, initialize_worker, initargs) as pool:
            records = list(pool.imap(generate_record, indices, chunksize=args.worker_batch))
    elapsed = time.perf_counter() - started
    exact = sum(record["exact_target_total"] for record in records)
    return {
        "schema": SCHEMA,
        "status": "exact_chunk" if exact == 13 * len(records) else "finite_residual_chunk",
        "full_theorem": False,
        "source_census_sha256": engine.EXPECTED_CENSUS_SHA256,
        "source_residual_total": len(census["residuals"]),
        "source_frontier_total": census["frontier_target_total"],
        "selected_residual_start": args.start,
        "record_total": len(records),
        "target_total": 13 * len(records),
        "exact_target_total": exact,
        "unresolved_target_total": 13 * len(records) - exact,
        "elapsed_seconds": float(f"{elapsed:.6f}"),
        "workers": args.workers,
        "search": {"restarts": args.restarts, "iterations": args.iterations,
                   "fallback_restarts": args.fallback_restarts,
                   "fallback_iterations": args.fallback_iterations,
                   "denominators": list(denominators)},
        "records": records,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=min(16, os.cpu_count() or 1))
    parser.add_argument("--worker-batch", type=int, default=8)
    parser.add_argument("--seed", type=int, default=67173)
    parser.add_argument("--restarts", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=180)
    parser.add_argument("--fallback-restarts", type=int, default=1)
    parser.add_argument("--fallback-iterations", type=int, default=300)
    parser.add_argument("--denominators", default="256,1024,4096,16384,65536")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--audit", nargs="*", type=Path)
    args = parser.parse_args()
    if args.audit is not None:
        require(args.audit, "audit requires at least one chunk")
        audit_chunks(args.audit)
        return
    if args.verify is not None:
        raw = artifact_bytes(args.verify)
        payload = load_json(raw)
        require(raw == canonical_bytes(payload), "chunk is not canonical JSON")
    else:
        require(args.start >= 0 and args.count >= 0 and args.workers >= 1, "bad range or workers")
        payload = run(args)
        output = args.output or OUTPUT_DIR / f"chunk-{args.start:05d}-{args.start + args.count:05d}.json"
        require(output.parent.is_dir(), "output directory is missing")
        raw = canonical_bytes(payload)
        temporary = output.with_name(output.name + ".tmp")
        temporary.write_bytes(raw)
        os.replace(temporary, output)
    verify(payload)
    digest = hashlib.sha256(raw).hexdigest()
    print(f"records={payload['record_total']} targets={payload['target_total']} "
          f"exact={payload['exact_target_total']} unresolved={payload['unresolved_target_total']}")
    print(f"elapsed_seconds={payload['elapsed_seconds']:.6f} sha256={digest}")


if __name__ == "__main__":
    main()
