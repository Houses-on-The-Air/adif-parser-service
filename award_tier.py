"""
Award Tier Module

This module provides functionality for determining award tiers based on unique contact counts
in amateur radio logs. The tiers represent different types of housing, from a basic
"Participant" level to the prestigious "Mansion" tier.
"""


def determine_award_tier(unique_count):
    """
    Determines the award tier based on the unique address count.

    Parameters:
        unique_count (int): The count of unique addresses.

    Returns:
        str: The award tier based on the number of unique addresses.
    """
    # Define the thresholds and corresponding tiers
    tier_thresholds = [
        (1000000, "Mansion"),
        (500000, "Victorian Villa"),
        (250000, "Country Cottage"),
        (100000, "Townhouse"),
        (10000, "Detached House"),
        (1000, "Semi-Detached House"),
        (500, "Terraced House"),
        (100, "Bedsit"),
        (0, "Participant")
    ]

    # Find the first threshold that the count exceeds
    for threshold, tier in tier_thresholds:
        if unique_count > threshold:
            return tier

    # Default case (should never reach here given the 0 threshold above)
    return "Participant"
