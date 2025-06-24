# backend/register_name/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 設計書の関数名 register_name_Main に合わせて、パスを空に設定
    path('', views.register_name_main, name='register_name_main'),
]