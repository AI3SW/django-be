from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone

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
simswapURL = "http://10.2.117.32:5001"

#hardcode info first TBC move to db
# gender_info = {'1':'female', '2':'male', '3':'female', '4':'female'}
# ref_src_reverse = ['1']
connect_to_db = True

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

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id, raw_src_img, style_id = data['session_id'], data['img'], data['style_id']

        if connect_to_db:
            src = base64_to_image(raw_src_img)
            new_src_img = InputImg(file_path = src, create_date = timezone.now())
            new_src_img.save()

        style_img = get_object_or_404(StyleImg, pk=int(style_id))
        ref = image_to_base64(style_img.file_path)

        if not style_img.is_ref:
            raw_src_img, ref = ref, raw_src_img

        msg = {'src_img': raw_src_img, 'ref_img': ref, 'ref_class': style_img.ref_class, 'align_face': True}
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
def predict_stargan_demo(request):

    result = ''

    if request.method == 'POST':
        form = SrcImgForm(request.POST, request.FILES)

        if form.is_valid():
            src = form.cleaned_data['src_img']

            if connect_to_db:
                new_src_img = InputImg(file_path = src, create_date = timezone.now())
                new_src_img.save()

            #print(type(src_img.file))
            img_bytes = base64.b64encode(src.file.getvalue())
            src_img = img_bytes.decode("utf-8")
            # return redirect('success')

            style_id = form.cleaned_data['selection']

            style_img = get_object_or_404(StyleImg, pk=int(style_id))
            #style_img = get_object_or_404(StyleImg, image_name = style_name, pk=1)
            ref = image_to_base64(style_img.file_path)

            if not style_img.is_ref:
                src_img, ref = ref, src_img

            msg = {'src_img': src_img, 'ref_img': ref, 'ref_class': style_img.ref_class, 'align_face': True}

            json_data = json.dumps(msg)
            headers = {'content-type': 'application/json'}

            with requests.Session() as s:
                try:
                    r = s.post(url = predictionURL + '/predict', data = json_data, headers = headers)
                    image_string = r.json()['output_img']
                    result = image_string
                    # response = json.dumps({"output_img": image_string})

                except Exception as e:
                    print('Error: ', e)

    else:
        form = SrcImgForm()

    references = []

    style_img_list = StyleImg.objects.all().filter(model__name = 'stargan')

    for style_img in style_img_list:
        item = {'title':style_img.image_name, 'path':style_img.file_path}
        references.append(item)

    return render(request, 'styletransfer/predict.html', {'references':references, 'form':form, 'result':result})

@csrf_exempt
def predict_simswap_demo(request):
    result = ''

    if request.method == 'POST':
        form = SimSwapForm(request.POST, request.FILES)

        if form.is_valid():
            src = form.cleaned_data['src_img']

            if connect_to_db:
                new_src_img = InputImg(file_path = src, create_date = timezone.now())
                new_src_img.save()

            img_bytes = base64.b64encode(src.file.getvalue())
            src_img = img_bytes.decode("utf-8")

            style_id = form.cleaned_data['selection']
            style_img = get_object_or_404(StyleImg, pk=int(style_id))
            ref = image_to_base64(style_img.file_path)

            if not style_img.is_ref:
                src_img, ref = ref, src_img

            msg = {'src_img': src_img, 'ref_img': ref}

            json_data = json.dumps(msg)
            headers = {'content-type': 'application/json'}

            with requests.Session() as s:
                try:
                    r = s.post(url = simswapURL + '/predict', data = json_data, headers = headers)
                    image_string = r.json()['output_img']
                    result = image_string
                    # response = json.dumps({"output_img": image_string})

                except Exception as e:
                    print('Error: ', e)

    else:
        form = SimSwapForm()

    references = []

    style_img_list = StyleImg.objects.all().filter(model__name = 'simswap')

    for style_img in style_img_list:
        item = {'title':style_img.image_name, 'path':style_img.file_path}
        references.append(item)

    return render(request, 'styletransfer/predict.html', {'references':references, 'form':form, 'result':result})