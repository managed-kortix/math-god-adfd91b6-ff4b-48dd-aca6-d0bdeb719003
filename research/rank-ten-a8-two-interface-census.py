#!/usr/bin/env python3
"""Exact marked two-interface experiment for an eight-triangle cluster.

The two labelled marks range over shared cuts and actual private triangle
vertices and may coincide.  The router objective is an exact Fraction credit
minus exact private-interval charges.  Acceptance at score >= 1 is a
conservative rational surrogate for subtracting two pentagonal deficits.  This
is a finite interface census, not a theorem claim.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SPEC = spec_from_file_location(
    "rank_nine_two_interface", HERE / "nonacyclic-t7-two-interface-census.py"
)
BASE = module_from_spec(SPEC)
if SPEC.loader is None:
    raise RuntimeError("rank-nine interface dependency has no import loader")
sys.modules[SPEC.name] = BASE
SPEC.loader.exec_module(BASE)
BASE.TRIANGLE_MARGIN[8] = Fraction(0)


def enumerate_rows():
    classes = BASE.BASE.enumerate_colors(("T",) * 8, 0)
    rows = {}
    labelled_positions = 0
    for incidence_signature, tree in classes:
        positions = BASE.position_universe(tree)
        labelled_positions += len(positions) ** 2
        local = {}
        for first in positions:
            for second in positions:
                pair = (first, second)
                signature = BASE.marked_signature(tree, pair)
                if signature in local:
                    old_pair, multiplicity = local[signature]
                    local[signature] = old_pair, multiplicity + 1
                else:
                    local[signature] = pair, 1
        for signature, (pair, multiplicity) in local.items():
            BASE.require(signature not in rows, f"duplicate canonical row: {signature}")
            rows[signature] = BASE.Row(
                signature, incidence_signature, tree, pair, multiplicity
            )
    return tuple(rows[key] for key in sorted(rows)), len(classes), labelled_positions


def exact_classify(rows):
    scores = Counter()
    routers = Counter()
    residuals = []
    plans = {}
    for row in rows:
        plan = BASE.best_plan(row)
        score = Fraction(plan.credit) - Fraction(plan.naked)
        BASE.require(score == plan.score, "router score is not exact")
        plans[row.signature] = plan
        scores[score] += 1
        routers[len(plan.routers)] += 1
        if score < 1:
            residuals.append(row)
    return plans, scores, routers, residuals


def residual_shapes(residuals):
    answer = Counter()
    for row in residuals:
        positions = tuple(
            sorted(
                (
                    position.kind,
                    len(BASE.BASE.adjacency(row.tree)[position.vertex])
                    if position.kind == "private"
                    else sum(
                        cycle < len(row.tree.colors)
                        for cycle in BASE.BASE.adjacency(row.tree)[position.vertex]
                    ),
                )
                for position in row.positions
            )
        )
        answer[(BASE.BASE.cut_count(row.tree), row.incidence_signature, positions)] += 1
    return answer


def compact(counter):
    return dict(sorted(counter.items(), key=lambda item: repr(item[0])))


def main():
    rows, incidence_count, labelled_positions = enumerate_rows()
    plans, scores, routers, residuals = exact_classify(rows)
    for row in rows:
        BASE.verify_interval_realization(row, plans[row.signature])

    row_digest = sha256(
        ("\n".join(row.signature for row in rows) + "\n").encode("ascii")
    ).hexdigest()
    residual_digest = sha256(
        ("\n".join(row.signature for row in residuals) + "\n").encode("ascii")
    ).hexdigest()
    print("eight-triangle incidence trees:", incidence_count)
    print("labelled interface placements before automorphisms:", labelled_positions)
    print("canonical marked two-interface rows:", len(rows))
    print("accepting rows at exact Fraction score >= 1:", len(rows) - len(residuals))
    print("canonical residuals:", len(residuals))
    print("best exact Fraction scores:", compact(scores))
    print("split-router counts:", compact(routers))
    print("residual shape templates:", compact(residual_shapes(residuals)))
    print("canonical-row sha256:", row_digest)
    print("canonical-residual sha256:", residual_digest)

    BASE.require(sum(scores.values()) == len(rows), "score census is incomplete")
    BASE.require(sum(routers.values()) == len(rows), "router census is incomplete")
    BASE.require(incidence_count == 126, "eight-triangle incidence count changed")
    BASE.require(labelled_positions == 36414, "labelled placement count changed")
    BASE.require(len(rows) == 11689, "marked canonical count changed")
    BASE.require(len(residuals) == 15, "marked residual count changed")
    BASE.require(
        scores == Counter({Fraction(0): 15, Fraction(1): 20, Fraction(2): 283, Fraction(3): 1378, Fraction(4): 4817, Fraction(5): 5176}),
        "exact score distribution changed",
    )
    BASE.require(
        routers == Counter({0: 6, 1: 10844, 2: 838, 3: 1}),
        "router distribution changed",
    )
    BASE.require(row_digest == "77468da6a473a52ece68d6e4319f78337feb17941e615e2a0ae65032f826cc86", "canonical row digest changed")
    BASE.require(residual_digest == "1f41279dad404a97627da24f1fa67e720f6a0d2ffc67b3c28bf1521ebeb11ca0", "canonical residual digest changed")
    BASE.require(
        all(plans[row.signature].score < 1 for row in residuals),
        "residual set contains an accepting score",
    )


if __name__ == "__main__":
    main()
