#!/usr/bin/env python3

import unittest

from cycle42_gcd_packet_pairing import packet_census, pairing_audit


class Cycle42GcdPacketPairingTests(unittest.TestCase):
    def test_every_packet_weight_is_certified_positive(self):
        groups = packet_census(2, 8, 192)
        self.assertTrue(all(packet.weight > 0 for group in groups for packet in group))

    def test_small_block_has_cardinality_obstruction_only(self):
        audit = pairing_audit(2, 8, 192)
        self.assertEqual(audit["counts"], {
            "diagonal": 6,
            "equal_sign": 7,
            "unfavorable_total": 13,
            "opposite_sign": 6,
        })
        self.assertTrue(audit["injective_domination_obstructed_by_count"])
        self.assertFalse(audit["arbitrary_capacity_domination_obstructed_by_mass"])

    def test_block_2_16_has_mass_obstruction(self):
        audit = pairing_audit(2, 16, 192)
        self.assertEqual(audit["counts"]["unfavorable_total"], 31)
        self.assertEqual(audit["counts"]["opposite_sign"], 22)
        self.assertTrue(audit["weights"]["deficit"] > 0)
        self.assertTrue(audit["arbitrary_capacity_domination_obstructed_by_mass"])


if __name__ == "__main__":
    unittest.main()
