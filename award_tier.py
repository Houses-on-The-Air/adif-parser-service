def determine_award_tier(unique_count):
    """
    Determines the award tier based on the unique address count.

    Parameters:
        unique_count (int): The count of unique addresses.

    Returns:
        str: The award tier, which can be "Gold", "Silver", "Bronze", or "Participant".
    """
    match unique_count:
        case _ if unique_count > 1000000:
            return "Mansion"
        case _ if unique_count > 500000:
            return "Victorian Villa"
        case _ if unique_count > 250000:
            return "Country Cottage"
        case _ if unique_count > 100000:
            return "Townhouse"
        case _ if unique_count > 10000:
            return "Detached House"
        case _ if unique_count > 1000:
            return "Semi-Detached House"
        case _ if unique_count > 500:
            return "Terraced House"
        case _ if unique_count > 100:
            return "Bedsit"
    return "Participant"
