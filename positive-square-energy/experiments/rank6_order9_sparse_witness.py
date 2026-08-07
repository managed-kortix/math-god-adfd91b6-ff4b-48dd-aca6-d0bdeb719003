#!/usr/bin/env python3
"""Compact exact-rational witness generator for the order-nine frontier.

This specializes the audited R8G2 sparse pipeline to K971--K1132. Numerical
optimization only proposes vectors; every stored witness is reconstructed and
verified with Fraction. The binary R9G1 stream supports shared, individual,
unresolved, and payload-free K971 template records and is XZ-compressed.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
import time
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


HERE = __import__("pathlib").Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE_PATH = HERE / "rank6_order8_sparse_pipeline.py"
ENGINE_PATH = ROOT / "pentacyclic" / "research" / "order7-dim7-rational-gram-experiment.py"
SOURCE = ROOT / "research" / "fixtures" / "rank-six-kernels.json"
SOURCE_SHA256 = "5a862a0e9ed5dfe91ff6f8491936c8e775eb39b71619df6b8c2a9be2c4643476"
ORDER = 9
RANK = 6
PATH_COUNT = ORDER + RANK - 1
BUDGET = Fraction(RANK - 1)
BUDGET_SCALED = 30 * (RANK - 1)
PAIRS = tuple(itertools.combinations(range(ORDER), 2))
PAIR_INDEX = {edge: index for index, edge in enumerate(PAIRS)}
SCHEMA = "rank-six-order-nine-sparse-witness-experiment-v1"
MAGIC = b"R9G1"
KERNEL_INTERVAL = (971, 1132)
EXPECTED_TOTALS = (1726000, 1108126, 921831, 186295, 2794425, 10, 150)
SIGNED_CYCLE_SUPPORTS = {
    971: ({"07", "16", "25", "34"}, {"08", "18", "27", "36", "45"}),
}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_module("rank6_order9_sparse_base", BASE_PATH)


def source_kernels():
    raw = SOURCE.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "rank-six fixture changed")
    payload = json.loads(raw.decode("ascii"))
    rows = []
    for number, record in enumerate(payload["kernels"], 1):
        if record["n"] != ORDER:
            continue
        dense = tuple(record["code"])
        require(len(dense) == len(PAIRS), "dense kernel width changed")
        support = tuple(index for index, value in enumerate(dense) if value)
        multiplicities = tuple(dense[index] for index in support)
        require(sum(multiplicities) == PATH_COUNT, "path count changed")
        degrees = [0] * ORDER
        for index, value in zip(support, multiplicities):
            u, v = PAIRS[index]
            degrees[u] += value
            degrees[v] += value
        require(sorted(degrees, reverse=True) == [4] + [3] * 8,
                "degree partition is not 4,3^8")
        rows.append((number, dense, support, multiplicities, tuple(degrees)))
    require(len(rows) == 162 and (rows[0][0], rows[-1][0]) == KERNEL_INTERVAL,
            "order-nine kernel interval changed")
    return tuple(rows)


def load_engine():
    engine = load_module("rank6_order9_vector_engine", ENGINE_PATH)
    engine.DIMENSION = ORDER
    engine.BUDGET = BUDGET
    engine.PAIRS = PAIRS
    return engine


def verify_individual_witness(engine, source, target, witness):
    _, support, multiplicities, row, _, _, _ = source
    kernel = base.dense_kernel(support, multiplicities)
    parity = base.dense_row(support, row)
    frontier = None if target == 0 else target - 1
    paths = engine.path_ledger(kernel, parity, frontier)
    denominator, branch_parameters, internals = witness
    require(type(denominator) is int and denominator > 0 and
            len(branch_parameters) == ORDER and len(internals) == PATH_COUNT,
            "bad individual witness")
    for parameters in branch_parameters:
        require(len(parameters) == ORDER - 1 and
                all(type(value) is Fraction and denominator % value.denominator == 0
                    for value in parameters), "individual branch denominator changed")
    branches = tuple(engine.rational_unit(value) for value in branch_parameters)
    total = Fraction()
    for (_, _, u, v, length), parameters in zip(paths, internals):
        require(len(parameters) == length - 1, "individual path width changed")
        for vector in parameters:
            require(len(vector) == ORDER - 1 and
                    all(type(value) is Fraction and denominator % value.denominator == 0
                        for value in vector), "individual internal denominator changed")
        endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
        chain = [branches[u], *(engine.rational_unit(value) for value in parameters), endpoint]
        total += sum((engine.exact_step_cost(a, b) for a, b in zip(chain, chain[1:])),
                     Fraction())
    require(total <= BUDGET, "individual exact cost exceeds five")
    return total


def census(collect_residuals=False, progress=False):
    started = time.perf_counter()
    ledgers = []
    residual_rows = []
    sources = source_kernels()
    for index, source in enumerate(sources, 1):
        ledger, local = base.kernel_census(source, collect_residuals)
        ledgers.append(ledger)
        residual_rows.extend(local)
        if progress:
            print(f"[{index}/{len(sources)}] K{ledger['kernel']} "
                  f"orbits={ledger['parity_orbits']} residuals={ledger['coarse_residuals']}",
                  flush=True)
    residual_total = sum(row["coarse_residuals"] for row in ledgers)
    template_total = sum(row["signed_cycle_template_orbits"] for row in ledgers)
    totals = (
        sum(row["physical_rows"] for row in ledgers),
        sum(row["parity_orbits"] for row in ledgers),
        sum(row["coarse_certified"] for row in ledgers),
        residual_total,
        (PATH_COUNT + 1) * residual_total,
        template_total,
        (PATH_COUNT + 1) * template_total,
    )
    require(totals == EXPECTED_TOTALS, "order-nine census totals changed")
    payload = {
        "schema": SCHEMA,
        "status": "census_complete_certificates_open",
        "full_theorem": False,
        "source_sha256": SOURCE_SHA256,
        "rank": RANK,
        "order": ORDER,
        "kernel_interval": list(KERNEL_INTERVAL),
        "kernel_total": len(ledgers),
        "path_count": PATH_COUNT,
        "frontiers_per_residual": PATH_COUNT + 1,
        "physical_total": totals[0],
        "parity_orbit_total": totals[1],
        "coarse_certified_total": totals[2],
        "coarse_residual_total": totals[3],
        "frontier_target_total": totals[4],
        "signed_cycle_template_orbit_total": totals[5],
        "signed_cycle_template_target_total": totals[6],
        "search_target_after_templates": totals[4] - totals[6],
        "representation": "support rows regenerated from source; no residual or target JSON",
        "elapsed_seconds": float(f"{time.perf_counter() - started:.6f}"),
        "kernels": ledgers,
    }
    return payload, residual_rows


def configure_base():
    values = {
        "SOURCE": SOURCE,
        "ENGINE_PATH": ENGINE_PATH,
        "SOURCE_SHA256": SOURCE_SHA256,
        "ORDER": ORDER,
        "RANK": RANK,
        "PATH_COUNT": PATH_COUNT,
        "BUDGET": BUDGET,
        "BUDGET_SCALED": BUDGET_SCALED,
        "PAIRS": PAIRS,
        "PAIR_INDEX": PAIR_INDEX,
        "MAGIC": MAGIC,
        "SCHEMA": SCHEMA,
        "SIGNED_CYCLE_SUPPORTS": SIGNED_CYCLE_SUPPORTS,
        "source_kernels": source_kernels,
        "load_engine": load_engine,
        "verify_individual_witness": verify_individual_witness,
        "census": census,
    }
    for name, value in values.items():
        setattr(base, name, value)
    base.COLORINGS = tuple(base.restricted_growth_strings())


configure_base()


if __name__ == "__main__":
    base.main()
