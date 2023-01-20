from google.cloud import vision
import io
import os
import hashlib

image_data = {}


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'reddys-rad-ads-859d5b1496fa.json'

def get_textual_details(image_file):
    #Generate Hash of the File
    with open(image_file, "rb") as f:
        hash = hashlib.sha256(f.read()).hexdigest()

    # If hash of the file is already in the dictionary then no need to call API 
    if hash in list(image_data.keys()):
        return image_data[hash]
    
    client = vision.ImageAnnotatorClient()
    with io.open(image_file, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    image_data[hash] = document
    return document

