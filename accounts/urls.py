from django.urls import path

from . import views

urlpatterns = [
    path('', views.presentation, name='home'),
    path('sec_page/', views.sec_page, name='sec_page'),
    path('seven_levels/', views.seven_levels, name='seven_levels'),
    path('maps/', views.map, name='map'),
    path('stage_one_main/', views.stage_one_main, name='stage_one_main'),
    path('stage_one_task/', views.stage_one_task, name='stage_one_task'),
    path('signup/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
