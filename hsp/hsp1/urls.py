from django.urls import path 
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',index,name='index'),
     path('form/<uuid:uid>/', views.form, name='form'),
    path('room/',room,name='room'),
    path('resturent/',resturent,name='resturent'),
    path('contact/',contact,name='contact'),
    path('success/',success,name='success'),
   

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)