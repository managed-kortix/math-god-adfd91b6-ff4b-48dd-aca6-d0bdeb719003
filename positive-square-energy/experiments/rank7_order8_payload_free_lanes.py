#!/usr/bin/env python3
"""Exact payload-free fast lanes for rank-seven order-eight residuals.

The three lanes reconstruct their Gram certificate from the sparse kernel and
parity row, so a later rational search only needs a mode tag:

* balanced signed rank one;
* a diagonally-dominant signed-imbalance Gram ``I + S/q``;
* mixed-pair/regular-simplex atom assemblies with an exact PSD completion.

Every accepted row owns its canonical target and all fourteen one-coordinate
length-plus-two targets.  This is a search pre-sieve, not a theorem artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import lzma
from collections import Counter
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "rank7_order8_exact_residual_census_manifest.json"
ATOM_RECOGNIZER = HERE / "rank7_order7_symbolic_atom_recognizer.py"
SCHEMA = "rank-seven-order-eight-payload-free-lane-coverage-v1"
ORDER = 8
RANK = 7
PATH_COUNT = 14
TARGETS_PER_RESIDUAL = 15
BUDGET = Fraction(6)
LANES = ("balanced-rank-one", "signed-imbalance-psd", "simplex-mixed-atom")
F = Fraction


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False)
            + "\n").encode("ascii")


def strict_json(raw, label):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"duplicate key in {label}: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise RuntimeError(f"nonstandard constant in {label}: {value}")

    try:
        return json.loads(raw.decode("ascii"), object_pairs_hook=pairs,
                          parse_constant=reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RuntimeError(f"cannot parse {label}") from error


def load_atom_recognizer():
    spec = importlib.util.spec_from_file_location("rank7_order8_atom_core", ATOM_RECOGNIZER)
    require(spec is not None and spec.loader is not None, "cannot load atom recognizer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ORDER = ORDER
    module.PATH_COUNT = PATH_COUNT
    module.BUDGET = RANK - 1
    return module


def canonical_lengths(multiplicity, odd):
    return (([1] + [3] * (odd - 1)) if odd else []) + [2] * (multiplicity - odd)


def path_ledger(edges, row):
    paths = []
    for edge_index, ((u, v, multiplicity), odd) in enumerate(zip(edges, row)):
        require(type(odd) is int and 0 <= odd <= multiplicity, "nonphysical parity row")
        paths.extend((edge_index, occurrence, u, v, length)
                     for occurrence, length in enumerate(canonical_lengths(multiplicity, odd)))
    require(len(paths) == PATH_COUNT, "row does not have fourteen paths")
    return tuple(paths)


def balanced_rank_one(edges, row):
    adjacency = [[] for _ in range(ORDER)]
    for (u, v, multiplicity), odd in zip(edges, row):
        if odd not in (0, multiplicity):
            return False
        parity = bool(odd)
        adjacency[u].append((v, parity))
        adjacency[v].append((u, parity))
    signs = [None] * ORDER
    for root in range(ORDER):
        if signs[root] is not None:
            continue
        signs[root] = 0
        queue = [root]
        for vertex in queue:
            for neighbor, parity in adjacency[vertex]:
                expected = signs[vertex] ^ parity
                if signs[neighbor] is None:
                    signs[neighbor] = expected
                    queue.append(neighbor)
                elif signs[neighbor] != expected:
                    return False
    return True


def path_bound(correlation, length):
    transformed = -correlation if length & 1 else correlation
    if transformed <= -1 or transformed > 1:
        return None
    return (1 - transformed) / (length * (1 + transformed))


def signed_imbalance_certificate(edges, row):
    """Return the best exact DD certificate ``(q, costs)``, or ``None``.

    For ``S_uv=m_uv-2r_uv`` and ``q >= max_u sum_v |S_uv|``, ``qI+S`` is
    symmetric diagonally dominant with nonnegative diagonal, hence PSD.
    Normalizing by q gives a correlation matrix.  We inspect a deterministic
    finite q interval; this is a sufficient recognizer and makes no converse
    claim.
    """
    imbalance = {}
    absolute_rows = [0] * ORDER
    weighted_rows = [0] * ORDER
    for (u, v, multiplicity), odd in zip(edges, row):
        value = multiplicity - 2 * odd
        imbalance[u, v] = value
        absolute_rows[u] += abs(value)
        absolute_rows[v] += abs(value)
        weighted_rows[u] += multiplicity
        weighted_rows[v] += multiplicity
    lower = max(absolute_rows)
    if lower == 0:
        return None
    upper = max(lower, 2 * max(weighted_rows))
    paths = path_ledger(edges, row)
    best = None
    for denominator in range(lower, upper + 1):
        local = []
        for _, _, u, v, length in paths:
            cost = path_bound(F(imbalance[u, v], denominator), length)
            if cost is None:
                break
            local.append(cost)
        else:
            base = sum(local, F())
            targets = (base,) + tuple(
                base - cost + path_bound(F(imbalance[u, v], denominator), length + 2)
                for cost, (_, _, u, v, length) in zip(local, paths))
            require(all(value <= base for value in targets), "lengthening increased DD bound")
            if max(targets) <= BUDGET and (best is None or max(targets) < max(best[1])):
                best = denominator, targets
    return best


def atom_owners(atom, edges, row):
    return tuple(record for record in atom.recognize(edges, row)
                 if record["status"] == "exact-equality-owner")


def recognize_row(atom, edges, row):
    balanced = balanced_rank_one(edges, row)
    imbalance = signed_imbalance_certificate(edges, row)
    atoms = atom_owners(atom, edges, row)
    matches = []
    if balanced:
        matches.append("balanced-rank-one")
    if imbalance is not None:
        matches.append("signed-imbalance-psd")
    if atoms:
        matches.append("simplex-mixed-atom")
    owner = next((lane for lane in LANES if lane in matches), None)
    detail = None
    if owner == "signed-imbalance-psd":
        denominator, targets = imbalance
        worst = max(targets)
        detail = {"denominator": denominator,
                  "worst_cost": [worst.numerator, worst.denominator]}
    elif owner == "simplex-mixed-atom":
        profiles = sorted({(record["profile"]["mixed"],
                            tuple(record["profile"]["simplex_widths"])) for record in atoms})
        detail = {"profiles": [[mixed, list(widths)] for mixed, widths in profiles]}
    return owner, tuple(matches), detail


def read_chunk(path, expected):
    stored = path.read_bytes()
    require(hashlib.sha256(stored).hexdigest() == expected["artifact_sha256"],
            f"chunk artifact digest changed: {path.name}")
    try:
        raw = lzma.decompress(stored) if path.suffix == ".xz" else stored
    except lzma.LZMAError as error:
        raise RuntimeError(f"bad XZ chunk: {path.name}") from error
    require(hashlib.sha256(raw).hexdigest() == expected["raw_sha256"],
            f"chunk raw digest changed: {path.name}")
    payload = strict_json(raw, path.name)
    require(raw == canonical_bytes(payload), f"noncanonical chunk: {path.name}")
    require(payload["kernel_range"] == expected["kernel_range"] and
            payload["coarse_residual_total"] == expected["coarse_residual_total"],
            f"chunk metadata changed: {path.name}")
    return payload


def load_manifest(path):
    raw = path.read_bytes()
    payload = strict_json(raw, "rank-seven order-eight manifest")
    require(raw == canonical_bytes(payload), "manifest is not canonical ASCII JSON")
    require(payload.get("schema") ==
            "rank-seven-order-eight-exact-residual-census-manifest-v1" and
            payload.get("full_theorem") is False, "wrong residual manifest")
    require((payload.get("rank"), payload.get("order"), payload.get("path_count"),
             payload.get("coarse_residual_total"), payload.get("frontier_target_total")) ==
            (RANK, ORDER, PATH_COUNT, 493417, 7401255), "residual universe changed")
    return payload, hashlib.sha256(raw).hexdigest()


def selected_chunks(manifest, indices):
    if indices is None:
        return tuple(range(len(manifest["chunks"])))
    result = tuple(indices)
    require(result and len(set(result)) == len(result) and
            all(0 <= index < len(manifest["chunks"]) for index in result),
            "bad chunk selection")
    return result


def scan(manifest_path, indices=None, progress=False, unresolved_path=None):
    manifest, manifest_digest = load_manifest(manifest_path)
    atom = load_atom_recognizer()
    chosen = selected_chunks(manifest, indices)
    raw_counts = Counter({lane: 0 for lane in LANES})
    owner_counts = Counter({lane: 0 for lane in LANES})
    overlap_counts = Counter()
    profiles = Counter()
    scanned = recognized = 0
    global_offset = 0
    unresolved = []
    key_digest = hashlib.sha256()
    for chunk_index, record in enumerate(manifest["chunks"]):
        chunk_size = record["coarse_residual_total"]
        if chunk_index not in chosen:
            global_offset += chunk_size
            continue
        path = (manifest_path.parent / record["path"]).resolve()
        require(path.parent == manifest_path.parent.resolve(), "chunk path escapes manifest directory")
        chunk = read_chunk(path, record)
        kernels = {item["order_kernel"]: tuple(map(tuple, item["edges"]))
                   for item in chunk["kernels"]}
        for local_index, source in enumerate(chunk["residuals"]):
            source_index = global_offset + local_index
            edges = kernels[source["order_kernel"]]
            row = tuple(source["row"])
            owner, matches, detail = recognize_row(atom, edges, row)
            scanned += 1
            raw_counts.update(matches)
            if len(matches) > 1:
                overlap_counts["+".join(matches)] += 1
            if owner is None:
                unresolved.append(source_index)
            else:
                recognized += 1
                owner_counts[owner] += 1
                if owner == "simplex-mixed-atom":
                    profiles.update(f"mixed-{mixed}/simplex-{'-'.join(map(str, widths)) or 'none'}"
                                    for mixed, widths in ((row[0], tuple(row[1]))
                                                          for row in detail["profiles"]))
            key_digest.update(canonical_bytes([source_index, source["global_kernel"],
                                               source["order_kernel"], source["row"], owner]))
        global_offset += chunk_size
        if progress:
            print(f"chunk={chunk_index} scanned={scanned} recognized={recognized}", flush=True)
    require(scanned == sum(manifest["chunks"][index]["coarse_residual_total"]
                           for index in chosen), "selected residual total changed")
    report = {
        "schema": SCHEMA,
        "full_theorem": False,
        "scope": "exact payload-free sufficient recognizers over rank-seven order-eight coarse residuals",
        "manifest_sha256": manifest_digest,
        "selected_chunks": list(chosen),
        "scanned_residual_total": scanned,
        "scanned_target_total": scanned * TARGETS_PER_RESIDUAL,
        "raw_lane_row_counts": dict(sorted(raw_counts.items())),
        "exclusive_owner_row_counts": dict(sorted(owner_counts.items())),
        "overlap_row_counts": dict(sorted(overlap_counts.items())),
        "atom_profile_owner_counts": dict(sorted(profiles.items())),
        "recognized_residual_total": recognized,
        "recognized_target_total": recognized * TARGETS_PER_RESIDUAL,
        "rational_search_residual_total": scanned - recognized,
        "rational_search_target_total": (scanned - recognized) * TARGETS_PER_RESIDUAL,
        "classification_stream_sha256": key_digest.hexdigest(),
    }
    if unresolved_path is not None:
        require(unresolved_path.parent.is_dir(), "unresolved output parent is missing")
        payload = {
            "schema": "rank-seven-order-eight-rational-search-indices-v1",
            "manifest_sha256": manifest_digest,
            "selected_chunks": list(chosen),
            "source_indices": unresolved,
        }
        unresolved_path.write_bytes(canonical_bytes(payload))
    return report


def verify_report(payload):
    require(type(payload) is dict and set(payload) == {
        "schema", "full_theorem", "scope", "manifest_sha256", "selected_chunks",
        "scanned_residual_total", "scanned_target_total", "raw_lane_row_counts",
        "exclusive_owner_row_counts", "overlap_row_counts", "atom_profile_owner_counts",
        "recognized_residual_total", "recognized_target_total",
        "rational_search_residual_total", "rational_search_target_total",
        "classification_stream_sha256",
    }, "coverage report fields changed")
    require(payload["schema"] == SCHEMA and payload["full_theorem"] is False,
            "wrong coverage report schema")
    require(set(payload["raw_lane_row_counts"]) == set(LANES) and
            set(payload["exclusive_owner_row_counts"]) == set(LANES),
            "lane ledger changed")
    require(sum(payload["exclusive_owner_row_counts"].values()) ==
            payload["recognized_residual_total"], "exclusive owner sum changed")
    require(payload["scanned_residual_total"] == payload["recognized_residual_total"] +
            payload["rational_search_residual_total"], "row partition changed")
    for prefix in ("scanned", "recognized", "rational_search"):
        require(payload[f"{prefix}_target_total"] ==
                TARGETS_PER_RESIDUAL * payload[f"{prefix}_residual_total"],
                f"{prefix} target total changed")


def parse_chunks(raw):
    if raw is None:
        return None
    try:
        return tuple(int(value) for value in raw.split(",") if value != "")
    except ValueError as error:
        raise RuntimeError("--chunks must be comma-separated integers") from error


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    recognize = subparsers.add_parser("recognize")
    recognize.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    recognize.add_argument("--chunks", help="comma-separated chunk indices; default is all")
    recognize.add_argument("--output", type=Path)
    recognize.add_argument("--unresolved-output", type=Path)
    recognize.add_argument("--progress", action="store_true")
    audit = subparsers.add_parser("audit")
    audit.add_argument("report", type=Path)
    audit.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    audit.add_argument("--progress", action="store_true")
    args = parser.parse_args()
    if args.command == "recognize":
        report = scan(args.manifest, parse_chunks(args.chunks), args.progress,
                      args.unresolved_output)
        verify_report(report)
        raw = canonical_bytes(report)
        if args.output is not None:
            require(args.output.parent.is_dir(), "report output parent is missing")
            args.output.write_bytes(raw)
        print(raw.decode("ascii"), end="")
        return
    raw = args.report.read_bytes()
    payload = strict_json(raw, "coverage report")
    require(raw == canonical_bytes(payload), "coverage report is not canonical JSON")
    verify_report(payload)
    regenerated = scan(args.manifest, tuple(payload["selected_chunks"]), args.progress)
    require(canonical_bytes(regenerated) == raw, "coverage report differs from exact rescan")
    print(f"audit=passed report_sha256={hashlib.sha256(raw).hexdigest()} "
          f"recognized_targets={payload['recognized_target_total']} "
          f"rational_search_targets={payload['rational_search_target_total']}")


if __name__ == "__main__":
    try:
        main()
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as error:
        raise RuntimeError(f"fail-closed malformed input: {error}") from error
