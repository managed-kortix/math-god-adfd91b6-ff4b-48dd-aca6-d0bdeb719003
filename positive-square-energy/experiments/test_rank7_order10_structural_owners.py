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


if __name__ == "__main__":
    unittest.main()
