from django.urls import path

from . import views

urlpatterns = [
    path('polls', views.index, name='index'),
    path('questions', views.get_questions, name='get_questions'),
    path('result', views.post_result, name='post_result'),
]