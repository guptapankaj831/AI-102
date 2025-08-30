"""
Lab 3: Face Detection & Facial Attributes using Azure Computer Vision (SDK v4.0)

Purpose:
--------
This lab demonstrates how to use the Azure Face API to:
1. Detect faces in an image.
2. Request modern attributes (when available): head pose, mask, quality, etc.
3. Output detection details in structured JSON format.

Requirements:
-------------
- Azure Face API key and endpoint
- Python packages: pip install azure-ai-vision-face==1.0.0b2 azure-core pillow
"""

import os
import os
import sys
import json
from typing import List, Dict, Any
from io import BytesIO
from dotenv import load_dotenv
from PIL import Image, ImageDraw

from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import FaceDetectionModel, FaceRecognitionModel, FaceAttributeTypeDetection01, FaceAttributeTypeRecognition04
from azure.core.credentials import AzureKeyCredential

load_dotenv()

face_endpoint = os.getenv("FACE_ENDPOINT")
face_key = os.getenv("FACE_KEY")

def draw_face_rectangles(image_path, faces):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    for face in faces:
        face_rect = face.face_rectangle
        left = face_rect.left
        top = face_rect.top
        right = left + face_rect.width
        bottom = top + face_rect.height

        # Red rectangle, 3px outline
        draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0), width=3)

    return img

face_client = FaceClient(endpoint=face_endpoint, credential=AzureKeyCredential(face_key))

image_name = 'face_detection_analysis.jpg'
with open(image_name, 'rb') as image_client:
    image_data = image_client.read()

detected_faces = face_client.detect(
    image_content=image_data,
    detection_model=FaceDetectionModel.DETECTION01,
    recognition_model=FaceRecognitionModel.RECOGNITION01,
    return_face_id=False,   # To use True, we should get permission from microsoft
    return_face_landmarks=True,
    return_face_attributes=[
        FaceAttributeTypeDetection01.HEAD_POSE,
        FaceAttributeTypeDetection01.GLASSES,
        FaceAttributeTypeDetection01.ACCESSORIES,
        FaceAttributeTypeDetection01.BLUR,
        FaceAttributeTypeDetection01.EXPOSURE,
        FaceAttributeTypeDetection01.NOISE,
        FaceAttributeTypeDetection01.OCCLUSION,
    ],
    # Keep TTL short; IDs expire after this many seconds (cost neutral).
    face_id_time_to_live=300,
    # Helpful to know exactly which recognition model was used.
    return_recognition_model=True,
)

try:
    with open('face_detection_analysis_response.json', 'w') as output:
        output.write(str(detected_faces))
except Exception:
    pass

if len(detected_faces) and detected_faces[0].face_rectangle:
    # ---- Visualize ----
    annotated = draw_face_rectangles(image_name, detected_faces)
    annotated.save(f"updated_{image_name}")
