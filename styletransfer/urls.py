from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('style', views.get_style, name='get_style'),
    path('predict', views.predict, name='predict'),
    path('predict/stargan/demo', views.predict_stargan_demo, name='predict_stargan_demo'),
    path('predict/simswap/demo', views.predict_simswap_demo, name='predict_simswap_demo'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)