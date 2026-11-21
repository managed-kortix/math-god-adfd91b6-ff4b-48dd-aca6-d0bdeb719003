#!/usr/bin/env python3
"""Hostile normal/-O regression tests for the independent family-H checker."""
import subprocess
import sys
import tempfile
from pathlib import Path

from check_m7_family_h_cnf import reconstruct, serialize

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check_m7_family_h_cnf.py"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(path, case, envelope, optimized):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        "-B", str(CHECKER), str(path),
        "--case", case,
        "--envelope", envelope,
    ])
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=90,
        check=False,
    )


def expect_pass(label, result):
    require(result.returncode == 0 and
            "PASS independent family-H CNF" in result.stdout,
            f"{label}: valid formula rejected\n{result.stdout}")


def expect_failure(label, result):
    require(result.returncode != 0,
            f"{label}: hostile mutation accepted\n{result.stdout}")


def mutate_clause_literal(raw, clause_index):
    lines = raw.splitlines(keepends=True)
    header_index = next(index for index, line in enumerate(lines)
                        if line.startswith(b"p cnf "))
    line_index = header_index + 1 + clause_index
    fields = lines[line_index].decode("ascii").split()
    require(fields[-1] == "0" and fields[:-1], "test mutation found bad clause")
    fields[0] = str(-int(fields[0]))
    lines[line_index] = (" ".join(fields) + "\n").encode("ascii")
    return b"".join(lines)


def main():
    with tempfile.TemporaryDirectory(prefix="family-h-checker-") as temporary:
        temporary = Path(temporary)
        valid = {}
        for case in ("A", "B"):
            formula = reconstruct(case)
            for envelope in ("mapped", "bare"):
                path = temporary / f"valid-{case}-{envelope}.cnf"
                path.write_bytes(serialize(formula, envelope))
                valid[case, envelope] = path
                normal = run(path, case, envelope, optimized=False)
                optimized = run(path, case, envelope, optimized=True)
                expect_pass(f"normal case={case} envelope={envelope}", normal)
                expect_pass(f"optimized case={case} envelope={envelope}", optimized)
                require(normal.stdout == optimized.stdout,
                        f"normal/-O output differs for case={case} envelope={envelope}")

        base = valid["A", "bare"].read_bytes()
        lines = base.splitlines(keepends=True)
        header = lines[0]
        mutations = {
            "wrong-case": (base, "B", "bare"),
            "wrong-envelope": (base, "A", "mapped"),
            "missing-final-newline": (base[:-1], "A", "bare"),
            "crlf": (base.replace(b"\n", b"\r\n"), "A", "bare"),
            "blank-line": (header + b"\n" + b"".join(lines[1:]), "A", "bare"),
            "comment-in-bare": (b"c hostile\n" + base, "A", "bare"),
            "duplicate-header": (header + base, "A", "bare"),
            "bad-header-vars": (base.replace(b"p cnf 23310 ", b"p cnf 23311 ", 1),
                                "A", "bare"),
            "bad-header-clauses": (base.replace(b" 90451\n", b" 90450\n", 1),
                                   "A", "bare"),
            "drop-clause": (b"".join(lines[:-1]), "A", "bare"),
            "extra-clause": (base + lines[1], "A", "bare"),
            "noncanonical-spacing": (base.replace(b" 0\n", b"  0\n", 1),
                                     "A", "bare"),
            # Semantic groups are all bound by exact clause-stream identity.
            "mutate-no-loop": (mutate_clause_literal(base, 0), "A", "bare"),
            "mutate-no-digon": (mutate_clause_literal(base, 36), "A", "bare"),
            "mutate-npp-biconditional": (mutate_clause_literal(base, 190), "A", "bare"),
            "mutate-high-mask": (mutate_clause_literal(base, 79300), "A", "bare"),
            "mutate-hole-at-least-seven": (
                mutate_clause_literal(base, 90342), "A", "bare"),
            "mutate-hole-at-most-seven": (
                mutate_clause_literal(base, 90343), "A", "bare"),
            "mutate-v-rob": (mutate_clause_literal(base, 90403), "A", "bare"),
            "mutate-q-to-r": (mutate_clause_literal(base, 90410), "A", "bare"),
            "mutate-q-rob": (mutate_clause_literal(base, 90411), "A", "bare"),
            "mutate-sorting": (mutate_clause_literal(base, 90427), "A", "bare"),
        }
        for label, (payload, case, envelope) in mutations.items():
            path = temporary / f"hostile-{label}.cnf"
            path.write_bytes(payload)
            expect_failure(f"normal {label}", run(path, case, envelope, optimized=False))
            expect_failure(f"optimized {label}", run(path, case, envelope, optimized=True))

    print("PASS family-H checker normal/-O baselines=8 hostile_mutations="
          f"{2 * len(mutations)}")


if __name__ == "__main__":
    main()
