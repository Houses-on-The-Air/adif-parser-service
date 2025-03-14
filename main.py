"""
ADIF Parser Service - Main Application

This module defines a FastAPI application for parsing ADIF files and extracting
callsign data. The application provides endpoints for uploading and processing
ADIF files, checking service health, and displaying welcome information.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from adif_parser import parse_adif

app = FastAPI(
    title="ADIF Parser Service",
    description="Service to parse ADIF files and extract callsign data",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """
    Handles the root endpoint of the ADIF service.

    Returns:
        dict: A dictionary containing a welcome message and the service status.
    """
    return {"message": "Welcome to the ADIF service. Visit /docs for the API documentation.",
            "status": "healthy"}


@app.get("/health")
def health_check():
    """
    Perform a health check of the service.

    Returns:
        dict: A dictionary containing the health status of the service.
    """
    return {"status": "healthy"}


@app.post("/upload_adif/")
async def upload_adif(file: UploadFile = File(...)):
    """
    Asynchronously uploads and processes an ADIF (Amateur Data Interchange Format) file.

    Args:
        file (UploadFile): The ADIF file to be uploaded.

    Returns:
        dict: The result of parsing the ADIF file content.

    Raises:
        HTTPException: If there's an error processing the file.
    """
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")

        if not file.filename.lower().endswith(('.adi', '.adif')):
            raise HTTPException(status_code=400, detail="File must be an ADIF file (.adi or .adif)")

        content = await file.read()
        try:
            file_content = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise HTTPException(
                status_code=400,
                detail="File encoding is not supported. Please provide a UTF-8 encoded file"
            ) from exc

        result = parse_adif(file_content)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the file: {str(exc)}"
        ) from exc
