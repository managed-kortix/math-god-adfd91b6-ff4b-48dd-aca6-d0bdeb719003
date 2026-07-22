#!/usr/bin/env python3
"""Fresh-process master certificate: s+(C5--Cq)>q+5 for every odd q>=3."""

from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def run(command: list[str], required: str) -> None:
    result = subprocess.run(command, cwd=HERE, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            check=True)
    if required not in result.stdout:
        raise RuntimeError(f"missing marker {required!r}:\n{result.stdout}")
    print(result.stdout, end="")


def main() -> None:
    python = str(Path.home()/"mathenv/bin/python")
    run([python, "c5_factor_audit.py"], "PASS full C5--Cq factor audit")
    run([python, "c5_moment_formulas.py"], "PASS exact small cases q=3..23")
    run([python, "c5_moment_minorant.py"],
        "PASS exact defect target for all odd q<=725")
    run([python, "c5_phase_equation.py"],
        "PASS continuous branch endpoints and positive-band integer count")
    run([python, "c5_phase_bounds.py"], "PASS exact phase bounds")
    run([python, "c5_phase_integral.py"], "PASS polynomial majorant")
    run([python, "c5_tail_certificate.py"],
        "PASS exact q>=727 quadrature constants")
    run(["gp", "-q", "c5_tail_pari.gp"],
        "PASS independent PARI C5--Cq tail certificate")
    print("PASS MASTER: for every odd q>=3, the bridge C5--Cq has s+>q+5")


if __name__ == "__main__":
    main()
