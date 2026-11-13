#!/usr/bin/env python3
"""Exact genuine-isomorphism transport audit for the exceptional doubled-C4 orbit."""

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE_VERIFIER = HERE / "doubled-c4-64-row-exact-verifier.py"
BASE_VERIFIER_SHA256 = "3849b3aef7ded9ed9abfe046f08b4e1ba292068232000172be9fee6ee646d9e8"
PACKET = (ROOT / "positive-square-energy" / "pentacyclic-general"
          / "doubled-c4-111-two-triangles-retained-packet.md")
PACKET_SHA256 = "ee760d3de23902bcabd2fb7844bce971a30c4aed04034fbf842f44268772ecf4"

PATH_NAMES = ("a", "A", "b", "c", "C", "d")
BASE_ROW = "010011"
BASE_EVEN_CONNECTOR = 2
BASE_ODD_CONNECTOR = 5
BASE_EVEN_DOUBLED = (0, 3)
BASE_OWNER_ROLES = ("branch", "branch", "branch", "branch",
                    "even-doubled-interior", "even-doubled-interior")
EXCEPTIONAL_ROWS = (
    "010011", "010101", "011010", "011100",
    "100011", "100101", "101010", "101100",
)
EXPECTED_CLASSES = {
    "010011": "111", "010101": "110", "011010": "111", "011100": "110",
    "100011": "110", "100101": "111", "101010": "110", "101100": "111",
}
SCHEMA = "doubled-c4-exceptional-owner-transport-v1"
EXPECTED_MANIFEST_SHA256 = "ba504e0ead31921b7c5b9c2c220b423fc92c100cd54b53da7f236038d504f073"
EXPECTED_NORMAL_OUTPUT_SHA256 = "2b11fb34c05eace618796558f1220cd3e17d1aaac4c173609a04f7b18a6ce2b0"
EXPECTED_OPTIMIZED_OUTPUT_SHA256 = "2b11fb34c05eace618796558f1220cd3e17d1aaac4c173609a04f7b18a6ce2b0"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_bytes(payload):
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


def check_packet(path=PACKET, digest=PACKET_SHA256):
    require(path == PACKET, "retained packet path changed")
    require(digest == PACKET_SHA256, "retained packet digest policy changed")
    require(path.is_file(), "missing retained packet")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
            "retained packet changed")
    text = path.read_text(encoding="ascii")
    required = (*EXCEPTIONAL_ROWS, "class `110`", "class `111`",
                "physical graph-isomorphism transport",
                "Arbitrary connector-only lengthening")
    require(all(token in text for token in required),
            "retained packet semantic transport ledger changed")
    return {"path": str(path.relative_to(ROOT)), "sha256": digest}


def load_base(path=BASE_VERIFIER, digest=BASE_VERIFIER_SHA256):
    require(path == BASE_VERIFIER, "base verifier path changed")
    require(digest == BASE_VERIFIER_SHA256, "base verifier digest policy changed")
    require(path.is_file(), "missing doubled-C4 exact verifier")
    require(hashlib.sha256(path.read_bytes()).hexdigest() == digest,
            "doubled-C4 exact verifier changed")
    spec = importlib.util.spec_from_file_location("doubled_c4_exact", path)
    require(spec is not None and spec.loader is not None, "cannot load doubled-C4 exact verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def switch_row(row, mask, endpoints):
    return "".join(str(int(bit) ^ ((mask >> u) & 1) ^ ((mask >> v) & 1))
                   for bit, (u, v) in zip(row, endpoints))


def switching_class(row, endpoints):
    classes = set()
    for mask in range(16):
        switched = switch_row(row, mask, endpoints)
        if switched[0] == switched[2] == switched[3] == "0":
            classes.add(switched[1] + switched[4] + switched[5])
    require(len(classes) == 1, f"switching normalization is not unique: {row}")
    return classes.pop()


def role_record(row, vertex_map, edge_map, module):
    require(module.act_on_row(BASE_ROW, edge_map) == row,
            f"witness does not map base row to {row}")
    lengths = module.first_simple_lengths(row)
    image_even_connector = edge_map[BASE_EVEN_CONNECTOR]
    image_odd_connector = edge_map[BASE_ODD_CONNECTOR]
    image_even_doubled = tuple(sorted(edge_map[index] for index in BASE_EVEN_DOUBLED))
    require(lengths[image_even_connector] == 2,
            f"{row}: transported even connector is not even first-simple")
    require(lengths[image_odd_connector] == 1,
            f"{row}: transported odd connector is not odd first-simple")
    require(all(lengths[index] == 2 for index in image_even_doubled),
            f"{row}: transported doubled owner is not an even member")
    require({module.ENDPOINTS[index] for index in image_even_doubled} ==
            {(0, 1), (2, 3)}, f"{row}: transported owners do not span both doubled fibres")
    require(sorted(vertex_map) == list(range(4)), f"{row}: branch map is not bijective")
    return {
        "row": row,
        "switching_class": switching_class(row, module.ENDPOINTS),
        "first_simple_lengths": list(lengths),
        "vertex_map": list(vertex_map),
        "edge_map": list(edge_map),
        "path_image": [PATH_NAMES[index] for index in edge_map],
        "even_connector": PATH_NAMES[image_even_connector],
        "odd_connector": PATH_NAMES[image_odd_connector],
        "even_doubled_members": [PATH_NAMES[index] for index in image_even_doubled],
        "owner_roles": list(BASE_OWNER_ROLES),
        "transported_predicates": [
            "branch-owner-bijection",
            "even-doubled-interior-owner-bijection",
            "even-connector-opening",
            "odd-connector-cut",
            "direct/direct-incidence",
            "direct/nested-incidence",
            "repeated-owner-incidence",
            "rooted-descendant-bijection",
            "induced-territory-partition",
        ],
    }


def transport_manifest(rows=EXCEPTIONAL_ROWS, expected_classes=EXPECTED_CLASSES,
                       expected_digest=EXPECTED_MANIFEST_SHA256):
    require(rows == EXCEPTIONAL_ROWS, "exceptional orbit row registry changed")
    require(expected_classes == EXPECTED_CLASSES, "switching-class ledger changed")
    module = load_base()
    packet = check_packet()
    automorphisms = module.genuine_kernel_automorphisms()
    require(len(automorphisms) == 16, "genuine incidence automorphism count changed")
    require(len({vertex_map for vertex_map, unused_edge_map in automorphisms}) == 4,
            "genuine vertex automorphism count changed")

    orbit = {module.act_on_row(BASE_ROW, edge_map)
             for unused_vertex_map, edge_map in automorphisms}
    require(orbit == set(rows), "base-row genuine orbit is not the exact exceptional set")

    records = []
    for row in rows:
        witnesses = sorted((vertex_map, edge_map) for vertex_map, edge_map in automorphisms
                           if module.act_on_row(BASE_ROW, edge_map) == row)
        require(len(witnesses) == 2, f"{row}: genuine witness multiplicity changed")
        records.append(role_record(row, *witnesses[0], module))
    require({record["switching_class"] for record in records} == {"110", "111"},
            "exceptional orbit switching split collapsed")
    require(sum(record["switching_class"] == "110" for record in records) == 4 and
            sum(record["switching_class"] == "111" for record in records) == 4,
            "exceptional orbit is not split 4+4 across classes 110 and 111")
    require(all(record["switching_class"] == expected_classes[record["row"]]
                for record in records), "switching-class assignment changed")

    manifest = {
        "schema": SCHEMA,
        "base_verifier_sha256": BASE_VERIFIER_SHA256,
        "retained_packet": packet,
        "base_row": BASE_ROW,
        "orbit_size": len(records),
        "incidence_automorphisms": len(automorphisms),
        "vertex_automorphisms": 4,
        "switching_class_counts": {"110": 4, "111": 4},
        "transport_kind": "genuine-physical-kernel-isomorphism-not-switching",
        "scope": {
            "doubled_pairs": "first-simple physical lengths {1,2}",
            "connectors": "arbitrary same-parity lengths, one even and one odd",
            "owners": "four branch vertices plus interiors of the two even doubled members",
            "incidence": "direct/direct or direct/nested, including repeated owners and rooted trees",
        },
        "conclusion": "normalized owner opening and induced territories transport to all eight anchors",
        "records": records,
    }
    digest = hashlib.sha256(canonical_bytes(manifest)).hexdigest()
    require(expected_digest == EXPECTED_MANIFEST_SHA256, "manifest digest policy changed")
    require(digest == expected_digest, "canonical owner-transport manifest changed")
    return manifest, digest


def expect_rejected(action, label):
    try:
        action()
    except (IndexError, KeyError, OSError, RuntimeError, StopIteration, TypeError, ValueError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    checks = 0
    expect_rejected(lambda: load_base(digest="0" * 64), "base verifier digest")
    checks += 1
    expect_rejected(lambda: check_packet(digest="0" * 64), "retained packet digest")
    checks += 1
    expect_rejected(lambda: transport_manifest(rows=EXCEPTIONAL_ROWS[:-1]), "missing anchor")
    checks += 1
    classes = dict(EXPECTED_CLASSES)
    classes["010011"] = "110"
    expect_rejected(lambda: transport_manifest(expected_classes=classes), "wrong switching class")
    checks += 1
    expect_rejected(lambda: transport_manifest(expected_digest="0" * 64), "manifest digest")
    checks += 1
    return checks


def acceptance_report(digest, rejected):
    return "\n".join((
        "doubled-C4 exceptional owner-transport verifier: all exact audits passed",
        "orbit: 8 anchors under 16 genuine incidence automorphisms",
        "switching_split: class 110=4; class 111=4",
        "owner_transport: branch vertices + two even doubled-member interiors",
        "incidence_transport: direct/direct + direct/nested + repeated owners + rooted descendants",
        "connector_scope: arbitrary same-parity lengths; no switching operation",
        f"canonical_transport_manifest_sha256: {digest}",
        f"rejected_hostile_mutations: {rejected}",
    )) + "\n"


def optimized_output():
    completed = subprocess.run((sys.executable, "-O", str(Path(__file__).resolve()), "--emit"),
                               check=False, capture_output=True, text=True)
    require(completed.returncode == 0, "python -O owner-transport verifier failed")
    require(completed.stderr == "", "python -O owner-transport verifier wrote stderr")
    return completed.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--print-manifest", action="store_true")
    args = parser.parse_args()
    manifest, digest = transport_manifest()
    rejected = hostile_self_checks()
    require(rejected == 5, "hostile mutation count changed")
    output = acceptance_report(digest, rejected)
    expected_output = (EXPECTED_OPTIMIZED_OUTPUT_SHA256 if sys.flags.optimize
                       else EXPECTED_NORMAL_OUTPUT_SHA256)
    require(hashlib.sha256(output.encode("ascii")).hexdigest() == expected_output,
            "canonical output digest changed")
    if not args.emit and not args.print_manifest and sys.flags.optimize == 0:
        require(optimized_output() == output, "normal and python -O output differ")
    if args.print_manifest:
        sys.stdout.write(canonical_bytes(manifest).decode("ascii"))
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
