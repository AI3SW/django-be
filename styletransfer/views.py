from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import base64
import json
import requests

from PIL import Image
from io import BytesIO

import pathlib
dirname = pathlib.Path(__file__).resolve().parent
# Create your views here.

def index(request):
    return HttpResponse("Hello, this is index.")

def predict(request, sid, rid):
    sourcepath = str(dirname.parent) + "\\resource\\"
    src_path = sourcepath + "\\src\\"
    ref_path = sourcepath + "\\ref\\"

    src = getBase64stringforImage(src_path + str(sid) +".jpg")
    ref = getBase64stringforImage(ref_path + str(rid) +".jpg")
    msg = {'src_img': src, 'ref_img': ref, 'ref_class': 'female', 'align_face': False}
    #print(msg)
    json_data = json.dumps(msg)
    headers = {'content-type': 'application/json'}

    #predictionURL = "https://7cc1981e-f1fd-4e64-9836-03183317add0.mock.pstmn.io"
    predictionURL = "http://10.2.117.32:5000"
    r = requests.post(url = predictionURL + '/predict', data = json_data, headers = headers)

    pic = BytesIO()
    image_string = BytesIO(base64.b64decode(r.json()['output_img']))
    image = Image.open(image_string)
    image.save(pic, image.format, quality=100)
    pic.seek(0)
    return HttpResponse(pic, content_type='image/jpeg')

    #return HttpResponse(r.json()['output_img'], content_type='image/jpeg')


def getBase64stringforImage(img):
    with Image.open(img) as image_file:
        buffered = BytesIO()
        image_file.save(buffered, format="JPEG")
        image_bytes = base64.b64encode(buffered.getvalue())
        return image_bytes.decode("utf-8")