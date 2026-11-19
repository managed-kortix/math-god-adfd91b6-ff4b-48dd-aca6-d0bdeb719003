#!/usr/bin/env python3
"""Full regeneration and hostile tests for the grouped residual campaign."""

import hashlib
import json
import tempfile
from pathlib import Path

import check_m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual as checker
import m6_b7_l6_hard_witness_positive_gain_coordinate_grouped_residual as producer


def reject(call, label):
    try:
        call()
    except (RuntimeError, ValueError, UnicodeError, IndexError):
        return
    raise RuntimeError(f"hostile grouped residual mutation accepted: {label}")


checker_groups, manifest = checker.check_manifest()
groups = producer.load_groups()
if [(group[0], producer.residual.key(group[1]), tuple(entry[0] for entry in group[2])) for group in groups] != [
        (group[0], checker.source.producer.key(group[1]), tuple(entry[0] for entry in group[2]))
        for group in checker_groups]:
    raise RuntimeError("producer and independent grouped scopes differ")
expected = checker.load_hashes()
seen_widths = set()
with tempfile.TemporaryDirectory(prefix="m6-grouped-residual-test-", dir=producer.HERE.parent) as directory:
    directory = Path(directory)
    path = directory / "leaf.cnf"
    samples = {}
    for ordinal, group in enumerate(groups):
        cnf, selectors = producer.build_group(group)
        producer.write_group(path, group, cnf, selectors, manifest)
        if (path.stat().st_size, hashlib.sha256(path.read_bytes()).hexdigest()) != expected[ordinal]:
            raise RuntimeError(f"regenerated grouped CNF differs: {ordinal:03d}")
        samples.setdefault(len(selectors), path.read_bytes())
        if len(selectors) not in seen_widths:
            checker.check(path)
            seen_widths.add(len(selectors))

    def mutate(label, width, predicate, replace):
        lines = samples[width].decode("ascii").splitlines()
        index = next(i for i, line in enumerate(lines) if predicate(line))
        lines[index] = replace(lines[index])
        bad = directory / f"bad-{label}.cnf"
        bad.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
        reject(lambda: checker.check(bad), label)

    mutate("alo-omission", 4, lambda line: line.split()[-1:] == ["0"] and len(line.split()) == 5,
           lambda line: " ".join(line.split()[:-2] + ["0"]))
    mutate("amo-polarity", 4, lambda line: len(line.split()) == 3 and line.startswith("-23617 -23618 "),
           lambda line: line[1:])
    mutate("projection-polarity", 4,
           lambda line: len(line.split()) == 3 and line.startswith("-23617 ") and not line.startswith("-23617 -23618 "),
           lambda line: line.replace("-23617 ", "23617 ", 1))
    mutate("selector-name", 4, lambda line: line.startswith("c var 23617 grouped_residual_"),
           lambda line: line + "_hostile")
    mutate("bound-ledger-hash", 4, lambda line: line.startswith("c singleton-certificate-ledger-sha256 "),
           lambda line: line.rsplit(" ", 1)[0] + " " + "0" * 64)

    ledger = checker.CERTIFICATE_LEDGER.read_bytes()
    bad_ledger = directory / "bad-certificates.tsv"
    bad_ledger.write_bytes(b"\n".join(ledger.splitlines()[:-1]) + b"\n")
    reject(lambda: checker.certificate_scope(bad_ledger), "certificate-scope")

    source_group = groups[0]
    source_cnf, old_selectors = producer.residual.build_leaf(source_group[1])
    old_parents = source_group[1][1][4][2][6]
    alo = next(i for i, clause in enumerate(source_cnf.clauses)
               if tuple(clause) == tuple(old_selectors))
    source_cnf.clauses[alo + 1], source_cnf.clauses[alo + 2] = \
        source_cnf.clauses[alo + 2], source_cnf.clauses[alo + 1]
    reject(lambda: producer.strip_old_selector_layer(source_cnf, old_selectors, old_parents),
           "old-selector-guard-order")

    checker.check_scout()
    scout = json.loads(checker.SCOUT.read_text(encoding="ascii"))
    scout["rows"][0]["status"] = "SAT"
    bad_scout = directory / "bad-scout.json"
    bad_scout.write_text(json.dumps(scout, sort_keys=True, indent=2) + "\n", encoding="ascii", newline="\n")
    reject(lambda: checker.check_scout(bad_scout), "scout-status")

print("PASS grouped residual: 153 CNFs, 1255 selectors, widths 1x1/3x2/2x3/38x4/109x10, hostile mutations")
