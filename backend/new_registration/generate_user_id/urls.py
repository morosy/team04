# backend/generate_user_id/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 設計書の関数名 New_registration_request_Main に合わせて、パスを空に設定
    path('', views.generate_user_id_main, name='generate_user_id_main'),
]