#!/usr/bin/env python3
"""Exact certification of positive square-energy slack for graph6 graphs.

For each graph6 input this computes the adjacency characteristic polynomial
with SymPy, isolates the positive roots using exact algebraic numbers, and
reports a rigorous interval for s^+(G) - n. The interval endpoints are exact
rational numbers (root-isolation intervals), so a positive lower endpoint
proves s^+(G) >= n rigorously for that graph.
"""

from __future__ import annotations

import argparse
import sympy as s

from search_geng import graph6_adjacency


def s_plus_bounds(g6: str) -> tuple[s.Poly, s.Rational, s.Rational, list[tuple]]:
    A = s.Matrix(graph6_adjacency(g6.encode()).astype(int))
    x = s.symbols("x")
    poly = s.Poly(A.charpoly(x).as_expr(), x)
    n_vertices = A.shape[0]

    # intervals() uses exact integer/rational polynomial arithmetic and returns
    # disjoint rational isolating intervals with exact root multiplicities.
    intervals = poly.intervals(eps=s.Rational(1, 10**30))
    lower = s.Rational(-n_vertices)
    upper = s.Rational(-n_vertices)
    positive: list[tuple] = []
    for (a, b), multiplicity in intervals:
        if b <= 0:
            continue
        if a <= 0:
            raise RuntimeError(f"root interval {(a, b)} straddles zero")
        lower += multiplicity * a**2
        upper += multiplicity * b**2
        positive.append((a, b, multiplicity))
    return poly, lower, upper, positive


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graphs", nargs="*", help="graph6 strings to certify")
    parser.add_argument(
        "--from-file", "-f", help="file with graph6 per line (after optional tab/space fields)"
    )
    args = parser.parse_args()

    lines: list[str] = []
    if args.from_file:
        with open(args.from_file) as fh:
            lines.extend(fh.read().splitlines())
    for g in args.graphs:
        lines.append(g)

    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        fields = line.split()
        # Accept either a bare graph6 string or search_geng.py output, whose
        # first field is slack and second field is graph6.
        g6 = fields[1] if len(fields) > 1 and fields[0][0] in "+-.0123456789" else fields[0]
        try:
            poly, lower, upper, positive = s_plus_bounds(g6)
        except Exception as exc:  # noqa: BLE001
            print(f"{g6}\tERROR\t{exc}")
            continue
        print(f"{g6}\tpoly={s.factor(poly.as_expr())}\tnpos={len(positive)}")
        print(f"\tslack_interval=[{lower},{upper}]")
        print(f"\tslack_decimal=[{s.N(lower, 18)},{s.N(upper, 18)}]")
        print(f"\tpositive_root_intervals={positive}")


if __name__ == "__main__":
    main()
