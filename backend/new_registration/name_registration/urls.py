# backend/name_registration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # モジュール名 name_registration_Main に合わせて、パスを設定
    path('register/', views.name_registration_main, name='name_registration_main'),
    path('', views.registration_form_view, name='registration_form_view'),
]