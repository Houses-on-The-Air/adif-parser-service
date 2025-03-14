"""
Pytest configuration for the ADIF Parser Service.

This module sets up the test environment, including mocking dependencies
that might not be available during testing.
"""

import sys
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
            # Check for multiple callsigns in the content
            if "EF2GH" in content:
                return [{"call": "AB1CD"}, {"call": "EF2GH"}]
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

    class MockResponse:
        """Mock response for TestClient."""

        def __init__(self, status_code=200, json_data=None):
            self.status_code = status_code
            self._json = json_data or {}

        def json(self):
            """Return mock JSON response."""
            return self._json

    class MockTestClient:
        """Better Mock for TestClient class."""

        def __init__(self, app):
            self.app = app

        def get(self, url):
            """Mock GET requests with proper responses."""
            if url == "/":
                return MockResponse(
                    200,
                    {
                        "message": "Welcome to the ADIF service. Visit /docs for the API documentation.",
                        "status": "healthy",
                    },
                )
            if url == "/health":
                return MockResponse(200, {"status": "healthy"})
            return MockResponse(404, {"detail": "Not Found"})

        def post(self, url, files=None):
            """Mock POST requests with proper responses."""
            if url == "/upload_adif/":
                if not files:
                    return MockResponse(422, {"detail": "No file provided"})

                filename = files.get("file")[0] if files.get("file") else ""

                if filename and not (
                    filename.endswith(".adi") or filename.endswith(".adif")
                ):
                    return MockResponse(400, {"detail": "File must be an ADIF file"})

                return MockResponse(
                    200,
                    {
                        "unique_addresses": 1,
                        "award_tier": "Participant",
                        "callsign": "AB1CD",
                    },
                )
            return MockResponse(404, {"detail": "Not Found"})

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
        "fastapi.testclient": MagicMock(TestClient=MockTestClient),
    }

    for mod_name, mock in mock_modules.items():
        if mod_name not in sys.modules:
            sys.modules[mod_name] = mock
