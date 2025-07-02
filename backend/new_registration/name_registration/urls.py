# backend/name_registration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.name_registration_main, name='name_registration_main'),
    path('', views.registration_form_view, name='registration_form_view'),
]