from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index ,name = 'index'),
    path('index_name', views.post, name = 'index_name'),
    path('results', views.musical_recommend, name = 'results'),
]