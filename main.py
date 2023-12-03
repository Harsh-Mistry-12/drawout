# BACKGROUND REMOVER API WITHOUT AUTH
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from random import randint
from rembg import remove
from PIL import Image
import os.path
import glob
import uuid
import os

IMAGEDIR_UPLOAD = "uploaded_images/"
IMAGEDIR_CLEANED = "cleaned_images/"

app = FastAPI() 

@app.post("/upload/")
async def create_upload_file(file: UploadFile = File(...)):
    file.filename=f"{uuid.uuid4()}"
    contents = await file.read()
    
    with open(f"{IMAGEDIR_UPLOAD}{file.filename}", "wb") as f:
        f.write(contents)
        
    removeBG = Image.open(f"{IMAGEDIR_UPLOAD}{file.filename}")
    R = remove(removeBG)
    R.save(f"{IMAGEDIR_CLEANED}{file.filename}.png")
    os.remove(f"{IMAGEDIR_UPLOAD}{file.filename}")

    return {"filename": file.filename}

@app.get("/show/") 
async def read_random_file():
    # files = os.listdir(IMAGEDIR_CLEANED)
    folder_path = r'cleaned_images/'
    file_type = r'\*.png'
    files = glob.glob(folder_path + file_type)
    max_file = max(files, key=os.path.getctime)

    path = f"{max_file}"
    
    return FileResponse(path)
