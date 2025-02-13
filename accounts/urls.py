from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.register, name='signup'),
    # path('login/', ..., name='login'),
    # path('logout/', ..., name='logout'),
]
