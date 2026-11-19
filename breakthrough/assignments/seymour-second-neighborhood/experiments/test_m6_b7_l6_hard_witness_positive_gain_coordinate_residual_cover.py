#!/usr/bin/env python3
"""Tests for the minimal sound residual coordinate cover."""

import hashlib
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover as checker
import m6_b7_l6_hard_witness_positive_gain_coordinate_residual_cover as producer


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError, IndexError):
        return
    raise RuntimeError(f"hostile residual-cover mutation accepted: {label}")


cover, manifest = checker.check_coverage()
checker.check_scout()
unresolved, produced = producer.load_cover()
if [(producer.key(item), item[2], item[3]) for item in produced] != [
        (producer.key(item), item[2], item[3]) for item in cover]:
    raise RuntimeError("producer and independent residual covers differ")
restored = {producer.key(item) for item in produced} & {
    "o03-w01-c16", "o03-w04-c16", "o17-w01-c16", "o17-w04-c16",
    "o33-w01-c16", "o33-w04-c16", "o41-w03-c17", "o41-w04-c17",
}
if len(restored) != 8:
    raise RuntimeError("eight uncertified coordinate-certificate siblings were not restored")

children = checker.frozen.derive_children()
grouped = {}
for ordinal, child in enumerate(children):
    grouped.setdefault(child[0], []).append((ordinal, child, *checker.independently_reduce(child)))
certified = set(checker.frozen.SCOUT_UNSAT_ORDINALS)
certificate_source = grouped[children[next(iter(certified))][0]]
certificate_residual = [item for item in certificate_source if item[0] not in certified]
reject(lambda: checker.prove_source_disjunction(certificate_source, [], certified),
       "coordinate-certificate-closes-source")
reject(lambda: checker.prove_source_disjunction(certificate_source, certificate_source, certified),
       "certified-child-retained")
two_child_source = next(items for items in grouped.values()
                        if len(items) == 2 and all(item[2] == "b-reduced" for item in items))
reject(lambda: checker.prove_source_disjunction(two_child_source, two_child_source[:1], certified),
       "uncertified-sibling-omitted")
checker.prove_source_disjunction(certificate_source, certificate_residual, certified)
with tempfile.TemporaryDirectory(prefix="m6-coordinate-residual-scout-test-", dir=producer.HERE.parent) as directory:
    bad_scout = Path(directory) / "bad-scout.json"
    scout = checker.SCOUT_PATH.read_text(encoding="ascii")
    bad_scout.write_text(scout.replace('"status": "TIMEOUT"', '"status": "UNSAT"', 1),
                         encoding="ascii", newline="\n")
    reject(lambda: checker.check_scout(bad_scout), "scout-status")

with tempfile.TemporaryDirectory(prefix="m6-coordinate-residual-cover-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    expected = checker.load_hashes(manifest)
    generated = {}
    samples = {}
    for ordinal, item in enumerate(produced):
        path = directory / "leaf.cnf"
        cnf, selectors = producer.build_leaf(item)
        producer.write_leaf(path, ordinal, item, cnf, selectors, manifest)
        generated[producer.key(item)] = hashlib.sha256(path.read_bytes()).hexdigest()
        checker.check(path)
        samples.setdefault(item[2], path.read_bytes())
        path.unlink()
    if generated != expected:
        raise RuntimeError("generated residual-cover CNFs differ from hash ledger")

    def mutate(disposition, label, predicate, replacement):
        lines = samples[disposition].decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        path = directory / f"bad-{label}.cnf"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(path), label)

    mutate("structural", "disposition", lambda line: line.startswith("c disposition "),
           lambda _: "c disposition b-reduced")
    mutate("b-reduced", "midpoints", lambda line: line.startswith("c alo-midpoints "),
           lambda _: "c alo-midpoints 9")
    mutate("b-reduced", "alo-polarity",
           lambda line: line.endswith(" 0") and not line.startswith(("c ", "p ")) and
           len(line.split()) in range(3, 8) and all(not value.startswith("-") for value in line.split()[:-1]),
           lambda line: "-" + line)

print("PASS residual-cover tests: 117-source coverage, all 153 CNFs, eight restored siblings, and hostile mutations")
