from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('update/<int:weeks>/', views.update),
    path('getArt/', views.getArt),
]
