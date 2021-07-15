from django import forms
from django.db.models.enums import Choices
from django.forms import fields, ModelChoiceField
from django.conf import settings
from django.conf.urls.static import static
from .models import *

import os

import pathlib

dirname = pathlib.Path(__file__).resolve().parent

class StyleImgChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.image_theme()

class SrcImgForm(forms.Form):
    
    # print(CHOICES)
    src_img = forms.ImageField(label='Source Image')
    selection = StyleImgChoiceField(queryset = StyleImg.objects.all().filter(model__name = 'stargan') )

    class Meta:
        model = InputImg
        fields = ['src_img']


class SimSwapForm(forms.Form):

    CHOICES = []
    
    src_img = forms.ImageField(label='Source Image')
    selection = StyleImgChoiceField(queryset = StyleImg.objects.all().filter(model__name = 'simswap') )

    class Meta:
        model = InputImg
        fields = ['src_img']

class AllTransferForm(forms.Form):

    CHOICES = []
    
    src_img = forms.ImageField(label='Source Image')
    selection = ModelChoiceField( queryset = Theme.objects.all().distinct() )

    class Meta:
        model = InputImg
        fields = ['src_img']