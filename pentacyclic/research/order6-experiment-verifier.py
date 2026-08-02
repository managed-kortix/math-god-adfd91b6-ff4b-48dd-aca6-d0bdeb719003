#!/usr/bin/env python3
"""Fail-closed verifier for the complete order-six experimental run."""

import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CENSUS_SCRIPT = HERE / "order6-tetra-census-experiment.py"
SEARCH_SCRIPT = HERE / "order6-dim6-rational-gram-experiment.py"
CENSUS = HERE / "order6-tetra-census.json"
RESULTS = HERE / "order6-dim6-rational-gram-results.json"
EXPECTED = {
    "census_sha256": "de4278bd890c99fa6c06e62c1641eb2f0ce3a3d4603427d2b80d24c674bb9089",
    "results_sha256": "6a46d2acebe60015c0071332f1152bb3da5c9b893e7fc22943a38162db37487e",
    "kernels": 38,
    "physical": 23208,
    "orbits": 12810,
    "tetra_certified": 11312,
    "tetra_residuals": 1498,
    "frontiers": 16478,
    "exact": 16451,
    "unresolved": 27,
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


def main():
    census_module = load_module("order6_census", CENSUS_SCRIPT)
    search_module = load_module("order6_search", SEARCH_SCRIPT)
    census, census_digest = census_module.audit()
    require(census_digest == EXPECTED["census_sha256"], "census digest changed")
    require(census["kernel_total"] == EXPECTED["kernels"], "kernel count changed")
    require(census["physical_total"] == EXPECTED["physical"], "physical count changed")
    require(census["orbit_total"] == EXPECTED["orbits"], "orbit count changed")
    require(census["tetra_certified_total"] == EXPECTED["tetra_certified"],
            "tetra-certified count changed")
    require(census["tetra_residual_total"] == EXPECTED["tetra_residuals"],
            "tetra residual count changed")
    require(census["frontier_target_total"] == EXPECTED["frontiers"],
            "frontier count changed")
    raw = RESULTS.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED["results_sha256"],
            "raw results digest changed")
    payload = json.loads(raw.decode("ascii"))
    require(raw == search_module.canonical_bytes(payload), "results are not canonical JSON")
    require(payload["complete_source_cover"] is True, "search does not cover the source")
    require(payload["target_total"] == EXPECTED["frontiers"], "search target count changed")
    require(payload["exact_certificate_total"] == EXPECTED["exact"], "exact count changed")
    require(payload["finite_unresolved_total"] == EXPECTED["unresolved"],
            "unresolved count changed")
    require(payload["full_theorem"] is False, "experimental result was theorem-promoted")
    search_module.verify(payload)
    unresolved = [record for record in payload["records"] if not record["exact_dnn_le_4"]]
    require(sorted({record["kernel"] for record in unresolved}) == [55, 61, 71],
            "unresolved kernel support changed")
    print("order-six experimental census/certificate audit passed")
    print("physical=23208 orbits=12810 tetra_certified=11312 tetra_residuals=1498")
    print("frontiers=16478 exact_rational=16451 finite_unresolved=27")
    print("unresolved_by_kernel=K55:9,K61:9,K71:9")
    print("full_theorem=false")
    print(f"census_sha256={census_digest}")
    print(f"results_sha256={hashlib.sha256(raw).hexdigest()}")


if __name__ == "__main__":
    main()
