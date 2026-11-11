#!/usr/bin/env python3
"""Exhaustive compact positive-gain, partition, binding, and hostile tests."""

import gc
import hashlib
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain as checker
import m6_b7_l6_hard_witness_positive_gain as producer

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "m6-b7-l6-hard-witness-positive-gain.tsv"


def reject(action, label):
    try:
        action()
    except (RuntimeError, ValueError, UnicodeError, IndexError):
        return
    raise RuntimeError(f"hostile mutation accepted: {label}")


produced = producer.load_leaves()
checked = checker.derive_leaves()
projection = lambda leaf: (leaf[0], leaf[1], leaf[3], leaf[4], [(a, c) for a, c, _ in leaf[2][6]])
if list(map(projection, produced)) != list(map(projection, checked)):
    raise RuntimeError("producer and independent checker source frontiers differ")
manifest = producer.manifest_payload(produced)
if manifest != checker.manifest_payload(checked) or manifest != MANIFEST.read_bytes():
    raise RuntimeError("producer/checker/frozen positive-gain manifests differ")
widths = [len(producer.gain_paths(leaf)) for leaf in produced]
if set(widths) != {16, 32} or widths.count(16) != 12 or widths.count(32) != 105:
    raise RuntimeError("exact 16/32 positive path census changed")
checker.check_partition()
print("PASS bound 117 sources, 1066 incidences, and one exact 16/32 positive ALO per source")

with tempfile.TemporaryDirectory(prefix="m6-witness-positive-gain-test-", dir=HERE.parent) as directory:
    directory = Path(directory)
    expected, generated, retained = checker.load_hashes(manifest), {}, None
    for ordinal, leaf in enumerate(produced):
        cnf, selectors = producer.build_leaf(leaf)
        path = directory / "leaf.cnf"
        producer.write_leaf(path, ordinal, leaf, cnf, selectors, manifest)
        generated[leaf[0]] = hashlib.sha256(path.read_bytes()).hexdigest()
        checker.check(path)
        if ordinal == 0:
            retained = path.read_bytes()
        path.unlink()
        del cnf, selectors
        gc.collect()
    if generated != expected:
        raise RuntimeError("generated positive-gain CNFs differ from complete hash ledger")
    print("PASS emitted, independently reconstructed, and hashed all 117 positive-gain CNFs")

    def mutate_cnf(label, predicate, replacement):
        lines = retained.decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replacement(lines[index])
        path = directory / f"bad-{label}.cnf"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(path), label)

    def alo(line):
        literals = line.split()[:-1]
        return len(literals) == 16 and all(not literal.startswith("-") for literal in literals)

    mutate_cnf("polarity", alo, lambda line: "-" + line)
    mutate_cnf("substitution", alo, lambda line: " ".join([line.split()[1], *line.split()[1:]]))
    mutate_cnf("omission", alo, lambda line: " ".join(line.split()[1:]))
    mutate_cnf("duplication", alo, lambda line: line.split()[0] + " " + line)
    mutate_cnf("source-binding", lambda line: line.startswith("c no-gain-manifest-sha256 "),
               lambda line: line[:-1] + ("0" if line[-1] != "0" else "1"))
    mutate_cnf("witness-binding", lambda line: line.startswith("c ordered-witnesses "),
               lambda _: "c ordered-witnesses 15")
    print("PASS hostile polarity/substitution/omission/duplication/source-binding/witness-binding CNF mutations")

    names, _, common, _ = checker.reconstruct_common(checked[0])
    positive = tuple(names.index(name) + 1 for name in checker.gain_names(checked[0]))
    negative = [(-literal,) for literal in positive]

    def mutate_complement(label, change):
        units = list(negative)
        change(units)
        reject(lambda: checker.validate_complement(checked[0], names, positive, units),
               f"negative-unit-{label}")

    mutate_complement("polarity", lambda units: units.__setitem__(0, (-units[0][0],)))
    mutate_complement("substitution", lambda units: units.__setitem__(0, units[1]))
    mutate_complement("omission", lambda units: units.pop(0))
    mutate_complement("duplication", lambda units: units.insert(1, units[0]))
    print("PASS hostile negative-unit polarity/substitution/omission/duplication mutations")

    no_gain_lines = checker.NO_GAIN_MANIFEST.read_text(encoding="ascii").splitlines()
    marker = next(i for i, line in enumerate(no_gain_lines) if line.startswith("columns\t"))

    def mutate_partition(label, change):
        lines = list(no_gain_lines)
        change(lines, marker)
        path = directory / f"bad-partition-{label}.tsv"
        path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check_partition(path), label)

    mutate_partition("omission", lambda lines, index: lines.pop(index + 1))
    mutate_partition("duplication", lambda lines, index: lines.insert(index + 2, lines[index + 1]))
    mutate_partition("polarity-count", lambda lines, index: lines.__setitem__(index + 1, lines[index + 1].replace("\t16\t", "\t15\t", 1)))
    mutate_partition("substitution", lambda lines, index: lines.__setitem__(index + 1, lines[index + 1].replace("\t13\t16\t", "\t12\t16\t", 1)))
    mutate_partition("source-binding", lambda lines, index: lines.__setitem__(index + 1, lines[index + 1].replace("o00-w00", "o00-w99")))
    print("PASS hostile partition polarity/substitution/omission/duplication/source-binding mutations")

print("PASS m6 B7-l6 hard witness compact positive-gain tests")
