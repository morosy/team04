# backend/register_user_id/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.register_user_id, name='register_user_id'),
    # (通常はもう少し具体的なパスを付けます)
    path('', views.register_user_id, name='register_user_id_main'),
]