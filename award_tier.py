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
        str: The award tier, which can be one of the following:
            - "Mansion" (over 1,000,000 unique addresses)
            - "Victorian Villa" (over 500,000 unique addresses)
            - "Country Cottage" (over 250,000 unique addresses)
            - "Townhouse" (over 100,000 unique addresses)
            - "Detached House" (over 10,000 unique addresses)
            - "Semi-Detached House" (over 1,000 unique addresses)
            - "Terraced House" (over 500 unique addresses)
            - "Bedsit" (over 100 unique addresses)
            - "Participant" (less than or equal to 100 unique addresses)
    """
    if unique_count > 1000000:
        return "Mansion"
    if unique_count > 500000:
        return "Victorian Villa"
    if unique_count > 250000:
        return "Country Cottage"
    if unique_count > 100000:
        return "Townhouse"
    if unique_count > 10000:
        return "Detached House"
    if unique_count > 1000:
        return "Semi-Detached House"
    if unique_count > 500:
        return "Terraced House"
    if unique_count > 100:
        return "Bedsit"
    return "Participant"
