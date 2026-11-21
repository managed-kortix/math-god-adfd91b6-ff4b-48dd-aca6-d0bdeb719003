#!/usr/bin/env python3
"""Producer-independent reconstruction of the two family-H CNFs.

The checker imports neither ``snc_cnf`` nor an eventual family-H producer.  It
reconstructs the complete variable order and clause stream from the graph
semantics, hostile-parses the candidate DIMACS, and requires a canonical byte
encoding.  It certifies formula identity only; SAT/UNSAT needs a separately
replayed proof.

Two explicit envelopes are supported because DIMACS variable-map comments do
not affect proof semantics:

* ``mapped`` requires every ``c var <id> <name>`` line in canonical order;
* ``bare`` forbids comments and begins with the ``p cnf`` line.

There is no auto-detection: callers must bind one envelope in their manifest.
"""
import argparse
import hashlib
import itertools
from pathlib import Path

N = 18
V = 0
Q = 1
A = frozenset(range(1, 9))
B = frozenset(range(9, 16))
C = (16, 17)
CASES = {
    "A": {"r": 2, "g1": tuple(range(3, 9)), "g2": tuple(range(9, 16))},
    "B": {"r": 9, "g1": tuple(range(2, 9)), "g2": tuple(range(10, 16))},
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class Formula:
    def __init__(self):
        self.names = {}
        self.clauses = []

    def var(self, name):
        require(type(name) is str and name and "\n" not in name and " " not in name,
                "invalid variable name")
        if name not in self.names:
            self.names[name] = len(self.names) + 1
        return self.names[name]

    def add(self, *literals):
        require(all(type(literal) is int and literal != 0 for literal in literals),
                "invalid clause literal")
        self.clauses.append(tuple(literals))


def and_gate(formula, output, left, right):
    """output iff left and right."""
    formula.add(-output, left)
    formula.add(-output, right)
    formula.add(output, -left, -right)


def threshold(formula, inputs, tag):
    """Exact unary outputs: result[t-1] iff at least t inputs are true."""
    previous = []
    for width, input_var in enumerate(inputs, 1):
        current = []
        for target in range(1, width + 1):
            output = formula.var(f"cnt_{tag}_{width}_{target}")
            current.append(output)
            old_same = previous[target - 1] if target <= len(previous) else None
            old_lower = previous[target - 2] if target >= 2 else True
            # output <-> old_same OR (input_var AND old_lower), simplified
            # for the boundary constants.
            if old_same is not None:
                formula.add(-old_same, output)
            if old_lower is True:
                formula.add(-input_var, output)
            else:
                formula.add(-input_var, -old_lower, output)
            if old_same is None:
                if old_lower is True:
                    formula.add(-output, input_var)
                else:
                    formula.add(-output, input_var)
                    formula.add(-output, old_lower)
            elif old_lower is True:
                formula.add(-output, old_same, input_var)
            else:
                formula.add(-output, old_same, input_var)
                formula.add(-output, old_same, old_lower)
        previous = current
    return previous


def add_mu2_link(formula, out_thresholds, second_thresholds, mu2):
    """Link mu2 exactly to d+ - d++ = 2 under the base deficit bounds."""
    order = len(out_thresholds) + 1
    for target in range(2, order):
        formula.add(mu2, -out_thresholds[target - 1],
                    second_thresholds[target - 2])
    formula.add(-mu2, out_thresholds[1])
    for target in range(1, order - 2):
        formula.add(-mu2, -second_thresholds[target - 1],
                    out_thresholds[target + 1])
    formula.add(-mu2, -second_thresholds[order - 3])
    formula.add(-mu2, -second_thresholds[order - 2])


def reconstruct(case):
    """Reconstruct the canonical family-H relaxation for case A or B."""
    require(case in CASES, "case must be A or B")
    r_vertex = CASES[case]["r"]
    high_vertices = {Q, r_vertex}
    formula = Formula()
    arcs = [[formula.var(f"a_{i}_{j}") for j in range(N)] for i in range(N)]
    second = [[formula.var(f"q_{i}_{j}") for j in range(N)] for i in range(N)]
    paths = {}

    # Oriented-pair and exact-distance-two semantics.
    for i in range(N):
        formula.add(-arcs[i][i])
        formula.add(-second[i][i])
    for i in range(N):
        for j in range(i + 1, N):
            formula.add(-arcs[i][j], -arcs[j][i])
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            path_vars = []
            for k in range(N):
                if k in (i, j):
                    continue
                path = formula.var(f"p_{i}_{k}_{j}")
                paths[i, k, j] = path
                path_vars.append(path)
                and_gate(formula, path, arcs[i][k], arcs[k][j])
            reach = formula.var(f"r_{i}_{j}")
            for path in path_vars:
                formula.add(-path, reach)
            formula.add(-reach, *path_vars)
            # second[i][j] <-> reach AND NOT arcs[i][j].
            formula.add(-second[i][j], reach)
            formula.add(-second[i][j], -arcs[i][j])
            formula.add(second[i][j], -reach, arcs[i][j])

    # Exact degree mask and global strict badness with deficit at most two.
    for i in range(N):
        out_count = threshold(
            formula, [arcs[i][j] for j in range(N) if j != i], f"d1_{i}"
        )
        second_count = threshold(
            formula, [second[i][j] for j in range(N) if j != i], f"d2_{i}"
        )
        formula.add(out_count[7])       # d+(i) >= 8
        formula.add(-out_count[9])      # d+(i) <= 9
        formula.add(out_count[0])       # retained base-envelope redundancy
        for target in range(1, N - 1):
            formula.add(-second_count[target - 1], out_count[target])
        formula.add(-second_count[N - 2])
        for target in range(3, N):
            formula.add(-out_count[target - 1], second_count[target - 3])
        mu2 = formula.var(f"mu2_{i}")
        add_mu2_link(formula, out_count, second_count, mu2)
        formula.add(out_count[8] if i in high_vertices else -out_count[8])

    # h_ij is exactly the third oriented-pair state; exactly seven are true.
    holes = []
    for i in range(N):
        for j in range(i + 1, N):
            hole = formula.var(f"h_{i}_{j}")
            holes.append(hole)
            formula.add(-hole, -arcs[i][j])
            formula.add(-hole, -arcs[j][i])
            formula.add(hole, arcs[i][j], arcs[j][i])
    hole_count = threshold(formula, holes, "missing")
    formula.add(hole_count[6])
    formula.add(-hole_count[7])

    # Exact low-root layers A=N+(v), B=N++(v), including A->B support
    # and the implied A-not-to-C barrier.
    for j in range(N):
        formula.add(arcs[V][j] if j in A else -arcs[V][j])
        formula.add(second[V][j] if j in B else -second[V][j])
    for b_vertex in sorted(B):
        formula.add(*[arcs[a_vertex][b_vertex] for a_vertex in sorted(A)])
    for a_vertex in sorted(A):
        for c_vertex in C:
            formula.add(-arcs[a_vertex][c_vertex])

    # V-Rob: deleting q preserves every member of N++(v)=B.
    for b_vertex in sorted(B):
        formula.add(*[
            arcs[a_vertex][b_vertex]
            for a_vertex in sorted(A - {Q})
        ])

    # The high-witness chain and Q-Rob after deleting r.
    formula.add(arcs[Q][r_vertex])
    for endpoint in range(N):
        if endpoint in (Q, r_vertex):
            continue
        alternatives = [
            paths[Q, middle, endpoint]
            for middle in range(N)
            if middle not in (Q, r_vertex, endpoint)
        ]
        formula.add(-second[Q][endpoint], *alternatives)

    # Complete q-status sorting within the uniform blocks, O < I < H.
    sorting_clauses = 0
    for block in (CASES[case]["g1"], CASES[case]["g2"], C):
        for left, right in zip(block, block[1:]):
            formula.add(-arcs[Q][right], arcs[Q][left])
            formula.add(-arcs[right][Q], arcs[Q][left], arcs[left][Q])
            sorting_clauses += 2

    require(sorting_clauses == 24, "wrong number of sorting clauses")
    require(len(formula.names) == 23310, "wrong reconstructed variable count")
    require(len(formula.clauses) == 90451, "wrong reconstructed clause count")
    return formula


def serialize(formula, envelope):
    require(envelope in ("mapped", "bare"), "unknown formula envelope")
    pieces = []
    if envelope == "mapped":
        pieces.extend(
            f"c var {number} {name}\n"
            for name, number in formula.names.items()
        )
    pieces.append(f"p cnf {len(formula.names)} {len(formula.clauses)}\n")
    pieces.extend(" ".join(map(str, clause)) + " 0\n" for clause in formula.clauses)
    return "".join(pieces).encode("ascii")


def hostile_parse(raw, envelope):
    """Parse the strict envelope without trusting DIMACS tolerance."""
    require(type(raw) is bytes, "candidate is not bytes")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise RuntimeError(f"candidate is not ASCII: {error}") from error
    require(text.endswith("\n"), "missing final newline")
    require("\r" not in text and "\t" not in text, "noncanonical whitespace")
    lines = text.splitlines()
    require(lines, "empty candidate")
    names = []
    clauses = []
    header = None
    for line_number, line in enumerate(lines, 1):
        require(line != "", f"blank line {line_number}")
        if line.startswith("c "):
            require(envelope == "mapped", "comment in bare envelope")
            require(header is None, "variable map after header")
            fields = line.split(" ")
            require(len(fields) == 4 and fields[:2] == ["c", "var"],
                    f"malformed map line {line_number}")
            require(fields[2] == str(len(names) + 1),
                    f"nonconsecutive map id at line {line_number}")
            require(fields[3] not in names and fields[3],
                    f"duplicate/empty map name at line {line_number}")
            names.append(fields[3])
            continue
        if line.startswith("p "):
            require(header is None, "duplicate header")
            fields = line.split(" ")
            require(len(fields) == 4 and fields[:2] == ["p", "cnf"],
                    "malformed header")
            require(all(field.isdecimal() and (field == "0" or not field.startswith("0"))
                        for field in fields[2:]), "noncanonical header integer")
            header = (int(fields[2]), int(fields[3]))
            continue
        require(header is not None, f"clause before header at line {line_number}")
        fields = line.split(" ")
        require(all(fields), f"noncanonical spacing at line {line_number}")
        require(fields[-1] == "0" and len(fields) >= 2,
                f"unterminated/empty clause at line {line_number}")
        literals = []
        for field in fields[:-1]:
            digits = field[1:] if field.startswith("-") else field
            require(digits.isdecimal() and digits != "0" and not digits.startswith("0"),
                    f"noncanonical literal at line {line_number}")
            literals.append(int(field))
        clauses.append(tuple(literals))
    require(header is not None, "missing header")
    require(header[1] == len(clauses), "header clause count mismatch")
    if envelope == "mapped":
        require(header[0] == len(names), "header/map variable count mismatch")
    else:
        require(not names, "bare envelope acquired names")
    require(all(abs(literal) <= header[0]
                for clause in clauses for literal in clause),
            "literal exceeds declared variable range")
    return names, clauses, header


def clause_satisfied(clause, assignment):
    return any(assignment[abs(literal)] == (literal > 0) for literal in clause)


def audit_and_and_distance_gates():
    # AND equivalence.
    formula = Formula()
    left = formula.var("left")
    right = formula.var("right")
    output = formula.var("output")
    and_gate(formula, output, left, right)
    for left_value, right_value, output_value in itertools.product((False, True), repeat=3):
        assignment = {left: left_value, right: right_value, output: output_value}
        accepted = all(clause_satisfied(clause, assignment) for clause in formula.clauses)
        require(accepted == (output_value == (left_value and right_value)),
                "AND gate audit failed")

    # Reach is an exact OR of all path gates, including representative widths.
    for width in range(1, 7):
        for path_values in itertools.product((False, True), repeat=width):
            for reach in (False, True):
                clauses = [((not value) or reach) for value in path_values]
                clauses.append((not reach) or any(path_values))
                require(all(clauses) == (reach == any(path_values)),
                        "reach OR audit failed")

    # q_ij iff reach_ij and not a_ij.
    for reach, direct, exact_second in itertools.product((False, True), repeat=3):
        clauses = (
            (not exact_second) or reach,
            (not exact_second) or (not direct),
            exact_second or (not reach) or direct,
        )
        require(all(clauses) == (exact_second == (reach and not direct)),
                "exact-second biconditional audit failed")


def audit_pair_trichotomy():
    # Include the no-digon clause and the three hole-equivalence clauses.
    accepted = set()
    for forward, backward, hole in itertools.product((False, True), repeat=3):
        clauses = (
            (not forward) or (not backward),
            (not hole) or (not forward),
            (not hole) or (not backward),
            hole or forward or backward,
        )
        if all(clauses):
            accepted.add((forward, backward, hole))
    require(accepted == {
        (True, False, False),
        (False, True, False),
        (False, False, True),
    }, "oriented-pair trichotomy audit failed")


def audit_threshold():
    # Exhaust all assignments, including auxiliary variables, through width 4.
    # This catches either a missing implication or a nonfunctional counter.
    for width in range(1, 5):
        formula = Formula()
        inputs = [formula.var(f"x_{index}") for index in range(width)]
        outputs = threshold(formula, inputs, "audit")
        auxiliaries = [number for name, number in formula.names.items()
                       if name.startswith("cnt_audit_")]
        for bits in itertools.product((False, True), repeat=width):
            accepted_assignments = 0
            accepted_outputs = None
            for aux_bits in itertools.product((False, True), repeat=len(auxiliaries)):
                assignment = {inputs[index]: bits[index] for index in range(width)}
                assignment.update(zip(auxiliaries, aux_bits))
                if all(clause_satisfied(clause, assignment) for clause in formula.clauses):
                    accepted_assignments += 1
                    accepted_outputs = tuple(assignment[output] for output in outputs)
            require(accepted_assignments == 1, "counter is not functional")
            require(accepted_outputs == tuple(sum(bits) >= target
                                               for target in range(1, width + 1)),
                    "counter output audit failed")


def audit_mu2_link():
    # Evaluate the actual linkage clauses for every cardinality pair at width 17.
    formula = Formula()
    outs = [formula.var(f"out_{target}") for target in range(1, N)]
    seconds = [formula.var(f"sec_{target}") for target in range(1, N)]
    mu2 = formula.var("mu2")
    add_mu2_link(formula, outs, seconds, mu2)
    for out_degree in range(2, N):
        for deficit in (1, 2):
            second_degree = out_degree - deficit
            if second_degree < 0:
                continue
            for mu2_value in (False, True):
                assignment = {mu2: mu2_value}
                assignment.update({var: out_degree >= target
                                   for target, var in enumerate(outs, 1)})
                assignment.update({var: second_degree >= target
                                   for target, var in enumerate(seconds, 1)})
                accepted = all(clause_satisfied(clause, assignment)
                               for clause in formula.clauses)
                require(accepted == (mu2_value == (deficit == 2)),
                        "mu2 linkage audit failed")


def exact_second(vertices, arcs, source):
    first = {target for target in vertices if (source, target) in arcs}
    return {
        target
        for middle in first
        for target in vertices
        if (middle, target) in arcs and target != source and target not in first
    }


def audit_q_robustness():
    # Exhaust all oriented graphs on four vertices with q->r.  The emitted
    # preservation predicate must be equivalent to exact N++ equality after r
    # is deleted, on surviving vertices.
    vertices = tuple(range(4))
    q_vertex, r_vertex = 0, 1
    pairs = tuple((i, j) for i in vertices for j in vertices if i < j)
    for states in itertools.product((0, 1, 2), repeat=len(pairs)):
        arcs = set()
        for (left, right), state in zip(pairs, states):
            if state == 0:
                arcs.add((left, right))
            elif state == 1:
                arcs.add((right, left))
        if (q_vertex, r_vertex) not in arcs:
            continue
        old = exact_second(vertices, arcs, q_vertex)
        surviving = tuple(vertex for vertex in vertices if vertex != r_vertex)
        reduced = {(left, right) for left, right in arcs
                   if left != r_vertex and right != r_vertex}
        new = exact_second(surviving, reduced, q_vertex)
        equality = old - {r_vertex} == new
        clause_predicate = all(
            any((q_vertex, middle) in arcs and (middle, endpoint) in arcs
                for middle in vertices
                if middle not in (q_vertex, r_vertex, endpoint))
            for endpoint in old
            if endpoint != r_vertex
        )
        require(equality == clause_predicate, "Q-Rob semantic audit failed")


def audit_semantics():
    audit_and_and_distance_gates()
    audit_pair_trichotomy()
    audit_threshold()
    audit_mu2_link()
    audit_q_robustness()


def check_candidate(path, case, envelope):
    audit_semantics()
    expected = reconstruct(case)
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise RuntimeError(f"candidate read failed: {error}") from error
    names, clauses, header = hostile_parse(raw, envelope)
    expected_names = list(expected.names)
    if envelope == "mapped":
        require(names == expected_names, "variable map differs from reconstruction")
    require(header == (len(expected.names), len(expected.clauses)),
            "formula dimensions differ from reconstruction")
    require(clauses == expected.clauses, "clause stream differs from reconstruction")
    require(raw == serialize(expected, envelope), "noncanonical formula bytes")
    digest = hashlib.sha256(raw).hexdigest()
    print(f"PASS independent family-H CNF case={case} envelope={envelope} "
          f"vars={header[0]} clauses={header[1]} sha256={digest}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--case", required=True, choices=tuple(CASES))
    parser.add_argument("--envelope", required=True, choices=("mapped", "bare"))
    arguments = parser.parse_args()
    check_candidate(arguments.cnf, arguments.case, arguments.envelope)


if __name__ == "__main__":
    main()
