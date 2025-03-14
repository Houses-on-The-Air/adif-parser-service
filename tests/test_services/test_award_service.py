"""
Unit tests for the award service.

This module contains test cases that verify the functionality of the award service,
including the determination of award tiers based on unique address counts.
"""

import unittest

from models.award_tier import AwardTier
from services.award_service import AwardService


class TestAwardService(unittest.TestCase):
    """
    Unit tests for the award service.

    This suite tests the AwardService class to ensure it correctly determines
    award tiers based on unique address counts.
    """

    def setUp(self):
        """Set up the award service for testing."""
        self.service = AwardService()

    def test_participant_tier(self):
        """Test that counts below 100 return 'Participant'."""
        self.assertEqual(self.service.determine_award_tier(0), AwardTier.PARTICIPANT)
        self.assertEqual(self.service.determine_award_tier(50), AwardTier.PARTICIPANT)
        self.assertEqual(self.service.determine_award_tier(99), AwardTier.PARTICIPANT)

    def test_bedsit_tier(self):
        """Test that counts between 100 and 500 return 'Bedsit'."""
        self.assertEqual(self.service.determine_award_tier(100), AwardTier.BEDSIT)
        self.assertEqual(self.service.determine_award_tier(250), AwardTier.BEDSIT)
        self.assertEqual(self.service.determine_award_tier(499), AwardTier.BEDSIT)

    def test_terraced_house_tier(self):
        """Test that counts between 500 and 1000 return 'Terraced House'."""
        self.assertEqual(
            self.service.determine_award_tier(500), AwardTier.TERRACED_HOUSE
        )
        self.assertEqual(
            self.service.determine_award_tier(750), AwardTier.TERRACED_HOUSE
        )
        self.assertEqual(
            self.service.determine_award_tier(999), AwardTier.TERRACED_HOUSE
        )

    def test_higher_tiers(self):
        """Test higher award tiers."""
        self.assertEqual(
            self.service.determine_award_tier(1000), AwardTier.SEMI_DETACHED_HOUSE
        )
        self.assertEqual(
            self.service.determine_award_tier(10000), AwardTier.DETACHED_HOUSE
        )
        self.assertEqual(self.service.determine_award_tier(100000), AwardTier.TOWNHOUSE)
        self.assertEqual(
            self.service.determine_award_tier(250000), AwardTier.COUNTRY_COTTAGE
        )
        self.assertEqual(
            self.service.determine_award_tier(500000), AwardTier.VICTORIAN_VILLA
        )
        self.assertEqual(self.service.determine_award_tier(1000000), AwardTier.MANSION)
