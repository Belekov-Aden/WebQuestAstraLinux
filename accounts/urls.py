from django.urls import path

from . import views

urlpatterns = [
    path('', views.presentation, name='home'),
    path('sec_page/', views.sec_page, name='sec_page'),
    path('signup/', views.register, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
