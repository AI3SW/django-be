from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import glob, os
import base64
import json
import requests

from PIL import Image
from io import BytesIO

from .forms import *
from .utils import *
from .models import *

import pathlib

dirname = pathlib.Path(__file__).resolve().parent

#predictionURL = "https://7cc1981e-f1fd-4e64-9836-03183317add0.mock.pstmn.io"
predictionURL = "http://10.2.117.32:5000"

#hardcode info first TBC move to db
gender_info = {'1':'female', '2':'male', '3':'female', '4':'female'}
ref_src_reverse = ['1']
connect_to_db = False

# Create your views here.

def index(request):
    return HttpResponse("Hello, this is index.")

def get_style(request):

    ref_path = str(dirname) + "/static/styletransfer"
    styles = []

    for file in os.listdir(ref_path):
        if file.endswith(".jpg"):
            img_str = image_to_base64(ref_path+'/'+file)
            item = {'style_id':int(file.split('.')[0]), 'style_img':img_str}
            styles.append(item)
    
    response = json.dumps({"styles":styles})
    return HttpResponse(response, content_type='application/json'
                                ,status=200)

def predict_using_local(request, sid, style_id):
    sourcepath = str(dirname) + "/resource/"
    src_path = sourcepath + "/src/"
    ref_path = sourcepath + "/ref/"

    src_img = image_to_base64(src_path + str(sid) +".jpg")
    ref = image_to_base64(ref_path + str(style_id) +".jpg")

    if str(style_id) in ref_src_reverse:
        src_img, ref = ref, src_img

    msg = {'src_img': src_img, 'ref_img': ref, 'ref_class': gender_info[str(style_id)], 'align_face': True}
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
        session_id, src_img, style_id = data['session_id'], data['img'], data['style_id']

        # ref_path = str(dirname) + "/static/styletransfer/" + str(style_id) + ".jpg"
        # ref = image_to_base64(ref_path)

        # if str(style_id) in ref_src_reverse:
        #     src_img, ref = ref, src_img

        style_img = get_object_or_404(StyleImg, pk=int(style_id))
        ref = image_to_base64(style_img.file_path)

        if not style_img.is_ref:
            src_img, ref = ref, src_img

        msg = {'src_img': src_img, 'ref_img': ref, 'ref_class': gender_info[str(style_id)], 'align_face': True}
        #print(msg)
        json_data = json.dumps(msg)
        headers = {'content-type': 'application/json'}

        with requests.Session() as s:
            try:
                r = s.post(url = predictionURL + '/predict', data = json_data, headers = headers)

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
            src = form.cleaned_data['src_img']
            #print(type(src_img.file))
            img_bytes = base64.b64encode(src.file.getvalue())
            src_img = img_bytes.decode("utf-8")
            # return redirect('success')

            style_id = form.cleaned_data['selection']

            style_img = get_object_or_404(StyleImg, pk=int(style_id))
            ref = image_to_base64(style_img.file_path)

            if not style_img.is_ref:
                src_img, ref = ref, src_img

            msg = {'src_img': src_img, 'ref_img': ref, 'ref_class': gender_info[str(style_id)], 'align_face': True}

            json_data = json.dumps(msg)
            headers = {'content-type': 'application/json'}

            with requests.Session() as s:
                try:
                    r = s.post(url = predictionURL + '/predict', data = json_data, headers = headers)
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
    
    #print(references)
    return render(request, 'styletransfer/predict.html', {'references':references, 'form':form, 'result':result})