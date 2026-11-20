#!/usr/bin/env python3
"""Read-only fail-closed verifier for the retained family-S h=1 package.

Trust boundary
--------------
* Git (or another external transport) authenticates this verifier and the
  package tree.  SHA256SUMS is an internal integrity map, not a signature and
  not self-authentication.
* The separately authored ``check_h1_selector_parent.py`` independently
  reconstructs the complete row universe, CNF variable order and clause stream.
* ``check_h1_composite_bridge.py`` exhausts the 742,320 V4/pair bridge cases,
  including the full ordinary-A/B type-sorting relabelling under C exchange.
* UNSAT validity comes only from the retained, identity-pinned ``drat-trim``
  replay of the retained CNF and decompressed DRAT proof.
* The retained CaDiCaL binary is optional proof-reproduction provenance.  This
  default verifier neither executes nor requires a SAT solver result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import os
import platform
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
MANIFEST_PATH = PACKAGE / "metadata" / "manifest.json"
SUMS_PATH = PACKAGE / "metadata" / "SHA256SUMS"
SCHEMA = "seymour-family-s-h1-certificate-v1"
HEX64 = re.compile(r"[0-9a-f]{64}\Z")

REQUIRED_DIRS = frozenset({
    ".",
    "artifacts",
    "ledger",
    "metadata",
    "tools",
    "verifier",
})

REQUIRED_FILES = frozenset({
    "README.md",
    "artifacts/h1-parent.cnf",
    "artifacts/h1-parent.drat.xz",
    "ledger/ordered-rows.json",
    "metadata/SHA256SUMS",
    "metadata/manifest.json",
    "tools/BUILD.md",
    "tools/cadical-1.7.3",
    "tools/cadical-LICENSE",
    "tools/drat-trim",
    "tools/drat-trim-LICENSE",
    "tools/drat-trim.c",
    "verifier/check_h1_composite_bridge.py",
    "verifier/check_h1_selector_parent.py",
    "verifier/hostile_mutations.py",
    "verifier/reproduce_proof.py",
    "verifier/verify_h1_package.py",
})

EXECUTABLES = frozenset({
    "tools/cadical-1.7.3",
    "tools/drat-trim",
    "verifier/check_h1_composite_bridge.py",
    "verifier/check_h1_selector_parent.py",
    "verifier/hostile_mutations.py",
    "verifier/reproduce_proof.py",
    "verifier/verify_h1_package.py",
})

IDENTITY_KEYS = {
    "artifacts/h1-parent.cnf": "cnf",
    "artifacts/h1-parent.drat.xz": "proof_xz",
    "ledger/ordered-rows.json": "ordered_ledger",
    "tools/cadical-1.7.3": "solver_binary",
    "tools/drat-trim": "proof_checker_binary",
    "tools/drat-trim.c": "proof_checker_source",
    "verifier/check_h1_composite_bridge.py": "composite_bridge_source",
    "verifier/check_h1_selector_parent.py": "independent_checker_source",
    "verifier/hostile_mutations.py": "hostile_mutations_source",
    "verifier/reproduce_proof.py": "proof_reproducer_source",
    "verifier/verify_h1_package.py": "package_verifier_source",
}

EXPECTED = {
    "scope": "order-18 seven-hole shared-low family-S h=1 cell only; no vertex or arc minimality",
    "cnf": {
        "bytes": 5_891_576,
        "sha256": "31db9866c15372555f9c102b3126fb4e8730f879b5e82ca5f6791318398d4e43",
        "variables": 25_211,
        "clauses": 330_705,
    },
    "ledger": {
        "bytes": 89_912,
        "sha256": "9c82a2a1fbe44872278cc4d6fe71abd53c359d6cbf9e85eac9262986721e61fe",
        "ordered_universe_sha256": "d713ca11b98de20010c923bf1cbe756230d2c9728834ffab51fb65c39068131f",
    },
    "proof_xz": {
        "bytes": 2_471_364,
        "sha256": "089e6ded1354db86151092c0603ca1d8aa5397bf7b4b7916c71ad6830375eaba",
    },
    "proof_raw": {
        "bytes": 30_989_483,
        "sha256": "32f35d5b3b0458c05f59bcf4467f3bb40103294e0100d7ba8276c2972cfa9de9",
    },
    "checker": {
        "bytes": 51_216,
        "sha256": "92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a",
        "source_bytes": 59_546,
        "source_sha256": "d834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee",
        "source_commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
        "source_tree": "b4e75a5f8c89d664652727458369cb5e0b610e31",
        "source_blob": "cf8a676ffcc7ef5a47124bbafc9b680a2df333e0",
        "build_id": "83768248f9562e7a5b87b8530e078148fe0b62a6",
    },
    "solver": {
        "bytes": 1_002_216,
        "sha256": "ff471d3c6b54fbbc161d65545a5f788d0032ad05b9aff4e2c748d9639400e951",
        "source_commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
        "build_id": "560ab92678327747ed4dae62010a6481075fe9b5",
    },
    "counts": {
        "pre_v4_rows": 6_186,
        "v4_rows": 1_919,
        "composite_cases": 742_320,
        "composite_mapping_witnesses": 921_120,
        "pair_orbits": 61_696,
        "guarded_nonrepresentatives": 168_584,
        "labelled_states": 14_428_260,
        "labelled_v4_orbits": 4_763_052,
        "pair_orbit_sha256": "922c184dcfaa6dc2fc2ae613b93b7e2b092a797faeeab9956f8865e44bdabb98",
        "full_canonicalizing_map_sha256": "c8b8cc8696ac80cb89f6774cdf1a7ea1cd051c9516d3e0be809aa5fe4d37bcc2",
    },
}


def fail(message: str) -> None:
    raise RuntimeError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def safe_rel(text: str) -> str:
    require(type(text) is str and text, "empty or non-string package path")
    path = PurePosixPath(text)
    require(
        not path.is_absolute()
        and "\\" not in text
        and str(path) == text
        and all(part not in ("", ".", "..") for part in path.parts),
        f"unsafe package path: {text!r}",
    )
    return text


def identity(path: Path) -> dict[str, object]:
    hasher = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            size += len(chunk)
            hasher.update(chunk)
    return {"bytes": size, "sha256": hasher.hexdigest()}


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key {key!r}")
        output[key] = value
    return output


def load_canonical_json(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    require(raw.endswith(b"\n") and b"\r" not in raw, f"noncanonical JSON line endings: {path}")
    try:
        value = json.loads(
            raw.decode("ascii"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(f"nonfinite JSON {token}")),
        )
    except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
        fail(f"manifest read/parse failed: {exc}")
    require(type(value) is dict, "manifest root is not an object")
    canonical = (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode("ascii")
    require(raw == canonical, "manifest is not exact canonical sorted ASCII JSON")
    return value


def exact_tree() -> None:
    found_files: set[str] = set()
    found_dirs: set[str] = set()
    inode_owners: dict[tuple[int, int], str] = {}
    for root, dirs, files in os.walk(PACKAGE, topdown=True, followlinks=False):
        root_path = Path(root)
        root_info = root_path.lstat()
        require(stat.S_ISDIR(root_info.st_mode) and not root_path.is_symlink(), f"non-directory package entry: {root_path}")
        require(root_info.st_nlink >= 2, f"invalid directory link count: {root_path}")
        root_rel = root_path.relative_to(PACKAGE).as_posix()
        found_dirs.add("." if root_rel == "." else safe_rel(root_rel))
        for name in dirs:
            path = root_path / name
            require(not path.is_symlink(), f"symlink directory forbidden: {path}")
        for name in files:
            path = root_path / name
            info = path.lstat()
            require(stat.S_ISREG(info.st_mode) and not path.is_symlink(), f"nonregular file: {path}")
            require(info.st_nlink == 1, f"regular file has unexpected hard links: {path}")
            key = (info.st_dev, info.st_ino)
            require(key not in inode_owners, f"package files share an inode: {inode_owners.get(key)} and {path}")
            inode_owners[key] = path.relative_to(PACKAGE).as_posix()
            found_files.add(safe_rel(path.relative_to(PACKAGE).as_posix()))
    require(
        found_dirs == REQUIRED_DIRS,
        f"package directories differ: missing={sorted(REQUIRED_DIRS-found_dirs)} extra={sorted(found_dirs-REQUIRED_DIRS)}",
    )
    require(
        found_files == REQUIRED_FILES,
        f"package tree differs: missing={sorted(REQUIRED_FILES-found_files)} extra={sorted(found_files-REQUIRED_FILES)}",
    )
    for rel in REQUIRED_DIRS:
        path = PACKAGE if rel == "." else PACKAGE / rel
        mode = stat.S_IMODE(path.lstat().st_mode)
        require(mode == 0o755, f"directory mode mismatch {rel}: {oct(mode)} != 0o755")
    for rel in REQUIRED_FILES:
        mode = stat.S_IMODE((PACKAGE / rel).lstat().st_mode)
        expected = 0o755 if rel in EXECUTABLES else 0o644
        require(mode == expected, f"mode mismatch {rel}: {oct(mode)} != {oct(expected)}")


def verify_sums() -> None:
    raw = SUMS_PATH.read_bytes()
    require(raw.endswith(b"\n") and b"\r" not in raw, "SHA256SUMS line endings changed")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeError as exc:
        fail(f"SHA256SUMS is not ASCII: {exc}")
    expected_paths = sorted(REQUIRED_FILES - {"metadata/SHA256SUMS"})
    require(len(lines) == len(expected_paths), "SHA256SUMS row count changed")
    seen: list[str] = []
    for line, expected_path in zip(lines, expected_paths):
        require(len(line) > 66 and line[64:66] == "  ", "malformed SHA256SUMS row")
        digest, rel = line[:64], safe_rel(line[66:])
        require(HEX64.fullmatch(digest) is not None, "malformed SHA-256 digest")
        require(rel == expected_path, "SHA256SUMS paths are not exact sorted package paths")
        require(identity(PACKAGE / rel)["sha256"] == digest, f"SHA256SUMS mismatch: {rel}")
        seen.append(rel)
    require(seen == expected_paths, "SHA256SUMS path cover changed")


def type_exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(
            type_exact_equal(left[key], right[key]) for key in left
        )
    if type(left) is list:
        return len(left) == len(right) and all(
            type_exact_equal(a, b) for a, b in zip(left, right)
        )
    return left == right


def exact_object(value: object, keys: set[str], label: str) -> dict[str, object]:
    require(type(value) is dict, f"{label} is not an object")
    require(set(value) == keys, f"{label} keys changed")
    return value


def exact_int(value: object, label: str, minimum: int = 0) -> int:
    require(type(value) is int and value >= minimum, f"{label} is not an exact integer")
    return value


def exact_hash(value: object, label: str) -> str:
    require(type(value) is str and HEX64.fullmatch(value) is not None, f"{label} is not SHA-256")
    return value


def verify_manifest(manifest: dict[str, object]) -> None:
    top = {
        "schema", "status", "scope", "exclusions", "requirements", "cnf",
        "ordered_ledger", "mathematical_counts", "proof", "proof_checker",
        "proof_producer", "identities", "safe_artifact_paths", "trust",
    }
    exact_object(manifest, top, "manifest")
    require(manifest["schema"] == SCHEMA, "manifest schema changed")
    require(manifest["status"] == "retained-finite-certificate", "manifest status changed")
    require(manifest["scope"] == EXPECTED["scope"], "manifest scope changed")
    require(
        manifest["exclusions"] == [
            "family-S h=0",
            "other m=7 families",
            "all order-18 oriented graphs",
            "Seymour's Second Neighborhood Conjecture",
        ],
        "manifest exclusions changed",
    )
    require(
        type_exact_equal(
            manifest["requirements"],
            {
                "bash": "required only for the documented command wrapper/build recipe",
                "os": "GNU/Linux",
                "architecture": "x86-64",
                "libc": "glibc",
                "python": ">=3.10",
            },
        ),
        "runtime requirements changed",
    )
    require(type_exact_equal(manifest["cnf"], EXPECTED["cnf"]), "CNF metadata changed")
    require(type_exact_equal(manifest["ordered_ledger"], EXPECTED["ledger"]), "ledger metadata changed")
    require(type_exact_equal(manifest["mathematical_counts"], EXPECTED["counts"]), "mathematical counts changed")
    require(
        type_exact_equal(
            manifest["proof"],
            {
                "format": "binary DRAT compressed as deterministic Python lzma XZ preset 9",
                "raw": EXPECTED["proof_raw"],
                "xz": EXPECTED["proof_xz"],
            },
        ),
        "proof metadata changed",
    )
    checker = exact_object(
        manifest["proof_checker"],
        {"name", "role", "source_commit", "source_tree", "source_blob", "source", "binary", "elf_build_id", "required_exit", "required_markers"},
        "proof_checker",
    )
    require(
        type_exact_equal(
            checker,
            {
                "name": "drat-trim",
                "role": "proof validity",
                "source_commit": EXPECTED["checker"]["source_commit"],
                "source_tree": EXPECTED["checker"]["source_tree"],
                "source_blob": EXPECTED["checker"]["source_blob"],
                "source": {"bytes": EXPECTED["checker"]["source_bytes"], "sha256": EXPECTED["checker"]["source_sha256"]},
                "binary": {"bytes": EXPECTED["checker"]["bytes"], "sha256": EXPECTED["checker"]["sha256"]},
                "elf_build_id": EXPECTED["checker"]["build_id"],
                "required_exit": 0,
                "required_markers": ["c detected empty clause", "s VERIFIED"],
            },
        ),
        "proof-checker metadata changed",
    )
    require(
        type_exact_equal(
            manifest["proof_producer"],
            {
                "name": "CaDiCaL",
                "version": "1.7.3",
                "role": "optional deterministic proof reproduction; not used by default verifier",
                "source_commit": EXPECTED["solver"]["source_commit"],
                "binary": {"bytes": EXPECTED["solver"]["bytes"], "sha256": EXPECTED["solver"]["sha256"]},
                "elf_build_id": EXPECTED["solver"]["build_id"],
                "required_unsat_exit": 20,
            },
        ),
        "proof-producer metadata changed",
    )
    require(
        manifest["safe_artifact_paths"] == [
            "artifacts/h1-parent.cnf",
            "artifacts/h1-parent.drat.xz",
        ],
        "safe artifact path list changed",
    )
    require(
        type_exact_equal(
            manifest["trust"],
            {
                "external_anchor": "Git commit/tree containing this package; SHA256SUMS is an internal integrity map, not a signature",
                "independence_boundary": "the independent checker reconstructs the full h=1 row universe and complete CNF without importing a producer; the composite checker separately exhausts the V4-to-row-stabilizer bridge with full ordinary-A/B type-sorting relabelling under C exchange",
            },
        ),
        "trust-boundary metadata changed",
    )

    identities = exact_object(manifest["identities"], set(IDENTITY_KEYS.values()), "identities")
    for rel, key in IDENTITY_KEYS.items():
        entry = exact_object(identities[key], {"bytes", "sha256"}, f"identity {key}")
        exact_int(entry["bytes"], f"identity {key} bytes")
        exact_hash(entry["sha256"], f"identity {key} sha256")
        require(identity(PACKAGE / rel) == entry, f"manifest identity mismatch: {rel}")


def require_runtime() -> None:
    require(sys.version_info >= (3, 10), "Python 3.10 or newer is required")
    require(platform.system() == "Linux", "retained proof-checker binary requires Linux")
    require(platform.machine() in ("x86_64", "AMD64"), "retained binaries require x86-64")
    libc_name, _ = platform.libc_ver()
    require(libc_name == "glibc", f"retained binaries require glibc, observed {libc_name!r}")


def run_python(script: Path, *arguments: str, timeout: int = 600) -> str:
    command = [sys.executable, "-O", "-B", str(script), *arguments]
    result = subprocess.run(
        command,
        cwd=PACKAGE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=timeout,
    )
    require(result.returncode == 0, f"command failed {command}:\n{result.stdout[-4000:]}")
    return result.stdout


def reconstruct_and_compare() -> tuple[str, str]:
    checker = PACKAGE / "verifier" / "check_h1_selector_parent.py"
    cnf = PACKAGE / "artifacts" / "h1-parent.cnf"
    ledger = PACKAGE / "ledger" / "ordered-rows.json"
    with tempfile.TemporaryDirectory(prefix="h1-package-reconstruct-") as directory:
        reconstructed = Path(directory) / "h1-parent.cnf"
        output = run_python(
            checker,
            "--write-reconstruction", str(reconstructed),
            "--ordered-ledger", str(ledger),
        )
        require(
            "PASS wrote independent reconstruction vars=25211 clauses=330705" in output,
            "independent reconstruction did not report exact dimensions",
        )
        # EXPECTED['cnf'] also includes dimensions; compare its byte identity explicitly.
        require(
            identity(reconstructed) == {"bytes": EXPECTED["cnf"]["bytes"], "sha256": EXPECTED["cnf"]["sha256"]},
            "independently reconstructed CNF identity changed",
        )
        require(reconstructed.read_bytes() == cnf.read_bytes(), "retained CNF differs from independent reconstruction")
    checked = run_python(checker, str(cnf), "--ordered-ledger", str(ledger))
    require("PASS independent h1 selector-parent rows=1919" in checked, "independent CNF check marker absent")
    return output, checked


def run_composite_bridge() -> str:
    output = run_python(PACKAGE / "verifier" / "check_h1_composite_bridge.py", timeout=600)
    require(
        "PASS composite V4-to-row-stabilizer bridge pre_rows=6186 cases=742320" in output
        and "PASS explicit composite mapping witnesses=921120 canonical_pair_orbits=61696" in output
        and "PASS full type-sorting canonicalizing maps digest=c8b8cc8696ac80cb89f6774cdf1a7ea1cd051c9516d3e0be809aa5fe4d37bcc2 regression=row3-c-0,13-to-0,14" in output,
        "composite bridge acceptance markers absent",
    )
    return output


def replay_proof() -> str:
    cnf = PACKAGE / "artifacts" / "h1-parent.cnf"
    packed_path = PACKAGE / "artifacts" / "h1-parent.drat.xz"
    checker = PACKAGE / "tools" / "drat-trim"
    require(identity(cnf) == {"bytes": EXPECTED["cnf"]["bytes"], "sha256": EXPECTED["cnf"]["sha256"]}, "CNF identity changed")
    require(identity(packed_path) == EXPECTED["proof_xz"], "compressed proof identity changed")
    require(identity(checker) == {"bytes": EXPECTED["checker"]["bytes"], "sha256": EXPECTED["checker"]["sha256"]}, "checker identity changed")
    require(os.access(checker, os.X_OK), "proof checker is not executable")

    with tempfile.TemporaryDirectory(prefix="h1-package-replay-") as directory:
        raw_path = Path(directory) / "h1-parent.drat"
        hasher = hashlib.sha256()
        size = 0
        try:
            with lzma.open(packed_path, "rb") as source, raw_path.open("wb") as target:
                while chunk := source.read(1 << 20):
                    target.write(chunk)
                    hasher.update(chunk)
                    size += len(chunk)
        except (OSError, lzma.LZMAError) as exc:
            fail(f"proof decompression failed: {exc}")
        require(
            {"bytes": size, "sha256": hasher.hexdigest()} == EXPECTED["proof_raw"],
            "raw proof identity changed",
        )
        result = subprocess.run(
            [str(checker), str(cnf), str(raw_path)],
            cwd=PACKAGE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=300,
        )
        output = result.stdout
        require(result.returncode == 0, f"drat-trim exit {result.returncode}:\n{output[-4000:]}")
        require(output.count("c detected empty clause") >= 1, "checker did not detect an empty clause")
        require(output.splitlines().count("s VERIFIED") == 1, "checker did not emit exactly one s VERIFIED")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--identity-only",
        action="store_true",
        help="check exact tree, modes, manifest and all internal file identities only",
    )
    args = parser.parse_args()

    require_runtime()
    exact_tree()
    manifest = load_canonical_json(MANIFEST_PATH)
    verify_manifest(manifest)
    verify_sums()
    if args.identity_only:
        print("PASS identity-only exact tree modes safe paths manifest SHA256SUMS identities")
        return

    reconstruction_output, independent_output = reconstruct_and_compare()
    composite_output = run_composite_bridge()
    replay_output = replay_proof()

    print("PASS exact tree modes safe paths canonical manifest SHA256SUMS")
    print(reconstruction_output, end="")
    print(independent_output, end="")
    print(composite_output, end="")
    # Preserve only the decisive proof-checker lines in the package verifier output.
    for line in replay_output.splitlines():
        if line in ("c detected empty clause; start verification via backward checking", "s VERIFIED"):
            print(line)
    print(
        "PASS authenticated DRAT replay "
        f"raw_bytes={EXPECTED['proof_raw']['bytes']} raw_sha256={EXPECTED['proof_raw']['sha256']}"
    )
    print(
        "PASS retained family-S h1 finite certificate; exclusions=h0,other-m7,all-order18,SNC"
    )


if __name__ == "__main__":
    try:
        main()
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, lzma.LZMAError, subprocess.TimeoutExpired, RuntimeError) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
