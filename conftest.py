"""
Pytest configuration for the ADIF Parser Service.

This module sets up the test environment, including mocking dependencies
that might not be available during testing.
"""

import sys
import pytest
from unittest.mock import MagicMock


def pytest_configure(config):
    """Configure pytest environment."""

    # Create mocks for dependencies that might be unavailable during testing
    class MockAdifIO:
        """Mock for adif_io library."""

        @staticmethod
        def read_from_string(content):
            """Mock read_from_string method."""
            if not content:
                return []
            # Simple mock parsing that returns a list with a single record
            return [{"call": "AB1CD"}]

    class MockFastAPI:
        """Mock for FastAPI class."""

        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def get(self, path):
            """Mock route decorator."""

            def decorator(func):
                return func

            return decorator

        def post(self, path):
            """Mock route decorator."""

            def decorator(func):
                return func

            return decorator

    class MockFile:
        """Mock for File class."""

        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            return self

    class MockUploadFile:
        """Mock for UploadFile class."""

        def __init__(self, *args, **kwargs):
            pass

    class MockHTTPException(Exception):
        """Mock for HTTPException class."""

        def __init__(self, status_code=400, detail="Error"):
            self.status_code = status_code
            self.detail = detail

    class MockJSONResponse:
        """Mock for JSONResponse class."""

        def __init__(self, content, **kwargs):
            self.content = content

    # Add mocks to sys.modules if the real modules are not available
    mock_modules = {
        "adif_io": MockAdifIO(),
        "fastapi": MagicMock(
            FastAPI=MockFastAPI,
            File=MockFile,
            UploadFile=MockUploadFile,
            HTTPException=MockHTTPException,
        ),
        "fastapi.responses": MagicMock(JSONResponse=MockJSONResponse),
        "fastapi.testclient": MagicMock(),
    }

    for mod_name, mock in mock_modules.items():
        if mod_name not in sys.modules:
            sys.modules[mod_name] = mock
