#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from cycle43_divisor_admission_multiprobe import (
    AFFINE,
    CompensatedBlock,
    certified_sign,
    first_certifying_prefix,
    singleton_scan,
)


class Cycle43DivisorAdmissionMultiprobeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192
        cls.blocks = {
            endpoints: CompensatedBlock(*endpoints, bits=192)
            for endpoints in ((39, 42), (95, 103), (219, 231))
        }

    def test_exact_residual_matches_endpoint_complete_energies(self):
        # Separate endpoint contraction (sharing the base Gram evaluator):
        # R_theta=P_a-P_b-2 theta sum w_n P_n.
        from certify_complete_gram import complete_energies

        energies = complete_energies(231, 192)
        for (start, stop), block in self.blocks.items():
            weighted = sum(
                (block.weight[n] * energies[n] for n in range(start, stop)),
                arb(0),
            )
            expected = (
                energies[start] - energies[stop]
                - 2 * block.theta * weighted
            )
            self.assertTrue(block.residual.overlaps(expected))
            self.assertGreater(block.residual, 0)

    def test_certified_sign_rejects_nonfinite_values(self):
        for value in (arb("inf"), arb("-inf"), arb("+/- inf")):
            with self.assertRaises(RuntimeError):
                certified_sign(value)

    def test_certificate_consumes_one_shot_family_once(self):
        block = self.blocks[(39, 42)]
        expected = block.certificate((AFFINE,))
        actual = block.certificate(iter((AFFINE,)))
        self.assertEqual(actual["family"], (AFFINE,))
        self.assertEqual(actual["rank"], 1)
        self.assertTrue(actual["projection"].overlaps(expected["projection"]))
        self.assertEqual(actual["verdict"], expected["verdict"])

    def test_probe_gram_and_correlation_match_direct_column_expansion(self):
        block = self.blocks[(39, 42)]
        for a, b in ((AFFINE, AFFINE), (AFFINE, 39), (3, 39), (39, 41)):
            direct = sum(
                (
                    block.scale_factor(n)
                    * block.probe_coefficient(n, a)
                    * block.probe_coefficient(n, b)
                    * block.base(a, b)
                    for n in block.scales
                ),
                arb(0),
            )
            self.assertTrue(block.probe_gram(a, b).overlaps(direct))

        for label in (AFFINE, 3, 39):
            direct = arb(0)
            for n in block.scales:
                inner = sum(
                    (
                        block.x_coefficient(n, other)
                        * block.base(other, label)
                        for other in block.labels
                    ),
                    arb(0),
                )
                direct += (
                    block.scale_factor(n)
                    * block.probe_coefficient(n, label)
                    * inner
                )
            self.assertTrue(block.correlation(label).overlaps(direct))

    def test_projection_is_monotone_and_bounded_by_positive_energy(self):
        families = ((AFFINE,), (AFFINE, 219), (AFFINE, 219, 221))
        block = self.blocks[(219, 231)]
        previous = arb(0)
        for family in families:
            projection, determinant = block.projection(family)
            self.assertGreater(determinant, 0)
            self.assertGreaterEqual(projection, previous)
            self.assertGreaterEqual(block.positive_energy, projection)
            previous = projection

    def test_minimum_certified_ranks_in_full_probe_pool(self):
        expected = {
            (39, 42): (AFFINE,),
            (95, 103): (AFFINE,),
            (219, 231): (AFFINE, 215),
        }
        for endpoints, family in expected.items():
            block = self.blocks[endpoints]
            selected, trace = block.greedy_family()
            self.assertEqual(selected, family)
            self.assertEqual(trace[-1]["verdict"], "PASS")
            if len(family) == 2:
                self.assertEqual(block.certificate(family[:1])["verdict"], "FAIL")

    def test_affine_free_small_families(self):
        self.assertEqual(
            self.blocks[(39, 42)].certificate((3,))["verdict"], "PASS"
        )
        self.assertEqual(
            self.blocks[(95, 103)].certificate((3,))["verdict"], "PASS"
        )
        block = self.blocks[(219, 231)]
        self.assertEqual(block.certificate((3,))["verdict"], "FAIL")
        self.assertEqual(block.certificate((3, 215))["verdict"], "PASS")

    def test_exhaustive_atomic_singleton_scan(self):
        expected_passing = {
            (39, 42): 14,  # affine plus 13 divisor columns
            (95, 103): 7,  # affine plus 6 divisor columns
            (219, 231): 0,
        }
        for endpoints, passing_count in expected_passing.items():
            block = self.blocks[endpoints]
            scan = singleton_scan(block)
            self.assertEqual(scan["pool_size"], len(block.labels))
            self.assertEqual(scan["passing_count"], passing_count)
        self.assertEqual(
            singleton_scan(self.blocks[(219, 231)])["best_midpoint_label"],
            AFFINE,
        )

    def test_current_block_admissions_alone_fail_even_at_full_rank(self):
        for (start, stop), block in self.blocks.items():
            family = tuple(
                d for d in block.labels if start <= d < stop
            )
            certificate = block.certificate(family)
            self.assertEqual(certificate["rank"], sum(
                1 for d in range(start, stop) if block.mu[d]
            ))
            self.assertEqual(certificate["verdict"], "FAIL")

    def test_first_squarefree_prefixes(self):
        expected = {
            (39, 42): (1, 1),
            (95, 103): (1, 1),
            (219, 231): (19, 13),
        }
        for endpoints, (cutoff_expected, rank_expected) in expected.items():
            cutoff, certificate = first_certifying_prefix(self.blocks[endpoints])
            self.assertEqual(cutoff, cutoff_expected)
            self.assertEqual(certificate["rank"], rank_expected)
            self.assertEqual(certificate["verdict"], "PASS")

    def test_late_affine_pairs_show_current_admission_boundary(self):
        block = self.blocks[(219, 231)]
        self.assertEqual(block.certificate((AFFINE, 227))["verdict"], "PASS")
        self.assertEqual(block.certificate((AFFINE, 229))["verdict"], "FAIL")


if __name__ == "__main__":
    unittest.main()
