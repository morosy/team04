# backend/register_user_id/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.register_user_id, name='register_user_id'),
    # 設計書に「関数名: Register_user_ID_Main」とあるので、パスを空にして直接このビューを呼ぶようにしてみます。
    # (通常はもう少し具体的なパスを付けます)
    path('', views.register_user_id, name='register_user_id_main'),
]