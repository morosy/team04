# backend/register_name/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_form, name='login_form'), # 例: /login/ にアクセスすると表示
]