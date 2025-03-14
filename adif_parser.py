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
    adif_io = None

from award_tier import determine_award_tier
from services.adif_service import extract_callsign_data


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
    if adif_io is None:
        # Mock behavior if adif_io is not available
        return {
            "unique_addresses": 0,
            "award_tier": "Participant",
            "callsign": "Unknown",
        }

    records = adif_io.read_from_string(file_content)

    # Extract data using the shared utility function
    unique_addresses, callsigns = extract_callsign_data(records)

    award_tier = determine_award_tier(unique_addresses)
    callsign = callsigns[0] if callsigns else "Unknown"

    return {
        "unique_addresses": unique_addresses,
        "award_tier": award_tier,
        "callsign": callsign,
    }
