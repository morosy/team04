# backend/generate_user_id/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_user_id_main, name='generate_user_id_main'),
]