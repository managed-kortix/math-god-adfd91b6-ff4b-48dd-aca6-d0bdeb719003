#!/usr/bin/env python3
"""Hostile mutation tests for the k4 simultaneous-source certificate package.

Every test is deterministic and expects rejection.  It attacks a different
trust boundary: graph semantics, exact predecessor union, split coverage,
ledger/artifact identity, and proof/CNF binding.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

# An accepted hostile mutation is a test failure.  The tests intentionally use
# temporary copies and never alter a retained artifact.

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GENERATOR = HERE / "k4_simsrc_cnf.py"
STRUCTURAL = HERE / "check_k4_simsrc_cnf.py"
SPLIT = HERE / "k4_simsrc_split.py"
VERIFY = HERE / "verify_k4_simsrc_certificates.py"
LEDGER = HERE / "k4-simsrc-certificates.tsv"
DEFAULT_CHECKER = Path("/workspace/toolchain-src/drat-trim/lrat-check")


def run(command, *, expected=0):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode != expected:
        raise RuntimeError(
            f"unexpected exit {result.returncode}, expected {expected}: {' '.join(map(str, command))}\n{result.stdout}"
        )
    return result.stdout


def expect_reject(command, label):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if result.returncode == 0:
        raise RuntimeError(f"hostile mutation was accepted: {label}\n{result.stdout}")
    print(f"PASS rejected={label}")


def load_module(path: Path, name: str):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    assert specification.loader is not None
    specification.loader.exec_module(module)
    return module


def rewrite_clause(path: Path, index: int, clause: tuple[int, ...]) -> None:
    lines = path.read_text(encoding="ascii").splitlines()
    lines[index + 1] = " ".join(map(str, clause)) + " 0"
    path.write_text("\n".join(lines) + "\n", encoding="ascii")


def mutate_byte(source: Path, target: Path) -> None:
    data = bytearray(source.read_bytes())
    if not data:
        raise RuntimeError("cannot mutate an empty checker")
    data[len(data) // 2] ^= 1
    target.write_bytes(data)
    target.chmod(0o755)


def main() -> None:
    checker = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CHECKER
    if not checker.is_file():
        raise RuntimeError(f"checker not found: {checker}")

    with tempfile.TemporaryDirectory(prefix="k4-simsrc-mutations-", dir=ROOT) as directory:
        work = Path(directory)
        base_cnf, variable_map = work / "base.cnf", work / "base.map"
        run([sys.executable, str(GENERATOR), "6", str(base_cnf), "--map", str(variable_map),
             "--select", "2:0,1"])
        run([sys.executable, str(STRUCTURAL), "6", str(base_cnf), str(variable_map),
             "--select", "2:0,1"])

        independent = load_module(STRUCTURAL, "independent_k4_checker")
        expected = independent.reconstruct(6)
        names = {name: variable for name, variable in expected.names.items()}
        selector = names["sel:2:0,1"]
        semantic_mutations = {
            "missing-endpoint-outside-row": (-selector, -names["a:2>0"]),
            "missing-endpoint-to-source-guard": (-selector, names["h:0-2"], names["a:0>2"]),
            "missing-two-walk-exclusion-guard": (-selector, -names["a:2>3"], names["h:0-3"], names["a:0>3"]),
            "missing-exact-P-negative": (-names["a:8>9"],),
        }
        base_clauses = independent.parse_cnf(base_cnf)[1]
        for label, target in semantic_mutations.items():
            try:
                index = base_clauses.index(target)
            except ValueError as error:
                raise RuntimeError(f"test target vanished: {label} {target}") from error
            mutated = work / f"{label}.cnf"
            shutil.copyfile(base_cnf, mutated)
            rewrite_clause(mutated, index, base_clauses[index][1:])
            expect_reject(
                [sys.executable, str(STRUCTURAL), "6", str(mutated), str(variable_map), "--select", "2:0,1"],
                label,
            )

        split = load_module(SPLIT, "hostile_k4_split")
        original = split.P6_REPRESENTATIVE_INDICES
        split.P6_REPRESENTATIVE_INDICES = original[:-1]
        split.p6_orbits.cache_clear()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                split.audit()
        except RuntimeError:
            print("PASS rejected=missing-split-representative")
        else:
            raise RuntimeError("hostile split mutation was accepted")

        ledger_lines = LEDGER.read_text(encoding="ascii").splitlines()
        header = next(i for i, line in enumerate(ledger_lines) if line.startswith("columns\t"))
        ledger_mutations = {
            "missing-ledger-row": ledger_lines[:header + 1] + ledger_lines[header + 2:],
            "mutated-artifact-hash": [
                line.replace("a6e6a7fa340ecf5a8f8903c4d1b42cc528d1eaf4ee2c5ec9416888edcc2bbb1a",
                             "0" * 64)
                for line in ledger_lines
            ],
        }
        for label, lines in ledger_mutations.items():
            ledger = work / f"{label}.tsv"
            ledger.write_text("\n".join(lines) + "\n", encoding="ascii")
            expect_reject(
                [sys.executable, str(VERIFY), "--checker", str(checker), "--ledger", str(ledger), "--identity-only"],
                label,
            )

        mutated_checker = work / "mutated-lrat-check"
        mutate_byte(checker, mutated_checker)
        expect_reject(
            [sys.executable, str(VERIFY), "--checker", str(mutated_checker), "--identity-only"],
            "mutated-checker-binary",
        )

        # Bind a real proof to the wrong deterministic branch CNF.  A trusted
        # lrat-check must reject, demonstrating that artifact hashes alone are
        # not treated as a proof of arbitrary formulas.
        wrong_cnf = work / "wrong-branch.cnf"
        run([sys.executable, str(GENERATOR), "6", str(wrong_cnf), "--select", "2:0,3"])
        proof = work / "proof.lrat"
        import lzma
        with lzma.open(ROOT / "certificates/k4-simsrc-p6-orbit-000.lrat.xz", "rb") as source, proof.open("wb") as target:
            shutil.copyfileobj(source, target, 1 << 20)
        expect_reject([str(checker), str(wrong_cnf), str(proof)], "proof-bound-to-wrong-CNF")

    print("PASS hostile-mutations=9")


if __name__ == "__main__":
    main()
