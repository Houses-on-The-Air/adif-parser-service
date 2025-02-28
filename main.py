from fastapi import FastAPI, File, UploadFile
from adif_parser import parse_adif

app = FastAPI()

@app.post("/upload_adif/")
async def upload_adif(file: UploadFile = File(...)):
    """
    Asynchronously uploads and processes an ADIF (Amateur Data Interchange Format) file.

    Args:
        file (UploadFile): The ADIF file to be uploaded. Defaults to a required file input.

    Returns:
        dict: The result of parsing the ADIF file content.

    Raises:
        UnicodeDecodeError: If the file content cannot be decoded using UTF-8.
    """
    content = await file.read()
    file_content = content.decode("utf-8")
    result = parse_adif(file_content)
    return result
