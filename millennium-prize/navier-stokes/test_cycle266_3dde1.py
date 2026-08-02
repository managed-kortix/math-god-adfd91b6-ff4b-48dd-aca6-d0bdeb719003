import hashlib
import json
import pathlib
import sys
import unittest
from fractions import Fraction


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from cycle266_3dde1 import canonical_bytes, euler_rhs, generate_family, kida_pelz


class Cycle266ThreeDDE1Tests(unittest.TestCase):
    def test_exact_family_count_order_and_digest(self):
        family = generate_family()
        self.assertEqual(len(family["profiles"]), 132)
        keys = [
            (row["a"], row["b"], tuple(row["phase_pi_over_2"]))
            for row in family["profiles"]
        ]
        self.assertEqual(len(keys), len(set(keys)))
        raw = (ROOT / "cycle266-3dde1-exact-family.json").read_bytes()
        self.assertEqual(raw, canonical_bytes(family))
        manifest = json.loads((ROOT / "cycle266-3dde1-manifest.json").read_text())
        self.assertEqual(hashlib.sha256(raw).hexdigest(), manifest["family"]["sha256"])

    def test_base_and_tangent_are_exactly_divergence_free_and_real(self):
        for field in (kida_pelz(), euler_rhs(kida_pelz())):
            for k, vector in field.items():
                divergence = tuple(
                    sum(Fraction(k[j]) * vector[j][part] for j in range(3))
                    for part in range(2)
                )
                self.assertEqual(divergence, (Fraction(0), Fraction(0)))
                opposite = field[tuple(-x for x in k)]
                self.assertEqual(opposite, tuple((z[0], -z[1]) for z in vector))

    def test_manifest_freezes_section_seven_constraints(self):
        manifest = json.loads((ROOT / "cycle266-3dde1-manifest.json").read_text())
        for name, digest in manifest["source_digests"].items():
            source = "cycle266_3dde1.py" if name == "generator_sha256" else \
                "cycle-265-genuine-3d-euler-pivot-architecture.md"
            self.assertEqual(hashlib.sha256((ROOT / source).read_bytes()).hexdigest(), digest)
        self.assertGreaterEqual(manifest["promotion"]["threshold"], 2.20)
        self.assertEqual(manifest["integrator"]["method"], "implicit_midpoint")
        self.assertEqual(manifest["family"]["profile_count"], 132)
        self.assertEqual(len(manifest["levels"]), 2)
        self.assertEqual(manifest["stop_rules"]["early_global_stop"],
                         "none except resource preflight failure or fail-closed numerical error")


if __name__ == "__main__":
    unittest.main()
