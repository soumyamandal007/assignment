from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.get_weather),
    path('pollution/', views.get_pollution),
]