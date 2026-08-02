#!/usr/bin/env python3
"""Fail-closed verifier for the complete order-seven experimental run."""

import collections
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CENSUS_SCRIPT = HERE / "order7-tetra-census-experiment.py"
SEARCH_SCRIPT = HERE / "order7-dim7-rational-gram-experiment.py"
RESULTS = HERE / "order7-dim7-rational-gram-results.json"
EXPECTED = {
    "census_sha256": "a9a05f50cf3db61cf104cd88c966f11064671d7b8027a83d065721e8b395d8b1",
    "results_sha256": "7d581bfaa5d02f2ee7642f998371f48c29cdb961c2cebc43d3d2d666632c1a17",
    "kernels": 23,
    "physical": 31112,
    "orbits": 18026,
    "tetra_certified": 14306,
    "tetra_residuals": 3720,
    "frontiers": 44640,
    "exact": 44616,
    "unresolved": 24,
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def key(record):
    return record["kernel"], tuple(record["row"]), record["frontier"]


def main():
    census_module = load_module("order7_census", CENSUS_SCRIPT)
    search_module = load_module("order7_search", SEARCH_SCRIPT)
    census, census_digest = census_module.audit()
    require(census_digest == EXPECTED["census_sha256"], "census digest changed")
    for field, expected in (("kernel_total", "kernels"), ("physical_total", "physical"),
                            ("orbit_total", "orbits"),
                            ("tetra_certified_total", "tetra_certified"),
                            ("tetra_residual_total", "tetra_residuals"),
                            ("frontier_target_total", "frontiers")):
        require(census[field] == EXPECTED[expected], f"{field} changed")

    raw = RESULTS.read_bytes()
    results_digest = hashlib.sha256(raw).hexdigest()
    require(results_digest == EXPECTED["results_sha256"], "raw results digest changed")
    payload = json.loads(raw.decode("ascii"))
    require(raw == search_module.canonical_bytes(payload), "results are not canonical JSON")
    require(payload["complete_source_cover"] is True, "search does not cover the source")
    require(payload["target_total"] == EXPECTED["frontiers"], "target count changed")
    require(payload["exact_certificate_total"] == EXPECTED["exact"], "exact count changed")
    require(payload["finite_unresolved_total"] == EXPECTED["unresolved"],
            "unresolved count changed")
    require(payload["full_theorem"] is False, "experimental result was theorem-promoted")
    search_module.verify(payload)

    expected_keys = {(record["kernel"], tuple(record["row"]), frontier)
                     for record in census["residuals"]
                     for frontier in (None, *range(11))}
    actual_keys = [key(record) for record in payload["records"]]
    require(len(actual_keys) == len(set(actual_keys)), "duplicate result key")
    require(set(actual_keys) == expected_keys, "result key cover changed")
    unresolved = [record for record in payload["records"] if not record["exact_dnn_le_4"]]
    require({record["kernel"] for record in unresolved} == {80},
            "unresolved kernel support changed")
    require({record["frontier"] for record in unresolved} == {None, 0, 3, 6},
            "unresolved frontier support changed")
    require(collections.Counter(record["frontier"] for record in unresolved)
            == collections.Counter({None: 6, 0: 6, 3: 6, 6: 6}),
            "unresolved frontier multiplicities changed")
    require(all(record["numerical_cost"] == 4.0 for record in unresolved),
            "unresolved targets are not equality limits")

    print("order-seven experimental census/certificate audit passed")
    print("physical=31112 orbits=18026 tetra_certified=14306 tetra_residuals=3720")
    print("frontiers=44640 exact_rational=44616 finite_unresolved=24")
    print("unresolved=K80:24 frontiers=canonical:6,0:6,3:6,6:6 numerical_cost=4")
    print("full_theorem=false")
    print(f"census_sha256={census_digest}")
    print(f"results_sha256={results_digest}")


if __name__ == "__main__":
    main()
