# backend/confirm_registration/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 設計書の関数名 New_name_registration_request_Main に合わせて、パスを空に設定
    path('', views.confirm_registration_main, name='confirm_registration_main'),
]