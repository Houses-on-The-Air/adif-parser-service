import adif_io
from award_tier import determine_award_tier

def parse_adif(file_content: str):
    """Parses ADIF file content and extracts relevant data."""
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
