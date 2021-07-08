from django.db import models

# Create your models here.
class SrcImg(models.Model):
    #name = models.CharField(max_length=20)
    file_path = models.ImageField(upload_to='images/input/')

    class Meta:
        managed = False
        db_table = 'input_img'

class Job(models.Model):
    session_id = models.CharField(max_length=20, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    style_img = models.ForeignKey('StyleImg', models.DO_NOTHING, blank=True, null=True)
    input_img_id = models.IntegerField(blank=True, null=True)
    output_img_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'job'


class StyleImg(models.Model):
    #file_path = models.CharField(max_length=125, blank=True, null=True)
    file_path = models.ImageField(upload_to='images/style/')
    is_ref = models.BooleanField(blank=True, null=True)
    ref_class = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'style_img'

class OutputImg(models.Model):
    file_path = models.CharField(max_length=125, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'output_img'