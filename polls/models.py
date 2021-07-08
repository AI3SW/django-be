# Create your models here.
from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self) -> str:
        return self.question_text


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    weight = models.DecimalField(max_digits=4, decimal_places=3)

    def __str__(self) -> str:
        return self.text

class Result(models.Model):
    session_id = models.CharField(max_length=20, blank=True, null=True)
    #quesion = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_id = models.ForeignKey(Option, on_delete=models.CASCADE)
    sequence_id = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.session_id