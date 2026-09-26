from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import io
from PIL import Image
import cv2
import numpy as np

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Amina Video Server is Running on Render!"}

@app.post("/generate-video")
async def generate_video(file: UploadFile = File(...), prompt: str = Form(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # تصویر کو پروسیس کر کے فوری ویڈیو بنانا
    img_np = np.array(image)
    img_np = cv2.resize(img_np, (256, 256))
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    video_path = "output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, 4.0, (256, 256))

    for _ in range(4):
        out.write(img_np)
    out.release()

    return FileResponse(video_path, media_type="video/mp4")
