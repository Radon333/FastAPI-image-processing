from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import base64
import numpy as np
from PIL import Image
import io, json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)
def PILImage_to_cv2(img):
    return np.asarray(img)

def PILImage_to_base64str(pilimg):
    buffered = io.BytesIO()
    pilimg.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')

def cv2_to_PILImage(img):
    return Image.fromarray(img)

def base64str_to_PILImage(base64str):
    base64_img_bytes = base64str.encode('utf-8')
    base64bytes = base64.b64decode(base64_img_bytes)
    bytesObj = io.BytesIO(base64bytes)
    pilimg = Image.open(bytesObj)
    return pilimg

def base64str_to_cv2(base64str):
    im_bytes = base64.b64decode(base64str)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    cv2img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return cv2img
    
def cv2_to_base64str(cv2img):
    pilimg = cv2_to_PILImage(cv2img)
    buffered = io.BytesIO()
    pilimg.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode('utf-8')

@app.get("/")
async def root():
    return {"message": "Sending image to client as base64 string"}

@app.post("/model")
async def root(file: UploadFile = File(...)):
    content = await file.read()
    base64str = base64.b64encode(content).decode("utf-8")
    #Use desired functions here
    return base64str



