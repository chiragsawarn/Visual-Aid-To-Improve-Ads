import requests
import json
import base64
from io import BytesIO
from PIL import Image

# Change the url accoring to the flask application running in Google Collab
url = "http://e04b-34-91-45-67.ngrok.io/objectDetect"



def object_detect_api(imagefile):
  payload={}
  files=[
    ('image',('2.jpg',open(imagefile,'rb'),'image/jpeg'))
  ]
  headers = {}
  response = requests.request("POST", url, headers=headers, data=payload, files=files)
  dict_data = json.loads(response.text) #Convert json to dictionary
  img = dict_data["image"] 
  img = base64.b64decode(img) 
  img = BytesIO(img)
  img = Image.open(img) 
  img.save('static/images/objects_classified.jpg')
  return dict_data['data']