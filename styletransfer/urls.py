from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.index, name='index'),
    path('predict/source/<int:sid>/reference/<int:rid>', views.predict, name='predict'),
]