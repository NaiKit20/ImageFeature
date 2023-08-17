import base64
import cv2
from fastapi import FastAPI, Request
import numpy as np
from app.HOG import hog_des
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
      return {"message": "This is my api"}

@app.get("/api/genhog")
async def getInformation(data : Request):
    json = await data.json()
    data = json['img']

    image_bytes = base64.b64decode(data)
    
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    
    image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)

    hog_descriptor = hog_des(image)

    return {"hog": hog_descriptor.tolist()}