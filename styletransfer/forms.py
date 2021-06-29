from django import forms
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

    ref_path = str(dirname) + "/static/styletransfer"
    CHOICES = []
    cnt = 1

    for file in os.listdir(ref_path):
        if file.endswith(".jpg"):
            CHOICES.append((cnt, int(file.split('.')[0])))
            cnt += 1

    src_img = forms.ImageField(label='src-img')
    selection = forms.ChoiceField(label='select reference', choices=CHOICES)

# class RefForm(forms.Form):
#     id = forms.CharField()
#     img = forms.ImageField()
#     selection = forms.ChoiceField(choices=id, widget=forms.RadioSelect)
