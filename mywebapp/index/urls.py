from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    
  path( '', views.index,name="index" ),
]