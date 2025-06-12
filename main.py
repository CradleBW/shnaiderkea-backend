from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
import cloudinary
import cloudinary.uploader
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/api/generate")
async def generate_image(
    prompt: str = Form(...),
    image: UploadFile = File(...)
):
    image_upload = cloudinary.uploader.upload(image.file)
    image_url = image_upload.get("secure_url")

    debug_info = {"image_url": image_url, "prompt": prompt}

    try:
        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers={
                "Authorization": f"Token {os.getenv('REPLICATE_API_TOKEN')}",
                "Content-Type": "application/json",
            },
            json={
                "version": "d2f73565c889f8099632e7b7df6c5d45ecf55e57be0063c037f95a009409d3a3",
                "input": {
                    "image": image_url,
                    "prompt": prompt,
                    "guidance_scale": 7.5,
                    "num_inference_steps": 30
                }
            }
        )

        debug_info["status_code"] = response.status_code
        debug_info["replicate_response"] = response.json()

        return debug_info

    except Exception as e:
        return {"error": str(e), "debug_info": debug_info}
