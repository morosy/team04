from django.urls import path
from . import views


urlpatterns = [
    # ホームへ戻る などのリンク対応
    path('', views.home, name='home'),
]


