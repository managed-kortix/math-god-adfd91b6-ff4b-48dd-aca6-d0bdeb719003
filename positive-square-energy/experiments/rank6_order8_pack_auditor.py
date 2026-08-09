#!/usr/bin/env python3
"""Manifest and fail-closed exact auditor for order-eight search packs."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PIPELINE_PATH = HERE / "rank6_order8_sparse_pipeline.py"
SYMBOLIC_PATH = HERE / "rank6_order8_symbolic_templates.json"
RECOGNIZER_PATH = HERE / "rank6_order8_symbolic_recognizers.py"
ENGINE_PATH = HERE.parents[1] / "pentacyclic" / "research" / \
    "order8-dim8-rational-canonical-frontiers-experiment.py"
KERNEL_PATH = HERE.parents[1] / "research" / "fixtures" / "rank-six-kernels.json"
DEFAULT_MANIFEST = HERE / "rank6_order8_search_manifest.json"
DEFAULT_TRANSCRIPT = HERE / "rank6_order8_exact_audit_transcript.json"
SCHEMA = "rank-six-order-eight-search-pack-manifest-v2"
TRANSCRIPT_SCHEMA = "rank-six-order-eight-exact-audit-transcript-v1"
FRONTIER_TOTAL = 14


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def stream_line(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("ascii") + b"\n"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw, label):
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=object_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label} is not canonical ASCII JSON") from error


def dependency_digests():
    paths = {
        "kernel_source": KERNEL_PATH,
        "pipeline": PIPELINE_PATH,
        "rational_engine": ENGINE_PATH,
        "symbolic_fixture": SYMBOLIC_PATH,
        "symbolic_recognizer": RECOGNIZER_PATH,
    }
    return {name: sha256(path.read_bytes()) for name, path in paths.items()}


def load_symbolic_nulls(pipeline):
    raw = SYMBOLIC_PATH.read_bytes()
    payload = strict_json(raw, "symbolic fixture")
    require(raw == canonical_bytes(payload), "symbolic fixture is not canonical JSON")
    recognizer = load_module("rank6_order8_symbolic_for_pack_audit", RECOGNIZER_PATH)
    derived = recognizer.derive_payload(pipeline)
    recognizer.verify_payload(payload, derived)
    result = set()
    for record in payload["records"]:
        source_index = record["source_index"]
        for target in record["targets"]:
            if target["relation"] == "eq":
                key = (source_index, target["frontier"])
                require(key not in result, "duplicate symbolic null key")
                result.add(key)
    require(len(result) == payload["exact_cost_five_total"] == 256,
            "symbolic null count changed")
    return result, sha256(raw)


def load_manifest(path):
    raw = path.read_bytes()
    payload = strict_json(raw, "manifest")
    require(raw == canonical_bytes(payload), "manifest is not canonical JSON")
    require(set(payload) == {"schema", "source_sha256", "symbolic_sha256",
                             "dependency_sha256",
                             "residual_total", "frontiers_per_residual", "chunks",
                             "covered_residual_range", "covered_target_total",
                             "covered_key_stream_sha256"}, "manifest fields changed")
    require(payload["schema"] == SCHEMA, "manifest schema changed")
    return payload


def auditor_sha256():
    return sha256(Path(__file__).resolve().read_bytes())


def authenticate_artifacts(manifest_path):
    """Authenticate every exact-audit input without decoding witness payloads."""
    manifest = load_manifest(manifest_path)
    dependencies = dependency_digests()
    require(manifest["dependency_sha256"] == dependencies,
            "transitive dependency digest changed")
    require(manifest["source_sha256"] == dependencies["kernel_source"],
            "manifest points to another kernel source")
    require(manifest["symbolic_sha256"] == dependencies["symbolic_fixture"],
            "manifest points to another symbolic fixture")
    require(manifest["frontiers_per_residual"] == FRONTIER_TOTAL,
            "manifest frontier width changed")

    expected_start = 0
    for index, chunk in enumerate(manifest["chunks"]):
        require(type(chunk) is dict and set(chunk) == {
            "path", "residual_range", "compressed_bytes", "compressed_sha256",
            "raw_bytes", "raw_sha256"}, f"bad chunk {index} manifest record")
        start, stop = chunk["residual_range"]
        require(type(start) is int and type(stop) is int and
                start == expected_start < stop <= manifest["residual_total"],
                f"chunk {index} range is not the next ordered interval")
        path = (manifest_path.parent / chunk["path"]).resolve()
        try:
            path.relative_to(manifest_path.parent.resolve())
        except ValueError as error:
            raise RuntimeError(f"chunk {index} escapes the manifest directory") from error
        require(path.is_file(), f"missing chunk {index}")
        digest = hashlib.sha256()
        size = 0
        with path.open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                size += len(block)
                digest.update(block)
        require(size == chunk["compressed_bytes"] and
                digest.hexdigest() == chunk["compressed_sha256"],
                f"chunk {index} compressed artifact changed")
        expected_start = stop
    require(expected_start == manifest["residual_total"],
            "manifest does not cover every residual")
    require(manifest["covered_residual_range"] == [0, expected_start] and
            manifest["covered_target_total"] == expected_start * FRONTIER_TOTAL,
            "manifest coverage totals changed")
    return manifest, sha256(canonical_bytes(manifest))


def transcript_payload(manifest_path, report):
    manifest, manifest_digest = authenticate_artifacts(manifest_path)
    require(report["exact_audit"] is True and report["status"] == "complete",
            "cannot attest an incomplete audit")
    return {
        "schema": TRANSCRIPT_SCHEMA,
        "auditor_sha256": auditor_sha256(),
        "manifest_sha256": manifest_digest,
        "dependency_sha256": manifest["dependency_sha256"],
        "covered_key_stream_sha256": manifest["covered_key_stream_sha256"],
        "report": report,
    }


def load_transcript(path):
    raw = path.read_bytes()
    payload = strict_json(raw, "exact audit transcript")
    require(raw == canonical_bytes(payload), "exact audit transcript is not canonical JSON")
    return raw, payload


def authenticate_transcript(manifest_path, transcript_path):
    """Bind a persisted exact result to all current inputs; do no exact replay."""
    manifest, manifest_digest = authenticate_artifacts(manifest_path)
    raw, transcript = load_transcript(transcript_path)
    require(set(transcript) == {"schema", "auditor_sha256", "manifest_sha256",
                                "dependency_sha256", "covered_key_stream_sha256", "report"},
            "exact audit transcript fields changed")
    require(transcript["schema"] == TRANSCRIPT_SCHEMA, "exact audit transcript schema changed")
    require(transcript["auditor_sha256"] == auditor_sha256(), "attested auditor changed")
    require(transcript["manifest_sha256"] == manifest_digest, "attested manifest changed")
    require(transcript["dependency_sha256"] == manifest["dependency_sha256"],
            "attested transitive dependencies changed")
    require(transcript["covered_key_stream_sha256"] == manifest["covered_key_stream_sha256"],
            "attested target key stream changed")
    require(transcript["report"].get("exact_audit") is True and
            transcript["report"].get("status") == "complete",
            "transcript does not attest a complete exact audit")
    return raw, transcript


def target_frontier(target):
    return None if target == 0 else target - 1


def key_digest(residual_rows, stop):
    digest = hashlib.sha256()
    for source_index, source in enumerate(residual_rows[:stop]):
        number, _, _, row, _, _, _ = source
        for target in range(FRONTIER_TOTAL):
            digest.update(stream_line(
                [source_index, number, list(row), target_frontier(target)]))
    return digest.hexdigest()


def audit(manifest_path, exact=True):
    manifest = load_manifest(manifest_path)
    dependencies = dependency_digests()
    require(manifest["dependency_sha256"] == dependencies,
            "transitive dependency digest changed")
    pipeline = load_module("rank6_order8_sparse_for_pack_audit", PIPELINE_PATH)
    require(manifest["source_sha256"] == pipeline.SOURCE_SHA256,
            "manifest points to another kernel source")
    require(manifest["source_sha256"] == dependencies["kernel_source"],
            "pipeline and manifest disagree on the kernel source")
    symbolic_nulls, symbolic_sha256 = load_symbolic_nulls(pipeline)
    require(manifest["symbolic_sha256"] == symbolic_sha256,
            "manifest points to another or unverified symbolic fixture")
    require(manifest["frontiers_per_residual"] == FRONTIER_TOTAL,
            "manifest frontier width changed")
    _, residual_rows = pipeline.census(collect_residuals=True)
    residual_total = len(residual_rows)
    require(manifest["residual_total"] == residual_total, "residual total changed")

    chunks = manifest["chunks"]
    require(type(chunks) is list and chunks, "manifest has no chunks")
    expected_start = 0
    decoded = []
    for index, chunk in enumerate(chunks):
        require(type(chunk) is dict and set(chunk) == {
            "path", "residual_range", "compressed_bytes", "compressed_sha256",
            "raw_bytes", "raw_sha256"}, f"bad chunk {index} manifest record")
        start, stop = chunk["residual_range"]
        require(type(start) is int and type(stop) is int and
                start == expected_start < stop <= residual_total,
                f"chunk {index} range is not the next ordered interval")
        path = (manifest_path.parent / chunk["path"]).resolve()
        try:
            path.relative_to(manifest_path.parent.resolve())
        except ValueError as error:
            raise RuntimeError(f"chunk {index} escapes the manifest directory") from error
        stored = path.read_bytes()
        require(len(stored) == chunk["compressed_bytes"] and
                sha256(stored) == chunk["compressed_sha256"],
                f"chunk {index} compressed artifact changed")
        try:
            raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"chunk {index} is not a valid XZ stream") from error
        require(len(raw) == chunk["raw_bytes"] and sha256(raw) == chunk["raw_sha256"],
                f"chunk {index} raw stream changed")
        actual_start, attempts, records = pipeline.decode_search(raw, residual_rows)
        require(actual_start == start and attempts == stop - start,
                f"chunk {index} embedded range changed")
        decoded.append((start, records))
        expected_start = stop

    covered = expected_start
    require(manifest["covered_residual_range"] == [0, covered] and
            manifest["covered_target_total"] == covered * FRONTIER_TOTAL,
            "manifest coverage totals changed")
    require(manifest["covered_key_stream_sha256"] == key_digest(residual_rows, covered),
            "covered ordered key stream digest changed")

    unresolved = set()
    observed_nulls = set()
    symbolic_missing = set()
    symbolic_unexpected = set()
    expected_nulls = {key for key in symbolic_nulls if key[0] < covered}
    if exact:
        engine = pipeline.load_engine()
        for start, records in decoded:
            for local, record in enumerate(records):
                source_index = start + local
                costs = pipeline.verify_record(engine, residual_rows[source_index], record)
                require(type(costs) is tuple and len(costs) == FRONTIER_TOTAL,
                        "record audit did not return every target")
                for target, cost in enumerate(costs):
                    key = (source_index, target_frontier(target))
                    if cost is None:
                        unresolved.add(key)
                    elif cost == pipeline.BUDGET:
                        observed_nulls.add(key)

        symbolic_missing = expected_nulls - unresolved
        symbolic_unexpected = unresolved - expected_nulls
        require(not symbolic_unexpected,
                f"unrecognized unresolved targets: {len(symbolic_unexpected)}")

    certified_symbolic = unresolved & expected_nulls
    complete = exact and covered == residual_total and unresolved == certified_symbolic
    status = "complete" if complete else "incomplete"
    report = {
        "status": status,
        "covered_residual_range": [0, covered],
        "residual_total": residual_total,
        "covered_target_total": covered * FRONTIER_TOTAL,
        "unresolved_target_total": len(unresolved),
        "symbolic_certified_target_total": len(certified_symbolic),
        "unresolved_keys": [[source, frontier] for source, frontier in
                            sorted(unresolved, key=lambda key: (key[0], -1 if key[1] is None
                                                               else key[1]))],
        "exact_cost_five_target_total": len(observed_nulls),
        "symbolic_expected_in_coverage": len(expected_nulls),
        "symbolic_rationally_certified_target_total": len(symbolic_missing),
        "symbolic_unexpected_target_total": len(symbolic_unexpected),
        "symbolic_coverage_match": exact and not symbolic_unexpected and
                                   len(certified_symbolic | symbolic_missing) ==
                                   len(expected_nulls),
        "exact_audit": exact,
    }
    return report, complete


def build_manifest(output, paths):
    require(output.parent.is_dir(), "manifest output parent does not exist")
    resolved_paths = tuple(path.resolve() for path in paths)
    require(len(set(resolved_paths)) == len(resolved_paths), "duplicate pack path")
    pipeline = load_module("rank6_order8_sparse_for_manifest", PIPELINE_PATH)
    _, symbolic_sha256 = load_symbolic_nulls(pipeline)
    _, residual_rows = pipeline.census(collect_residuals=True)
    chunks = []
    for path in paths:
        stored = path.read_bytes()
        try:
            raw = lzma.decompress(stored, format=lzma.FORMAT_XZ)
        except lzma.LZMAError as error:
            raise RuntimeError(f"{path.name} is not a valid XZ stream") from error
        start, attempts, _ = pipeline.decode_search(raw, residual_rows)
        chunks.append((start, start + attempts, path, stored, raw))
    chunks.sort(key=lambda item: item[0])
    require(chunks, "no packs supplied")
    expected_start = 0
    records = []
    for index, (start, stop, path, stored, raw) in enumerate(chunks):
        require(start == expected_start < stop, f"pack {index} leaves a gap or overlaps")
        try:
            relative = path.resolve().relative_to(output.parent.resolve()).as_posix()
        except ValueError as error:
            raise RuntimeError("pack is outside the manifest directory") from error
        records.append({
            "path": relative,
            "residual_range": [start, stop],
            "compressed_bytes": len(stored),
            "compressed_sha256": sha256(stored),
            "raw_bytes": len(raw),
            "raw_sha256": sha256(raw),
        })
        expected_start = stop
    payload = {
        "schema": SCHEMA,
        "source_sha256": pipeline.SOURCE_SHA256,
        "symbolic_sha256": symbolic_sha256,
        "dependency_sha256": dependency_digests(),
        "residual_total": len(residual_rows),
        "frontiers_per_residual": FRONTIER_TOTAL,
        "chunks": records,
        "covered_residual_range": [0, expected_start],
        "covered_target_total": expected_start * FRONTIER_TOTAL,
        "covered_key_stream_sha256": key_digest(residual_rows, expected_start),
    }
    output.write_bytes(canonical_bytes(payload))
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--digest-only", action="store_true",
                        help="check ranges and byte/key digests without exact witnesses")
    parser.add_argument("--build-manifest", nargs="+", type=Path, metavar="PACK",
                        help="derive a canonical manifest from ordered-range packs")
    parser.add_argument("--write-transcript", type=Path, metavar="PATH",
                        help="exhaustively audit, then persist a canonical transcript")
    args = parser.parse_args()
    if args.build_manifest is not None:
        require(not args.digest_only, "--digest-only cannot build a manifest")
        payload = build_manifest(args.manifest, args.build_manifest)
        print(f"manifest_sha256={sha256(canonical_bytes(payload))} "
              f"covered_residual_range=0..{payload['covered_residual_range'][1]}")
        return
    require(not (args.digest_only and args.write_transcript),
            "--digest-only cannot write an exact transcript")
    report, complete = audit(args.manifest, not args.digest_only)
    if args.write_transcript is not None:
        require(complete, "cannot write transcript for an incomplete audit")
        require(args.write_transcript.parent.is_dir(), "transcript output parent does not exist")
        args.write_transcript.write_bytes(canonical_bytes(transcript_payload(args.manifest, report)))
    sys.stdout.write(canonical_bytes(report).decode("ascii"))
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
