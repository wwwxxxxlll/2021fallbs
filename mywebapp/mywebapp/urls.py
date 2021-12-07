"""mywebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from index import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles

urlpatterns = [
    path('pub_video',include('index.urls')),
    path('pub_pic',views.pub_pic),
    path('upload',views.upload),
    path('home',views.home),
    path('reg',views.reg),
    path('register',views.register),
    path('sign_in',views.sign_in),
    path('signin',views.signin),
    path('log_out',views.log_out),
    path('act',views.act),
    path('admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
