# Rad-Ads-Model 🏣➕

## Description : 


1. <b>Text Contrast : 🎛️ </b>
For this we will firstly change the text to the grey scale. Now that all the pixels will
have intensity ranging from 0-255. Then we will extract the background color near to the font
and compare it with text's mean intensity. We will compare this contrast ratio with our
recommended contrast ratio to remove bad ADs.

2. <b>Text Limit : 💯</b>
Google Cloud Vision’s text detection API returns info related to all the text segments in the
image, separately, in the form of an Array where length of the array is the word count.

3. <b> Text to Composition Area Ratio : 🔢 </b>
Google's Cloud Vision’s text detection API returns the coordinates of the polynomial of each
text blob found in the image. We will calculate the combined area of all text using Shoelace
formula and compare it with the image's dimensions . We will compare the ratio of area of
text with the complete image.

4. <b> Layout : 🟥 </b>
We will segment the image into sections to identify the primary message area, and primary
image area. If text’s coordinates lie within the primary message area then we will check if the
text is primary, if not-found we will discard the image.
We will need more knowledge about the characteristics of the principal object to classify it.


5. <b> Object Count : 📖 </b>
To identify the number of objects we will use Google Cloud Vision’s Object localization API [4].
It works on both the physical world and animated objects.

## Tech Stack 💻
<br>

<p align="left"> <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a> <a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a> <a href="https://cloud.google.com" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/google_cloud/google_cloud-icon.svg" alt="gcp" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://opencv.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/opencv/opencv-icon.svg" alt="opencv" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>

<br>

## Installation and Setup for Windows 🎛️

1. Install latest version of python from their official website.
2. Create a GCP account. Then, select enable the cloud vision API and get all the desired keys. (This step is not required if the mentioned API key in project is working).
3. Change the API keys in reddys-rad-ads-859d5b1496fa.json file.
4. Go to the project folder and run the following commands.

```
pip install virtualenv
virtualenv venv
.\venv\Scripts\activate.ps1

pip install -r requirements.txt
py app.py  
```

5. This will run a flask server at http://localhost:8000
6. You are good to go !

## Screenshots of the application


Home Page            |  Center Textual Area Statistics
:-------------------------:|:-------------------------:
![](/screenshots/home.png)  |  ![](/screenshots/center_to_text.png)


Text Contrast Statistics            |  Object Count Details
:-------------------------:|:-------------------------:
![](/screenshots/contrast.png)  |  ![](/screenshots/objects.png)

Text to Composition Area Statistics           |  Word Count Details
:-------------------------:|:-------------------------:
![](/screenshots/text_composition.png)  |  ![](/screenshots/text_count.png)






## Built by </>
## Built with ❤️

