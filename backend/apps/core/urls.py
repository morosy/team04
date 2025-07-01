from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ranking/', views.ranking_view, name='ranking'),
    path('friend/registration/', views.friend_registration_view, name='friend_registration'),
    path('friend/request/', views.friend_request_view, name='friend_request'),
    path('friend/accept/', views.friend_accept_view, name='friend_accept'),
    path('friend/decline/', views.friend_decline_view, name='friend_decline'),
]


