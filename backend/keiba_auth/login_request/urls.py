from django.urls import path
from . import views

app_name = 'login_request'
urlpatterns = [
    # ログインフォームからのPOSTリクエストを受け取るURL
    path('process/', views.login_process_view, name='process_login'),
    # ログアウトのURL
    path('logout/', views.user_logout, name='logout'),
]