# backend/register_name/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # editor: Shunsuke MOROZUMI
    # Date: 2025/07/03
    # Usage: ログインフォームを表示するビュー関数を指定するURLパターン
    # Note: このコメントアウトを[''']三重引用符で囲むと、DjangoのURLパターンとして認識されなくなる
    path('', views.login_form, name='login'),
    # path('', views.login_form, name='login_form'), # 例: /login/ にアクセスすると表示
]