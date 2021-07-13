from django import forms
from django.db.models.enums import Choices
from django.forms import fields
from django.conf import settings
from django.conf.urls.static import static
from .models import *

import os

import pathlib

dirname = pathlib.Path(__file__).resolve().parent
# class SrcImgForm(forms.ModelForm):

#     class Meta:
#         model = SrcImg
#         fields = ['src_img']

class SrcImgForm(forms.Form):

    #ref_path = str(dirname) + "/static/styletransfer"
    CHOICES = []
    
    style_img_list = StyleImg.objects.all().filter(model__name = 'stargan')

    for style_img in style_img_list:
        # print(style_img.image_name(), style_img.model, type(style_img.model))
        CHOICES.append(( style_img.id, style_img.image_name() ))
    
    # print(CHOICES)
    src_img = forms.ImageField(label='Source Image')
    selection = forms.ChoiceField(label='Select Reference', choices=CHOICES)

    class Meta:
        model = InputImg
        fields = ['src_img']


class SimSwapForm(forms.Form):

    CHOICES = []
    
    style_img_list = StyleImg.objects.all().filter(model__name = 'simswap')

    for style_img in style_img_list:
        CHOICES.append(( style_img.id, style_img.image_name() ))
    
    src_img = forms.ImageField(label='Source Image')
    selection = forms.ChoiceField(label='Select Reference', choices=CHOICES)

    class Meta:
        model = InputImg
        fields = ['src_img']

    # ref_path = str(dirname) + "/static/templates"
    # CHOICES = []
    # cnt = 1

    # for file in os.listdir(ref_path):
    #     if file.endswith(".jpg"):
    #         CHOICES.append((file.split('.')[0], file.split('.')[0]))
    #         cnt += 1

    # src_img = forms.ImageField(label='Source Image')
    # selection = forms.ChoiceField(label='Select Reference', choices=CHOICES)