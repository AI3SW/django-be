from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict', views.predict, name='predict'),
    path('predict/demo', views.predict_demo, name='predict_demo'),
    path('predict/source/<int:sid>/reference/<int:rid>', views.predict_using_local, name='predict_using_local'),
]