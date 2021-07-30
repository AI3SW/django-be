import base64
import json
import logging
import pathlib
from io import BytesIO

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *
from .utils import *

logger = logging.getLogger(__name__)

dirname = pathlib.Path(__file__).resolve().parent

# if need to connect to db
connect_to_db = settings.CONNECT_TO_DB

# Create your views here.

def index(request):
    return HttpResponse("Hello, this is index.")

def get_style(request):
    styles = []

    style_list = StyleImg.objects.all()

    for style_img in style_list:

        item = {}
        item['style_id'] = style_img.id
        item['style_img'] = image_to_base64(style_img.file_path)
        item['style_theme'] = style_img.image_theme()
        item['model'] = style_img.image_model()
        styles.append(item)

    response = json.dumps({"styles":styles})
    return HttpResponse(response, content_type='application/json'
                                ,status=200)

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id, raw_src_img, style_id = data['session_id'], data['img'], data['style_id']
        logging.info(f"Predicting style_id: {style_id} for session id: {session_id}")
        
        if connect_to_db:
            storeImageIntoDB(InputImg, raw_src_img)

        style_img = get_object_or_404(StyleImg, pk=int(style_id))
        ref = image_to_base64(style_img.file_path)

        if not style_img.is_ref:
            raw_src_img, ref = ref, raw_src_img
        
        if style_img.image_model() == 'stargan':
            msg = {'src_img': raw_src_img, 'ref_img': ref, 'ref_class': style_img.ref_class, 'align_face': True}

        elif style_img.image_model() == 'simswap':
            msg = {'src_img': raw_src_img, 'ref_img': ref}
        
        else:
            e = "Unsupported model"
            error = json.dumps({"Error": str(e)})
                
            return HttpResponse(error, content_type='application/json'
                                ,status=503)

        json_data = json.dumps(msg)
        headers = {'content-type': 'application/json'}

        dest = settings.PREDICTION_MODEL_URL[style_img.image_model()]
        targetURL = dest['HOST'] + ':' + dest['PORT'] + '/' + dest['ENDPOINT']

        with requests.Session() as s:
            try:
                response = s.post(url=targetURL, data=json_data,
                                  headers=headers).json()

                if 'error' in response:
                    logging.error(response['error'])
                    error = json.dumps({'error': response['error']})
                    return HttpResponse(error, content_type='application/json',
                                        status=503)

                image_string = response['output_img']

                if connect_to_db:
                    storeImageIntoDB(OutputImg, image_string)

                response = json.dumps({"output_img": image_string})

                return HttpResponse(response, content_type='application/json', status=200)
            except Exception as e:
                logging.error(e)
                error = json.dumps({"Error": str(e)})

                return HttpResponse(error, content_type='application/json', status=503)

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

            img_bytes = base64.b64encode(src.file.getvalue())
            src_img = img_bytes.decode("utf-8")
            # return redirect('success')

            style_img = form.cleaned_data['selection']

            #style_img = get_object_or_404(StyleImg, pk=int(style_id))
            #style_img = get_object_or_404(StyleImg, image_name = style_name, pk=1)
            ref = image_to_base64(style_img.file_path)

            if not style_img.is_ref:
                src_img, ref = ref, src_img

            msg = {'src_img': src_img, 'ref_img': ref, 'ref_class': style_img.ref_class, 'align_face': True}

            json_data = json.dumps(msg)
            headers = {'content-type': 'application/json'}

            dest = settings.PREDICTION_MODEL_URL[style_img.image_model()]
            targetURL = dest['HOST'] + ':' + dest['PORT'] + '/' + dest['ENDPOINT']

            with requests.Session() as s:
                try:
                    r = s.post(url = targetURL, data = json_data, headers = headers)
                    image_string = r.json()['output_img']
                    result = image_string

                    if connect_to_db:
                        storeImageIntoDB(OutputImg, image_string)

                except Exception as e:
                    logging.error(e)

    else:
        form = SrcImgForm()

    references = []

    style_img_list = StyleImg.objects.all().filter(model__name = 'stargan')
    
    for style_img in style_img_list:
        item = {'title':style_img.image_theme(), 'path':style_img.file_path}
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

            style_img = form.cleaned_data['selection']
            #style_img = get_object_or_404(StyleImg, pk=int(style_id))
            ref = image_to_base64(style_img.file_path)

            if not style_img.is_ref:
                src_img, ref = ref, src_img

            msg = {'src_img': src_img, 'ref_img': ref}

            json_data = json.dumps(msg)
            headers = {'content-type': 'application/json'}

            dest = settings.PREDICTION_MODEL_URL[style_img.image_model()]
            targetURL = dest['HOST'] + ':' + dest['PORT'] + '/' + dest['ENDPOINT']

            with requests.Session() as s:
                try:
                    r = s.post(url = targetURL, data = json_data, headers = headers)
                    image_string = r.json()['output_img']
                    result = image_string
                    # response = json.dumps({"output_img": image_string})

                    if connect_to_db:
                        storeImageIntoDB(OutputImg, image_string)

                except Exception as e:
                    logging.error(e)

    else:
        form = SimSwapForm()

    references = []

    style_img_list = StyleImg.objects.all().filter(model__name = 'simswap')

    for style_img in style_img_list:
        item = {'title':style_img.image_theme(), 'path':style_img.file_path}
        references.append(item)

    return render(request, 'styletransfer/predict.html', {'references':references, 'form':form, 'result':result})


@csrf_exempt
def predict_all_demo(request):
    result = []

    if request.method == 'POST':
        form = AllTransferForm(request.POST, request.FILES)

        if form.is_valid():
            src = form.cleaned_data['src_img']

            if connect_to_db:
                new_src_img = InputImg(file_path = src, create_date = timezone.now())
                new_src_img.save()

            img_bytes = base64.b64encode(src.file.getvalue())
            src_img = img_bytes.decode("utf-8")

            theme = form.cleaned_data['selection']
            #style_img = get_object_or_404(StyleImg, pk=int(style_id))
            ref_list = StyleImg.objects.all().filter(theme = theme)

            for style_img in ref_list:
                ref = image_to_base64(style_img.file_path)

                if not style_img.is_ref:
                    src_img, ref = ref, src_img
                
                if style_img.image_model() == 'stargan':
                    msg = {'src_img': src_img, 'ref_img': ref, 'ref_class': style_img.ref_class, 'align_face': True}

                elif style_img.image_model() == 'simswap':
                    msg = {'src_img': src_img, 'ref_img': ref}
                
                else:
                    e = "Unsupported model"
                    logging.error(e)
                    continue

                json_data = json.dumps(msg)
                headers = {'content-type': 'application/json'}

                dest = settings.PREDICTION_MODEL_URL[style_img.image_model()]
                targetURL = dest['HOST'] + ':' + dest['PORT'] + '/' + dest['ENDPOINT']

                with requests.Session() as s:
                    try:
                        r = s.post(url = targetURL, data = json_data, headers = headers)
                        image_string = r.json()['output_img']
                        result.append({'model':style_img.image_model(), 'img': image_string})
                        # response = json.dumps({"output_img": image_string})

                        if connect_to_db:
                            storeImageIntoDB(OutputImg, image_string)

                    except Exception as e:
                        logging.error(e)

    else:
        form = AllTransferForm()
    
    references = []

    style_img_list = StyleImg.objects.all().distinct('theme__name')

    for style_img in style_img_list:
        cur_theme = Theme.objects.get(name = style_img.image_theme())
        models_list = StyleImg.objects.all().filter(theme=cur_theme.id).values_list('model__name', flat=True)
        models = ', '.join(sorted(list(models_list)))
        item = {'title':style_img.image_theme, 'path':style_img.file_path, 'models': models}
        references.append(item)

    return render(request, 'styletransfer/predict_all.html', {'references':references, 'form':form, 'result':result})
