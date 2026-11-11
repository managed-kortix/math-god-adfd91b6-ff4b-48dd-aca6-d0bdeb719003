#!/usr/bin/env python3
"""Read-only exact bridge from base owners to the 83,856-row boundary stream.

This verifier closes an authentication gap between three independently stored
layers of the rank-seven/order-eight computation:

* the twenty typed-diagonal receipt bitmaps;
* the precedence-exclusive base-owner index artifact; and
* the exact shared-Gram boundary rescue and its 83,856-row complement.

Only Python's standard library is used.  No search is rerun and no file is
written.  The checks are exact: strict canonical JSON, exact hashes, set
identities, and Fraction replay of every boundary shared-Gram witness.  The
receipts are semantically validated as receipts, but their underlying 492,812
row searches are not rerun here; that expensive replay is a separate theorem
gate dependency and is reported explicitly rather than laundered as part of
this bridge.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import lzma
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
RECEIPT_DIR = HERE / "rank7_order8_typed_diagonal_receipts"
CACHE_PATH = HERE / "rank7_order8_rational_search_cache.r7o8c.xz"
PAYLOAD_REPORT_PATH = HERE / "rank7_order8_payload_free_lane_coverage.json"
SCALAR_REPORT_PATH = HERE / "rank7_order8_parametric_gram_ansatz_coverage.json"
TYPED_REPORT_PATH = HERE / "rank7_order8_typed_diagonal_gram_coverage.json"
TYPED_ACCOUNTING_PATH = HERE / "rank7_order8_combined_owner_accounting.json"
BASE_LEDGER_PATH = HERE / "rank7_order8_combined_owner_ledger.json"
INDICES_PATH = HERE / "rank7_order8_combined_owner_indices.json.xz"
FINITE_OWNERS_PATH = HERE / "rank7_order8_packet_spectral_owners.json.xz"
BOUNDARY_OWNERS_PATH = HERE / "rank7_order8_theorem_dnn_owners.json.xz"
BOUNDARY_LEDGER_PATH = HERE / "rank7_order8_theorem_eligible_combined_ledger.json"
BOUNDARY_REMAINDER_PATH = HERE / "rank7_order8_after_packet_spectral_remainder.jsonl.xz"

SOURCE_SHA256 = "53c64c930846c92d8a4f35e5c228c60afb4c56c1a35009cfec60eaf2ffba6ee3"
CACHE_STORED_SHA256 = "0e31fb87d7bfa8e01d8cf168240cb2cc164673628f2c22b9e14347186cea7502"
CACHE_RAW_SHA256 = "b56459cb832370340c7d44c1dca77e97adb59192f9f2703df739f048c25e3d30"
PAYLOAD_REPORT_SHA256 = "0f7f2f495cb0755f4e89d5aa81ad6e11f53d4130c300c8ee74a283333831370f"
SCALAR_REPORT_SHA256 = "57bd9da7d1483f6132a3cf54f15bf18b4733c74a384395585cc208b876d3b6fe"
TYPED_REPORT_SHA256 = "88fc494d52a824354368153a1b6cd2f88db12d7a330f67cbc728aac5308c53bd"
TYPED_ACCOUNTING_SHA256 = "ed13ec5f8cacaefd3a0dca00a06635dcdcee2c010e2b8eea2582ce8e77f1e314"
BASE_LEDGER_SHA256 = "5700803dd3989853440291423a6cae736978125cbcf3a13ffa89281e7b5ea84e"
INDICES_STORED_SHA256 = "1dacaf02fc546c634ba879bdd1af49774040d963e09a40331bba77bdff50c6d5"
INDICES_RAW_SHA256 = "5126acb54fc67f639e0bc3b158825a3ca68bfe480432a9d75046e26117191d82"
BOUNDARY_LEDGER_SHA256 = "69199fccf20574a133ffa605833b9abfecf692cae816571f25b50a4f986a233d"
BOUNDARY_OWNERS_STORED_SHA256 = "55e354cd9db5c91a6e5926d199c392194c03b27f1bed1fac586055b41f26ecd5"
BOUNDARY_OWNERS_RAW_SHA256 = "c821ff7994b6502a917db69aed9ef874ba12d976c13c2a20113949f97e5d44d7"
BOUNDARY_REMAINDER_STORED_SHA256 = "cc5ce720adb8d4ea650544dca5846462675d97433af9016313fce68e781e249b"
BOUNDARY_REMAINDER_RAW_SHA256 = "210d2ad2beb19e251c3e9095c169d57a5941fc147e7cdc3d90390607f4408724"

RECEIPT_SCHEMA = "rank-seven-order-eight-typed-diagonal-segment-receipt-v1"
BASE_LEDGER_SCHEMA = "rank-seven-order-eight-combined-owner-ledger-v1"
ACCOUNTING_SCHEMA = "rank-seven-order-eight-combined-owner-accounting-v1"
PAYLOAD_SCHEMA = "rank-seven-order-eight-payload-free-lane-coverage-v1"
SCALAR_SCHEMA = "rank-seven-order-eight-parametric-gram-ansatz-v1"
TYPED_SCHEMA = "rank-seven-order-eight-typed-diagonal-gram-lane-v1"
CACHE_MAGIC = b"R7O8C1"
ROW_TOTAL = 492_812
COARSE_TOTAL = 493_417
PAYLOAD_TOTAL = 605
TARGETS_PER_ROW = 15
TYPED_RAW_TOTAL = 402_712
SCALAR_RAW_TOTAL = 204_766
BOUNDARY_RESCUE_TOTAL = 296
BOUNDARY_REMAINDER_TOTAL = 83_856
ORDER = 8
PATH_COUNT = 14
BUDGET = Fraction(6)
EXPECTED_PRECEDENCE = ["payload-free", "direct-rational", "scalar-sos", "typed-diagonal"]
EXPECTED_EXCLUSIVE = {
    "direct-rational": 29_000,
    "scalar-sos": 194_351,
    "typed-diagonal": 185_309,
    "remaining": 84_152,
}
EXPECTED_RECEIPT_SEARCH = {
    "coordinate_passes": 3,
    "d0_scales": [[1, 2], [2, 3], [1, 1], [3, 2], [2, 1]],
    "maximum": 4,
    "maximum_denominator": 8,
}
EXPECTED_PROOF_CONTRACT = {
    "costs": "canonical and fourteen length-plus-two targets checked with Fraction",
    "gram": "XX^T/M plus diag(1-diag(XX^T)/M)",
    "psd": "exact rational Gram factor plus exact nonnegative diagonal completion",
}
EXPECTED_RECEIPT_KEYS = {
    "schema", "source_stream_sha256", "row_range", "row_total",
    "first_source_index", "last_source_index", "search", "verified",
    "typed_owner_total", "unowned_total", "ownership_bitmap_base64",
    "ownership_bitmap_sha256", "coverage_stream_sha256",
    "full_classification_segment_sha256", "proof_contract",
}
F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def is_int(value):
    return type(value) is int


def is_hex(value, length=64):
    return (type(value) is str and len(value) == length and
            all(character in "0123456789abcdef" for character in value))


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       allow_nan=False) + "\n").encode("ascii")


def strict_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(type(key) is str, f"{label}: non-string JSON key")
            require(key not in result, f"{label}: duplicate key {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                RuntimeError(f"{label}: nonstandard constant {value}")),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: cannot parse strict ASCII JSON") from error


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def read_canonical_json(path, expected_sha256=None, compressed=False):
    stored = path.read_bytes()
    if expected_sha256 is not None:
        require(sha256(stored) == expected_sha256,
                f"{path.name}: stored SHA-256 changed")
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ) if compressed else stored
    except lzma.LZMAError as error:
        raise RuntimeError(f"{path.name}: invalid XZ stream") from error
    payload = strict_json(raw, path.name)
    require(raw == canonical_bytes(payload), f"{path.name}: noncanonical JSON")
    return payload, sha256(raw), sha256(stored)


def read_jsonl(path, expected_stored_sha256=None, expected_raw_sha256=None):
    stored = path.read_bytes()
    if expected_stored_sha256 is not None:
        require(sha256(stored) == expected_stored_sha256,
                f"{path.name}: stored SHA-256 changed")
    records = []
    digest = hashlib.sha256()
    try:
        with lzma.open(path, "rb") as stream:
            for line_number, raw in enumerate(stream, 1):
                record = strict_json(raw, f"{path.name}:{line_number}")
                require(raw == canonical_bytes(record),
                        f"{path.name}:{line_number}: noncanonical JSONL record")
                records.append(record)
                digest.update(raw)
    except lzma.LZMAError as error:
        raise RuntimeError(f"{path.name}: invalid XZ stream") from error
    raw_digest = digest.hexdigest()
    if expected_raw_sha256 is not None:
        require(raw_digest == expected_raw_sha256,
                f"{path.name}: raw JSONL SHA-256 changed")
    return records, raw_digest, sha256(stored)


def get_uvarint(raw, position):
    value = 0
    shift = 0
    while True:
        require(position < len(raw) and shift <= 63,
                "census cache: truncated or overlong unsigned varint")
        byte = raw[position]
        position += 1
        value |= (byte & 0x7f) << shift
        if byte < 0x80:
            require(shift == 0 or byte != 0,
                    "census cache: noncanonical unsigned varint")
            return value, position
        shift += 7


def decode_cache(path):
    stored = path.read_bytes()
    require(sha256(stored) == CACHE_STORED_SHA256,
            "rational-search cache: stored SHA-256 changed")
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError("rational-search cache: invalid XZ stream") from error
    require(sha256(raw) == CACHE_RAW_SHA256,
            "rational-search cache: raw SHA-256 changed")
    header = len(CACHE_MAGIC)
    require(raw[:header] == CACHE_MAGIC and
            raw[header:header + 32] == bytes.fromhex(SOURCE_SHA256),
            "rational-search cache: wrong magic or source identity")
    digest_start = header + 32
    payload_start = digest_start + 32
    require(raw[digest_start:payload_start] == hashlib.sha256(raw[payload_start:]).digest(),
            "rational-search cache: payload digest changed")
    position = payload_start
    count, position = get_uvarint(raw, position)
    require(count == ROW_TOTAL, "rational-search cache: wrong row total")
    pairs = tuple((u, v) for u in range(ORDER) for v in range(u + 1, ORDER))
    rows = []
    previous_source = -1
    for stream_index in range(count):
        global_kernel, position = get_uvarint(raw, position)
        source_index, position = get_uvarint(raw, position)
        width, position = get_uvarint(raw, position)
        support = []
        multiplicities = []
        odd_counts = []
        for _ in range(width):
            dense, position = get_uvarint(raw, position)
            multiplicity, position = get_uvarint(raw, position)
            odd, position = get_uvarint(raw, position)
            require(dense < len(pairs) and multiplicity > 0 and odd <= multiplicity,
                    "rational-search cache: nonphysical row")
            support.append(dense)
            multiplicities.append(multiplicity)
            odd_counts.append(odd)
        orbit_size, position = get_uvarint(raw, position)
        require(source_index > previous_source and orbit_size > 0 and
                all(left < right for left, right in zip(support, support[1:])) and
                sum(multiplicities) == PATH_COUNT,
                "rational-search cache: noncanonical row")
        previous_source = source_index
        rows.append((stream_index, global_kernel, source_index, tuple(support),
                     tuple(multiplicities), tuple(odd_counts), orbit_size))
    require(position == len(raw), "rational-search cache: trailing bytes")
    return tuple(rows), pairs


def bitmap_decode(encoded, count):
    require(type(encoded) is str and is_int(count) and count >= 0,
            "receipt bitmap: wrong field type")
    try:
        raw = base64.b64decode(encoded.encode("ascii"), validate=True)
    except (UnicodeEncodeError, ValueError) as error:
        raise RuntimeError("receipt bitmap: invalid base64") from error
    require(len(raw) == (count + 7) // 8,
            "receipt bitmap: wrong byte length")
    if count % 8:
        require(raw[-1] >> (count % 8) == 0,
                "receipt bitmap: nonzero padding")
    values = tuple(bool(raw[index // 8] & (1 << (index % 8)))
                   for index in range(count))
    return raw, values


def validate_receipts(rows):
    paths = sorted(RECEIPT_DIR.glob("receipt-*.json"))
    require(len(paths) == 20, "typed receipts: expected exactly twenty files")
    records = []
    for path in paths:
        receipt, digest, _ = read_canonical_json(path)
        require(set(receipt) == EXPECTED_RECEIPT_KEYS,
                f"{path.name}: receipt schema keys changed")
        require(receipt["schema"] == RECEIPT_SCHEMA and
                receipt["source_stream_sha256"] == SOURCE_SHA256 and
                receipt["search"] == EXPECTED_RECEIPT_SEARCH and
                receipt["proof_contract"] == EXPECTED_PROOF_CONTRACT,
                f"{path.name}: receipt scope or proof contract changed")
        row_range = receipt["row_range"]
        require(type(row_range) is list and len(row_range) == 2 and
                all(is_int(value) for value in row_range),
                f"{path.name}: malformed row range")
        start, stop = row_range
        count = stop - start
        require(0 <= start < stop <= len(rows) and
                is_int(receipt["row_total"]) and receipt["row_total"] == count and
                is_int(receipt["first_source_index"]) and
                is_int(receipt["last_source_index"]) and
                (receipt["first_source_index"], receipt["last_source_index"]) ==
                (rows[start][2], rows[stop - 1][2]),
                f"{path.name}: receipt range identity changed")
        verified = receipt["verified"]
        require(verified == {
            "exact_frontier_cost_total": count * TARGETS_PER_ROW,
            "exact_psd_decomposition_rows": count,
            "rational_feature_formula_rows": count,
        }, f"{path.name}: exact-verification counts changed")
        bitmap_raw, values = bitmap_decode(receipt["ownership_bitmap_base64"], count)
        require(is_hex(receipt["ownership_bitmap_sha256"]) and
                sha256(bitmap_raw) == receipt["ownership_bitmap_sha256"],
                f"{path.name}: bitmap digest changed")
        owner_total = sum(values)
        require(is_int(receipt["typed_owner_total"]) and
                is_int(receipt["unowned_total"]) and
                receipt["typed_owner_total"] == owner_total and
                receipt["unowned_total"] == count - owner_total and
                is_hex(receipt["coverage_stream_sha256"]) and
                is_hex(receipt["full_classification_segment_sha256"]),
                f"{path.name}: receipt count or digest field changed")
        coverage = hashlib.sha256()
        for offset, accepted in enumerate(values):
            index = start + offset
            coverage.update(canonical_bytes([index, rows[index][2], accepted]))
        require(coverage.hexdigest() == receipt["coverage_stream_sha256"],
                f"{path.name}: coverage stream digest changed")
        records.append((start, stop, values, path.name, digest, owner_total))
    records.sort()
    require(records[0][0] == 0 and records[-1][1] == len(rows) and
            all(left[1] == right[0] for left, right in zip(records, records[1:])),
            "typed receipts: ranges are not a gap-free full partition")
    typed = set()
    coverage = hashlib.sha256()
    ledger = []
    for start, stop, values, name, digest, owner_total in records:
        for offset, accepted in enumerate(values):
            index = start + offset
            coverage.update(canonical_bytes([index, rows[index][2], accepted]))
            if accepted:
                typed.add(index)
        ledger.append({"path": name, "row_range": [start, stop],
                       "sha256": digest, "typed_owner_total": owner_total})
    require(len(typed) == TYPED_RAW_TOTAL,
            "typed receipts: raw owner total changed")
    return frozenset(typed), coverage.hexdigest(), ledger


def canonical_index_set(values, label):
    require(type(values) is list and all(is_int(value) for value in values) and
            values == sorted(values) and len(values) == len(set(values)) and
            all(0 <= value < ROW_TOTAL for value in values),
            f"combined indices: malformed {label} list")
    return frozenset(values)


def read_integer_vector(value, denominator, label):
    require(type(value) is list and len(value) == ORDER - 1 and
            all(is_int(component) for component in value),
            f"{label}: malformed stereographic vector")
    return tuple(F(component, denominator) for component in value)


def rational_unit(parameters):
    norm = sum(value * value for value in parameters)
    denominator = 1 + norm
    return tuple([F(1) - norm, *(2 * value for value in parameters)][index] / denominator
                 for index in range(ORDER))


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), F())


def exact_step_cost(left, right):
    correlation = dot(left, right)
    require(-1 < correlation <= 1,
            "boundary witness: antipodal or invalid adjacent vectors")
    return (1 - correlation) / (1 + correlation)


def canonical_lengths(multiplicity, odd):
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(row):
    paths = []
    for sparse, (dense, multiplicity, odd) in enumerate(
            zip(row[3], row[4], row[5], strict=True)):
        u, v = PAIRS[dense]
        paths.extend((sparse, occurrence, u, v, length)
                     for occurrence, length in enumerate(
                         canonical_lengths(multiplicity, odd)))
    require(len(paths) == PATH_COUNT, "boundary witness: path count changed")
    return tuple(paths)


def decode_shared_witness(payload, label):
    require(type(payload) is dict and set(payload) == {
        "branches", "canonical", "denominator", "extended"
    }, f"{label}: witness keys changed")
    denominator = payload["denominator"]
    require(is_int(denominator) and denominator in (256, 1024, 4096, 16384, 65536),
            f"{label}: unexpected shared denominator")
    branches = payload["branches"]
    canonical = payload["canonical"]
    extended = payload["extended"]
    require(type(branches) is list and len(branches) == ORDER and
            type(canonical) is list and len(canonical) == PATH_COUNT and
            type(extended) is list and len(extended) == PATH_COUNT,
            f"{label}: wrong witness dimensions")
    branch_rows = tuple(read_integer_vector(value, denominator, f"{label}: branch")
                        for value in branches)
    canonical_rows = tuple(
        tuple(read_integer_vector(value, denominator, f"{label}: canonical")
              for value in path) if type(path) is list else
        (_ for _ in ()).throw(RuntimeError(f"{label}: malformed canonical path"))
        for path in canonical)
    extended_rows = tuple(
        tuple(read_integer_vector(value, denominator, f"{label}: extended")
              for value in path) if type(path) is list else
        (_ for _ in ()).throw(RuntimeError(f"{label}: malformed extended path"))
        for path in extended)
    return denominator, branch_rows, canonical_rows, extended_rows


def verify_shared_witness(row, payload, label):
    _, branch_parameters, canonical, extended = decode_shared_witness(payload, label)
    branches = tuple(rational_unit(value) for value in branch_parameters)
    paths = path_ledger(row)
    target_costs = []
    for frontier in (None, *range(PATH_COUNT)):
        total = F()
        for index, ((_, _, u, v, length), base, longer) in enumerate(
                zip(paths, canonical, extended, strict=True)):
            parameters = longer if index == frontier else base
            expected_width = length - 1 + (2 if index == frontier else 0)
            require(len(parameters) == expected_width,
                    f"{label}: path parameter width changed")
            endpoint = branches[v] if length % 2 == 0 else tuple(-x for x in branches[v])
            chain = [branches[u], *(rational_unit(item) for item in parameters), endpoint]
            edge_total = length + (2 if index == frontier else 0)
            require(len(chain) == edge_total + 1,
                    f"{label}: reconstructed chain width changed")
            total += sum((exact_step_cost(chain[step], chain[step + 1])
                          for step in range(edge_total)), F())
        require(total <= BUDGET, f"{label}: exact target cost exceeds six")
        target_costs.append(total)
    require(len(target_costs) == TARGETS_PER_ROW,
            f"{label}: wrong frontier target total")
    return tuple(target_costs)


def validate_base_bridge(rows, typed_raw, typed_coverage, receipt_ledger):
    payload, _, _ = read_canonical_json(PAYLOAD_REPORT_PATH, PAYLOAD_REPORT_SHA256)
    scalar, _, _ = read_canonical_json(SCALAR_REPORT_PATH, SCALAR_REPORT_SHA256)
    typed_report, _, _ = read_canonical_json(TYPED_REPORT_PATH, TYPED_REPORT_SHA256)
    accounting, accounting_raw, _ = read_canonical_json(
        TYPED_ACCOUNTING_PATH, TYPED_ACCOUNTING_SHA256)
    ledger, ledger_raw, _ = read_canonical_json(BASE_LEDGER_PATH, BASE_LEDGER_SHA256)
    indices, indices_raw, indices_stored = read_canonical_json(
        INDICES_PATH, INDICES_STORED_SHA256, compressed=True)
    require(indices_raw == INDICES_RAW_SHA256,
            "combined indices: raw SHA-256 changed")
    require(payload.get("schema") == PAYLOAD_SCHEMA and
            payload.get("full_theorem") is False and
            payload.get("scanned_residual_total") == COARSE_TOTAL and
            payload.get("recognized_residual_total") == PAYLOAD_TOTAL and
            payload.get("rational_search_residual_total") == ROW_TOTAL and
            scalar.get("schema") == SCALAR_SCHEMA and
            scalar.get("full_theorem") is False and
            scalar.get("source_stream_sha256") == SOURCE_SHA256 and
            scalar.get("scanned_residual_total") == ROW_TOTAL and
            scalar.get("covered_residual_total") == SCALAR_RAW_TOTAL and
            typed_report.get("schema") == TYPED_SCHEMA and
            typed_report.get("full_theorem") is False and
            typed_report.get("source_stream_sha256") == SOURCE_SHA256 and
            typed_report.get("scanned_residual_total") == ROW_TOTAL and
            typed_report.get("covered_residual_total") == TYPED_RAW_TOTAL,
            "base reports: scope or raw owner counts changed")
    require(accounting_raw == TYPED_ACCOUNTING_SHA256 and
            accounting.get("schema") == ACCOUNTING_SCHEMA and
            accounting.get("full_theorem") is False and
            accounting.get("source_stream_sha256") == SOURCE_SHA256 and
            accounting.get("segment_receipts") == receipt_ledger and
            accounting.get("typed_coverage_stream_sha256") == typed_coverage and
            accounting.get("typed_full_scan_report_sha256") == TYPED_REPORT_SHA256 and
            accounting.get("combined_owned_residual_total") == PAYLOAD_TOTAL + TYPED_RAW_TOTAL and
            accounting.get("remaining_residual_total") == ROW_TOTAL - TYPED_RAW_TOTAL,
            "typed accounting: receipt bridge changed")
    require(ledger_raw == BASE_LEDGER_SHA256 and
            ledger.get("schema") == BASE_LEDGER_SCHEMA and
            ledger.get("full_theorem") is False and
            ledger.get("source_stream_sha256") == SOURCE_SHA256 and
            ledger.get("owner_precedence") == EXPECTED_PRECEDENCE and
            ledger.get("combined_indices") == {
                "path": INDICES_PATH.name, "raw_sha256": indices_raw,
                "xz_sha256": indices_stored,
            } and ledger.get("authenticated_inputs") == {
                "payload-free-report": PAYLOAD_REPORT_SHA256,
                "scalar-sos-report": SCALAR_REPORT_SHA256,
                "typed-diagonal-report": TYPED_REPORT_SHA256,
            }, "base ledger: artifact links or precedence changed")
    require(indices.get("schema") == "rank-seven-order-eight-combined-owner-indices-v1" and
            indices.get("source_stream_sha256") == SOURCE_SHA256 and
            indices.get("precedence") == EXPECTED_PRECEDENCE,
            "combined indices: scope or precedence changed")
    groups = indices.get("exclusive_stream_indices")
    require(type(groups) is dict and set(groups) == set(EXPECTED_EXCLUSIVE),
            "combined indices: exclusive groups changed")
    exclusive = {name: canonical_index_set(groups[name], name)
                 for name in EXPECTED_EXCLUSIVE}
    require({name: len(values) for name, values in exclusive.items()} == EXPECTED_EXCLUSIVE,
            "combined indices: exclusive counts changed")
    universe = frozenset(range(ROW_TOTAL))
    require(sum(map(len, exclusive.values())) == ROW_TOTAL and
            frozenset().union(*exclusive.values()) == universe and
            all(left.isdisjoint(right) for index, left in enumerate(exclusive.values())
                for right in list(exclusive.values())[index + 1:]),
            "combined indices: groups are not an exact partition")
    direct = exclusive["direct-rational"]
    scalar_exclusive = exclusive["scalar-sos"]
    typed_exclusive = exclusive["typed-diagonal"]
    remaining = exclusive["remaining"]
    require(direct == frozenset(range(EXPECTED_EXCLUSIVE["direct-rational"])),
            "combined indices: direct committed range changed")
    require(typed_exclusive == typed_raw - direct - scalar_exclusive,
            "precedence equation failed: E != T \\ (D union S)")
    require(remaining == universe - direct - scalar_exclusive - typed_raw,
            "complement equation failed: R != U \\ (D union S union T)")
    require(scalar_exclusive <= typed_raw and
            len(typed_raw & direct) == 23_052 and
            len(typed_raw & scalar_exclusive) == len(scalar_exclusive) and
            not typed_raw & remaining,
            "typed overlap atoms changed")
    require(indices.get("remaining_source_indices") ==
            [rows[index][2] for index in groups["remaining"]],
            "combined indices: remaining source-index projection changed")
    expected_counts = {"payload-free": PAYLOAD_TOTAL, **{
        name: EXPECTED_EXCLUSIVE[name] for name in
        ("direct-rational", "scalar-sos", "typed-diagonal")
    }}
    require(ledger.get("exclusive_owner_row_counts") == expected_counts and
            ledger.get("combined_owned_residual_total") == sum(expected_counts.values()) and
            ledger.get("remaining_residual_total") == len(remaining) and
            ledger.get("coarse_residual_total") == COARSE_TOTAL,
            "base ledger: partition arithmetic changed")
    return ledger, indices, exclusive


def validate_boundary_ledger(rows, base_ledger, exclusive):
    """Replay boundary owners and authenticate their exact complement."""
    finite, finite_raw, finite_stored = read_canonical_json(
        FINITE_OWNERS_PATH, compressed=True)
    boundary, boundary_raw, boundary_stored = read_canonical_json(
        BOUNDARY_OWNERS_PATH, BOUNDARY_OWNERS_STORED_SHA256, compressed=True)
    ledger, ledger_raw, _ = read_canonical_json(
        BOUNDARY_LEDGER_PATH, BOUNDARY_LEDGER_SHA256)
    require(boundary_raw == BOUNDARY_OWNERS_RAW_SHA256,
            "boundary owners: raw SHA-256 changed")
    require(sha256(FINITE_OWNERS_PATH.read_bytes()) == finite_stored,
            "finite owners: stored digest replay failed")
    finite_records = finite.get("owners")
    owners = boundary.get("owners")
    require(finite.get("schema") == "rank-seven-order-eight-packet-spectral-owners-v2" and
            type(finite_records) is list and len(finite_records) == BOUNDARY_RESCUE_TOTAL and
            boundary.get("schema") == "rank-seven-order-eight-theorem-dnn-owners-v1" and
            boundary.get("source_stream_sha256") == SOURCE_SHA256 and
            type(boundary.get("owner_method")) is str and
            type(boundary.get("theorem_contract")) is dict and
            boundary.get("owner_total") == BOUNDARY_RESCUE_TOTAL and
            boundary.get("target_total") == BOUNDARY_RESCUE_TOTAL * TARGETS_PER_ROW and
            type(owners) is list and len(owners) == BOUNDARY_RESCUE_TOTAL,
            "boundary owner artifacts: scope changed")
    rescue = []
    for position, (finite_owner, owner) in enumerate(
            zip(finite_records, owners, strict=True)):
        require(type(finite_owner) is dict and type(owner) is dict and
                set(owner) == {"displaced_finite_lane", "global_kernel", "source_index",
                               "stream_index", "witness"},
                f"boundary owner {position}: schema changed")
        index = owner["stream_index"]
        require(is_int(index) and 0 <= index < ROW_TOTAL and
                finite_owner.get("stream_index") == index and
                finite_owner.get("source_index") == owner.get("source_index") and
                finite_owner.get("global_kernel") == owner.get("global_kernel") and
                finite_owner.get("lane") == owner.get("displaced_finite_lane") and
                owner.get("displaced_finite_lane") in
                ("induced-packet", "direct-spectral-rayleigh"),
                f"boundary owner {position}: finite classification identity changed")
        row = rows[index]
        require((owner.get("global_kernel"), owner.get("source_index")) == (row[1], row[2]),
                f"boundary owner {position}: escaped authenticated source row")
        verify_shared_witness(row, owner["witness"], f"boundary owner {position}")
        rescue.append(index)
    require(rescue == sorted(set(rescue)) and len(rescue) == BOUNDARY_RESCUE_TOTAL and
            set(rescue) <= exclusive["remaining"],
            "boundary owners: index set changed")
    remainder_records, remainder_raw, remainder_stored = read_jsonl(
        BOUNDARY_REMAINDER_PATH, BOUNDARY_REMAINDER_STORED_SHA256,
        BOUNDARY_REMAINDER_RAW_SHA256)
    expected_indices = sorted(exclusive["remaining"] - set(rescue))
    observed_indices = []
    for position, record in enumerate(remainder_records):
        require(type(record) is list and len(record) == 6 and is_int(record[0]) and
                0 <= record[0] < ROW_TOTAL,
                f"boundary remainder row {position}: malformed record")
        source = rows[record[0]]
        expected = [record[0], source[2], source[1],
                    [[*PAIRS[dense], multiplicity]
                     for dense, multiplicity in zip(source[3], source[4], strict=True)],
                    list(source[5]), source[6]]
        require(record == expected,
                f"boundary remainder row {position}: source projection changed")
        observed_indices.append(record[0])
    require(observed_indices == expected_indices and
            len(observed_indices) == BOUNDARY_REMAINDER_TOTAL,
            "boundary remainder: not the exact order-preserving complement")
    expected_inputs = {
        "base_combined_ledger": {"path": BASE_LEDGER_PATH.name,
                                   "raw_sha256": BASE_LEDGER_SHA256},
        "combined_owner_indices": {"artifact_sha256": INDICES_STORED_SHA256,
                                     "path": INDICES_PATH.name,
                                     "raw_sha256": INDICES_RAW_SHA256},
        "finite_owner_classification": {"artifact_sha256": finite_stored,
                                          "path": FINITE_OWNERS_PATH.name,
                                          "raw_sha256": finite_raw},
        "typed_segmented_accounting": {"path": TYPED_ACCOUNTING_PATH.name,
                                         "raw_sha256": TYPED_ACCOUNTING_SHA256},
    }
    expected_counts = dict(base_ledger["exclusive_owner_row_counts"])
    expected_counts["shared-rational-gram-rescue"] = BOUNDARY_RESCUE_TOTAL
    require(ledger_raw == BOUNDARY_LEDGER_SHA256 and
            ledger.get("schema") ==
            "rank-seven-order-eight-theorem-eligible-combined-ledger-v1" and
            ledger.get("full_theorem") is False and
            ledger.get("source_stream_sha256") == SOURCE_SHA256 and
            ledger.get("authenticated_inputs") == expected_inputs and
            ledger.get("owner_precedence") ==
            [*EXPECTED_PRECEDENCE, "shared-rational-gram-rescue"] and
            ledger.get("exclusive_owner_row_counts") == expected_counts and
            ledger.get("rescue_owner_artifact") == {
                "artifact_sha256": boundary_stored,
                "bytes": BOUNDARY_OWNERS_PATH.stat().st_size,
                "path": BOUNDARY_OWNERS_PATH.name,
                "raw_sha256": boundary_raw,
            } and ledger.get("exact_remainder_stream") == {
                "artifact_sha256": remainder_stored,
                "path": BOUNDARY_REMAINDER_PATH.name,
                "raw_sha256": remainder_raw,
                "record_total": BOUNDARY_REMAINDER_TOTAL,
            } and ledger.get("combined_owned_residual_total") ==
            sum(expected_counts.values()) and
            ledger.get("remaining_residual_total") == BOUNDARY_REMAINDER_TOTAL and
            sum(expected_counts.values()) + BOUNDARY_REMAINDER_TOTAL == COARSE_TOTAL,
            "boundary ledger: links, precedence, or arithmetic changed")
    return {
        "rescue_indices": frozenset(rescue),
        "remainder_indices": frozenset(observed_indices),
        "boundary_ledger_sha256": ledger_raw,
        "boundary_owner_raw_sha256": boundary_raw,
        "boundary_remainder_raw_sha256": remainder_raw,
    }


def hostile_audit(rows):
    """Exercise malformed-input rejection without touching committed artifacts."""
    rejections = 0

    def rejected(action, label):
        nonlocal rejections
        try:
            action()
        except (KeyError, OSError, RuntimeError, TypeError, ValueError,
                ZeroDivisionError, lzma.LZMAError):
            rejections += 1
            return
        raise RuntimeError(f"hostile mutation accepted: {label}")

    rejected(lambda: strict_json(b'{"a":1,"a":2}\n', "duplicate key"),
             "duplicate JSON key")
    rejected(lambda: strict_json(b'{"a":NaN}\n', "NaN"),
             "nonstandard JSON constant")
    rejected(lambda: bitmap_decode("gA==", 1), "nonzero bitmap padding")
    rejected(lambda: canonical_index_set([0, 2, 1], "unsorted"),
             "unsorted owner indices")
    rejected(lambda: canonical_index_set([0, True], "boolean"),
             "boolean owner index")
    rejected(lambda: get_uvarint(b"\x80\x00", 0), "overlong unsigned varint")
    rejected(lambda: read_integer_vector([0] * (ORDER - 2), 256, "short vector"),
             "short stereographic vector")
    rejected(lambda: read_integer_vector([True] + [0] * (ORDER - 2), 256,
                                         "boolean vector"),
             "boolean stereographic numerator")
    rejected(lambda: exact_step_cost((F(1), F(0)), (F(-1), F(0))),
             "antipodal adjacent vectors")

    owners, _, _ = read_canonical_json(
        BOUNDARY_OWNERS_PATH, BOUNDARY_OWNERS_STORED_SHA256, compressed=True)
    first = owners["owners"][0]
    row = rows[first["stream_index"]]
    witness = first["witness"]
    mutations = []
    changed = copy.deepcopy(witness)
    changed["denominator"] = 0
    mutations.append((changed, "zero shared denominator"))
    changed = copy.deepcopy(witness)
    changed["branches"][0] = changed["branches"][0][:-1]
    mutations.append((changed, "short shared branch vector"))
    changed = copy.deepcopy(witness)
    changed["canonical"] = changed["canonical"][:-1]
    mutations.append((changed, "short canonical path list"))
    changed = copy.deepcopy(witness)
    changed["extended"][0] = changed["extended"][0][:-1]
    mutations.append((changed, "short extended path"))
    changed = copy.deepcopy(witness)
    changed["extra"] = 1
    mutations.append((changed, "extra witness field"))
    changed = copy.deepcopy(witness)
    changed["branches"][0][0] = True
    mutations.append((changed, "boolean shared numerator"))
    for changed, label in mutations:
        rejected(lambda changed=changed, label=label:
                 verify_shared_witness(row, changed, label), label)
    require(rejections == 15, "hostile mutation suite did not run completely")
    return rejections


def audit(*, hostile=False):
    global PAIRS
    rows, PAIRS = decode_cache(CACHE_PATH)
    typed_raw, typed_coverage, receipt_ledger = validate_receipts(rows)
    base_ledger, indices, exclusive = validate_base_bridge(
        rows, typed_raw, typed_coverage, receipt_ledger)
    boundary = validate_boundary_ledger(rows, base_ledger, exclusive)
    result = {
        "schema": "rank-seven-order-eight-base-owner-bridge-audit-v1",
        "status": "passed",
        "source_stream_sha256": SOURCE_SHA256,
        "receipt_count": len(receipt_ledger),
        "typed_raw_owner_total": len(typed_raw),
        "typed_coverage_stream_sha256": typed_coverage,
        "base_exclusive_counts": {name: len(exclusive[name])
                                  for name in EXPECTED_EXCLUSIVE},
        "typed_overlap_atoms": {
            "direct-rational": len(typed_raw & exclusive["direct-rational"]),
            "exclusive-scalar-sos": len(typed_raw & exclusive["scalar-sos"]),
            "exclusive-typed-diagonal": len(exclusive["typed-diagonal"]),
            "remaining": len(typed_raw & exclusive["remaining"]),
        },
        "boundary_rescue_total": len(boundary["rescue_indices"]),
        "boundary_remainder_total": len(boundary["remainder_indices"]),
        "boundary_target_replay_total": BOUNDARY_RESCUE_TOTAL * TARGETS_PER_ROW,
        "output_stream": {
            "path": BOUNDARY_REMAINDER_PATH.name,
            "record_total": BOUNDARY_REMAINDER_TOTAL,
            "raw_sha256": boundary["boundary_remainder_raw_sha256"],
            "artifact_sha256": BOUNDARY_REMAINDER_STORED_SHA256,
        },
        "set_identities": {
            "typed-exclusive": "E = T \\ (D union S)",
            "base-remainder": "R = U \\ (D union S union T)",
            "boundary-remainder": "B = R \\ Q",
        },
        "semantically_replayed": [
            "strict canonical JSON and pinned artifact hashes",
            "twenty receipt bitmap/range/source/count/coverage contracts",
            "typed precedence and exact-complement set equations",
            "296 shared rational Gram witnesses on canonical plus fourteen frontiers",
            "83,856-row output as authenticated source projection and exact rescue complement",
        ],
        "digest_pinned_not_recomputed": [
            "payload-free recognizer semantics",
            "raw scalar-SOS membership semantics (only its report and exclusive set are pinned)",
            "the 492,812 expensive typed searches behind the receipts",
            "29,000 direct-rational witness packs",
        ],
        "remaining_gate_gap": (
            "This bridge ends at the authenticated 83,856-row post-boundary stream. "
            "Structural lanes I-III and packet lanes IV-XII require their own exact "
            "semantic replay before a final theorem gate may claim them."
        ),
        "hostile_mutations_rejected": hostile_audit(rows) if hostile else 0,
    }
    result["audit_sha256"] = sha256(canonical_bytes(result))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hostile", action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(hostile=args.hostile), sort_keys=True, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            ZeroDivisionError, lzma.LZMAError) as error:
        raise SystemExit(
            f"rank-seven order-eight typed precedence bridge: FAIL CLOSED: {error}"
        )
