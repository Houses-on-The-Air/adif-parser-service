def determine_award_tier(unique_count):
    """Determines award tier based on unique address count."""
    if unique_count > 100:
        return "Gold"
    elif unique_count > 50:
        return "Silver"
    elif unique_count > 10:
        return "Bronze"
    return "Participant"
