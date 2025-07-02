# backend/confirm_registration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.confirm_registration_main, name='confirm_registration_main'),
]