from base64 import b64encode
from os import makedirs
import json
import requests
import os
from os.path import join, basename
import time

def make_image_data_list(image_filenames, language):
    """
    image_filenames is a list of filename strings
    Returns a list of dicts formatted as the Vision API
        needs them to be
    """
    img_requests = []
    for imgname in image_filenames:
        with open(imgname, 'rb') as f:
            ctxt = b64encode(f.read()).decode()
            img_requests.append({
                    'image': {'content': ctxt},
                    'features': [{
                        'type': 'DOCUMENT_TEXT_DETECTION',
                        'maxResults': 10
                    }],
                    "imageContext": {"languageHints": [language]}
            })
    return img_requests


def make_image_data(image_filenames, language):
    """Returns the image data lists as bytes"""
    imgdict = make_image_data_list(image_filenames, language)
    return json.dumps({"requests": imgdict }).encode()


def request_ocr(api_key, image_filenames, language):
    response = requests.post(ENDPOINT_URL,
                             data=make_image_data(image_filenames, language),
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})
    return response


def Textonly(response):
    loadtext = json.loads(response.text)
    if not 'fullTextAnnotation' in (loadtext[['responses'][0]][0]):
        text = []
        loadtext = []
        print("OCR retuns empty..........")
    else:
        text = loadtext['responses'][0]['fullTextAnnotation']['text']
    return text,loadtext


def google_ocr_entry(api_key,image_filenames,output_path,language):
    jresponse = []
    ocr_text = []
    try:
        response = request_ocr(api_key, [image_filenames],language)
        if response.status_code == 200:
            jsfile = os.path.splitext(basename(image_filenames))[0]
            jpath = join(output_path, basename(jsfile) + '_ocr.json')
            with open(jpath, 'w') as f:
                datatxt = json.dumps(response.json(), indent=2)

                f.write(datatxt)
            try:
                ocr_text, jresponse = Textonly(response)
            except:
                print("error")
    except:
        print("no response")

    return ocr_text,jresponse


PATH_TO_TEST_IMAGES_DIR = r'C:\Users\amarsr01\Desktop\workspace\rnd\semantic-topline\Mask_RCNN\test'
TEST_IMAGE_PATHS2 = []
# ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
ENDPOINT_URL = 'https://vision.googleapis.com/v1p1beta1/images:annotate'

for filepath in os.listdir(PATH_TO_TEST_IMAGES_DIR):
    if filepath.endswith('.jpg'):
        file_ocr = os.path.join(PATH_TO_TEST_IMAGES_DIR, filepath)
        TEST_IMAGE_PATHS2.append(file_ocr)

for image_path in TEST_IMAGE_PATHS2:
    start = time.time()
    print('File name: ' + basename(image_path))
    jpath = join(PATH_TO_TEST_IMAGES_DIR, basename(image_path)[:-4] + '_ocr.json')
    if not os.path.exists(jpath):
        print("...Creating Google OCR output json file{}".format(jpath))
        ocr_text, jresponse = google_ocr_entry(
            '********************************', image_path, PATH_TO_TEST_IMAGES_DIR, 'en')
    else:
        print("Google OCR output json file already exits {}".format(jpath))
    print("Process time: ................" + str(time.time() - start))






