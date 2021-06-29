from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('style', views.get_style, name='get_style'),
    path('predict', views.predict, name='predict'),
    path('predict/demo', views.predict_demo, name='predict_demo'),
    path('predict/source/<int:sid>/reference/<int:rid>', views.predict_using_local, name='predict_using_local'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)