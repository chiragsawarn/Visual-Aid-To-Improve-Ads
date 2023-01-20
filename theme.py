from extract_textual_details import get_textual_details
import io
from google.cloud import vision
from textcount import  get_words_and_theme_words, bound_center_text_area


RESULT_IMAGE_PATH = "./static/images/divided_image.jpeg"

def polygonArea(X, Y, n):
    area = 0.0
    j = n - 1
    for i in range(0,n):
        area += (X[j] + X[i]) * (Y[j] - Y[i])
        j = i  
    return (abs(area / 2.0))



def find_theme_of_image(image_file):
    client = vision.ImageAnnotatorClient()
    with io.open(image_file, "rb") as image_file_object:
        content = image_file_object.read()

    imageGCVA = vision.Image(content=content)
    response = client.document_text_detection(image=imageGCVA)
    document = response.full_text_annotation
    words, theme_words = get_words_and_theme_words(document, 1)
    result_image = bound_center_text_area(image_file, response, document, theme_words)
    result_image.save(RESULT_IMAGE_PATH)
    # random number - 123, fill in when decided
    return 123
   


