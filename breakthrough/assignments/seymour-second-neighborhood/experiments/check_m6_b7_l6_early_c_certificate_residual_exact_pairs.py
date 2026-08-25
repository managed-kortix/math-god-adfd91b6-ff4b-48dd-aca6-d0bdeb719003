#!/usr/bin/env python3
"""Independent certificate-relative residual graph and exact-cell checker."""

import argparse
import hashlib
import itertools
import json
import math
import re
import tempfile
from functools import lru_cache
from pathlib import Path

import check_m6_b7_l6_early_c_inaccessible_pair_orbits as source
from check_m6_parent_cnf import parse_cnf

HERE = Path(__file__).resolve().parent
PREFIX = "m6-b7-l6-early-c-certificate-residual-exact-pair"
FORMAT = f"{PREFIX}-cnf-v1"
MANIFEST_FORMAT = f"{PREFIX}-orbits-v1"
HASH_FORMAT = f"{PREFIX}-hashes-v1"
MANIFEST = HERE / f"{PREFIX}-orbits.tsv"
HASHES = HERE / f"{PREFIX}-hashes.tsv"
SCOUT10 = HERE / f"{PREFIX}-scout-10s.json"
SCOUT = HERE / "m6-b7-l6-early-c-inaccessible-pair-scout-1s.json"
CERTIFICATES = HERE / "m6-b7-l6-early-c-inaccessible-pair-scout-unsat-certificates.tsv"
SCOUT_IDENTITY = (47594, "1c324d6ce3b73ebdb9abdc8bafcaed1a3373541b208c7ef22002d1556bd3a480")
CERTIFICATE_IDENTITY = (61761, "85a74a1a11f5abc169fc91a9ea61ea9068258a2bb0435d097709ec80c825e42e")
CHILDREN = 20
CELL_PARENT_MEMBERSHIPS = 101
COMPATIBLE_PROFILE_PARENT_GRAPHS = 55
PROFILE_PARENTS = 72
SCOUT10_IDENTITY = (6090, "f0013bdcd704fc34450be9c3ffcdf2c94038786e2d6de6e7018dcb02ef3c001e")
STATUS_SEQUENCE_SHA256 = "558cf81bde85f8ec4400eac223eb1747b742ae83610083017868b24d7136ddb6"


def identity(path):
    data = path.read_bytes()
    return len(data), hashlib.sha256(data).hexdigest()


def certificate_scope():
    if identity(SCOUT) != SCOUT_IDENTITY or identity(CERTIFICATES) != CERTIFICATE_IDENTITY:
        raise RuntimeError("frozen certificate ancestry changed")
    scout = json.loads(SCOUT.read_text(encoding="ascii"))
    statuses = tuple(row.get("status") for row in scout.get("rows", ()))
    if len(statuses) != 192 or set(statuses) != {"UNSAT", "TIMEOUT"}:
        raise RuntimeError("frozen scout framing differs")
    scout_scope = tuple(i for i, status in enumerate(statuses) if status == "UNSAT")
    lines = CERTIFICATES.read_text(encoding="ascii").splitlines()
    marker = next((i for i, line in enumerate(lines) if line.startswith("columns\t")), None)
    if marker is None:
        raise RuntimeError("certificate ledger has no columns")
    ledger_scope = tuple(int(line.split("\t", 1)[0]) for line in lines[marker + 1:])
    if len(scout_scope) != 172 or ledger_scope != scout_scope or len(set(ledger_scope)) != 172:
        raise RuntimeError("certified pair set is not the committed 172-child set")
    return frozenset(ledger_scope)


@lru_cache(maxsize=1)
def derive():
    all_children = source.derive_children()
    certified_ordinals = certificate_scope()
    certified = frozenset((child[1], child[3]) for ordinal, child in enumerate(all_children)
                          if ordinal in certified_ordinals)
    residual = tuple((ordinal, child) for ordinal, child in enumerate(all_children)
                     if ordinal not in certified_ordinals)
    if len(certified) != 172 or len(residual) != CHILDREN or \
            sum(len(child[5]) for _, child in residual) != CELL_PARENT_MEMBERSHIPS:
        raise RuntimeError("certified/residual pair reconstruction differs")

    residual_pairs = frozenset((child[1], child[3]) for _, child in residual)
    if certified & residual_pairs or len(certified | residual_pairs) != 192:
        raise RuntimeError("certified and residual pair-orbit sets do not partition the original cover")

    cell_coverage = set()
    profile_parents_traversed = 0
    compatible_profile_parent_graphs = 0
    for profile_ordinal in source.PROFILES:
        profile = next(child[2] for _, child in residual if child[1] == profile_ordinal)
        supports = tuple(source.parent_nonoutneighbors(profile, row)[1] for _, _, row in profile[7])
        group = source.explicit_stabilizer(profile[5])
        certified_edges = set()
        residual_edges = set()
        for ordinal, child in enumerate(all_children):
            if child[1] != profile_ordinal:
                continue
            orbit = {frozenset(permutation.get(v, v) for v in child[3]) for permutation in group}
            (certified_edges if ordinal in certified_ordinals else residual_edges).update(orbit)
        original_edges = {frozenset(pair) for support in supports
                          for pair in itertools.combinations(support, 2)}
        if certified_edges & residual_edges or certified_edges | residual_edges != original_edges:
            raise RuntimeError("original pair profile minus certified union is not the residual graph")
        for parent_ordinal, support in enumerate(supports):
            profile_parents_traversed += 1
            profile_parent_graph = residual_edges & {
                frozenset(pair) for pair in itertools.combinations(support, 2)
            }
            compatible_profile_parent_graphs += bool(profile_parent_graph)
            if any(frozenset(triple_pairs) <= profile_parent_graph
                   for triple in itertools.combinations(support, 3)
                   for triple_pairs in [[frozenset(pair) for pair in itertools.combinations(triple, 2)]]):
                raise RuntimeError("certificate-relative residual pair graph contains a triangle")

            surviving_profiles = set()
            exact_cells = set()
            for size in range(2, len(support) + 1):
                for inaccessible in itertools.combinations(support, size):
                    inaccessible = frozenset(inaccessible)
                    pairs = {frozenset(pair) for pair in itertools.combinations(inaccessible, 2)}
                    if pairs.isdisjoint(certified_edges):
                        surviving_profiles.add(inaccessible)
            for pair in profile_parent_graph:
                exact_cells.add(pair)
                cell_coverage.add((profile_ordinal, parent_ordinal, pair))
            if surviving_profiles != exact_cells or any(len(item) != 2 for item in surviving_profiles):
                raise RuntimeError("surviving model is not exactly one residual inaccessible pair")

    expected_coverage = {(child[1], parent, child[3]) for _, child in residual for parent in child[5]}
    if cell_coverage != expected_coverage or len(cell_coverage) != CELL_PARENT_MEMBERSHIPS:
        raise RuntimeError("exact-pair cells do not preserve the 101 cell-parent memberships")
    if (compatible_profile_parent_graphs, profile_parents_traversed) != \
            (COMPATIBLE_PROFILE_PARENT_GRAPHS, PROFILE_PARENTS):
        raise RuntimeError("compatible/all profile-parent graph count differs")
    return residual


def dimensions(record):
    _, child = record
    variables, clauses = source.dimensions(child)
    return variables, clauses + 7 * len(child[5])


def manifest_payload(children):
    lines = [MANIFEST_FORMAT,
             f"source-scout-bytes\t{SCOUT_IDENTITY[0]}", f"source-scout-sha256\t{SCOUT_IDENTITY[1]}",
             f"certificate-ledger-bytes\t{CERTIFICATE_IDENTITY[0]}",
             f"certificate-ledger-sha256\t{CERTIFICATE_IDENTITY[1]}",
             "committed-certified-children\t172", f"children\t{CHILDREN}",
             f"cell-parent-memberships\t{CELL_PARENT_MEMBERSHIPS}",
             f"distinct-compatible-profile-parent-graphs\t{COMPATIBLE_PROFILE_PARENT_GRAPHS}",
             f"profile-parents-traversed\t{PROFILE_PARENTS}",
             "semantics\teach compatible selector adds seven guarded positive q clauses, leaving exactly its inaccessible pair",
             "cover\toriginal 192-pair profile cover minus the certified 172-orbit union equals this disjoint exact-pair cover",
             "columns\tcell,source-child,key,profile,low-C,pair,compatible-parents,positive-q-clauses,variables,clauses"]
    for cell, (source_ordinal, child) in enumerate(children):
        variables, clauses = dimensions((source_ordinal, child))
        lines.append(f"{cell:03d}\t{source_ordinal:03d}\t{child[0]}\t{child[1]:02d}\t"
                     f"{source.low_vertex(child[2][3])}\t{','.join(map(str, sorted(child[3])))}\t"
                     f"{len(child[5])}\t{7 * len(child[5])}\t{variables}\t{clauses}")
    return ("\n".join(lines) + "\n").encode("ascii")


def reconstruct(record):
    _, child = record
    names, clauses, selectors = source.reconstruct(child)
    low, pair = source.low_vertex(child[2][3]), child[3]
    profile = child[2]
    for parent_ordinal in child[5]:
        support = source.parent_nonoutneighbors(profile, profile[7][parent_ordinal][2])[1]
        if not pair < support or len(support - pair) != 7:
            raise RuntimeError("residual parent support differs")
        selector = selectors[parent_ordinal]
        clauses.extend((-selector, names.index(f"q_{low}_{vertex}") + 1)
                       for vertex in sorted(support - pair))
    return names, clauses, selectors


def metadata(cell, record, manifest, selectors):
    source_ordinal, child = record
    return [("format", FORMAT), ("manifest-format", MANIFEST_FORMAT),
            ("manifest-bytes", str(len(manifest))),
            ("manifest-sha256", hashlib.sha256(manifest).hexdigest()),
            ("cell", str(cell)), ("source-child", str(source_ordinal)),
            ("child-key", child[0]), ("profile", str(child[1])),
            ("low-C", str(source.low_vertex(child[2][3]))),
            ("exact-inaccessible-pair", ",".join(map(str, sorted(child[3])))),
            ("compatible-parent-ordinals", ",".join(map(str, child[5]))),
            ("compatible-parents", str(len(child[5]))),
            ("positive-q-clauses", str(7 * len(child[5]))),
            ("first-selector", str(selectors[0])), ("last-selector", str(selectors[-1]))]


def write_reconstruction(path, cell, record, manifest):
    names, clauses, selectors = reconstruct(record)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        for name, value in metadata(cell, record, manifest, selectors):
            handle.write(f"c {name} {value}\n")
        for number, name in enumerate(names, 1):
            handle.write(f"c var {number} {name}\n")
        handle.write(f"p cnf {len(names)} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")


def load_hashes(manifest, path=HASHES):
    lines = path.read_text(encoding="ascii").splitlines()
    expected = [HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
                f"children\t{CHILDREN}",
                "columns\tcell,source-child,key,compatible-parents,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != CHILDREN + 5:
        raise RuntimeError("residual hash ledger framing differs")
    result = {}
    for cell, (line, record) in enumerate(zip(lines[5:], derive())):
        source_ordinal, child = record
        fields = line.split("\t")
        variables, clauses = dimensions(record)
        if len(fields) != 8 or fields[:6] != [f"{cell:03d}", f"{source_ordinal:03d}", child[0],
                                             str(len(child[5])), str(variables), str(clauses)] or \
                not fields[6].isdigit() or re.fullmatch(r"[0-9a-f]{64}", fields[7]) is None:
            raise RuntimeError("residual hash row differs")
        result[child[0]] = int(fields[6]), fields[7]
    return result


def check(path):
    children = derive()
    manifest = manifest_payload(children)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("frozen residual manifest differs")
    parsed_metadata, variables, clauses, declared = parse_cnf(path)
    cell = int(dict(parsed_metadata).get("cell", "-1"))
    if not 0 <= cell < CHILDREN:
        raise RuntimeError("cell outside residual cover")
    names, expected, selectors = reconstruct(children[cell])
    if parsed_metadata != metadata(cell, children[cell], manifest, selectors) or variables != names or \
            clauses != expected or declared != dimensions(children[cell]):
        raise RuntimeError("residual cell differs from independent reconstruction")
    digest = identity(path)
    if digest != load_hashes(manifest)[children[cell][1][0]]:
        raise RuntimeError("residual cell hash differs")
    print(f"PASS cell={cell:03d} source_child={children[cell][0]:03d} "
          f"parents={len(children[cell][1][5])} sha256={digest[1]}")


def check_scout(manifest, hashes, path=SCOUT10, require_frozen_identity=True):
    raw = path.read_bytes()
    if require_frozen_identity and identity(path) != SCOUT10_IDENTITY:
        raise RuntimeError("ten-second residual scout identity differs")
    data = json.loads(raw.decode("ascii"))
    ledger_identity = identity(HASHES)
    expected_header = {
        "schema": f"{PREFIX}-scout-v1", "seconds_per_cell": 10,
        "solver": "/tmp/opencode/cadical-1.7.3/build/cadical", "solver_bytes": 1002216,
        "solver_sha256": "108d1042b38ceae5cb71e4a806870c4f4d4b8ffdb48a124f2e1fb7b23d3a8292",
        "solver_version": "1.7.3", "manifest_bytes": len(manifest),
        "manifest_sha256": hashlib.sha256(manifest).hexdigest(),
        "hash_ledger_bytes": ledger_identity[0], "hash_ledger_sha256": ledger_identity[1],
        "status_sequence_sha256": STATUS_SEQUENCE_SHA256,
    }
    rows = data.get("rows", [])
    if set(data) != set(expected_header) | {"rows"} or \
            any(data.get(key) != value for key, value in expected_header.items()) or len(rows) != CHILDREN:
        raise RuntimeError("ten-second residual scout provenance differs")
    statuses = "".join({"TIMEOUT": "T"}.get(row.get("status"), "?") for row in rows)
    if statuses != "T" * CHILDREN or hashlib.sha256(statuses.encode("ascii")).hexdigest() != \
            STATUS_SEQUENCE_SHA256:
        raise RuntimeError("ten-second residual scout is not exactly 20 TIMEOUTs")
    expected_keys = {"cell", "source_child", "key", "profile", "compatible_parents",
                     "status", "seconds", "cnf_sha256"}
    for cell, (row, record) in enumerate(zip(rows, derive())):
        source_ordinal, child = record
        seconds = row.get("seconds")
        if set(row) != expected_keys or row.get("cell") != cell or \
                row.get("source_child") != source_ordinal or row.get("key") != child[0] or \
                row.get("profile") != child[1] or row.get("compatible_parents") != len(child[5]) or \
                row.get("cnf_sha256") != hashes[child[0]][1] or isinstance(seconds, bool) or \
                not isinstance(seconds, (int, float)) or not math.isfinite(seconds) or not 10 <= seconds <= 11:
            raise RuntimeError("ten-second residual scout row differs")
    if raw != (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("ascii"):
        raise RuntimeError("ten-second residual scout is not canonical JSON")


def check_exhaustion():
    children = derive()
    manifest = manifest_payload(children)
    if MANIFEST.read_bytes() != manifest:
        raise RuntimeError("frozen residual manifest differs")
    hashes = load_hashes(manifest)
    with tempfile.TemporaryDirectory(prefix="certificate-residual-check-", dir=HERE.parent) as directory:
        path = Path(directory) / "cell.cnf"
        for cell, record in enumerate(children):
            write_reconstruction(path, cell, record, manifest)
            if identity(path) != hashes[record[1][0]]:
                raise RuntimeError(f"regenerated residual cell {cell:03d} differs")
    check_scout(manifest, hashes)
    print(f"PASS certified_pairs=172 cells={CHILDREN} "
          f"cell_parent_memberships={CELL_PARENT_MEMBERSHIPS} "
          f"compatible_profile_parent_graphs={COMPATIBLE_PROFILE_PARENT_GRAPHS} "
          f"profile_parents_traversed={PROFILE_PARENTS} "
          f"triangle_free_profile_parents={PROFILE_PARENTS} exact_cover=yes scout_timeout=20 "
          f"manifest_sha256={hashlib.sha256(manifest).hexdigest()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path, nargs="?")
    parser.add_argument("--exhaustion", action="store_true")
    args = parser.parse_args()
    if args.exhaustion:
        check_exhaustion()
    if args.cnf:
        check(args.cnf)
    if not args.exhaustion and not args.cnf:
        parser.error("provide --exhaustion or a CNF")


if __name__ == "__main__":
    main()
