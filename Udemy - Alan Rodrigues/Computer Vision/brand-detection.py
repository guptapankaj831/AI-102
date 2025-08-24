# azure-cognitiveservices.vision.computervision

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from dotenv import load_dotenv
import os

load_dotenv()

computer_vision_endpoint = os.environ.get('COMPUTER_VISION_ENDPOINT')
computer_vision_key = os.environ.get('COMPUTER_VISION_KEY')

# VisualFeatureTypes.categories       # Categorizes the image content into a taxonomy.
# VisualFeatureTypes.tags             # Identifies tags related to the image content.
# VisualFeatureTypes.description      # Generates a human-readable description of the image.
# VisualFeatureTypes.faces            # Detects human faces along with age and gender.
# VisualFeatureTypes.image_type       # Identifies if the image is clip art or a line drawing.
# VisualFeatureTypes.color            # Analyzes the image's dominant colors and whether it's black and white.
# VisualFeatureTypes.adult            # Detects adult, racy, or gory content in the image.
# VisualFeatureTypes.objects          # Detects and identifies objects in the image.
# VisualFeatureTypes.brands           # Detects commercial brands/logos present in the image.
# VisualFeatureTypes.scene            # Identifies the overall scene of the image.
# VisualFeatureTypes.smart_crops      # Suggests smart crop regions based on image composition.

client = ComputerVisionClient(endpoint=computer_vision_endpoint, credentials=CognitiveServicesCredentials(computer_vision_key))
features = [VisualFeatureTypes.brands, VisualFeatureTypes.description]

with open('microsoft.png', 'rb') as image_client:
    response = client.analyze_image_in_stream(image_client, visual_features=features)
    print(response)

for brand in response.brands:
   print(f"{brand.name} - (confidence: {brand.confidence:.2f}) at {brand.rectangle}")
