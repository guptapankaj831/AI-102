# azure-ai-vision-imageanalysis
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
import json

load_dotenv()

computer_vision_endpoint = os.environ.get('COMPUTER_VISION_ENDPOINT')
computer_vision_key = os.environ.get('COMPUTER_VISION_KEY')

client = ImageAnalysisClient(endpoint=computer_vision_endpoint, credential=AzureKeyCredential(computer_vision_key))

with open('lady-dog.jpg', 'rb') as image_file:
    image_details = image_file.read()

# VisualFeatures.CAPTION         # Generates a natural language caption describing the image.
# VisualFeatures.DENSE_CAPTIONS  # Produces multiple captions for different regions of the image.
# VisualFeatures.READ            # Extracts printed and handwritten text from the image. This is OCR
# VisualFeatures.TAGS            # Extracts descriptive tags for the image content.
# VisualFeatures.OBJECTS         # Detects and identifies objects within the image. # Object Detection
# VisualFeatures.SMART_CROPS     # Suggests smart crop regions based on visual saliency.
# VisualFeatures.PEOPLE          # Detects human figures in the image without identifying them.

response = client.analyze(
    image_data=image_details,
    visual_features=[VisualFeatures.TAGS, VisualFeatures.CAPTION, VisualFeatures.OBJECTS, VisualFeatures.READ]
)

print(json.dumps(response.as_dict(), indent=4))

# # Read individual line when we use only VisualFeatures.READ - OCR
# for line in response.read.blocks[0].lines:
#     print(line)


