from django.urls import path

from . import views

urlpatterns = [
    path('', views.presentation, name='home'),
    path('sec_page/', views.sec_page, name='sec_page'),
    path('seven_levels/', views.seven_levels, name='seven_levels'),
    path('maps/', views.map, name='map'),
    path('stage_one_main/', views.stage_one_main, name='stage_one_main'),
    path('stage_one_task/', views.stage_one_task, name='stage_one_task'),
    path('terminal/', views.terminal_view, name='terminal'),
    path('stage_four/', views.stage_four, name='stage_four'),
    path('stage_five_main/', views.stage_five_main, name='stage_five_main'),
    path('stage_three_main/', views.stage_three_main, name='stage_three_main'),
    path('stage_six/', views.stage_six, name='stage_six'),
    path('stage_seven/', views.stage_seven, name='stage_seven'),
    path('stage_seven_terminal/', views.stage_seven_terminal, name='stage_seven_terminal'),
    path('stage_seven_conf/', views.stage_seven_conf, name='stage_seven_conf'),
    path("save_quiz_result_one/", views.save_quiz_result, name="save_quiz_result"),
    path('save_quiz_result_two/', views.save_quiz_result_two, name='save_quiz_result_two'),
    path('save_quiz_result_five/', views.save_quiz_result_five, name='save_quiz_result_five'),
    path('signup/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
