#!/usr/bin/env python3
"""Fail-closed finite replay of the independent R21 analytic kernel.

This dependency-free standard-library program authenticates exact source bytes
and statement tokens, then checks only finite algebra and logical ledgers.  It
does NOT prove the universally quantified spectral, attachment, opening, or
territory theorems whose source receipts it authenticates.
"""

from __future__ import annotations

import ast
import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


REPO = Path(__file__).resolve().parents[1]

SOURCE_SPECS = {
    "packing_two": {
        "path": "packing-two-square-energy/paper.tex",
        "sha256": "9638f6847892e8a043454d945e7945418ec96e393b639dfd65f664670dba8791",
        "bytes": 44126,
        "lines": 1043,
        "tokens": {
            "sign_theorem": r"\begin{theorem}\label{thm:main}",
            "packing_hypothesis":
                "Let $G$ be a finite simple graph that contains a cycle and satisfies\n"
                r"$\vp(G)\le2$.",
            "favourable_phase":
                r"If every cycle of $G$ has length congruent to $3\pmod4$, then",
            "cycle_territories":
                r"\begin{lemma}[Cycle territories]\label{lem:cycle-territories}",
            "maximum_packing":
                "maximum-cardinality collection of pairwise vertex-disjoint cycles",
            "packing_one_territory": "cycle packing number is one.",
            "territory_credit": r"s^+(G_i)>m_i\ge n_i,",
            "triangular_source_corollary":
                r"\begin{corollary}[Triangular block graphs]\label{cor:triangular-block}",
            "literal_triangle_scope":
                "Here triangular means that every cyclic block is a triangle; bridge blocks",
            "arbitrary_trees_scope": "and arbitrary attached trees are allowed.",
            "four_triangle_proposition":
                r"\begin{proposition}[Tetracyclic block graphs]\label{prop:tetracyclic-block}",
            "central_star_classification":
                r"This proves the required one-cluster classification; $T_0$ is the central",
            "packing_four_disposition":
                "If $p=4$, contract the four\npairwise disjoint triangle blocks",
            "central_imaginary_identity": r"\label{eq:tetracyclic-imaginary}",
            "central_injection": r"\label{eq:central-deletion-bound}",
            "petal_injection": r"\label{eq:petal-deletion-bound}",
            "four_term_domination":
                r"\sum_{j=0}^3Z_{G-V(T_j)}(t)>4Z_F(t).",
        },
    },
    "heptacyclic_shared_triangle": {
        "path": "all-heptacyclic-cacti/paper.tex",
        "sha256": "9323dc212d36b610a66e890df3a267242ae0800efcd445dd911575cc2bd9a4d1",
        "bytes": 31896,
        "lines": 730,
        "tokens": {
            "superadditivity": r"\begin{equation}\label{eq:super}",
            "a4_base": r"\sig(A_4)>3,",
            "packing_two_receipt": r"\cite[Proposition~4.11]{PackingTwo}",
            "territory_lemma":
                r"\begin{lemma}[Arbitrary connector territories]\label{lem:territories}",
            "opening_lemma":
                r"\begin{lemma}[Intervals and private openings]\label{lem:intervals}",
            "recurrence_lemma":
                r"\begin{lemma}[Shared-triangle recurrence]\label{lem:triangle-recurrence}",
            "tree_cost": "The opened territory is a nonempty tree",
            "recurrence": r"\sig(A_r)\geq\sig(A_{r-1})-1.",
            "strict_outputs":
                r"\sig(A_5)>2$, $\sig(A_6)>1$, and $\sig(A_7)>0$.",
            "main_theorem": r"\begin{theorem}\label{thm:main}",
        },
    },
    "tricyclic_c5_floor": {
        "path": "all-tricyclic-cacti/paper.tex",
        "sha256": "d928a56b0257936fcc326ddc2c85e40593117a7749b55502bb42379c805e71e8",
        "bytes": 17669,
        "lines": 434,
        "tokens": {
            "arbitrary_tree_scope":
                "The following hold, with arbitrary tree attachments.",
            "branch_recurrence": r"\begin{equation}\label{eq:BP}",
            "effective_activities": r"activity $a_v=t+y_v$, $y_v\geq0$",
            "packet_lemma":
                r"\begin{lemma}[Phase and packet bounds]\label{lem:packets}",
            "unicycle_floor":
                r"A unicyclic $C_q$ cactus with $q=1\pmod4$ satisfies",
            "eliminated_phase": r"$\Psi/K=Z_{C_q}(a)+2i$.",
            "coefficient_monotonicity": "coefficientwise monotonicity of",
            "cycle_formula":
                r"s^+(C_q)=q+1-\sec(\pi/q),\qquad D(C_q)=-2\delta_q.",
            "coulson_step": "Coulson integration proves (2).",
            "main_theorem": r"\begin{theorem}\label{thm:main}",
        },
    },
}


@dataclass(frozen=True)
class Surd5:
    """An exact element a+b*sqrt(5), with rational a,b."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", Fraction(self.a))
        object.__setattr__(self, "b", Fraction(self.b))

    def __add__(self, other: Surd5 | int | Fraction) -> Surd5:
        rhs = as_surd(other)
        return Surd5(self.a + rhs.a, self.b + rhs.b)

    __radd__ = __add__

    def __neg__(self) -> Surd5:
        return Surd5(-self.a, -self.b)

    def __sub__(self, other: Surd5 | int | Fraction) -> Surd5:
        return self + (-as_surd(other))

    def __rsub__(self, other: Surd5 | int | Fraction) -> Surd5:
        return as_surd(other) - self

    def __mul__(self, other: Surd5 | int | Fraction) -> Surd5:
        rhs = as_surd(other)
        return Surd5(self.a * rhs.a + 5 * self.b * rhs.b,
                     self.a * rhs.b + self.b * rhs.a)

    __rmul__ = __mul__

    def __truediv__(self, other: Surd5 | int | Fraction) -> Surd5:
        rhs = as_surd(other)
        denominator = rhs.a * rhs.a - 5 * rhs.b * rhs.b
        require(denominator != 0, "division by zero in Q(sqrt(5))")
        numerator = self * Surd5(rhs.a, -rhs.b)
        return Surd5(numerator.a / denominator, numerator.b / denominator)

    def __pow__(self, exponent: int) -> Surd5:
        require(type(exponent) is int and exponent >= 0,
                "Surd5 exponent must be a nonnegative integer")
        answer = Surd5(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                answer = answer * base
            base = base * base
            power //= 2
        return answer

    def sign(self) -> int:
        """Return the exact sign, using rational square comparison only."""
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.b < 0:
            return -(-self).sign()
        if self.a >= 0:
            return 1
        comparison = 5 * self.b * self.b - self.a * self.a
        require(comparison != 0,
                "unexpected rational equality to a nonzero multiple of sqrt(5)")
        return (comparison > 0) - (comparison < 0)

    def render(self) -> str:
        def q(value: Fraction) -> str:
            return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"

        if self.b == 0:
            return q(self.a)
        if self.a == 0:
            return "sqrt(5)" if self.b == 1 else ("-sqrt(5)" if self.b == -1 else f"{q(self.b)}*sqrt(5)")
        sign = "+" if self.b > 0 else "-"
        coefficient = "" if abs(self.b) == 1 else f"{q(abs(self.b))}*"
        return f"{q(self.a)}{sign}{coefficient}sqrt(5)"


def as_surd(value: Surd5 | int | Fraction) -> Surd5:
    return value if isinstance(value, Surd5) else Surd5(Fraction(value))


ZERO = Surd5(0)
ONE = Surd5(1)
SQRT5 = Surd5(0, 1)


def polynomial_multiply(left: tuple[Surd5, ...],
                        right: tuple[Surd5, ...]) -> tuple[Surd5, ...]:
    answer = [ZERO for _ in range(len(left) + len(right) - 1)]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] = answer[i + j] + a * b
    return tuple(answer)


def polynomial_from_roots(roots: Iterable[Surd5]) -> tuple[Surd5, ...]:
    answer = (ONE,)
    for root in roots:
        answer = polynomial_multiply(answer, (-root, ONE))
    return answer


@dataclass(frozen=True)
class RationalLowerBound:
    """The proposition x>value if strict, and x>=value otherwise."""

    value: Fraction
    strict: bool

    def __add__(self, other: RationalLowerBound) -> RationalLowerBound:
        return RationalLowerBound(self.value + other.value,
                                  self.strict or other.strict)

    def proves_strictly_above(self, threshold: int | Fraction) -> bool:
        target = Fraction(threshold)
        return self.value > target or (self.value == target and self.strict)


def authenticate_sources() -> tuple[dict[str, object], dict[str, str]]:
    reports: dict[str, object] = {}
    texts: dict[str, str] = {}
    for name, raw_spec in SOURCE_SPECS.items():
        path = REPO / str(raw_spec["path"])
        require(path.is_file(), f"missing pinned source: {path}")
        source_bytes = path.read_bytes()
        digest = hashlib.sha256(source_bytes).hexdigest()
        require(digest == raw_spec["sha256"],
                f"source byte pin failed for {raw_spec['path']}: {digest}")
        require(len(source_bytes) == raw_spec["bytes"],
                f"source byte length failed for {raw_spec['path']}: {len(source_bytes)}")
        require(source_bytes.count(b"\n") == raw_spec["lines"],
                f"source line count failed for {raw_spec['path']}: {source_bytes.count(b'\n')}")
        text = source_bytes.decode("utf-8")
        token_report = {}
        for label, token in dict(raw_spec["tokens"]).items():
            count = text.count(token)
            require(count == 1,
                    f"semantic token {name}:{label} occurs {count} times")
            token_report[label] = count
        texts[name] = text
        reports[name] = {
            "path": raw_spec["path"],
            "sha256": digest,
            "bytes": len(source_bytes),
            "lines": source_bytes.count(b"\n"),
            "semantic_tokens": token_report,
        }

    packing = texts["packing_two"]
    packing_main = packing.index(r"\begin{theorem}\label{thm:main}")
    packing_territories = packing.index(
        r"\begin{lemma}[Cycle territories]\label{lem:cycle-territories}")
    packing_triangular = packing.index(
        r"\begin{corollary}[Triangular block graphs]\label{cor:triangular-block}")
    packing_a4 = packing.index(
        r"\begin{proposition}[Tetracyclic block graphs]\label{prop:tetracyclic-block}")
    require(packing_main < packing_territories < packing_triangular < packing_a4,
            "packing-two dependency sections are out of expected order")
    packing_a4_end = packing.index(
        r"\begin{proposition}[Block graphs of cyclomatic number five]", packing_a4)
    packing_a4_slice = packing[packing_a4:packing_a4_end]
    require(r"If $p=4$" in packing_a4_slice and
            r"Suppose finally that $p=3$" in packing_a4_slice and
            "The same phase and Coulson argument again yields" in packing_a4_slice,
            "A4 proposition lost one of its packing-four/packing-three proof branches")
    require(packing_a4_slice.count(
                r"Proposition~\ref{prop:tetracyclic-block}") == 1 and
            "also an immediate instance" in packing_a4_slice,
            "unexpected self-reference inside the A4 proposition slice")

    hepta = texts["heptacyclic_shared_triangle"]
    base_start = hepta.index(r"\begin{equation}\label{eq:triangle-small}")
    base_end = hepta.index(r"\section{Territories, intervals, and openings}", base_start)
    recurrence_start = hepta.index(
        r"\begin{lemma}[Shared-triangle recurrence]\label{lem:triangle-recurrence}")
    recurrence_end = hepta.index(r"\section{The exact DNN residual classification}",
                                 recurrence_start)
    main_start = hepta.index(r"\begin{theorem}\label{thm:main}")
    require(base_start < recurrence_start < recurrence_end < main_start,
            "shared-triangle base/recurrence is not before the heptacyclic main theorem")
    require("PackingTwo" in hepta[base_start:base_end],
            "A4 base slice lost its PackingTwo receipt")
    require("thm:main" not in hepta[base_start:base_end],
            "A4 base slice cites the heptacyclic main theorem")
    require("thm:main" not in hepta[recurrence_start:recurrence_end],
            "shared-triangle recurrence cites the heptacyclic main theorem")
    require("eq:lower-rank" not in hepta[recurrence_start:recurrence_end],
            "shared-triangle recurrence imports the qualitative lower-rank theorem")

    tricycle = texts["tricyclic_c5_floor"]
    branch_start = tricycle.index(r"\begin{equation}\label{eq:BP}")
    packet_start = tricycle.index(
        r"\begin{lemma}[Phase and packet bounds]\label{lem:packets}")
    packet_end = tricycle.index(r"\section{The exact DNN reduction}", packet_start)
    tricycle_main = tricycle.index(r"\begin{theorem}\label{thm:main}")
    require(branch_start < packet_start < packet_end < tricycle_main,
            "tree elimination/C5 packet proof is not before the tricyclic main theorem")
    require("thm:main" not in tricycle[branch_start:packet_end],
            "tree elimination/C5 packet proof cites the tricyclic main theorem")
    c5_start = tricycle.index(r"For (2), \eqref{eq:BP} gives", packet_start)
    c5_end = tricycle.index("For the mixed packet", c5_start)
    c5_slice = tricycle[c5_start:c5_end]
    for token in (r"\Psi/K=Z_{C_q}(a)+2i", "coefficientwise monotonicity",
                  r"s^+(C_q)=q+1-\sec(\pi/q)",
                  "Coulson integration proves (2)."):
        require(token in c5_slice, f"C5 item-(2) proof slice lost token: {token}")
    require("AllBicyclic" not in c5_slice and "thm:main" not in c5_slice,
            "C5 item-(2) proof imports a later/external main theorem")

    return reports, texts


def audit_exact_c5() -> dict[str, object]:
    alpha = (SQRT5 - 1) / 2
    beta = -(SQRT5 + 1) / 2
    roots = (Surd5(2), alpha, alpha, beta, beta)
    require(alpha.sign() > 0 and beta.sign() < 0,
            "C5 radical roots have wrong signs")

    characteristic = polynomial_from_roots(roots)
    expected = tuple(Surd5(value) for value in (-2, 5, 0, -5, 0, 1))
    require(characteristic == expected,
            "C5 radical roots do not factor x^5-5x^3+5x-2")

    positive_square_energy = Surd5(2) ** 2 + 2 * alpha ** 2
    require(positive_square_energy == 7 - SQRT5,
            "wrong exact positive square energy for C5")
    sigma_c5 = positive_square_energy - 5
    delta = SQRT5 - 2
    cosine_pi_over_five = (ONE + SQRT5) / 4
    secant_pi_over_five = ONE / cosine_pi_over_five
    require(secant_pi_over_five == SQRT5 - 1,
            "wrong exact sec(pi/5) identity")
    require(secant_pi_over_five - 1 == delta,
            "wrong C5 phase deficit")
    require(sigma_c5 == -delta,
            "bare C5 does not attain the claimed non-strict floor")
    require(delta.sign() > 0 and (ONE - delta).sign() > 0,
            "failed exact inequalities 0<sqrt(5)-2<1")
    require((sigma_c5 + 1).sign() > 0,
            "C5 floor is not strictly above -1")

    return {
        "characteristic_polynomial_coefficients_ascending":
            [coefficient.render() for coefficient in characteristic],
        "positive_eigenvalue_types": ["2", alpha.render(), alpha.render()],
        "s_plus_C5": positive_square_energy.render(),
        "sigma_C5": sigma_c5.render(),
        "delta_5": delta.render(),
        "sec_pi_over_5": secant_pi_over_five.render(),
        "floor_relation": "sigma(attached C5)>=-delta_5>-1 (universal first inequality is a source theorem)",
    }


def integer_partitions(total: int, maximum: int | None = None) -> Iterable[tuple[int, ...]]:
    if total == 0:
        yield ()
        return
    cap = total if maximum is None else min(total, maximum)
    for head in range(cap, 0, -1):
        for tail in integer_partitions(total - head, head):
            yield (head, *tail)


def audit_four_triangle_intersection_graphs() -> dict[str, object]:
    """Enumerate the finite four-block intersection-graph classification."""
    vertices = range(4)
    possible_edges = tuple(itertools.combinations(vertices, 2))
    connected_by_alpha = {1: 0, 2: 0, 3: 0, 4: 0}
    alpha_three_degree_sequences = set()

    for mask in range(1 << len(possible_edges)):
        edges = {possible_edges[index]
                 for index in range(len(possible_edges)) if mask & (1 << index)}
        neighbors = {vertex: set() for vertex in vertices}
        for left, right in edges:
            neighbors[left].add(right)
            neighbors[right].add(left)
        reached = {0}
        frontier = [0]
        while frontier:
            current = frontier.pop()
            for neighbor in neighbors[current]:
                if neighbor not in reached:
                    reached.add(neighbor)
                    frontier.append(neighbor)
        if len(reached) != 4:
            continue

        alpha = 0
        for subset_mask in range(1 << 4):
            subset = {vertex for vertex in vertices if subset_mask & (1 << vertex)}
            if all(not ({left, right} <= subset) for left, right in edges):
                alpha = max(alpha, len(subset))
        connected_by_alpha[alpha] += 1
        if alpha == 3:
            alpha_three_degree_sequences.add(
                tuple(sorted(len(neighbors[vertex]) for vertex in vertices)))

    require(connected_by_alpha[4] == 0,
            "a connected four-node intersection graph unexpectedly has packing four")
    require(connected_by_alpha[3] == 4 and
            alpha_three_degree_sequences == {(1, 1, 1, 3)},
            "packing-three four-triangle incidence is not exactly a labelled K1,3")
    require(sum(connected_by_alpha.values()) == 38,
            "wrong number of connected labelled graphs on four vertices")
    return {
        "connected_labelled_graphs_by_independence_number":
            {str(key): value for key, value in connected_by_alpha.items()},
        "packing_three_classes": 4,
        "packing_three_degree_sequence": [1, 1, 1, 3],
        "conclusion": "connected + packing three forces central triangle with three independent petals",
    }


def audit_finite_ledgers() -> dict[str, object]:
    # If S=sum of the four positive matching partitions and F>0, the source
    # injection gives S>4F.  The exact boundary -2*(4F)+8F=0 means
    # -2S+8F<0.  This checks the coefficient implication, not the injection.
    require(-2 * 4 + 8 == 0,
            "central-triangle imaginary coefficients do not cancel at equality")

    b = {1: 0, 2: 1, 3: 2, 4: 3}
    b[5] = b[4] - 1
    b[6] = b[5] - 1
    require((b[4], b[5], b[6]) == (3, 2, 1),
            "shared-triangle recurrence is not 3 -> 2 -> 1")

    partitions = tuple(integer_partitions(6))
    require(len(partitions) == 11 and len(set(partitions)) == 11,
            "did not generate the 11 integer partitions of six")
    partition_report = {}
    for partition in partitions:
        require(sum(partition) == 6 and all(1 <= part <= 6 for part in partition),
                f"invalid partition {partition}")
        if partition == (1, 1, 1, 1, 1, 1):
            # Replace two nearest singleton clusters by one arbitrary-connector
            # TT territory (>1); each of the other four territories is >0.
            bound = RationalLowerBound(Fraction(1), True)
            for _ in range(4):
                bound += RationalLowerBound(Fraction(0), True)
            route = "nearest-singleton-pair TT plus four positive triangular territories"
        else:
            bound = RationalLowerBound(Fraction(0), False)
            for part in partition:
                bound += RationalLowerBound(Fraction(b[part]), True)
            route = "whole shared-cut clusters plus positive triangular territories"
        require(bound.proves_strictly_above(1),
                f"six-triangle ledger does not prove >1 for {partition}")
        partition_report["+".join(map(str, partition))] = {
            "strict_lower_constant": str(bound.value),
            "route": route,
        }

    # Conditional owner-fibre implications.  The script checks that the
    # triangle counts stay nonzero and that strict lower bounds add correctly;
    # the universal territory theorem remains an analytic premise.
    theta_fibres = {}
    tree = RationalLowerBound(Fraction(-1), False)
    six_triangles = RationalLowerBound(Fraction(1), True)
    zero_case = tree + six_triangles
    require(zero_case.proves_strictly_above(0),
            "tree plus six-triangle fibre does not close strictly")
    theta_fibres["k=0"] = ">1 + (-1) > 0"
    for k in range(1, 6):
        require(k >= 1 and 6 - k >= 1,
                "theta split produced an empty triangular side")
        left = RationalLowerBound(Fraction(0), True)
        right = RationalLowerBound(Fraction(0), True)
        require((left + right).proves_strictly_above(0),
                f"two triangular territories fail at k={k}")
        theta_fibres[f"k={k}"] = f"triangular({k}) + triangular({6-k}) > 0"

    anchor = RationalLowerBound(Fraction(1), True)
    require((anchor + tree).proves_strictly_above(0),
            "retained-C5 tree side does not close against a >1 anchor")
    for q in range(1, 5):
        triangular = RationalLowerBound(Fraction(0), True)
        require((anchor + triangular).proves_strictly_above(0),
                f"retained-C5 triangular side fails at q={q}")

    delta = SQRT5 - 2
    away_c5_constant = ONE - delta
    require(away_c5_constant.sign() > 0,
            ">1 anchor plus >=-delta C5 floor is not positive")

    # Connected rank-r cactus arithmetic: m-n=r-1 and D>0 imply
    # sigma=(m-n)+D/2>r-1.  These are the TT and A4 thresholds.
    require(2 - 1 == 1 and 4 - 1 == 3,
            "rank-to-surplus threshold arithmetic failed")

    return {
        "four_triangle_intersection_classification":
            audit_four_triangle_intersection_graphs(),
        "central_triangle_coefficient_implication":
            "S>4F and Im(Psi)=-2S+8F imply Im(Psi)<0",
        "shared_triangle_floors": {str(key): value for key, value in sorted(b.items())},
        "recurrence": "b4=3 -> b5=2 -> b6=1",
        "six_triangle_integer_partitions": partition_report,
        "triangular_territory_owner_fibres": theta_fibres,
        "retained_c5_conditional_ledger": {
            "q=0": "anchor>1 plus tree=-1 gives >0",
            "q=1..4": "anchor>1 plus nonempty triangular cactus>0 gives >0",
            "away_C5": "anchor>1 plus C5 floor>=-(sqrt(5)-2) gives >3-sqrt(5)>0",
        },
        "rank_arithmetic": {
            "two_triangles": "D>0 and m=n+1 imply sigma>1",
            "four_triangle_shared_base": "D>0 and m=n+3 imply sigma>3",
            "triangular_packing_one_territory": "D>0 and m>=n imply sigma>0",
        },
    }


def audit_optimization_stability() -> None:
    own_source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(own_source)
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            "verifier contains Python assert and is not -O stable")


def main() -> None:
    audit_optimization_stability()
    source_reports, _ = authenticate_sources()
    report = {
        "schema": "r21-independent-analytic-kernel/1",
        "status": "PASS_FINITE_LOGICAL_KERNEL_ONLY",
        "source_receipts": source_reports,
        "exact_c5_arithmetic": audit_exact_c5(),
        "finite_implications": audit_finite_ledgers(),
        "trust_boundary": [
            "No finite script proves the universally quantified packing-two spectral sign theorem.",
            "No finite script proves induced superadditivity or the universal physical territory/opening lemmas.",
            "No finite script proves tree elimination and phase comparison for every attached C5 unicycle.",
            "This report authenticates source bytes/tokens and checks only exact finite algebra and implications.",
            "This is not an R21 closure or theorem-promotion certificate.",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
