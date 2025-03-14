"""
Award Service Module

This module provides functionality for determining award tiers based on unique contact counts
in amateur radio logs. The tiers represent different types of housing, from a basic
"Participant" level to the prestigious "Mansion" tier.
"""

from models.award_tier import AwardTier


class AwardService:
    """
    Service for determining award tiers.

    This class follows the Single Responsibility Principle by handling only
    the business logic for determining award tiers.
    """

    def __init__(self):
        """Initialize the award service with tier thresholds."""
        self.tier_thresholds = [
            (1000000, AwardTier.MANSION),
            (500000, AwardTier.VICTORIAN_VILLA),
            (250000, AwardTier.COUNTRY_COTTAGE),
            (100000, AwardTier.TOWNHOUSE),
            (10000, AwardTier.DETACHED_HOUSE),
            (1000, AwardTier.SEMI_DETACHED_HOUSE),
            (500, AwardTier.TERRACED_HOUSE),
            (100, AwardTier.BEDSIT),
            (0, AwardTier.PARTICIPANT),
        ]

    def determine_award_tier(self, unique_count):
        """
        Determines the award tier based on the unique address count.

        Parameters:
            unique_count (int): The count of unique addresses.

        Returns:
            str: The award tier based on the number of unique addresses.
        """
        # Find the first threshold that the count exceeds or equals
        for threshold, tier in self.tier_thresholds:
            if unique_count >= threshold:
                return tier

        # Default case (should never reach here given the 0 threshold above)
        return AwardTier.PARTICIPANT
