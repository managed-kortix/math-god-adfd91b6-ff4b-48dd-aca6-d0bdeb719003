#!/usr/bin/env python3
"""Fail-closed exact audit of the rank-uniform sharp-DNN cactus frontier.

The certificate works in Q(sqrt(5))[K] with degree at most one.  It proves
that every comparison cancels its symbolic K coefficient; no finite list of
ranks is used to establish the arbitrary-rank reduction.  It does not verify
the sharp DNN theorem or the structural theorems closing the residual families.
"""

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class Qsqrt5:
    rational: Fraction
    radical: Fraction = Fraction(0)

    def __add__(self, other):
        other = as_qsqrt5(other)
        return Qsqrt5(self.rational + other.rational, self.radical + other.radical)

    __radd__ = __add__

    def __neg__(self):
        return Qsqrt5(-self.rational, -self.radical)

    def __sub__(self, other):
        return self + (-as_qsqrt5(other))

    def __rsub__(self, other):
        return as_qsqrt5(other) - self

    def __mul__(self, other):
        other = as_qsqrt5(other)
        return Qsqrt5(
            self.rational * other.rational + 5 * self.radical * other.radical,
            self.rational * other.radical + self.radical * other.rational,
        )

    __rmul__ = __mul__

    def sign(self):
        a, b = self.rational, self.radical
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0:
            return (b > 0) - (b < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        comparison = a * a - 5 * b * b
        require(comparison != 0, "unexpected zero in Q(sqrt(5)) sign test")
        if a > 0:
            return 1 if comparison > 0 else -1
        return -1 if comparison > 0 else 1

    def __lt__(self, other):
        return (self - other).sign() < 0

    def __gt__(self, other):
        return (self - other).sign() > 0

    def canonical(self):
        return [fraction_text(self.rational), fraction_text(self.radical)]


def as_qsqrt5(value):
    if isinstance(value, Qsqrt5):
        return value
    return Qsqrt5(Fraction(value))


@dataclass(frozen=True)
class AffineK:
    """An exact c*K+d in Q(sqrt(5))[K]."""

    k_coefficient: Qsqrt5
    constant: Qsqrt5

    def __add__(self, other):
        other = as_affine(other)
        return AffineK(
            self.k_coefficient + other.k_coefficient,
            self.constant + other.constant,
        )

    __radd__ = __add__

    def __neg__(self):
        return AffineK(-self.k_coefficient, -self.constant)

    def __sub__(self, other):
        return self + (-as_affine(other))

    def __rsub__(self, other):
        return as_affine(other) - self

    def __mul__(self, scalar):
        scalar = as_qsqrt5(scalar)
        return AffineK(self.k_coefficient * scalar, self.constant * scalar)

    __rmul__ = __mul__

    def evaluate(self, k):
        require(isinstance(k, int), "symbolic substitution requires an integer K")
        return self.k_coefficient * k + self.constant

    def canonical(self):
        return {
            "K": self.k_coefficient.canonical(),
            "constant": self.constant.canonical(),
        }


def as_affine(value):
    if isinstance(value, AffineK):
        return value
    return AffineK(Qsqrt5(Fraction(0)), as_qsqrt5(value))


K = AffineK(Qsqrt5(Fraction(1)), Qsqrt5(Fraction(0)))
ZERO = Qsqrt5(Fraction(0))
ONE = Qsqrt5(Fraction(1))
EXPECTED_A = Qsqrt5(Fraction(5), Fraction(-2))
EXPECTED_SURVIVORS = ("T^(K-1)Q", "T^(K-2)PP")
SUBSTITUTION_RANKS = (2, 3, 4, 5, 7, 13, 64)
EXPECTED_CERTIFICATE_SHA256 = "1b549165c84ab20bdaebfec9329c37fb3e808ef435bda7a3586c8285c2d075ca"


@dataclass(frozen=True)
class ComparisonRecord:
    name: str
    domain: str
    left: AffineK
    relation: str
    right: AffineK

    def gap(self):
        return self.right - self.left

    def canonical(self):
        return {
            "type": "comparison",
            "name": self.name,
            "domain": self.domain,
            "left": self.left.canonical(),
            "relation": self.relation,
            "right": self.right.canonical(),
            "right_minus_left": self.gap().canonical(),
        }


@dataclass(frozen=True)
class SurvivorRecord:
    family: str
    domain: str
    triangle_count: AffineK
    other_cycle_count: AffineK
    total_cycle_count: AffineK
    dnn_gap_relation: str
    dnn_gap_bound: AffineK

    def canonical(self):
        return {
            "type": "survivor",
            "family": self.family,
            "domain": self.domain,
            "triangle_count": self.triangle_count.canonical(),
            "other_cycle_count": self.other_cycle_count.canonical(),
            "total_cycle_count": self.total_cycle_count.canonical(),
            "dnn_gap_relation": self.dnn_gap_relation,
            "dnn_gap_bound": self.dnn_gap_bound.canonical(),
        }


def build_symbolic_records(
    *,
    a=EXPECTED_A,
    h_ge_lower=3,
    h_pair=2,
    survivors=EXPECTED_SURVIVORS,
    triangle_k_coefficient=1,
):
    """Generate the certificate ledger using the same exact arithmetic it audits."""
    a = as_qsqrt5(a)
    triangle_base = triangle_k_coefficient * K
    threshold = K - 1
    epsilon7_upper = Qsqrt5(Fraction(7, 15))

    # For h nontriangles, (K-h) triangles plus h contributions bounded by a.
    h_endpoint_upper = triangle_base - h_ge_lower + h_ge_lower * a
    h_increment = as_affine(a - 1)
    pair_nonpp_upper = triangle_base - h_pair + a + epsilon7_upper
    pair_pp = triangle_base - h_pair + 2 * a

    comparisons = (
        ComparisonRecord(
            "h>=3 endpoint monotonicity",
            f"integer h>={h_ge_lower}; increment when h increases",
            h_increment,
            "<",
            as_affine(0),
        ),
        ComparisonRecord(
            "h>=3 maximal endpoint",
            f"h={h_ge_lower}; upper bound for all h>={h_ge_lower}",
            h_endpoint_upper,
            "<",
            threshold,
        ),
        ComparisonRecord(
            "h=2 non-PP",
            f"h={h_pair}; even-containing or odd pair other than PP",
            pair_nonpp_upper,
            "<",
            threshold,
        ),
        ComparisonRecord(
            "h=2 PP survives",
            f"h={h_pair}; pair=PP",
            pair_pp,
            ">",
            threshold,
        ),
    )

    survivor_records = (
        SurvivorRecord(
            survivors[0],
            "h<=1 (Q=T represents h=0)",
            K - 1,
            as_affine(1),
            K,
            "<=",
            as_affine(0),
        ),
        SurvivorRecord(
            survivors[1],
            "h=2; pair=PP",
            K - 2,
            as_affine(2),
            K,
            "<",
            threshold - pair_pp,
        ),
    )
    return comparisons + survivor_records


def prove_comparison(record):
    gap = record.gap()
    require(gap.k_coefficient == ZERO,
            f"{record.name}: K did not cancel symbolically")
    sign = gap.constant.sign()
    expected = {"<": 1, ">": -1}.get(record.relation)
    require(expected is not None, f"{record.name}: unsupported relation")
    require(sign == expected, f"{record.name}: exact inequality failed")


def verify_substitution_identities(records):
    """Semantically test every serialized affine template, including K=5."""
    for record in records:
        expressions = []
        if isinstance(record, ComparisonRecord):
            expressions = (record.left, record.right, record.gap())
            for k in SUBSTITUTION_RANKS:
                require(record.gap().evaluate(k) == record.right.evaluate(k) - record.left.evaluate(k),
                        f"{record.name}: substitution identity failed at K={k}")
        else:
            expressions = (
                record.triangle_count,
                record.other_cycle_count,
                record.total_cycle_count,
                record.dnn_gap_bound,
            )
            for k in SUBSTITUTION_RANKS:
                require(
                    record.triangle_count.evaluate(k) + record.other_cycle_count.evaluate(k)
                    == record.total_cycle_count.evaluate(k),
                    f"{record.family}: cycle-count identity failed at K={k}",
                )
        for expression in expressions:
            for k in SUBSTITUTION_RANKS:
                direct = expression.k_coefficient * k + expression.constant
                require(expression.evaluate(k) == direct,
                        f"affine substitution implementation failed at K={k}")


def audit(**record_mutations):
    a = as_qsqrt5(record_mutations.get("a", EXPECTED_A))
    require(a == EXPECTED_A, "epsilon_5 exact radical changed")
    require(ZERO < a < ONE, "0 < epsilon_5 < 1 failed")
    require(3 * a < 2, "3 epsilon_5 < 2 failed")
    require(2 * a > 1, "2 epsilon_5 > 1 failed")
    require(Fraction(2159, 2401) > Fraction(7, 8),
            "cos(pi/7) lower certificate is too weak")
    require(Fraction(67, 30) ** 2 < 5, "67/30 < sqrt(5) certificate failed")
    require(Qsqrt5(Fraction(7, 15)) < ONE - a, "epsilon_5+epsilon_7 < 1 failed")

    require(record_mutations.get("h_ge_lower", 3) == 3, "h>=3 boundary changed")
    require(record_mutations.get("h_pair", 2) == 2, "h=2 boundary changed")
    require(tuple(record_mutations.get("survivors", EXPECTED_SURVIVORS)) == EXPECTED_SURVIVORS,
            "survivor families changed")

    records = build_symbolic_records(**record_mutations)
    require(len(records) == 6, "symbolic ledger length changed")
    for record in records:
        if isinstance(record, ComparisonRecord):
            prove_comparison(record)

    survivor_records = tuple(record for record in records if isinstance(record, SurvivorRecord))
    require(tuple(record.family for record in survivor_records) == EXPECTED_SURVIVORS,
            "symbolic survivor ledger changed")
    require(survivor_records[0].dnn_gap_relation == "<=", "h<=1 gap direction changed")
    require(survivor_records[0].dnn_gap_bound == as_affine(0), "h<=1 gap bound changed")
    require(survivor_records[1].dnn_gap_relation == "<", "PP gap direction changed")
    require(survivor_records[1].dnn_gap_bound.k_coefficient == ZERO,
            "PP survivor K coefficient did not cancel")
    require(survivor_records[1].dnn_gap_bound.constant < ZERO,
            "PP survivor is not DNN-nonstrict")

    verify_substitution_identities(records)
    payload = json.dumps(
        [record.canonical() for record in records],
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ) + "\n"
    return sha256(payload.encode("ascii")).hexdigest()


def expect_rejected(action, label):
    try:
        action()
    except (RuntimeError, IndexError):
        return
    raise RuntimeError(f"hostile mutation was accepted: {label}")


def hostile_self_checks():
    mutations = (
        (lambda: audit(triangle_k_coefficient=2), "K coefficient"),
        (lambda: audit(a=Qsqrt5(Fraction(5), Fraction(2))), "radical sign"),
        (lambda: audit(h_ge_lower=4), "h>=3 boundary"),
        (lambda: audit(h_pair=3), "h=2 boundary"),
        (lambda: audit(survivors=("T^(K-1)Q",)), "missing PP survivor"),
        (lambda: audit(survivors=tuple(reversed(EXPECTED_SURVIVORS))), "survivor order"),
        (lambda: audit(survivors=("T^(K-1)P", "T^(K-2)PP")), "changed Q survivor"),
    )
    for action, label in mutations:
        expect_rejected(action, label)
    return len(mutations)


def main():
    digest = audit()
    require(digest == EXPECTED_CERTIFICATE_SHA256, "symbolic certificate digest changed")
    mutation_count = hostile_self_checks()
    require(mutation_count == 7, "hostile mutation count changed")
    print("rank-uniform sharp-DNN cactus frontier: symbolic exact audit passed")
    print("frontier display (not a trusted function): T^(K-1)Q, T^(K-2)PP")
    print("symbolic_variable: K (integer K>=2); no representative-rank proof calls")
    print("semantic_substitutions: " + ",".join(map(str, SUBSTITUTION_RANKS)))
    print(f"certificate_sha256: {digest}")
    print(f"rejected_hostile_mutations: {mutation_count}")
    print("status: DNN frontier only; structural closure is dependency-based")


if __name__ == "__main__":
    main()
