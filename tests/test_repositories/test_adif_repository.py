"""
Unit tests for the ADIF repository.

This module contains test cases that verify the functionality of the ADIF repository,
including the parsing of ADIF data from strings.
"""

import unittest
from unittest.mock import patch

from repositories.adif_repository import AdifIoRepository


class TestAdifIoRepository(unittest.TestCase):
    """
    Unit tests for the ADIF IO repository.

    This suite tests the AdifIoRepository class to ensure it correctly parses ADIF data.
    """

    def test_read_from_string_with_no_adif_io(self):
        """Test reading from string when adif_io is not available."""
        with patch("repositories.adif_repository.adif_io", None):
            repo = AdifIoRepository()
            result = repo.read_from_string("test content")
            self.assertEqual(result, [{"call": "AB1CD"}])

            # Test with empty content
            empty_result = repo.read_from_string("")
            self.assertEqual(empty_result, [])

    @patch("repositories.adif_repository.adif_io")
    def test_read_from_string_with_adif_io(self, mock_adif_io):
        """Test reading from string with adif_io available."""
        # Set up the mock
        mock_records = [{"call": "TEST1"}, {"call": "TEST2"}]
        mock_adif_io.read_from_string.return_value = mock_records

        # Call the repository method
        repo = AdifIoRepository()
        result = repo.read_from_string("test content")

        # Check the result and that the mock was called correctly
        self.assertEqual(result, mock_records)
        mock_adif_io.read_from_string.assert_called_once_with("test content")
