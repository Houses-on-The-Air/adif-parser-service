"""
ADIF Parser Service - Main Application

This module defines a FastAPI application for parsing ADIF files and extracting
callsign data. The application provides endpoints for uploading and processing
ADIF files, checking service health, and displaying welcome information.
"""

try:
    from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
    from fastapi.responses import JSONResponse
except ImportError:
    # Mock for testing when fastapi is not available
    class MockClass:
        """Mock class for testing when FastAPI is not available."""

        def __init__(self, *args, **kwargs):
            pass

        def __call__(self, *args, **kwargs):
            return self

        def get(self, *args, **kwargs):
            return self

        def post(self, *args, **kwargs):
            return self

    class MockException(Exception):
        """Base exception class for mock exceptions."""

    class MockHTTPException(MockException):
        """Mock exception class for HTTPException."""

        def __init__(self, status_code=400, detail="Error"):
            self.status_code = status_code
            self.detail = detail
            super().__init__(f"{status_code}: {detail}")

    FastAPI = File = UploadFile = MockClass
    HTTPException = MockHTTPException
    JSONResponse = MockClass

# Third party imports
from dependencies import get_adif_service
from services.adif_service import AdifService

app = FastAPI(
    title="ADIF Parser Service",
    description="Service to parse ADIF files and extract callsign data",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """
    Handles the root endpoint of the ADIF service.

    Returns:
        dict: A dictionary containing a welcome message and the service status.
    """
    return {
        "message": "Welcome to the ADIF service. Visit /docs for the API documentation.",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    """
    Perform a health check of the service.

    Returns:
        dict: A dictionary containing the health status of the service.
    """
    return {"status": "healthy"}


@app.post("/upload_adif/")
async def upload_adif(
    file: UploadFile = File(...), adif_service: AdifService = Depends(get_adif_service)
):
    """
    Asynchronously uploads and processes an ADIF (Amateur Data Interchange Format) file.

    Args:
        file (UploadFile): The ADIF file to be uploaded.
        adif_service (AdifService): The service for processing ADIF files.

    Returns:
        dict: The result of parsing the ADIF file content.

    Raises:
        HTTPException: If there's an error processing the file.
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        if not adif_service.is_valid_adif_file(file.filename):
            raise HTTPException(
                status_code=400, detail="File must be an ADIF file (.adi or .adif)"
            )

        content = await file.read()
        try:
            file_content = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise HTTPException(
                status_code=400,
                detail="File encoding is not supported. Please provide a UTF-8 encoded file",
            ) from exc

        result = adif_service.process_adif_content(file_content)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(exc)}",
        ) from exc
