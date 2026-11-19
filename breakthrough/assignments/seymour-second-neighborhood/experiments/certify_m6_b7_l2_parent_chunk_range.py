#!/usr/bin/env python3
"""Regenerate and verify a resumable range of B7-l2 parent-chunk LRATs.

The output directory is a staging area accepted by
``finalize_m6_b7_l2_parent_chunk_certificates.py`` once all 652 leaves exist.
Each completed leaf has a compressed LRAT plus canonical JSON identities for
its regenerated CNF, raw LRAT, and compressed artifact.  Existing leaves are
accepted only after all three identities are rechecked; malformed or partial
files fail closed.
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import hashlib
import json
import lzma
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import m6_b7_l2_parent_chunk_cover as producer

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_SOLVER_COMMIT = "38e073b389a877b0a0d3c91136d2443ab95fdeba"
EXPECTED_SOLVER_VERSION = "1.7.3"
EXPECTED_CHECKER_SHA256 = "e9e71c96b68dc9ed22db35d7581e613e6b161ffbc82c20cba5699f8320a065b8"
OPTIONS = ("--restart=false", "--phase=false", "--seed=3")


def identity(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1 << 20):
            digest.update(block)
    return path.stat().st_size, digest.hexdigest()


def decompressed_identity(path):
    digest, size = hashlib.sha256(), 0
    with lzma.open(path, "rb") as handle:
        while block := handle.read(1 << 20):
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest()


def load_hashes(manifest):
    path = HERE / f"{producer.PREFIX}-hashes.tsv"
    lines = path.read_text(encoding="ascii").splitlines()
    expected = [producer.HASH_FORMAT, f"manifest-bytes\t{len(manifest)}",
                f"manifest-sha256\t{hashlib.sha256(manifest).hexdigest()}",
                "leaves\t652",
                "columns\tleaf-ordinal,key,parents,variables,clauses,cnf-bytes,cnf-sha256"]
    if lines[:5] != expected or len(lines) != 657:
        raise RuntimeError("canonical hash ledger changed")
    result = []
    for ordinal, line in enumerate(lines[5:]):
        fields = line.split("\t")
        if len(fields) != 7 or int(fields[0]) != ordinal:
            raise RuntimeError("malformed canonical hash row")
        result.append((int(fields[5]), fields[6]))
    return tuple(result)


def metadata_path(stage, leaf):
    return stage / f"leaf-{leaf:03d}.json"


def artifact_path(stage, leaf):
    return stage / "artifacts" / f"leaf-{leaf:03d}.lrat.xz"


def load_metadata(path):
    data = json.loads(path.read_text(encoding="ascii"))
    if set(data) != {"leaf", "cnf", "lrat", "xz"} or not isinstance(data["leaf"], int):
        raise RuntimeError(f"malformed metadata: {path}")
    for name in ("cnf", "lrat", "xz"):
        item = data[name]
        if not isinstance(item, list) or len(item) != 2 or not isinstance(item[0], int) or \
                not isinstance(item[1], str) or len(item[1]) != 64:
            raise RuntimeError(f"malformed {name} identity: {path}")
    return data


def validate_existing(stage, leaf, cnf_identity):
    meta, artifact = metadata_path(stage, leaf), artifact_path(stage, leaf)
    if not meta.exists() and not artifact.exists():
        return False
    if not meta.is_file() or not artifact.is_file():
        raise RuntimeError(f"partial stage leaf {leaf:03d}")
    data = load_metadata(meta)
    if data["leaf"] != leaf or tuple(data["cnf"]) != cnf_identity or \
            tuple(data["xz"]) != identity(artifact) or \
            tuple(data["lrat"]) != decompressed_identity(artifact):
        raise RuntimeError(f"existing stage identity mismatch at leaf {leaf:03d}")
    return True


def certify_one(arguments):
    leaf, stage_text, solver_text, checker_text, cnf_identity = arguments
    stage, solver, checker = Path(stage_text), Path(solver_text), Path(checker_text)
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    description = leaves[leaf]
    with tempfile.TemporaryDirectory(prefix=f"b7-l2-{leaf:03d}-", dir=ROOT) as directory:
        work = Path(directory)
        cnf, lrat, compressed = work / "leaf.cnf", work / "leaf.lrat", work / "leaf.lrat.xz"
        producer.write_cnf(cnf, leaf, description, *producer.build(description), manifest)
        if identity(cnf) != tuple(cnf_identity):
            raise RuntimeError(f"regenerated CNF differs at leaf {leaf:03d}")
        solved = subprocess.run([str(solver), "--lrat", "--no-binary", "-q", *OPTIONS,
                                 str(cnf), str(lrat)], stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        if solved.returncode != 20 or "s UNSATISFIABLE" not in solved.stdout.splitlines():
            raise RuntimeError(f"solver did not certify UNSAT at leaf {leaf:03d}: exit {solved.returncode}")
        checked = subprocess.run([str(checker), str(cnf), str(lrat)], capture_output=True, text=True)
        if checked.returncode or "c VERIFIED" not in checked.stdout.splitlines():
            raise RuntimeError(f"LRAT rejected at leaf {leaf:03d}")
        with lrat.open("rb") as source, lzma.open(compressed, "wb", preset=3) as target:
            shutil.copyfileobj(source, target, length=1 << 20)
        data = {"leaf": leaf, "cnf": list(identity(cnf)), "lrat": list(identity(lrat)),
                "xz": list(identity(compressed))}
        destination = artifact_path(stage, leaf)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary_artifact = destination.with_suffix(".lrat.xz.tmp")
        shutil.copyfile(compressed, temporary_artifact)
        os.replace(temporary_artifact, destination)
        meta = metadata_path(stage, leaf)
        temporary = meta.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n",
                             encoding="ascii", newline="\n")
        os.replace(temporary, meta)
    return leaf, data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--stage", type=Path, required=True)
    parser.add_argument("--first", type=int, default=0)
    parser.add_argument("--last", type=int, default=651)
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    if not 0 <= args.first <= args.last < producer.LEAF_COUNT or args.jobs < 1:
        parser.error("require 0 <= first <= last <= 651 and jobs >= 1")
    solver, checker = args.solver.resolve(strict=True), args.checker.resolve(strict=True)
    stage = args.stage.resolve()
    stage.mkdir(parents=True, exist_ok=True)
    (stage / "artifacts").mkdir(exist_ok=True)
    version = subprocess.run([str(solver), "--version"], capture_output=True, text=True)
    if version.returncode or version.stdout.strip() != EXPECTED_SOLVER_VERSION:
        parser.error("solver is not CaDiCaL 1.7.3")
    solver_identity = identity(solver)
    if identity(checker)[1] != EXPECTED_CHECKER_SHA256:
        parser.error("checker identity differs from pinned lrat-check")
    leaves = producer.load_leaves()
    manifest = producer.manifest_payload(leaves)
    hashes = load_hashes(manifest)
    print(f"INFO solver_commit={EXPECTED_SOLVER_COMMIT} solver_bytes={solver_identity[0]} "
          f"solver_sha256={solver_identity[1]}", flush=True)
    missing = []
    for leaf in range(args.first, args.last + 1):
        if validate_existing(stage, leaf, hashes[leaf]):
            print(f"PASS resume leaf={leaf:03d}", flush=True)
        else:
            missing.append(leaf)
    work = [(leaf, str(stage), str(solver), str(checker), hashes[leaf]) for leaf in missing]
    if args.jobs == 1:
        for item in work:
            leaf, data = certify_one(item)
            print(f"PASS certified leaf={leaf:03d} xz_bytes={data['xz'][0]}", flush=True)
    else:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            futures = {pool.submit(certify_one, item): item[0] for item in work}
            for future in as_completed(futures):
                leaf, data = future.result()
                print(f"PASS certified leaf={leaf:03d} xz_bytes={data['xz'][0]}", flush=True)
    print(f"PASS range={args.first:03d}-{args.last:03d} existing={args.last-args.first+1-len(missing)} "
          f"new={len(missing)}")


if __name__ == "__main__":
    main()
