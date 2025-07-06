# backend/keiba_auth/login_request/apps.py

from django.apps import AppConfig


class LoginRequestConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'keiba_auth.login_request'