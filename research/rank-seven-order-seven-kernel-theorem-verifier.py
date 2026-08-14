#!/usr/bin/env python3
"""Fail-closed exact verifier for the rank-seven order-seven kernel theorem."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDITOR = ROOT / "positive-square-energy/experiments/rank7_order7_pack_auditor.py"
MANIFEST = ROOT / "positive-square-energy/experiments/rank7_order7_search_manifest.json"
PACKET = (ROOT / "positive-square-energy/heptacyclic-general"
          / "rank-seven-order-seven-k2763-direct-frontiers.md")
K4_THEOREM = (ROOT / "positive-square-energy/tricyclic-general"
              / "k4-all-odd-dnn-cover.md")
K4_VERIFIER = ROOT / "positive-square-energy/experiments/k4_all_odd_exact_verify.py"
EXPECTED_SHA256 = {
    "auditor": "a4b93e385886b687718160e2f45fca250602f8048484da0e7c710d80f80c431b",
    "manifest": "7c1d57be8cdf1f859272b100f25f9dfcb598d944efd40b774a155e52bb651b5a",
    "packet": "0bc8e36f5793983bf338503eea67244bb8ad7429a9a6e19f72f50ecc91ae9515",
    "k4_theorem": "5c2b9b2b981807a82451edb0a6e26a3d960147801798b4b4cbccdd79ffdc8ec4",
    "k4_verifier": "2c5f943534a20e07655be2af75235b27fcfec05eb6e9750338a9fdc2b7615e42",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_auditor():
    spec = importlib.util.spec_from_file_location("rank7_order7_theorem_auditor", AUDITOR)
    require(spec is not None and spec.loader is not None, "cannot load order-seven auditor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit():
    paths = {"auditor": AUDITOR, "manifest": MANIFEST, "packet": PACKET,
             "k4_theorem": K4_THEOREM, "k4_verifier": K4_VERIFIER}
    require(all(path.is_file() for path in paths.values()), "order-seven dependency missing")
    require({name: digest(path) for name, path in paths.items()} == EXPECTED_SHA256,
            "order-seven dependency digest changed")

    packet = PACKET.read_text(encoding="ascii")
    required = (
        "A={03,05,06,35,36,56},   B={12,14,16,24,26,46}.",
        "sigma(U)>=1",
        "sigma(G)>=1-1=0",
        "every same-parity descendant of frontier `10`",
        "arbitrary rooted-tree attachments",
        "no spectral subdivision monotonicity is",
    )
    require(all(fragment in packet for fragment in required), "K2763 packet contract changed")

    k4 = subprocess.run([sys.executable, str(K4_VERIFIER)], check=False,
                        capture_output=True, text=True)
    require(k4.returncode == 0 and k4.stderr == "" and
            "all-odd K4 exact audit passed" in k4.stdout,
            "all-odd K4 dependency failed")

    auditor = load_auditor()
    report, complete = auditor.audit(MANIFEST, exact=True)
    require(complete and report["status"] == "complete", "finite replay is incomplete")
    require(report["theorem_gate_eligible"] is True and
            report["theorem_gate_blocker"] is None,
            "order-seven theorem gate is closed")
    require(report["covered_target_total"] == 573496 and
            report["exact_certified_target_total"] == 573496 and
            report["uncertified_target_total"] == 0,
            "finite target partition changed")
    owners = report["direct_spectral_owners"]
    require(len(owners) == 2 and all(row["all_length_rooted_tree_lift"] is True and
            row["packet"] ==
            "two-actual-K4-one-sum-plus-open-45-path-with-rational-routing"
            for row in owners), "K2763 all-length owners changed")
    return {
        "schema": "rank-seven-order-seven-kernel-theorem-v1",
        "rank": 7,
        "kernel_order": 7,
        "kernel_count": 2270,
        "finite_target_total": 573496,
        "theorem_gate_eligible": True,
        "length_scope": "arbitrary positive simple-subdivision lengths",
        "attachments": "arbitrary finite rooted trees at branch or subdivision vertices",
        "conclusion": "s+(G)>=|V(G)|",
        "ownership_stream_sha256": report["ownership_stream_sha256"],
    }


def main():
    try:
        report = audit()
    except (OSError, RuntimeError, TypeError, ValueError, UnicodeError) as error:
        sys.stderr.write(f"rank-seven order-seven kernel theorem: FAIL CLOSED: {error}\n")
        return 1
    if "--print-manifest" in sys.argv:
        sys.stdout.write(json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.write("rank-seven order-seven kernel theorem: exact audit passed\n"
                     "targets=573496 theorem_gate=eligible all_lengths=true rooted_trees=true\n"
                     "conclusion=s+(G)>=|V(G)| for rank-seven kernel order seven only\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
