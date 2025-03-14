"""
Unit tests for the award tier determination module.

This module contains tests that verify the correct determination of award tiers
based on the number of unique addresses in an ADIF file.
"""

import unittest

from award_tier import determine_award_tier


class TestAwardTier(unittest.TestCase):
    """
    Test cases for the award tier determination function.

    These tests verify that the determine_award_tier function returns the correct
    tier for various unique address counts, covering all possible tiers.
    """

    def test_participant_tier(self):
        """Test that counts below 100 return 'Participant'."""
        self.assertEqual(determine_award_tier(0), "Participant")
        self.assertEqual(determine_award_tier(50), "Participant")
        self.assertEqual(determine_award_tier(99), "Participant")

    def test_bedsit_tier(self):
        """Test that counts between 100 and 500 return 'Bedsit'."""
        self.assertEqual(determine_award_tier(100), "Bedsit")
        self.assertEqual(determine_award_tier(250), "Bedsit")
        self.assertEqual(determine_award_tier(499), "Bedsit")

    def test_terraced_house_tier(self):
        """Test that counts between 500 and 1000 return 'Terraced House'."""
        self.assertEqual(determine_award_tier(500), "Terraced House")
        self.assertEqual(determine_award_tier(750), "Terraced House")
        self.assertEqual(determine_award_tier(999), "Terraced House")

    def test_higher_tiers(self):
        """Test higher award tiers."""
        self.assertEqual(determine_award_tier(1000), "Semi-Detached House")
        self.assertEqual(determine_award_tier(10000), "Detached House")
        self.assertEqual(determine_award_tier(100000), "Townhouse")
        self.assertEqual(determine_award_tier(250000), "Country Cottage")
        self.assertEqual(determine_award_tier(500000), "Victorian Villa")
        self.assertEqual(determine_award_tier(1000000), "Mansion")
