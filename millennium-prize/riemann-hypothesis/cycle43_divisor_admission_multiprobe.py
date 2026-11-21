#!/usr/bin/env python3
"""Certified finite divisor-admission multiprobe diagnostics.

This script tests the compensated projection certificate suggested after
Cycle 42 on the three hard finite blocks.  Every reported certificate is an
outward-rounded Arb enclosure obtained from the complete restricted Vasyunin
Gram matrix; there is no unit-cell cutoff.  The greedy ordering is chosen from
Arb midpoints and is explicitly diagnostic; every candidate and every final
pass/fail statement is nevertheless evaluated with Arb interval linear algebra
and fails closed if its sign is unresolved.

This is finite diagnostic code only.  It proves no asymptotic estimate and no
instance of the Riemann hypothesis.
"""

import argparse
import json
from pathlib import Path

from flint import arb, arb_mat, ctx

from certify_complete_gram import RestrictedGram, mobius_sieve

HARD_BLOCKS = ((39, 42), (95, 103), (219, 231))
AFFINE = 0


def _sum(items):
    return sum(items, arb(0))


def interval_text(value, digits=40):
    return value.str(digits)


def certified_sign(value):
    if not value.is_finite():
        raise RuntimeError(f"nonfinite Arb value: {value}")
    if value > 0:
        return 1
    if value < 0:
        return -1
    if value.is_zero():
        return 0
    raise RuntimeError(f"unresolved Arb sign: {value}")


def gram_entry(gram, a, b):
    if a == AFFINE and b == AFFINE:
        return arb(1)
    if a == AFFINE:
        return gram.chi_cross(b)
    if b == AFFINE:
        return gram.chi_cross(a)
    return gram.entry(a, b)


class CompensatedBlock:
    """Complete-Gram data for one block at theta=1/(4 log(start))."""

    def __init__(self, start, stop, bits=192):
        if not (2 <= start < stop):
            raise ValueError("invalid block")
        ctx.prec = bits
        self.start = start
        self.stop = stop
        self.bits = bits
        self.mu = mobius_sieve(stop)
        self.logs = [arb(0)] + [arb(n).log() for n in range(1, stop + 2)]
        self.gram = RestrictedGram()
        self.scales = tuple(range(start, stop))
        self.labels = (AFFINE,) + tuple(
            d for d in range(1, stop) if self.mu[d]
        )
        self.theta = arb(1) / (4 * self.logs[start])
        self.weight = {}
        self.positive_weight = {}
        self.eta = {}
        self.negative_factor = {}
        for n in self.scales:
            ratio_inverse = self.logs[n] / self.logs[n + 1]
            self.weight[n] = 1 - ratio_inverse
            self.positive_weight[n] = 1 + ratio_inverse - 2 * self.theta
            self.eta[n] = (
                (1 - 2 * self.theta) / self.positive_weight[n]
            )
            self.negative_factor[n] = (
                2 * self.theta
                + (1 - 2 * self.theta) ** 2 / self.positive_weight[n]
            )
        if any(certified_sign(self.positive_weight[n]) != 1
               for n in self.scales):
            raise RuntimeError("positive square has uncertified/nonpositive weight")
        self._base = {}
        self._probe_gram = {}
        self._correlation = {}
        self._positive_energy = None
        self._negative_budget = None

    def base(self, a, b):
        key = (min(a, b), max(a, b))
        if key not in self._base:
            self._base[key] = gram_entry(self.gram, a, b)
        return self._base[key]

    def x_coefficient(self, n, label):
        """Coefficient of chi (0) or rho_label in Z_n."""
        if label == AFFINE:
            return -self.eta[n]
        if label <= n:
            return arb(self.mu[label]) * (
                self.logs[label] / self.logs[n] - self.eta[n]
            )
        return arb(0)

    # The admission probe p_label is exactly the matching summand of X.
    def probe_coefficient(self, n, label):
        return self.x_coefficient(n, label)

    def scale_factor(self, n):
        return self.weight[n] * self.positive_weight[n]

    def probe_gram(self, a, b):
        key = (min(a, b), max(a, b))
        if key not in self._probe_gram:
            self._probe_gram[key] = _sum(
                self.scale_factor(n)
                * self.probe_coefficient(n, a)
                * self.probe_coefficient(n, b)
                * self.base(a, b)
                for n in self.scales
            )
        return self._probe_gram[key]

    def correlation(self, label):
        if label not in self._correlation:
            value = arb(0)
            for n in self.scales:
                inner = _sum(
                    self.x_coefficient(n, other) * self.base(other, label)
                    for other in self.labels
                )
                value += (
                    self.scale_factor(n)
                    * self.probe_coefficient(n, label)
                    * inner
                )
            self._correlation[label] = value
        return self._correlation[label]

    def u_norm(self, n):
        active = (AFFINE,) + tuple(
            d for d in self.labels[1:] if d <= n
        )
        return _sum(
            (arb(1) if a == AFFINE else arb(self.mu[a]))
            * (arb(1) if b == AFFINE else arb(self.mu[b]))
            * self.base(a, b)
            for a in active for b in active
        )

    @property
    def positive_energy(self):
        if self._positive_energy is None:
            self._positive_energy = _sum(
                self.scale_factor(n) * _sum(
                    self.x_coefficient(n, a)
                    * self.x_coefficient(n, b)
                    * self.base(a, b)
                    for a in self.labels for b in self.labels
                )
                for n in self.scales
            )
        return self._positive_energy

    @property
    def negative_budget(self):
        if self._negative_budget is None:
            self._negative_budget = _sum(
                self.weight[n] * self.negative_factor[n] * self.u_norm(n)
                for n in self.scales
            )
        return self._negative_budget

    @property
    def residual(self):
        return self.positive_energy - self.negative_budget

    def projection(self, family):
        family = tuple(family)
        if not family:
            return arb(0), arb(1)
        if len(set(family)) != len(family):
            raise ValueError("duplicate probe")
        if any(label not in self.labels for label in family):
            raise ValueError("probe outside complete divisor family")
        size = len(family)
        matrix = arb_mat(size, size)
        vector = arb_mat(size, 1)
        for i, a in enumerate(family):
            vector[i, 0] = self.correlation(a)
            for j, b in enumerate(family):
                matrix[i, j] = self.probe_gram(a, b)
        determinant = matrix.det()
        if certified_sign(determinant) != 1:
            raise RuntimeError(
                f"probe Gram determinant not certified positive for {family}: "
                f"{determinant}"
            )
        try:
            solution = matrix.solve(vector)
        except ZeroDivisionError as exc:
            raise RuntimeError(f"Arb solve failed for {family}") from exc
        projection = (vector.transpose() * solution)[0, 0]
        return projection, determinant

    def certificate(self, family):
        family = tuple(family)
        projection, determinant = self.projection(family)
        margin = projection - self.negative_budget
        return {
            "family": family,
            "rank": len(family),
            "projection": projection,
            "determinant": determinant,
            "margin": margin,
            "verdict": "PASS" if certified_sign(margin) >= 0 else "FAIL",
        }

    def greedy_family(self, pool=None):
        """Midpoint-greedy search; each returned row is Arb-certified."""
        if pool is None:
            pool = self.labels
        pool = tuple(pool)
        selected = []
        current = arb(0)
        trace = []
        while certified_sign(current - self.negative_budget) < 0:
            choices = []
            for label in pool:
                if label in selected:
                    continue
                candidate, determinant = self.projection(selected + [label])
                gain = candidate - current
                # Ordering only: this midpoint comparison is not a certificate.
                choices.append((float(gain.mid()), label, candidate, determinant))
            if not choices:
                break
            _, label, candidate, determinant = max(choices)
            gain = candidate - current
            selected.append(label)
            current = candidate
            margin = current - self.negative_budget
            trace.append({
                "rank": len(selected),
                "label": label,
                "gain": gain,
                "projection": current,
                "determinant": determinant,
                "margin": margin,
                "verdict": (
                    "PASS" if certified_sign(margin) >= 0 else "FAIL"
                ),
            })
        return tuple(selected), trace


def squarefree_prefix(block, cutoff):
    return tuple(d for d in block.labels if d != AFFINE and d <= cutoff)


def first_certifying_prefix(block):
    for cutoff in range(1, block.stop):
        family = squarefree_prefix(block, cutoff)
        if not family:
            continue
        certificate = block.certificate(family)
        if certificate["verdict"] == "PASS":
            return cutoff, certificate
    return None, None


def singleton_scan(block, pool=None):
    """Exhaust all atomic rank-one probes, certifying every verdict."""
    if pool is None:
        pool = block.labels
    certificates = [block.certificate((label,)) for label in pool]
    best = max(
        certificates,
        key=lambda item: float(item["projection"].mid()),
    )
    passing = [
        item["family"][0] for item in certificates
        if item["verdict"] == "PASS"
    ]
    return {
        "pool_size": len(certificates),
        "passing_count": len(passing),
        "passing_labels": tuple(passing),
        "best_midpoint_label": best["family"][0],
        "best_midpoint_certificate": best,
    }


def report_record(block):
    full_admissions = tuple(
        d for d in block.labels if block.start <= d < block.stop
    )
    greedy, trace = block.greedy_family()
    prefix_cutoff, prefix = first_certifying_prefix(block)
    records = {
        "start": block.start,
        "stop": block.stop,
        "theta": block.theta,
        "positive_energy": block.positive_energy,
        "negative_budget": block.negative_budget,
        "residual": block.residual,
        "candidate_probe_count": len(block.labels),
        "greedy_family": greedy,
        "greedy_trace": trace,
        "singleton_scan": singleton_scan(block),
        "divisor_singleton_scan": singleton_scan(block, block.labels[1:]),
        "affine_only": block.certificate((AFFINE,)),
        "divisor_3_only": block.certificate((3,)),
        "new_admissions_only": block.certificate(full_admissions),
        "first_prefix_cutoff": prefix_cutoff,
        "first_prefix": prefix,
    }
    if block.start == 219:
        records["affine_plus_219"] = block.certificate((AFFINE, 219))
        records["affine_plus_227"] = block.certificate((AFFINE, 227))
        records["affine_plus_229"] = block.certificate((AFFINE, 229))
        records["divisor_3_plus_215"] = block.certificate((3, 215))
    return records


def jsonable(value):
    if isinstance(value, arb):
        return interval_text(value)
    if isinstance(value, tuple):
        return [jsonable(item) for item in value]
    if isinstance(value, list):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bits", type=int, default=192)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    if args.bits < 128:
        parser.error("--bits must be at least 128 for fail-closed certification")
    ctx.prec = args.bits
    records = []
    print("CERTIFIED FINITE DIAGNOSTIC ONLY; NOT AN ASYMPTOTIC THEOREM OR RH PROOF")
    print("greedy ordering uses Arb midpoints; all displayed verdicts use Arb balls")
    for start, stop in HARD_BLOCKS:
        block = CompensatedBlock(start, stop, args.bits)
        record = report_record(block)
        records.append(record)
        print(f"\nblock [{start},{stop}), theta={interval_text(block.theta, 18)}")
        print(
            "  positive={}  budget={}  residual={}".format(
                interval_text(block.positive_energy, 18),
                interval_text(block.negative_budget, 18),
                interval_text(block.residual, 18),
            )
        )
        print(
            f"  midpoint-greedy family={record['greedy_family']} "
            f"rank={len(record['greedy_family'])}"
        )
        for row in record["greedy_trace"]:
            print(
                "    add {}: gain={} projection={} margin={} {}".format(
                    row["label"], interval_text(row["gain"], 18),
                    interval_text(row["projection"], 18),
                    interval_text(row["margin"], 18), row["verdict"],
                )
            )
        scan = record["singleton_scan"]
        divisor_scan = record["divisor_singleton_scan"]
        print(
            f"  exhaustive atomic singletons: {scan['passing_count']}/"
            f"{scan['pool_size']} pass; midpoint-best="
            f"{scan['best_midpoint_label']}"
        )
        print(
            f"  exhaustive divisor singletons: {divisor_scan['passing_count']}/"
            f"{divisor_scan['pool_size']} pass; midpoint-best="
            f"{divisor_scan['best_midpoint_label']}"
        )
        for name in ("affine_only", "divisor_3_only", "new_admissions_only"):
            certificate = record[name]
            print(
                f"  {name}: rank={certificate['rank']} "
                f"projection={interval_text(certificate['projection'], 18)} "
                f"margin={interval_text(certificate['margin'], 18)} "
                f"{certificate['verdict']}"
            )
        prefix = record["first_prefix"]
        print(
            "  first squarefree prefix: cutoff={} rank={} margin={} {}".format(
                record["first_prefix_cutoff"], prefix["rank"],
                interval_text(prefix["margin"], 18), prefix["verdict"],
            )
        )
        if start == 219:
            for name in (
                "affine_plus_219", "affine_plus_227", "affine_plus_229",
                "divisor_3_plus_215",
            ):
                certificate = record[name]
                print(
                    f"  {name}: projection="
                    f"{interval_text(certificate['projection'], 18)} "
                    f"margin={interval_text(certificate['margin'], 18)} "
                    f"{certificate['verdict']}"
                )
    if args.json:
        payload = {
            "scope": "certified finite diagnostic only; no RH claim",
            "arb_precision_bits": args.bits,
            "complete_gram": "restricted Vasyunin formula; no cell cutoff",
            "greedy_ordering": "Arb midpoints (diagnostic only)",
            "verdicts": "outward Arb; unresolved signs raise RuntimeError",
            "blocks": records,
        }
        args.json.write_text(json.dumps(jsonable(payload), indent=2) + "\n")


if __name__ == "__main__":
    main()
