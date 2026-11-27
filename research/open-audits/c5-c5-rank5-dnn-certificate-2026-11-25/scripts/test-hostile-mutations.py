#!/usr/bin/env python3
"""Hostile fail-closed mutation tests for the exact certificate verifier."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
VERIFIER = Path("scripts/verify-certificates.py")


class TestFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise TestFailure(message)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def manifest_entries(root: Path):
    entries = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name == "SHA256SUMS" or "__pycache__" in path.parts:
            continue
        entries.append((path.relative_to(root).as_posix(), sha256(path)))
    return entries


def rewrite_manifest(root: Path) -> None:
    text = "".join(f"{digest}  {name}\n" for name, digest in manifest_entries(root))
    (root / "SHA256SUMS").write_text(text, encoding="ascii")


def strict_load(path: Path):
    def pairs_hook(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"fixture unexpectedly has duplicate key {key!r}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=pairs_hook)


def dump(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(root: Path):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(VERIFIER)],
        cwd=root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def mutate_json(root: Path, relative: str, mutator) -> None:
    path = root / relative
    value = strict_load(path)
    mutator(value)
    dump(path, value)
    rewrite_manifest(root)


def insert_duplicate_schema(root: Path) -> None:
    path = root / "data/n8-multiblock-route-witness.json"
    raw = path.read_text(encoding="utf-8")
    require(raw.startswith("{"), "witness JSON does not start with object")
    path.write_text(
        '{"schema":"attacker-shadow-schema",' + raw[1:],
        encoding="utf-8",
    )
    rewrite_manifest(root)


def manifest_self_member(root: Path) -> None:
    manifest = root / "SHA256SUMS"
    with manifest.open("a", encoding="ascii") as stream:
        stream.write("0" * 64 + "  SHA256SUMS\n")


def manifest_traversal(root: Path) -> None:
    manifest = root / "SHA256SUMS"
    lines = manifest.read_text(encoding="ascii").splitlines()
    digest, _name = lines[0].split("  ", 1)
    lines[0] = f"{digest}  ../escape"
    manifest.write_text("\n".join(lines) + "\n", encoding="ascii")


def extra_unlocked_file(root: Path) -> None:
    (root / "UNLOCKED").write_text("attacker\n", encoding="ascii")


def delete_networkx_license(root: Path) -> None:
    (root / "THIRD-PARTY-NETWORKX-3.7-LICENSE.txt").unlink()
    rewrite_manifest(root)


def mutate_networkx_license(root: Path) -> None:
    path = root / "THIRD-PARTY-NETWORKX-3.7-LICENSE.txt"
    path.write_bytes(path.read_bytes().replace(b"3-clause BSD", b"altered BSD", 1))
    rewrite_manifest(root)


def mutate_enum_n_bool(root: Path) -> None:
    mutate_json(root, "data/atlas-rank5-enumeration.json",
                lambda value: value["records"][0].__setitem__("n", True))


def mutate_enum_n_string(root: Path) -> None:
    mutate_json(root, "data/atlas-rank5-enumeration.json",
                lambda value: value["records"][0].__setitem__("n", "5"))


def mutate_enum_selected_int(root: Path) -> None:
    mutate_json(root, "data/atlas-rank5-enumeration.json",
                lambda value: value["records"][0].__setitem__("selected_bridge_free_core", 1))


def mutate_fraction_int(root: Path) -> None:
    mutate_json(root, "data/atlas-rank5-rational-gram-certificates.json",
                lambda value: value["records"][0].__setitem__("edge_cost", 1))


def mutate_fraction_bool(root: Path) -> None:
    mutate_json(root, "data/atlas-rank5-rational-gram-certificates.json",
                lambda value: value["records"][0]["rational_gram_matrix"][0].__setitem__(0, True))


def mutate_fraction_noncanonical(root: Path) -> None:
    mutate_json(root, "data/atlas-rank5-rational-gram-certificates.json",
                lambda value: value["records"][0]["rational_gram_matrix"][0].__setitem__(0, "2/2"))


def mutate_unknown_field(root: Path) -> None:
    mutate_json(root, "data/atlas-rank5-enumeration.json",
                lambda value: value["records"][0].__setitem__("attacker_shadow", 5))


def mutate_atlas_exhaustiveness_wording(root: Path) -> None:
    mutate_json(root, "data/atlas-rank5-enumeration.json",
                lambda value: value["source"].__setitem__(
                    "exhaustiveness_assumption", "unconditional exhaustive theorem"))


def mutate_k4_lower_witness(root: Path) -> None:
    mutate_json(root, "data/n8-multiblock-route-witness.json",
                lambda value: value["local_exact_kappa_certificates"]["K4"].__setitem__(
                    "primal", "M=J_4 gives objective 8"))


def mutate_c3_upper_witness(root: Path) -> None:
    mutate_json(root, "data/n8-multiblock-route-witness.json",
                lambda value: value["local_exact_kappa_certificates"]["C3"].__setitem__(
                    "dual_edge_cost", "5"))


def mutate_block_additivity(root: Path) -> None:
    mutate_json(root, "data/n8-multiblock-route-witness.json",
                lambda value: value["center"]["kappa_blocks"][1].__setitem__("kappa", 5))


def mutate_one_vertex_overlap(root: Path) -> None:
    def mutate(value):
        value["center"]["blocks"][1]["vertices"][1] = 1
    mutate_json(root, "data/n8-multiblock-route-witness.json", mutate)


def mutate_route_kappa(root: Path) -> None:
    mutate_json(root, "data/n8-multiblock-route-witness.json",
                lambda value: value["repeated_port_representative"].__setitem__(
                    "exact_kappa", "38-4*sqrt(5)"))


def mutate_repeated_port_type(root: Path) -> None:
    mutate_json(root, "data/n8-multiblock-route-witness.json",
                lambda value: value["repeated_port_representative"]["ports"].__setitem__(0, True))


CASES = (
    ("duplicate-json-key", insert_duplicate_schema, "duplicate JSON key"),
    ("manifest-self-member", manifest_self_member, "must not circularly include itself"),
    ("manifest-traversal", manifest_traversal, "unsafe or noncanonical manifest path"),
    ("manifest-unlocked-file", extra_unlocked_file, "coverage mismatch"),
    ("networkx-license-deletion", delete_networkx_license,
     "NetworkX redistribution license missing from manifest"),
    ("networkx-license-mutation", mutate_networkx_license,
     "NetworkX 3.7 redistribution license SHA-256 mismatch"),
    ("integer-bool-laundering", mutate_enum_n_bool, "must be a JSON integer"),
    ("integer-string-laundering", mutate_enum_n_string, "must be a JSON integer"),
    ("boolean-int-laundering", mutate_enum_selected_int, "must be a JSON boolean"),
    ("fraction-int-laundering", mutate_fraction_int, "must be a JSON string"),
    ("fraction-bool-laundering", mutate_fraction_bool, "must be a JSON string"),
    ("fraction-noncanonical", mutate_fraction_noncanonical, "not reduced canonical rational text"),
    ("unknown-shadow-field", mutate_unknown_field, "fields changed"),
    ("atlas-conditional-wording", mutate_atlas_exhaustiveness_wording,
     "exhaustiveness must remain explicitly conditional"),
    ("k4-lower-witness", mutate_k4_lower_witness, "K4 lower-witness description changed"),
    ("c3-upper-witness", mutate_c3_upper_witness, "stored C3 feasible cost changed"),
    ("block-additivity", mutate_block_additivity, "witness kappa block 1 changed"),
    ("one-vertex-overlap", mutate_one_vertex_overlap, "witness block vertices changed"),
    ("attached-route-arithmetic", mutate_route_kappa, "stored attached route arithmetic changed"),
    ("repeated-port-type", mutate_repeated_port_type, "must be a JSON integer"),
)


def copy_fixture(destination: Path) -> None:
    shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def main() -> None:
    baseline = run(ROOT)
    require(baseline.returncode == 0, "baseline verifier failed: " + baseline.stderr)
    for name, mutator, expected_error in CASES:
        with tempfile.TemporaryDirectory(prefix="c5-c5-hostile-") as temporary:
            fixture = Path(temporary) / "bundle"
            copy_fixture(fixture)
            mutator(fixture)
            result = run(fixture)
            require(result.returncode != 0, f"{name}: hostile mutation was accepted")
            require(expected_error in result.stderr,
                    f"{name}: wrong failure; wanted {expected_error!r}; got {result.stderr!r}")
            require("PASS exact" not in result.stdout, f"{name}: failure emitted PASS")
            print(f"PASS hostile mutation rejected: {name}")
    print(f"PASS hostile suite: {len(CASES)} mutations rejected fail-closed")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL hostile suite: {exc}", file=sys.stderr)
        raise SystemExit(1)
