from django.db import models

# Create your models here.
class SrcImg(models.Model):
    #name = models.CharField(max_length=20)
    src_img = models.ImageField(upload_to='images/')