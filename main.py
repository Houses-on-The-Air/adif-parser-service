from fastapi import FastAPI, File, UploadFile
from adif_parser import parse_adif

app = FastAPI()

@app.post("/upload_adif/")
async def upload_adif(file: UploadFile = File(...)):
    content = await file.read()
    file_content = content.decode("utf-8")
    result = parse_adif(file_content)
    return result
