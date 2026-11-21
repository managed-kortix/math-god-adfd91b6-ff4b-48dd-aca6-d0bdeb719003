#!/usr/bin/env python3
"""Independent 256-bit Arb reconstruction of Cycle 43 finite multiprobe data.

This verifier deliberately does not import ``cycle43_divisor_admission_multiprobe``
or its projection routines.  It builds the block-Hilbert vectors directly,
forms Gram matrices/correlation vectors from those coordinates, and evaluates
small-family projections with explicit closed formulas (rank one and rank two)
or a fresh Arb solve (larger local spans).  Endpoint residuals are reconstructed
by a separate dense endpoint norm calculation.

Finite diagnostic only.  This is not an asymptotic theorem or an RH claim.
"""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, arb_mat, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve

BITS = 256
BLOCKS = ((39, 42), (95, 103), (219, 231))
AFFINE = 0
OUT = Path(__file__).with_name("cycle43-independent-multiprobe-results.json")
REFERENCE = Path(__file__).with_name("cycle43-divisor-admission-multiprobe-results.json")
DIRECT_GRAM_PAIRS = ((1, 2), (3, 5), (39, 41), (227, 229))
DIRECT_GRAM_CELLS = 100_000


def asum(values):
    return sum(values, arb(0))


def sign_str(x):
    if not x.is_finite():
        raise RuntimeError(f"nonfinite Arb value: {x}")
    if x > 0:
        return "PASS"
    if x < 0:
        return "FAIL"
    raise RuntimeError(f"unresolved Arb sign: {x}")


def text(x, digits=55):
    return x.str(digits)


def assert_overlap(x, y, label):
    if not x.overlaps(y):
        raise AssertionError(f"nonoverlap for {label}: {x} versus {y}")


def assert_positive(x, label):
    if not x.is_finite() or not x > 0:
        raise RuntimeError(f"{label} is not certified finite and positive: {x}")


def direct_cell_prefix(a, b, cells=DIRECT_GRAM_CELLS):
    """Direct reciprocal-cell integral of rho_a*rho_b through ``cells``.

    On t in [k,k+1], {t/a}{t/b}/t^2 is integrated exactly in Arb
    using only a rational constant, log(1+1/k), and a rational endpoint term.
    The omitted tail is nonnegative and at most 1/cells because fractional
    parts lie in [0,1].  This independently brackets selected Vasyunin entries.
    """
    prefix = arb(0)
    for k in range(1, cells + 1):
        fa, fb = k // a, k // b
        constant = arb(1) / (a * b)
        logarithmic = -(arb(fb) / a + arb(fa) / b) * (arb(k + 1) / k).log()
        endpoint = arb(fa * fb) * (arb(1) / k - arb(1) / (k + 1))
        prefix += constant + logarithmic + endpoint
    return prefix


def audit_base_gram():
    """Selected base-kernel cross-check independent of the cotangent formula."""
    rg = RestrictedGram()
    rows = []
    for a, b in DIRECT_GRAM_PAIRS:
        prefix = direct_cell_prefix(a, b)
        value = rg.entry(a, b)
        # rho_a*rho_b >= 0, and the remaining integral is <= int_K^inf dt/t^2.
        lower, upper = prefix, prefix + arb(1) / DIRECT_GRAM_CELLS
        if not (value >= lower and value <= upper):
            raise AssertionError(
                f"base Gram cell bracket failed for {(a,b)}: "
                f"prefix={prefix}, value={value}, upper={upper}"
            )
        rows.append({
            "pair": [a, b],
            "cells": DIRECT_GRAM_CELLS,
            "direct_prefix": text(prefix),
            "rigorous_tail_upper": text(arb(1) / DIRECT_GRAM_CELLS),
            "vasyunin_value": text(value),
            "bracket_pass": True,
        })
    return rows


class DirectBlockHilbert:
    """Fresh direct-sum Hilbert assembly, independent of Cycle 43 code."""

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop
        self.scales = tuple(range(start, stop))
        self.mu = mobius_sieve(stop)
        self.labels = (AFFINE,) + tuple(d for d in range(1, stop) if self.mu[d])
        self.logs = [arb(0)] + [arb(n).log() for n in range(1, stop + 2)]
        self.theta = arb(1) / (4 * self.logs[start])
        self.rg = RestrictedGram()
        self._h = {}
        self.weights = {}
        self.A = {}
        self.eta = {}
        self.B = {}
        for n in self.scales:
            q = self.logs[n] / self.logs[n + 1]
            self.weights[n] = 1 - q
            self.A[n] = 1 + q - 2 * self.theta
            assert_positive(self.A[n], f"A[{n}]")
            self.eta[n] = (1 - 2 * self.theta) / self.A[n]
            self.B[n] = 2 * self.theta + (1 - 2 * self.theta) ** 2 / self.A[n]

        # Coordinates are coefficient rows in the fixed Hilbert basis
        # e_0=chi and e_d=rho_d.  X is the direct-sum vector over scales.
        self.xrows = {n: self._xrow(n) for n in self.scales}
        self.prows = {d: self._probe_rows(d) for d in self.labels}
        self.positive_energy = self.direct_sum_inner(self.xrows, self.xrows)
        self.negative_budget = asum(
            self.weights[n] * self.B[n] * self.hilbert_norm(self._urow(n))
            for n in self.scales
        )
        self.residual = self.positive_energy - self.negative_budget

    def h(self, a, b):
        key = (min(a, b), max(a, b))
        if key not in self._h:
            if a == AFFINE and b == AFFINE:
                self._h[key] = arb(1)
            elif a == AFFINE:
                self._h[key] = self.rg.chi_cross(b)
            elif b == AFFINE:
                self._h[key] = self.rg.chi_cross(a)
            else:
                self._h[key] = self.rg.entry(a, b)
        return self._h[key]

    def _urow(self, n):
        row = {AFFINE: arb(1)}
        for d in self.labels[1:]:
            if d <= n:
                row[d] = arb(self.mu[d])
        return row

    def _xrow(self, n):
        row = {AFFINE: -self.eta[n]}
        for d in self.labels[1:]:
            if d <= n:
                row[d] = arb(self.mu[d]) * (
                    self.logs[d] / self.logs[n] - self.eta[n]
                )
        return row

    def _probe_rows(self, label):
        rows = {}
        for n in self.scales:
            if label == AFFINE:
                rows[n] = {AFFINE: -self.eta[n]}
            elif label <= n:
                rows[n] = {
                    label: arb(self.mu[label]) * (
                        self.logs[label] / self.logs[n] - self.eta[n]
                    )
                }
            else:
                rows[n] = {}
        return rows

    def hilbert_inner(self, left, right):
        return asum(
            ca * cb * self.h(a, b)
            for a, ca in left.items()
            for b, cb in right.items()
        )

    def hilbert_norm(self, row):
        return self.hilbert_inner(row, row)

    def direct_sum_inner(self, left_rows, right_rows):
        return asum(
            self.weights[n] * self.A[n]
            * self.hilbert_inner(left_rows[n], right_rows[n])
            for n in self.scales
        )

    def probe_data(self, family):
        family = tuple(family)
        m = len(family)
        G = [[arb(0) for _ in range(m)] for _ in range(m)]
        c = [arb(0) for _ in range(m)]
        for i, a in enumerate(family):
            c[i] = self.direct_sum_inner(self.xrows, self.prows[a])
            for j, b in enumerate(family):
                G[i][j] = self.direct_sum_inner(self.prows[a], self.prows[b])
        return G, c

    def projection(self, family):
        family = tuple(family)
        G, c = self.probe_data(family)
        m = len(family)
        if m == 0:
            return arb(0), arb(1), "empty", ()
        if m == 1:
            assert_positive(G[0][0], f"rank-one Gram {family}")
            return c[0] * c[0] / G[0][0], G[0][0], "closed-rank1", ()
        if m == 2:
            # Independent adjugate formula; no matrix.solve call.
            a, b, d = G[0][0], G[0][1], G[1][1]
            assert_overlap(G[0][1], G[1][0], f"Gram symmetry {family}")
            det = a * d - b * b
            assert_positive(det, f"rank-two Gram determinant {family}")
            num = d * c[0] ** 2 - 2 * b * c[0] * c[1] + a * c[1] ** 2
            y0 = (d * c[0] - b * c[1]) / det
            y1 = (a * c[1] - b * c[0]) / det
            residuals = (a * y0 + b * y1 - c[0], b * y0 + d * y1 - c[1])
            for i, item in enumerate(residuals):
                if not item.contains(0):
                    raise RuntimeError(
                        f"rank-two adjugate residual excludes zero for {family} "
                        f"at row {i}: {item}"
                    )
            return num / det, det, "closed-rank2-adjugate-residual-checked", residuals

        M = arb_mat(m, m)
        v = arb_mat(m, 1)
        for i in range(m):
            v[i, 0] = c[i]
            for j in range(m):
                M[i, j] = G[i][j]
        det = M.det()
        assert_positive(det, f"Gram determinant {family}")
        solution = M.solve(v)
        residual = M * solution - v
        residuals = tuple(residual[i, 0] for i in range(m))
        for i, item in enumerate(residuals):
            if not item.contains(0):
                raise RuntimeError(
                    f"linear-solve residual excludes zero for {family} at row {i}: "
                    f"{item}"
                )
        return (v.transpose() * solution)[0, 0], det, "fresh-arb-solve-residual-checked", residuals

    def certificate(self, family):
        family = tuple(family)
        p, det, method, solve_residuals = self.projection(family)
        margin = p - self.negative_budget
        return {
            "family": list(family),
            "rank": len(family),
            "projection": text(p),
            "determinant": text(det),
            "margin": text(margin),
            "verdict": sign_str(margin),
            "method": method,
            "linear_solve_residuals": [text(item) for item in solve_residuals],
        }

    def dense_endpoint_energy(self, N):
        # Direct dense coefficient contraction for F_N, no complete_energies.
        row = {AFFINE: arb(1)}
        LN = self.logs[N]
        for d in range(1, N + 1):
            if self.mu[d]:
                row[d] = arb(self.mu[d]) * (1 - self.logs[d] / LN)
        return self.hilbert_norm(row)

    def endpoint_residual(self):
        Pa = self.dense_endpoint_energy(self.start)
        Pb = self.dense_endpoint_energy(self.stop)
        weighted = asum(
            self.weights[n] * self.dense_endpoint_energy(n)
            for n in self.scales
        )
        return Pa - Pb - 2 * self.theta * weighted


def count_singletons(block):
    passing = []
    margins = {}
    for d in block.labels:
        cert = block.certificate((d,))
        margins[d] = cert["margin"]
        if cert["verdict"] == "PASS":
            passing.append(d)
    return passing, margins


def summarize(block):
    direct_endpoint = block.endpoint_residual()
    assert_overlap(block.residual, direct_endpoint, f"endpoint residual {block.start}")
    assert_positive(block.residual, f"residual {block.start}")

    singletons, singleton_margins = count_singletons(block)
    local = tuple(d for d in block.labels if block.start <= d < block.stop)
    record = {
        "start": block.start,
        "stop": block.stop,
        "theta": text(block.theta),
        "positive_energy": text(block.positive_energy),
        "negative_budget": text(block.negative_budget),
        "residual_direct_square": text(block.residual),
        "residual_dense_endpoints": text(direct_endpoint),
        "endpoint_residual_overlap": True,
        "singleton_pool_size": len(block.labels),
        "singleton_passing_count": len(singletons),
        "singleton_passing_labels": singletons,
        "singleton_margins": {str(k): v for k, v in singleton_margins.items()},
        "local_full_span": block.certificate(local),
    }

    if block.start in (39, 95):
        record["rank_one_affine"] = block.certificate((AFFINE,))
        record["rank_one_divisor_3"] = block.certificate((3,))
    else:
        for family in ((AFFINE,), (3,), (AFFINE, 215), (3, 215),
                       (AFFINE, 219), (AFFINE, 227), (AFFINE, 229)):
            record["family_" + "_".join(map(str, family))] = block.certificate(family)

        # Exhaustively certify all 143 affine+divisor rank-two families and,
        # separately, all C(143,2)=10153 divisor-only pairs.  This is stronger
        # than the listed examples and tests the stated rank-two existence
        # without using the original midpoint-greedy routine.
        pair_results = {}
        passing_pairs = []
        for d in block.labels[1:]:
            cert = block.certificate((AFFINE, d))
            pair_results[d] = cert
            if cert["verdict"] == "PASS":
                passing_pairs.append(d)
        record["affine_divisor_pair_scan"] = {
            "pool_size": len(pair_results),
            "passing_count": len(passing_pairs),
            "passing_labels": passing_pairs,
            "current_local": {
                str(d): pair_results[d]
                for d in local
            },
        }

        divisor_pair_passes = []
        labels = block.labels[1:]
        target_3_215_seen = False
        for i, a in enumerate(labels):
            for b in labels[i + 1:]:
                cert = block.certificate((a, b))
                if cert["verdict"] == "PASS":
                    divisor_pair_passes.append((a, b))
                if (a, b) == (3, 215):
                    target_3_215_seen = cert["verdict"] == "PASS"
        record["divisor_pair_scan"] = {
            "pool_size": len(labels) * (len(labels) - 1) // 2,
            "passing_count": len(divisor_pair_passes),
            "first_passing_pairs_lexicographic": [
                list(pair) for pair in divisor_pair_passes[:25]
            ],
            "contains_3_215": target_3_215_seen,
        }
        if not target_3_215_seen:
            raise AssertionError("divisor pair (3,215) did not reproduce")
        if pair_results[227]["verdict"] != "PASS" or pair_results[229]["verdict"] != "FAIL":
            raise AssertionError("227/229 boundary did not reproduce")

    expected_counts = {39: 14, 95: 7, 219: 0}
    if len(singletons) != expected_counts[block.start]:
        raise AssertionError(
            f"singleton discrepancy on {block.start}: {len(singletons)}"
        )
    if record["local_full_span"]["verdict"] != "FAIL":
        raise AssertionError(f"local full span unexpectedly passed: {block.start}")
    return record



def compare_published(records):
    """Compare independent balls with the Cycle 43 JSON only after reconstruction."""
    if not REFERENCE.exists():
        return {"available": False, "discrepancies": ["reference JSON absent"]}
    published = json.loads(REFERENCE.read_text())
    pblocks = {(b["start"], b["stop"]): b for b in published["blocks"]}
    discrepancies = []

    def overlap_string(ours, theirs, label):
        x, y = arb(ours), arb(theirs)
        if not x.overlaps(y):
            discrepancies.append(f"interval nonoverlap: {label}: {x} versus {y}")

    for rec in records:
        key = (rec["start"], rec["stop"])
        pub = pblocks.get(key)
        if pub is None:
            discrepancies.append(f"published block missing: {key}")
            continue
        for ours_key, pub_key in (
            ("positive_energy", "positive_energy"),
            ("negative_budget", "negative_budget"),
            ("residual_direct_square", "residual"),
        ):
            overlap_string(rec[ours_key], pub[pub_key], f"{key} {ours_key}")
        if rec["singleton_passing_count"] != pub["singleton_scan"]["passing_count"]:
            discrepancies.append(f"singleton count mismatch: {key}")
        if rec["singleton_passing_labels"] != pub["singleton_scan"]["passing_labels"]:
            discrepancies.append(f"singleton labels mismatch: {key}")
        ours_local = rec["local_full_span"]
        pub_local = pub["new_admissions_only"]
        if ours_local["verdict"] != pub_local["verdict"]:
            discrepancies.append(f"local full-span verdict mismatch: {key}")
        overlap_string(ours_local["projection"], pub_local["projection"],
                       f"{key} local projection")
        overlap_string(ours_local["margin"], pub_local["margin"],
                       f"{key} local margin")

        if rec["start"] == 219:
            pairs = (
                ("family_0_215", "greedy_trace", -1),
                ("family_3_215", "divisor_3_plus_215", None),
                ("family_0_227", "affine_plus_227", None),
                ("family_0_229", "affine_plus_229", None),
            )
            for ours_name, pub_name, index in pairs:
                ours = rec[ours_name]
                theirs = pub[pub_name][index] if index is not None else pub[pub_name]
                if ours["verdict"] != theirs["verdict"]:
                    discrepancies.append(f"family verdict mismatch: {ours_name}")
                overlap_string(ours["projection"], theirs["projection"],
                               f"{ours_name} projection")
                overlap_string(ours["margin"], theirs["margin"],
                               f"{ours_name} margin")
    return {
        "available": True,
        "reference_precision_bits": published.get("arb_precision_bits"),
        "discrepancies": discrepancies,
    }


def main():
    ctx.prec = BITS
    records = [summarize(DirectBlockHilbert(a, b)) for a, b in BLOCKS]
    payload = {
        "scope": "independent certified finite diagnostic only; no RH claim",
        "precision_bits": BITS,
        "independence": [
            "does not import cycle43_divisor_admission_multiprobe",
            "direct block-Hilbert coefficient-row assembly",
            "dense endpoint norms computed separately",
            "rank-one quotient and rank-two adjugate formulas",
            "larger families use a fresh Arb matrix assembly and solve",
            "all final signs fail closed on overlapping zero",
            "all 143 affine-divisor and 10153 divisor-divisor rank-two families scanned on [219,231)",
            "selected shared Vasyunin entries bracketed by direct reciprocal-cell integration",
        ],
        "selected_base_gram_direct_cell_audit": audit_base_gram(),
        "blocks": records,
        "post_reconstruction_comparison": compare_published(records),
    }
    if payload["post_reconstruction_comparison"]["discrepancies"]:
        raise AssertionError(
            "published-result discrepancies: "
            + repr(payload["post_reconstruction_comparison"]["discrepancies"])
        )
    OUT.write_text(json.dumps(payload, indent=2) + "\n")

    print("INDEPENDENT 256-BIT FINITE DIAGNOSTIC; NOT AN RH CLAIM")
    for r in records:
        print(
            f"[{r['start']},{r['stop']}): residual={r['residual_direct_square']} "
            f"singletons={r['singleton_passing_count']}/{r['singleton_pool_size']} "
            f"local-full={r['local_full_span']['verdict']}"
        )
        if r["start"] == 219:
            for key in ("family_0_215", "family_3_215", "family_0_227", "family_0_229"):
                c = r[key]
                print(f"  {key}: {c['verdict']} margin={c['margin']}")
            aps = r["affine_divisor_pair_scan"]
            dps = r["divisor_pair_scan"]
            print(f"  affine-divisor pair scan: {aps['passing_count']}/{aps['pool_size']} pass")
            print(f"  divisor-divisor pair scan: {dps['passing_count']}/{dps['pool_size']} pass")
    discrepancies = payload["post_reconstruction_comparison"]["discrepancies"]
    print(f"published-result discrepancies={len(discrepancies)}")
    for discrepancy in discrepancies:
        print(f"  DISCREPANCY: {discrepancy}")
    print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
