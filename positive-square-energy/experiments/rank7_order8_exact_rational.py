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
import re
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
FRAGMENT_PATTERN = re.compile(r"fragment-(\d+)-(\d+)\.r7o8g\.xz\Z")
_CENSUS = None
_RESIDUALS = None
_LANES = None


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


def load_census_module():
    global _CENSUS, _RESIDUALS
    if _CENSUS is not None:
        return _CENSUS
    lanes = lanes_module()
    manifest, manifest_digest = lanes.load_manifest(MANIFEST_PATH)
    require(manifest_digest == EXPECTED_MANIFEST_SHA256, "residual manifest changed")
    wanted = load_indices(manifest_digest)
    pairs = tuple((u, v) for u in range(ORDER) for v in range(u + 1, ORDER))
    pair_index = {edge: index for index, edge in enumerate(pairs)}
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
    stream_identity = hashlib.sha256(
        (manifest_digest + ":" + EXPECTED_INDICES_SHA256).encode("ascii")).hexdigest()
    _CENSUS = SimpleNamespace(SOURCE_SHA256=stream_identity, PAIRS=pairs)
    _RESIDUALS = tuple(residuals)
    return _CENSUS


def residual_rows(census, progress=False, cache_path=None):
    require(cache_path is None, "the authenticated chunk set is already the census cache")
    require(census is load_census_module(), "foreign census object")
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


def fragment_path(directory, start, stop):
    return directory / f"fragment-{start:06d}-{stop:06d}.r7o8g.xz"


def search(args, census, residuals):
    base._summary_start = args.start
    return base._r10_search(args, census, residuals)


def configure_base():
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
        "structural_certified": structural_certified,
        "fragment_path": fragment_path,
        "search": search,
    }
    for name, value in values.items():
        setattr(base, name, value)


configure_base()


if __name__ == "__main__":
    base.main()
    print("full_theorem=false")
