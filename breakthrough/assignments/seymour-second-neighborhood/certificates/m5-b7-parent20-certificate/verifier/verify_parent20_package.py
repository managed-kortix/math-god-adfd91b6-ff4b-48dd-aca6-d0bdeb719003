#!/usr/bin/env python3
"""Fail-closed replay verifier for the private exact B7 parent-20 package.

Trust boundary:
* This script reconstructs the parent/packet/witness/high-selector universe and
  complete CNF with ``verify_parent20_structure.py``.
* That structural checker is independent of the parent-20 producer/split code
  and selector-suffix builder, but intentionally imports the pinned common
  encoder ``source-pins/snc_cnf.py``.  It binds the common base independently
  to its frozen variable-map and clause-stream hashes; this is not a second
  implementation of the base encoding.
* UNSAT validity is established only by replaying the retained LRAT with the
  identity-pinned checker.  CaDiCaL is retained solely as producer provenance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent
METADATA = PACKAGE / "metadata" / "certificate.json"
MANIFEST = PACKAGE / "metadata" / "SHA256SUMS"
FORMAT = "seymour-snc-b7-parent20-certificate-v1"
CAP = 250_000_000
REQUIRED_FILES = frozenset({
    "artifacts/parent20.cnf",
    "artifacts/parent20.lrat.xz",
    "ledger/m5-b7-parent20-probe.tsv",
    "metadata/SHA256SUMS",
    "metadata/certificate.json",
    "metadata/checker-run.txt",
    "metadata/checker.exit",
    "metadata/checker.stderr",
    "metadata/checker.stdout",
    "metadata/solver-run.txt",
    "metadata/solver.exit",
    "metadata/solver.stderr",
    "metadata/solver.stdout",
    "source-pins/check_m5_selector_batch_cnf.py",
    "source-pins/snc_cnf.py",
    "tools/cadical-1.7.3",
    "tools/cadical-LICENSE",
    "tools/drat-trim-LICENSE",
    "tools/lrat-check",
    "tools/lrat-check.c",
    "verifier/hostile_mutations.py",
    "verifier/verify_parent20_package.py",
    "verifier/verify_parent20_structure.py",
})
EXECUTABLES = frozenset({
    "tools/cadical-1.7.3", "tools/lrat-check",
    "verifier/hostile_mutations.py", "verifier/verify_parent20_package.py",
    "verifier/verify_parent20_structure.py",
})
IDENTITY_FIELDS = {
    "artifacts/parent20.cnf": "cnf",
    "artifacts/parent20.lrat.xz": "lrat_xz",
    "ledger/m5-b7-parent20-probe.tsv": "ledger",
    "source-pins/check_m5_selector_batch_cnf.py": "cover_checker_source",
    "source-pins/snc_cnf.py": "common_encoder_source",
    "tools/cadical-1.7.3": "solver_binary",
    "tools/lrat-check": "checker_binary",
    "tools/lrat-check.c": "checker_source",
    "verifier/hostile_mutations.py": "hostile_mutations_source",
    "verifier/verify_parent20_package.py": "package_verifier_source",
    "verifier/verify_parent20_structure.py": "structural_verifier_source",
}


def identity(path: Path) -> tuple[int, str]:
    h = hashlib.sha256(); n = 0
    with path.open("rb") as f:
        while block := f.read(1 << 20):
            n += len(block); h.update(block)
    return n, h.hexdigest()


def fail(message: str):
    raise RuntimeError(message)


def safe_rel(text: str) -> str:
    p = PurePosixPath(text)
    if (not text or p.is_absolute() or "\\" in text or any(x in ("", ".", "..") for x in p.parts)
            or str(p) != text):
        fail(f"unsafe package path: {text!r}")
    return text


def load_json(path: Path):
    raw = path.read_bytes()
    if not raw.endswith(b"\n"):
        fail(f"JSON lacks final newline: {path}")
    try:
        obj = json.loads(raw.decode("ascii"))
    except Exception as exc:
        fail(f"invalid canonical ASCII JSON: {exc}")
    canonical = (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("ascii")
    if raw != canonical:
        fail("certificate.json is not exact canonical sorted JSON")
    return obj


def expected_metadata_shape(m):
    required_top = {
        "format", "scope", "repo", "ancestry", "canonical_parent", "bridge",
        "universes", "cnf", "common_base", "proof", "producer", "checker",
        "compression_cap_bytes", "safe_artifact_paths", "identities",
    }
    if set(m) != required_top or m["format"] != FORMAT:
        fail("metadata top-level schema or format changed")
    if m["scope"] != "exact canonical B7/P6 parent ordinal 20 only":
        fail("scope changed")
    repo = m["repo"]
    if repo != {
        "ledger_commit": "fe0c02ae22efe59d95e8439bcad03427092b21e7",
        "parent_cover_commit": "eb2930553b6e4078c5c7f677bd1d2468846d0f03",
        "staging_head_observed": "fe0c02ae22efe59d95e8439bcad03427092b21e7",
    }:
        fail("repo pins changed")
    if m["ancestry"] != {"parent_cover_is_ancestor_of_ledger": True,
                           "ledger_is_staging_head": True}:
        fail("ancestry claims changed")
    # If a repository checkout is available at the package's former sibling
    # location, recheck ancestry rather than trusting metadata.  The package
    # remains replayable elsewhere, where immutable full commit pins and copied
    # source identities are the portable binding.
    repo_path = PACKAGE.parent / "repo"
    if (repo_path / ".git").exists():
        def git_output(*args):
            r=subprocess.run(["git","-C",str(repo_path),*args],stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,text=True)
            if r.returncode: fail(f"git command failed: {args}")
            return r.stdout.strip()
        def git_ancestor(old,new):
            r=subprocess.run(["git","-C",str(repo_path),"merge-base","--is-ancestor",old,new],
                             stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            if r.returncode != 0: fail(f"git ancestry failed: {old} !<= {new}")
        if git_output("rev-parse","HEAD") != repo["staging_head_observed"]:
            fail("available repository HEAD differs from staged head pin")
        git_ancestor(repo["parent_cover_commit"],repo["ledger_commit"])
        git_ancestor(repo["ledger_commit"],repo["staging_head_observed"])
    if m["canonical_parent"] != {
        "branch": "B7", "ordinal": 20, "shape": "P6", "placement": "RBACAC",
        "support_color_orbit_weight": 2,
        "holes": [[0, 9], [1, 9], [1, 16], [2, 16], [2, 17]],
        "rooted_cell_labelled_hole_vectors": 784,
    }:
        fail("canonical parent metadata changed")
    if m["bridge"] != {
        "vertices": 18, "pairs": 153, "holes": 5, "arcs": 148,
        "degree_values": [8, 9], "high_vertices": 4,
        "root_outneighbors": list(range(1, 9)), "root_degree": 8,
        "root_is_low": True, "remaining_high_domain": list(range(1, 16)),
        "semantic_transport": "graph variables relabelled; witness variables mapped/reselected; threshold/mu2/missing auxiliaries recomputed from permuted inputs; no literal-CNF-automorphism claim",
    }:
        fail("root-low/exactly-four-high/transport bridge metadata changed")
    if m["universes"] != {
        "packet_labelled": 92, "packet_orbits": 14, "witness_rows": 68,
        "weighted_packet_witness": 3081, "easy_selector_rows": 14,
        "hard_witness_rows": 54, "hard_high_profile_rows": 1332,
        "hard_labelled_assignments": 323400, "selectors": 1346,
        "hard_first_signatures": [3, 4, 6, 7, 8, 9, 12, 13],
        "hard_rows_by_first": {"3": 32, "4": 81, "6": 156, "7": 156,
                                "8": 156, "9": 356, "12": 156, "13": 239},
        "hard_labelled_by_first": {"3": 2730, "4": 16380, "6": 26460,
                                    "7": 26460, "8": 26460, "9": 132300,
                                    "12": 26460, "13": 66150},
        "high_orbit_count_distribution": {"17": 8, "18": 2, "23": 24,
                                           "24": 4, "30": 11, "31": 1,
                                           "32": 2, "38": 1, "49": 1},
        "b_stabilizer_orders": [2, 4, 6, 12, 24, 48, 120],
    }:
        fail("finite-universe metadata changed")
    if m["cnf"] != {
        "variables": 24962, "clauses": 188312, "selectors": 1346,
        "strata": {"common_base": 142729, "parent_hole_units": 153,
                    "guarded_packet_literals": 22882, "guarded_witness_literals": 2567,
                    "guarded_hard_high_literals": 19980, "selector_alo": 1,
                    "refinement_suffix_total": 45430},
        "selector_amo": 0,
    }:
        fail("CNF dimensions or exact clause strata changed")
    if m["common_base"] != {
        "variables": 23616, "clauses": 142729,
        "variable_map_sha256": "cff4c18a4425f26c188790871da51a58b13569764bf89c83d1c736d5f9db070e",
        "clause_stream_sha256": "5af8262714f3e42a595fb19f437f7a87042715056a3735e61e0d06b918db2ccb",
        "independence_boundary": "structural verifier independently reconstructs parent/packet/witness/high orbit bridge and 45,430-clause post-parent refinement suffix (45,583 clauses including the 153 parent-hole units), but imports the pinned shared snc_cnf.generate common-base encoder; hashes bind that common base; this is not a second base implementation",
    }:
        fail("common-base binding or independence boundary changed")
    if m["proof"] != {
        "raw_bytes": 51087439,
        "raw_sha256": "f40ccf3fe14c06c3eb5a1b56adec1706c8be1ae7ec1957bbc05cf7abc4047f2e",
        "xz_bytes": 5679740,
        "xz_sha256": "5453d9ecba1ac5c26aaf18a3d87f28d68b6a35ba3e2143933fb112de0d5270e9",
        "xz_preset": 3,
    }:
        fail("proof identities changed")
    if m["producer"] != {
        "role": "provenance only; not used to establish proof validity",
        "name": "CaDiCaL", "version": "1.7.3",
        "source_commit": "38e073b389a877b0a0d3c91136d2443ab95fdeba",
        "binary_bytes": 1002216,
        "binary_sha256": "ff471d3c6b54fbbc161d65545a5f788d0032ad05b9aff4e2c748d9639400e951",
        "command": "tools/cadical-1.7.3 -q --lrat --no-binary artifacts/parent20.cnf artifacts/parent20.lrat",
        "required_exit": 20, "observed_exit": 20,
    }:
        fail("producer provenance changed")
    chk = m["checker"]
    if chk.get("role") != "proof validity" or chk.get("name") != "lrat-check" \
            or chk.get("source_commit") != "2e3b2dc0ecf938addbd779d42877b6ed69d9a985" \
            or chk.get("source_bytes") != 17682 \
            or chk.get("source_sha256") != "bf07c2ac96b9035da1ebcc578cb95e956a2b795629d613154cdb307f8a8f4a95" \
            or chk.get("required_exit") != 0 or chk.get("required_output") != "exactly one line c VERIFIED" \
            or not isinstance(chk.get("binary_bytes"), int) or chk["binary_bytes"] <= 0 \
            or not isinstance(chk.get("binary_sha256"), str) or len(chk["binary_sha256"]) != 64:
        fail("checker identity/protocol metadata changed")
    if m["compression_cap_bytes"] != CAP:
        fail("compressed-byte cap changed")
    if m["safe_artifact_paths"] != ["artifacts/parent20.cnf", "artifacts/parent20.lrat.xz"]:
        fail("safe artifact list changed")
    if set(m["identities"]) != set(IDENTITY_FIELDS.values()):
        fail("identity table schema changed")


def exact_tree():
    found = set()
    for root, dirs, files in os.walk(PACKAGE, topdown=True, followlinks=False):
        rp = Path(root)
        for name in dirs:
            p = rp / name
            if p.is_symlink(): fail(f"symlink directory forbidden: {p}")
        for name in files:
            p = rp / name
            if p.is_symlink() or not p.is_file(): fail(f"non-regular file forbidden: {p}")
            rel = safe_rel(p.relative_to(PACKAGE).as_posix())
            found.add(rel)
    if found != REQUIRED_FILES:
        fail(f"package tree differs: missing={sorted(REQUIRED_FILES-found)}, extra={sorted(found-REQUIRED_FILES)}")
    for rel in REQUIRED_FILES:
        mode = (PACKAGE / rel).stat().st_mode & 0o777
        expected = 0o755 if rel in EXECUTABLES else 0o644
        if mode != expected: fail(f"mode mismatch {rel}: {oct(mode)} != {oct(expected)}")


def verify_manifest(m):
    lines = MANIFEST.read_text("ascii").splitlines()
    expected_paths = sorted(REQUIRED_FILES - {"metadata/SHA256SUMS"})
    if len(lines) != len(expected_paths): fail("SHA256SUMS row count changed")
    seen = []
    for line, rel in zip(lines, expected_paths):
        fields = line.split("  ")
        if len(fields) != 2 or fields[1] != rel or len(fields[0]) != 64:
            fail("SHA256SUMS not canonical sorted two-space form")
        safe_rel(fields[1]); seen.append(fields[1])
        if identity(PACKAGE / rel)[1] != fields[0]: fail(f"SHA256SUMS mismatch: {rel}")
    if seen != expected_paths: fail("SHA256SUMS paths changed")
    for rel, field in IDENTITY_FIELDS.items():
        actual = identity(PACKAGE / rel)
        item = m["identities"][field]
        if item != {"bytes": actual[0], "sha256": actual[1]}:
            fail(f"metadata identity mismatch: {field}")


def run(command, label, **kwargs):
    r = subprocess.run(command, **kwargs)
    if r.returncode: fail(f"{label} failed with exit {r.returncode}")
    return r


def verify_structure_and_proof(m):
    with tempfile.TemporaryDirectory(prefix="parent20-replay-") as td:
        t = Path(td); cnf = t / "parent20.cnf"; raw = t / "parent20.lrat"
        run([sys.executable, "-B", str(HERE / "verify_parent20_structure.py"), "--write", str(cnf)],
            "independent structure/CNF reconstruction", cwd=PACKAGE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if identity(cnf) != identity(PACKAGE / "artifacts/parent20.cnf") or \
                cnf.read_bytes() != (PACKAGE / "artifacts/parent20.cnf").read_bytes():
            fail("independently reconstructed CNF is not byte-exact")
        digest = hashlib.sha256(); size = 0; saw_empty = False
        dec = lzma.LZMADecompressor(format=lzma.FORMAT_XZ)
        with (PACKAGE / "artifacts/parent20.lrat.xz").open("rb") as source, raw.open("wb") as out:
            while block := source.read(1 << 20):
                try: data = dec.decompress(block)
                except lzma.LZMAError as exc: fail(f"XZ decompression failed: {exc}")
                if data:
                    size += len(data); digest.update(data); out.write(data)
                    # Empty LRAT clause has the form "<id> 0 <hints> 0".
                    for line in data.splitlines():
                        fields=line.split()
                        if len(fields)>=3 and fields[1]==b"0" and fields[-1]==b"0": saw_empty=True
            if not dec.eof or dec.unused_data: fail("XZ stream truncated or has trailing data")
        if (size, digest.hexdigest()) != (m["proof"]["raw_bytes"], m["proof"]["raw_sha256"]):
            fail("raw LRAT identity changed after fresh decompression")
        if not saw_empty:
            # Boundary-safe fallback, only over the small tail.
            with raw.open("rb") as f:
                f.seek(max(0, size - (1 << 20)))
                for line in f:
                    fields=line.split()
                    if len(fields)>=3 and fields[1]==b"0" and fields[-1]==b"0": saw_empty=True
        if not saw_empty: fail("decompressed LRAT does not visibly derive an empty clause")
        checked = run([str(PACKAGE / "tools/lrat-check"), str(cnf), str(raw)], "LRAT replay",
                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if checked.stdout.splitlines().count("c VERIFIED") != 1:
            fail("checker did not emit exactly one literal c VERIFIED line")
    print("PASS full parent20 package: exact universe/CNF, fresh XZ->raw identity, pinned LRAT replay")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--identity-only", action="store_true")
    args = ap.parse_args()
    exact_tree(); m = load_json(METADATA); expected_metadata_shape(m); verify_manifest(m)
    if identity(PACKAGE / "artifacts/parent20.lrat.xz")[0] >= CAP:
        fail("retained compressed LRAT violates strict <250,000,000-byte cap")
    if identity(PACKAGE / "tools/lrat-check") != (m["checker"]["binary_bytes"], m["checker"]["binary_sha256"]):
        fail("checker binary identity changed")
    if args.identity_only:
        print("PASS identity-only exact-safe-tree identities cap checker pins")
    else:
        verify_structure_and_proof(m)


if __name__ == "__main__":
    try: main()
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        raise SystemExit(1)
