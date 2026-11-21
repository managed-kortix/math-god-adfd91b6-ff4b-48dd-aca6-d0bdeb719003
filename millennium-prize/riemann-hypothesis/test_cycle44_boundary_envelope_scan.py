#!/usr/bin/env python3

import unittest

from flint import arb, ctx

from cycle43_divisor_admission_multiprobe import CompensatedBlock
from cycle44_boundary_envelope_scan import (
    envelope_certificate,
    envelope_family,
    first_passing_width,
    natural_width,
    set_fixed_theta,
)


class Cycle44BoundaryEnvelopeScanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ctx.prec = 192

    def block(self, start):
        block = CompensatedBlock(start, 2 * start, bits=192)
        set_fixed_theta(block, arb(2) / 5)
        return block

    def test_fixed_theta_reset_matches_fresh_direct_recomputation(self):
        block = CompensatedBlock(32, 64, bits=192)
        # Populate every theta-dependent cache before changing theta.
        _ = block.probe_gram(33, 35)
        _ = block.correlation(33)
        _ = block.positive_energy
        _ = block.negative_budget
        set_fixed_theta(block, arb(2) / 5)

        self.assertTrue(block.theta.overlaps(arb(2) / 5))
        self.assertFalse(block._probe_gram)
        self.assertFalse(block._correlation)
        self.assertIsNone(block._positive_energy)
        self.assertIsNone(block._negative_budget)
        for n in block.scales:
            ratio = block.logs[n] / block.logs[n + 1]
            expected_a = 1 + ratio - arb(4) / 5
            expected_eta = (arb(1) / 5) / expected_a
            expected_b = arb(4) / 5 + (arb(1) / 25) / expected_a
            self.assertTrue(block.positive_weight[n].overlaps(expected_a))
            self.assertTrue(block.eta[n].overlaps(expected_eta))
            self.assertTrue(block.negative_factor[n].overlaps(expected_b))

    def test_envelope_family_is_exact_and_nested(self):
        block = self.block(32)
        previous = set(envelope_family(block, 0))
        self.assertEqual(
            previous,
            {q for q in block.labels if q and 32 <= q < 64},
        )
        for width in range(1, 32):
            current = set(envelope_family(block, width))
            self.assertTrue(previous <= current)
            self.assertEqual(
                current,
                {q for q in block.labels if q and 32 - width <= q < 64},
            )
            previous = current
        with self.assertRaises(ValueError):
            envelope_family(block, -1)
        with self.assertRaises(ValueError):
            envelope_family(block, 32)

    def test_projection_is_monotone_on_nested_envelopes(self):
        block = self.block(32)
        previous = arb(0)
        previous_family = ()
        for width in range(32):
            certificate = envelope_certificate(block, width)
            projection = certificate["projection"]
            # Adding a nonsquarefree boundary integer leaves the span unchanged.
            if certificate["family"] == previous_family:
                self.assertTrue(projection.overlaps(previous))
            else:
                self.assertGreater(projection, previous)
            self.assertGreater(block.positive_energy, projection)
            previous = projection
            previous_family = certificate["family"]

    def test_first_passing_widths_at_small_certified_starts(self):
        expected = {32: 0, 64: 0, 128: 19}
        for start, wanted in expected.items():
            block = self.block(start)
            width, cache = first_passing_width(block)
            self.assertEqual(width, wanted)
            self.assertEqual(cache[width]["verdict"], "PASS")
            if width:
                self.assertEqual(cache[width - 1]["verdict"], "FAIL")

    def test_natural_width_uses_certified_integer_ceiling(self):
        self.assertEqual(
            [natural_width(start) for start in (32, 64, 128, 256, 512)],
            [10, 16, 27, 47, 83],
        )


if __name__ == "__main__":
    unittest.main()
