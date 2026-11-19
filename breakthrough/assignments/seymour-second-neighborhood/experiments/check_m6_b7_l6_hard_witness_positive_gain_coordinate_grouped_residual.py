#!/usr/bin/env python3
"""Independent checker for the exact grouped singleton-certified residual."""

import argparse
import hashlib
import json
import math
import re
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover as source
from check_m6_parent_cnf import LABELS, PAIRS, parse_cnf

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-hard-witness-positive-gain-coordinate"
MANIFEST = HERE / f"{PREFIX}-grouped-residual.tsv"
HASHES = HERE / f"{PREFIX}-grouped-residual-hashes.tsv"
SCOUT = HERE / f"{PREFIX}-grouped-residual-scout-20s.json"
CERTIFICATE_LEDGER = HERE / f"{PREFIX}-residual-singleton-parent-certificates.tsv"
CERTIFICATE_VERIFIER = HERE / f"verify_{PREFIX.replace('-', '_')}_residual_singleton_parent_certificates.py"
BOUND = {
    "singleton-certificate-ledger": (CERTIFICATE_LEDGER, 72132, "bdad79d28b22d2b48ed0aef779765a6aafed752227c1952da36a8e180b48ca3d"),
    "singleton-certificate-verifier": (CERTIFICATE_VERIFIER, 16978, "ca3205e94f01b3b6e551373bad75333130a5d82bf3bc7cdf2e00f92be55e2d08"),
}
FORMAT = f"{PREFIX}-grouped-residual-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-grouped-residual-v1"
HASH_FORMAT = f"{PREFIX}-grouped-residual-hashes-v1"
MANIFEST_IDENTITY = (12775, "188efce389bbfcca54e6b6d5f881de3d9ae1603f2ecf7d671592abeabc1cd7f1")
HASH_IDENTITY = (16431, "f4cc9738c0a5f40ed2fb213358a7025c72bd9d358d8bc694ad009b6743d93148")
SCOUT_IDENTITY = (33769, "0729870deced23f34e87866dea86faac6aafc7740168230c54348b3778f53112")
SCOUT_STATUS_SHA256 = "2fbf70a2995a1925ae0a969ec9e2b645a6cf8d2d62f332472c7b607afefcaeb6"
SOLVER = ("/tmp/opencode/cadical-1.7.3/build/cadical", 1002216,
          "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292", "1.7.3")
WIDTHS = {1: 1, 2: 3, 3: 2, 4: 38, 10: 109}


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def certificate_scope(path=CERTIFICATE_LEDGER):
    for name, (bound_path, size, digest) in BOUND.items():
        if identity(bound_path) != (size, digest):
            raise RuntimeError(f"bound checked singleton input changed: {name}")
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    marker = next((i for i, line in enumerate(lines) if line.startswith("columns\t")), -1)
    if marker < 0 or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("certificate ledger framing changed")
    columns = lines[marker].split("\t", 1)[1].split(",")
    rows = [dict(zip(columns, line.split("\t"))) for line in lines[marker + 1:]]
    ordinals = tuple(int(row.get("membership-ordinal", "-1")) for row in rows)
    if len(rows) != 127 or ordinals != tuple(sorted(set(ordinals))):
        raise RuntimeError("certificate ledger is not the exact ordered 127-row scope")
    for row in rows:
        if re.fullmatch(r"[0-9a-f]{64}", row.get("cnf-sha256", "")) is None or \
                re.fullmatch(r"[0-9a-f]{64}", row.get("xz-sha256", "")) is None:
            raise RuntimeError("certificate row lacks exact CNF/artifact identity")
    return frozenset(ordinals)


def projection(row):
    used = Counter()
    image = {}
    for vertex, cell in enumerate(row["word"]):
        image[vertex] = LABELS[row["branch"]][cell][used[cell]]
        used[cell] += 1
    return frozenset(tuple(sorted((image[a], image[b]))) for a, b in row["edges"])


@lru_cache(maxsize=1)
def derive():
    cover, _ = source.check_coverage()
    certified = certificate_scope()
    groups, membership = [], 0
    for leaf_ordinal, item in enumerate(cover):
        survivors = []
        all_projections = []
        for parent_ordinal, parent in enumerate(item[1][4][2][6]):
            holes = projection(parent[2])
            if len(holes) != 6:
                raise RuntimeError("parent projection is not six holes")
            all_projections.append(holes)
            if membership not in certified:
                survivors.append((membership, parent_ordinal, parent, holes))
            membership += 1
        if len(all_projections) != len(set(all_projections)) or not survivors:
            raise RuntimeError("exact parent projections are duplicate or fully eliminated")
        groups.append((leaf_ordinal, item, tuple(survivors)))
    widths = Counter(len(group[2]) for group in groups)
    if membership != 1382 or len(groups) != 153 or sum(map(lambda group: len(group[2]), groups)) != 1255:
        raise RuntimeError("independent grouped census differs")
    if dict(widths) != WIDTHS:
        raise RuntimeError(f"independent width distribution differs: {dict(widths)}")
    return tuple(groups)


def reconstruct(group):
    leaf_ordinal, item, survivors = group
    variables, clauses, old_selectors = source.reconstruct(item)
    matches = [i for i, clause in enumerate(clauses) if tuple(clause) == tuple(old_selectors)]
    if len(matches) != 1:
        raise RuntimeError("old selector ALO is not unique in independent reconstruction")
    start = matches[0]
    stop = start + 1 + 153 * len(old_selectors)
    hole_numbers = {pair: variables.index(f"h_{pair[0]}_{pair[1]}") + 1 for pair in PAIRS}
    expected_guards = []
    for selector, parent in zip(old_selectors, item[1][4][2][6]):
        holes = projection(parent[2])
        expected_guards.extend((-selector, number if pair in holes else -number)
                               for pair, number in hole_numbers.items())
    if clauses[start + 1:stop] != expected_guards:
        raise RuntimeError("old selector layer count, order, or exact guards differ")
    del clauses[start:stop]
    base_names = variables[:-len(old_selectors)]
    selectors = tuple(range(len(base_names) + 1, len(base_names) + len(survivors) + 1))
    clauses.append(selectors)
    clauses.extend((-left, -right) for left, right in combinations(selectors, 2))
    hole_numbers = {pair: base_names.index(f"h_{pair[0]}_{pair[1]}") + 1 for pair in PAIRS}
    for selector, (_, _, _, holes) in zip(selectors, survivors):
        clauses.extend((-selector, number if pair in holes else -number)
                       for pair, number in hole_numbers.items())
    variable_names = base_names + [
        f"grouped_residual_leaf_{leaf_ordinal:03d}_selector_{i:02d}" for i in range(len(survivors))]
    return variable_names, clauses, selectors


def manifest_payload(groups):
    lines = [MANIFEST_FORMAT]
    for name, (_, size, digest) in BOUND.items():
        lines.extend((f"{name}-bytes\t{size}", f"{name}-sha256\t{digest}"))
    lines.extend(("singleton-certificate-scope\texactly the 127 ordered LRAT rows accepted by the bound verifier",
                  "disjunction-equivalence\tper frozen residual leaf, checked singleton UNSAT members are false; the surviving exact-parent disjunction is equivalent",
                  "selector-rebuild\tremove the complete old selector ALO/guard layer; add surviving ALO, pairwise AMO, and 153 guarded projection clauses per survivor",
                  "leaves\t153", "selectors\t1255", "width-distribution\t1x1,3x2,2x3,38x4,109x10",
                  "columns\tleaf-ordinal,key,width,certified-memberships,surviving-memberships,variables,clauses"))
    offset = 0
    for group in groups:
        leaf_ordinal, item, survivors = group
        width = len(item[1][4][2][6])
        surviving = {entry[0] for entry in survivors}
        rejected = ",".join(f"{i:04d}" for i in range(offset, offset + width) if i not in surviving)
        kept = ",".join(f"{entry[0]:04d}" for entry in survivors)
        names, clauses, _ = reconstruct(group)
        lines.append(f"{leaf_ordinal:03d}\t{source.producer.key(item)}\t{len(survivors)}\t{rejected}\t{kept}\t"
                     f"{len(names)}\t{len(clauses)}")
        offset += width
    return ("\n".join(lines) + "\n").encode("ascii")


def metadata(group, manifest, selectors):
    leaf_ordinal, item, survivors = group
    result = [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
              ("manifest-bytes", str(len(manifest))),
              ("manifest-sha256", hashlib.sha256(manifest).hexdigest())]
    for name, (_, size, digest) in BOUND.items():
        result.extend(((f"{name}-bytes", str(size)), (f"{name}-sha256", digest)))
    result.extend((("leaf-ordinal", str(leaf_ordinal)), ("key", source.producer.key(item)),
                   ("surviving-selectors", str(len(selectors))),
                   ("surviving-memberships", ",".join(f"{entry[0]:04d}" for entry in survivors)),
                   ("selector-alo-clauses", "1"),
                   ("selector-amo-clauses", str(len(selectors) * (len(selectors) - 1) // 2)),
                   ("projection-clauses-per-selector", "153"),
                   ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))))
    return result


@lru_cache(maxsize=1)
def check_manifest():
    groups = derive()
    manifest = manifest_payload(groups)
    if identity(MANIFEST) != MANIFEST_IDENTITY or MANIFEST.read_bytes() != manifest:
        raise RuntimeError("grouped manifest differs from independent reconstruction")
    return groups, manifest


@lru_cache(maxsize=1)
def load_hashes(path=HASHES):
    groups, manifest = check_manifest()
    if identity(path) != HASH_IDENTITY:
        raise RuntimeError("grouped hash ledger identity differs")
    data = path.read_bytes()
    lines = data.decode("ascii").splitlines()
    expected = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}", "leaves\t153",
                "columns\tleaf-ordinal,key,width,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 158 or data != ("\n".join(lines) + "\n").encode("ascii"):
        raise RuntimeError("grouped hash ledger framing differs")
    result = []
    for ordinal, (group, line) in enumerate(zip(groups, lines[5:])):
        fields = line.split("\t")
        names, clauses, _ = reconstruct(group)
        prefix = [f"{ordinal:03d}", source.producer.key(group[1]), str(len(group[2])),
                  str(len(names)), str(len(clauses))]
        if len(fields) != 7 or fields[:5] != prefix or not fields[5].isdigit() or \
                re.fullmatch(r"[0-9a-f]{64}", fields[6]) is None:
            raise RuntimeError(f"grouped hash row differs: {ordinal:03d}")
        result.append((int(fields[5]), fields[6]))
    return tuple(result)


def check(path):
    groups, manifest = check_manifest()
    hashes = load_hashes()
    parsed_metadata, variables, clauses, declared = parse_cnf(path)
    try:
        ordinal = int(dict(parsed_metadata).get("leaf-ordinal", "-1"))
    except ValueError as error:
        raise RuntimeError("invalid grouped leaf ordinal") from error
    if not 0 <= ordinal < 153:
        raise RuntimeError("grouped leaf ordinal outside exact scope")
    names, expected_clauses, selectors = reconstruct(groups[ordinal])
    if parsed_metadata != metadata(groups[ordinal], manifest, selectors) or variables != names or \
            clauses != expected_clauses or declared != (len(names), len(expected_clauses)):
        raise RuntimeError("grouped CNF differs from independent exact reconstruction")
    if identity(path) != hashes[ordinal]:
        raise RuntimeError("grouped CNF identity differs from hash ledger")
    print(f"PASS grouped-leaf={ordinal:03d} width={len(selectors)} sha256={hashes[ordinal][1]}")


def check_scout(path=SCOUT):
    groups, manifest = check_manifest()
    hashes = load_hashes()
    data = path.read_bytes()
    if identity(path) != SCOUT_IDENTITY:
        raise RuntimeError("grouped scout bytes or hash differ")
    payload = json.loads(data.decode("ascii"))
    if data != (json.dumps(payload, sort_keys=True, indent=2) + "\n").encode("ascii"):
        raise RuntimeError("grouped scout is not canonical ASCII JSON")
    expected = {"schema": f"{PREFIX}-grouped-residual-scout-v1", "seconds_per_leaf": 20,
                "solver": SOLVER[0], "solver_bytes": SOLVER[1], "solver_sha256": SOLVER[2],
                "solver_version": SOLVER[3], "manifest_bytes": len(manifest),
                "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
                "hash_ledger_bytes": HASH_IDENTITY[0], "hash_ledger_sha256": HASH_IDENTITY[1]}
    if set(payload) != set(expected) | {"rows"} or any(payload.get(k) != v for k, v in expected.items()):
        raise RuntimeError("grouped scout provenance differs")
    rows = payload["rows"]
    if len(rows) != 153:
        raise RuntimeError("grouped scout does not cover all 153 leaves")
    for ordinal, (group, row) in enumerate(zip(groups, rows)):
        fixed = {"leaf": ordinal, "key": source.producer.key(group[1]), "width": len(group[2]),
                 "cnf_sha256": hashes[ordinal][1]}
        if any(row.get(k) != v for k, v in fixed.items()) or set(row) != set(fixed) | {"status", "seconds"}:
            raise RuntimeError(f"grouped scout row identity differs: {ordinal:03d}")
        if row["status"] not in ("SAT", "UNSAT", "TIMEOUT") or isinstance(row["seconds"], bool) or \
                not isinstance(row["seconds"], (int, float)) or not math.isfinite(row["seconds"]):
            raise RuntimeError(f"grouped scout status/timing malformed: {ordinal:03d}")
        if row["status"] == "TIMEOUT" and not 20 <= row["seconds"] <= 21:
            raise RuntimeError(f"grouped scout timeout duration differs: {ordinal:03d}")
        if row["status"] != "TIMEOUT" and not 0 <= row["seconds"] < 20:
            raise RuntimeError(f"grouped scout solved duration differs: {ordinal:03d}")
    totals = Counter(row["status"] for row in rows)
    status_sequence = "".join({"SAT": "S", "UNSAT": "U", "TIMEOUT": "T"}[row["status"]]
                              for row in rows)
    if totals != {"TIMEOUT": 152, "UNSAT": 1} or [row["leaf"] for row in rows
                                                   if row["status"] == "UNSAT"] != [129] or \
            hashlib.sha256(status_sequence.encode("ascii")).hexdigest() != SCOUT_STATUS_SHA256:
        raise RuntimeError("grouped scout exact status sequence or totals differ")
    print(f"PASS grouped-scout leaves=153 selectors=1255 totals={dict(totals)}")
    return totals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--campaign", action="store_true")
    parser.add_argument("--scout", action="store_true")
    args = parser.parse_args()
    if args.campaign:
        groups, manifest = check_manifest()
        load_hashes()
        print(f"PASS grouped-campaign leaves={len(groups)} selectors=1255 widths={WIDTHS} "
              f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")
    if args.cnf:
        check(args.cnf)
    if args.scout:
        check_scout()
    if not args.campaign and not args.cnf and not args.scout:
        parser.error("provide --campaign, --scout, or a CNF")


if __name__ == "__main__":
    main()
