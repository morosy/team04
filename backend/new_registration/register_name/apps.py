from django.apps import AppConfig


class RegisterNameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # 'settings.INSTALLED_APPS' で指定された新しいパスと一致させる
    name = 'new_registration.register_name' 