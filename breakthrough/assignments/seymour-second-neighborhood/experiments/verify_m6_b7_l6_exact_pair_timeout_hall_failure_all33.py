#!/usr/bin/env python3
"""Replay both Hall proof packages and prove their scopes partition all 33 memberships."""

import argparse
from pathlib import Path
import subprocess
import sys

import check_m6_b7_l6_exact_pair_timeout_hall_failure as hall_check
import verify_m6_b7_l6_exact_pair_timeout_hall_failure_scout_unsat_certificates as prior29
import verify_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split_certificates as split28

HERE = Path(__file__).resolve().parent


def scope_audit():
    all33 = tuple((position, record[0]["membership"])
                  for position, record in enumerate(hall_check.independent_scope()))
    direct = prior29.frozen_scope()
    _, split_rows = split28.load_ledger()
    split_parents = tuple(dict.fromkeys(
        (int(row["parent-position"]), int(row["membership"])) for row in split_rows))
    if len(all33) != 33 or len(set(all33)) != 33:
        raise RuntimeError("canonical Hall campaign is not exactly 33 unique rows")
    if len(direct) != 29 or len(set(direct)) != 29:
        raise RuntimeError("direct certificate scope is not exactly 29 unique rows")
    if len(split_parents) != 4 or len(set(split_parents)) != 4:
        raise RuntimeError("split certificate ancestry is not exactly four unique parents")
    if set(direct) & set(split_parents):
        raise RuntimeError("direct and split parent scopes overlap")
    if set(direct) | set(split_parents) != set(all33):
        raise RuntimeError("direct and split parent scopes do not exhaust canonical all33")
    if tuple(item for item in all33 if item in set(direct)) != direct or \
            tuple(item for item in all33 if item in set(split_parents)) != split_parents:
        raise RuntimeError("proof scopes do not preserve canonical campaign order")
    print("PASS all33=33 prior29=29 split_parents=4 disjoint=yes exhaustive=yes")
    return all33, direct, split_parents


def run(verifier, checker):
    completed = subprocess.run(
        [sys.executable, str(HERE / verifier), "--checker", str(checker)], check=False)
    if completed.returncode:
        raise RuntimeError(f"replay failed: {verifier}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    if not args.checker.is_absolute():
        parser.error("--checker must be an explicit absolute path")
    checker = args.checker.resolve(strict=True)
    scope_audit()
    run("verify_m6_b7_l6_exact_pair_timeout_hall_failure_scout_unsat_certificates.py", checker)
    run("verify_m6_b7_l6_exact_pair_timeout_hall_failure_cardinality_split_certificates.py", checker)
    scope_audit()
    print("PASS canonical Hall completion replayed prior29 and split28")


if __name__ == "__main__":
    main()
