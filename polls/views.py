from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import *

import json

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def get_questions(request):
    question_list = Question.objects.order_by('id')

    output = {'questions':[]}
    for q in question_list:
        item = {}
        item['id'] = q.id
        item['text'] = q.text

        optionlist = Option.objects.filter(question = q)
        if optionlist:
            item['options'] = []
            for op in optionlist:
                opitem = {}
                opitem['id'] = op.id
                opitem['text'] = op.text
                opitem['weight'] = str(op.weight)
                item['options'].append(opitem)

        output['questions'].append(item)

    response = json.dumps(output)
    return HttpResponse(response, content_type='application/json'
                                ,status=200)

@csrf_exempt
def post_result(request):
    if request.method == 'POST':
        incoming_data = json.loads(request.body)
        session_id = incoming_data['session_id']
        #question_list = incoming_data['question_list']
        option_list = incoming_data['option_list']
    
    n = len(option_list)

    for i in range(n):

        optionitem = Option.objects.filter(id = int(option_list[i]))
        
        if optionitem:
            result_item = Result(session_id = session_id,
            option_id = optionitem, sequence_id = i )

            result_item.save()
    
    return HttpResponse(status = 200)