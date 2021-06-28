from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

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

def predict_using_local(request, sid, rid):
    sourcepath = str(dirname.parent) + "/resource/"
    src_path = sourcepath + "/src/"
    ref_path = sourcepath + "/ref/"

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

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id, input_img, style_id = data['session_id'], data['img'], data['style_id']

        ref_path = str(dirname.parent) + "/resource/ref/" + str(style_id) + ".jpg"
        ref = getBase64stringforImage(ref_path)

        msg = {'src_img': input_img, 'ref_img': ref, 'ref_class': 'female', 'align_face': False}

        json_data = json.dumps(msg)
        headers = {'content-type': 'application/json'}

        #predictionURL = "https://7cc1981e-f1fd-4e64-9836-03183317add0.mock.pstmn.io"
        predictionURL = "http://10.2.117.32:5000"

        try:
            r = requests.post(url = predictionURL + '/predict', data = json_data, headers = headers)

            pic = BytesIO()
            image_string = r.json()['output_img']
            
            response = json.dumps({"output_img": image_string})

            return HttpResponse(response, content_type='application/json'
                                ,status=200)
        except Exception as e:
            print(e)
            error = json.dumps({"Error": str(e)})
            return HttpResponse(error, content_type='application/json'
                                ,status=503)

@csrf_exempt
def predict_demo(request):

    ref_path = str(dirname.parent) + "/resource/ref/"
    # images = {
    #     'latest_question_list': latest_question_list,
    # }
    context = {}
    return render(request, 'styletransfer/predict.html', context)

def getBase64stringforImage(img):
    with Image.open(img) as image_file:
        buffered = BytesIO()
        image_file.save(buffered, format="JPEG")
        image_bytes = base64.b64encode(buffered.getvalue())
        return image_bytes.decode("utf-8")