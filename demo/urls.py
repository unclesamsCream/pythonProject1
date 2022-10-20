from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),
    path('world_map', views.world_map)
]