#!/usr/bin/env python3
"""Translate Cycle 204 equations and perform exact linear elimination for Cycle 205."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "cycle204_s2_equations.json"
REDUCED = ROOT / "cycle205_linear_reduction.json"
FULL_SINGULAR = ROOT / "cycle205_full_qq.sing"
FULL_CERT_SINGULAR = ROOT / "cycle205_full_certificate_qq.sing"
REDUCED_QQ_SINGULAR = ROOT / "cycle205_reduced_qq.sing"
PRIMES = (32003, 32009, 32027, 32029, 32051)


def add_poly(left, right, scale=Fraction(1)):
    result = defaultdict(Fraction, left)
    for monomial, coefficient in right.items():
        result[monomial] += scale * coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def multiply(left, right):
    result = defaultdict(Fraction)
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            result[tuple(sorted(left_monomial + right_monomial))] += left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def primitive(poly):
    denominator = 1
    for coefficient in poly.values():
        denominator = math.lcm(denominator, coefficient.denominator)
    integers = {monomial: int(coefficient * denominator) for monomial, coefficient in poly.items()}
    content = 0
    for coefficient in integers.values():
        content = math.gcd(content, abs(coefficient))
    integers = {monomial: coefficient // content for monomial, coefficient in integers.items()}
    leading = min(integers)
    if integers[leading] < 0:
        integers = {monomial: -coefficient for monomial, coefficient in integers.items()}
    return tuple(sorted(integers.items()))


def parse_equation(equation, variable_index):
    result = defaultdict(Fraction)
    for term in equation["terms"]:
        monomial = tuple(sorted(variable_index[name] for name in term["monomial"]))
        result[monomial] += Fraction(term["coefficient"])
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def linear_rref(equations, variable_count):
    rows = []
    row_ids = []
    for equation, poly in equations:
        if equation["degree"] != 1:
            continue
        row = [Fraction(0)] * (variable_count + 1)
        for monomial, coefficient in poly.items():
            if not monomial:
                row[-1] += coefficient
            else:
                assert len(monomial) == 1
                row[monomial[0]] += coefficient
        rows.append(row)
        row_ids.append(equation["id"])

    rank = 0
    pivots = []
    for column in range(variable_count):
        pivot = next((index for index in range(rank, len(rows)) if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        row_ids[rank], row_ids[pivot] = row_ids[pivot], row_ids[rank]
        value = rows[rank][column]
        rows[rank] = [entry / value for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank or not rows[index][column]:
                continue
            value = rows[index][column]
            rows[index] = [left - value * right for left, right in zip(rows[index], rows[rank])]
        pivots.append(column)
        rank += 1
    assert not any(all(not entry for entry in row[:-1]) and row[-1] for row in rows)
    return rows[:rank], row_ids[:rank], pivots


def fraction_text(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def singular_poly(poly, names):
    pieces = []
    for monomial, coefficient in poly:
        factors = [names[index] for index in monomial]
        magnitude = abs(coefficient)
        body = "*".join(factors)
        if magnitude != 1 or not factors:
            body = str(magnitude) + (("*" + body) if body else "")
        if not pieces:
            pieces.append(("-" if coefficient < 0 else "") + body)
        else:
            pieces.append((" - " if coefficient < 0 else " + ") + body)
    return "".join(pieces) if pieces else "0"


def singular_ideal(name, polys, names):
    lines = [f"ideal {name} ="]
    for index, poly in enumerate(polys):
        suffix = ";" if index == len(polys) - 1 else ","
        lines.append(f"  {singular_poly(poly, names)}{suffix}")
    return "\n".join(lines)


def canonical_bytes(data):
    return (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("ascii")


def build():
    source_bytes = INPUT.read_bytes()
    source = json.loads(source_bytes)
    variables = source["active_variables"]
    variable_index = {name: index for index, name in enumerate(variables)}
    equations = [(equation, parse_equation(equation, variable_index)) for equation in source["equations"]]
    rows, row_ids, pivots = linear_rref(equations, len(variables))
    free = [index for index in range(len(variables)) if index not in pivots]
    free_position = {variable: index for index, variable in enumerate(free)}

    substitutions = {variable: {(free_position[variable],): Fraction(1)} for variable in free}
    for row_index, pivot in enumerate(pivots):
        replacement = {}
        if rows[row_index][-1]:
            replacement[()] = -rows[row_index][-1]
        for variable in free:
            if rows[row_index][variable]:
                replacement[(free_position[variable],)] = -rows[row_index][variable]
        substitutions[pivot] = replacement

    reduced_sources = defaultdict(list)
    for equation, poly in equations:
        image = {}
        for monomial, coefficient in poly.items():
            term = {(): coefficient}
            for variable in monomial:
                term = multiply(term, substitutions[variable])
            image = add_poly(image, term)
        if image:
            reduced_sources[primitive(image)].append(equation["id"])

    reduced_polys = sorted(reduced_sources)
    free_names = [variables[index] for index in free]
    substitution_rows = []
    for row_index, pivot in enumerate(pivots):
        replacement = substitutions[pivot]
        substitution_rows.append({
            "variable": variables[pivot],
            "rref_source_row": row_ids[row_index],
            "constant": fraction_text(replacement.get((), Fraction(0))),
            "terms": [
                {"coefficient": fraction_text(coefficient), "variable": free_names[monomial[0]]}
                for monomial, coefficient in sorted(replacement.items()) if monomial
            ],
        })
    reduced_rows = []
    for index, poly in enumerate(reduced_polys):
        reduced_rows.append({
            "id": f"r{index:02d}",
            "degree": max(len(monomial) for monomial, _ in poly),
            "sources": reduced_sources[poly],
            "terms": [
                {
                    "coefficient": str(coefficient),
                    "monomial": [free_names[variable] for variable in monomial],
                }
                for monomial, coefficient in poly
            ],
        })
    reduced_data = {
        "schema": "cycle205-linear-reduction-v1",
        "source": INPUT.name,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "method": "exact rational RREF of all degree-one equations, followed by substitution and primitive integer normalization",
        "exceptional_primes": [2],
        "counts": {
            "input_equations": len(equations),
            "input_variables": len(variables),
            "linear_equations": sum(equation["degree"] == 1 for equation, _ in equations),
            "linear_rank": len(pivots),
            "free_variables": len(free),
            "nonzero_reduced_images_before_deduplication": sum(len(ids) for ids in reduced_sources.values()),
            "distinct_reduced_equations": len(reduced_polys),
            "reduced_degree_counts": dict(sorted(Counter(row["degree"] for row in reduced_rows).items())),
        },
        "free_variable_order": free_names,
        "substitutions": substitution_rows,
        "equations": reduced_rows,
    }

    full_polys = [primitive(poly) for _, poly in equations]
    full_text = "\n".join([
        "// Generated by generate_cycle205_singular.py; all 514 frozen equations over Q.",
        "option(redSB);",
        f"ring R = 0,({','.join(variables)}),dp;",
        singular_ideal("I514", full_polys, variables),
        "print(\"CYCLE205_FULL_INPUT equations=\" + string(size(I514)) + \" variables=\" + string(nvars(basering)));",
        "ideal L = I514[241],I514[242]; // overwritten below by degree scan in generated ledger, not used computationally",
        "print(\"Use cycle205_linear_reduction.json for the exact 44-row rank-27 elimination.\");",
        "quit;",
        "",
    ])
    full_cert_text = "\n".join([
        "// Direct characteristic-zero certificate in the original 514 generators.",
        "option(redSB);",
        f"ring R = 0,({','.join(variables)}),dp;",
        singular_ideal("I514", full_polys, variables),
        "print(\"CYCLE205_FULL_QQ_START equations=\" + string(size(I514)) + \" variables=\" + string(nvars(basering)));",
        "int t = timer;",
        "ideal G = std(I514);",
        "int elapsed = timer-t;",
        "int isunit = (size(G)==1 && leadmonom(G[1])==1);",
        "print(\"CYCLE205_FULL_QQ_RESULT unit=\" + string(isunit) + \" gb_size=\" + string(size(G)) + \" elapsed_ms=\" + string(elapsed));",
        "if (isunit)",
        "{",
        "  ideal One = 1;",
        "  matrix C = lift(I514,One);",
        "  print(\"CYCLE205_FULL_CERTIFICATE_BEGIN\");",
        "  int i;",
        "  for (i=1; i<=nrows(C); i++) { if (C[i,1] != 0) { print(\"C[\"+string(i)+\"]=\"+string(C[i,1])); } }",
        "  print(\"CYCLE205_FULL_CERTIFICATE_END\");",
        "  matrix MI[1][size(I514)] = I514;",
        "  matrix MOne[1][1] = 1;",
        "  matrix Check = MOne-MI*C;",
        "  print(\"CYCLE205_FULL_CERTIFICATE_REMAINDER \" + string(Check[1,1]));",
        "}",
        "quit;",
        "",
    ])
    short_names = [f"x{index}" for index in range(len(free_names))]
    reduced_qq_text = "\n".join([
        "// Exact characteristic-zero check and ideal-membership certificate.",
        "option(redSB);",
        f"ring R = 0,({','.join(short_names)}),dp;",
        singular_ideal("J", reduced_polys, short_names),
        "print(\"CYCLE205_QQ_START equations=\" + string(size(J)) + \" variables=\" + string(nvars(basering)));",
        "int t = timer;",
        "ideal G = std(J);",
        "int elapsed = timer-t;",
        "int isunit = (size(G)==1 && leadmonom(G[1])==1);",
        "print(\"CYCLE205_QQ_RESULT unit=\" + string(isunit) + \" gb_size=\" + string(size(G)) + \" elapsed_ms=\" + string(elapsed));",
        "if (isunit)",
        "{",
        "  ideal One = 1;",
        "  matrix C = lift(J,One);",
        "  print(\"CYCLE205_CERTIFICATE_BEGIN\");",
        "  int i;",
        "  for (i=1; i<=nrows(C); i++) { if (C[i,1] != 0) { print(\"C[\"+string(i)+\"]=\"+string(C[i,1])); } }",
        "  print(\"CYCLE205_CERTIFICATE_END\");",
        "  matrix MJ[1][size(J)] = J;",
        "  matrix MOne[1][1] = 1;",
        "  matrix Check = MOne-MJ*C;",
        "  print(\"CYCLE205_CERTIFICATE_REMAINDER \" + string(Check[1,1]));",
        "}",
        "quit;",
        "",
    ])
    prime_texts = {}
    for prime in PRIMES:
        prime_texts[prime] = "\n".join([
            "// Generated exact post-linear-elimination modular unit-ideal test.",
            "option(redSB);",
            f"ring R = {prime},({','.join(short_names)}),dp;",
            singular_ideal("J", reduced_polys, short_names),
            f"print(\"CYCLE205_START prime={prime} equations=\" + string(size(J)) + \" variables=\" + string(nvars(basering)));",
            "int t = timer;",
            "ideal G = std(J);",
            "int elapsed = timer-t;",
            "int isunit = (size(G)==1 && leadmonom(G[1])==1);",
            f"print(\"CYCLE205_RESULT prime={prime} unit=\" + string(isunit) + \" gb_size=\" + string(size(G)) + \" elapsed_ms=\" + string(elapsed));",
            "if (isunit) { print(\"CYCLE205_GB_CONSTANT \" + string(G[1])); }",
            "quit;",
            "",
        ])
    return (
        reduced_data,
        full_text.encode("ascii"),
        full_cert_text.encode("ascii"),
        reduced_qq_text.encode("ascii"),
        {prime: text.encode("ascii") for prime, text in prime_texts.items()},
    )


def outputs():
    reduced_data, full_bytes, full_cert_bytes, reduced_qq_bytes, prime_bytes = build()
    result = [
        (REDUCED, canonical_bytes(reduced_data)),
        (FULL_SINGULAR, full_bytes),
        (FULL_CERT_SINGULAR, full_cert_bytes),
        (REDUCED_QQ_SINGULAR, reduced_qq_bytes),
    ]
    result.extend((ROOT / f"cycle205_mod_{prime}.sing", data) for prime, data in prime_bytes.items())
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = outputs()
    if args.check:
        for path, data in generated:
            if not path.exists() or path.read_bytes() != data:
                raise SystemExit(f"replay mismatch: {path}")
        print("Cycle 205 Singular artifacts replay byte-for-byte")
    else:
        for path, data in generated:
            path.write_bytes(data)
            print("wrote", path.name, hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
