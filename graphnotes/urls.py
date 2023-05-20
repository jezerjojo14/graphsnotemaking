from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="index"),
    path('open_paper', views.open_paper, name="open_paper"),
]