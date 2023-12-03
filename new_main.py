# BASCKGROUND REMOVER API 
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
from random import randint
from rembg import remove
import mysql.connector
from PIL import Image
import os.path
import glob
import uuid
import os

fetch_credentials = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='user_token',
    port=3306
)
fetch_cur = fetch_credentials.cursor()

username_query = "SELECT user_name, token from user_credentials"
fetch_cur.execute(username_query)
info = fetch_cur.fetchall()
# print(username[0][0]) ---> username
# print(username[0][1]) ---> token

for credentials in info:
    # print(credentials[0])

    IMAGEDIR_UPLOAD = "uploaded_images/"
    IMAGEDIR_CLEANED = "cleaned_images/"

    app = FastAPI() 

    # OAuth2 password bearer for user authentication
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def get_current_user(token: str = Depends(oauth2_scheme)):
        # You can implement user authentication logic here based on the token
        if token ==f'{credentials[1]}':
        # For simplicity, I'm just returning a dummy user for now
            return {"username": f"{credentials[0]}"}
        else:
            return {"Error":"Please enter correct Token!!!"}

    @app.post("/upload/")
    async def create_upload_file(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
        file.filename = f"{uuid.uuid4()}_{current_user['username']}"
        contents = await file.read()
        
        with open(f"{IMAGEDIR_UPLOAD}{file.filename}", "wb") as f:
            f.write(contents)
            
        removeBG = Image.open(f"{IMAGEDIR_UPLOAD}{file.filename}")
        R = remove(removeBG)
        R.save(f"{IMAGEDIR_CLEANED}{file.filename}.png")
        os.remove(f"{IMAGEDIR_UPLOAD}{file.filename}")

        return {"filename": file.filename}

    @app.get("/show/") 
    async def read_user_files(current_user: dict = Depends(get_current_user)):
        folder_path = r'cleaned_images/'
        file_type = r'\*.png'
        files = glob.glob(folder_path + file_type)

        user_files = [file for file in files if current_user['username'] in file]

        if not user_files:
            raise HTTPException(status_code=404, detail="No cleaned images found for the user.")

        latest_file = max(user_files, key=os.path.getctime)
        
        return FileResponse(latest_file)
