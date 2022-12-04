from django.urls import path, include
from .import views

urlpatterns = [
    path('link', views.link),
    path('touch/<str:uid>', views.touch),
]