#!/usr/bin/env python3
"""Hostile self-tests for the m=5 selector-batch generator/checker pair."""

import subprocess
import sys
import tempfile
from pathlib import Path

import check_m5_selector_batch_cnf as checker
import m5_selector_batch_cnf as producer

HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "m5_selector_batch_cnf.py"
CHECKER = HERE / "check_m5_selector_batch_cnf.py"


def run(*arguments, success=True):
    result = subprocess.run(arguments, capture_output=True, text=True)
    if (result.returncode == 0) != success:
        raise RuntimeError(
            f"unexpected exit {result.returncode}: {' '.join(map(str, arguments))}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def rewrite(path, transform):
    lines = path.read_text(encoding="ascii").splitlines()
    transformed = transform(lines)
    path.write_text("\n".join(transformed) + "\n", encoding="ascii", newline="\n")


def replace_once(lines, predicate, replacement):
    output = list(lines)
    indices = [index for index, line in enumerate(output) if predicate(line)]
    if len(indices) != 1:
        raise RuntimeError(f"hostile test expected one target, found {len(indices)}")
    output[indices[0]] = replacement(output[indices[0]])
    return output


def main():
    manifest = producer.checked_manifest()
    independent = checker.reconstruct_manifest()
    if manifest != independent:
        raise RuntimeError("producer and independent manifests disagree")
    if len(producer.batches()) != 80 or len(checker.reconstruct_batches()) != 80:
        raise RuntimeError("batch count changed")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        cases = (
            "B6-main-P6-00",
            "B6-residual23-MIXED-00",
            "B7-all-P3_P3_K2-11",
        )
        for key in cases:
            cnf = root / f"{key}.cnf"
            run(sys.executable, PRODUCER, "--key", key, "--output", cnf)
            output = run(sys.executable, CHECKER, cnf).stdout
            if f"PASS key={key}" not in output:
                raise RuntimeError("checker did not authenticate requested batch")

        source = root / f"{cases[0]}.cnf"

        bad_manifest = root / "bad-manifest.cnf"
        bad_manifest.write_bytes(source.read_bytes())
        rewrite(
            bad_manifest,
            lambda lines: replace_once(
                lines, lambda line: line.startswith("c manifest-sha256 "),
                lambda line: line[:-1] + ("0" if line[-1] != "0" else "1"),
            ),
        )
        run(sys.executable, CHECKER, bad_manifest, success=False)

        bad_alo = root / "bad-alo.cnf"
        bad_alo.write_bytes(source.read_bytes())
        def mutate_alo(lines):
            header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
            base = checker.BASE_CLAUSES["B6"]
            target = header + 1 + base
            literals = lines[target].split()
            if len(literals) != 101 or literals[-1] != "0":
                raise RuntimeError("unexpected ALO clause shape")
            literals[0] = literals[1]
            lines[target] = " ".join(literals)
            return lines
        rewrite(bad_alo, mutate_alo)
        run(sys.executable, CHECKER, bad_alo, success=False)

        bad_guard = root / "bad-guard.cnf"
        bad_guard.write_bytes(source.read_bytes())
        def mutate_guard(lines):
            header = next(i for i, line in enumerate(lines) if line.startswith("p cnf "))
            target = header + 2 + checker.BASE_CLAUSES["B6"]
            literals = lines[target].split()
            if len(literals) != 3 or literals[-1] != "0":
                raise RuntimeError("unexpected guarded clause shape")
            literals[1] = str(-int(literals[1]))
            lines[target] = " ".join(literals)
            return lines
        rewrite(bad_guard, mutate_guard)
        run(sys.executable, CHECKER, bad_guard, success=False)

        bad_selector = root / "bad-selector.cnf"
        bad_selector.write_bytes(source.read_bytes())
        rewrite(
            bad_selector,
            lambda lines: replace_once(
                lines, lambda line: line.startswith("c var 23617 "),
                lambda line: line.replace("m5_batch_selector_000", "m5_batch_selector_999"),
            ),
        )
        run(sys.executable, CHECKER, bad_selector, success=False)

        truncated = root / "truncated.cnf"
        data = source.read_bytes()
        truncated.write_bytes(data[:-1])
        run(sys.executable, CHECKER, truncated, success=False)

    print(
        "PASS batches=80 B6=4355 B6-main=4332 B6-residual=23 B7=3083 "
        "representatives=3 hostile_mutations=5"
    )


if __name__ == "__main__":
    main()
