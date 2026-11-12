#!/usr/bin/env python3
"""Fail-closed master gate for the rank-seven/order-nine single-block theorem.

Quick mode freshly authenticates the exact coarse/residual set identity, stored
structural partition, every persisted SOS/Gram certificate, the induced
transfer classification, obstruction closure, and the documentary analytic
sources.  It is deliberately theorem-ineligible: quick mode neither regenerates
the coarse census nor reruns all 2,835,895 structural owner predicates.

Full theorem eligibility requires three independent facts on the exact pinned
structural replayer bytes: a fresh eight-chunk census reconstruction, a fresh
precedence-ordered predicate replay with exact call/pass vectors, and canonical
normal/-O/no-write execution evidence for both.  Committed evidence is accepted
only when its own bytes, complete schema, source hashes, argv, outputs, and
before/after snapshots are exact.  No mode label or aggregate count suffices.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, NoReturn

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "research"
EXPERIMENTS = ROOT / "positive-square-energy" / "experiments"
HEPTACYCLIC = ROOT / "positive-square-energy" / "heptacyclic-general"

STRUCTURAL = EXPERIMENTS / "rank7_order9_structural_semantic_replayer.py"
UPSTREAM = EXPERIMENTS / "rank7_order9_upstream_owner_replayer.py"
CYCLE = EXPERIMENTS / "rank7_order9_cycle_gram_engine.py"
TRANSFER = HERE / "rank-seven-order-nine-induced-partition-transfer-verifier.py"
OBSTRUCTION = HERE / "rank-seven-order-nine-obstruction-branch-gram-verifier.py"
ANALYTIC_LIFT = HERE / "rank-seven-conditional-analytic-lift-verifier.py"
CENSUS_PRODUCER = EXPERIMENTS / "rank7_orders9_12_exact_residual_census.py"
COARSE_ENGINE = EXPERIMENTS / "rank7_parity_coarse_digest_census.py"
STRUCTURAL_OWNER = EXPERIMENTS / "rank7_order12_structural_owners.py"
ATOM_RECOGNIZER = EXPERIMENTS / "rank7_order7_symbolic_atom_recognizer.py"
KERNEL_FIXTURE = HERE / "fixtures" / "rank-seven-kernel-frontier-census.json"
EVIDENCE = HERE / "rank-seven-order-nine-child-execution-evidence.json"

STRUCTURAL_NOTE = HEPTACYCLIC / "rank-seven-single-block-structural-theorem.md"
TRANSFER_NOTE = HEPTACYCLIC / "rank-seven-order-nine-induced-partition-transfer.md"
OBSTRUCTION_NOTE = HEPTACYCLIC / "rank-seven-order-nine-obstruction-branch-gram-theorem.md"
BICYCLIC = ROOT / "all-bicyclic-graphs" / "paper.tex"
TRICYCLIC = ROOT / "all-tricyclic-graphs" / "paper.tex"
TETRACYCLIC = ROOT / "all-tetracyclic-graphs" / "paper.tex"

SCHEMA = "rank-seven-order-nine-kernel-theorem-master-v1"
EVIDENCE_SCHEMA = "rank-seven-order-nine-child-execution-evidence-v1"
Json = Any

# This first review head intentionally leaves the changed public structural
# source and execution-evidence digest unregistered.  It cannot claim theorem
# eligibility until exact normal/-O evidence lands and these two pins are
# replaced.  All other pins bind the exact integrated dependency bytes.
PYTHON_PINS = {
    STRUCTURAL: None,
    UPSTREAM: "f8d05d43a31b10058cf37176ceaa14c2562b1e845495ebc210232db0fce6f56c",
    CYCLE: "f9267ac9b2d41a4a09254e71e66f39fd78ffaadd334a4761c44c1a51ca59072e",
    TRANSFER: "4b9cb58aeb68b869b9c254a21ae7bd3cf18fc7360e7afb0a47fd8e570c40b2fe",
    OBSTRUCTION: "21acdb25b08b89ce9a5241932bc23d5fbdfec4c76333ab50c78d9371cf79e0b8",
    ANALYTIC_LIFT: "55e7d67a670f22a7b872b122f3aadcd2036ba922993f5faac1c5b72e2232e611",
    CENSUS_PRODUCER: "c6dcc792c7899c3f494a3beb521c94da972a01a392cd77be78b0956bbee3b921",
    COARSE_ENGINE: "d285a1c29cace4cb30882662e786cf1e5086ebc579676a3aa114a18e2365b2a5",
    STRUCTURAL_OWNER: "ffd76058b58344ea066777bdfd6d29eaed154c8d8d243d2c37ddf942f9558c45",
    ATOM_RECOGNIZER: "10de4fb714c15756341a7dbddb5a4da9f8ce5e0393aacc9e9434d619ebce9734",
}
DOCUMENT_PINS = {
    STRUCTURAL_NOTE: "f1daf9109f4843aa2db149c974fb21c847bb6f8144275201aebabed7fe4ea516",
    TRANSFER_NOTE: "3069961fe0937eabf3281685bcc04dd4e77de20150ddd49b57f1fa0eeb6c58ad",
    OBSTRUCTION_NOTE: "69d9a6d7a061ee8b9ef029d560799f51e19c3d6c199da9258f5929f684862899",
    BICYCLIC: "56a2b521ed0fee18d7e34ebb330e5b181e00979805fca951398f7a33d35b19da",
    TRICYCLIC: "13f8f8c7996c0f58f764c52b4a5b915132038e2ce38d3e56285f1bf952990fc1",
    TETRACYCLIC: "7d8174e64095e5cccf90776ccac92d2dd2ca3f73d500e2518461f5dfb907b93b",
    KERNEL_FIXTURE: "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5",
}
EVIDENCE_SHA256: str | None = None

STRUCTURAL_FAST_OUTPUT_SHA256: str | None = None
UPSTREAM_OUTPUT_SHA256 = "8975de0c41137973452e5699cd4eb339f520b7a8f8863a06e9d5f2a74192425b"
CYCLE_OUTPUT_SHA256 = "aa0f11d2a5f7e2bd49bba6d93bdd6b97de03eace705a98fd4c8cf7b636a6fb24"
TRANSFER_OUTPUT_SHA256 = "70154fd4dbded871ae77ffdc6a8ffdf7dc23ac86b8411aba983a90029fb642cd"
OBSTRUCTION_OUTPUT_SHA256 = "9e9bacf32b73627db45c092acfa785d1aafe465e4c8743f7054f74cf967d9770"

CHILDREN = (
    {"name": "structural-fast", "path": STRUCTURAL, "arguments": (),
     "source_sha256": None, "output_sha256": STRUCTURAL_FAST_OUTPUT_SHA256,
     "kind": "quick"},
    {"name": "upstream-sos-dominant", "path": UPSTREAM, "arguments": (),
     "source_sha256": PYTHON_PINS[UPSTREAM], "output_sha256": UPSTREAM_OUTPUT_SHA256,
     "kind": "quick"},
    {"name": "third-fourth-cycle-grams", "path": CYCLE,
     "arguments": ("--audit-historical", "third", "fourth"),
     "source_sha256": PYTHON_PINS[CYCLE], "output_sha256": CYCLE_OUTPUT_SHA256,
     "kind": "quick"},
    {"name": "induced-transfer", "path": TRANSFER, "arguments": (),
     "source_sha256": PYTHON_PINS[TRANSFER], "output_sha256": TRANSFER_OUTPUT_SHA256,
     "kind": "quick"},
    {"name": "obstruction-branch-gram", "path": OBSTRUCTION, "arguments": (),
     "source_sha256": PYTHON_PINS[OBSTRUCTION], "output_sha256": OBSTRUCTION_OUTPUT_SHA256,
     "kind": "quick"},
)

RESIDUAL_ORBITS = 2_835_895
RESIDUAL_PHYSICAL = 3_518_609
PARITY_ORBITS = 65_167_570
PARITY_PHYSICAL = 81_885_688
COARSE_ORBITS = 62_331_675
PARTITION_ORBITS = {
    "structural": 2_450_066,
    "sos": 113_309,
    "gram": 2_795,
    "transfer": 268_110,
    "obstruction": 1_615,
}
PARTITION_PHYSICAL = {
    "structural": 3_076_384,
    "sos": 134_899,
    "gram": 3_204,
    "transfer": 302_177,
    "obstruction": 1_945,
}
STRUCTURAL_CALLS = {
    "balanced-rank-one": 2_835_895,
    "signed-imbalance-psd": 2_834_382,
    "simplex-mixed-atom": 2_831_563,
    "generalized-ray": 2_831_150,
}
STRUCTURAL_PASSES = {
    "balanced-rank-one": 1_513,
    "signed-imbalance-psd": 2_819,
    "simplex-mixed-atom": 413,
    "generalized-ray": 2_445_321,
}
CENSUS_RAW_SHA256 = (
    "2712d3b761b7518ee6481d767410408673da825c9a31ec17d5a17784926da812",
    "6e4f63314b9f0dfb04fd9ecfd4b4c658fe306e31db6aaaa64b63e883afc099f0",
    "43c09e2ed2f38946e02efe095b7ff1621a48f98a1456ade7f8ebe19df51e3537",
    "6159cf8336b5c88cdeba6ca08bfc101fbe4f9d6051a24ff88bd899304feaa60f",
    "8ae1b27ca907a081962626a43d0847f84a33a0f38d3e5cb605c741db029a1528",
    "d56e9117bb04e508177693f383aa31a3e3928254f544a4c4842e41c7a54ff94b",
    "6b9a46b712003412da9c53caa14dfdf80e14a95c152e1a1b215c87f420273842",
    "e94b21dc4cc7e9dd0b88e3ca70f7a455cbc8373f3a0eb06c2f2ab7bbc0728392",
)


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def canonical_bytes(value: Json) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw: bytes, label: str) -> Json:
    def pairs(items: list[tuple[str, Json]]) -> dict[str, Json]:
        result: dict[str, Json] = {}
        for key, value in items:
            require(type(key) is str and key not in result,
                    f"{label}: duplicate or non-string key")
            result[key] = value
        return result

    def reject_float(token: str) -> NoReturn:
        fail(f"{label}: floating-point token rejected: {token}")

    try:
        value = json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                           parse_float=reject_float, parse_constant=reject_float)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: invalid JSON") from error
    require(raw == canonical_bytes(value), f"{label}: noncanonical JSON")
    return value


def exact_int(value: Json, label: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, f"{label}: invalid exact integer")
    return value


def exact_bool(value: Json, label: str) -> bool:
    require(type(value) is bool, f"{label}: invalid exact boolean")
    return value


def audit_pins(require_registered: bool) -> dict[str, str]:
    require(set(PYTHON_PINS).isdisjoint(DOCUMENT_PINS), "dependency registries overlap")
    observed = {}
    for path, expected in {**PYTHON_PINS, **DOCUMENT_PINS}.items():
        require(path.is_file(), f"missing dependency: {path.relative_to(ROOT)}")
        digest = sha256(path.read_bytes())
        if expected is None:
            require(not require_registered, f"unregistered dependency: {path.name}")
        else:
            require(digest == expected, f"dependency bytes changed: {path.name}")
        observed[path.relative_to(ROOT).as_posix()] = digest
    return observed


def audit_no_asserts() -> int:
    paths = (Path(__file__).resolve(), *PYTHON_PINS)
    require(len(set(paths)) == len(paths), "Python source registry duplicates a path")
    for path in paths:
        tree = ast.parse(path.read_text("ascii"), filename=str(path))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
                f"optimization-removable assert in {path.name}")
    return len(paths)


def parse_lines(output: str, expected_lines: int, label: str) -> tuple[Json, ...]:
    try:
        raw_lines = output.encode("ascii").splitlines(keepends=True)
    except UnicodeError as error:
        raise RuntimeError(f"{label}: non-ASCII output") from error
    require(len(raw_lines) == expected_lines and all(line.endswith(b"\n") for line in raw_lines),
            f"{label}: unexpected line count")
    return tuple(strict_json(line, f"{label} line {index}")
                 for index, line in enumerate(raw_lines, 1))


def validate_structural(result: Json, *, predicates: bool, census: bool) -> None:
    require(type(result) is dict and result.get("schema") ==
            "rank-seven-order-nine-structural-semantic-replay-v1" and
            result.get("status") == "passed" and result.get("complete") is True and
            result.get("read_only") is True and result.get("writes") == 0,
            "structural result identity changed")
    require(result.get("base_identity") == {
        "coarse_certified_total": COARSE_ORBITS,
        "coarse_residual_physical_total": RESIDUAL_PHYSICAL,
        "coarse_residual_total": RESIDUAL_ORBITS,
        "frontier_target_total": RESIDUAL_ORBITS * 16,
        "identity_validated": True,
        "kernel_total": 4_495,
        "parity_orbit_total": PARITY_ORBITS,
        "physical_row_total": PARITY_PHYSICAL,
    }, "structural base identity changed")
    require(result.get("exclusive_owner_orbit_counts") == STRUCTURAL_PASSES and
            result.get("exclusive_owner_physical_counts") == {
                "balanced-rank-one": 1_593,
                "generalized-ray": 3_071_139,
                "signed-imbalance-psd": 3_185,
                "simplex-mixed-atom": 467,
            } and result.get("owner_orbit_total") == PARTITION_ORBITS["structural"] and
            result.get("owner_physical_total") == PARTITION_PHYSICAL["structural"] and
            result.get("remainder_orbit_total") == 385_829 and
            result.get("remainder_physical_total") == 442_225 and
            result.get("row_zip_total") == RESIDUAL_ORBITS and
            result.get("orbit_recomputations") == RESIDUAL_ORBITS and
            result.get("automorphism_recomputations") == 4_495 and
            result.get("burnside_recomputations") == 4_495,
            "structural exact partition ledger changed")
    source = result.get("source_identity", {})
    require(type(source) is dict and source.get("partition_validated") is True and
            source.get("universe_orbit_total") == RESIDUAL_ORBITS and
            source.get("universe_physical_total") == RESIDUAL_PHYSICAL and
            source.get("owner_orbit_total") == PARTITION_ORBITS["structural"] and
            source.get("remainder_orbit_total") == 385_829,
            "structural source-key partition changed")
    if predicates:
        require(result.get("predicate_replay_eligible") is True and
                result.get("recognition_calls") == RESIDUAL_ORBITS and
                result.get("row_recognition_calls") == RESIDUAL_ORBITS and
                result.get("predicate_calls") == STRUCTURAL_CALLS and
                result.get("predicate_call_total") == sum(STRUCTURAL_CALLS.values()) and
                result.get("predicate_passes") == STRUCTURAL_PASSES and
                result.get("predicate_pass_total") == PARTITION_ORBITS["structural"] and
                result.get("generalized_three_ray_calls") ==
                STRUCTURAL_CALLS["generalized-ray"] and
                result.get("generalized_three_ray_passes") ==
                STRUCTURAL_PASSES["generalized-ray"],
                "structural full predicate vector changed")
    else:
        require(result.get("predicate_replay_eligible") is False and
                result.get("recognition_calls") == 0 and
                result.get("predicate_call_total") == 0 and
                result.get("predicate_calls") == {key: 0 for key in STRUCTURAL_CALLS} and
                result.get("predicate_passes") == {key: 0 for key in STRUCTURAL_PASSES},
                "structural quick mode laundered predicate replay")
    require(result.get("census_reconstruction") is census and
            result.get("census_reconstruction_chunks") == (8 if census else 0),
            "structural census reconstruction evidence changed")
    if census:
        require(tuple(result.get("census_reconstructed_raw_sha256", ())) ==
                CENSUS_RAW_SHA256 and
                result.get("census_reconstruction_kernel_total") == 4_495 and
                result.get("census_reconstruction_generate_calls") == 8,
                "fresh census call/hash vector changed")


def validate_upstream(result: Json) -> None:
    require(type(result) is dict and result.get("schema") ==
            "rank-seven-order-nine-upstream-owner-replay-v1" and
            result.get("status") == "exact-upstream-owner-replay-passed" and
            result.get("read_only") is True and result.get("arithmetic") ==
            "fractions.Fraction", "upstream replay identity changed")
    sos = result.get("sos", {})
    dominant = result.get("dominant_family", {})
    require(sos.get("structural_remainder_orbits") == 385_829 and
            sos.get("owner_orbits") == PARTITION_ORBITS["sos"] and
            sos.get("owner_physical") == PARTITION_PHYSICAL["sos"] and
            sos.get("after_sos_orbits") == 272_520 and
            sos.get("exclusive_owner_orbits") == {
                "scalar-sos": 7_796, "typed-sos": 105_513} and
            dominant.get("owner_orbits") == 1_128 and
            dominant.get("owner_physical") == 1_173 and
            result.get("sos_owner_physical") == PARTITION_PHYSICAL["sos"] and
            result.get("combined_sos_dominant_physical") == 136_072,
            "upstream exact owner ledger changed")


def validate_cycle(result: Json) -> None:
    require(type(result) is dict and set(result) == {"third", "fourth"},
            "cycle lane registry changed")
    require(result["third"].get("record_total") == 631 and
            result["third"].get("physical_total") == 748 and
            result["fourth"].get("record_total") == 1_036 and
            result["fourth"].get("physical_total") == 1_283,
            "cycle lane exact replay ledger changed")


def validate_transfer(result: Json) -> None:
    require(type(result) is dict and result.get("analytic_dependencies_authenticated") is False and
            result.get("source_orbits_recomputed") == 272_520 and
            result.get("post_lane_orbits") == 269_725 and
            result.get("post_lane_physical") == 304_122 and
            result.get("partition_owned_orbits") == PARTITION_ORBITS["transfer"] and
            result.get("partition_owned_physical") == PARTITION_PHYSICAL["transfer"] and
            result.get("obstruction_orbits") == PARTITION_ORBITS["obstruction"] and
            result.get("obstruction_physical") == PARTITION_PHYSICAL["obstruction"],
            "induced transfer ledger changed")


def validate_obstruction(result: Json) -> None:
    require(type(result) is dict and result == {
        "all_descendant_rows": 1_615,
        "all_descendant_targets": 25_840,
        "direct_exact_cost": [607_593_754, 122_731_245],
        "direct_rows": 1,
        "frontier_physical_rows": 1_945,
        "frontier_rows": 1_615,
        "represented_kernels": 115,
        "switched_three_ray_max_scaled_charge": 360,
        "switched_three_ray_rows": 1_614,
        "witness_stream_sha256":
            "912058dbc7f22d33bd777c4b848aaba7168f8dd280a1605871403eb22a213d4c",
    }, "obstruction closure ledger changed")


def validate_child_output(name: str, output: str) -> Json:
    if name == "structural-fast":
        (result,) = parse_lines(output, 1, name)
        validate_structural(result, predicates=False, census=False)
        return result
    if name == "upstream-sos-dominant":
        (result,) = parse_lines(output, 1, name)
        validate_upstream(result)
        return result
    if name == "third-fourth-cycle-grams":
        (result,) = parse_lines(output, 1, name)
        validate_cycle(result)
        return result
    if name == "induced-transfer":
        result, = parse_lines(output.splitlines(keepends=True)[0], 1, name)
        require(output.splitlines() == [output.splitlines()[0],
                "rank-seven order-nine induced-partition transfer verifier: PASS"],
                "induced transfer report line changed")
        validate_transfer(result)
        return result
    if name == "obstruction-branch-gram":
        result, = parse_lines(output.splitlines(keepends=True)[0], 1, name)
        require(output.splitlines() == [output.splitlines()[0],
                "rank-seven order-nine obstruction branch-Gram verifier: PASS"],
                "obstruction report line changed")
        validate_obstruction(result)
        return result
    fail(f"unknown child: {name}")


def invoke(child: dict[str, Json]) -> dict[str, Json]:
    require(child["source_sha256"] is not None and child["output_sha256"] is not None,
            f"unregistered quick child: {child['name']}")
    raw = child["path"].read_bytes()
    require(sha256(raw) == child["source_sha256"], f"child source changed: {child['name']}")
    command = [sys.executable, "-B"]
    if sys.flags.optimize:
        command.append("-O")
    command.extend((str(child["path"]), *child["arguments"]))
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(command, check=False, capture_output=True,
                               text=True, env=environment)
    require(completed.returncode == 0 and completed.stderr == "",
            f"quick child failed: {child['name']}")
    require(sha256(completed.stdout.encode("ascii")) == child["output_sha256"],
            f"quick child output changed: {child['name']}")
    result = validate_child_output(child["name"], completed.stdout)
    return {"name": child["name"], "source_sha256": child["source_sha256"],
            "output_sha256": child["output_sha256"], "result": result}


def validate_evidence_record(record: Json, name: str, arguments: tuple[str, ...],
                             *, predicates: bool, census: bool) -> dict[str, Json]:
    fields = {"arguments", "exit_code", "mode", "name", "normal_output",
              "normal_output_sha256", "optimized_output",
              "optimized_output_sha256", "source_path", "source_sha256",
              "stderr_normal", "stderr_optimized", "write_snapshot_after_sha256",
              "write_snapshot_before_sha256"}
    require(type(record) is dict and set(record) == fields,
            f"execution evidence fields changed: {name}")
    require(record["name"] == name and record["arguments"] == list(arguments) and
            record["exit_code"] == 0 and record["stderr_normal"] == "" and
            record["stderr_optimized"] == "" and
            record["mode"] == "normal-and-python-O-read-only" and
            record["source_path"] == STRUCTURAL.relative_to(ROOT).as_posix() and
            record["source_sha256"] == PYTHON_PINS[STRUCTURAL] and
            record["write_snapshot_before_sha256"] ==
            record["write_snapshot_after_sha256"],
            f"execution evidence identity changed: {name}")
    normal = record["normal_output"]
    optimized = record["optimized_output"]
    require(type(normal) is str and normal == optimized and
            record["normal_output_sha256"] == record["optimized_output_sha256"] ==
            sha256(normal.encode("ascii")),
            f"normal/-O output evidence differs: {name}")
    (result,) = parse_lines(normal, 1, name)
    validate_structural(result, predicates=predicates, census=census)
    return {"name": name, "arguments": list(arguments),
            "source_sha256": record["source_sha256"],
            "output_sha256": record["normal_output_sha256"],
            "no_write_snapshot_sha256": record["write_snapshot_before_sha256"]}


def load_full_evidence() -> tuple[dict[str, Json], dict[str, Json]]:
    require(EVIDENCE_SHA256 is not None, "unregistered full execution evidence")
    raw = EVIDENCE.read_bytes()
    require(sha256(raw) == EVIDENCE_SHA256, "full execution evidence bytes changed")
    payload = strict_json(raw, "full execution evidence")
    require(type(payload) is dict and set(payload) == {"schema", "evidence_kind", "records"}
            and payload["schema"] == EVIDENCE_SCHEMA and
            payload["evidence_kind"] == "canonical-normal-O-no-write-executions" and
            type(payload["records"]) is list and len(payload["records"]) == 2,
            "full execution evidence semantics changed")
    census = validate_evidence_record(
        payload["records"][0], "structural-census-reconstruction",
        ("--reconstruct-census",), predicates=False, census=True)
    predicates = validate_evidence_record(
        payload["records"][1], "structural-full-predicate-replay",
        ("--full-rescan",), predicates=True, census=False)
    return census, predicates


def validate_partition() -> None:
    require(sum(PARTITION_ORBITS.values()) == RESIDUAL_ORBITS and
            sum(PARTITION_PHYSICAL.values()) == RESIDUAL_PHYSICAL and
            COARSE_ORBITS + RESIDUAL_ORBITS == PARITY_ORBITS,
            "orbit partition arithmetic changed")
    require((PARTITION_ORBITS["structural"] + PARTITION_ORBITS["sos"] == 2_563_375 and
             385_829 - PARTITION_ORBITS["sos"] == 272_520 and
             PARTITION_ORBITS["gram"] == 1_128 + 631 + 1_036 and
             272_520 - PARTITION_ORBITS["gram"] == 269_725 and
             PARTITION_ORBITS["transfer"] + PARTITION_ORBITS["obstruction"] ==
             269_725), "precedence complement arithmetic changed")
    require((PARTITION_PHYSICAL["structural"] + PARTITION_PHYSICAL["sos"] == 3_211_283 and
             442_225 - PARTITION_PHYSICAL["sos"] == 307_326 and
             PARTITION_PHYSICAL["gram"] == 1_173 + 748 + 1_283 and
             307_326 - PARTITION_PHYSICAL["gram"] == 304_122 and
             PARTITION_PHYSICAL["transfer"] + PARTITION_PHYSICAL["obstruction"] ==
             304_122), "precedence physical-complement arithmetic changed")


def validate_analytic_lift() -> dict[str, Json]:
    completed = subprocess.run(
        (sys.executable, "-B", str(ANALYTIC_LIFT), "--print-manifest"),
        check=False, capture_output=True, text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    require(completed.returncode == 0 and completed.stderr == "",
            "analytic lift verifier failed")
    first, separator, report = completed.stdout.partition("\n")
    require(separator and report, "analytic lift omitted report")
    manifest = strict_json((first + "\n").encode("ascii"), "analytic lift manifest")
    require(manifest.get("schema") == "rank-seven-conditional-analytic-lift-v1" and
            manifest.get("rank") == 7 and manifest.get("budget") == 6 and
            manifest.get("finite_premise_discharged") is False and
            manifest.get("global_claim") is False and
            manifest.get("proof_sha256") == DOCUMENT_PINS[STRUCTURAL_NOTE],
            "analytic lift conditional contract changed")
    return manifest


def implication_manifest(dependencies: dict[str, str], quick: list[dict[str, Json]],
                         full: tuple[dict[str, Json], dict[str, Json]]
                         ) -> dict[str, Json]:
    census_evidence, predicate_evidence = full
    return {
        "schema": SCHEMA,
        "evidence_kind": "exact-theorem-owner",
        "mode": "full",
        "theorem_eligible": True,
        "scope": {
            "kernel": "loopless 2-connected rank-seven multigraph of order nine",
            "realization": ("finite simple positive-length subdivision; at most one unit path "
                            "per parallel class"),
            "block_scope": "exactly one positive-rank cyclic block",
            "attachments": ("finite rooted trees attached at branch or subdivision vertices; "
                            "one root per tree and pairwise-disjoint nonroot sets"),
        },
        "conclusion": "s+(G)>=|V(G)|",
        "base_universe": {
            "kernel_total": 4_495,
            "physical_rows": PARITY_PHYSICAL,
            "parity_orbits": PARITY_ORBITS,
            "coarse_certified_orbits": COARSE_ORBITS,
            "residual_orbits": RESIDUAL_ORBITS,
            "residual_physical": RESIDUAL_PHYSICAL,
        },
        "residual_partition_orbits": PARTITION_ORBITS,
        "residual_partition_physical": PARTITION_PHYSICAL,
        "precedence": ["structural", "sos", "gram", "transfer", "obstruction"],
        "fresh_census_evidence": census_evidence,
        "fresh_structural_predicate_evidence": predicate_evidence,
        "quick_exact_replays": quick,
        "dependency_sha256": dependencies,
        "analytic_dependency_authentication": {
            "structural_reduction": DOCUMENT_PINS[STRUCTURAL_NOTE],
            "induced_transfer_note": DOCUMENT_PINS[TRANSFER_NOTE],
            "obstruction_note": DOCUMENT_PINS[OBSTRUCTION_NOTE],
            "rank_two_theorem": DOCUMENT_PINS[BICYCLIC],
            "rank_three_theorem": DOCUMENT_PINS[TRICYCLIC],
            "rank_four_theorem": DOCUMENT_PINS[TETRACYCLIC],
        },
        "excluded_scope": [
            "kernel orders other than nine",
            "multiple positive-rank cyclic blocks",
            "non-simple or looped realizations",
            "STATE or project-global promotion",
        ],
    }


def blocked_manifest(dependencies: dict[str, str], reason: str) -> dict[str, Json]:
    return {
        "schema": SCHEMA,
        "evidence_kind": "fail-closed-incomplete-review-gate",
        "mode": "quick-blocked",
        "theorem_eligible": False,
        "global_claim": False,
        "reason": reason,
        "base_partition_arithmetic_authenticated": True,
        "residual_partition_orbits": PARTITION_ORBITS,
        "residual_partition_physical": PARTITION_PHYSICAL,
        "dependency_sha256": dependencies,
        "required_full_evidence": {
            "fresh_census_reconstruction": True,
            "fresh_structural_predicate_replay": True,
            "normal_and_python_O_output_identity": True,
            "read_only_before_after_snapshot_identity": True,
            "exact_census_raw_hash_vector": list(CENSUS_RAW_SHA256),
            "exact_predicate_calls": STRUCTURAL_CALLS,
            "exact_predicate_passes": STRUCTURAL_PASSES,
        },
    }


def expect_rejected(action, label: str) -> None:
    try:
        action()
    except (RuntimeError, TypeError, ValueError, KeyError):
        return
    fail(f"hostile mutation accepted: {label}")


def hostile_self_checks() -> int:
    validate_partition()
    count = 0
    changed = deepcopy(PARTITION_ORBITS)
    changed["gram"] -= 1
    expect_rejected(lambda: require(sum(changed.values()) == RESIDUAL_ORBITS,
                                    "gap accepted"), "orbit gap")
    count += 1
    changed = deepcopy(PARTITION_PHYSICAL)
    changed["transfer"] += 1
    expect_rejected(lambda: require(sum(changed.values()) == RESIDUAL_PHYSICAL,
                                    "physical laundering accepted"), "physical laundering")
    count += 1
    expect_rejected(lambda: strict_json(b'{"x":1,"x":2}\n', "duplicate"),
                    "duplicate JSON")
    count += 1
    expect_rejected(lambda: strict_json(b'{"x":1.0}\n', "float"), "JSON float")
    count += 1
    expect_rejected(lambda: exact_int(True, "bool"), "boolean integer")
    count += 1
    synthetic = {"schema": "rank-seven-order-nine-structural-semantic-replay-v1",
                 "status": "passed", "complete": True, "read_only": True, "writes": 0}
    expect_rejected(lambda: validate_structural(synthetic, predicates=True, census=False),
                    "status-only structural result")
    count += 1
    require(EVIDENCE_SHA256 is None and PYTHON_PINS[STRUCTURAL] is None,
            "review skeleton unexpectedly registered evidence")
    count += 1
    return count


def audit(full: bool) -> dict[str, Json]:
    validate_partition()
    require(hostile_self_checks() == 7, "hostile self-check count changed")
    dependencies = audit_pins(require_registered=full)
    require(audit_no_asserts() == len(PYTHON_PINS) + 1,
            "AST source count changed")
    if not full:
        reason = ("structural source/output and committed full execution evidence are not yet "
                  "registered on this review head")
        return blocked_manifest(dependencies, reason)
    validate_analytic_lift()
    quick = [invoke(child) for child in CHILDREN]
    full_evidence = load_full_evidence()
    return implication_manifest(dependencies, quick, full_evidence)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="require exact registered normal/-O/no-write full evidence")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = audit(args.full)
    except (OSError, RuntimeError, TypeError, ValueError, UnicodeError,
            json.JSONDecodeError) as error:
        sys.stderr.write(f"rank-seven order-nine master: FAIL CLOSED: {error}\n")
        return 1
    if args.print_manifest:
        sys.stdout.buffer.write(canonical_bytes(manifest))
    if manifest["theorem_eligible"]:
        sys.stdout.write("rank-seven order-nine kernel theorem: exact full audit passed\n")
    else:
        sys.stdout.write("rank-seven order-nine master review gate: blocked fail-closed\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
