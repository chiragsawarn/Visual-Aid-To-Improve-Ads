import cv2
from google.cloud import vision
import io
import os 
import numpy as np




def localize_objects(path):
    """Localize objects in the local image.
    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    image1 = cv2.imread(path)
    width, height = image1.shape[0],image1.shape[1]
    for object_ in objects:
        pts = []
        for vertex in object_.bounding_poly.normalized_vertices:
            pts.append([int(vertex.x*height),int(vertex.y*width)])
        pts = np.array(pts)
        pts = pts.reshape((-1, 1, 2))
        image1 = cv2.polylines(image1,[pts] ,True, (0,0,0), 2)
        # print(pts)
    cv2.imwrite("./static/images/object.jpg",image1)
    return len(objects)