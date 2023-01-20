from flask import Flask, render_template, flash, request
from findcontrast import get_text_contrast
import os
from theme import find_theme_of_image
from text_to_area import find_ratio_of_text_to_area
# from detect_image import localize_objects
from textcount import get_document_bounds
from object_detection_new import object_detect_api
from textblob import TextBlob
# from nltk.corpus import words as corpa
# from nltk.metrics.distance import jaccard_distance
# from nltk.util import ngrams  


app = Flask(__name__)



UPLOAD_FOLDER = './static/images/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'some secret key here'


def get_uploaded_image_path():
	return os.path.join(app.config['UPLOAD_FOLDER'], 'uploadedImage.jpg')

@app.route('/textContrast', methods=[ 'POST'])
def find_contrast():
    file = request.files['formFile']
    file.save(get_uploaded_image_path())
    flash('Image uploaded!')
    main_data, total_data = get_text_contrast(get_uploaded_image_path())
    return render_template('contrast.html',data = {
        'imageContrast' : total_data,
        'characters' : main_data,
        'image' : './static/images/sampleAnswerConstrast.jpg'

    })



@app.route('/centerToTextArea', methods=[ 'POST'])
def theme_of_image():
    file = request.files['formFile']
    file.save(get_uploaded_image_path())
    flash('Image uploaded!')
    data = find_theme_of_image(get_uploaded_image_path())
    return render_template('center.html',data = {
        'image' : "./static/images/divided_image.jpeg",
        'ratio_value' : round(100*data,2)
    })


@app.route('/textAreaToCompositionAreaRatio',methods = ['POST'])
def textualArea():
    
    file = request.files['formFile']
    file.save(get_uploaded_image_path())
    flash('Image uploaded!')
    data = find_ratio_of_text_to_area(get_uploaded_image_path())
    score = 10 - (abs(round(100*data,2) - 30)/30)*10
    return render_template('textualArea.html',data = {
        'ratio_value' : round(100*data,2),
        'score' : score
    })


@app.route('/objectCount',methods = ['POST'])
def objectCounts():
    file = request.files['formFile']
    file.save(get_uploaded_image_path())
    flash('Image uploaded!')
    data1 = object_detect_api(get_uploaded_image_path())
    score = 10 - (abs(len(data1) - 5)/5)*10
    
    return render_template('objects.html',data = {
        'object_count' : len(data1),
        'score' : score, 
        'image' : './static/images/objects_classified.jpg',
        'objects' : data1,
    })

@app.route('/textLimit', methods = ['POST'])
def find_words():
    file = request.files['formFile']
    file.save(get_uploaded_image_path())
    flash('Image uploaded!')
    words, theme = get_document_bounds(get_uploaded_image_path())
    score = 10 - (abs(50 - len(words))/50)*10
    
    corrections = []
    # correct_words = corpa.words()
    for word in words:
        org_word = word
        corrected_word = TextBlob(org_word).correct()
        if org_word != corrected_word:
            corrections.append(
                {
                    'Original Word' : org_word,
                    'Corrected Word' : corrected_word
                }
            )

    return render_template('textLimit.html',data = {
        'word_count' : len(words),
        'words' : words,
        'image' : './static/images/words_with_boxes.jpg',
        'theme' : theme,
        'corrections' : corrections,
        'score' : score

    })


@app.route('/')
def hello_world():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=8000)