#!/usr/bin/env python3
"""Read-only exact verifier for order-eight packet lanes VII--XII.

This test starts at the authenticated sixth-family remainder.  For each later
lane it replays every stored shared witness with ``Fraction``, proves that the
owners are exactly the lane's declared target family, and checks that the next
remainder is the ordered byte-for-byte complement of those owners.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import lzma
import math
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any, Iterator, Mapping, NoReturn, Sequence, TypeGuard

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
if str(EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(EXPERIMENTS))

ORDINALS = ("seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth")
EXPECTED = {
    "seventh": {
        "counts": (76085, 6817, 69268),
        "target": ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (2, 3, 6), 4, 2),
        "schema": "rank-seven-order-eight-seventh-induced-packet-gram-family-v1",
        "physical": 7492,
    },
    "eighth": {
        "counts": (69268, 4219, 65049),
        "target": ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (3, 3, 5), 4, 2),
        "schema": "rank-seven-order-eight-eighth-induced-packet-gram-family-v1",
        "physical": 4656,
    },
    "ninth": {
        "counts": (65049, 3765, 61284),
        "target": ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (2, 3, 6), 4, 1),
        "schema": "rank-seven-order-eight-ninth-induced-packet-gram-family-v1",
        "physical": 3916,
    },
    "tenth": {
        "counts": (61284, 2731, 58553),
        "target": ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (1, 3, 7), 4, 2),
        "schema": "rank-seven-order-eight-tenth-induced-packet-gram-family-v1",
        "physical": 2968,
    },
    "eleventh": {
        "counts": (58553, 2167, 56386),
        "target": ((2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), (2, 2, 8), 5, 3),
        "schema": "rank-seven-order-eight-eleventh-induced-packet-gram-family-v1",
        "physical": 2275,
    },
    "twelfth": {
        "counts": (56386, 1788, 54598),
        "target": ((2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1), (2, 3, 6), 4, 3),
        "schema": "rank-seven-order-eight-twelfth-induced-packet-gram-family-v1",
        "physical": 1958,
    },
}
OWNER_FIELDS = {
    "global_kernel", "numerical_canonical_cost", "orbit_size", "source_index",
    "stream_index", "witness",
}
WITNESS_FIELDS = {"denominator", "branches", "canonical", "extended"}
BASE_PATH = EXPERIMENTS / "rank6_order10_cubic_exact_rational.py"
LANES_PATH = EXPERIMENTS / "rank7_order8_payload_free_lanes.py"
MANIFEST_PATH = EXPERIMENTS / "rank7_order8_exact_residual_census_manifest.json"
INDICES_PATH = EXPERIMENTS / "rank7_order8_rational_search_indices.json"
EXPECTED_RESIDUALS = 492812
EXPECTED_MANIFEST_SHA256 = "5d41e78a2f688f4c3064cb88f1d6d475008d36c84f892edc4cba28ade424fe98"
EXPECTED_INDICES_SHA256 = "245cceaab164ba9c2a604d0db8b09a65598fd52084b1df2363911c6d1d4d3a59"
EXPECTED_SIXTH_REPORT_SHA256 = "d396cc1070fde5422a5a07640314c4fcbe3ee970ade479d5c2bec781ba51f0e6"
EXPECTED_SIXTH_REMAINDER_SHA256 = "9e2827ef55df4046a14c0530fb401176dca4484a846cbc3c191d7e06b57e376f"

Json = Any
SourceRecord = list[Json]
Residual = tuple[Any, ...]
SourceEntry = tuple[SourceRecord, bytes, Residual]
Witness = tuple[
    int,
    tuple[tuple[Fraction, ...], ...],
    tuple[tuple[tuple[Fraction, ...], ...], ...],
    tuple[tuple[tuple[Fraction, ...], ...], ...],
]


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def is_exact_int(value: object) -> TypeGuard[int]:
    return type(value) is int


def exact_int(value: object, label: str, *, minimum: int | None = None) -> int:
    if not is_exact_int(value):
        fail(f"{label} is not an integer")
    if minimum is not None and value < minimum:
        fail(f"{label} is below {minimum}")
    return value


def exact_string(value: object, label: str) -> str:
    if type(value) is not str or not value:
        fail(f"{label} is not a nonempty string")
    return value


def exact_mapping(value: object, label: str) -> dict[str, Json]:
    if type(value) is not dict:
        fail(f"{label} is not an object")
    if not all(type(key) is str for key in value):
        fail(f"{label} has a non-string key")
    return value


def exact_list(value: object, label: str) -> list[Json]:
    if type(value) is not list:
        fail(f"{label} is not a list")
    return value


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_functions(path: Path, names: set[str], globals_: dict[str, object]) -> SimpleNamespace:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    definitions = [node for node in tree.body
                   if isinstance(node, ast.FunctionDef) and node.name in names]
    require({node.name for node in definitions} == names,
            f"exact verifier function set changed in {path.name}")
    namespace = dict(globals_)
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(path), "exec"), namespace)
    return SimpleNamespace(**{name: namespace[name] for name in names})


def load(ordinal: str) -> ModuleType:
    path = EXPERIMENTS / f"rank7_order8_{ordinal}_induced_packet_gram_family.py"
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    assignments = {node.targets[0].id: node.value for node in tree.body
                   if isinstance(node, ast.Assign) and len(node.targets) == 1 and
                   isinstance(node.targets[0], ast.Name)}
    wanted = {
        "SOURCE_REPORT", "SOURCE_STREAM", "OUTPUT", "OWNERS", "REMAINDER",
        "SCHEMA", "SOURCE_REMAINDER", "PREVIOUS_FAMILY_TOTAL", "TARGET",
        "EXPECTED_TARGET",
    }
    require(wanted <= set(assignments), f"{ordinal} lane constants changed")
    def constant(name: str) -> object:
        node = assignments[name]
        if (name in {"SOURCE_REPORT", "SOURCE_STREAM", "OUTPUT", "OWNERS", "REMAINDER"}
                and isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
                and isinstance(node.left, ast.Name) and node.left.id == "HERE"):
            relative = ast.literal_eval(node.right)
            require(type(relative) is str and Path(relative).name == relative,
                    f"{ordinal} {name} is not a safe artifact basename")
            return EXPERIMENTS / relative
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError) as error:
            raise RuntimeError(f"{ordinal} {name} is not a literal constant") from error

    values = {name: constant(name) for name in wanted}
    structural = load_functions(
        EXPERIMENTS / "rank7_order8_structural_cycle_gram_lane.py",
        {"require", "canonical_bytes", "strict_json", "family"},
        {"json": json, "ORDER": 8},
    )
    values["structural"] = structural
    values["lane"] = SimpleNamespace(
        canonical_bytes=structural.canonical_bytes,
        DENOMINATORS=(256, 1024, 4096, 16384, 65536),
    )
    module = ModuleType(f"audit_{ordinal}")
    for name, value in values.items():
        setattr(module, name, value)
    return module


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def safe_artifact_path(info: Mapping[str, Json], expected: Path, label: str) -> Path:
    name = exact_string(info.get("path"), f"{label}.path")
    require(Path(name).name == name, f"{label}.path is not a basename")
    path = EXPERIMENTS / name
    require(path == expected, f"{label}.path changed")
    require(path.is_file(), f"{label} is missing")
    return path


def canonical_report(module: ModuleType, ordinal: str) -> tuple[bytes, Mapping[str, Json]]:
    raw = module.OUTPUT.read_bytes()
    report = module.structural.strict_json(raw, module.OUTPUT.name)
    require(type(report) is dict, f"{ordinal} report is not an object")
    require(raw == module.lane.canonical_bytes(report), f"{ordinal} report noncanonical")
    return raw, report


def source_rows(module: ModuleType, path: Path, info: Mapping[str, Json],
                expected_total: int, label: str) -> Iterator[tuple[SourceRecord, bytes]]:
    require(file_sha256(path) == exact_string(info.get("artifact_sha256"),
                                               f"{label}.artifact_sha256"),
            f"{label} compressed digest changed")
    expected_raw = exact_string(info.get("raw_sha256"), f"{label}.raw_sha256")
    require(exact_int(info.get("record_total"), f"{label}.record_total", minimum=0) ==
            expected_total, f"{label} record count changed")
    digest = hashlib.sha256()
    total = 0
    try:
        with lzma.open(path, "rb") as stream:
            for raw in stream:
                payload = module.structural.strict_json(raw, path.name)
                record = exact_list(payload, f"{label} row {total}")
                require(len(record) == 6, f"{label} row {total} is not six fields")
                require(raw == module.lane.canonical_bytes(record),
                        f"{label} row {total} is noncanonical")
                digest.update(raw)
                total += 1
                yield record, raw
    except lzma.LZMAError as error:
        raise RuntimeError(f"{label} is not a valid XZ stream") from error
    require(total == expected_total and digest.hexdigest() == expected_raw,
            f"{label} raw identity changed")


def reconstructed_source(record: SourceRecord, residuals: Sequence[Residual],
                         census: ModuleType, label: str) -> tuple[int, Residual]:
    stream_index = exact_int(record[0], f"{label}.stream_index", minimum=0)
    require(stream_index < len(residuals), f"{label}.stream_index is out of range")
    source_index = exact_int(record[1], f"{label}.source_index", minimum=0)
    global_kernel = exact_int(record[2], f"{label}.global_kernel", minimum=0)
    edges_raw = exact_list(record[3], f"{label}.edges")
    row_raw = exact_list(record[4], f"{label}.row")
    orbit_size = exact_int(record[5], f"{label}.orbit_size", minimum=1)

    edges: list[tuple[int, int, int]] = []
    for edge_index, edge_raw in enumerate(edges_raw):
        edge = exact_list(edge_raw, f"{label}.edges[{edge_index}]")
        require(len(edge) == 3, f"{label}.edges[{edge_index}] is not a triple")
        u = exact_int(edge[0], f"{label}.edges[{edge_index}][0]", minimum=0)
        v = exact_int(edge[1], f"{label}.edges[{edge_index}][1]", minimum=0)
        multiplicity = exact_int(edge[2], f"{label}.edges[{edge_index}][2]", minimum=1)
        require(u < v < 8, f"{label}.edges[{edge_index}] has invalid endpoints")
        edges.append((u, v, multiplicity))
    require(all(left < right for left, right in zip(edges, edges[1:])),
            f"{label}.edges are not strictly ordered")
    row = tuple(exact_int(value, f"{label}.row[{index}]", minimum=0)
                for index, value in enumerate(row_raw))
    require(len(row) == len(edges) and
            all(odd <= edge[2] for edge, odd in zip(edges, row, strict=True)),
            f"{label}.row is not physical")

    residual = residuals[stream_index]
    support = tuple(census.PAIRS.index((u, v)) for u, v, _ in edges)
    rebuilt = (global_kernel, source_index, support,
               tuple(multiplicity for _, _, multiplicity in edges), row, orbit_size)
    require(residual[:6] == rebuilt, f"{label} differs from regenerated residual")
    require(residual[6] is None and residual[7] is False,
            f"{label} has unexpected regenerated metadata")
    return stream_index, residual


def fraction_rows(value: object, denominator: int, label: str) -> tuple[tuple[Fraction, ...], ...]:
    rows_raw = exact_list(value, label)
    rows: list[tuple[Fraction, ...]] = []
    for row_index, row_raw in enumerate(rows_raw):
        row_values = exact_list(row_raw, f"{label}[{row_index}]")
        require(len(row_values) == 7, f"{label}[{row_index}] has wrong dimension")
        numerators = tuple(exact_int(item, f"{label}[{row_index}][{column}]")
                           for column, item in enumerate(row_values))
        rows.append(tuple(Fraction(item, denominator) for item in numerators))
    return tuple(rows)


def decode_witness(value: object, allowed_denominators: Sequence[int], label: str) -> Witness:
    payload = exact_mapping(value, label)
    require(set(payload) == WITNESS_FIELDS, f"{label} fields changed")
    denominator = exact_int(payload.get("denominator"), f"{label}.denominator", minimum=1)
    require(denominator in allowed_denominators, f"{label}.denominator is unexpected")
    branches = fraction_rows(payload.get("branches"), denominator, f"{label}.branches")
    canonical_raw = exact_list(payload.get("canonical"), f"{label}.canonical")
    extended_raw = exact_list(payload.get("extended"), f"{label}.extended")
    require(len(branches) == 8 and len(canonical_raw) == len(extended_raw) == 14,
            f"{label} packet dimensions changed")
    canonical = tuple(fraction_rows(path, denominator, f"{label}.canonical[{index}]")
                      for index, path in enumerate(canonical_raw))
    extended = tuple(fraction_rows(path, denominator, f"{label}.extended[{index}]")
                     for index, path in enumerate(extended_raw))
    return denominator, branches, canonical, extended


def owner_rows(module: ModuleType, path: Path, info: Mapping[str, Json],
               expected_total: int, source_by_index: Mapping[int, SourceEntry],
               census: ModuleType, engine: ModuleType, ordinal: str) -> set[int]:
    require(file_sha256(path) == exact_string(info.get("artifact_sha256"),
                                               f"{ordinal} owner artifact_sha256"),
            f"{ordinal} owner compressed digest changed")
    expected_raw = exact_string(info.get("raw_sha256"),
                                f"{ordinal} owner raw_sha256")
    require(exact_int(info.get("record_total"), f"{ordinal} owner record_total", minimum=0) ==
            expected_total, f"{ordinal} owner record count changed")

    digest = hashlib.sha256()
    seen: set[int] = set()
    total = 0
    try:
        with lzma.open(path, "rb") as stream:
            for raw in stream:
                value = module.structural.strict_json(raw, path.name)
                owner = exact_mapping(value, f"{ordinal} owner row {total}")
                require(raw == module.lane.canonical_bytes(owner),
                        f"{ordinal} owner row {total} is noncanonical")
                require(set(owner) == OWNER_FIELDS, f"{ordinal} owner row {total} fields changed")
                stream_index = exact_int(owner.get("stream_index"),
                                         f"{ordinal} owner row {total}.stream_index", minimum=0)
                require(stream_index not in seen, f"{ordinal} owner index is duplicated")
                require(stream_index in source_by_index,
                        f"{ordinal} owner escaped its authenticated source")
                source_record, _, residual = source_by_index[stream_index]
                require(exact_int(owner.get("source_index"),
                                  f"{ordinal} owner row {total}.source_index", minimum=0) ==
                        source_record[1] and
                        exact_int(owner.get("global_kernel"),
                                  f"{ordinal} owner row {total}.global_kernel", minimum=0) ==
                        source_record[2] and
                        exact_int(owner.get("orbit_size"),
                                  f"{ordinal} owner row {total}.orbit_size", minimum=1) ==
                        source_record[5],
                        f"{ordinal} owner metadata differs from its source row")
                numerical = owner.get("numerical_canonical_cost")
                require(type(numerical) is float and math.isfinite(numerical),
                        f"{ordinal} owner numerical provenance is malformed")
                family = module.structural.family(tuple(map(tuple, source_record[3])),
                                                  tuple(source_record[4]))
                require(family == module.TARGET,
                        f"{ordinal} owner is outside the exact target family")
                witness = decode_witness(owner.get("witness"), module.lane.DENOMINATORS,
                                         f"{ordinal} owner row {total}.witness")
                engine.base.verify_shared(census, residual, witness)
                digest.update(raw)
                seen.add(stream_index)
                total += 1
    except lzma.LZMAError as error:
        raise RuntimeError(f"{ordinal} owner stream is not valid XZ") from error
    require(total == expected_total and len(seen) == expected_total and
            digest.hexdigest() == expected_raw,
            f"{ordinal} owner raw identity changed")
    return seen


def verify_lane(module: ModuleType, ordinal: str, source_path: Path,
                source_info: Mapping[str, Json], census: ModuleType,
                residuals: Sequence[Residual], engine: ModuleType) -> Path:
    contract = EXPECTED[ordinal]
    source_total, owner_total, remainder_total = contract["counts"]
    require(module.SOURCE_STREAM == source_path,
            f"{ordinal} does not chain from the previous remainder")
    require(module.TARGET == contract["target"] and
            module.EXPECTED_TARGET == owner_total and
            module.SCHEMA == contract["schema"],
            f"{ordinal} wrapper contract changed")
    report_raw, report = canonical_report(module, ordinal)
    require(report.get("schema") == contract["schema"] and report.get("full_theorem") is True,
            f"{ordinal} theorem report identity changed")
    expected_target_report = {
        "dominance_rank": 1,
        "multiplicity_partition": list(contract["target"][0]),
        "bundle_types": list(contract["target"][1]),
        "cycle_rank": contract["target"][2],
        "triangle_total": contract["target"][3],
        "orbit_total": owner_total,
        "physical_total": contract["physical"],
        "scanned_total": owner_total,
    }
    require(report.get("target_family") == expected_target_report,
            f"{ordinal} target-family report changed")
    require(exact_int(report.get("scanned_remainder_total"),
                      f"{ordinal}.scanned_remainder_total", minimum=0) == source_total and
            exact_int(report.get("owned_orbit_total"),
                      f"{ordinal}.owned_orbit_total", minimum=0) == owner_total and
            exact_int(report.get("owned_target_total"),
                      f"{ordinal}.owned_target_total", minimum=0) == 15 * owner_total and
            exact_int(report.get("owned_physical_total"),
                      f"{ordinal}.owned_physical_total", minimum=0) == contract["physical"] and
            exact_int(report.get("remaining_target_family_total"),
                      f"{ordinal}.remaining_target_family_total", minimum=0) == 0 and
            exact_int(report.get("remaining_remainder_total"),
                      f"{ordinal}.remaining_remainder_total", minimum=0) == remainder_total,
            f"{ordinal} theorem counts changed")
    require(source_total == owner_total + remainder_total,
            f"{ordinal} partition arithmetic changed")

    source_report = exact_mapping(report.get("source_report"), f"{ordinal}.source_report")
    require(set(source_report) == {"path", "sha256"} and
            source_report.get("path") == module.SOURCE_REPORT.name and
            source_report.get("sha256") == hashlib.sha256(
                module.SOURCE_REPORT.read_bytes()).hexdigest(),
            f"{ordinal} source report changed")
    report_source_info = exact_mapping(report.get("source_stream"),
                                       f"{ordinal}.source_stream")
    require(report_source_info == source_info,
            f"{ordinal} source-stream metadata does not chain exactly")
    safe_artifact_path(report_source_info, source_path, f"{ordinal}.source_stream")

    source_order: list[int] = []
    source_by_index: dict[int, SourceEntry] = {}
    for position, (record, raw) in enumerate(source_rows(
            module, source_path, report_source_info, source_total, f"{ordinal} source")):
        stream_index, residual = reconstructed_source(
            record, residuals, census, f"{ordinal} source row {position}")
        require(stream_index not in source_by_index,
                f"{ordinal} source contains a duplicate stream index")
        source_order.append(stream_index)
        source_by_index[stream_index] = (record, raw, residual)
    require(len(source_by_index) == source_total,
            f"{ordinal} source indices are not unique")

    owner_info = exact_mapping(report.get("owner_stream"), f"{ordinal}.owner_stream")
    owner_path = safe_artifact_path(owner_info, module.OWNERS, f"{ordinal}.owner_stream")
    owners = owner_rows(module, owner_path, owner_info, owner_total,
                        source_by_index, census, engine, ordinal)
    target_indices = {
        index for index, (record, _, _) in source_by_index.items()
        if module.structural.family(tuple(map(tuple, record[3])), tuple(record[4])) ==
        module.TARGET
    }
    require(owners == target_indices and len(target_indices) == owner_total,
            f"{ordinal} owners are not exactly the target family")
    require(sum(source_by_index[index][0][5] for index in owners) == contract["physical"],
            f"{ordinal} authenticated owner physical total changed")
    classification = hashlib.sha256()
    for index in source_order:
        record = source_by_index[index][0]
        if index in target_indices:
            classification.update(module.lane.canonical_bytes(
                [index, record[1], index in owners]))
    require(classification.hexdigest() == exact_string(
        report.get("classification_stream_sha256"),
        f"{ordinal}.classification_stream_sha256"),
        f"{ordinal} owner classification stream changed")

    remainder_info = exact_mapping(report.get("reduced_remainder_stream"),
                                   f"{ordinal}.reduced_remainder_stream")
    remainder_path = safe_artifact_path(remainder_info, module.REMAINDER,
                                        f"{ordinal}.reduced_remainder_stream")
    expected = ((source_by_index[index][0], source_by_index[index][1])
                for index in source_order if index not in owners)
    observed = source_rows(module, remainder_path, remainder_info, remainder_total,
                           f"{ordinal} remainder")
    compared = 0
    for compared, ((expected_record, expected_raw), (actual_record, actual_raw)) in enumerate(
            zip(expected, observed, strict=True), 1):
        require(actual_raw == expected_raw and actual_record == expected_record,
                f"{ordinal} remainder row {compared - 1} is not the byte-for-byte complement")
    require(compared == remainder_total,
            f"{ordinal} remainder complement count changed")
    require(report_raw == module.OUTPUT.read_bytes(),
            f"{ordinal} report changed during read-only verification")
    return remainder_path


def load_exact_engine() -> SimpleNamespace:
    base = load_module("rank7_order8_chain_base", BASE_PATH)
    base.ORDER = base.DIMENSION = 8
    base.PATH_COUNT = 14
    base.BUDGET = Fraction(6)
    return SimpleNamespace(
        base=base,
        lanes=load_module("rank7_order8_chain_lanes", LANES_PATH),
    )


def regenerated_residuals(engine: SimpleNamespace) -> tuple[SimpleNamespace, tuple[Residual, ...]]:
    pairs = tuple((u, v) for u in range(8) for v in range(u + 1, 8))
    census = SimpleNamespace(PAIRS=pairs)
    manifest, manifest_digest = engine.lanes.load_manifest(MANIFEST_PATH)
    require(manifest_digest == EXPECTED_MANIFEST_SHA256, "residual manifest changed")
    indices_raw = INDICES_PATH.read_bytes()
    require(hashlib.sha256(indices_raw).hexdigest() == EXPECTED_INDICES_SHA256,
            "rational-search index artifact changed")
    indices_payload = engine.lanes.strict_json(indices_raw, INDICES_PATH.name)
    require(indices_raw == engine.lanes.canonical_bytes(indices_payload),
            "noncanonical rational-search indices")
    require(type(indices_payload) is dict and set(indices_payload) == {
        "schema", "manifest_sha256", "selected_chunks", "source_indices"
    } and indices_payload.get("schema") ==
        "rank-seven-order-eight-rational-search-indices-v1" and
        indices_payload.get("manifest_sha256") == manifest_digest and
        indices_payload.get("selected_chunks") == list(range(8)),
        "wrong rational-search index scope")
    wanted_raw = exact_list(indices_payload.get("source_indices"), "source_indices")
    wanted = tuple(exact_int(value, f"source_indices[{index}]", minimum=0)
                   for index, value in enumerate(wanted_raw))
    require(len(wanted) == EXPECTED_RESIDUALS and
            all(left < right for left, right in zip(wanted, wanted[1:])),
            "rational-search indices changed")

    pair_index = {edge: index for index, edge in enumerate(pairs)}
    residuals: list[Residual] = []
    wanted_position = 0
    source_offset = 0
    for chunk_record_raw in exact_list(manifest.get("chunks"), "manifest.chunks"):
        chunk_record = exact_mapping(chunk_record_raw, "manifest chunk")
        chunk_path = (MANIFEST_PATH.parent / exact_string(
            chunk_record.get("path"), "manifest chunk.path")).resolve()
        require(chunk_path.parent == MANIFEST_PATH.parent.resolve(),
                "residual chunk escaped the experiment directory")
        chunk = engine.lanes.read_chunk(chunk_path, chunk_record)
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
        source_offset += exact_int(chunk_record.get("coarse_residual_total"),
                                   "chunk coarse_residual_total", minimum=0)
    require(wanted_position == len(wanted) and len(residuals) == EXPECTED_RESIDUALS,
            "rational-search stream materialization changed")
    return census, tuple(residuals)


def main() -> None:
    modules = {ordinal: load(ordinal) for ordinal in ORDINALS}
    engine = load_exact_engine()
    # Regenerate from authenticated source chunks; do not trust the convenience cache.
    census, residuals = regenerated_residuals(engine)

    sixth = load("sixth")
    sixth_raw, sixth_report = canonical_report(sixth, "sixth")
    require(hashlib.sha256(sixth_raw).hexdigest() == EXPECTED_SIXTH_REPORT_SHA256,
            "sixth trust-root report changed")
    sixth_info = exact_mapping(sixth_report.get("reduced_remainder_stream"),
                               "sixth.reduced_remainder_stream")
    source_path = safe_artifact_path(sixth_info, sixth.REMAINDER,
                                     "sixth.reduced_remainder_stream")
    require(sixth_report.get("full_theorem") is True and
            sixth_report.get("remaining_remainder_total") ==
            EXPECTED["seventh"]["counts"][0] and
            sixth_info.get("record_total") == EXPECTED["seventh"]["counts"][0] and
            sixth_info.get("artifact_sha256") == EXPECTED_SIXTH_REMAINDER_SHA256 and
            file_sha256(source_path) == EXPECTED_SIXTH_REMAINDER_SHA256,
            "sixth source closure changed")
    require(sixth_raw == sixth.OUTPUT.read_bytes(),
            "sixth report changed during read-only verification")

    source_info = sixth_info
    for ordinal in ORDINALS:
        module = modules[ordinal]
        source_path = verify_lane(module, ordinal, source_path, source_info,
                                  census, residuals, engine)
        _, report = canonical_report(module, ordinal)
        source_info = exact_mapping(report.get("reduced_remainder_stream"),
                                    f"{ordinal}.reduced_remainder_stream")
    print("rank7 order8 packet chain exact Fraction audit: PASS")


if __name__ == "__main__":
    main()
