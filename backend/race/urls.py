from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('select_ticket/', views.select_ticket, name='select_ticket'),
    path('display_race1/', views.display_race1, name='display_race1'),
    path('display_race2/', views.display_race2, name='display_race2'),
    path('start_race/', views.start_race, name='start_race'),
    path('submit_race1/', views.submit_race1, name='submit_race1'),
    path('submit_race2/', views.submit_race2, name='submit_race2'),
]
