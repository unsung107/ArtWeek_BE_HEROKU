from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update),
    path('getArt/', views.getArt),
]
