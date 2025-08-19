import os
from fastapi import UploadFile

UPLOAD_DIR = "input"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_upload(file: UploadFile):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path
