"""
ADIF Service Module

This module provides the service layer for processing ADIF files.
"""


class AdifService:
    """
    Service for processing ADIF files.

    This class follows the Single Responsibility Principle by handling only
    the business logic for processing ADIF files.
    """

    def __init__(self, adif_repository, award_service):
        """
        Initialize the ADIF service.

        Args:
            adif_repository: A repository for ADIF data.
            award_service: A service for determining award tiers.
        """
        self.adif_repository = adif_repository
        self.award_service = award_service

    def is_valid_adif_file(self, filename):
        """
        Check if a file is a valid ADIF file based on its extension.

        Args:
            filename (str): The name of the file to check.

        Returns:
            bool: True if the file has a valid ADIF extension, False otherwise.
        """
        if not filename:
            return False
        return filename.lower().endswith((".adi", ".adif"))

    def process_adif_content(self, file_content):
        """
        Process the content of an ADIF file.

        Args:
            file_content (str): The content of the ADIF file.

        Returns:
            dict: A dictionary containing information about the ADIF data.
        """
        records = self.adif_repository.read_from_string(file_content)
        callsigns = [record.get("call", "") for record in records]
        unique_addresses = len(set(callsigns))
        award_tier = self.award_service.determine_award_tier(unique_addresses)
        callsign = callsigns[0] if callsigns else "Unknown"

        return {
            "unique_addresses": unique_addresses,
            "award_tier": award_tier,
            "callsign": callsign,
        }
