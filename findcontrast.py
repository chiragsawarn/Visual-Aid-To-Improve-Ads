import cv2 
import numpy as np 
import sys
import shutil
# from extract_textual_details import get_textual_details
import os
import io
from google.cloud import vision
from textcount import draw_box_for_contrast

def contrastOfAllWords(wordData):
    sum_ = 0
    count = 0
    for word in wordData:
        try:
            contrastOfWord = word[1]
            sum_ += contrastOfWord
            count += 1
        except:
            pass
    contrastOfImage = round(sum_/count,2)
    return (wordData, contrastOfImage)


def contrastOfWord(img):
    return round(img.std())

def get_text_contrast(image_file):
    charSet = set()
    wordData = []
    word_bounds = []
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []

    with io.open(image_file, "rb") as image_file_object:
        content = image_file_object.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    check = cv2.imread(image_file_object.name,cv2.IMREAD_GRAYSCALE)
    check_for_word = cv2.imread(image_file_object.name)
    shutil.rmtree("./static/images/characters")
    os.mkdir("./static/images/characters")

    for page in document.pages: 
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    w = ""
                    for symbol in word.symbols:
                   
                    # print(word.bounding_box.vertices[0].x)
                    # print("\n\n\n")
                        pts = np.array(  [ 
                        [symbol.bounding_box.vertices[0].x,
                        symbol.bounding_box.vertices[0].y],
                        [symbol.bounding_box.vertices[1].x,
                        symbol.bounding_box.vertices[1].y],
                        [symbol.bounding_box.vertices[2].x,
                        symbol.bounding_box.vertices[2].y],
                        [symbol.bounding_box.vertices[3].x,
                        symbol.bounding_box.vertices[3].y]
                        ],
                        np.int32)
                        
                        min_x = min(
                            symbol.bounding_box.vertices[0].x,
                            symbol.bounding_box.vertices[1].x,
                            symbol.bounding_box.vertices[2].x,
                            symbol.bounding_box.vertices[3].x,
                            
                        )
                        max_x = max(
                            symbol.bounding_box.vertices[0].x,
                            symbol.bounding_box.vertices[1].x,
                            symbol.bounding_box.vertices[2].x,
                            symbol.bounding_box.vertices[3].x,
                        )


                        min_y = min(
                            symbol.bounding_box.vertices[0].y,
                            symbol.bounding_box.vertices[1].y,
                            symbol.bounding_box.vertices[2].y,
                            symbol.bounding_box.vertices[3].y,
                            
                        )
                        max_y = max(
                            symbol.bounding_box.vertices[0].y,
                            symbol.bounding_box.vertices[1].y,
                            symbol.bounding_box.vertices[2].y,
                            symbol.bounding_box.vertices[3].y,
                            
                        )
                        cropped_image = check[min_y:max_y,min_x:max_x] # Slicing to crop the image
                    
                        # try:      
                            # cropped_image = cv2.Sobel(cropped_image,cv2.CV_64F,1,1,ksize=5)
                        w += symbol.text
                        cv2.imwrite(f"./static/images/characters/{symbol.text}.jpg",cropped_image)
                        charSet.add(symbol.text)
                        # except Exception as e:
                        #     print("HEEREHEEEEHIOEHWEIOHEW\n\n\n")
                        #     print(e)
                        # pts = pts.reshape((-1, 1, 2))
                        # check = cv2.polylines(check, [pts],True, (0, 0,0), 5)
                    print(w)
                    word_bound = word.bounding_box
                    # word_box_points = [[word_bound.vertices[0].x, word_bound.vertices[0].y], [word_bound.vertices[2].x, word_bound.vertices[2].y]]
                    # word_key = word_bound.text + "@=" + str(hex(random.getrandbits(128)))
                    word_contrast = contrastOfWord(check_for_word[word_bound.vertices[0].y:word_bound.vertices[2].y, word_bound.vertices[0].x:word_bound.vertices[2].x])
                    word_bounds.append([word_bound, word_contrast])   
                    wordData.append((w, word_contrast))        
    
    result_image = draw_box_for_contrast(image_file, word_bounds)
    result_image.save('./static/images/sampleAnswerConstrast.jpg')

    return contrastOfAllWords(wordData)