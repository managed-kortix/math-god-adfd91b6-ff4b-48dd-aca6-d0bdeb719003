#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


PATH = Path(__file__).with_name("rank7_order10_structural_owners.py")


def load_module():
    spec = importlib.util.spec_from_file_location("rank7_order10_owner_test", PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StructuralOwnerTest(unittest.TestCase):
    def test_exact_owner_precedence_is_delegated(self):
        module = load_module()
        core = module.load_core()
        calls = []

        class Owner:
            @staticmethod
            def recognize_row(atom, edges, row):
                calls.append((atom, edges, row))
                return "signed-imbalance-psd", [1, 2, 3]

        result = core.recognize_row(Owner(), "atom", ((0, 1, 1),), (1,))
        self.assertEqual(result, ("signed-imbalance-psd", [1, 2, 3]))
        self.assertEqual(calls, [("atom", ((0, 1, 1),), (1,))])

    def test_order_ten_scope(self):
        core = load_module().load_core()
        self.assertEqual((core.ORDER, core.PATH_COUNT, core.TARGETS_PER_RESIDUAL,
                          core.KERNEL_TOTAL), (10, 16, 17, 3396))
        self.assertEqual(core.LANES[-1], "cubic-cycle-space-candidate")

    def test_census_header_validation_is_fail_closed(self):
        module = load_module()
        core = module.load_core()
        kernel = {
            "automorphisms": 2,
            "coarse_certified_orbits": 2,
            "coarse_residual_orbits": 1,
            "coarse_residual_physical_rows": 2,
            "edges": [[0, 1, 1]],
            "global_kernel": 100,
            "order_kernel": 1,
            "parity_orbits": 3,
            "physical_rows": 4,
        }
        header = {
            "schema": core.CHUNK_SCHEMA,
            "full_theorem": False,
            "rank": 7,
            "order": 10,
            "budget": [6, 1],
            "path_count": 16,
            "frontiers_per_residual": 17,
            "source_sha256": module.SOURCE_SHA256,
            "kernel_range": [0, 1],
            "kernel_total": 1,
            "kernels": [kernel],
            "physical_row_total": 4,
            "parity_orbit_total": 3,
            "coarse_certified_total": 2,
            "coarse_residual_total": 1,
            "coarse_residual_physical_total": 2,
            "frontier_target_total": 17,
        }
        module.validate_census_header(core, header, Path("chunk.json.xz"))
        header["frontier_target_total"] = 16
        with self.assertRaisesRegex(RuntimeError, "frontier total mismatch"):
            module.validate_census_header(core, header, Path("chunk.json.xz"))


if __name__ == "__main__":
    unittest.main()
