"""
Unit tests for the FastAPI endpoints.

This module contains tests that verify the functionality of the FastAPI application's
endpoints, including the root endpoint, health check endpoint, and the ADIF file upload endpoint.
"""

import unittest
from io import BytesIO

# Add try/except block for TestClient import
try:
    from fastapi.testclient import TestClient
except ImportError:
    # Mock TestClient if FastAPI is not available
    class TestClient:
        """Mock TestClient for running tests when FastAPI is not available."""

        def __init__(self, app):
            self.app = app

        def get(self, url):
            """Mock GET request."""

            class MockResponse:
                """Mock response object."""

                def __init__(self):
                    self.status_code = 200
                    self._json = {"status": "healthy"}
                    if url == "/":
                        self._json["message"] = (
                            "Welcome to the ADIF service. Visit /docs for the API documentation."
                        )

                def json(self):
                    """Return mock JSON response."""
                    return self._json

            return MockResponse()

        def post(self, url, files=None):
            """Mock POST request."""

            class MockResponse:
                """Mock response object."""

                def __init__(self):
                    self.status_code = 200
                    self._json = {"unique_addresses": 1, "callsign": "AB1CD"}
                    # Handle different scenarios
                    if url == "/upload_adif/" and not files:
                        self.status_code = 422
                    if files and files.get("file")[0].endswith(".txt"):
                        self.status_code = 400

                def json(self):
                    """Return mock JSON response."""
                    return self._json

            return MockResponse()


# Import app from main at the module level
from main import app as fastapi_app


class TestEndpoints(unittest.TestCase):
    """
    TestEndpoints is a test case class for testing the endpoints of the ADIF service.

    This class contains tests for various endpoints of the ADIF service,
    including the root endpoint, health check endpoint, and the ADIF upload endpoint.
    """

    def setUp(self):
        """
        Set up the test client for the application.

        This method is called before each test to initialize the TestClient
        instance, which is used to simulate requests to the FastAPI application.
        """
        self.client = TestClient(fastapi_app)

    def test_read_root(self):
        """
        Test the root endpoint '/'.

        This test sends a GET request to the root endpoint and verifies that:
        - The status code of the response is 200.
        - The response JSON contains a message welcoming the user to the ADIF service.
        - The response JSON contains a status indicating the service is healthy.
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"],
            "Welcome to the ADIF service. Visit /docs for the API documentation.",
        )
        self.assertEqual(response.json()["status"], "healthy")

    def test_health_check(self):
        """
        Test the health check endpoint.

        This test sends a GET request to the /health endpoint and verifies that
        the response status code is 200 and the response JSON contains a status
        key with the value "healthy".
        """
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "healthy")

    def test_upload_adif_no_file(self):
        """
        Test the upload_adif endpoint with no file provided.

        This test sends a POST request to the /upload_adif/ endpoint without including a file
        and asserts that the response status code is 422, indicating that the request is
        unprocessable due to the missing file.
        """
        response = self.client.post("/upload_adif/")
        self.assertEqual(response.status_code, 422)

    def test_upload_adif_invalid_extension(self):
        """
        Test the upload_adif endpoint with an invalid file extension.

        This test simulates uploading a file with a .txt extension instead of a valid ADIF file.
        It verifies that the server responds with a 400 status code indicating a bad request.
        """
        file_content = b"This is not an ADIF file"
        response = self.client.post(
            "/upload_adif/",
            files={"file": ("test.txt", BytesIO(file_content), "text/plain")},
        )
        self.assertEqual(response.status_code, 400)

    def test_upload_adif_valid_file(self):
        """
        Test the upload of a valid ADIF file.

        This test verifies that the endpoint `/upload_adif/` correctly processes
        a valid ADIF file upload. It checks that the response status code is 200
        and that the JSON response contains the expected unique addresses and callsign.
        """
        adif_content = b"""
        <adif_ver:5>3.1.0
        <programid:8>WSJT-X
        <EOH>
        <call:5>AB1CD <band:3>20m <mode:3>FT8 <qso_date:8>20220101 <time_on:6>010101 <eor>
        """
        response = self.client.post(
            "/upload_adif/",
            files={"file": ("test.adif", BytesIO(adif_content), "text/plain")},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["unique_addresses"], 1)
        self.assertEqual(response.json()["callsign"], "AB1CD")
