from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import glob, os
import base64
import json
import requests

from PIL import Image
from io import BytesIO

from .forms import *

import pathlib

dirname = pathlib.Path(__file__).resolve().parent

#predictionURL = "https://7cc1981e-f1fd-4e64-9836-03183317add0.mock.pstmn.io"
predictionURL = "http://10.2.117.32:5000"

# Create your views here.

def index(request):
    return HttpResponse("Hello, this is index.")

def get_style(request):

    ref_path = str(dirname) + "/static/styletransfer"
    styles = []

    for file in os.listdir(ref_path):
        if file.endswith(".jpg"):
            img_str = getBase64stringforImage(ref_path+'/'+file)
            item = {'style_id':int(file.split('.')[0]), 'style_img':img_str}
            styles.append(item)
    
    response = json.dumps({"styles":styles})
    return HttpResponse(response, content_type='application/json'
                                ,status=200)

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

    r = requests.post(url = predictionURL + '/predict', data = json_data, headers = headers)

    pic = BytesIO()
    image_string = BytesIO(base64.b64decode(r.json()['output_img']))
    image = Image.open(image_string)
    image.save(pic, image.format, quality=100)
    pic.seek(0)
    return HttpResponse(pic, content_type='image/jpeg', status=200)

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id, input_img, style_id = data['session_id'], data['img'], data['style_id']

        ref_path = str(dirname) + "/static/styletransfer/" + str(style_id) + ".jpg"
        ref = getBase64stringforImage(ref_path)

        msg = {'src_img': input_img, 'ref_img': ref, 'ref_class': 'female', 'align_face': False}

        json_data = json.dumps(msg)
        headers = {'content-type': 'application/json'}

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

    result = ''

    if request.method == 'POST':
        form = SrcImgForm(request.POST, request.FILES)

        if form.is_valid():
            src_img = form.cleaned_data['src_img']
            print(type(src_img.file))
            img_bytes = base64.b64encode(src_img.file.getvalue())
            img_str = img_bytes.decode("utf-8")
            # return redirect('success')

            rid = form.cleaned_data['selection']

            ref_path = str(dirname) + "/static/styletransfer/"
            ref = getBase64stringforImage(ref_path + str(rid) +".jpg")
            msg = {'src_img': img_str, 'ref_img': ref, 'ref_class': 'female', 'align_face': False}

            json_data = json.dumps(msg)
            headers = {'content-type': 'application/json'}

            try:
                r = requests.post(url = predictionURL + '/predict', data = json_data, headers = headers)
                image_string = r.json()['output_img']
                result = image_string
                # response = json.dumps({"output_img": image_string})

            except Exception as e:
                print(e)

    else:
        form = SrcImgForm()

    ref_path = str(dirname) + "/static/styletransfer"
    references = []

    for file in os.listdir(ref_path):
        if file.endswith(".jpg"):
            item = {'title':file, 'path':'styletransfer/'+file}
            references.append(item)

    return render(request, 'styletransfer/predict.html', {'references':references, 'form':form, 'result':result})

def getBase64stringforImage(img):
    with Image.open(img) as image_file:
        buffered = BytesIO()
        image_file.save(buffered, format="JPEG")
        image_bytes = base64.b64encode(buffered.getvalue())
        return image_bytes.decode("utf-8")