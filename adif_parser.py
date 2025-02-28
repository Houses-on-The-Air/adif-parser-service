import adif_io
from award_tier import determine_award_tier

def parse_adif(file_content: str):
    """
    Parses ADIF file content and extracts relevant data.

    Args:
        file_content (str): The content of the ADIF file as a string.

    Returns:
        dict: A dictionary containing the following keys:
            - unique_addresses (int): The number of unique callsigns found in the ADIF file.
            - award_tier (str): The award tier determined based on the number of unique callsigns.
            - callsign (str): The first callsign found in the ADIF file, or "Unknown" if no callsigns are found.
    """
    records = adif_io.read_from_string(file_content)
    callsigns = [record.get("call", "") for record in records]
    unique_addresses = len(set(callsigns))
    award_tier = determine_award_tier(unique_addresses)
    callsign = callsigns[0] if callsigns else "Unknown"

    return {
        "unique_addresses": unique_addresses,
        "award_tier": award_tier,
        "callsign": callsign
    }
