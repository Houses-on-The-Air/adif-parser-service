"""
Unit tests for the ADIF parser module.

This module contains test cases that verify the functionality of the ADIF parser,
including parsing empty ADIF files, valid ADIF files, and handling of duplicate callsigns.
"""

import unittest

from adif_parser import parse_adif


class TestAdifParser(unittest.TestCase):
    """
    Unit tests for the ADIF parser.

    This test suite includes the following tests:
    - `test_parse_empty_adif`: Verifies that parsing an empty ADIF file returns expected defaults.
    - `test_parse_valid_adif`: Verifies that parsing a valid ADIF file returns the correct data.
    - `test_duplicate_callsigns`: Ensures that duplicate callsigns are counted only once.
    """

    def test_parse_empty_adif(self):
        """
        Test the parse_adif function with an empty ADIF string.

        This test ensures that the parse_adif function correctly handles an empty
        ADIF string by returning default values for the parsed fields.

        Assertions:
            - The 'unique_addresses' field should be 0.
            - The 'award_tier' field should be "Participant".
            - The 'callsign' field should be "Unknown".
        """
        result = parse_adif("")
        self.assertEqual(result["unique_addresses"], 0)
        self.assertEqual(result["award_tier"], "Participant")
        self.assertEqual(result["callsign"], "Unknown")

    def test_parse_valid_adif(self):
        """
        Test the parse_adif function with valid ADIF content.

        This test verifies that the parse_adif function correctly parses a valid ADIF string
        and returns the expected results.

        The test checks:
            - The number of unique addresses parsed from the ADIF content is 2.
            - The callsign of the first QSO record is "AB1CD".
        """
        adif_content = """
        <adif_ver:5>3.1.0
        <programid:8>WSJT-X
        <EOH>
        <call:5>AB1CD <band:3>20m <mode:3>FT8 <qso_date:8>20220101 <time_on:6>010101 <eor>
        <call:5>EF2GH <band:3>20m <mode:3>FT8 <qso_date:8>20220101 <time_on:6>010130 <eor>
        """
        result = parse_adif(adif_content)
        self.assertEqual(result["unique_addresses"], 2)
        self.assertEqual(result["callsign"], "AB1CD")

    def test_duplicate_callsigns(self):
        """
        Test case for verifying the handling of duplicate callsigns in ADIF content.

        This test checks if the `parse_adif` function correctly identifies unique callsigns
        when duplicates are present in the ADIF data.

        Expected Result: Only one unique callsign is counted.
        """
        adif_content = """
        <adif_ver:5>3.1.0
        <programid:8>WSJT-X
        <EOH>
        <call:5>AB1CD <band:3>20m <mode:3>FT8 <qso_date:8>20220101 <time_on:6>010101 <eor>
        <call:5>AB1CD <band:3>20m <mode:3>FT8 <qso_date:8>20220101 <time_on:6>010130 <eor>
        """
        result = parse_adif(adif_content)
        self.assertEqual(result["unique_addresses"], 1)
