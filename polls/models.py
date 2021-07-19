# Create your models here.
from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.question_text
    
    class Meta:
        managed = True
        db_table = 'question'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=4, decimal_places=3)

    def __str__(self) -> str:
        return self.text
    
    class Meta:
        managed = True
        db_table = 'option'

class Result(models.Model):
    session_id = models.CharField(max_length=20, blank=True, null=True)
    #quesion = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_id = models.ForeignKey(Option, on_delete=models.CASCADE)
    sequence_id = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.session_id

    class Meta:
        managed = True
        db_table = 'result'

class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        managed = True
        db_table = 'user'

class Session(models.Model):
    uid = models.CharField(max_length=200)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.uid
    
    class Meta:
        managed = True
        db_table = 'session'

