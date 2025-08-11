from django.contrib import admin
from django.urls import path
from core import views as views

urlpatterns = [
    path('', views.index, name="home"),
]