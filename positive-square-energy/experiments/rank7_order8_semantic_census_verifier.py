#!/usr/bin/env python3
"""Fresh read-only semantic replay of the rank-seven/order-eight coarse census.

The committed manifest verifier is intentionally only an integrity checker: it
checks schemas, arithmetic, hashes, and reported totals.  This verifier closes
the semantic gap.  Starting from the pinned rank-seven kernel fixture, it runs
the pinned exact census producer afresh for each of the eight committed ranges
and requires the regenerated canonical payload to equal the decompressed chunk
byte for byte.  Thus kernel identities, automorphism actions, Burnside counts,
canonical orbit representatives, orbit sizes, and exact coarse classifications
are all recomputed rather than trusted from the chunk ledgers.

Nothing is written.  The optional hostile checks demonstrate that two mutations
accepted by the old integrity-only ``verify_chunk`` routine are rejected by the
semantic comparison: a residual duplicate/omission and a kernel-edge change.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import lzma
import sys
from pathlib import Path
from typing import Any, NoReturn

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRODUCER = HERE / "rank7_order8_exact_residual_census.py"
SOURCE_ENGINE = HERE / "rank7_parity_coarse_digest_census.py"
KERNEL_FIXTURE = ROOT / "research" / "fixtures" / "rank-seven-kernel-frontier-census.json"
MANIFEST = HERE / "rank7_order8_exact_residual_census_manifest.json"

PRODUCER_SHA256 = "c55b037dbfd6dcf6971e1a1738e9cc507ff0fc7f0a9e76d0cda548e73e22e9a5"
SOURCE_ENGINE_SHA256 = "d285a1c29cace4cb30882662e786cf1e5086ebc579676a3aa114a18e2365b2a5"
KERNEL_FIXTURE_SHA256 = "a241139ab54ce4cce1ab3812887359edb241c0abfb1018e804b4a5f86762cfd5"
MANIFEST_SHA256 = "5d41e78a2f688f4c3064cb88f1d6d475008d36c84f892edc4cba28ade424fe98"

# (start, stop, filename, canonical-raw SHA-256, stored-XZ SHA-256, residual rows)
CHUNKS = (
    (0, 502, "rank7_order8_residual_chunk_0000_0502.json.xz",
     "58d015d7a89a20e94ba40f3a7455d455caaf0fba0f0cd6fa66f7311b7d906c96",
     "e6ac741d85d3270717064f72515189c256e2452fb969f691fd52c18564b74bc0", 57945),
    (502, 1004, "rank7_order8_residual_chunk_0502_1004.json.xz",
     "63d749a26f883048a87da47b2ffd6668a62457c95b3be164357be2e2615dd085",
     "e0a152337c03d4cc90d9019b9df1d78f193953a9da020a366dcf207f294591a2", 62357),
    (1004, 1506, "rank7_order8_residual_chunk_1004_1506.json.xz",
     "b0cf2e4d8f59b858b834c2931c9c7a00f2b3f7d4345a25ada9bc6f9cbfc2ae0e",
     "d9466950815330ce39213661c0236a3bf3071aa492032f04c7fb9178f84f5760", 57921),
    (1506, 2008, "rank7_order8_residual_chunk_1506_2008.json.xz",
     "bc31cd1f0d0bac8b899701c321cd8f28410f023672beb6bd0899622df0947659",
     "e8669b9627e8444085cca49fe644909b59f820274a96ea636bc07ccd1d0cfc9f", 66889),
    (2008, 2510, "rank7_order8_residual_chunk_2008_2510.json.xz",
     "2aa1b37fb33af25ddcf2d8c3b557b1587ab8625f2e991c32dd684379ec4eab03",
     "61360494cab5ed7f1092e7c31bf614d1060ca9951174bb7d8be70c872516e8da", 63574),
    (2510, 3012, "rank7_order8_residual_chunk_2510_3012.json.xz",
     "438a34e8c6d9ccb379c70e95dc2804fac30abdffa300f07da7a18ab072d74b19",
     "5fcdf62b7f746d53e48084ab1f064b89516a42ffbe3d937265891bd2962a017d", 68019),
    (3012, 3514, "rank7_order8_residual_chunk_3012_3514.json.xz",
     "82d12e35a80d7342d0c1ed4c518d19ffa945de4e8f1cbc733f6c0978ccf3f359",
     "e5738403a73a2980a5cf3b96380b7f3d010dc451956da365bb6a9b5e3e4c8c85", 58101),
    (3514, 4015, "rank7_order8_residual_chunk_3514_4015.json.xz",
     "5c5a6353aa327cb08bb136f32aedcba6f609ccc43726d79a14edc1e0ffd8dc1a",
     "8688fe3966675ec53967613df90176297edcbb1ba98088eef3bd3992284716b9", 58611),
)

EXPECTED_TOTALS = {
    "kernel_total": 4015,
    "physical_row_total": 33006092,
    "parity_orbit_total": 26426026,
    "coarse_certified_total": 25932609,
    "coarse_residual_total": 493417,
    "frontier_target_total": 7401255,
}
SCHEMA = "rank-seven-order-eight-semantic-census-replay-v1"
Json = Any


def fail(message: str) -> NoReturn:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_bytes(value: Json) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def strict_json(raw: bytes, label: str) -> Json:
    def pairs(items: list[tuple[str, Json]]) -> dict[str, Json]:
        result: dict[str, Json] = {}
        for key, value in items:
            require(type(key) is str and key not in result,
                    f"{label}: duplicate or non-string key")
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("ascii"), object_pairs_hook=pairs,
            parse_constant=lambda token: fail(f"{label}: non-finite token {token}"),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label}: invalid strict JSON") from error
    require(raw == canonical_bytes(value), f"{label}: noncanonical JSON")
    return value


def load_producer() -> Any:
    spec = importlib.util.spec_from_file_location("rank7_order8_semantic_producer", PRODUCER)
    require(spec is not None and spec.loader is not None, "cannot load census producer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit_source_pins() -> None:
    pins = {
        PRODUCER: PRODUCER_SHA256,
        SOURCE_ENGINE: SOURCE_ENGINE_SHA256,
        KERNEL_FIXTURE: KERNEL_FIXTURE_SHA256,
        MANIFEST: MANIFEST_SHA256,
    }
    for path, expected in pins.items():
        require(path.is_file() and sha256(path.read_bytes()) == expected,
                f"pinned dependency changed: {path.name}")


def read_manifest() -> dict[str, Json]:
    raw = MANIFEST.read_bytes()
    manifest = strict_json(raw, MANIFEST.name)
    require(type(manifest) is dict and manifest.get("schema") ==
            "rank-seven-order-eight-exact-residual-census-manifest-v1" and
            manifest.get("status") == "complete-exact-residual-orbit-decomposition" and
            manifest.get("full_theorem") is False and
            manifest.get("rank") == 7 and manifest.get("order") == 8 and
            manifest.get("budget") == [6, 1] and manifest.get("path_count") == 14 and
            manifest.get("frontiers_per_residual") == 15 and
            manifest.get("source_sha256") == KERNEL_FIXTURE_SHA256,
            "manifest scope changed")
    require(all(manifest.get(key) == value for key, value in EXPECTED_TOTALS.items()),
            "manifest exact totals changed")
    records = manifest.get("chunks")
    require(type(records) is list and len(records) == len(CHUNKS),
            "manifest chunk ledger changed")
    expected_records = [
        {
            "artifact_sha256": stored_digest,
            "coarse_residual_total": residuals,
            "kernel_range": [start, stop],
            "path": filename,
            "raw_sha256": raw_digest,
        }
        for start, stop, filename, raw_digest, stored_digest, residuals in CHUNKS
    ]
    require(records == expected_records, "manifest chunk records changed")
    return manifest


def read_chunk(specification: tuple[int, int, str, str, str, int]) -> tuple[dict[str, Json], bytes]:
    start, stop, filename, raw_digest, stored_digest, residuals = specification
    path = HERE / filename
    stored = path.read_bytes()
    require(sha256(stored) == stored_digest, f"{filename}: stored bytes changed")
    try:
        raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
    except lzma.LZMAError as error:
        raise RuntimeError(f"{filename}: invalid XZ stream") from error
    require(sha256(raw) == raw_digest, f"{filename}: raw bytes changed")
    payload = strict_json(raw, filename)
    require(type(payload) is dict and payload.get("kernel_range") == [start, stop] and
            payload.get("kernel_total") == stop - start and
            payload.get("coarse_residual_total") == residuals and
            payload.get("source_sha256") == KERNEL_FIXTURE_SHA256,
            f"{filename}: pinned chunk scope changed")
    return payload, raw


def require_semantic_identity(generated: Json, candidate: Json, label: str) -> None:
    require(canonical_bytes(generated) == canonical_bytes(candidate),
            f"{label}: fresh semantic regeneration differs from committed payload")


def replay(hostile: bool) -> dict[str, Json]:
    audit_source_pins()
    manifest = read_manifest()
    producer = load_producer()
    require(Path(producer.SOURCE_ENGINE).resolve() == SOURCE_ENGINE.resolve() and
            producer.ORDER == 8 and producer.RANK == 7 and
            producer.KERNEL_TOTAL == 4015 and producer.BUDGET_SCALED == 180 and
            producer.FRONTIERS_PER_RESIDUAL == 15,
            "producer constants or source-engine linkage changed")
    engine = producer.load_engine()
    require(Path(engine.SOURCE).resolve() == KERNEL_FIXTURE.resolve() and
            engine.SOURCE_SHA256 == KERNEL_FIXTURE_SHA256 and
            engine.RANK == 7 and engine.BUDGET_SCALED == 180,
            "source-engine fixture linkage or constants changed")

    totals = {key: 0 for key in EXPECTED_TOTALS}
    first_pair: tuple[dict[str, Json], dict[str, Json]] | None = None
    chunk_receipts = []
    for specification in CHUNKS:
        start, stop, filename, raw_digest, stored_digest, residuals = specification
        committed, committed_raw = read_chunk(specification)
        # This is the semantic step.  It regenerates kernels, automorphisms,
        # Burnside counts, orbit representatives, and coarse classifications.
        generated = producer.generate_chunk(start, stop, progress=False)
        producer.verify_chunk(generated)
        generated_raw = producer.canonical_bytes(generated)
        require(generated_raw == committed_raw,
                f"{filename}: fresh semantic regeneration is not byte-identical")
        if first_pair is None:
            first_pair = generated, committed
        for key in totals:
            totals[key] += generated[key]
        chunk_receipts.append({
            "artifact_sha256": stored_digest,
            "coarse_residual_total": residuals,
            "kernel_range": [start, stop],
            "raw_sha256": raw_digest,
        })

    require(totals == EXPECTED_TOTALS, "fresh census totals changed")
    producer.verify_manifest(manifest, MANIFEST)

    rejected = 0
    if hostile:
        require(first_pair is not None, "hostile seed is missing")
        generated, committed = first_pair

        duplicate = copy.deepcopy(committed)
        require(len(duplicate["residuals"]) >= 2, "hostile residual seed is too short")
        duplicate["residuals"][1] = copy.deepcopy(duplicate["residuals"][0])
        digest = hashlib.sha256()
        for record in duplicate["residuals"]:
            digest.update(producer.canonical_bytes(record))
        duplicate["residual_stream_sha256"] = digest.hexdigest()
        # Establish that this is precisely the former integrity-only gap.
        producer.verify_chunk(duplicate)
        try:
            require_semantic_identity(generated, duplicate, "duplicate/omission mutation")
        except RuntimeError:
            rejected += 1
        else:
            fail("semantic comparator accepted duplicate/omission mutation")

        changed_edge = copy.deepcopy(committed)
        edge = changed_edge["kernels"][0]["edges"][0]
        require(edge[:2] == [0, 6], "hostile kernel-edge seed changed")
        edge[:2] = [0, 5]
        # Residual hashes do not cover kernel ledgers, so the old checker accepts this.
        producer.verify_chunk(changed_edge)
        try:
            require_semantic_identity(generated, changed_edge, "kernel-edge mutation")
        except RuntimeError:
            rejected += 1
        else:
            fail("semantic comparator accepted kernel-edge mutation")

    require(rejected == (2 if hostile else 0), "hostile rejection ledger changed")
    return {
        "schema": SCHEMA,
        "status": "passed",
        "scope": "rank-seven-order-eight-coarse-residual-census",
        "semantic_replay": (
            "fresh in-memory regeneration of kernels, automorphisms, Burnside orbit counts, "
            "canonical representatives, orbit sizes, and exact tetrahedral coarse classifications"
        ),
        "kernel_fixture_boundary": (
            "starts from the pinned rank-seven kernel fixture; its removable-ear generation audit "
            "is a separate dependency"
        ),
        "source_sha256": {
            "census_producer": PRODUCER_SHA256,
            "kernel_fixture": KERNEL_FIXTURE_SHA256,
            "source_engine": SOURCE_ENGINE_SHA256,
        },
        "manifest_sha256": MANIFEST_SHA256,
        "chunk_total": len(CHUNKS),
        "semantic_chunk_byte_matches": len(CHUNKS),
        "chunks": chunk_receipts,
        **totals,
        "hostile_mutations_rejected": rejected,
        "writes": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hostile", action="store_true",
                        help="also reject duplicate/omission and kernel-edge mutations")
    args = parser.parse_args(argv)
    try:
        sys.stdout.buffer.write(canonical_bytes(replay(args.hostile)))
        return 0
    except (KeyError, OSError, RuntimeError, TypeError, ValueError,
            UnicodeError, lzma.LZMAError) as error:
        sys.stderr.write(f"rank-seven order-eight semantic census: FAIL CLOSED: {error}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
