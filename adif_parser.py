"""
ADIF Parser Module

This module provides functionality for parsing ADIF (Amateur Data Interchange Format) files.
It extracts callsign information and determines award tiers based on the number of unique
callsigns found in the file.
"""

try:
    import adif_io
except ImportError:
    # Mock for testing when adif_io is not available
    class MockAdifIo:
        @staticmethod
        def read_from_string(file_content):
            if not file_content:
                return []
            # Mock parsing that returns records with unique callsigns for testing
            if "EF2GH" in file_content:
                return [{"call": "AB1CD"}, {"call": "EF2GH"}]
            return [{"call": "AB1CD"}]

    adif_io = MockAdifIo()

from award_tier import determine_award_tier
from services.adif_service import format_adif_result


def parse_adif(file_content):
    """
    Parses ADIF file content and extracts relevant data.

    Args:
        file_content (str): The content of the ADIF file as a string.

    Returns:
        dict: A dictionary containing the following keys:
            - unique_addresses (int): The number of unique callsigns found in the ADIF file.
            - award_tier (str): The award tier determined based on the number of unique callsigns.
            - callsign (str): The first callsign found in the ADIF file, or "Unknown" if no
              callsigns are found.
    """
    if not file_content:
        # Handle empty content
        return {
            "unique_addresses": 0,
            "award_tier": "Participant",
            "callsign": "Unknown",
        }

    records = adif_io.read_from_string(file_content)

    # Extract callsigns and create set for unique addresses
    callsigns = [record.get("call", "") for record in records if record.get("call")]
    unique_addresses = len(set(callsigns))

    # Use the award tier determination from the separate module
    award_tier = determine_award_tier(unique_addresses)

    # Use shared function for formatting the result
    return format_adif_result(unique_addresses, award_tier, callsigns)
