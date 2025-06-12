from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
import os

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

materials_db = []

@app.post("/api/materials")
async def upload_material(
    name: str = Form(...),
    category: str = Form(...),
    width: float = Form(...),
    height: float = Form(...),
    file: UploadFile = File(...)
):
    result = cloudinary.uploader.upload(file.file)
    material = {
        "name": name,
        "category": category,
        "width": width,
        "height": height,
        "image_url": result.get("secure_url")
    }
    materials_db.append(material)
    return material

@app.get("/api/materials")
def get_materials():
    return materials_db

@app.get("/")
def root():
    return {"message": "ShnaiderKea backend работает"}
