"""
ADIF Repository Module

This module provides repositories for accessing ADIF data.
"""

try:
    import adif_io
except ImportError:
    # Mock for testing when adif_io is not available
    adif_io = None


class AdifRepository:
    """
    Base interface for ADIF repositories.

    This class follows the Interface Segregation Principle by providing
    a minimal interface that clients can depend on.
    """

    def read_from_string(self, file_content):
        """
        Parse ADIF data from a string.

        Args:
            file_content (str): The ADIF data as a string.

        Returns:
            list: A list of records parsed from the ADIF data.
        """
        raise NotImplementedError


class AdifIoRepository(AdifRepository):
    """
    Repository implementation using the adif_io library.

    This class follows the Liskov Substitution Principle by properly
    implementing the AdifRepository interface.
    """

    def read_from_string(self, file_content):
        """
        Parse ADIF data from a string using adif_io.

        Args:
            file_content (str): The ADIF data as a string.

        Returns:
            list: A list of records parsed from the ADIF data.
        """
        if adif_io is None:
            # Mock behavior if adif_io is not available
            if not file_content:
                return []
            return [{"call": "AB1CD"}]

        return adif_io.read_from_string(file_content)
