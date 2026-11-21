#!/usr/bin/env python3
"""Hostile normal/-O tests for the exact family-H q-status census."""
import subprocess
import sys
from pathlib import Path

from m7_family_h_census_check import (
    CASES,
    audit_group_canonicalization,
    audit_sorting_clauses,
    integer_rows,
    labelled_multiplicity,
    sorting_clause_pair,
)

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "m7_family_h_census_check.py"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(optimized):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(CHECKER)])
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=120,
        check=False,
    )


def main():
    normal = run(False)
    optimized = run(True)
    require(normal.returncode == optimized.returncode == 0,
            f"normal/-O census failed\nNORMAL:\n{normal.stdout}\nOPT:\n{optimized.stdout}")
    require(normal.stdout == optimized.stdout,
            "normal/-O census output differs")
    require("case=A q_status_orbits=168 labelled_rows=164736" in normal.stdout,
            "missing exact case-A count")
    require("case=B q_status_orbits=168 labelled_rows=164736" in normal.stdout,
            "missing exact case-B count")

    audit_sorting_clauses()
    require(not sorting_clause_pair("I", "O"), "I/O inversion accepted")
    require(not sorting_clause_pair("H", "O"), "H/O inversion accepted")
    require(not sorting_clause_pair("H", "I"), "H/I inversion accepted")
    for case, (g1, g2, _) in CASES.items():
        rows = integer_rows(len(g1), len(g2))
        require(len(rows) == 168, f"case {case}: wrong exact orbit count")
        require(sum(labelled_multiplicity(row, len(g1), len(g2)) for row in rows)
                == 164736, f"case {case}: wrong labelled multiplicity")
        require(audit_group_canonicalization(case) == (168, 164736),
                f"case {case}: group canonicalization failed")

    # The exact universe fixes v->q.  Restoring the impossible v-q-hole option
    # produces the historical strict overcover, not the accepted 168-row scope.
    def rows_with_v_status(size1, size2, v_status):
        count = 0
        for o1 in range(size1 + 1):
            for i1 in range(size1 - o1 + 1):
                h1 = size1 - o1 - i1
                for o2 in range(size2 + 1):
                    for i2 in range(size2 - o2 + 1):
                        h2 = size2 - o2 - i2
                        for h_c in range(3):
                            outdegree_ok = o1 + o2 == 8
                            holes = h1 + h2 + h_c + int(v_status == "H")
                            if outdegree_ok and holes <= 7:
                                count += 1
        return count

    actual = rows_with_v_status(6, 7, "I")
    impossible = rows_with_v_status(6, 7, "H")
    require((actual, impossible, actual + impossible) == (168, 162, 330),
            "historical overcover regression failed")
    print("PASS family-H census normal/-O exact=168 impossible_vq_hole=162 overcover=330")


if __name__ == "__main__":
    main()
