from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index ,name = 'index'),
    path('ver1', views.ver1, name = 'ver1'),
    path('ver2', views.ver2, name = 'ver2'),
    path('index_name', views.post, name = 'index_name'),
    path('results', views.musical_recommend, name = 'results'),
]