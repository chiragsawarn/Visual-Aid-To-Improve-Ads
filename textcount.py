from extract_textual_details import get_textual_details
import numpy as np
import cv2 
from collections import Counter
import os
from enum import Enum
from PIL import Image, ImageDraw, ImageFont

def draw_box_for_contrast(image_file, word_bounds):
    word_image = Image.open(image_file)
    return draw_boxes(word_image, word_bounds, "yellow", 2, True)


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

# plotting bounding boxes from response
def draw_boxes(image, bounds, color, width=5, contrastMode=False):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        if contrastMode:
            draw.line([
                bound[0].vertices[0].x, bound[0].vertices[0].y,
                bound[0].vertices[1].x, bound[0].vertices[1].y,
                bound[0].vertices[2].x, bound[0].vertices[2].y,
                bound[0].vertices[3].x, bound[0].vertices[3].y,
                bound[0].vertices[0].x, bound[0].vertices[0].y],
                fill=color, 
                width=width)    
            font = ImageFont.truetype("arial.ttf", 22)
            draw.text([bound[0].vertices[2].x, bound[0].vertices[2].y], str(bound[1]), fill="red", font=font)
            continue
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y],
            fill=color, 
            width=width)
    return image

def bound_word(image_file, bounds):
    image = Image.open(image_file)
    result_image = draw_boxes(image, bounds, 'yellow', 2)
    return result_image

def bound_center_text_area(image_file, response, document, theme_words):
    biggest_word = get_max_word_bound(image_file, response, document)
    bounds = [biggest_word]
    # for word in theme_words:
    #     word_bound = find_word_location(document, word)
    #     bounds.append(word_bound)
    return bound_word(image_file, bounds)

def get_bounds(response, feature,document):
    bounds = []
    for i,page in enumerate(document.pages):
        for block in page.blocks:
            if feature==FeatureType.BLOCK:
                bounds.append(block.bounding_box)
            for paragraph in block.paragraphs:
                if feature==FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)
                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)
    return bounds


def find_word_location(document,word_to_find):
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    assembled_word=assemble_word(word)
                    if(assembled_word==word_to_find):
                        return word.bounding_box


def get_bounding_area(bound):
    return abs(bound.vertices[0].x-bound.vertices[2].x) * abs(bound.vertices[0].y-bound.vertices[2].y)


#finding coordinates of the word
def assemble_word(word):
    assembled_word=""
    for symbol in word.symbols:
        assembled_word+=symbol.text
    return assembled_word

def get_max_word_bound(image_file, response, document):
    max_bound_area = 0
    word_bounds = get_bounds(response, FeatureType.WORD, document)
    for bound in word_bounds:
        area = get_bounding_area(bound)
        if area > max_bound_area:
            biggest_word = bound
            max_bound_area = area
    return biggest_word

def get_document_bounds(image_file):
    document = get_textual_details(image_file)
    image1 = cv2.imread(image_file)

    ## Code Snippet to find Word Count in the image
    words = []
    for elem in document.text.split('\n'):
        for el in elem.split():
            words.append(el)
    for page in document.pages: 
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    
                    points = []
                    for i in range(4):
                        points.append(
                            (word.bounding_box.vertices[i].x,
                            word.bounding_box.vertices[i].y)
                            )

                    pts = np.array([[points[0][0],points[0][1]],[points[1][0],points[1][1]],
                    [points[2][0],points[2][1]],[points[3][0],points[3][1]]],np.int32)

                    pts = pts.reshape((-1, 1, 2))
                    image1 = cv2.polylines(image1,[pts] ,True, (0,0,0), 2)
    cv2.imwrite("static/images/words_with_boxes.jpg",image1)
    words, theme_words = get_words_and_theme_words(document, 2)
    return words, theme_words


def get_stop_words():
    stopwords = []
    with open(os.path.join(os.getcwd(), os.path.join('data', 'stopwords.txt'))) as f:
        stopwords = f.readlines()
    stopwords = list(map(lambda word: word.strip().lower(), stopwords))
    return stopwords

def get_words_and_theme_words(document, top_how_many):
    ## Code Snippet to find Word Count in the image
    words = []
    for elem in document.text.split('\n'):
        for el in elem.split():
            words.append(el)
        thisDict = {}
    
    stopwords = get_stop_words()
    for word in words:
        if word.lower() in stopwords:
            continue
        if word in thisDict:
            thisDict[word] += 1
            continue
        thisDict[word] = 1
    theme_words = list(dict(Counter(thisDict).most_common(top_how_many)).keys())
    return words, theme_words

