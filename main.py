from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
import os

app = FastAPI()

# Настройка CORS (разрешаем доступ с фронтенда Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloudinary конфиг
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

@app.post("/api/materials")
async def upload_material(
    name: str = Form(...),
    category: str = Form(...),
    width: int = Form(...),
    height: int = Form(...),
    file: UploadFile = Form(...)
):
    result = cloudinary.uploader.upload(file.file)
    return {
        "name": name,
        "category": category,
        "width": width,
        "height": height,
        "image_url": result.get("secure_url")
    }

@app.get("/")
def root():
    return {"message": "ShnaiderKea backend работает"}
