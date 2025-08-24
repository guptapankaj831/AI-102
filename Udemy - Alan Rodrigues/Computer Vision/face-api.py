# azure-ai-vision-face

from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import *
import json

load_dotenv()

face_api_endpoint = os.environ.get('FACE_API_ENDPOINT')
face_api_key = os.environ.get('FACE_API_KEY')

# Authenticate Face client
client = FaceClient(endpoint=face_api_endpoint, credential=AzureKeyCredential(face_api_key))

# Specify facial features to be retrieved
features = [
    FaceAttributeTypeDetection01.HEAD_POSE,
    FaceAttributeTypeDetection01.OCCLUSION,
    FaceAttributeTypeDetection01.ACCESSORIES,
    ]

with open('pankaj.jpg', 'rb') as image_data:
    detected_faces = client.detect(
        image_content=image_data.read(),
        detection_model=FaceDetectionModel.DETECTION01,
        recognition_model=FaceRecognitionModel.RECOGNITION01,
        return_face_id=False,
        return_face_attributes=features
    )

face_count = 0
if len(detected_faces) > 0:
     print(len(detected_faces), 'faces detected.')
     for face in detected_faces:    
         # Get face properties
         face_count += 1
         print('\nFace number {}'.format(face_count))
         print(' - Head Pose (Yaw): {}'.format(face.face_attributes.head_pose.yaw))
         print(' - Head Pose (Pitch): {}'.format(face.face_attributes.head_pose.pitch))
         print(' - Head Pose (Roll): {}'.format(face.face_attributes.head_pose.roll))
         print(' - Forehead occluded?: {}'.format(face.face_attributes.occlusion["foreheadOccluded"]))
         print(' - Eye occluded?: {}'.format(face.face_attributes.occlusion["eyeOccluded"]))
         print(' - Mouth occluded?: {}'.format(face.face_attributes.occlusion["mouthOccluded"]))
         print(' - Accessories:')
         for accessory in face.face_attributes.accessories:
             print('   - {}'.format(accessory.type))
