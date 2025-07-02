"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from apps.core import views

# 新規登録モジュールで使用
from new_registration.generate_user_id.views import generate_user_id_main
from new_registration.register_name.views import register_name_main

# ログアウトモジュールで使用
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    #新規登録モジュールで使用
    path('api/user-registration/', include('new_registration.register_user_id.urls')),
    path('api/register-credentials/', include('new_registration.register_name.urls')),
    path('api/generate-user-id/', include('new_registration.generate_user_id.urls')),
    path('api/confirm-registration/', include('new_registration.confirm_registration.urls')),
    path('new-registration/', include('new_registration.name_registration.urls')),

    #　ログインモジュールで使用
    path('login/', include('keiba_auth.login_ui.urls')),
    path('api/login/', include('keiba_auth.login_request.urls')),

    # ログアウトモジュールで使用
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # path('logout/', LogoutViewAllowGet.as_view(next_page='login'), name='logout'),



    # mypageのURL
    path('', views.home, name='home'),
    path('mypage/', views.mypage, name='mypage'),

    # user_resultのURL
    path('user_result/<str:user_id>/', views.user_result, name='user_result'),

    # ランキングページへのリンク対応
    path('ranking/', views.ranking, name='ranking'),

    # マイページへのリンク対応
    path('mypage/', views.mypage, name='mypage'),

    # ユーザー結果ページへのリンク対応
    path('user_result/<str:user_id>/', views.user_result, name='user_result'),

]
