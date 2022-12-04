from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.index),
    path('emaillog', views.emaillog),
    path('contacts', views.contacts),
    path('prices', views.prices),
]