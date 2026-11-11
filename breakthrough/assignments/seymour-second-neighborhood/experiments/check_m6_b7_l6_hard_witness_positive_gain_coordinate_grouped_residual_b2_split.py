#!/usr/bin/env python3
"""Independent checker for the exact disjoint grouped B-reduced width-two split."""

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual as source
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-hard-witness-positive-gain-coordinate-grouped-residual-b2-split"
MANIFEST = HERE / f"{PREFIX}.tsv"
HASHES = HERE / f"{PREFIX}-hashes.tsv"
SCOUT = HERE / f"{PREFIX}-scout-20s.json"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
SCOUT_IDENTITY = (8393, "73cb4a5d3040764da9c9efb752136f7f1e86224e16819ae54228e5b7b666c901")
SCOUT_STATUS_SHA256 = "9f2d19fb7801da4c7e15d08c92e8abce897ad315bce4ffb3214059fb9f73e59c"
SOLVER = ("/tmp/opencode/cadical-1.7.3/build/cadical", 1002216,
           "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
RECONSTRUCTIONS = {}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def path_name(path):
    return f"p_{path[0]}_{path[1]}_{path[2]}"


def path_arcs(path):
    return f"{path[0]}>{path[1]},{path[1]}>{path[2]}"


@lru_cache(maxsize=1)
def derive():
    groups, _ = source.check_manifest()
    source.check_scout()
    scout = json.loads(source.SCOUT.read_text(encoding="ascii"))
    selected = []
    for group, row in zip(groups, scout["rows"]):
        item = group[1]
        if item[2] == "b-reduced" and len(item[3]) == 2 and row["status"] == "TIMEOUT":
            names, clauses, selectors = source.reconstruct(group)
            paths = tuple(item[3])
            details = tuple((names.index(path_name(path)) + 1, path_name(path), path_arcs(path)) for path in paths)
            if tuple(detail[0] for detail in details) not in map(tuple, clauses):
                raise RuntimeError("independent source reconstruction lacks x OR y")
            selected.append((group, details, names, clauses, selectors))
    if len(selected) != 15 or 129 in {entry[0][0] for entry in selected}:
        raise RuntimeError("independent exact source scope differs")
    children = []
    for entry in selected:
        children.extend(((entry, 0), (entry, 1)))
    return tuple(children)


def reconstruct(child):
    (group, details, names, clauses, selectors), branch = child
    key = group[0], branch
    if key in RECONSTRUCTIONS:
        return RECONSTRUCTIONS[key]
    result = list(clauses)
    result.append((details[0][0] if branch == 0 else -details[0][0],))
    RECONSTRUCTIONS[key] = names, result, selectors
    return RECONSTRUCTIONS[key]


def manifest_payload(items):
    lines = [MANIFEST_FORMAT]
    for name, path in (("source-manifest", source.MANIFEST), ("source-hash-ledger", source.HASHES),
                       ("source-scout", source.SCOUT)):
        size, digest = identity(path)
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend(("scope\texactly grouped scout-TIMEOUT leaves with B-reduced coordinate ALO width 2",
                  "partition\tfor source ALO x OR y, child 0 adds x and child 1 adds NOT x; source plus NOT x implies y",
                  "selector-preservation\teach child retains its source grouped selector ALO, AMO, names, and guarded projections unchanged",
                  "excluded-certified-grouped-leaf\t129", "sources\t15", "children\t30",
                  "columns\tchild-ordinal,source-leaf,key,branch,unit,path-x-var,path-x,path-x-arcs,path-y-var,path-y,path-y-arcs,grouped-width,variables,clauses"))
    for ordinal, child in enumerate(items):
        (group, details, _, _, selectors), branch = child
        names, clauses, _ = reconstruct(child)
        unit = details[0][0] if branch == 0 else -details[0][0]
        lines.append(f"{ordinal:02d}\t{group[0]:03d}\t{source.source.producer.key(group[1])}\t{branch}\t{unit}\t"
                     f"{details[0][0]}\t{details[0][1]}\t{details[0][2]}\t{details[1][0]}\t{details[1][1]}\t"
                     f"{details[1][2]}\t{len(selectors)}\t{len(names)}\t{len(clauses)}")
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(ordinal, child, manifest):
    (group, details, _, _, selectors), branch = child
    unit = details[0][0] if branch == 0 else -details[0][0]
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))), ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("child-ordinal", str(ordinal)), ("source-leaf", str(group[0])),
            ("key", source.source.producer.key(group[1])), ("branch", str(branch)), ("split-unit", str(unit)),
            ("path-x-var", str(details[0][0])), ("path-x", details[0][1]), ("path-x-arcs", details[0][2]),
            ("path-y-var", str(details[1][0])), ("path-y", details[1][1]), ("path-y-arcs", details[1][2]),
            ("grouped-selectors", str(len(selectors))), ("first-selector", str(selectors[0])),
            ("last-selector", str(selectors[-1]))]


@lru_cache(maxsize=1)
def check_manifest():
    items = derive()
    manifest = manifest_payload(items)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("split manifest differs from independent reconstruction")
    return items, manifest


@lru_cache(maxsize=1)
def load_hashes():
    items, manifest = check_manifest()
    data = HASHES.read_bytes()
    lines = data.decode("ascii").splitlines()
    expected = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "children\t30",
                "columns\tchild-ordinal,source-leaf,key,branch,grouped-width,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 35 or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("split hash ledger framing differs")
    result = []
    for ordinal, (child, line) in enumerate(zip(items, lines[5:])):
        (group, _, _, _, selectors), branch = child
        names, clauses, _ = reconstruct(child)
        fields = line.split("\t")
        prefix = [f"{ordinal:02d}", f"{group[0]:03d}", source.source.producer.key(group[1]), str(branch),
                  str(len(selectors)), str(len(names)), str(len(clauses))]
        if len(fields) != 9 or fields[:7] != prefix or not fields[7].isdigit() or re.fullmatch(r"[0-9a-f]{64}", fields[8]) is None:
            raise RuntimeError(f"split hash row differs: {ordinal:02d}")
        result.append((int(fields[7]), fields[8]))
    return tuple(result)


def check_partition():
    items, manifest = check_manifest()
    load_hashes()
    for pair in range(15):
        first, second = items[2 * pair:2 * pair + 2]
        first_entry, first_branch = first
        second_entry, second_branch = second
        if first_entry is not second_entry or (first_branch, second_branch) != (0, 1):
            raise RuntimeError("children are not paired by source")
        group, details, names, clauses, selectors = first_entry
        x, y = details[0][0], details[1][0]
        if (x, y) not in clauses or reconstruct(first)[1][-1] != (x,) or reconstruct(second)[1][-1] != (-x,):
            raise RuntimeError("x/not-x split or source x OR y differs")
        if reconstruct(first)[1][:-1] != clauses or reconstruct(second)[1][:-1] != clauses:
            raise RuntimeError("child changed source grouped selectors or clauses")
        print(f"source={group[0]:03d} key={source.source.producer.key(group[1])} "
              f"x={x}:{details[0][1]}[{details[0][2]}] y={y}:{details[1][1]}[{details[1][2]}] "
              f"selectors={len(selectors)}")
    print(f"PASS exact-partition sources=15 children=30 manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def check(path):
    items, manifest = check_manifest()
    hashes = load_hashes()
    parsed_metadata, variables, clauses, declared = parse_cnf(path)
    try:
        ordinal = int(dict(parsed_metadata).get("child-ordinal", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid child ordinal") from error
    if not 0 <= ordinal < 30:
        raise RuntimeError("child ordinal outside exact split")
    names, expected_clauses, _ = reconstruct(items[ordinal])
    if parsed_metadata != metadata(ordinal, items[ordinal], manifest) or variables != names or clauses != expected_clauses or declared != (len(names), len(clauses)):
        raise RuntimeError("split child differs from independent reconstruction")
    if identity(path) != hashes[ordinal]:
        raise RuntimeError("split child identity differs")


def check_identity(path, ordinal):
    hashes = load_hashes()
    if not 0 <= ordinal < len(hashes) or identity(path) != hashes[ordinal]:
        raise RuntimeError(f"split child identity differs: {ordinal:02d}")


def check_scout(path=SCOUT, require_frozen_identity=True):
    items, manifest = check_manifest()
    hashes = load_hashes()
    data = path.read_bytes()
    if require_frozen_identity and identity(path) != SCOUT_IDENTITY:
        raise RuntimeError("split scout bytes or hash differ")
    payload = json.loads(data.decode("ascii"))
    expected = {"schema": f"{PREFIX}-scout-v1", "seconds_per_child": 20, "solver": SOLVER[0],
                "solver_bytes": SOLVER[1], "solver_sha256": SOLVER[2], "solver_version": SOLVER[3],
                "manifest_bytes": len(manifest), "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
                "hash_ledger_bytes": identity(HASHES)[0], "hash_ledger_sha256": identity(HASHES)[1]}
    if data != (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("ascii") or set(payload) != set(expected) | {"rows"} or any(payload.get(k) != v for k, v in expected.items()):
        raise RuntimeError("split scout provenance or framing differs")
    if len(payload["rows"]) != 30:
        raise RuntimeError("split scout does not contain 30 children")
    for ordinal, (child, row) in enumerate(zip(items, payload["rows"])):
        (group, _, _, _, selectors), branch = child
        fixed = {"child": ordinal, "source_leaf": group[0], "key": source.source.producer.key(group[1]),
                 "branch": branch, "width": len(selectors), "cnf_sha256": hashes[ordinal][1]}
        if set(row) != set(fixed) | {"status", "seconds"} or any(row.get(k) != v for k, v in fixed.items()):
            raise RuntimeError(f"split scout row differs: {ordinal:02d}")
        if row["status"] not in ("SAT", "UNSAT", "TIMEOUT") or isinstance(row["seconds"], bool) or \
                not isinstance(row["seconds"], (int, float)) or not math.isfinite(row["seconds"]):
            raise RuntimeError(f"split scout status/timing malformed: {ordinal:02d}")
        if row["status"] == "TIMEOUT" and not 20 <= row["seconds"] <= 21:
            raise RuntimeError("split scout timeout duration differs")
        if row["status"] != "TIMEOUT" and not 0 <= row["seconds"] < 20:
            raise RuntimeError("split scout solved duration differs")
    totals = Counter(row["status"] for row in payload["rows"])
    status_sequence = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]]
                              for row in payload["rows"])
    if totals != {"TIMEOUT": 30} or \
            hashlib.sha256(status_sequence.encode("ascii")).hexdigest() != SCOUT_STATUS_SHA256:
        raise RuntimeError("split scout exact all-TIMEOUT status sequence or totals differ")
    print(f"PASS split-scout children=30 totals={dict(totals)}")
    return totals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--partition", action="store_true")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.partition:
        check_partition()
    if args.cnf:
        check(args.cnf)
    if args.scout:
        check_scout()
    if not args.partition and not args.cnf and not args.scout:
        parser.error("provide --partition, --scout, or a CNF")


if __name__ == "__main__":
    main()
