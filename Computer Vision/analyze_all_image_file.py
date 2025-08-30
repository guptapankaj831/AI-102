import os
from dotenv import load_dotenv

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv('COMPUTER_VISION_ENDPOINT')
key = os.getenv('COMPUTER_VISION_KEY')

client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
features = [
    VisualFeatures.CAPTION,
    VisualFeatures.DENSE_CAPTIONS,
    VisualFeatures.TAGS,
    VisualFeatures.PEOPLE,
    VisualFeatures.OBJECTS,
    VisualFeatures.SMART_CROPS,
    VisualFeatures.READ
]

with open('analyze_all_image_file.jpg', 'rb') as image_file:
    image_data = image_file.read()

response = client.analyze(
        image_data=image_data,
        visual_features=features,   # Mandatory. Select one or more visual features to analyze.
        smart_crops_aspect_ratios=[0.9, 1.33],  # Optional. Relevant only if SMART_CROPS was specified above.
        gender_neutral_caption=True,  # Optional. Relevant only if CAPTION or DENSE_CAPTIONS were specified above.
        language='en',  # Optional. Relevant only if TAGS is specified above. See https://aka.ms/cv-languages for supported languages.
        model_version="latest",  # Optional. Analysis model version to use. Defaults to "latest".
    )
client.close()

try:
    with open('analyze_all_image_file_response.json', 'w') as file:
        file.write(str(response))
except:
    pass

# Print all analysis results to the console
print(f"{'-' * 50}\nImage analysis results:\n")

if response.caption is not None:
    print(f"\n{'-' * 50}\nCAPTION:\n{'-' * 50}\n")
    print(f"Text: {response.caption.text}, Confidence: {response.caption.confidence:.4f}")

if response.dense_captions is not None:
    print(f"\n{'-' * 50}DENSE_CAPTIONS:\n{'-' * 50}\n")
    # Print dense caption results to the console. The first caption always
    # corresponds to the entire image. The rest correspond to sub regions.
    for res in response.dense_captions.list:
        print(f"Text: {res.text}, Confidence: {res.confidence:.4f}, Bounding Box: {res.bounding_box}")

if response.read is not None:
    print(f"\n{'-' * 50}\nREAD - OCR:\n{'-' * 50}\n")
    for line in response.read.blocks[0].lines:
        print(f"Line: {line}, Line Bounding Box: {line.bounding_polygon}")
        for word in line.words:
            print(f"Word: {word.text}, Confidence:{word.confidence:.4f}, Word Bounding polygon: {word.bounding_polygon}")

if response.tags is not None:
    print(f"\n{'-' * 50}\nTAGS:\n{'-' * 50}\n")
    for tag in response.tags.list:
        print(f'Text: {tag.name}, Confidence: {tag.confidence:.4f}')

if response.objects is not None:
    print(f"\n{'-' * 50}\nOBJECTS:\n{'-' * 50}\n")
    for obj in response.objects.list:
        print(f'Text: {obj.tags[0].name} Bounding Box: {obj.bounding_box}, Confidence: {obj.tags[0].confidence:.4f}')

if response.people is not None:
    print(f"\n{'-' * 50}\nPEOPLE:\n{'-' * 50}\n")
    for people in response.people.list:
        print(f"Bounding Box: {people.bounding_box}, Confidence: {people.confidence:.4f}")

if response.smart_crops is not None:
    print(f"\n{'-' * 50}\nSMART_CORPS:\n{'-' * 50}\n")
    for smart_crop in response.smart_crops.list:
        print(f'Aspect Ratio: {smart_crop.aspect_ratio}, Smart Crop: {smart_crop.bounding_box}')

print(f"\n{'-' * 50}\nImage Height : {response.metadata.height}")
print(f"\n{'-' * 50}\nImage Width : {response.metadata.width}")
print(f"\n{'-' * 50}\nModel Version : {response.model_version}")
