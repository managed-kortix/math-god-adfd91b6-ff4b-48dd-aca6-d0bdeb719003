#!/usr/bin/env python3
"""Compressed exact-rational witness search for rank-seven/order-seven residuals.

This specializes the audited R10G1 engine to the 40,964-row order-seven census.
Numerics only propose vectors; every stored witness is replayed with Fraction.
Payload-free atom records certify only their exact equality-owner target bitmap,
not all fourteen targets. The stream is an experiment and makes no theorem claim.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import lzma
import re
from pathlib import Path
from types import SimpleNamespace


HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "rank6_order10_cubic_exact_rational.py"
CENSUS_PATH = HERE / "rank7_order7_residual_census.json.xz"
CENSUS_ENGINE_PATH = HERE / "rank7_order7_residual_census.py"
ATOM_PATH = HERE / "rank7_order7_symbolic_atom_recognizer.py"
MAGIC = b"R7G1"
ORDER = DIMENSION = 7
PATH_COUNT = 13
BUDGET = __import__("fractions").Fraction(6)
EXPECTED_RESIDUALS = 40964
EXPECTED_SOURCE_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"
EXPECTED_RESIDUAL_SHA256 = "9cbc1f7ed5b156f8a9338990c0e32ba136796ac0fd6587710d3a4a37c3b2362c"
FRAGMENT_PATTERN = re.compile(r"fragment-(\d+)-(\d+)\.r7g\.xz\Z")
_CENSUS_PAYLOAD = None
_ATOM_MODULE = None
_ATOM_TARGETS = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = load_module("rank7_order7_r10_base", BASE_PATH)


def census_payload():
    global _CENSUS_PAYLOAD
    if _CENSUS_PAYLOAD is None:
        stored = CENSUS_PATH.read_bytes()
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        payload = json.loads(raw.decode("ascii"))
        engine = load_module("rank7_order7_census_audit", CENSUS_ENGINE_PATH)
        require(raw == engine.canonical_bytes(payload), "noncanonical order-seven census")
        engine.verify(payload)
        require(payload["coarse_residual_total"] == EXPECTED_RESIDUALS and
                payload["source_sha256"] == EXPECTED_SOURCE_SHA256 and
                payload["residual_stream_sha256"] == EXPECTED_RESIDUAL_SHA256,
                "order-seven residual census changed")
        _CENSUS_PAYLOAD = payload
    return _CENSUS_PAYLOAD


def load_census_module():
    payload = census_payload()
    pairs = tuple((u, v) for u in range(ORDER) for v in range(u + 1, ORDER))
    return SimpleNamespace(SOURCE_SHA256=payload["source_sha256"], PAIRS=pairs)


def residual_rows(census, progress=False, cache_path=None):
    require(cache_path is None, "the canonical order-seven census is already the cache")
    payload = census_payload()
    ledgers = {row["order_kernel"]: row for row in payload["kernels"]}
    pair_index = {edge: index for index, edge in enumerate(census.PAIRS)}
    result = []
    for source in payload["residuals"]:
        ledger = ledgers[source["order_kernel"]]
        edges = tuple(tuple(edge) for edge in ledger["edges"])
        support = tuple(pair_index[(u, v)] for u, v, _ in edges)
        multiplicities = tuple(value for _, _, value in edges)
        result.append((source["global_kernel"], None, support, multiplicities,
                       tuple(source["row"]), source["orbit_size"], None, False))
    require(len(result) == EXPECTED_RESIDUALS, "residual materialization changed")
    return tuple(result)


def source_edges(census, source):
    return tuple((*census.PAIRS[dense], multiplicity)
                 for dense, multiplicity in zip(source[2], source[3]))


def atom_target_map(census, residuals):
    global _ATOM_MODULE, _ATOM_TARGETS
    if _ATOM_TARGETS is None:
        if _ATOM_MODULE is None:
            _ATOM_MODULE = load_module("rank7_order7_stream_atoms", ATOM_PATH)
        targets = {}
        for source_index, source in enumerate(residuals):
            records = _ATOM_MODULE.recognize(source_edges(census, source), source[4])
            covered = set()
            for record in records:
                if record["status"] != "exact-equality-owner":
                    continue
                covered.update(0 if target is None else target + 1
                               for target in record["equality_frontiers"])
            if covered:
                targets[source_index] = frozenset(covered)
        require(len(targets) == 20, "exact symbolic atom owner total changed")
        _ATOM_TARGETS = targets
    return _ATOM_TARGETS


def atom_source_indices(residuals):
    return frozenset(atom_target_map(load_census_module(), residuals))


def verify_atom(census, source):
    global _ATOM_MODULE
    if _ATOM_MODULE is None:
        _ATOM_MODULE = load_module("rank7_order7_stream_atoms", ATOM_PATH)
    records = _ATOM_MODULE.recognize(source_edges(census, source), source[4])
    require(any(row["status"] == "exact-equality-owner" for row in records),
            "bad order-seven atom symbolic record")


def atom_targets(census, source):
    global _ATOM_MODULE
    if _ATOM_MODULE is None:
        _ATOM_MODULE = load_module("rank7_order7_stream_atoms", ATOM_PATH)
    covered = set()
    for record in _ATOM_MODULE.recognize(source_edges(census, source), source[4]):
        if record["status"] == "exact-equality-owner":
            covered.update(0 if target is None else target + 1
                           for target in record["equality_frontiers"])
    return frozenset(covered)


def summarize(records):
    shared, templates, fallback, unresolved, structural, atoms, balanced = (
        base._r10_summarize(records))
    if atoms:
        census = load_census_module()
        payload = census_payload()
        residuals = residual_rows(census)
        start = base._summary_start
        unresolved += sum(PATH_COUNT + 1 - len(atom_targets(census, residuals[start + local]))
                          for local, (mode, _) in enumerate(records)
                          if mode == base.MODE_ATOM)
    return shared, templates, fallback, unresolved, structural, atoms, balanced


def fragment_path(directory, start, stop):
    return directory / f"fragment-{start:06d}-{stop:06d}.r7g.xz"


def search(args, census, residuals):
    base._summary_start = args.start
    return base._r10_search(args, census, residuals)


def configure_base():
    base._r10_summarize = base.summarize
    base._r10_search = base.search
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
        "structural_certified": lambda census, source: False,
        "fragment_path": fragment_path,
        "summarize": summarize,
        "search": search,
    }
    for name, value in values.items():
        setattr(base, name, value)


configure_base()


if __name__ == "__main__":
    base.main()
    print("full_theorem=false")
