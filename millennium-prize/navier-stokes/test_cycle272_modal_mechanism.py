import unittest

from analyze_cycle272_modal_mechanism import EXAMPLE, LABELS, exact_decomposition


class Cycle272ModalMechanismTest(unittest.TestCase):
    def decomposition(self, deleted=()):
        modes = [
            mode for label, mode in zip(LABELS, EXAMPLE["modes"])
            if label not in deleted
        ]
        return exact_decomposition(modes)

    def test_unweighted_cubic_integral_cancels_exactly(self):
        orders, _ = self.decomposition()
        self.assertEqual(orders[0], 0)
        self.assertGreater(orders[1], 0)
        self.assertGreater(sum(orders), 0)

    def test_shear_occurs_in_nonzero_signed_pressure_seeds(self):
        _, seeds = self.decomposition()
        shear_total = sum(
            sum(values) for members, values in seeds.items()
            if any(label in {"Sx", "Sy"} for label, _ in members)
        )
        self.assertNotEqual(shear_total, 0)

    def test_A_and_C_reverse_the_exact_polynomial_sign(self):
        for label in ("A", "C"):
            with self.subTest(label=label):
                orders, _ = self.decomposition({label})
                self.assertLess(sum(orders), 0)


if __name__ == "__main__":
    unittest.main()
