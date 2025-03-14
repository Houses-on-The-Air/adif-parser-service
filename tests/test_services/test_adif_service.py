"""
Unit tests for the ADIF service.

This module contains test cases that verify the functionality of the ADIF service,
including file validation and ADIF content processing.
"""

import unittest
from unittest.mock import Mock

from services.adif_service import AdifService


class TestAdifService(unittest.TestCase):
    """
    Unit tests for the ADIF service.

    This suite tests the AdifService class to ensure it correctly validates files
    and processes ADIF content.
    """

    def setUp(self):
        """Set up test dependencies."""
        self.mock_repository = Mock()
        self.mock_award_service = Mock()
        self.service = AdifService(self.mock_repository, self.mock_award_service)

    def test_is_valid_adif_file(self):
        """Test validation of ADIF file names."""
        self.assertTrue(self.service.is_valid_adif_file("test.adi"))
        self.assertTrue(self.service.is_valid_adif_file("test.adif"))
        self.assertFalse(self.service.is_valid_adif_file("test.txt"))
        self.assertFalse(self.service.is_valid_adif_file(None))

    def test_process_adif_content(self):
        """Test processing of ADIF content."""
        # Setup mock behaviors
        self.mock_repository.read_from_string.return_value = [
            {"call": "AB1CD"},
            {"call": "EF2GH"},
        ]
        self.mock_award_service.determine_award_tier.return_value = "Test Tier"

        # Call the service method
        result = self.service.process_adif_content("mock content")

        # Check the result
        self.assertEqual(result["unique_addresses"], 2)
        self.assertEqual(result["award_tier"], "Test Tier")
        self.assertEqual(result["callsign"], "AB1CD")

        # Verify the mocks were called correctly
        self.mock_repository.read_from_string.assert_called_once_with("mock content")
        self.mock_award_service.determine_award_tier.assert_called_once_with(2)

    def test_process_adif_content_empty(self):
        """Test processing of empty ADIF content."""
        # Setup mock behaviors for empty content
        self.mock_repository.read_from_string.return_value = []
        self.mock_award_service.determine_award_tier.return_value = "Participant"

        # Call the service method
        result = self.service.process_adif_content("")

        # Check the result
        self.assertEqual(result["unique_addresses"], 0)
        self.assertEqual(result["award_tier"], "Participant")
        self.assertEqual(result["callsign"], "Unknown")
