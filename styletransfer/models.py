from django.db import models
import os

# Create your models here.
class InputImg(models.Model):
    #name = models.CharField(max_length=20)
    file_path = models.ImageField(upload_to='images/input/')
    create_date = models.DateTimeField(blank=True, null=True)

    def image_name(self):
        return os.path.basename(self.file_path.name).split('.')[0]
    
    def __str__(self) -> str:
        return os.path.basename(self.file_path.name)

    class Meta:
        managed = True
        db_table = 'input_img'

class Job(models.Model):
    session = models.CharField(max_length=20, blank=True, null=True)
    status = models.SmallIntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    style_img = models.ForeignKey('StyleImg', models.DO_NOTHING, blank=True, null=True)
    input_img = models.ForeignKey('InputImg', models.DO_NOTHING, blank=True, null=True)
    output_img = models.ForeignKey('OutputImg', models.DO_NOTHING, blank=True, null=True)

    def __str__(self) -> str:
        return self.session_id

    class Meta:
        managed = True
        db_table = 'job'


class StyleImg(models.Model):
    #file_path = models.CharField(max_length=125, blank=True, null=True)
    file_path = models.ImageField(upload_to='images/style/')
    model = models.ForeignKey('Model', models.DO_NOTHING, blank=True, null=True)
    is_ref = models.BooleanField(blank=True, null=True)
    ref_class = models.CharField(max_length=10, blank=True, null=True)

    def image_name(self):
        return os.path.basename(self.file_path.name).split('.')[0]
    
    def image_model(self):
        return self.model.name
    
    def __str__(self) -> str:
        return os.path.basename(self.file_path.name)

    class Meta:
        managed = True
        db_table = 'style_img'

class OutputImg(models.Model):
    #file_path = models.CharField(max_length=125, blank=True, null=True)
    file_path = models.ImageField(upload_to='images/result/')
    create_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return os.path.basename(self.file_path.name)

    class Meta:
        managed = True
        db_table = 'output_img'

class Model(models.Model):
    #file_path = models.CharField(max_length=125, blank=True, null=True)
    name = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        managed = True
        db_table = 'model'