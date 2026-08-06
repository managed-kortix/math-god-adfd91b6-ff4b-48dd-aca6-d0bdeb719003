#!/usr/bin/env python3
"""Fail-closed verifier for order-seven rank-six frontier chunks.

The verifier deliberately reports an open theorem until all 319,202 targets
are present and every target has an exact DNN or separately audited structural
certificate. It never treats a numerical value as a proof.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CENSUS = ROOT / "positive-square-energy" / "experiments" / "rank6_order7_orbit_frontier_census.json"
ENGINE_PATH = (ROOT / "positive-square-energy" / "experiments"
               / "rank6_order7_dim7_rational_frontier.py")
CENSUS_SHA256 = "2e38e09a1b7f800e0a17faa9a05c12adda2bfc45367aecd999b10e121b34bdb3"
FRONTIERS = (None, *range(12))
EXPECTED_TARGETS = 319202


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def locked_census():
    raw = CENSUS.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == CENSUS_SHA256, "census digest changed")
    payload = json.loads(raw.decode("ascii"))
    require(raw == (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii"),
            "census JSON is not canonical")
    require((payload["kernel_total"], payload["physical_total"], payload["orbit_total"],
             payload["coarse_certified_total"], payload["coarse_residual_total"],
             payload["frontier_target_total"])
            == (314, 700792, 519453, 494899, 24554, EXPECTED_TARGETS),
            "census totals changed")
    return payload


def key(record):
    return record["source_index"], record["frontier"]


def audit_structural(record, census, kernels, engine):
    require(set(record) == {"source_index", "kernel", "row", "frontier", "method",
                            "clique_vertices", "tree_vertices"},
            "structural record fields changed")
    require(record["method"] == "induced_clique_plus_nonempty_tree", "structural method changed")
    index = record["source_index"]
    require(type(index) is int and 0 <= index < len(census["residuals"]), "bad structural index")
    source = census["residuals"][index]
    require((record["kernel"], record["row"]) == (source["kernel"], source["row"]),
            "structural source changed")
    paths = engine.path_ledger(kernels[record["kernel"]], tuple(record["row"]), record["frontier"])
    vertices = set(range(7))
    clique, tree = set(record["clique_vertices"]), set(record["tree_vertices"])
    require(clique.isdisjoint(tree) and clique | tree == vertices and len(clique) >= 4 and tree,
            "structural vertex partition changed")
    unit_edges = {tuple(sorted((u, v))) for _, _, u, v, length in paths if length == 1}
    require(set(itertools.combinations(sorted(clique), 2)) <= unit_edges,
            "structural clique is not induced by unit paths")
    tree_edges = {edge for edge in unit_edges if edge[0] in tree and edge[1] in tree}
    require(len(tree_edges) == len(tree) - 1, "structural complement is not a tree")
    seen = {min(tree)}
    while True:
        expanded = seen | {v for edge in tree_edges for v in edge if set(edge) & seen}
        if expanded == seen:
            break
        seen = expanded
    require(seen == tree, "structural complement is disconnected")


def audit_payloads(paths, structural_path=None):
    census = locked_census()
    engine = load_module(ENGINE_PATH, "rank6_order7_rational_engine")
    kernels = {row["kernel"]: tuple(row["code"]) for row in census["kernels"]}
    expected = {(index, frontier) for index in range(len(census["residuals"]))
                for frontier in FRONTIERS}
    records = {}
    rational = unresolved = 0
    for path in paths:
        raw = path.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(raw == engine.canonical_bytes(payload), f"noncanonical chunk {path}")
        engine.verify(payload)
        for record in payload["records"]:
            target = key(record)
            require(target in expected and target not in records, "duplicate or out-of-scope target")
            records[target] = record
            rational += bool(record["exact_dnn_le_5"])
            unresolved += not record["exact_dnn_le_5"]
    structural = {}
    if structural_path is not None:
        raw = structural_path.read_bytes()
        payload = json.loads(raw.decode("ascii"))
        require(payload.get("schema") == "rank-six-order-seven-structural-residuals-v1",
                "structural schema changed")
        require(payload.get("full_theorem") is False, "structural residuals were theorem-promoted")
        for record in payload["records"]:
            audit_structural(record, census, kernels, engine)
            target = (record["source_index"], record["frontier"])
            require(target not in structural, "duplicate structural target")
            structural[target] = record
    require(set(structural) <= {target for target, record in records.items()
                               if not record["exact_dnn_le_5"]},
            "structural record does not close a DNN residual")
    covered = {target for target, record in records.items() if record["exact_dnn_le_5"]} | set(structural)
    theorem = set(records) == expected and covered == expected
    return {
        "chunks": len(paths), "loaded": len(records), "rational": rational,
        "unresolved": unresolved, "structural": len(structural),
        "missing": len(expected - set(records)), "theorem": theorem,
    }


def hostile_checks(paths):
    if not paths:
        census = locked_census()
        attacks = []

        def rejected(candidate):
            try:
                require(candidate["kernel_total"] == 314, "kernel total changed")
                require(candidate["frontier_target_total"] == EXPECTED_TARGETS,
                        "frontier total changed")
                require(candidate["full_theorem"] is False, "census theorem promotion")
                keys = {(row["kernel"], tuple(row["row"])) for row in candidate["residuals"]}
                require(len(candidate["residuals"]) == len(keys) == 24554,
                        "residual key universe changed")
            except (KeyError, RuntimeError, TypeError, ValueError):
                return True
            return False

        for label, mutate in (
            ("kernel count", lambda value: value.__setitem__("kernel_total", 313)),
            ("frontier count", lambda value: value.__setitem__("frontier_target_total", 319201)),
            ("theorem promotion", lambda value: value.__setitem__("full_theorem", True)),
            ("deleted residual", lambda value: value["residuals"].pop()),
            ("duplicate residual", lambda value: value["residuals"].append(
                copy.deepcopy(value["residuals"][0]))),
        ):
            candidate = copy.deepcopy(census)
            mutate(candidate)
            attacks.append((label, candidate))
        require(all(rejected(candidate) for _, candidate in attacks),
                "hostile census mutation accepted")
        return len(attacks)
    engine = load_module(ENGINE_PATH, "rank6_order7_hostile_engine")
    payload = json.loads(paths[0].read_text(encoding="ascii"))
    attacks = []

    def add(label, mutate):
        candidate = copy.deepcopy(payload)
        mutate(candidate)
        attacks.append((label, candidate))

    add("theorem promotion", lambda value: value.__setitem__("full_theorem", True))
    add("wrong census", lambda value: value.__setitem__("source_census_sha256", "0" * 64))
    add("forged count", lambda value: value.__setitem__("exact_certificate_total", -1))
    add("duplicate target", lambda value: value["records"].append(copy.deepcopy(value["records"][0])))
    add("source drift", lambda value: value["records"][0].__setitem__("source_index", 24554))
    rejected = 0
    for label, candidate in attacks:
        try:
            engine.verify(candidate)
            local = {}
            for record in candidate["records"]:
                require(key(record) not in local, "duplicate target")
                local[key(record)] = record
        except (IndexError, KeyError, RuntimeError, TypeError, ValueError, ZeroDivisionError):
            rejected += 1
            continue
        raise RuntimeError(f"hostile mutation accepted: {label}")
    return rejected


def format_report(report, hostile):
    status = "PROVED" if report["theorem"] else "OPEN"
    return "\n".join((
        "rank-six order-seven frontier audit passed",
        "kernels=314 physical=700792 orbits=519453 coarse=494899 residuals=24554",
        f"frontier_targets=319202 loaded={report['loaded']} missing={report['missing']}",
        f"rational={report['rational']} structural={report['structural']} "
        f"finite_unresolved={report['unresolved']}",
        f"rejected_hostile_mutations={hostile}",
        f"theorem_status={status}",
    )) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("chunks", nargs="*", type=Path)
    parser.add_argument("--structural", type=Path)
    parser.add_argument("--emit", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    report = audit_payloads(args.chunks, args.structural)
    hostile = hostile_checks(args.chunks)
    output = format_report(report, hostile)
    if sys.flags.optimize == 0 and not args.emit:
        command = [sys.executable, "-O", __file__, "--emit"]
        command.extend(str(path) for path in args.chunks)
        if args.structural is not None:
            command.extend(("--structural", str(args.structural)))
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        require(completed.returncode == 0 and completed.stderr == "", "optimized verifier failed")
        require(completed.stdout == output, "normal and optimized outputs differ")
    sys.stdout.write(output)


if __name__ == "__main__":
    main()
