from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# コアビュー
from apps.core import views as core_views

# ログイン関連
from keiba_auth.login_request import views as login_views

urlpatterns = [
    # 管理画面
    path('admin/', admin.site.urls),

    # 初期画面 → login_form（トップ画面をこれに固定）
    path('', login_views.login_form, name='login_form'),

    # --- 認証関連 ---
    path('login/', include('keiba_auth.login_ui.urls')),  # フロント用UI
    path('api/login/', include('keiba_auth.login_request.urls')),  # 認証処理API
    path('logout/', auth_views.LogoutView.as_view(next_page='login_form'), name='logout'),

    # --- 新規登録 ---
    path('api/user-registration/', include('new_registration.register_user_id.urls')),
    path('api/register-credentials/', include('new_registration.register_name.urls')),
    path('api/generate-user-id/', include('new_registration.generate_user_id.urls')),
    path('api/confirm-registration/', include('new_registration.confirm_registration.urls')),
    path('new-registration/', include('new_registration.name_registration.urls')),

    # --- アプリコア ---
    path('friend-registration/', core_views.friend_registration_view, name='friend_registration'),
    path('friend-request/', core_views.friend_request_view, name='friend_request'),
    path('friend-accept/', core_views.friend_accept_view, name='friend_accept'),
    path('home/', core_views.home, name='home'),
    path('mypage/', core_views.mypage, name='mypage'),
    path('user_result/<int:user_id>/', core_views.user_result, name='user_result'),
    path('ranking/', core_views.ranking_view, name='ranking'),
]
