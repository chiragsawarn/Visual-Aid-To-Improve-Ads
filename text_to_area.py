import cv2
from extract_textual_details import get_textual_details


def polygonArea(X, Y, n):
    area = 0.0
    j = n - 1
    for i in range(0,n):
        area += (X[j] + X[i]) * (Y[j] - Y[i])
        j = i  
    return (abs(area / 2.0))



def find_ratio_of_text_to_area(filein):
    X, Y = [],[]
    
    document = get_textual_details(filein)
    for page in document.pages: 
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        for i in range(4):
                            X.append(symbol.bounding_box.vertices[i].x)
                            Y.append(symbol.bounding_box.vertices[i].y)
                        
            
    textual_area = polygonArea(X, Y, len(X))
    matrix = cv2.imread(filein)
    image_area = matrix.shape[0]*matrix.shape[1]
    return textual_area/image_area    